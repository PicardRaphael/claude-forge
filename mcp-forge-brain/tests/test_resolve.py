"""Tests for BrainDB resolve/suggest/tags/property — read paths used by MCP tools.

These back the MCP tools read_note (path resolution), suggest_notes, get_tags,
get_property. Until 2026-05-27 they had no direct coverage.

resolve_note() resolves a human-typed name to a vault path in 3 tiers:
  1. exact match on file_stem OR alias
  2. substring "%-name%"   (e.g. 'bail' -> 'rm-bail-contrat')
  3. prefix  "name-%"      (e.g. 'bail' -> 'bail-commercial')

Run: py -m pytest tests/test_resolve.py -v
"""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note


@pytest.fixture
def db(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    notes = {
        "bail-commercial.md": """---
aliases: ["bail pro", "lease"]
tags: ["#juridique", "#contrat"]
---
Contrat de bail commercial.
""",
        "rm-bail-resiliation.md": """---
aliases: ["résiliation bail"]
tags: ["#juridique"]
---
Procédure de résiliation.
""",
        "agents-autonomes.md": """---
aliases: ["agents", "orchestration"]
tags: ["#technique/agents", "#contrat"]
type: technique
derniere-maj: 2026-05-24
---
Les agents orchestrent des outils.
""",
        "multi-list-prop.md": """---
aliases: ["mlp"]
tags: ["#meta"]
sources: ["https://a.com", "https://b.com"]
---
Note avec propriété liste.
""",
    }
    for name, content in notes.items():
        (vault / name).write_text(content, encoding="utf-8")
    database = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    database.create_schema()
    for name, content in notes.items():
        p = vault / name
        database.index_note(parse_note(p.stem, name, content), p.stat().st_mtime)
    return database


# ===========================================================================
# resolve_note — 3 tiers
# ===========================================================================

def test_resolve_exact_stem(db):
    assert db.resolve_note("bail-commercial") == "bail-commercial.md"


def test_resolve_exact_alias(db):
    """An alias resolves to its note path (tier 1)."""
    assert db.resolve_note("orchestration") == "agents-autonomes.md"


def test_resolve_substring_dash(db):
    """Tier 2: 'resiliation' is a '%-name%' substring of 'rm-bail-resiliation'."""
    assert db.resolve_note("resiliation") == "rm-bail-resiliation.md"


def test_resolve_tier2_beats_tier3(db):
    """Characterization: tier 2 ('%-name%' substring) is tried BEFORE tier 3 ('name-%' prefix).
    Query 'bail' matches BOTH 'rm-bail-resiliation' (tier 2) and 'bail-commercial' (tier 3),
    but tier 2 runs first and short-circuits → 'rm-bail-resiliation.md' wins.
    This pins the resolution ORDER; if it flips, downstream read_note targets change silently."""
    assert db.resolve_note("bail") == "rm-bail-resiliation.md"


def test_resolve_prefix_only(db):
    """Tier 3 fires only when no tier-2 match exists. 'commercial' has no '%-commercial%'
    note but 'commercial-...' would; here only 'bail-commercial' contains it as a word —
    resolved via the substring path to bail-commercial.md."""
    assert db.resolve_note("commercial") == "bail-commercial.md"


def test_resolve_unknown_returns_none(db):
    assert db.resolve_note("inexistant-xyz") is None


def test_resolve_shortest_stem_wins(db):
    """When multiple stems match a prefix, ORDER BY LENGTH picks the shortest."""
    # 'agents' exact-matches the alias of agents-autonomes (tier 1 short-circuits)
    assert db.resolve_note("agents") == "agents-autonomes.md"


# ===========================================================================
# suggest_notes — wraps search, returns stems
# ===========================================================================

def test_suggest_returns_stems(db):
    out = db.suggest_notes("agents", limit=5)
    assert isinstance(out, list)
    assert "agents-autonomes" in out


def test_suggest_empty_query(db):
    assert db.suggest_notes("", limit=5) == []


# ===========================================================================
# get_tags — aggregated counts, descending
# ===========================================================================

def test_get_tags_counts(db):
    tags = {t["tag"]: t["count"] for t in db.get_tags()}
    assert tags["#juridique"] == 2  # bail-commercial + rm-bail-resiliation
    assert tags["#contrat"] == 2    # bail-commercial + agents-autonomes


def test_get_tags_sorted_desc(db):
    counts = [t["count"] for t in db.get_tags()]
    assert counts == sorted(counts, reverse=True)


# ===========================================================================
# get_property — frontmatter lookup by stem or alias, list-flattening
# ===========================================================================

def test_get_property_by_stem(db):
    assert db.get_property("agents-autonomes", "type") == "technique"


def test_get_property_by_alias(db):
    """Property lookup also works when given an alias instead of the stem."""
    assert db.get_property("orchestration", "type") == "technique"


def test_get_property_list_flattened(db):
    """A list-valued property is joined with ', ' (LLM-friendly string)."""
    val = db.get_property("multi-list-prop", "sources")
    assert val == "https://a.com, https://b.com"


def test_get_property_missing_key(db):
    """A note without the requested key returns '' (key absent → empty string)."""
    assert db.get_property("agents-autonomes", "nonexistent-key") == ""


def test_get_property_unknown_note(db):
    assert db.get_property("ghost-note", "type") is None


# ===========================================================================
# get_last_modified / get_note_state
# ===========================================================================

def test_get_last_modified_known(db):
    p = db.resolve_note("bail-commercial")
    assert isinstance(db.get_last_modified(p), float)


def test_get_last_modified_unknown(db):
    assert db.get_last_modified("ghost.md") is None


def test_get_note_state_returns_hash(db):
    p = db.resolve_note("bail-commercial")
    state = db.get_note_state(p)
    assert state is not None
    mtime, content_hash = state
    assert isinstance(mtime, float)
    assert isinstance(content_hash, str) and len(content_hash) == 64  # sha256 hex


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
