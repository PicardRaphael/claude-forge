---
name: never-commit-foreign-repos
description: Never git init, commit, or push in repos that are not claude-forge — never ask about git setup in other projects
type: feedback
---

Ne JAMAIS initialiser git, commit, ou push dans des repos externes de facon AUTONOME.
Ne JAMAIS poser la question "tu veux que j'initialise git ?" dans un autre projet.

**Exception :** Si l'utilisateur demande explicitement de commit/push dans un repo externe (ia_back, neoteem-brain, neo_ia...), c'est OK. La regle interdit l'initiative autonome, pas l'obeissance a une demande explicite.

**Why:** L'utilisateur gère lui-même git pour ses projets. Proposer d'init/commit de facon proactive est intrusif et dangereux.

**How to apply:** Quand on analyse un projet externe (via /analyze-project ou /add-dir), on ne touche JAMAIS au git sauf demande explicite. On se limite à lire, analyser, et proposer des fichiers de config Claude (.claude/, CLAUDE.md, rules, agents).
