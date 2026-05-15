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
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/ia-back"
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
