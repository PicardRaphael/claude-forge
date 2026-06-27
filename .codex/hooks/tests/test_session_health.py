#!/usr/bin/env python3
"""Functional tests for session-health.py (UserPromptSubmit reminder).

SCOPE: session-health is a NON-blocking, fail-open reminder hook — NOT a
security/control hook. The 3:1 adversarial ratio (canon: hooks sécu) does not
apply. These tests pin the reminder LOGIC (turn thresholds, session reset),
which is the only thing that can silently break.

get_reminder(turn) contract (session-health.py:74-82):
  - turn <= 2          -> RECAP_MSG       (early /recap nudge)
  - turn % 40 == 0     -> WARN_40_MSG     (urgent, checked before %20)
  - turn % 20 == 0     -> WARN_20_MSG
  - otherwise          -> None
load_state resets the counter when session_id changes.

Run: py -m pytest tests/test_session_health.py -v
"""
import importlib.util
import json
import os
import sys

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "session-health.py",
)
_spec = importlib.util.spec_from_file_location("session_health", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

get_reminder = _mod.get_reminder
load_state = _mod.load_state
save_state = _mod.save_state


# ===========================================================================
# get_reminder — threshold logic
# ===========================================================================

def test_turn_1_recap():
    assert "recap" in get_reminder(1).lower()


def test_turn_2_recap():
    assert "recap" in get_reminder(2).lower()


def test_turn_3_silent():
    """Turn 3 is past the recap window and not a multiple of 20/40 → no reminder."""
    assert get_reminder(3) is None


def test_turn_19_silent():
    assert get_reminder(19) is None


def test_turn_20_warns():
    msg = get_reminder(20)
    assert msg is not None and "20" in msg


def test_turn_21_silent():
    assert get_reminder(21) is None


def test_turn_40_urgent_not_20():
    """40 is a multiple of BOTH 20 and 40 — the %40 branch must win (urgent message)."""
    msg = get_reminder(40)
    assert msg is not None
    assert "ATTENTION" in msg or "fortement" in msg


def test_turn_60_warns_20():
    """60 % 40 != 0 but 60 % 20 == 0 → the regular 20-turn warning."""
    msg = get_reminder(60)
    assert msg is not None and "60" in msg


def test_turn_80_urgent():
    """80 % 40 == 0 → urgent again."""
    msg = get_reminder(80)
    assert "ATTENTION" in msg or "fortement" in msg


# ===========================================================================
# load_state / save_state — session-scoped counter with reset on change
# ===========================================================================

def test_state_roundtrip(tmp_path, monkeypatch):
    counter = tmp_path / ".session-turn-counter"
    monkeypatch.setattr(_mod, "COUNTER_PATH", str(counter))
    save_state({"session_id": "S1", "count": 7})
    state = load_state("S1")
    assert state["count"] == 7


def test_state_resets_on_new_session(tmp_path, monkeypatch):
    """A different session_id must reset the counter to 0 (no cross-session bleed)."""
    counter = tmp_path / ".session-turn-counter"
    monkeypatch.setattr(_mod, "COUNTER_PATH", str(counter))
    save_state({"session_id": "S1", "count": 99})
    state = load_state("S2")  # different session
    assert state["count"] == 0
    assert state["session_id"] == "S2"


def test_state_missing_file_starts_at_zero(tmp_path, monkeypatch):
    counter = tmp_path / "does-not-exist"
    monkeypatch.setattr(_mod, "COUNTER_PATH", str(counter))
    state = load_state("fresh")
    assert state["count"] == 0


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
