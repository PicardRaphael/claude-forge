#!/usr/bin/env python3
"""Functional tests for metrics-tracker.py (PostToolUse advisory logger).

SCOPE: metrics-tracker is a NON-blocking, fail-open advisory logger. It logs
I/O size proxies to JSONL. These tests verify the log format, fail-open
behavior on bad input, and write-permission errors.

Run: py -m pytest tests/test_metrics_tracker.py -v
"""
import importlib.util
import io
import json
import os
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "metrics-tracker.py",
)
_spec = importlib.util.spec_from_file_location("metrics_tracker", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _run_hook(stdin_data: str, monkeypatch, tmp_path):
    """Run main() with the given stdin string, metrics dir patched to tmp_path."""
    monkeypatch.setattr(_mod, "METRICS_DIR", str(tmp_path))
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin_data))
    with __import__("pytest").raises(SystemExit) as exc:
        _mod.main()
    return exc.value.code


# ===========================================================================
# Nominal
# ===========================================================================

def test_log_normal(tmp_path, monkeypatch):
    """Valid Read stdin → 1 JSONL line written with all required fields."""
    payload = json.dumps({
        "session_id": "abc123",
        "tool_name": "Read",
        "tool_input": {"file_path": "/some/file.py"},
        "tool_response": "line1\nline2\n",
        "cwd": str(tmp_path),
    })
    exit_code = _run_hook(payload, monkeypatch, tmp_path)
    assert exit_code == 0

    import glob
    files = glob.glob(str(tmp_path / "*.jsonl"))
    assert len(files) == 1
    with open(files[0], encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["session_id"] == "abc123"
    assert record["tool"] == "Read"
    assert isinstance(record["input_chars"], int) and record["input_chars"] > 0
    assert isinstance(record["output_chars"], int) and record["output_chars"] > 0
    assert isinstance(record["estimated_tokens"], int)
    assert "ts" in record


def test_log_mcp_tool(tmp_path, monkeypatch):
    """MCP tool name with full path logged correctly."""
    payload = json.dumps({
        "session_id": "mcp_session",
        "tool_name": "mcp__forge-brain__read_note",
        "tool_input": {"file": "comment-creer-hook"},
        "tool_response": {"content": "some vault content"},
        "cwd": str(tmp_path),
    })
    exit_code = _run_hook(payload, monkeypatch, tmp_path)
    assert exit_code == 0

    import glob
    files = glob.glob(str(tmp_path / "*.jsonl"))
    assert len(files) == 1
    with open(files[0], encoding="utf-8") as f:
        record = json.loads(f.readline())
    assert record["tool"] == "mcp__forge-brain__read_note"
    assert record["estimated_tokens"] > 0


# ===========================================================================
# Adversarial — fail-open
# ===========================================================================

def test_stdin_absent(tmp_path, monkeypatch):
    """Empty stdin → exit 0, no file written."""
    exit_code = _run_hook("", monkeypatch, tmp_path)
    assert exit_code == 0
    import glob
    assert glob.glob(str(tmp_path / "*.jsonl")) == []


def test_json_malformed(tmp_path, monkeypatch):
    """Malformed JSON stdin → exit 0, no file written."""
    exit_code = _run_hook("not json{", monkeypatch, tmp_path)
    assert exit_code == 0
    import glob
    assert glob.glob(str(tmp_path / "*.jsonl")) == []


def test_write_permission_denied(tmp_path, monkeypatch):
    """OSError on open() → exit 0, no crash (fail-open)."""
    payload = json.dumps({
        "session_id": "s1",
        "tool_name": "Write",
        "tool_input": {"file_path": "x.py"},
        "tool_response": "ok",
        "cwd": str(tmp_path),
    })
    import builtins
    real_open = builtins.open

    def _blocked_open(path, *args, **kwargs):
        if str(path).endswith(".jsonl"):
            raise OSError("Permission denied")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", _blocked_open)
    exit_code = _run_hook(payload, monkeypatch, tmp_path)
    assert exit_code == 0


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
