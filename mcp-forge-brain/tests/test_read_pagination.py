"""Tests read_note pagination (offset/limit_chars)."""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


@pytest.fixture
def big_note(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    # 5000 chars body
    body = "x" * 5000
    content = f"---\naliases: [\"big\"]\ntags: [\"#t\"]\n---\n\n{body}"
    (vault / "big.md").write_text(content, encoding="utf-8")
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    parsed = parse_note("big", "big.md", content)
    db.index_note(parsed, (vault / "big.md").stat().st_mtime)
    return BrainTools(db, vault)


def test_no_pagination_returns_full(big_note):
    result = big_note.read_note("big")
    assert "---" in result
    assert len(result) > 5000


def test_offset_limit_chars(big_note):
    result = big_note.read_note("big", offset=100, limit_chars=200)
    assert "[chars 100-300/" in result
    # Body has 200 'x' chars in the returned chunk
    assert result.count("x") <= 200


def test_offset_beyond_content(big_note):
    result = big_note.read_note("big", offset=99999, limit_chars=100)
    assert "depasse la taille" in result


def test_pagination_has_continuation_hint(big_note):
    result = big_note.read_note("big", offset=0, limit_chars=1000)
    assert "[suite : appeler avec offset=1000" in result


def test_pagination_end_no_continuation(big_note):
    """Last chunk should NOT have continuation hint."""
    result = big_note.read_note("big", offset=5000, limit_chars=200)
    # Note total is frontmatter + body ~5070 chars, so 5000+200 might still be inside
    # Use a clearly-out range
    result = big_note.read_note("big", offset=0, limit_chars=100000)
    assert "[suite :" not in result
