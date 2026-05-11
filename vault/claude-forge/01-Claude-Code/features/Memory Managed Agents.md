---
titre: "Memory for Claude Managed Agents — Architecture & Principes"
resume: "Memory = filesystem monté dans l'agent. Permission scopes (read-only org-wide + read-write working), optimistic concurrency, version history, attribution metadata. Public beta avril 2026. Opus 4.7 state-of-the-art file-based memory"
aliases:
  - "memory managed agents"
  - "claude memory api"
  - "agent memory"
  - "memory filesystem"
  - "memory anthropic"
  - "managed agents memory"
type: feature
derniere-maj: 2026-05-11
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=RtywqDFBYnQ"
  - "https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Contexte

Présenté par **Mahesh Murag** (PM Platform, Anthropic) à Code with Claude SF, 6 mai 2026. Memory = primitive suivante après MCP, harnesses (Claude Code, Agent SDK) et Skills.

## Architecture — 3 couches

| Couche | Rôle |
|--------|------|
| **Storage** | Où les données sont stockées, métadonnées, attribution |
| **Structure & Content** | Memory modélisée comme filesystem + Skills comme mémoire procédurale |
| **Process** | Fréquence de mise à jour, triggers, sources de décision → c'est ici qu'intervient [[Dreaming Managed Agents]] |

## Principes de design

### 1. Memory = filesystem
Pas un tool call spécifique — Claude gère un filesystem de fichiers avec hiérarchie et format. Il utilise bash et grep pour lire, écrire, organiser. Opus 4.7 est state-of-the-art en file-based memory : meilleur discernement de quoi retenir, meilleure structure.

### 2. Permission scopes
- **Read-only** : mémoire org-wide (runbooks, best practices, SLO guidelines)
- **Read-write** : working memory spécifique à la tâche, fréquemment mise à jour

### 3. Optimistic concurrency
Hash de contenu avant overwrite — un agent vérifie qu'il ne va pas écraser la mémoire d'un autre agent. Critique pour les systèmes multi-agents (100s-1000s d'agents parallèles).

### 4. Version history + attribution
Audit log complet : quel agent a fait quelle modification, quand, dans quelle session. Rollback possible. Accessible aux agents eux-mêmes pour suivre l'historique.

### 5. Standalone API
API portable hors managed agents — PII scanning, cleanup pipelines, clonage vers systèmes externes.

## Résultats early adopters

- **Rakuten** : -97% first-pass errors, -27% coût, -34% latence avec memory
- **Netflix** : carry context across sessions, corrections human-in-the-loop persistées
- **Harvey** : +6% completion rate avec Dreaming

## Pattern SRE démontré

1. Agent SRE 1 reçoit alerte P1 → investigue → écrit findings dans memory store
2. Même alerte page à nouveau → Agent SRE 2 lit la mémoire → short-circuit l'investigation → gain immédiat tokens + intelligence

## Pertinence pour forge-brain

Notre vault Obsidian + MCP = une implémentation du même pattern :
- `vault/` = filesystem memory
- `04-Techniques/`, `Knowledge/erreurs/` = read-only org-wide knowledge
- `0-Inbox/context-actuel.md` = working memory
- git + CHANGELOG = version history
- MCP forge-brain = standalone API

**Gap identifié** : pas de process "dreaming" automatique (cross-session pattern detection, verification, deduplication).

## Liens

- [[Dreaming Managed Agents]] — Process de review/enrichissement automatique
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]
