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
derniere-maj: 2026-06-16
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

---

## AJOUT 16 juin 2026 — Corrections + détails primaires (platform.claude.com)

> Vérifié sur [platform.claude.com/docs/en/managed-agents/memory](https://platform.claude.com/docs/en/managed-agents/memory.md) (16 juin). Précise/corrige le corps rédigé d'après la présentation orale du 6 mai.

### Mécanique réelle (primaire)

- **Montage** : le memory store (workspace-scoped, docs texte) est monté dans le sandbox sous **`/mnt/memory/`** ; l'agent l'édite avec ses file tools.
- **Permission scopes — correction** : il n'y a **PAS** de couche « read-only org-wide » système. Chaque store a un accès **`read_write` (défaut) ou `read_only`** (enforced filesystem). Le modèle « 2 couches » (référentiel partagé + working memory) s'obtient en **attachant plusieurs stores** à la session (un read_only partagé + un read_write par user/projet), pas via une hiérarchie native.
- **Optimistic concurrency** : précondition `content_sha256` sur `memories.update` (confirme le « hash avant overwrite » du corps).
- **Version history** : chaque mutation = version immuable `memver_...`, **rétention 30 jours** (les plus récentes toujours gardées), redactable (PII/GDPR).
- **Beta header** : `managed-agents-2026-04-01`. Setup : `POST /v1/memory_stores` → seed `POST .../memories` → attacher dans `resources[]` à la **création** de session (`access`, `instructions` ≤ 4096 chars) — uniquement à la création.
- **Caps** : **2000 memories/store**, **100 kB/memory**, **8 stores/session**.

### Modèle « state-of-the-art » — à élargir

Le corps dit « Opus 4.7 state-of-the-art file-based memory ». Depuis, **Opus 4.8** est le flagship et Dreaming supporte aussi `opus-4-8` (cf [[technique-dreaming-cross-session]] AJOUT 16 juin). Ne pas figer sur 4.7.

### Chiffres early adopters — prudence

« Rakuten -97% first-pass errors » : **non confirmé en primaire** (page client Rakuten = 79% time-to-market). Voir le détail dans [[technique-dreaming-cross-session]] § AJOUT 16 juin. Traiter le 97% comme à confirmer.

### Vaults ≠ Memory (ne pas confondre)

Côté Managed Agents, les **Vaults** (`vlt_...`) stockent des **credentials** par end-user (`mcp_oauth`/`static_bearer`/`environment_variable`, substitué à l'egress — l'agent ne voit jamais la vraie valeur), PAS de la mémoire. Les **scheduled deployments** (cron) ne persistent PAS le contexte entre runs par défaut → la persistance s'obtient en attachant des memory stores dans `resources[]`.

`derniere-maj` → 2026-06-16.
