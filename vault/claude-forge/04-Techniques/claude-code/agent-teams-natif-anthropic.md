---
aliases:
  - Agent Teams natif
  - Agent Teams Anthropic
  - CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
  - orchestrateur officiel Claude Code
  - Anthropic multi-agent 2026
  - team lead teammates pattern
resume: "Agent Teams = orchestrateur multi-agents natif Claude Code (fév 2026, Opus 4.6). Lead session + teammates en context windows isolés + shared task list. Flag expérimental, requires 2.1.32+."
derniere-maj: 2026-05-26
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Agent Teams — Orchestrateur natif Anthropic

## Source

Feature shippée par Anthropic en **février 2026** avec Opus 4.6.

## Architecture

- Une session devient **team lead** (coordinateur)
- Plusieurs **teammates** chacun en context window isolé
- Coordination via **shared task list**
- Teammates communiquent entre eux directement

## Activation

- Claude Code **2.1.32+** requis
- Flag : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- Disabled by default (expérimental)

## Contrôles avancés

- Display modes
- Delegate mode
- Plan approval
- Quality gate hooks
- Task assignment
- Token cost management
- CLAUDE.md optimisé pour teams

## Policy shift critique (avril 2026)

> Le **4 avril 2026**, Anthropic a bloqué Claude Pro et Max subscribers d'utiliser leurs subscriptions avec la plupart des frameworks tiers d'agent orchestration (Ruflo 31.1K stars, ccpm 7.9K stars, Swarm SDK, etc.).

API users non affectés.

**Conséquence** : pour Pro/Max users, Agent Teams natif devient la **seule option fully-supported**.

## Pattern recommandé 2026

**Phase-based workflow** :
1. **Exploration phase** : Agent Teams (collaborative)
2. **Implementation phase** : builder-validator pattern (quality gates)

## Comparaison avec sub-agents Claude Code classiques

| Aspect | Sub-agents | Agent Teams |
|--------|------------|-------------|
| Coordination | Hiérarchique parent→child | Lead + teammates peer-like |
| Communication | Via parent | Directe entre teammates |
| State | Isolé par invocation | Shared task list |
| Officiel | Oui (stable) | Oui (expérimental) |
| Multi-tour | Limité | Designed for |

## Implications forge

**On ne l'utilise pas dans forge.** Gap à investiguer :
1. Tester `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` sur un workflow forge complexe
2. Voir si Agent Teams remplace certains patterns sub-agents actuels (devils-advocate, project-auditor parallèle)
3. Mesurer overhead tokens vs gains

**Production validé** :
- Fountain : 50% faster delivery
- CRED : 2x speed
- Anthropic Engineering : C compiler avec Agent Teams + git coordination

## Liens

- [[ecc-pattern-personal-dev-setup]] — peut adopter Agent Teams
- [[software-factory-pattern-2026]] — chain orchestrable par Agent Teams
- [[google-mit-scaling-agent-systems-2025]] — coordination centralisée 4.4x error vs 17x indépendants

## Référence

- [ClaudeFast Agent Teams guide](https://claudefa.st/blog/guide/agents/agent-teams)
- [Developers Digest 2026 playbook](https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026)
- [Shipyard multi-agent orchestration 2026](https://shipyard.build/blog/claude-code-multi-agent/)
- [Anthropic managed agents docs](https://platform.claude.com/docs/en/managed-agents/multi-agent)
