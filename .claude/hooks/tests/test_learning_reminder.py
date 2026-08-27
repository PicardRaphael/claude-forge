import importlib.util
import json
from pathlib import Path


HOOK = Path(__file__).resolve().parents[1] / "learning-reminder.py"
SPEC = importlib.util.spec_from_file_location("learning_reminder", HOOK)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def event(text: str) -> str:
    return json.dumps({"message": {"content": [{"type": "text", "text": text}]}})


def tool(payload: dict) -> str:
    return json.dumps(
        {"message": {"content": [{"type": "tool_use", "input": payload}]}}
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
