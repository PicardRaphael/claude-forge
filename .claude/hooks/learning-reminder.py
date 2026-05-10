#!/usr/bin/env python3
"""Learning reminder — fires ONCE per session on Stop.

Marker in %TEMP% prevents infinite loop (decision:block re-triggers Stop).
SessionStart hook (session-reminder.py) cleans the marker.
"""
import json
import os
import sys
import tempfile

MARKER = os.path.join(tempfile.gettempdir(), "claude-forge-learning-reminded")

REMINDER = (
    "Avant de terminer : as-tu appris quelque chose cette session ? Vérifie :\n"
    "1. Mémoire projet (feedback_* / reference_*) — apprentissages à sauvegarder ?\n"
    "2. Vault forge-brain (Knowledge/erreurs/, Knowledge/questions/) — note à créer ?\n"
    "3. Skills (section Apprentissage) — pattern efficace ou gotcha découvert ?\n"
    "4. CLAUDE.md — erreur à ne plus refaire ?\n"
    "5. /reasoning-cache — as-tu résolu un problème complexe (raisonnement multi-étapes, "
    "direction changée, approche non-évidente) ? Si oui, lance /reasoning-cache pour le sauvegarder.\n\n"
    "Si rien à sauvegarder, réponds juste 'rien à sauvegarder' pour continuer."
)


def main() -> None:
    try:
        sys.stdin.read()
    except Exception:
        pass

    if os.path.exists(MARKER):
        sys.exit(0)

    try:
        with open(MARKER, "w") as f:
            f.write("1")
    except Exception:
        pass

    try:
        print(json.dumps({"decision": "block", "reason": REMINDER}))
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
