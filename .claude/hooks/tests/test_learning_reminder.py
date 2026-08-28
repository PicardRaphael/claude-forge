import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


HOOK = Path(__file__).resolve().parents[1] / "learning-reminder.py"
SPEC = importlib.util.spec_from_file_location("learning_reminder", HOOK)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def event(text: str) -> str:
    return json.dumps({"message": {"content": [{"type": "text", "text": text}]}})


def tool(payload: dict, name: str = "Edit") -> str:
    return json.dumps(
        {
            "message": {
                "content": [
                    {"type": "tool_use", "name": name, "input": payload}
                ]
            }
        }
    )


def test_personal_preference_is_detected():
    labels = MODULE.pending_labels([event("Je préfère des réponses franches.")])
    assert labels == ["fait ou préférence personnelle explicite"]


def test_profile_write_handles_only_profile_signal():
    lines = [
        event("Je préfère le format court, et c'est faux pour ce point."),
        tool({"file_path": "memory/user_raphael_profile.md"}),
    ]
    assert MODULE.pending_labels(lines) == ["correction explicite de Raphaël"]


def test_vault_write_does_not_mask_personal_signal():
    lines = [
        event("Je veux que tu apprennes ça sur moi. Cette doctrine est obsolète."),
        event("mcp__forge-brain__update_note"),
    ]
    assert MODULE.pending_labels(lines) == ["fait ou préférence personnelle explicite"]


def test_raphael_vault_write_handles_personal_signal():
    lines = [
        event("Je veux que tu apprennes ça sur moi."),
        tool(
            {"file": "Raphael-Picard", "content": "updated"},
            name="mcp__forge_brain__update_note",
        ),
    ]
    assert MODULE.pending_labels(lines) == []


def test_raphael_vault_read_does_not_mask_personal_signal():
    lines = [
        event("Je veux que tu apprennes ça sur moi."),
        tool({"file": "Raphael-Picard"}, name="mcp__forge_brain__read_note"),
    ]
    assert MODULE.pending_labels(lines) == [
        "fait ou préférence personnelle explicite"
    ]


def test_unrelated_vault_write_does_not_mask_personal_signal():
    lines = [
        event("Je veux que tu apprennes ça sur moi."),
        tool(
            {"file": "Claude-Forge", "content": "updated"},
            name="mcp__forge_brain__update_note",
        ),
    ]
    assert MODULE.pending_labels(lines) == [
        "fait ou préférence personnelle explicite"
    ]


def test_plain_mention_of_profile_is_not_write_evidence():
    lines = [event("Apprends ça sur moi dans Raphael-Picard.")]
    assert MODULE.pending_labels(lines) == [
        "fait ou préférence personnelle explicite"
    ]


def test_done_report_handles_all_categories():
    lines = [
        event("Je préfère ceci. C'est faux et désormais on fait autrement."),
        event("## Session done — 2026-08-27\n### Appliqué"),
    ]
    assert MODULE.pending_labels(lines) == []


def test_banal_session_stays_silent():
    assert MODULE.pending_labels([event("Merci, à bientôt.")]) == []


def test_invalid_json_is_fail_open():
    assert MODULE.pending_labels(["not-json", ""]) == []


def test_cli_emits_non_blocking_advisory_for_pending_signal(
    tmp_path: Path,
) -> None:
    transcript = tmp_path / "session.jsonl"
    transcript.write_text(
        event("Je préfère des réponses franches.") + "\n", encoding="utf-8"
    )
    env = os.environ.copy()
    env["TEMP"] = str(tmp_path)
    env["TMP"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(
            {
                "session_id": "pytest-signal",
                "transcript_path": str(transcript),
            }
        ),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert "systemMessage" in result.stdout
    assert "préférence personnelle explicite" in result.stdout


def test_cli_is_silent_when_stop_hook_is_already_active(tmp_path: Path) -> None:
    transcript = tmp_path / "session.jsonl"
    transcript.write_text(
        event("Je préfère des réponses franches.") + "\n", encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(
            {
                "session_id": "pytest-active",
                "transcript_path": str(transcript),
                "stop_hook_active": True,
            }
        ),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""


def test_cli_invalid_input_fails_open() -> None:
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input="not-json",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""
