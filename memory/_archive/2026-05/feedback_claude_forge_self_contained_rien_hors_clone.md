---
name: claude-forge-self-contained-rien-hors-clone
description: "claude-forge est self-contained : TOUT vit dans le clone git (agents, skills, hooks, vault, MCP, ET mémoire). Rien d'essentiel hors du repo. Mémoire = <repo>/memory/ via autoMemoryDirectory (pointeur user-scope par machine)"
metadata:
  type: feedback
---

claude-forge est un dossier **self-contained** : tout ce qui le définit suit le `git clone`. Avant de placer un état persistant hors du repo (`~/.claude/...`, dossier temp, chemin machine), se demander : « est-ce que ça survit au clone sur une autre machine ? ». Si non et que c'est essentiel → le mettre dans le repo.

**Why:** Session 2026-05-27 (Mémoire Portable). La mémoire (feedback_*, MEMORY.md) vivait dans `~/.claude/projects/<repo-encoded>/memory/`, hors du repo → perdue sur PC perso après clone. Dernière faille de portabilité. Migrée vers `<repo>/memory/`, chargée nativement via `autoMemoryDirectory` (user-settings, par machine). Le vault, lui, était déjà portable car dans `vault/`.

**How to apply:**
1. Mémoire forge = `<repo>/memory/` (versionné). Y écrire les feedbacks, pas dans `~/.claude/`.
2. Le pointeur `autoMemoryDirectory` dans `~/.claude/settings.json` est local à chaque machine (1 ligne, étape `install-forge`). Le contenu suit le clone.
3. Confidentialité : `memory/` est non-confidentiel par principe. Item sensible → `memory/private/` ou `memory/*-private.md` (gitignored).
4. Toute nouvelle dépendance à un chemin hors repo = signal d'alerte portabilité. Préférer un chemin relatif au repo (`${CLAUDE_PROJECT_DIR}` dans hooks).

Référence vault : [[decision-memoire-dans-le-repo]].
