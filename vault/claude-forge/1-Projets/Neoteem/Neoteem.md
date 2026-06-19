---
titre: Neoteem
resume: Entreprise où Raphael est Lead IA — solutions IA sur-mesure, agents autonomes, RAG. Note ombrelle des repos + dispositif d'agents Claude Code
aliases:
  - neoteem
  - la boîte
  - le taf
  - boulot
  - neoyah
type: context
status: active
derniere-maj: 2026-06-19
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/neoteem"
---
## Description

Entreprise où [[Raphael-Picard|Raphael]] travaille comme Lead Ingénieur IA & Architecte Solutions depuis novembre 2025 (CDI remote).

## Responsabilités

- Décision stratégique & innovation : choix architecturaux IA (Gemini, Claude)
- Architecture neuro-symbolique (scale 1000+ outils)
- Optimisation recherche hybride pgvector + RRF
- Pilotage pôle IA, acculturation équipes
- UX IA-friendly pour profils non-techniques

## Repos

- **[[ia_back|ia_back]]** : backend IA FastAPI/Bun-Hono-postgres.js — **14 agents** Claude Code
- **[[neo_ia|neo_ia]]** : monorepo Python NeoChat/NeoDoc/NeoMail — **14 agents** Claude Code
- **[[neoteem-brain|neoteem-brain]]** : vault Obsidian métier (682+ notes) — **5 agents** Claude Code
- **[[neoteem-back-ts|neoteem-back-ts]]** : monorepo backend TS (migration PG→TS)
- **[[bdd|bdd]]** : repo PG/PL-pgSQL (2779 fichiers)

## Stack

Python (FastAPI), TypeScript (Bun/Hono), Gemini (Vertex AI), Claude, PostgreSQL, pgvector, MCP, n8n

## Contraintes

- Org Team bloque GitHub cloud → tout en local (Task Scheduler)
- 100% opus sur repos projet, zero sonnet pour le jugement ; sonnet pour l'exécution
- Repos autonomes (collègues sans claude-forge)

## Dispositif d'agents Claude Code

> Inventaire vérifié sur disque le 2026-06-19 (33 agents projet, hors `agent-memory/`). Modèle : **opus = jugement/architecture, sonnet = exécution, haiku = scan/analyse mécanique**. Effort calibré par type (xhigh agentique profond, high comparatif/jugement, medium maintenance).
> Gouvernance du rôle (qui maintient, bus factor, frontière perso/team) : [[agent-manager-neoteem]].

### neo_ia — 14 agents (monorepo Python NeoChat/NeoDoc/NeoMail)

| Agent | Modèle | Effort | Rôle / quand l'invoquer |
|---|---|---|---|
| dev-lead | opus | xhigh | Chef dev senior, vision monorepo complète — feature cross-app ou changement multi-packages |
| dev-neochat | sonnet | high | Dev NeoChat (orchestration multi-agent Gemini) — `apps/neochat/` |
| dev-neodoc | sonnet | high | Dev NeoDoc (pipeline RAG) — périmètre NeoDoc |
| dev-neomail | sonnet | high | Dev NeoMail — périmètre NeoMail |
| dev-shared-utils | sonnet | high | Infra partagée (engine ReAct, LLM factories, billing, auth) — `packages/shared_utils/` |
| dev-shared-tools | sonnet | high | LangChain tools partagés — `packages/shared_tools/` |
| architect-deep | opus | xhigh | Architecte read-only design/review multi-fichiers — avant nouveau module/agent |
| codebase-analyst | haiku | high | Analyste read-only (structure, deps, santé) — health check sans modif |
| prompt-eval-runner | sonnet | high | Tests DeepEval après modif de prompts système — régression prompts |
| reviewer | opus | high | Review read-only Python (plan, types, OWASP IA, LangGraph) — après impl, avant merge |
| security-auditor | opus | high | Audit sécu read-only (prompt injection, PII, hallucination, token leak) — PR auth/endpoint/tool/web-fetch |
| performance | opus | high | Review perf (N+1, index SQL, latence LangGraph, coûts tokens) — PR queries/streaming/chemins chauds |
| test-writer | sonnet | high | Génère tests Python (happy/edge/erreur, max 3/behavior) — tests délégués explicitement |
| outcomes-grader | opus | high | Évalue livrable vs RUBRIC.md (PASS/FAIL/PARTIAL) — exclusif au skill outcomes-test |

