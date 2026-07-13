---
description: Convention d'écriture hooks Windows — py launcher, ${CLAUDE_PROJECT_DIR}, forward slashes. Cross-machine obligatoire sur forge, ia_back, neo_ia, lojii.
---

# Hooks Windows — Convention cross-machine

## Template settings.json (correct)

```json
"command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.py\""
"timeout": 10
```

## Règles cross-machine

- **Interpréteur** : `py` (PEP 514 launcher) — jamais `python` ni `python3` (pointent vers Microsoft Store alias sur certaines machines)
- **Chemins** : `${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.py` — jamais chemin absolu `C:/Users/...`
- **Séparateurs** : forward slashes `/` — backslashes mangés par Bash
- **Timeout** : obligatoire (`timeout: N`, N ≤ 30) — sans timeout, freeze Claude Code indéfini
- **Chemins dans le script** : via `__file__` (`os.path.dirname(os.path.abspath(__file__))`)
- `shutil.which("outil")` avant tout appel d'outil externe — fail-open si absent

## Gotchas

- `${CLAUDE_PROJECT_DIR}` disponible UNIQUEMENT dans le champ `command` de settings.json — pas dans le script Python lui-même
- Chemins avec espaces → toujours quoter dans le JSON
- `py` absent → Python mal installé. Fallback : chemin absolu depuis `where python`
- Triplet `Write|Edit|MultiEdit` sur hooks PreToolUse écriture — oublier MultiEdit = trou architectural
- Backslashes dans heredoc Bash : doubler pour éviter interprétation

## Vérification

```bash
py --version      # doit pointer vers le vrai Python installé
python --version  # peut pointer vers Microsoft Store alias (no-op)
```

Si les deux ne pointent pas vers le même Python → utiliser `py` exclusivement.

Source : `memory/feedback_python_path_windows.md`
