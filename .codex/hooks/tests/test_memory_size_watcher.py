#!/usr/bin/env python3
"""Functional tests for memory-size-watcher.py (SessionStart advisory hook).

SCOPE: memory-size-watcher is a NON-blocking, fail-open advisory hook — NOT a
security/control hook. The 3:1 adversarial ratio does not apply. These tests
pin the warning LOGIC (threshold, message format) and the fail-open contract
(missing file, IO error, non-UTF-8 bytes).

check_memory_size(path, threshold=38000) contract:
  - size <= threshold  -> None  (no warning)
  - size > threshold   -> warning string containing size info
  - missing file       -> None  (fail-open)
  - non-UTF-8 bytes    -> None  (fail-open)

Run: py -m pytest tests/test_memory_size_watcher.py -v
"""
import importlib.util
import os
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "memory-size-watcher.py",
)
_spec = importlib.util.spec_from_file_location("memory_size_watcher", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

check_memory_size = _mod.check_memory_size


# ===========================================================================
# Nominal — threshold boundary
# ===========================================================================

def test_below_threshold_returns_none(tmp_path):
    """File exactly at threshold (38000 chars) must NOT trigger the warning."""
    f = tmp_path / "MEMORY.md"
    f.write_text("x" * 38000, encoding="utf-8")
    assert check_memory_size(str(f)) is None


def test_above_threshold_returns_warning(tmp_path):
    """File one char above threshold must trigger the warning with size info."""
    f = tmp_path / "MEMORY.md"
    content = "x" * 38001
    f.write_text(content, encoding="utf-8")
    msg = check_memory_size(str(f))
    assert msg is not None
    assert "38001" in msg
    assert "memory-size-watcher" in msg


# ===========================================================================
# Adversarial — fail-open contract
# ===========================================================================

def test_missing_file_returns_none():
    """Non-existent path must return None silently (fail-open)."""
    assert check_memory_size("/nonexistent/path/MEMORY.md") is None


def test_non_utf8_bytes_returns_none(tmp_path):
    """Non-UTF-8 bytes trigger UnicodeDecodeError which must be swallowed."""
    f = tmp_path / "MEMORY.md"
    f.write_bytes(b"\xff\xfe" * 20000)
    assert check_memory_size(str(f)) is None


def test_custom_threshold_respected(tmp_path):
    """Caller-supplied threshold overrides the default 38000."""
    f = tmp_path / "MEMORY.md"
    f.write_text("x" * 100, encoding="utf-8")
    # Below custom threshold of 200 -> None
    assert check_memory_size(str(f), threshold=200) is None
    # Above custom threshold of 50 -> warning
    msg = check_memory_size(str(f), threshold=50)
    assert msg is not None


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
