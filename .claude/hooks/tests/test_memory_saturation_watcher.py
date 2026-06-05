#!/usr/bin/env python3
"""Functional tests for memory-saturation-watcher.py (SessionStart advisory hook).

SCOPE: memory-saturation-watcher is a NON-blocking, fail-open advisory hook —
NOT a security/control hook. The 3:1 adversarial ratio does not apply. These
tests pin the threshold LOGIC (WARNING 250, CRITICAL 290, excluded files) and
the fail-open contract (missing dir).

check_memory_saturation(dir, warning=250, critical=290) contract:
  - count < warning   -> None
  - warning <= count < critical -> WARNING message
  - count >= critical -> CRITICAL message
  - missing dir       -> None (fail-open)
  - MEMORY.md and _index_archive.md not counted

Run: py -m pytest tests/test_memory_saturation_watcher.py -v
"""
import importlib.util
import os
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "memory-saturation-watcher.py",
)
_spec = importlib.util.spec_from_file_location("memory_saturation_watcher", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

check_memory_saturation = _mod.check_memory_saturation
count_memory_files = _mod.count_memory_files


def _make_files(tmp_path, n: int, prefix: str = "feedback_") -> None:
    """Create n .md files (other than MEMORY.md / _index_archive.md)."""
    for i in range(n):
        (tmp_path / f"{prefix}{i}.md").write_text("body", encoding="utf-8")


# ===========================================================================
# Nominal — threshold boundaries
# ===========================================================================

def test_below_warning_returns_none(tmp_path):
    """Count below WARNING threshold (250) must NOT trigger anything."""
    _make_files(tmp_path, 249)
    assert check_memory_saturation(str(tmp_path)) is None


def test_warning_threshold_triggers_warning(tmp_path):
    """Count >= warning but < critical triggers WARNING message."""
    _make_files(tmp_path, 250)
    msg = check_memory_saturation(str(tmp_path))
    assert msg is not None
    assert "WARNING" in msg
    assert "250" in msg


# ===========================================================================
# Adversarial — boundary cases + fail-open
# ===========================================================================

def test_critical_threshold_triggers_critical(tmp_path):
    """Count >= critical triggers CRITICAL message (must NOT be WARNING)."""
    _make_files(tmp_path, 290)
    msg = check_memory_saturation(str(tmp_path))
    assert msg is not None
    assert "CRITICAL" in msg
    assert "WARNING" not in msg
    assert "290" in msg


def test_excluded_files_not_counted(tmp_path):
    """MEMORY.md and _index_archive.md must be excluded from the count."""
    _make_files(tmp_path, 249)
    (tmp_path / "MEMORY.md").write_text("index", encoding="utf-8")
    (tmp_path / "_index_archive.md").write_text("archive", encoding="utf-8")
    # 249 real + 2 excluded = should still return None (below 250)
    assert count_memory_files(str(tmp_path)) == 249
    assert check_memory_saturation(str(tmp_path)) is None


def test_missing_dir_returns_none():
    """Non-existent path must return None silently (fail-open)."""
    assert check_memory_saturation("/nonexistent/path/memory") is None
    assert count_memory_files("/nonexistent/path/memory") is None


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
