---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-21
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Tests comportementaux terminés sur neo_ia (25/25) et ia_back (32/41, 0 FAIL réel) — les deux repos sont au niveau production.

## Dernière session (2026-05-21)
### Decisions prises
- Pattern behavioral-dispatch-test capitalisé comme Phase 7 du workflow agentic engineering
- ia_back CLAUDE.md corrigé : Drizzle→postgres.js (le code n'a jamais utilisé Drizzle)
- api-designer ia_back : instruction neo-brain-dev-ia déplacée en étape 0 bloquante
- Prompts de test corrigés 3 fois (fausses prémisses, hooks en cascade, /go sans diff)
- IDOR documenté sur /api/v1/coproprietes/:id/conseil-syndical

### En cours
- neo_ia : fix conftest.py pushé (4ab67ef), pipeline TDD validé en conditions réelles
- ia_back : 4 commits pushés (api-designer, CLAUDE.md, Drizzle→postgres.js 23 fichiers, artifacts)
- Reste ~64 occurrences Drizzle dans sql-best-practices/references/ et connect-table (refacto future)

### Prochaines etapes
- Refacto Drizzle→postgres.js dans les exemples de code des skills ia_back
- Corriger IDOR conseil-syndical avant prod
- Lancer les scénarios 1 et 2 ia_back avec des prompts corrigés (vrais noms de tables/fonctions)

## Fils ouverts
- neo_ia : get_lots_archives_immeuble en cours de dev (questions architect répondues, session active)
- Proposition /test-dispatch refusée — Raphael a fait autrement
- neo_ia scénario 1 original (search_acteur) abandonné — doublon détecté

## Liens
[[Raphael-Picard]]
[[Claude-Forge]]
[[pattern-behavioral-dispatch-test]]
[[synthese-audit-coherence-neo-ia-ia-back]]
