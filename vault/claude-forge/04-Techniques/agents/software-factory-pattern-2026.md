---
aliases:
  - software factory pattern
  - 7 agents pattern Claude Code
  - feature factory Claude
  - researcher story spec backend frontend verifier validator
  - vibe coding ceiling solution
  - structured agent chain
resume: "Pattern '7 agents software factory' (Sairahul + FreeCodeCamp + dev.to + Heeki Park, 2026) — researcher / story / spec / backend / frontend / verifier / validator avec 3 human checkpoints. Consensus communauté mai 2026."
derniere-maj: 2026-05-26
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#statut/canonique"
---

# Software Factory Pattern — 7 agents structurés

## Diagnostic du problème (vibe coding ceiling)

Un single Claude Code session qui fait TOUT (analyst + architect + backend + frontend + tests + review) :
- Day 1 : magique
- Day 30 : on supervise plus qu'on code
- Wrong assumptions compound silencieusement à travers modèles → APIs → UI
- Pattern observé chez de nombreux devs depuis 2025

## La structure 7 agents

| # | Agent | Tools | Responsabilité |
|---|-------|-------|----------------|
| 1 | **Researcher** | Read, Grep, Glob | Map codebase, patterns, risks, files concernés |
| 2 | **Story Writer** | Read | User story + acceptance criteria + edge cases |
| 3 | **Spec Writer** | Read, Grep, Glob | Technical brief : data model, API, frontend, tests |
| 4 | **Backend Builder** | Read/Edit/Write/Bash scopés backend | API, services, jobs, unit tests backend |
| 5 | **Frontend Builder** | Read/Edit/Write/Bash scopés frontend | Components, hooks, UI tests |
| 6 | **Test Verifier** | Read/Edit/Write tests + Bash | Acceptance tests vs user story |
| 7 | **Validator** | Read, Grep, Glob | Compare implementation vs brief, sévérité C/I/M |

## Les 3 human checkpoints

1. **Approve story** (entre 2 et 3)
2. **Approve brief** (entre 3 et 4) — catch les "store IDs in memory" avant 10 fichiers
3. **Approve PR** (après 7)

## Doctrine de tool restriction

Validator = read-only OBLIGATOIRE (anti-self-grading)
Researcher = read-only OBLIGATOIRE (no edits avant compréhension)
Builders = scopés folders (backend ne touche pas frontend et vice-versa)

## Origines documentées (consensus)

- **Sairahul (@sairahul1)** — tweet épinglé 25 mai 2026, 1.25M vues, 3.5K bookmarks
- **FreeCodeCamp** — article "How to Build a Software Factory with Claude Code"
- **dev.to** — javatarz "Multi-Agent Development Workflows"
- **Heeki Park** (Medium) — Collaborating with agents teams
- **VoltAgent** — repo `awesome-claude-code-subagents` (100+ subagents)
- **eesel.ai** — "Claude Code multiple agent systems: Complete 2026 guide"
- **Panaversity** — Agent Factory (Chapter 16 spec-driven dev)

Tous décrivent la MÊME structure avec les MÊMES noms d'agents → c'est un pattern qui s'est cristallisé dans la communauté.

⚠️ Origine exacte non tracée — probablement seed Anthropic docs + relais communauté début 2026.

## Critique technique (croisement avec autres sources)

Voir [[will-vs-ecc-deux-doctrines-anthropic]] pour la résolution complète.

**Points forts** :
- ✅ Tool restriction = aligné Anthropic
- ✅ Validator read-only séparé = anti-self-grading
- ✅ Human checkpoints = bon pattern

**Points faibles** :
- ⚠️ "7 agents systématique" sans threshold = ignorer [[google-mit-scaling-agent-systems-2025]] (single agent >45% → multi inutile)
- ⚠️ Backend/Frontend split rigide pose problème sur features cross-stack
- ⚠️ Aucune mesure eval livrée par les sources (vs Will Stock Pilot 62%→92% mesuré)

## Quand l'utiliser

✅ Features bien définies, scope clair, > 5 fichiers à toucher
✅ Onboarding d'un nouveau dev (chain pédagogique)
✅ Codebases legacy avec patterns à respecter

❌ Bug fix one-line (overhead inutile)
❌ Exploration / prototype (déstructure le flow)
❌ Features cross-stack tight coupling

## Implications forge

Notre setup actuel a déjà :
- ✅ `cc-advisor` (~ researcher pre-prompt)
- ✅ `spec` skill (~ Story + Spec Writer combinés)
- ✅ `project-auditor` (~ researcher)
- ✅ `devils-advocate` (~ validator)
- ❌ Pas de backend/frontend builder séparés
- ❌ Pas de test-verifier dédié acceptance tests

Gap potentiel à investiguer en Phase 2 audit repos.

## Liens

- [[google-mit-scaling-agent-systems-2025]] — threshold quantitatif
- [[ecc-pattern-personal-dev-setup]] — pattern différent (dev setup)
- [[will-vs-ecc-deux-doctrines-anthropic]] — résolution
- [[agent-teams-natif-anthropic]] — orchestration officielle
- [[comment-creer-agent]] — canonique forge

## Référence

- [FreeCodeCamp article](https://www.freecodecamp.org/news/how-to-build-software-factory-with-claude-code/)
- [dev.to multi-agent workflows](https://dev.to/javatarz/multi-agent-development-workflows-with-claude-code-n23)
- [VoltAgent awesome subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Panaversity Agent Factory](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/spec-driven-development)
- Tweet @sairahul1 id 2058832033628241931
