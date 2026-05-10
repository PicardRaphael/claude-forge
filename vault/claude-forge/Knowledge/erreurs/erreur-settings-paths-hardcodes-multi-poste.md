---
aliases:
- settings hardcoded paths
- hooks cassés multi-machine
- paths absolus settings.json
- claude code multi-poste
- git-synced settings broken
auteur: claude
contexte: claude-forge poste perso (rapha) — premier usage après pull depuis poste
  pro (raphael.picard_neote)
cree: 2026-05-08
derniere-maj: 2026-05-08
gravite: importante
resume: Settings Claude Code synchronisés via git contenaient des paths absolus user-spécifiques.
  Sur un autre poste, hooks Python échouent silencieusement avec No such file or directory.
tags:
  - "#type/erreur"
  - "#erreur/infra"
  - "#domaine/claude-code"
  - "#domaine/multi-poste"
titre: settings.json avec paths absolus hardcodés cassent en multi-poste
type: erreur
---
## Ce qui s'est passé

`/recap` lancé sur poste perso → flot d'erreurs `Python was not found` sur chaque PreToolUse/PostToolUse hook. Investigation :

1. **Python absent** — seuls les stubs Microsoft Store (`WindowsApps/python.exe`) étaient dans le PATH, pas un vrai Python.
2. **Paths hooks pointent sur l'autre poste** — tous les `command` dans `.claude/settings.json` référençaient `C:/Users/raphael.picard_neote/...` alors que ce poste est `C:/Users/rapha/...`.
3. **Marker path vault-query-guard également hardcodé** — même corrigé settings.json, le guard `vault-query-guard.py` cherche le marker à `C:/Users/raphael.picard_neote/.../.session-vault-queried`. Sur l'autre poste, ce path n'existe jamais → blocage permanent de tout Write sur vault/output/skills/agents.

Trois couches du même bug : settings.json + hooks Python + marker file.

## Pourquoi c'était une erreur

- `.claude/settings.json` est checké dans git → synchronisé entre postes.
- Mais il contient des **paths absolus user-spécifiques** qui diffèrent par machine.
- Les **hooks Python eux-mêmes** ont aussi des constantes `MARKER_PATH` hardcodées avec le user.
- `.claude/settings.local.json` était commit par erreur (devrait être local).

Résultat : pull depuis l'autre poste = système entier cassé silencieusement.

## Ce qu'il fallait faire

**Dans settings.json** : paths relatifs au repo, pas absolus.

```json
"command": "python \".claude/hooks/learning-reminder.py\""
```

**Dans les hooks Python** : dériver le path depuis `__file__` au lieu d'une constante.

```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
MARKER_PATH = os.path.join(PROJECT_ROOT, ".claude", ".session-vault-queried")
```

**Pour `.claude/settings.local.json`** : ajouter au `.gitignore`.

## Comment éviter à l'avenir

1. **Règle absolue** : aucun path absolu user-spécifique dans settings.json ni dans hooks Python. Toujours relatif au repo (`__file__` dans Python, paths relatifs dans JSON).
2. **Audit pré-commit** : grep `C:/Users/` ou `/home/` dans `.claude/settings*.json` et `.claude/hooks/*.py` → si match, c'est un bug.
3. **`.claude/settings.local.json` doit être dans `.gitignore`** — c'est le fichier prévu pour les overrides locaux.
4. **Hook de validation** : un PreCommit qui scan settings et hooks pour paths absolus.

## Procédure de récupération sur nouveau poste Windows

1. `winget install Python.Python.3.13`
2. **Désactiver App Execution Aliases** dans Settings Windows → off pour `python.exe` et `python3.exe` (sinon le stub Store intercepte)
3. **Redémarrer Claude Code** — sinon le PATH du process reste figé d'avant l'install
4. Sed-replace `<old_user>` → `<new_user>` dans `.claude/settings*.json` ET `.claude/hooks/*.py`

## Liens

- [[erreur-edit-direct-skills]]
- [[erreur-marker-ttl-blocage-agents]]
