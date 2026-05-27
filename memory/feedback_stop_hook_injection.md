---
name: stop-hook-context-injection
description: Sur l'event Stop, additionalContext n'est pas supporté — seul decision:block+reason injecte du contenu dans le contexte Claude
type: feedback
originSessionId: 00ed39aa-17db-4d58-bcdc-ef097926d20a
---
Sur l'événement `Stop`, le mécanisme `additionalContext` dans `hookSpecificOutput` n'est **pas supporté** (documenté uniquement pour `UserPromptSubmit`).

Le seul moyen d'injecter du contenu visible par Claude sur `Stop` est `{"decision": "block", "reason": "..."}`.

**Why:** "block" sur Stop = "ne pas arrêter, continuer avec reason comme nouveau prompt". Ce n'est pas un blocage définitif — c'est le mécanisme d'injection sur cet événement.

**How to apply:** Toujours utiliser `decision: "block"` + `"once": true` pour les hooks Stop qui veulent injecter un rappel. Sans `once: true`, chaque tentative d'arrêt relance le hook → boucle infinie. `once: true` garantit une seule injection par session.

Pattern validé dans `learning-reminder.py` (claude-forge, 2026-05-08).
