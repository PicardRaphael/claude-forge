"""Tests for SessionDB.search and SessionWatcher — FTS5 over transcripts.

Mirrors test_search.py: deterministic fixture, each filter and edge case
exercised. Search must be FTS-injection-safe and never raise on hostile input.

Run: py -m pytest tests/test_sessions_search.py -v
"""

import json
import sqlite3

import pytest

from src.sessions_db import SessionDB
from src.sessions_watcher import SessionWatcher


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    sdb = SessionDB(conn)
    sdb.create_schema()
    return sdb


def _msg(role, text, ts="2026-05-20T10:00:00Z", sid="sess-1"):
    content = text if role == "user" else [{"type": "text", "text": text}]
    return {"type": role, "sessionId": sid, "timestamp": ts, "message": {"content": content}}


def _transcript(tmp_path, name, msgs):
    p = tmp_path / name
    p.write_text("\n".join(json.dumps(m) for m in msgs), encoding="utf-8")
    return str(p)


@pytest.fixture
def populated(db, tmp_path):
    """Two transcripts in two projects, distinct vocabulary."""
    t1 = _transcript(tmp_path, "a.jsonl", [
        _msg("user", "Comment indexer les transcripts avec une table FTS5 separee",
             ts="2026-05-20T09:00:00Z", sid="s-a"),
        _msg("assistant", "On cree un watcher incremental base sur le mtime des fichiers",
             ts="2026-05-20T09:01:00Z", sid="s-a"),
    ])
    t2 = _transcript(tmp_path, "b.jsonl", [
        _msg("user", "Explique la doctrine des hooks de securite et delegation",
             ts="2026-05-25T14:00:00Z", sid="s-b"),
    ])
    db.index_transcript(t1, "claude-forge", 1000.0)
    db.index_transcript(t2, "ia-back", 2000.0)
    return db


# ===========================================================================
# HAPPY PATH
# ===========================================================================

def test_finds_content(populated):
    rows = populated.search("transcripts", limit=10)
    assert any("transcripts" in r["snippet"].lower() for r in rows)


def test_prefix_match(populated):
    """'index' (prefix of 'indexer') matches via wildcard."""
    rows = populated.search("index", limit=10)
    assert rows


def test_snippet_highlight(populated):
    rows = populated.search("watcher", limit=10)
    assert rows
    assert ">>>" in rows[0]["snippet"]


def test_result_shape(populated):
    rows = populated.search("transcripts", limit=10)
    assert rows
    for r in rows:
        for k in ("session_id", "project", "role", "timestamp", "path", "snippet", "score"):
            assert k in r


# ===========================================================================
# FILTERS
# ===========================================================================

def test_filter_by_project(populated):
    rows = populated.search("doctrine", limit=10, project="ia-back")
    assert rows
    assert all(r["project"] == "ia-back" for r in rows)


def test_filter_by_project_excludes_others(populated):
    rows = populated.search("transcripts", limit=10, project="ia-back")
    assert rows == []  # 'transcripts' only in claude-forge


def test_filter_by_role(populated):
    rows = populated.search("indexer OR watcher OR mtime", limit=10, role="assistant")
    assert rows
    assert all(r["role"] == "assistant" for r in rows)


def test_filter_since(populated):
    """since cutoff drops the 2026-05-20 messages, keeps 2026-05-25."""
    rows = populated.search("doctrine securite transcripts", limit=10, since="2026-05-23")
    assert rows
    assert all(r["timestamp"] >= "2026-05-23" for r in rows)


def test_filter_nonexistent_project(populated):
    assert populated.search("transcripts", limit=10, project="does-not-exist") == []


# ===========================================================================
# ADVERSE — injection safety, empty, limits
# ===========================================================================

def test_empty_query(populated):
    assert populated.search("", limit=10) == []
    assert populated.search("   ", limit=10) == []


def test_fts_operators_safe(populated):
    for hostile in ["transcripts OR", "AND watcher", "NEAR(x y)", "* index", '"unbalanced']:
        rows = populated.search(hostile, limit=10)
        assert isinstance(rows, list)  # never raises


