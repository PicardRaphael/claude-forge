#!/usr/bin/env python3
"""Session health — rappel /compact ou /clear sur sessions longues.

Triggered on: UserPromptSubmit (une fois par tour utilisateur)

Comportement :
- Tour 1 : suggestion /recap si retour en session existante
- Tour 2 : suggestion /recap (dernier rappel discret)
- Tous les 20 tours : rappel "Session longue — considérer /compact ou /clear"
- Tous les 40 tours : rappel urgent "/compact fortement recommandé"

Le compteur est scopé par session_id (pas de TTL, existence seule).
Toujours exit 0 — non bloquant.

Output via additionalContext (UserPromptSubmit) → Claude voit le rappel dans son contexte.
"""
import json
import os
import sys
from pathlib import Path

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
COUNTER_PATH = os.path.join(_CLAUDE_DIR, ".session-turn-counter")

RECAP_MSG = (
    "[session-health] Tour {turn} — Nouvelle session détectée. "
    "Tip : /recap pour résumer la session précédente si tu reprends un travail en cours."
)

WARN_20_MSG = (
    "[session-health] Session longue ({turn} tours). "
    "Considérer : /compact (compacte le contexte) ou /clear (efface tout). "
    "Pattern recommandé : Document & Clear — dumper le plan dans un .md, puis /clear."
)

WARN_40_MSG = (
    "[session-health] ATTENTION — Session > 40 tours ({turn} tours). "
    "/compact fortement recommandé maintenant. "
    "Pattern : Plan → .md → /clear → nouvelle session propre."
)


def load_state(session_id: str) -> dict:
    """Load counter state, reset if session_id changed."""
    try:
        if os.path.exists(COUNTER_PATH):
            with open(COUNTER_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
            if state.get("session_id") == session_id:
                return state
    except Exception:
        pass
    # New session — reset learning-reminder marker
    reminder_marker = os.path.join(os.path.dirname(__file__), ".learning-reminder-fired")
    if os.path.exists(reminder_marker):
        try:
            os.remove(reminder_marker)
        except Exception:
            pass
    return {"session_id": session_id, "count": 0}


def save_state(state: dict) -> None:
    """Persist counter state to file."""
    try:
        Path(COUNTER_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(COUNTER_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception:
        pass


def get_reminder(turn: int) -> str | None:
    """Return a reminder message or None if nothing to say at this turn."""
    if turn <= 2:
        return RECAP_MSG.format(turn=turn)
    if turn % 40 == 0:
        return WARN_40_MSG.format(turn=turn)
    if turn % 20 == 0:
        return WARN_20_MSG.format(turn=turn)
    return None


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        session_id = data.get("session_id", "unknown")

        state = load_state(session_id)
        state["count"] += 1
        turn = state["count"]
        save_state(state)

        reminder = get_reminder(turn)
        if reminder:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": reminder,
                }
            }
            print(json.dumps(output))

    except Exception:
        pass  # Fail-open — jamais bloquer

    sys.exit(0)


if __name__ == "__main__":
    main()