### ia_back — 14 agents (backend IA, migration PG→TS hexagonale)

| Agent | Modèle | Effort | Rôle / quand l'invoquer |
|---|---|---|---|
| dev | sonnet | high | Implémente features (Bun + Hono + postgres.js + TS) — "implémente", "crée l'endpoint", post-plan architecte |
| architect-deep | opus | xhigh | Conception/review archi multi-fichiers — fichiers critiques (env, migrations, schema, auth, routers) ; pas pour hotfix < 30 LOC |
| api-designer | opus | high | Conçoit endpoints REST depuis besoin métier — "j'ai besoin d'un endpoint", "crée une API pour" |
| debugger | sonnet | high | Diagnostic cause racine avant correction — "ça marche pas", stack trace, test qui échoue |
| test-writer | sonnet | high | TDD strict, UN test échouant à la fois (phase red) — AVANT le dev |
| reviewer | opus | high | Review archi/conventions/équivalence migration PG→TS — après impl, avant commit |
| security-auditor | opus | high | Audit sécu stack Neoteem (injections, vulnérabilités, données user) — avant prod d'un endpoint |
| performance-engineer | opus | high | Profile/optimise perf (N+1, indexes, lenteurs) — "c'est lent", avant prod |
| outcomes-grader | opus | high | Évalue livrable vs RUBRIC.md — exclusif au skill outcomes-test |
| codebase-analyst | haiku | high | Health check global du codebase + plan priorisé |
| db-inspector | sonnet | high | Explore le schéma PostgreSQL via MCP — "montre la table", "les FK de", "explore la base" |
| repo-functions-analyzer | haiku | high | Analyse repo externe de fonctions PG (conventions f_/p_/proc_/tr_) — contexte pour migrate-function |
| schema-mapper | sonnet | high | Mappe la BD complète → doc par domaine `doc/schemas/*.md` — "documente le schéma" |
| refactor-pg-function | opus | xhigh | Migre fonction PG stockée → archi hexagonale TS — "migre f_", "refactor function" |

### neoteem-brain — 5 agents (vault Obsidian métier)

| Agent | Modèle | Effort | Rôle / quand l'invoquer |
|---|---|---|---|
| repo-analyzer | sonnet | high | Analyse un repo en profondeur → doc technique dans le vault — "analyse ce repo", "documente [repo]" |
| vault-enricher | sonnet | high | Importe Confluence/Jira dans le vault — import/màj depuis Confluence ou Jira |
| vault-linker | sonnet | high | Structure le vault (liens + MOCs) — après création de notes par repo-analyzer/vault-enricher |
| sync-checker | sonnet | high | Audit intégrité vault (frontmatter, wikilinks cassés, orphelins) + rapport |
| vault-validator | sonnet | medium | Conformité frontmatter v2 (read-only) — "valide le vault", "check conformité v2" |

### Patterns transverses observés

- **Trio qualité opus partout** (reviewer + security-auditor + performance) sur les deux backends IA — review systématique avant merge/prod.
- **outcomes-grader + codebase-analyst dupliqués** à l'identique sur neo_ia et ia_back → candidats à un plugin Neoteem distribué (cf [[agent-manager-neoteem]] frontière perso/team).
- **architect-deep cloné** sur les deux backends (même intention, stack adaptée) — opus/xhigh.
- **neoteem-brain = agents vault** (sonnet/haiku, pas de jugement opus) : maintenance documentaire, pas de dev.

## Liens

- [[Raphael-Picard|Raphael Picard]]
- [[Claude-Forge|Claude-Forge]]
- [[agent-manager-neoteem]] — gouvernance du dispositif (qui maintient, bus factor, perso vs team)
- [[archi-backs-neoteem]] — architecture des backends
- [[comprendre-neoteem-vue-responsable-ia]] — vue Lead IA

## Stratégie

- [[neoteem-agentic-engineering-mapping]] — Validation externe du workflow Neoteem par le framework Karpathy (Sequoia AI Ascent 2026). Mapping complet neo_ia + ia_back + forge vs concepts Software 3.0.
