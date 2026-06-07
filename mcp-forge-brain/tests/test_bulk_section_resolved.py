"""Tests bulk_update_property, read_section."""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


@pytest.fixture
def vault(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    notes = {
        "alpha.md": """---
aliases: ["a"]
tags: ["#t"]
derniere-maj: 2026-05-01
---

# Alpha

## COMMENT
Content of COMMENT section.
With more text here.

### Sub-detail
Subsection content.

## POURQUOI
Pourquoi content.
End of pourquoi.

## DERNIER
Dernier content.
""",
        "bravo.md": """---
aliases: ["b"]
tags: ["#t"]
derniere-maj: 2026-05-01
---

# Bravo

See ![[alpha]] embedded here.

End body.
""",
        "charlie.md": """---
aliases: ["c"]
tags: ["#t"]
derniere-maj: 2026-05-01
---

# Charlie

Embed with section: ![[alpha#COMMENT]]

Cycle test: ![[delta]]
""",
        "delta.md": """---
aliases: ["d"]
tags: ["#t"]
derniere-maj: 2026-05-01
---

Cycle back: ![[charlie]]
""",
    }
    for name, content in notes.items():
        (v / name).write_text(content, encoding="utf-8")
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for name, content in notes.items():
        p = v / name
        db.index_note(parse_note(p.stem, name, content), p.stat().st_mtime)
    return BrainTools(db, v)


# --- bulk_update_property ---

def test_bulk_update_3_notes(vault):
    result = vault.bulk_update_property(["alpha", "bravo", "charlie"], "derniere-maj", "2026-05-24")
    assert "3/3" in result
    for stem in ("alpha", "bravo", "charlie"):
        actual = vault.get_property(stem, "derniere-maj")
        assert actual == "2026-05-24"


def test_bulk_update_partial_failure(vault):
    result = vault.bulk_update_property(["alpha", "nonexistent", "bravo"], "derniere-maj", "2026-05-24")
    assert "2/3" in result
    assert "ECHEC" in result
    assert "nonexistent" in result


def test_bulk_update_empty_list_rejected(vault):
    result = vault.bulk_update_property([], "derniere-maj", "x")
    assert "REFUS" in result


def test_bulk_update_not_a_list_rejected(vault):
    result = vault.bulk_update_property("alpha", "derniere-maj", "x")  # type: ignore
    assert "REFUS" in result


# --- read_section ---

def test_read_section_simple(vault):
    result = vault.read_section("alpha", "## POURQUOI")
    assert "Pourquoi content" in result
    assert "End of pourquoi" in result
    # Doit s'arreter au prochain ## DERNIER
    assert "Dernier content" not in result


def test_read_section_with_subsections(vault):
    result = vault.read_section("alpha", "## COMMENT")
    assert "Content of COMMENT" in result
    assert "Subsection content" in result  # Subsection included by default
    # Doit s'arreter a ## POURQUOI
    assert "Pourquoi content" not in result


def test_read_section_exclude_subsections(vault):
    result = vault.read_section("alpha", "## COMMENT", include_subsections=False)
    assert "Content of COMMENT" in result
    assert "Subsection content" not in result


def test_read_section_unknown_heading(vault):
    result = vault.read_section("alpha", "## INEXISTANT")
    assert "introuvable" in result


def test_read_section_rejects_non_header(vault):
    result = vault.read_section("alpha", "no hash here")
    assert "REFUS" in result
