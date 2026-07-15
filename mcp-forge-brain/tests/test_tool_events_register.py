"""Exercises register_tools for search_tool_events via a real FastMCP instance.

Constructing BrainTools directly and calling .search_tool_events() does NOT
exercise register_tools (the @_tool wrapper, arg schema, MCP dispatch). These
tests build a real FastMCP app and call through call_tool/_list_tools, exactly
like test_write_by_path.py does for the *_by_path tools, without binding a port.

Run: py -m pytest tests/test_tool_events_register.py -v
"""

import asyncio
import json

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.tool_events_db import ToolEventsDB
from src.tools.brain import BrainTools, register_tools


def _live_tools(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    tevt_db = ToolEventsDB(db._conn)  # noqa: SLF001 — mirrors server.py wiring
    tevt_db.create_schema()
    return BrainTools(db, vault, git_sync=None, sessions_db=None, tool_events_db=tevt_db), tevt_db


def _tool_use(tool_id, name, input_value, ts="2026-05-20T10:00:00Z", sid="sess-1"):
    return {
        "type": "assistant", "sessionId": sid, "timestamp": ts,
        "message": {"content": [{"type": "tool_use", "id": tool_id, "name": name, "input": input_value}]},
    }


def _tool_result(tool_use_id, content, is_error=None, ts="2026-05-20T10:00:01Z", sid="sess-1"):
    block = {"type": "tool_result", "tool_use_id": tool_use_id, "content": content}
    if is_error is not None:
        block["is_error"] = is_error
    return {"type": "user", "sessionId": sid, "timestamp": ts, "message": {"content": [block]}}


def test_register_tools_exposes_search_tool_events():
    """search_tool_events must be on the MCP tool registry."""
    from fastmcp import FastMCP

    class _Stub:
        def __getattr__(self, _name):
            return lambda *a, **k: ""

    mcp = FastMCP(name="forge-brain-test")
    register_tools(mcp, _Stub())
    names = {t.name for t in asyncio.run(mcp._list_tools())}
    assert "search_tool_events" in names


def test_search_tool_events_disabled_via_call_tool(tmp_path):
    """When tool_events_db is None (feature disabled), the wrapper returns the disabled message."""
    from fastmcp import FastMCP

    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    tools = BrainTools(db, vault, git_sync=None, sessions_db=None, tool_events_db=None)

    mcp = FastMCP(name="forge-brain-test")
    register_tools(mcp, tools)
    result = asyncio.run(mcp.call_tool("search_tool_events", {"query": "anything"}))
    assert "desactivee" in result.structured_content["result"]


def test_search_tool_events_end_to_end_via_call_tool(tmp_path):
    """Full path: index a transcript, call the MCP tool, get back a real result."""
    from fastmcp import FastMCP

    tools, tevt_db = _live_tools(tmp_path)
    t = tmp_path / "a.jsonl"
    t.write_text("\n".join(json.dumps(m) for m in [
        _tool_use("tu1", "Bash", {"command": "git status"}),
        _tool_result("tu1", "Error: permission denied", is_error=True),
    ]), encoding="utf-8")
    tevt_db.index_transcript(str(t), "claude-forge", 1.0)

    mcp = FastMCP(name="forge-brain-test")
    register_tools(mcp, tools)
    result = asyncio.run(
        mcp.call_tool("search_tool_events", {"query": "", "is_error": "true", "limit": 10})
    )
    text = result.structured_content["result"]
    assert "Bash" in text
    assert "ERROR" in text


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
