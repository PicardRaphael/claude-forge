#!/usr/bin/env python3
"""Learning reminder — rappel de sauvegarder les apprentissages avant d'arrêter.

Triggered on: Stop (une fois par session via once:true dans settings.json)

Comportement :
- Injecte un rappel dans le contexte de Claude via decision:block + reason
- Claude voit le message et peut sauvegarder avant de s'arrêter vraiment
- once:true dans settings.json = se déclenche une seule fois par session

Note sur le mécanisme Stop :
- Sur l'événement Stop, additionalContext n'est pas supporté
- Le seul moyen d'injecter du contenu est decision:block + reason
- "block" sur Stop = "continue avec reason comme prompt", pas "empêcher définitivement"
- Avec once:true, le hook ne se déclenche qu'une fois → pas de boucle infinie

Toujours exit 0 — pas de blocage sur erreur.
"""
import json
import sys

REMINDER = (
    "Avant de terminer : as-tu appris quelque chose cette session ? Vérifie :\n"
    "1. Mémoire projet (feedback_* / reference_*) — apprentissages à sauvegarder ?\n"
    "2. Vault forge-brain (Knowledge/erreurs/, Knowledge/questions/) — note à créer ?\n"
    "3. Skills (section Apprentissage) — pattern efficace ou gotcha découvert ?\n"
    "4. CLAUDE.md — erreur à ne plus refaire ?\n\n"
    "Si rien à sauvegarder, réponds juste 'rien à sauvegarder' pour continuer."
)


def main() -> None:
    try:
        # Lire stdin même si on n'utilise pas les données
        sys.stdin.read()
    except Exception:
        pass

    try:
        output = {
            "decision": "block",
            "reason": REMINDER,
        }
        print(json.dumps(output))
    except Exception:
        pass  # Fail-open — jamais bloquer sur erreur

    sys.exit(0)


if __name__ == "__main__":
    main()
