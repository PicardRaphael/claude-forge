"""Security dispatcher fails closed if its critical guard cannot run."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


HOOK_PATH = Path(__file__).resolve().parents[1] / "pre-bash-guards.py"
SPEC = importlib.util.spec_from_file_location("codex_pre_bash_guards", HOOK_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_missing_security_guard_is_blocking(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MODULE, "_HOOK_DIR", tmp_path)
    with pytest.raises(MODULE.SecurityGuardFailure):
        MODULE.run_guard("security-guard.py", "{}", critical=True)


def test_crashing_security_guard_is_blocking(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "security-guard.py").write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    monkeypatch.setattr(MODULE, "_HOOK_DIR", tmp_path)
    with pytest.raises(MODULE.SecurityGuardFailure):
        MODULE.run_guard("security-guard.py", "{}", critical=True)


def test_missing_noncritical_guard_is_fail_open(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MODULE, "_HOOK_DIR", tmp_path)
    assert MODULE.run_guard("optional.py", "{}", critical=False) == 0
