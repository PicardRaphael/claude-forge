---
name: windows-hooks-cross-machine
description: ALWAYS invoke when writing or reviewing Windows hook configurations in settings.json. DO NOT use hardcoded paths or bare python command -- use py launcher and ${CLAUDE_PROJECT_DIR} for cross-machine portability.
allowed-tools: Read, Write, Edit
effort: high
user-invokable: true
---

## Role

Garantir que les hooks Windows dans .claude/settings.json sont portables entre machines.
Applicable a forge, ia_back, neo_ia, lojii.

## Template settings.json

Commande hook correcte dans settings.json :
  py "${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.py"
  avec timeout: 10

## Regles cross-machine

FAUX : chemin absolu hardcode type C:/Users/raphael/.../hook.py
VRAI : ${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.py

FAUX : commande python hook.py ou python3 hook.py
VRAI : py hook.py (PEP 514 launcher, resout Python installe)

FAUX : backslashes dans Bash -- Bash les mange
VRAI : forward slashes C:/path/to/hook.py

## Microsoft Store Python -- gotcha critique

Sur certaines machines, python et python3 pointent vers le Microsoft Store alias (no-op).
Le py launcher (PEP 514) bypasse ce piege en cherchant le vrai Python installe.
Verifier : py --version vs python --version -- doivent pointer vers le meme Python.

## Timeout obligatoire

Tout hook DOIT avoir timeout N (N <= 30 secondes).
Sans timeout, un hook bloque freeze Claude Code indefiniment.

## Gotchas

- ${CLAUDE_PROJECT_DIR} disponible UNIQUEMENT dans le champ command des hooks settings.json
- Chemin avec espaces : toujours quoter dans le JSON
- py launcher absent : Python mal installe. Fallback : chemin absolu depuis where python
- Hook PreToolUse triplet obligatoire : matcher Write|Edit|MultiEdit -- oublier MultiEdit = trou architectural
- Backslashes dans heredoc Bash : les doubler pour eviter interpretation

## Apprentissage

Feedback source : feedback_python_path_windows_hooks.md + feedback_hooks_absolute_paths.md
Pattern valide : py launcher + ${CLAUDE_PROJECT_DIR} = portabilite garantie entre machines Windows.
Si nouveau gotcha Windows decouvert -> ajouter ici.
