"""Tests for parse_transcript (tool_events) — robustness on real and malformed JSONL.

Mirrors test_sessions_indexer.py: transcripts are external data, the parser must
never raise on bad input. Adverse cases dominate.

Run: py -m pytest tests/test_tool_events_indexer.py -v
"""

import json

import pytest

from src.tool_events_indexer import parse_transcript


def _write(tmp_path, name, lines):
    p = tmp_path / name
    out = [line if isinstance(line, str) else json.dumps(line) for line in lines]
    p.write_text("\n".join(out), encoding="utf-8")
    return str(p)


def _tool_use(tool_id, name, input_value, ts="2026-05-20T10:00:00Z", sid="sess-1"):
    return {
        "type": "assistant",
        "sessionId": sid,
        "timestamp": ts,
        "message": {"content": [{"type": "tool_use", "id": tool_id, "name": name, "input": input_value}]},
    }


def _tool_result(tool_use_id, content, is_error=None, ts="2026-05-20T10:00:01Z", sid="sess-1"):
    block = {"type": "tool_result", "tool_use_id": tool_use_id, "content": content}
    if is_error is not None:
        block["is_error"] = is_error
    return {
        "type": "user",
        "sessionId": sid,
        "timestamp": ts,
        "message": {"content": [block]},
    }


# ===========================================================================
# HAPPY PATH
# ===========================================================================

def test_parses_tool_use_and_result(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "ls -la"}),
        _tool_result("tu1", "total 0\ndrwxr-xr-x"),
    ])
    events = parse_transcript(path, "claude-forge")
    assert len(events) == 2
    assert events[0].event_kind == "tool_use"
    assert events[0].tool_name == "Bash"
    assert "ls -la" in events[0].text
    assert events[1].event_kind == "tool_result"
    assert events[1].project == "claude-forge"


def test_tool_result_inherits_tool_name_from_pairing(tmp_path):
    """tool_result carries tool_use_id, not a name — must resolve via forward pairing."""
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Edit", {"file_path": "/foo/bar.py"}),
        _tool_result("tu1", "Edited successfully"),
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert result.tool_name == "Edit"


def test_salient_field_extracted_for_known_tools(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "git status", "description": "check status"}),
    ])
    events = parse_transcript(path, "p")
    assert events[0].text == "git status"


def test_unknown_tool_input_dumped_as_json(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "mcp__forge-brain__search_brain", {"query": "hello", "limit": 5}),
    ])
    events = parse_transcript(path, "p")
    assert "hello" in events[0].text


# ===========================================================================
# is_error — native field vs heuristic fallback
# ===========================================================================

def test_is_error_native_true(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "false"}),
        _tool_result("tu1", "command not found", is_error=True),
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert result.is_error is True


def test_is_error_native_false_even_with_error_keyword(tmp_path):
    """Native is_error=False must win over the keyword heuristic (authoritative)."""
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Read", {"file_path": "/x"}),
        _tool_result("tu1", "no error found in this file, all good", is_error=False),
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert result.is_error is False


def test_is_error_heuristic_fallback_when_absent(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "rm /nope"}),
        _tool_result("tu1", "Error: file not found"),  # no is_error field
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert result.is_error is True


def test_is_error_heuristic_false_when_no_keyword(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "ls"}),
        _tool_result("tu1", "file1.txt file2.txt"),  # no is_error field, no keyword
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert result.is_error is False


def test_tool_use_is_error_always_none(tmp_path):
    """tool_use blocks never carry is_error — only tool_result does."""
    path = _write(tmp_path, "t.jsonl", [_tool_use("tu1", "Bash", {"command": "ls"})])
    events = parse_transcript(path, "p")
    assert events[0].is_error is None


# ===========================================================================
# content shape — str vs list of blocks
# ===========================================================================

