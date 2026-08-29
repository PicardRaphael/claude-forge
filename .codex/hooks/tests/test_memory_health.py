"""The Codex adapter exposes the shared memory lifecycle policy."""

from datetime import date
import importlib.util
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "memory-health.py"
SPEC = importlib.util.spec_from_file_location("codex_memory_health", HOOK)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_codex_adapter_exposes_lifecycle_check(tmp_path: Path) -> None:
    (tmp_path / "project_old.md").write_text("---\ntype: project\nexpires: 2020-01-01\n---\n", encoding="utf-8")
    missing, expired = MODULE.lifecycle_issues(tmp_path, today=date(2026, 8, 29))
    assert missing == []
    assert expired == ["project_old.md"]
