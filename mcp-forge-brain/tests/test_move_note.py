"""Tests move_note: wikilink rewriting + safety."""

import tempfile
from pathlib import Path

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


@pytest.fixture
def vault_with_notes(tmp_path):
    """Create a tmp vault with 3 interlinked notes + indexer."""
    vault = tmp_path / "vault"
    vault.mkdir()
    db_path = tmp_path / "test.db"

    note_a = """---
aliases:
  - "alpha"
  - "alpha-canonique"
tags:
  - "#type/test"
---

# Alpha

Some content.
"""
    note_b = """---
aliases:
  - "bravo"
tags:
  - "#type/test"
---

# Bravo

Pointing to [[alpha]] and [[alpha|Alpha alias]] and [[alpha#section]].
"""
    note_c = """---
aliases:
  - "charlie"
tags:
  - "#type/test"
---

# Charlie

Pointing to [[alpha-bis]] (which doesn't exist) and [[bravo]].
"""

    (vault / "alpha.md").write_text(note_a, encoding="utf-8")
    (vault / "bravo.md").write_text(note_b, encoding="utf-8")
    (vault / "charlie.md").write_text(note_c, encoding="utf-8")

    db = BrainDB(db_path, FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for name in ("alpha", "bravo", "charlie"):
        p = vault / f"{name}.md"
        parsed = parse_note(name, f"{name}.md", p.read_text(encoding="utf-8"))
        db.index_note(parsed, p.stat().st_mtime)

    tools = BrainTools(db, vault)
    return tools, vault, db


def test_move_note_basic(vault_with_notes):
    tools, vault, _ = vault_with_notes
    result = tools.move_note("alpha", "Archive/alpha.md")
    assert "deplacee" in result
    assert (vault / "Archive" / "alpha.md").exists()
    assert not (vault / "alpha.md").exists()


def test_move_note_rejects_existing_destination(vault_with_notes):
    tools, vault, _ = vault_with_notes
    (vault / "Archive").mkdir()
    (vault / "Archive" / "alpha.md").write_text("existing")
    result = tools.move_note("alpha", "Archive/alpha.md")
    assert "REFUS" in result


def test_move_note_rejects_non_md_destination(vault_with_notes):
    tools, _, _ = vault_with_notes
    result = tools.move_note("alpha", "Archive/alpha.txt")
    assert "REFUS" in result


def test_move_note_unknown_source(vault_with_notes):
    tools, _, _ = vault_with_notes
    result = tools.move_note("nonexistent-note", "anywhere/foo.md")
    assert "introuvable" in result


def test_move_note_rewrites_wikilinks_on_rename(vault_with_notes):
    """When stem changes (alpha -> alpha-renamed), wikilinks in backlinks must update."""
    tools, vault, _ = vault_with_notes
    result = tools.move_note("alpha", "Archive/alpha-renamed.md")
    assert "deplacee" in result
    bravo_content = (vault / "bravo.md").read_text(encoding="utf-8")
    # Original [[alpha]] -> [[alpha-renamed]]
    assert "[[alpha-renamed]]" in bravo_content
    # Pipe form preserved: [[alpha|Alpha alias]] -> [[alpha-renamed|Alpha alias]]
    assert "[[alpha-renamed|Alpha alias]]" in bravo_content
    # Section form preserved: [[alpha#section]] -> [[alpha-renamed#section]]
    assert "[[alpha-renamed#section]]" in bravo_content
    # The original [[alpha]] should be gone (no partial leak)
    assert "[[alpha]]" not in bravo_content
    assert "[[alpha|" not in bravo_content
    assert "[[alpha#" not in bravo_content


def test_move_note_no_partial_match(vault_with_notes):
    """Critical safety: moving 'alpha' must NOT touch 'alpha-bis' wikilink in charlie."""
    tools, vault, _ = vault_with_notes
    tools.move_note("alpha", "Archive/alpha-renamed.md")
    charlie_content = (vault / "charlie.md").read_text(encoding="utf-8")
    # [[alpha-bis]] should be untouched
    assert "[[alpha-bis]]" in charlie_content


def test_move_note_same_stem_no_wikilink_update(vault_with_notes):
    """Moving without renaming (same stem, different folder) does NOT rewrite wikilinks."""
    tools, vault, _ = vault_with_notes
    tools.move_note("alpha", "Archive/alpha.md")
    bravo_content = (vault / "bravo.md").read_text(encoding="utf-8")
    # [[alpha]] still works because Obsidian resolves by stem, not path
    assert "[[alpha]]" in bravo_content


def test_delete_note_blocked_by_backlinks(vault_with_notes):
    tools, vault, _ = vault_with_notes
    result = tools.delete_note("alpha")
    assert "REFUS" in result
    assert "backlinks" in result
    assert (vault / "alpha.md").exists()  # not deleted


def test_delete_note_force_works(vault_with_notes):
    tools, vault, _ = vault_with_notes
    result = tools.delete_note("alpha", force=True)
    assert "supprimee" in result
    assert not (vault / "alpha.md").exists()


def test_delete_note_no_backlinks_ok(vault_with_notes):
    tools, vault, _ = vault_with_notes
    result = tools.delete_note("charlie")
    assert "supprimee" in result
    assert not (vault / "charlie.md").exists()


def test_delete_note_force_reports_broken_count(vault_with_notes):
    """B2 fix: delete_note(force=True) must report number of broken wikilinks."""
    tools, _, _ = vault_with_notes
    result = tools.delete_note("alpha", force=True)
    assert "supprimee" in result
    assert "BRISES" in result
    assert "bravo" in result  # source listed


def test_move_note_self_link_rewritten(tmp_path):
    """B1.b fix: a self-link inside the moved note must be rewritten too."""
    from src.config import FTSWeights
    from src.database import BrainDB
    vault = tmp_path / "vault"
    vault.mkdir()
    note = """---
aliases: ["alpha"]
tags: ["#type/test"]
---

I am [[alpha]] referencing myself, and also ![[alpha]] embedded.
"""
    (vault / "alpha.md").write_text(note, encoding="utf-8")
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    parsed = parse_note("alpha", "alpha.md", note)
    db.index_note(parsed, (vault / "alpha.md").stat().st_mtime)
    tools = BrainTools(db, vault)

    result = tools.move_note("alpha", "Archive/alpha-new.md")
    assert "deplacee" in result
    new_content = (vault / "Archive" / "alpha-new.md").read_text(encoding="utf-8")
    assert "[[alpha-new]] referencing" in new_content
    assert "![[alpha-new]] embedded" in new_content
    assert "[[alpha]]" not in new_content


def test_move_note_embed_rewrite(vault_with_notes):
    """B1.a: ![[stem]] embeds must be rewritten with leading ! preserved."""
    tools, vault, _ = vault_with_notes
    # Add embed in bravo
    bravo_path = vault / "bravo.md"
    bravo_path.write_text(
        bravo_path.read_text(encoding="utf-8") + "\n\nEmbed: ![[alpha]]\n",
        encoding="utf-8",
    )
    parsed = parse_note("bravo", "bravo.md", bravo_path.read_text(encoding="utf-8"))
    tools._db.index_note(parsed, bravo_path.stat().st_mtime)

    tools.move_note("alpha", "Archive/alpha-renamed.md")
    bravo_content = bravo_path.read_text(encoding="utf-8")
    assert "![[alpha-renamed]]" in bravo_content
    assert "![[alpha]]" not in bravo_content


def test_move_note_case_insensitive(tmp_path):
    """B1.c: [[Alpha]] (capital) must match old_stem 'alpha' (Obsidian case-insensitive)."""
    from src.config import FTSWeights
    from src.database import BrainDB
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("---\naliases: [\"a\"]\ntags: [\"#t\"]\n---\n\nbody\n", encoding="utf-8")
    (vault / "bravo.md").write_text(
        "---\naliases: [\"b\"]\ntags: [\"#t\"]\n---\n\nSee [[Alpha]] and [[ALPHA#sec]].\n",
        encoding="utf-8",
    )
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for name in ("alpha", "bravo"):
        p = vault / f"{name}.md"
        db.index_note(parse_note(name, f"{name}.md", p.read_text(encoding="utf-8")), p.stat().st_mtime)
    tools = BrainTools(db, vault)

    tools.move_note("alpha", "Archive/alpha-new.md")
    bravo_content = (vault / "bravo.md").read_text(encoding="utf-8")
    assert "[[alpha-new]]" in bravo_content
    assert "[[alpha-new#sec]]" in bravo_content
    assert "[[Alpha]]" not in bravo_content
    assert "[[ALPHA" not in bravo_content


def test_move_note_inside_code_block_preserved(tmp_path):
    """B1.d: [[alpha]] inside code blocks/inline code MUST stay literal."""
    from src.config import FTSWeights
    from src.database import BrainDB
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("---\naliases: [\"a\"]\ntags: [\"#t\"]\n---\n\nbody\n", encoding="utf-8")
    bravo_body = """---
aliases: ["b"]
tags: ["#t"]
---

Real link: [[alpha]]
Inline code: `[[alpha]]`
Fenced block:
```
[[alpha]] should stay literal
```
End.
"""
    (vault / "bravo.md").write_text(bravo_body, encoding="utf-8")
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for name in ("alpha", "bravo"):
        p = vault / f"{name}.md"
        db.index_note(parse_note(name, f"{name}.md", p.read_text(encoding="utf-8")), p.stat().st_mtime)
    tools = BrainTools(db, vault)

    tools.move_note("alpha", "Archive/alpha-new.md")
    bravo_content = (vault / "bravo.md").read_text(encoding="utf-8")
    # Real link rewritten
    assert "Real link: [[alpha-new]]" in bravo_content
    # Inline code preserved
    assert "`[[alpha]]`" in bravo_content
    # Fenced code preserved
    assert "[[alpha]] should stay literal" in bravo_content
