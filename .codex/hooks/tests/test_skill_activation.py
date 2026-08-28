#!/usr/bin/env python3
"""Functional tests for skill-activation.py (UserPromptSubmit recommender).

SCOPE: skill-activation is NON-blocking, fail-open — it injects a skill
recommendation when the prompt matches a trigger. Not a security hook, so the
3:1 adversarial ratio does not apply. These tests pin the matching LOGIC:
  - word-boundary regex (must NOT match substrings — 'done' != 'abandoned')
  - per-session dedup (a skill recommended once is not re-recommended)
  - skill vs command formatting (Skill(name) vs /name)
  - bypass prefixes handled by main() (*, /, #, !)

Run: py -m pytest tests/test_skill_activation.py -v
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skill-activation.py",
)
_spec = importlib.util.spec_from_file_location("skill_activation", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

find_matches = _mod.find_matches
format_recommendation = _mod.format_recommendation
BYPASS_PREFIXES = _mod.BYPASS_PREFIXES

TRIGGERS = {
    "done": {"type": "command", "triggers": ["done", "fin de session"], "description": "Capitalisation"},
    "recap": {"type": "command", "triggers": ["recap", "reprise"], "description": "Snapshot contexte"},
    "forge-brain": {"type": "skill", "triggers": ["vault", "brain"], "description": "Acces vault"},
}


# ===========================================================================
# find_matches — word-boundary matching
# ===========================================================================

def test_match_simple_word():
    m = find_matches("je veux faire un recap", TRIGGERS, set())
    assert any(x["name"] == "recap" for x in m)


def test_word_boundary_no_substring_match():
    """'abandoned' contains 'done' as a substring but must NOT trigger /done
    (word-boundary regex \\bdone\\b). This is the core anti-false-positive guard."""
    m = find_matches("the feature was abandoned last week", TRIGGERS, set())
    assert not any(x["name"] == "done" for x in m)


def test_word_boundary_no_match_inside_word():
    """'vaulted' must not trigger the 'vault' skill."""
    m = find_matches("he vaulted over the fence", TRIGGERS, set())
    assert not any(x["name"] == "forge-brain" for x in m)


def test_multiword_trigger_phrase():
    """A multi-word trigger ('fin de session') matches as a phrase."""
    m = find_matches("on arrive en fin de session la", TRIGGERS, set())
    assert any(x["name"] == "done" for x in m)


def test_case_insensitive():
    m = find_matches("REPRISE du travail", TRIGGERS, set())
    assert any(x["name"] == "recap" for x in m)


def test_no_match_returns_empty():
    assert find_matches("texte totalement neutre sans declencheur", TRIGGERS, set()) == []


# ===========================================================================
# Per-session dedup
# ===========================================================================

def test_already_recommended_skipped():
    """A skill already recommended this session is not returned again."""
    m = find_matches("recap maintenant", TRIGGERS, {"recap"})
    assert not any(x["name"] == "recap" for x in m)


def test_multiple_distinct_matches():
    """Two distinct triggers in one prompt → both matched (none deduped yet)."""
    m = find_matches("fais un recap puis ouvre le vault", TRIGGERS, set())
    names = {x["name"] for x in m}
    assert "recap" in names and "forge-brain" in names


def test_real_project_memory_trigger_matches_explicit_creation_only():
    trigger_path = Path(__file__).resolve().parents[2] / ".skill-triggers.json"
    real_triggers = json.loads(trigger_path.read_text(encoding="utf-8"))

    matches = find_matches(
        "Crée un projet Atlas pour construire un assistant de veille.",
        real_triggers,
        set(),
    )
    assert any(item["name"] == "project-memory" for item in matches)

    casual = find_matches(
        "J'ai une idée d'assistant de veille qui s'appellerait peut-être Atlas.",
        real_triggers,
        set(),
    )
    assert not any(item["name"] == "project-memory" for item in casual)


# ===========================================================================
# format_recommendation — skill vs command
# ===========================================================================

def test_format_command_uses_slash():
    line = format_recommendation({"name": "done", "type": "command", "description": "Capi"})
    assert line.startswith("- /done")


def test_format_skill_uses_skill_call():
    line = format_recommendation({"name": "forge-brain", "type": "skill", "description": "Vault"})
    assert "Skill(forge-brain)" in line


def test_format_default_type_is_skill():
    """No 'type' key defaults to skill formatting."""
    line = format_recommendation({"name": "x", "description": "d"})
    assert "Skill(x)" in line


def test_format_no_description():
    line = format_recommendation({"name": "done", "type": "command"})
    assert line == "- /done"


# ===========================================================================
# Bypass prefixes
# ===========================================================================

def test_bypass_prefixes_declared():
    """Slash commands, directives and system markers are bypassed by main()."""
    assert set(BYPASS_PREFIXES) == {"*", "/", "#", "!"}


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