def test_single_char_terms_dropped(populated):
    """Terms of length<=1 are dropped; query of only short terms → empty."""
    assert populated.search("a e i", limit=10) == []


def test_limit_respected(populated):
    rows = populated.search("transcripts watcher mtime doctrine", limit=1)
    assert len(rows) <= 1


def test_search_empty_db(db):
    assert db.search("anything", limit=10) == []


# ===========================================================================
# REINDEX / INCREMENTAL
# ===========================================================================

def test_reindex_replaces_not_duplicates(db, tmp_path):
    t = _transcript(tmp_path, "a.jsonl", [_msg("user", "premiere version du message indexe")])
    db.index_transcript(t, "p", 1.0)
    n1 = db.stats()["messages"]
    # Reindex same path → old rows dropped, not duplicated
    db.index_transcript(t, "p", 2.0)
    n2 = db.stats()["messages"]
    assert n1 == n2 == 1


def test_delete_path_removes_messages(db, tmp_path):
    t = _transcript(tmp_path, "a.jsonl", [_msg("user", "message a supprimer ensuite proprement")])
    db.index_transcript(t, "p", 1.0)
    assert db.stats()["messages"] == 1
    db.delete_path(t)
    assert db.stats()["messages"] == 0
    assert db.search("supprimer", limit=10) == []


# ===========================================================================
# WATCHER — incremental scan, subagent exclusion
# ===========================================================================

def test_watcher_indexes_new_files(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "my-project"
    proj.mkdir(parents=True)
    (proj / "sess.jsonl").write_text(
        json.dumps(_msg("user", "contenu du transcript a indexer par le watcher")),
        encoding="utf-8",
    )
    w = SessionWatcher(root, db)
    r = w.scan()
    assert r.added == 1
    assert r.messages == 1
    assert db.search("transcript", limit=10, project="my-project")


def test_watcher_skips_subagents_by_default(db, tmp_path):
    root = tmp_path / "projects"
    sub = root / "proj" / "uuid-1" / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent.jsonl").write_text(
        json.dumps(_msg("assistant", "raisonnement interne du sous-agent a ignorer")),
        encoding="utf-8",
    )
    w = SessionWatcher(root, db, include_subagents=False)
    r = w.scan()
    assert r.added == 0
    assert db.stats()["messages"] == 0


def test_watcher_includes_subagents_when_configured(db, tmp_path):
    root = tmp_path / "projects"
    sub = root / "proj" / "uuid-1" / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent.jsonl").write_text(
        json.dumps(_msg("assistant", "raisonnement interne du sous-agent a indexer maintenant")),
        encoding="utf-8",
    )
    w = SessionWatcher(root, db, include_subagents=True)
    r = w.scan()
    assert r.added == 1


def test_watcher_incremental_no_rescan_on_unchanged(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "proj"
    proj.mkdir(parents=True)
    f = proj / "sess.jsonl"
    f.write_text(json.dumps(_msg("user", "contenu stable qui ne change pas du tout")),
                 encoding="utf-8")
    w = SessionWatcher(root, db)
    w.scan()
    r2 = w.scan()  # nothing changed
    assert r2.added == 0
    assert r2.modified == 0


def test_watcher_deletes_vanished(db, tmp_path):
    root = tmp_path / "projects"
    proj = root / "proj"
    proj.mkdir(parents=True)
    f = proj / "sess.jsonl"
    f.write_text(json.dumps(_msg("user", "transcript qui va disparaitre du disque bientot")),
                 encoding="utf-8")
    w = SessionWatcher(root, db)
    w.scan()
    assert db.stats()["messages"] == 1
    f.unlink()
    r = w.scan()
    assert r.deleted == 1
    assert db.stats()["messages"] == 0


def test_watcher_missing_root_is_safe(db, tmp_path):
    w = SessionWatcher(tmp_path / "does-not-exist", db)
    r = w.scan()
    assert r.added == 0


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
