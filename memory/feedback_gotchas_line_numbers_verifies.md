---
name: gotchas-line-numbers-verifies-empiriquement
description: "Tout claim `fichier.py:N` dans CLAUDE.md/doc vérifié grep -n empirique AVANT relayage"
metadata:
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Cf [[erreur-gotchas-line-numbers-non-verifies-claudemd]] (doctrine canonique vault — verbatim Anthropic over-specified anti-pattern).

**Cas empirique session 3 neo_ia 22 mai 2026** : 2 gotchas relayés du plan ULTIME S1+S2 sans vérif :
- `react.py:151` — chemin n'existait pas (vrai `packages/shared_utils/shared_utils/engine/react.py:150`)
- `streaming.py:929` — aucun `gemini-2.5-flash` (hardcode dans 7 autres fichiers).

Détectés par advisor V2 post-write. Corrigés commit `96142b0`. Préférer chemin sans numéro OU pattern grepable si volatile.
