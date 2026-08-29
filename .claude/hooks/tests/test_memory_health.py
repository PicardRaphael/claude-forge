"""Lifecycle tests for the consolidated temporary-memory health hook."""

from datetime import date
import importlib.util
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "memory-health.py"
SPEC = importlib.util.spec_from_file_location("memory_health", HOOK)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _project(folder: Path, name: str, expiry: str | None) -> None:
    expiry_line = f"expires: {expiry}\n" if expiry else ""
    (folder / name).write_text(f"---\ntype: project\n{expiry_line}---\n", encoding="utf-8")


def test_lifecycle_reports_missing_and_expired_without_deleting(tmp_path: Path) -> None:
    _project(tmp_path, "project_missing.md", None)
    _project(tmp_path, "project_expired.md", "2025-01-01")
    _project(tmp_path, "project_active.md", "2099-01-01")
    missing, expired = MODULE.lifecycle_issues(tmp_path, today=date(2026, 8, 29))
    assert missing == ["project_missing.md"]
    assert expired == ["project_expired.md"]
    assert len(list(tmp_path.glob("project_*.md"))) == 3


def test_clean_lifecycle_is_silent(tmp_path: Path) -> None:
    _project(tmp_path, "project_active.md", "2099-01-01")
    assert MODULE.warning(tmp_path, tmp_path / "MEMORY.md") is None
