#!/usr/bin/env python3
"""Adversarial tests for the Codex UserPromptSubmit memory recall hook."""

from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path

import pytest


HOOK_PATH = Path(__file__).resolve().parents[1] / "memory-recall.py"
SPEC = importlib.util.spec_from_file_location("codex_memory_recall", HOOK_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write_memory(
    memory_dir: Path,
    filename: str,
    *,
    name: str,
    description: str,
    trigger: str | None,
    memory_type: str = "feedback",
) -> None:
    trigger_line = f"trigger: {trigger}\n" if trigger is not None else ""
    (memory_dir / filename).write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"type: {memory_type}\n"
        f"{trigger_line}"
        "---\n"
        "Body intentionally not injected.\n",
        encoding="utf-8",
    )


@pytest.fixture
def isolated_memory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    monkeypatch.setattr(MODULE, "_MEMORY_DIR", memory_dir)
    monkeypatch.setattr(MODULE, "_CACHE", tmp_path / "memory-recall-cache.json")
    return memory_dir


def _run_main(payload: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> str:
    monkeypatch.setattr(MODULE.sys, "stdin", io.StringIO(payload))
    with pytest.raises(SystemExit) as exit_info:
        MODULE.main()
    assert exit_info.value.code == 0
    return capsys.readouterr().out.strip()


def test_malformed_json_is_silent_fail_open(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _run_main("{not-json", monkeypatch, capsys) == ""


def test_neutral_prompt_and_short_prompt_are_silent(
    isolated_memory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_memory(
        isolated_memory,
        "feedback_git.md",
        name="git-policy",
        description="Commit policy",
        trigger="commit, push",
    )

    assert _run_main(json.dumps({"prompt": "bonjour"}), monkeypatch, capsys) == ""
    assert _run_main(
        json.dumps({"prompt": "analyse cette architecture neutre"}),
        monkeypatch,
        capsys,
    ) == ""


def test_user_profile_without_trigger_is_never_injected(
    isolated_memory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_memory(
        isolated_memory,
        "user_raphael_profile.md",
        name="raphael-full-profile",
        description="Profil personnel complet de Raphael et ses preferences",
        trigger=None,
        memory_type="user",
    )

    output = _run_main(
        json.dumps({"prompt": "Parle-moi du profil personnel complet de Raphael"}),
        monkeypatch,
        capsys,
    )

    assert output == ""


def test_explicit_trigger_emits_official_codex_json_shape(
    isolated_memory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_memory(
        isolated_memory,
        "feedback_commit.md",
        name="commit-policy",
        description="Commit and push directly on main after verification",
        trigger="commit, push",
    )

    output = _run_main(
        json.dumps({"prompt": "Fais le commit puis le push maintenant"}),
        monkeypatch,
        capsys,
    )
    parsed = json.loads(output)

    assert parsed == {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "Ce repo contient 1 souvenir dont les mots-cles recoupent "
                "la demande en cours :\n"
                "- **commit-policy** (`memory/feedback_commit.md`) — "
                "Commit and push directly on main after verification"
            ),
        }
    }


def test_word_boundaries_reject_substrings_and_accept_known_flexion() -> None:
    prompt = "fais le deux maintenant"
    assert MODULE._contains("main", prompt) is False
    assert MODULE._contains("audit", "audite cette configuration") is True
    assert MODULE._contains("log", "la logique fonctionne") is False


def test_output_is_limited_to_three_memories_and_1200_characters(
    isolated_memory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for index in range(5):
        _write_memory(
            isolated_memory,
            f"feedback_{index}.md",
            name=f"policy-{index}-" + ("n" * 180),
            description="d" * 400,
            trigger="architecture",
        )

    output = _run_main(
        json.dumps({"prompt": "Analyse cette architecture en profondeur"}),
        monkeypatch,
        capsys,
    )
    context = json.loads(output)["hookSpecificOutput"]["additionalContext"]

    assert context.count("(`memory/") <= 3
    assert len(context) <= 1200


def test_missing_memory_directory_is_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(MODULE, "_MEMORY_DIR", tmp_path / "missing")
    monkeypatch.setattr(MODULE, "_CACHE", tmp_path / "cache.json")

    output = _run_main(
        json.dumps({"prompt": "Fais un commit maintenant"}),
        monkeypatch,
        capsys,
    )

    assert output == ""


def test_hook_is_registered_portably_for_user_prompt_submit() -> None:
    hooks_path = Path(__file__).resolve().parents[2] / "hooks.json"
    config = json.loads(hooks_path.read_text(encoding="utf-8"))
    handlers = config["hooks"]["UserPromptSubmit"][0]["hooks"]
    handler = next(
        item for item in handlers if "memory-recall.py" in item.get("command", "")
    )

    assert handler["type"] == "command"
    assert handler["commandWindows"] == "py .codex/hooks/memory-recall.py"
    assert ":\\" not in handler["commandWindows"]
