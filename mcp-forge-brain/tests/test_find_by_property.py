"""Tests find_by_property — Dataview-equivalent query frontmatter for LLMs."""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


@pytest.fixture
def vault_with_props(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    notes = {
        "alpha.md": """---
aliases: ["a"]
tags: ["#t"]
type: erreur
derniere-maj: 2026-05-20
statut: actif
---
body
""",
        "bravo.md": """---
aliases: ["b"]
tags: ["#t"]
type: erreur
derniere-maj: 2026-05-23
---
body
""",
        "charlie.md": """---
aliases: ["c"]
tags: ["#t"]
type: technique
derniere-maj: 2026-04-01
statut: doublon
canonique: "[[alpha]]"
---
body
""",
        "delta.md": """---
aliases: ["d"]
tags: ["#t"]
type: leader
derniere-maj: 2026-05-24
sources: ["https://x.com/foo"]
---
body
""",
        "echo.md": """---
aliases: ["e"]
tags: ["#t"]
type: leader
derniere-maj: 2026-05-24
sources: []
---
body
""",
    }
    for name, content in notes.items():
        (vault / name).write_text(content, encoding="utf-8")
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for name, content in notes.items():
        p = vault / name
        db.index_note(parse_note(p.stem, name, content), p.stat().st_mtime)
    return BrainTools(db, vault)


def test_eq_simple(vault_with_props):
    result = vault_with_props.find_by_property("type", "erreur")
    assert "alpha" in result
    assert "bravo" in result
    assert "charlie" not in result


def test_lt_dates(vault_with_props):
    result = vault_with_props.find_by_property("derniere-maj", "2026-05-22", "lt")
    assert "alpha" in result
    assert "charlie" in result
    assert "bravo" not in result


def test_gt_dates(vault_with_props):
    result = vault_with_props.find_by_property("derniere-maj", "2026-05-23", "gt")
    assert "delta" in result
    assert "echo" in result
    assert "bravo" not in result


def test_ne(vault_with_props):
    result = vault_with_props.find_by_property("type", "erreur", "ne")
    assert "alpha" not in result
    assert "bravo" not in result
    assert "charlie" in result


def test_contains(vault_with_props):
    result = vault_with_props.find_by_property("statut", "doub", "contains")
    assert "charlie" in result
    assert "alpha" not in result


def test_missing(vault_with_props):
    result = vault_with_props.find_by_property("statut", comparator="missing")
    assert "bravo" in result
    assert "delta" in result
    assert "echo" in result
    assert "alpha" not in result
    assert "charlie" not in result


def test_present(vault_with_props):
    result = vault_with_props.find_by_property("canonique", comparator="present")
    # Only charlie has the 'canonique' property set
    assert "[[charlie]]" in result
    assert "[[bravo]]" not in result
    assert "[[delta]]" not in result


def test_sources_empty_list_treated_as_missing(vault_with_props):
    result = vault_with_props.find_by_property("sources", comparator="missing")
    assert "echo" in result
    assert "delta" not in result


def test_no_match_returns_empty_msg(vault_with_props):
    result = vault_with_props.find_by_property("type", "nonexistent")
    assert "Aucune note" in result


def test_invalid_comparator(vault_with_props):
    result = vault_with_props.find_by_property("type", "x", "invalid")
    assert "REFUS" in result


def test_limit_respected(vault_with_props):
    result = vault_with_props.find_by_property("type", "leader", limit=1)
    assert result.count("- [[") == 1