def test_tool_result_content_as_list_of_text_blocks(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Agent", {"subagent_type": "explore"}),
        _tool_result("tu1", [{"type": "text", "text": "agent finished successfully"}]),
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert "agent finished" in result.text


def test_tool_result_content_list_with_tool_reference_dropped(tmp_path):
    """tool_reference blocks (observed in real transcripts) carry no text — dropped."""
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "TaskCreate", {}),
        _tool_result("tu1", [{"type": "tool_reference", "tool_name": "WebFetch"}]),
    ])
    events = parse_transcript(path, "p")
    # No text block -> nothing indexable for this tool_result
    assert not any(e.event_kind == "tool_result" for e in events)


def test_tool_result_empty_content_skipped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "true"}),
        _tool_result("tu1", ""),
    ])
    events = parse_transcript(path, "p")
    assert not any(e.event_kind == "tool_result" for e in events)


# ===========================================================================
# truncation — never index a full file blob
# ===========================================================================

def test_large_input_truncated(tmp_path):
    huge_content = "x" * 5000
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Write", {"file_path": "/f.py", "content": huge_content}),
    ])
    events = parse_transcript(path, "p")
    # salient field is only file_path for Write -> short text, huge content never surfaces
    assert len(events[0].text) < 600
    assert "xxxx" not in events[0].text or len(events[0].text) <= 500


def test_large_result_text_truncated(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        _tool_use("tu1", "Bash", {"command": "cat bigfile"}),
        _tool_result("tu1", "y" * 5000),
    ])
    events = parse_transcript(path, "p")
    result = [e for e in events if e.event_kind == "tool_result"][0]
    assert len(result.text) <= 500


# ===========================================================================
# ROBUSTNESS — malformed input must never raise
# ===========================================================================

def test_malformed_json_lines_skipped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        "{ not valid json",
        _tool_use("tu1", "Bash", {"command": "ls"}),
        "null",
        "[1,2,3]",
    ])
    events = parse_transcript(path, "p")
    assert len(events) == 1


def test_empty_file(tmp_path):
    path = _write(tmp_path, "t.jsonl", [])
    assert parse_transcript(path, "p") == []


def test_tool_result_without_tool_use_id_field(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "user", "sessionId": "s", "message": {"content": [
            {"type": "tool_result", "content": "orphan result, no tool_use_id at all"}
        ]}},
    ])
    events = parse_transcript(path, "p")
    assert len(events) == 1
    assert events[0].tool_name == ""


def test_tool_use_without_name_skipped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "assistant", "sessionId": "s", "message": {"content": [
            {"type": "tool_use", "id": "tu1", "input": {}}
        ]}},
    ])
    assert parse_transcript(path, "p") == []


def test_message_content_not_list_skipped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "assistant", "sessionId": "s", "message": {"content": "plain string content"}},
    ])
    assert parse_transcript(path, "p") == []


def test_message_missing_or_wrong_type(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "assistant", "message": "not a dict"},
        {"type": "assistant", "message": None},
        {"type": "assistant"},
    ])
    assert parse_transcript(path, "p") == []


def test_nonexistent_file_returns_empty(tmp_path):
    assert parse_transcript(str(tmp_path / "nope.jsonl"), "p") == []


def test_non_dict_block_in_content_skipped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "assistant", "sessionId": "s", "message": {"content": [
            "not a dict block",
            {"type": "tool_use", "id": "tu1", "name": "Bash", "input": {"command": "ls"}},
        ]}},
    ])
    events = parse_transcript(path, "p")
    assert len(events) == 1


def test_fallback_to_agent_id_when_no_session(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "assistant", "agentId": "agent-xyz", "message": {"content": [
            {"type": "tool_use", "id": "tu1", "name": "Bash", "input": {"command": "ls"}}
        ]}},
    ])
    events = parse_transcript(path, "p")
    assert events[0].session_id == "agent-xyz"


def test_other_message_types_dropped(tmp_path):
    path = _write(tmp_path, "t.jsonl", [
        {"type": "system", "message": {"content": [
            {"type": "tool_use", "id": "tu1", "name": "Bash", "input": {"command": "ls"}}
        ]}},
    ])
    assert parse_transcript(path, "p") == []


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
