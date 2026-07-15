"""Tests for ToolEventsDB.search and ToolEventsWatcher — FTS5 over tool events.

Mirrors test_sessions_search.py. Key divergence: an empty query with filters
must return rows (filter-only is the central use case), unlike SessionDB where
an empty query is meaningless.

Run: py -m pytest tests/test_tool_events_search.py -v
"""

import json
import sqlite3

import pytest

from src.tool_events_db import ToolEventsDB
from src.tool_events_watcher import ToolEventsWatcher


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    tdb = ToolEventsDB(conn)
    tdb.create_schema()
    return tdb


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


def _transcript(tmp_path, name, msgs):
    p = tmp_path / name
    p.write_text("\n".join(json.dumps(m) for m in msgs), encoding="utf-8")
    return str(p)


@pytest.fixture
def populated(db, tmp_path):
    """Two transcripts, two projects, mix of tool_use/tool_result and errors."""
    t1 = _transcript(tmp_path, "a.jsonl", [
        _tool_use("tu1", "Bash", {"command": "git status"}, ts="2026-05-20T09:00:00Z", sid="s-a"),
        _tool_result("tu1", "nothing to commit", is_error=False, ts="2026-05-20T09:00:01Z", sid="s-a"),
        _tool_use("tu2", "Edit", {"file_path": "/x.py"}, ts="2026-05-20T09:01:00Z", sid="s-a"),
        _tool_result("tu2", "Error: permission denied writing file", is_error=True,
                     ts="2026-05-20T09:01:01Z", sid="s-a"),
    ])
    t2 = _transcript(tmp_path, "b.jsonl", [
        _tool_use("tu3", "Bash", {"command": "npm test"}, ts="2026-05-25T14:00:00Z", sid="s-b"),
        _tool_result("tu3", "42 tests passed", is_error=False, ts="2026-05-25T14:00:01Z", sid="s-b"),
    ])
    db.index_transcript(t1, "claude-forge", 1000.0)
    db.index_transcript(t2, "ia-back", 2000.0)
    return db


# ===========================================================================
# HAPPY PATH — text search
# ===========================================================================

def test_finds_content(populated):
    rows = populated.search("permission", limit=10)
    assert any("permission" in r["snippet"].lower() for r in rows)


def test_result_shape(populated):
    rows = populated.search("git", limit=10)
    assert rows
    for r in rows:
        for k in ("session_id", "project", "event_kind", "tool_name", "is_error", "timestamp", "path", "snippet", "score"):
            assert k in r


def test_search_matches_tool_name_field(populated):
    rows = populated.search("Bash", limit=10)
    assert rows


# ===========================================================================
# FILTER-ONLY — empty query, central use case
# ===========================================================================

def test_empty_query_with_is_error_filter_returns_rows(populated):
    """The whole point of this source: 'all errors', no text term at all."""
    rows = populated.search("", limit=10, is_error=True)
    assert rows
    assert all(r["is_error"] == 1 for r in rows)


def test_empty_query_with_tool_name_filter_returns_rows(populated):
    rows = populated.search("", limit=10, tool_name="Bash")
    assert rows
    assert all(r["tool_name"] == "Bash" for r in rows)


def test_empty_query_no_filters_returns_all(populated):
    rows = populated.search("", limit=100)
    assert len(rows) == 6  # 3 tool_use + 3 tool_result across both transcripts


def test_is_error_false_filters_correctly(populated):
    rows = populated.search("", limit=100, is_error=False)
    assert rows
    assert all(r["is_error"] == 0 for r in rows)


def test_is_error_none_means_no_filter(populated):
    """is_error=None (default) must not filter — distinct from is_error=False."""
    rows_none = populated.search("", limit=100)
    rows_explicit_false = populated.search("", limit=100, is_error=False)
    assert len(rows_none) > len(rows_explicit_false)


# ===========================================================================
# FILTERS combined with text
# ===========================================================================

def test_filter_by_project(populated):
    rows = populated.search("npm", limit=10, project="ia-back")
    assert rows
    assert all(r["project"] == "ia-back" for r in rows)


def test_filter_by_project_excludes_others(populated):
    rows = populated.search("permission", limit=10, project="ia-back")
    assert rows == []


def test_filter_by_event_kind(populated):
    rows = populated.search("Bash", limit=10, event_kind="tool_use")
    assert rows
    assert all(r["event_kind"] == "tool_use" for r in rows)


def test_filter_since(populated):
    rows = populated.search("test", limit=10, since="2026-05-23")
    assert rows
    assert all(r["timestamp"] >= "2026-05-23" for r in rows)


