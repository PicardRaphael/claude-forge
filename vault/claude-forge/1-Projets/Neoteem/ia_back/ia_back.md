---
titre: ia_back
resume: Backend IA Neoteem — FastAPI Python, agents autonomes, RAG, pgvector, 1000+ outils
aliases:
  - ia_back
  - ia back
  - backend ia
  - api ia
  - back ia
type: context
status: active
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/ia_back"
---
## Description

Backend IA de [[Neoteem|Neoteem]]. FastAPI Python, architecture neuro-symbolique, agents autonomes, RAG hybride pgvector+RRF. Scale 1000+ outils.

## Stack

- Bun + Hono + @hono/zod-openapi + Drizzle ORM + Zod + bun:test
- Architecture hexagonale, pas de formatter/linter
- PostgreSQL, pgvector, MCP PostgreSQL (read-only)
- Gemini (Vertex AI), Claude

## Composants Claude Code (audit 2026-05-08)

- **15 agents opus** : architect, debugger, codebase-analyst, security-auditor (high) + api-designer, code-reviewer, dev, test-writer... (medium)
- **28 skills** : 3 création, 3 migration, 6 qualité, 9 référence, 3 schema, 2 update, 1 recap
- **14 rules** : agent-delegation, check-before-create, database-rules, quality-gates...
- **8 hooks** TypeScript/Bun : architect-guard, commit-guard, typecheck, GChat webhook...

## Contraintes

- Migration PG → applicatif (200+ tables, 1000+ fonctions)
- Projet principal du collègue Jérôme
- Emplacement : `neot-v2/ia_back` (Bitbucket, branche `develop`)

## Liens

- [[Neoteem|Neoteem]]
- [[Raphael-Picard|Raphael Picard]]


## Correction stack mai 2026

**Drizzle ORM n'est PAS utilisé.** Le projet utilise `postgres.js` (SQL template literals). Le CLAUDE.md et 23 fichiers agents/skills/rules ont été corrigés le 2026-05-21. Il reste ~64 occurrences dans les exemples de code des skills references/ — refacto planifiée.

Stack corrigée : Bun + Hono + @hono/zod-openapi + **postgres.js** + Zod + bun:test


## Migration vers le monorepo TS (juin 2026)

ia_back est la **source de la migration** vers [[neoteem-back-ts]] (epic E1, `apps/neoia-api`) : 15 entités, 22 use-cases, 16 routes, 17 repositories (mesuré 9 juin 2026). Règle gravée : ia_back fournit le **comportement** (parité de résultat requête par requête), jamais le modèle d'architecture. À terme, ce repo sera archivé.
## Refonte hooks 22 mai 2026

Suppression de 7 hooks workflow (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers) suite à friction 6×. Doctrine encodée dans `rules/quality-gates.md` + `rules/when-to-architect.md`. Architect split en `architect-quick` (sonnet) + `architect-deep` (opus xhigh).

Hooks restants (7) : `typecheck`, `guard-core-imports`, `guard-pg-repo-readonly`, `guard-test-scope`, `on-push-notify`, `session-health`, `spec-brief-boundary-guard`. Tous = lint/test/security/observabilité légitimes selon doctrine Anthropic.

Voir [[raisonnement-22mai-doctrine-vs-enforcement]].
