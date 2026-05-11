---
titre: "Code with Claude 2026 — Résumé conférence Anthropic (6 mai 2026)"
resume: "Conférence développeur Anthropic SF : SpaceX Colossus (220K GPUs, limites doublées), Dreaming, Outcomes (grader séparé), Multi-agent orchestration (lead→specialists), Routines (cron cloud). Pas de nouveau modèle"
aliases:
  - "code with claude 2026"
  - "code with claude SF"
  - "anthropic developer conference 2026"
  - "code with claude announcements"
  - "CwC 2026"
type: feature
derniere-maj: 2026-05-11
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=0ZyqYPBQ7nc"
  - "https://claude.com/code-with-claude/san-francisco"
  - "https://simonwillison.net/2026/May/6/code-w-claude-2026/"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/anthropic"
---

## Annonces principales

### 1. SpaceX Colossus Deal
220 000 GPUs NVIDIA, online immédiatement. Résultat : limites Claude Code doublées, rate limits peak hours supprimés, limites API Opus augmentées.

### 2. Dreaming (Research Preview)
Process scheduled qui review les sessions passées des managed agents, extrait patterns, déduplique, vérifie et enrichit la mémoire. Voir [[Dreaming Managed Agents]].

### 3. Outcomes (Public Beta, API only)
Grader séparé dans son propre context window qui score l'output contre un rubric. Différent du worker agent qui fait le travail. Quand ça échoue, le grader pinpointe le problème et les workers fixent. Similaire à `/go` de Codex.

### 4. Multi-agent Orchestration (Public Beta, API)
Lead agent → délègue à des specialists, chacun avec ses propres tools. Shared filesystem. Trace complète disponible. Travail en parallèle.

### 5. Routines (Live, Claude Code Web)
Cron jobs cloud : "Every night at 2am, pull top bug from Linear, attempt fix, open draft PR." Réagissent aussi aux events (webhooks). 15 routines gratuites/jour.

### 6. Autres
- Remote control (terminal → web/mobile)
- Flicker-free terminal
- Desktop split view
- Auto mode, auto memory, automated code reviews

## Speakers

- **Boris Cherny** — Demo multi-agent live (agents pick up GitHub issues → fix → PR → review)
- **Mahesh Murag** — Memory and Dreaming for self-learning agents
- **Dickson Tsai** — What's new in Claude Code
- **Mario Rodriguez & Brad Abrams** — Caching, harnesses, advisors at GitHub scale
- **Jarred Sumner** — Co-demo avec Boris

## Impact token spend

> "All four of these features are upping your token spend" — Matt Cuda

Dreaming, Outcomes, Multi-agent, Routines = plus d'autonomie mais plus de consommation. À monitorer.

## Liens

- [[Dreaming Managed Agents]] — Détail du dreaming
- [[Memory Managed Agents]] — Architecture memory
- [[boris-workflow-2026-may]] — Boris setup mai 2026
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]