def test_filter_nonexistent_project(populated):
    assert populated.search("git", limit=10, project="does-not-exist") == []


# ===========================================================================
# ADVERSE — injection safety, limits
# ===========================================================================

def test_fts_operators_safe(populated):
    for hostile in ["permission OR", "AND bash", "NEAR(x y)", "* denied", '"unbalanced']:
        rows = populated.search(hostile, limit=10)
        assert isinstance(rows, list)


def test_single_char_terms_dropped_falls_back_to_filter_only(populated):
    """Query of only short terms -> sanitized to empty -> filter-only branch."""
    rows = populated.search("a e i", limit=100)
    assert len(rows) == 6  # same as empty query, no filters


def test_limit_respected(populated):
    rows = populated.search("", limit=1)
    assert len(rows) <= 1


def test_search_empty_db(db):
    assert db.search("anything", limit=10) == []
    assert db.search("", limit=10) == []


# ===========================================================================
# REINDEX / INCREMENTAL
# ===========================================================================

def test_reindex_replaces_not_duplicates(db, tmp_path):
    t = _transcript(tmp_path, "a.jsonl", [
        _tool_use("tu1", "Bash", {"command": "ls"}),
        _tool_result("tu1", "file listing here"),
    ])
    db.index_transcript(t, "p", 1.0)
    n1 = db.stats()["events"]
    db.index_transcript(t, "p", 2.0)
    n2 = db.stats()["events"]
    assert n1 == n2 == 2


def test_delete_path_removes_events(db, tmp_path):
    t = _transcript(tmp_path, "a.jsonl", [_tool_use("tu1", "Bash", {"command": "ls"})])
    db.index_transcript(t, "p", 1.0)
    assert db.stats()["events"] == 1
    db.delete_path(t)
    assert db.stats()["events"] == 0


def test_stats_counts_errors(db, tmp_path):
    t = _transcript(tmp_path, "a.jsonl", [
        _tool_use("tu1", "Bash", {"command": "false"}),
        _tool_result("tu1", "Error: failed", is_error=True),
    ])
    db.index_transcript(t, "p", 1.0)
    stats = db.stats()
    assert stats["events"] == 2
    assert stats["errors"] == 1


# ===========================================================================
# WATCHER — incremental scan, subagent exclusion
# ===========================================================================

def test_watcher_indexes_new_files(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "my-project"
    proj.mkdir(parents=True)
    (proj / "sess.jsonl").write_text(
        json.dumps(_tool_use("tu1", "Bash", {"command": "ls"})), encoding="utf-8",
    )
    w = ToolEventsWatcher(root, db)
    r = w.scan()
    assert r.added == 1
    assert r.events == 1
    assert db.search("", limit=10, project="my-project")


def test_watcher_skips_subagents_by_default(db, tmp_path):
    root = tmp_path / "projects"
    sub = root / "proj" / "uuid-1" / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent.jsonl").write_text(
        json.dumps(_tool_use("tu1", "Bash", {"command": "ls"})), encoding="utf-8",
    )
    w = ToolEventsWatcher(root, db, include_subagents=False)
    r = w.scan()
    assert r.added == 0
    assert db.stats()["events"] == 0


def test_watcher_includes_subagents_when_configured(db, tmp_path):
    root = tmp_path / "projects"
    sub = root / "proj" / "uuid-1" / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent.jsonl").write_text(
        json.dumps(_tool_use("tu1", "Bash", {"command": "ls"})), encoding="utf-8",
    )
    w = ToolEventsWatcher(root, db, include_subagents=True)
    r = w.scan()
    assert r.added == 1


def test_watcher_incremental_no_rescan_on_unchanged(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "proj"
    proj.mkdir(parents=True)
    f = proj / "sess.jsonl"
    f.write_text(json.dumps(_tool_use("tu1", "Bash", {"command": "ls"})), encoding="utf-8")
    w = ToolEventsWatcher(root, db)
    w.scan()
    r2 = w.scan()
    assert r2.added == 0
    assert r2.modified == 0


def test_watcher_deletes_vanished(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "proj"
    proj.mkdir(parents=True)
    f = proj / "sess.jsonl"
    f.write_text(json.dumps(_tool_use("tu1", "Bash", {"command": "ls"})), encoding="utf-8")
    w = ToolEventsWatcher(root, db)
    w.scan()
    assert db.stats()["events"] == 1
    f.unlink()
    r = w.scan()
    assert r.deleted == 1
    assert db.stats()["events"] == 0


def test_watcher_missing_root_is_safe(db, tmp_path):
    w = ToolEventsWatcher(tmp_path / "does-not-exist", db)
    r = w.scan()
    assert r.added == 0


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
