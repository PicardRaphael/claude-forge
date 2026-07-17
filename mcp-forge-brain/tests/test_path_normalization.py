"""Tests path normalization: strip accidental vault prefix."""

from pathlib import Path

import pytest

from src.tools.brain import _normalize_path


def test_no_prefix_passthrough():
    vault = Path("vault/claude-forge")
    norm, warn = _normalize_path(vault, "Knowledge/syntheses/foo.md")
    assert norm == "Knowledge/syntheses/foo.md"
    assert warn is None


def test_full_prefix_stripped():
    vault = Path("vault/claude-forge")
    norm, warn = _normalize_path(vault, "vault/claude-forge/Knowledge/syntheses/foo.md")
    assert norm == "Knowledge/syntheses/foo.md"
    assert warn is not None
    assert "stripped" in warn


def test_partial_prefix_stripped():
    vault = Path("vault/claude-forge")
    norm, warn = _normalize_path(vault, "claude-forge/Knowledge/foo.md")
    assert norm == "Knowledge/foo.md"
    assert warn is not None


def test_backslash_normalized():
    vault = Path("vault/claude-forge")
    norm, _ = _normalize_path(vault, "vault\\claude-forge\\Knowledge\\foo.md")
    assert norm == "Knowledge/foo.md"


def test_leading_dot_slash_handled():
    vault = Path("vault/claude-forge")
    norm, warn = _normalize_path(vault, "./vault/claude-forge/foo.md")
    assert norm == "foo.md"
    assert warn is not None


def test_leading_slash_rejected():
    vault = Path("vault/claude-forge")
    with pytest.raises(ValueError, match="Absolute path refused"):
        _normalize_path(vault, "/Knowledge/foo.md")


def test_windows_abs_outside_vault_rejected(tmp_path):
    """B3 fix: a Windows absolute path that resolves outside vault must raise."""
    vault = tmp_path / "vault"
    vault.mkdir()
    with pytest.raises(ValueError, match="Absolute path refused"):
        _normalize_path(vault, r"C:\Users\evil\note.md")


def test_parent_segment_rejected():
    with pytest.raises(ValueError, match="Parent path segment refused"):
        _normalize_path(Path("vault/claude-forge"), "../cognition-store/private.md")
