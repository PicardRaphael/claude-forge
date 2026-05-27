---
name: python-path-windows-hooks
description: "Sur Windows, hooks Python doivent utiliser le chemin absolu Python313, pas juste \"python\" (alias Microsoft Store)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42f0ff3e-7431-4682-bf0b-f2823840a715
---

## Règle

Sur Windows, TOUJOURS utiliser le chemin absolu pour Python dans les hooks Claude Code :
`/c/Users/raphael.picard_neote/AppData/Local/Programs/Python/Python313/python.exe`

Ne JAMAIS utiliser `python` seul — c'est un alias Microsoft Store qui ne fonctionne pas.

**Why:** Les hooks forge utilisaient `python "$(git rev-parse...)"` et échouaient silencieusement avec "Python est introuvable". Détecté le 2026-05-12, tous les hooks corrigés d'un coup.

**How to apply:** 
- Vérifier chaque settings.json pour `python` sans chemin absolu
- neo_ia utilise `uv run python` (correct — uv gère le venv)
- ia_back utilise Bun (pas concerné)
- forge utilise Python direct → chemin absolu obligatoire
