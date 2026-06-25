---
aliases:
  - Agent Teams natif
  - Agent Teams Anthropic
  - CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
  - orchestrateur officiel Claude Code
  - Anthropic multi-agent 2026
  - team lead teammates pattern
resume: "Agent Teams = orchestrateur multi-agents natif Claude Code (fév 2026, Opus 4.6). Lead session + teammates en context windows isolés + shared task list. Flag expérimental, requires 2.1.32+."
derniere-maj: 2026-06-24
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


---

## AJOUT 24 juin 2026 — v2.1.178 : `TeamCreate`/`TeamDelete` supprimés, équipe implicite

> Source primaire : [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) v2.1.178 (15 juin 2026), fetch 24 juin. **Amendement de la couche mécanisme** (pas un pivot — l'intention « orchestrateur multi-agents natif » tient), cf [[amende-vs-pivot-couche-factuelle-design]].

Le modèle d'activation décrit plus haut (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` + `TeamCreate`/`TeamDelete` + 2.1.32) est **périmé sur la mécanique de création** :

- **`TeamCreate` et `TeamDelete` supprimés.** Plus d'étape de setup d'équipe.
- Avec `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, **chaque session a désormais une équipe implicite** : on spawn un teammate directement via le paramètre **`name`** du tool `Agent` (ex `Agent(name="reviewer", …)`). Le flag reste donc requis pour activer le mode, mais la création d'équipe disparaît.
- Le paramètre `team_name` du tool `Agent` est **toujours accepté mais ignoré** (rétrocompat, no-op).
- **v2.1.186 (22 juin)** — fix : les deny-rules `Agent(type)` et les restrictions `Agent(x,y)` (allowed-types) n'étaient pas appliquées aux spawns de **sous-agents nommés** ; corrigé. À croiser avec la syntaxe `Tool(param:value)` de 2.1.178 (ex `Agent(model:opus)`).

Ce qui NE change pas : architecture lead + teammates en context windows isolés, shared task list, communication directe entre teammates, statut expérimental (flag toujours requis). La note features minimale [[Agent Teams]] pointe ici pour le détail mécanique.

`derniere-maj` → 2026-06-24.