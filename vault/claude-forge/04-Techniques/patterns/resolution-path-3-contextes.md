---
titre: "Résolution de path par contexte d'exécution — skill / hook / settings / .mcp.json"
resume: "Chaque contexte d'exécution Claude Code résout le chemin du repo différemment : skill = git rev-parse, hook = __file__, settings command = ${CLAUDE_PROJECT_DIR}, .mcp.json = paths relatifs au cwd. Table empirique avec preuve par ligne."
aliases:
  - "résolution path contextes"
  - "resolution path 3 contextes"
  - "CLAUDE_PROJECT_DIR disponibilité"
  - "git rev-parse vs __file__ vs CLAUDE_PROJECT_DIR"
  - "chemin repo skill hook settings"
  - "path resolution claude code"
domaine: claude-code
type: technique
derniere-maj: 2026-05-27
auteur: claude
sources:
  - "Session 2026-05-27 — chantier Mémoire Portable étape 7 (adaptation done/recap/session-reminder)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/portabilite"
---

# Résolution de path par contexte d'exécution

Pour résoudre la racine du repo (et donc des chemins comme `<repo>/memory/`), **le mécanisme correct dépend du contexte d'exécution**. La variable `${CLAUDE_PROJECT_DIR}` du harness n'est PAS universelle : elle n'est peuplée que dans certains contextes. Utiliser le mauvais mécanisme produit une valeur vide silencieuse (faux constat "dossier vide").

## Table de vérité (vérifiée empiriquement, 27 mai 2026)

| Contexte | `${CLAUDE_PROJECT_DIR}` dispo ? | Mécanisme correct | Preuve empirique |
|----------|-------------------------------|-------------------|------------------|
| **Skill** (Bash lancé par la skill) | ❌ NON — `$CLAUDE_PROJECT_DIR` est vide dans le shell | `$(git rev-parse --show-toplevel)` | `echo "[$CLAUDE_PROJECT_DIR]"` → `[]` vide ; `git rev-parse --show-toplevel` → repo root correct (27 mai) |
| **Hook** (script Python) | ❌ NON utilisé — aucun hook forge ne le lit | `os.path.dirname(os.path.abspath(__file__))` puis remonter | Prior art `grep CLAUDE_PROJECT_DIR .claude/hooks/` → 0 match. Test `session-reminder.py` exécuté depuis `/tmp` → résout sa mémoire correctement (robuste au cwd). `__file__` > `git rev-parse` car robuste hors-repo (27 mai) |
| **settings.json** (string `command`) | ✅ OUI — expansé par le harness dans la string | `${CLAUDE_PROJECT_DIR}` directement dans la commande | `"command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/session-reminder.py\""` (settings.json L125) fonctionne |
| **.mcp.json** (args/env d'un MCP) | ❌ NON — pas de variable d'env Claude Code | Paths relatifs au cwd (`./wrapper.mjs`) | Voir [[mcp-paths-relatifs-portabilite]] — Claude lance le MCP avec cwd = dossier du `.mcp.json` |

## Nuance clé : expansion harness ≠ environnement du process

`${CLAUDE_PROJECT_DIR}` dans la **string command** de settings.json est expansé par le harness AU MOMENT de construire la ligne de commande. Cela ne signifie PAS que `os.environ["CLAUDE_PROJECT_DIR"]` soit peuplé **à l'intérieur** du process Python lancé. Les deux sont indépendants — c'est pourquoi un hook ne doit pas compter sur `os.environ`, mais sur `__file__`.

## Pourquoi `__file__` est supérieur pour les hooks

- **Déterministe** : pas de cas vide à gérer (contrairement à `os.environ.get`)
- **Zéro dépendance harness** : marche même si le harness change son injection de variables
- **Zéro fork process** : pas de `subprocess.run(["git", ...])`
- **Robuste au cwd** : un hook peut être déclenché avec un cwd imprévisible. `__file__` pointe toujours vers l'emplacement réel du script. Prouvé : `session-reminder.py` lancé depuis `/tmp` trouve quand même sa mémoire.

```python
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))  # .claude/hooks/
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)                 # .claude/
repo_root = os.path.dirname(_CLAUDE_DIR)                 # <repo>/
```

## Anti-patterns

- ❌ `${CLAUDE_PROJECT_DIR}/memory` dans une skill Bash → variable vide → chemin `/memory` faux
- ❌ `os.environ["CLAUDE_PROJECT_DIR"]` dans un hook → non garanti peuplé, dépendance fragile
- ❌ Supposer que l'expansion dans la string command settings.json implique la présence dans `os.environ` du process enfant
- ❌ `git rev-parse` dans un hook → fonctionne si cwd dans le repo, mais échoue si déclenché hors-repo ; `__file__` n'a pas ce risque

## Liens

- [[mcp-paths-relatifs-portabilite]] — le 4e contexte (.mcp.json), paths relatifs au cwd
- [[comment-creer-skill]] — applique le mécanisme skill (git rev-parse)
- [[comment-creer-hook]] — applique le mécanisme hook (__file__)
- [[architecture-decision-memoire-portable-import]] — chantier qui a révélé l'asymétrie
- [[decision-memoire-dans-le-repo]] — décision mémoire portable
- [[reference_python_windows_cross_machine]] — py launcher, paths absolus hooks
