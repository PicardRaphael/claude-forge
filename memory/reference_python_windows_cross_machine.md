---
name: python-windows-cross-machine
description: "Pattern py launcher Windows pour hooks cross-machine — jamais python, jamais path absolu, jamais antislash echappes"
type: reference
---

# Pattern Python Windows cross-machine

## Le bon pattern

Dans tout fichier `.json`, `.md` ou agent où un hook lance Python sur Windows :

```json
"command": "py \"$(git rev-parse --show-toplevel)/.claude/hooks/X.py\""
```

**`py`** = Python launcher Windows officiel, installé avec tout Python officiel. Cross-machine, cross-version, pas de username.

## Les 3 mauvais patterns à NE PLUS UTILISER

### ❌ `python` (alias MS Store cassé)
```json
"command": "python script.py"
```
Sur certains PC, `python` ouvre Microsoft Store ou pointe vers une install fantôme cassée. Erreur silencieuse exit 127.

### ❌ Chemin absolu avec antislash JSON-échappé
```json
"command": "C:\\Users\\xxx\\Python313\\python.exe script.py"
```
Sur Git Bash, `\\` est interprété comme escape et **les antislashes sont mangés** → `C:Usersxxx...` → command not found.

### ❌ Chemin POSIX user-specific
```json
"command": "/c/Users/raphael.picard_neote/AppData/Local/Programs/Python/Python313/python.exe script.py"
```
Marche sur la machine où le username est `raphael.picard_neote`. **Casse sur autre machine** du même user (username différent).

## Cross-platform

| OS | Commande |
|----|----------|
| Windows | `py` |
| macOS / Linux | `python3` |

Pour repos cross-platform : shebang `#!/usr/bin/env python3` dans le `.py` + `chmod +x` + `command: "$(git rev-parse --show-toplevel)/.claude/hooks/X.py"`. Le shebang résout.

## Vérif systématique

Avant de modifier `.claude/settings.json` (ou tout autre config hook), grep TOUT :

```bash
grep -rn 'python \|python.exe' .claude/ | grep -v ".pyc\|.proposed"
```

Inclut les hooks embedded dans agents (`PostToolUse` dans `agents/python-dev.md`), pas juste `settings.json`.

**Why:** Bug détecté 2026-05-22 — 3 itérations sur path Python avant de trouver `py`. Aussi un hook embedded dans `python-dev.md` ligne 19 oublié à l'audit settings.json (pattern : audit settings.json ≠ audit complet config hooks).

**How to apply:** Tout nouveau hook Python sur Windows → `py`. Toute modification config existante → grep complet, pas juste settings.json.
