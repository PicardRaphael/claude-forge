---
name: python-path-windows-hooks
description: "Hooks Python sous Windows — lancer avec le launcher `py` (PEP 514), jamais `python`/`python3` seul (alias Microsoft Store, échec silencieux) et jamais un chemin absolu vers un Python313 (casse au changement de machine ou de version)"
trigger: hook, settings.json, python, py launcher, windows, interpreteur, PreToolUse, SessionStart
metadata:
  node_type: memory
  type: feedback
---

## Règle

Dans un hook Claude Code sous Windows, l'interpréteur s'écrit **`py`** (launcher PEP 514) :

```json
"command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/mon-hook.py\""
```

Deux formes à ne pas utiliser, pour deux raisons différentes :

- **`python` ou `python3` seul** → peut résoudre vers l'alias Microsoft Store, qui échoue **silencieusement** (« Python est introuvable »). C'est l'incident d'origine du 12 mai 2026.
- **Un chemin absolu vers un interpréteur** (`.../Python313/python.exe`) → casse dès que la machine ou la version change. Mesuré le 29 juillet 2026 : `mcp-forge-brain/start.bat` épinglait Python313 alors que la machine tournait en 3.14.2, et 26 hooks de neo_ia utilisaient `python` nu.

**Why :** les deux formes produisent le même symptôme — un hook qui ne s'exécute pas sans que rien ne le signale. Le chemin absolu ajoute la casse cross-machine (deux PC, noms d'utilisateur différents).

**How to apply :**
- Vérifier l'interpréteur réel : `py .claude/scripts/check-portability.py` (échoue en exit 1 s'il trouve `python` nu ou un chemin utilisateur en dur)
- Chemins dans le script : `os.path.dirname(os.path.abspath(__file__))`, jamais en dur
- `${CLAUDE_PROJECT_DIR}` n'est disponible que dans le champ `command` de `settings.json`
- Stack TypeScript (neoteem-back-ts) : `bun` est l'interpréteur légitime, cette règle ne s'applique pas
