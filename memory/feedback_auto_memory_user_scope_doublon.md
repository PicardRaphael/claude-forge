---
name: auto-memory-user-scope-doublon
description: ~/.claude/projects/.../MEMORY.md (auto-memory user-scope) doublonne memory/MEMORY.md projet a 90%. Purge sans risque apres diff. 10.8k tokens fantome charges chaque session.
metadata:
  type: feedback
---

**Constat empirique** 28 mai 2026, audit context tokens.

Le harness Claude Code charge DEUX memoires distinctes au demarrage :
1. `memory/MEMORY.md` (projet, dans le repo, ~6.7k tokens) chargee via `@memory/MEMORY.md` dans CLAUDE.md
2. `~/.claude/projects/C--Users-raphael-picard-neote-Documents-claude-forge/MEMORY.md` (auto-memory user-scope, ~10.8k tokens)

**Pourquoi le doublon** : depuis [[decision-memoire-dans-le-repo]] (migration memory dans le repo), l'user-scope est devenu un fantome historique jamais purge. Ecriture continue par /done auto-memory tool.

**Why** : 10.8k tokens charges chaque session = 4-5% budget Opus, 5% Sonnet. Pour zero valeur ajoutee.

**How to apply** :
1. AVANT toute purge : diff structurel `~/.claude/projects/.../MEMORY.md` vs `<repo>/memory/MEMORY.md` pour identifier les ~5-10 entrees uniques (a migrer dans projet)
2. Migrer les uniques dans `memory/` projet
3. Vider l'user-scope MEMORY.md (laisser le fichier vide pour eviter recreation auto)
4. Hook ou rule pour empecher /done de re-ecrire dedans : verifier que /done ecrit DANS memory/ projet (resolution via `git rev-parse --show-toplevel`)

Lien : [[feedback_consolidate_searches]] (UN fichier canonique par concept) + [[decision-memoire-dans-le-repo]].
