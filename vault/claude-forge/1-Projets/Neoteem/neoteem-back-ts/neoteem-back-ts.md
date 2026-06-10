---
titre: neoteem-back-ts
resume: Monorepo backend TS Loji — migration ia_back→neoia-api, Drizzle, MCP par client, développé 100% par Claude Code sous supervision, CI Bitbucket capteur primaire
aliases:
  - neoteem-back-ts
  - neoteem back ts
  - monorepo backend loji
  - neoia-api
  - monorepo ts neoteem
type: context
status: active
derniere-maj: 2026-06-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/neoteem-back-ts"
---
## Description

Monorepo backend TypeScript de [[Neoteem|Neoteem]] pour Loji, conçu « parfait par construction » : 100 % développé par Claude Code sous supervision humaine au terminal, qualité garantie par l'outillage (CI bloquante + hooks + agents), pas par l'espoir. Remplace [[ia_back]] (migré en `apps/neoia-api`) et prépare les serveurs MCP clients.

Repo : `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-back-ts` (Bitbucket neot-v2, branche défaut master). Source de vérité : `doc/cahier-des-charges.md` (CDC, ~700L, citer `CDC §X` jamais dupliquer). Epics dans `doc/epics/`.

## Stack

- pnpm 11 (workspaces + catalog) + Turborepo + Bun (runtime/tests) + TypeScript 6 + tsup — rôles distincts pnpm/Bun voulus
- Architecture hexagonale : `domain` ← `application` ← `db` (Drizzle, SEULE couche PG) ; apps = adaptateurs ; MCP n'importent que `@neoteem/api-client` (HTTP)
- Qualité CI (Bitbucket Pipelines, capteur primaire — CDC §19bis.1) : Biome, dependency-cruiser (frontières §16), jscpd, knip, StrykerJS mutation 2 étages (incrémental PR + full hebdo)
- Zod v4, `@hono/zod-openapi` (OpenAPI généré), erreurs RFC 9457, `numeric mode:'string'` partout

## Décisions gravées (ne jamais rouvrir sans Raphael)

- **Règle de tri fonctions PG (CDC §7.2)** : lecture simple → Drizzle builder ; logique métier IA-only qui évolue → réécrite TS ; écriture neuve → full Drizzle jamais `p_*` ; gros moteur stable → PG raw. La perf n'est JAMAIS l'argument pour sortir de PG.
- **Moteur `requete.*` = 4 fonctions raw DÉFINITIF** (`f_lance_requete`, `f_lance_requete_detail`, `f_donne_filtres`, `f_donne_saisie_assistee`) — un seul moteur, vérifié dans le code ia_back (9 juin 2026), jamais réécrit.
- **Parité stricte d'abord** : migration = reproduire le comportement à l'identique (diff vide `compareRows` requête par requête), optimiser dans une passe ultérieure dédiée.
- **ia_back = source de comportement, JAMAIS de modèle** : son code est potentiellement mal architecturé ; on reproduit le comportement observable avec l'architecture cible (fonctions de requête typées §7.3, pas d'objets Repository).
- **ws (Go) / WinDev = scope étanche** : ils appellent la BDD directement, ne consomment jamais le monorepo — réinternaliser ne casse rien pour eux (faux conflit ADR-005).
- **Tickets** : hiérarchie Epic→Story→Sous-tâche par LABELS (`IA-DEV` + `neoteem-back-ts` + domaine + one-shot/récurrent), epic Jira créé par un humain, parent validé avant stories, BRIEF auto-suffisant, TDD-as-done (le test EST le critère).

## Outillage .claude/ (E0, audité)

- 9 skills (feature, spec autonome, api-endpoint, drizzle-query, migration-parite, mcp-tool, test, go, notes) + `.skill-triggers.json` + `skill-activation.ts` (portage forge TS/Bun)
- 6 agents (architect Opus xhigh / test-writer + dev Sonnet / reviewer + performance + security-auditor Opus read-only sur déclencheur) — escalade structurée in-body, brief-then-direct
- 8 hooks TS/Bun same-stack, testés payloads réels : guards frontières/secrets/schéma, typecheck, git-guard (6 branches protégées), config-guard (sub-agents bloqués sur `.claude/**`+CDC via `agent_id` — discriminant officiel, jamais `agent_type` seul ni env var), memory-watcher (anti-saturation pattern forge)
- `memory/` versionnée dans le repo (pattern forge) ; `/go` = miroir EXACT des commandes CI (leçon : 4 pipelines cassés par gates locaux partiels — @types/bun TS6, biome ci, jscpd 5 Rust, turbo test squelettes)
- `scripts/ci-status.ts` : lecture pipelines Bitbucket par l'agent (token API requis)

## État (2026-06-09)

E0 Fondation LIVRÉ (direct master, sans tickets — décision Raphael) ; 6 branches env alignées (develop/test/prepilote/pilote/preprod = master à chaque validation E0). **Epic E1 migration proposé** (`doc/epics/E1-migration-ia-back.md`, 10 stories, chiffres réels : 15 entités, 22 use-cases, 16 routes) — en attente OK parent. Phase suivante : stories E1 → pipeline `/feature` par ticket.

## Liens

- [[ia_back]] — source de la migration (comportement, pas modèle)
- [[bdd]] — fonctions PG, gouvernance DDL (gate humain Jérôme+Raphael §7.4)
- [[Neoteem|Neoteem]] · [[Raphael-Picard|Raphael Picard]]
- [[anti-pattern-hookify-workflow-hooks]] — doctrine hooks appliquée au repo (CDC §19bis.2)
- [[workflow-claude-code-optimal]] — couches de test du code IA + cadence mutation (section 9 juin)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — pourquoi le pipeline vit dans une skill, pas un hook
