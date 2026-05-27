---
name: rules-for-routing-not-claudemd
description: Le routing agents et les workflows vont dans .claude/rules/, PAS dans CLAUDE.md. CLAUDE.md = contexte projet. Rules = comportement obligatoire.
type: feedback
---

## .claude/rules/ = comportement obligatoire de Claude

Les rules sont le bon endroit pour :
- `agent-delegation.md` — QUI appeler QUAND (workflows complets)
- `skill-navigator.md` — QUELLE skill charger quand ambigu
- `database-rules.md` — règles SQL strictes
- Toute règle MANDATORY que Claude doit suivre

## CLAUDE.md = contexte projet

CLAUDE.md contient :
- Contexte du projet (ce qu'on fait, pourquoi)
- Config (paths, stack, conventions)
- Standards de code
- Un pointeur vers `.claude/rules/` pour les règles

**Why:** Validé sur le projet neo_ia qui utilise `.claude/rules/` avec succès pour le routing agents, la navigation skills, et les règles DB. Le CLAUDE.md de neo_ia ne contient que le contexte projet.

**How to apply:**
- Routing/workflows → `.claude/rules/agent-delegation.md`
- Navigation skills → `.claude/rules/skill-navigator.md`
- Règles DB/SQL → `.claude/rules/database-rules.md`
- Contexte projet → `CLAUDE.md`
