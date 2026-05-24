"""Tests indexer: null/empty filtering + aliases duplicate detection."""

from src.indexer import parse_note


def test_aliases_null_filtered():
    content = """---
aliases:
  - "alpha"
  - null
  - "beta"
  - ""
tags:
  - "#type/test"
  - null
---

# Body
"""
    parsed = parse_note("test", "test.md", content)
    assert parsed.aliases == ["alpha", "beta"]
    assert parsed.tags == ["#type/test"]


def test_aliases_string_form():
    content = """---
aliases: "single-alias"
tags: "#type/single"
---

body
"""
    parsed = parse_note("test", "test.md", content)
    assert parsed.aliases == ["single-alias"]
    assert parsed.tags == ["#type/single"]


def test_aliases_duplicate_blocks_detected():
    """Inline + list block declaration detected as lint warning."""
    content = """---
aliases: ["alpha", "beta"]
  - "gamma"
  - "delta"
tags:
  - "#type/test"
---

body
"""
    parsed = parse_note("test", "test.md", content)
    assert any("aliases declared TWICE" in w for w in parsed.lint_warnings)


def test_aliases_single_block_no_warning():
    content = """---
aliases:
  - "alpha"
  - "beta"
tags:
  - "#type/test"
---

body
"""
    parsed = parse_note("test", "test.md", content)
    assert parsed.lint_warnings == []
    assert parsed.aliases == ["alpha", "beta"]


def test_wikilinks_with_pipe_and_section():
    content = """---
aliases:
  - "x"
---

See [[note-a]], [[note-b|alias]], [[note-c#section]], [[note-d|alias#section]].
"""
    parsed = parse_note("test", "test.md", content)
    assert "note-a" in parsed.wikilinks
    assert "note-b" in parsed.wikilinks
    assert "note-c#section" in parsed.wikilinks
    assert "note-d" in parsed.wikilinks


def test_no_frontmatter():
    parsed = parse_note("test", "test.md", "# Just body\n\nNo frontmatter here.")
    assert parsed.aliases == []
    assert parsed.tags == []
    assert parsed.lint_warnings == []
