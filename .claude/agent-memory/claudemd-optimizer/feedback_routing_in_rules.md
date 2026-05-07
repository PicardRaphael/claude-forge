---
name: routing-table-in-rules
description: Les tables dispatch (situation → action) appartiennent dans .claude/rules/, pas dans CLAUDE.md
type: feedback
---

Les tables de type "Situation | Action" qui routent vers des agents/skills sont du routing, pas de la configuration.

Le feedback `rules-for-routing` (MEMORY.md forge) dit explicitement : routing dans `.claude/rules/`, pas CLAUDE.md.

**Why:** CLAUDE.md doit rester ~100 lignes. Les tables dispatch grossissent et ne préviennent pas d'erreurs directement — elles délèguent. Mieux dans une rule dédiée qui peut évoluer sans toucher le fichier principal.

**How to apply:** Quand CLAUDE.md contient une table "situation → invoke X", la déporter dans `.claude/rules/comportement-proactif.md` et remplacer par une ligne pointeur. Les rows qui dupliquent la Posture ou d'autres rules → supprimer (pas migrer).
