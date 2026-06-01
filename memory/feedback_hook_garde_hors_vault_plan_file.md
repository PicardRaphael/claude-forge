---
name: hook-garde-hors-vault-bloque-plan-file
description: Hook qui bloque toute écriture hors-périmètre intercepte le plan file ~/.claude/plans/ en faux positif et casse le plan mode. Exception explicite requise.
metadata:
  type: feedback
---

Un hook PreToolUse Write/Edit qui bloque **toute écriture hors d'un périmètre strict** (vault, repo) avec `if not normalized.startswith(PERIMETRE): exit(2)` attrape le **plan file** du plan mode (`~/.claude/plans/*.md`) en faux positif → plan mode cassé.

**Why:** le plan file est un fichier **système du harness** Claude Code, hors de tout repo de code. Un guard scopé par repo parent (neo_ia, forge) y est immunisé (hors repo = autorisé) ; un guard scopé par vault strict (neoteem-brain `guard-external-writes.py`) le bloque car `~/.claude/plans/` n'est sous aucun repo connu du hook.

**How to apply:** ajouter une exception explicite EN TÊTE du hook, avant le filtre générique : `PLANS_DIR = normcase(normpath(join(expanduser("~"), ".claude", "plans")))` puis `if normalized.startswith(PLANS_DIR): sys.exit(0)`. Gotcha Windows : `normcase` (lowercase) comme les autres exceptions. Blocage secondaire : le classifier auto-mode **refuse l'édition autonome** de tout hook de sécurité (Security Weaken / Self-Modification) — édition manuelle Raphael ou `.proposed`. Ne pas contourner. Détail vault : [[erreur-hook-garde-hors-vault-bloque-plan-file]].
