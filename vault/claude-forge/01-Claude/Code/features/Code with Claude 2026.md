---
titre: "Code with Claude 2026 — Résumé conférence Anthropic (6 mai 2026)"
resume: "Conférence développeur Anthropic SF : SpaceX Colossus (220K GPUs, limites doublées), Dreaming, Outcomes (grader séparé), Multi-agent orchestration (lead→specialists), Routines (cron cloud). Pas de nouveau modèle"
aliases: ["code with claude 2026", "code with claude SF", "anthropic developer conference 2026", "code with claude announcements", "CwC 2026", "code with claude london", "task horizon", "higher order prompts", "keynote anthropic mai 2026", "cwc london 2026", "cwc sf 2026"]
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
- **Mario Rodriguez & [[Brad-Abrams]]** — Caching, harnesses, advisors at GitHub scale ([[Advisor Strategy]] : executor Haiku + advisor Opus, "close to Opus-level intelligence at much lower prices")
- **Jarred Sumner** — Co-demo avec Boris

## Impact token spend

> "All four of these features are upping your token spend" — Matt Cuda

Dreaming, Outcomes, Multi-agent, Routines = plus d'autonomie mais plus de consommation. À monitorer.

## Liens

- [[Dreaming Managed Agents]] — Détail du dreaming
- [[Memory Managed Agents]] — Architecture memory
- [[workflow-claude-code-optimal]] — Boris setup mai 2026
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]
- [[Brad-Abrams]] — créateur Advisor Strategy
- [[Mitchell-Hashimoto]] — popularisateur "harness engineering" (5 fév 2026)


## Stats keynote (transcription complète)

| Métrique | Valeur | Source |
|----------|--------|--------|
| API volume YoY | +17x | Ami Vora |
| Temps dev moyen sur CC | 20h/semaine | Ami Vora |
| Demande 2026 YTD | +80x | Dario Amodei (Chris Ebert) |
| PRs/engineer Anthropic | +200% | Cat Wu |
| Mercado Libre PRs | 500K+ reviewées | Cat Wu |
| Stripe Scala→Java | 10 semaines estimées → 4 jours | Ami Vora |
| Binti foster licensing | -20 jours sur le process | Ami Vora |

## Concept : Task Horizon (Dianne Penn)

Mesure de combien de temps Claude peut travailler de façon autonome tout en améliorant ses livrables :
- L'an dernier : minutes
- Maintenant : heures
- Demain : proactif, always-on, sait quoi faire sans perdre le fil

## Opus Preview / Mythos

Mentionné comme "le prochain point de l'exponentielle, pas un petit pas". A trouvé une vulnérabilité de 27 ans dans OpenBSD qui avait survécu à tous les reviewers et fuzzers humains.

## Conseil Dianne Penn aux développeurs

> "Design for the next version of Claude, not just the current one. Maintain harder evals, build ambitious prototypes that don't work today."

## Boris Cherny — Higher Order Prompts

> "The default isn't 'I'm going to prompt Claude Code.' The default is 'I will have Claude prompt Claude Code.'"

Routines = higher order prompts. Boris ne prompt plus — il crée des routines qui promptent.

## London (19 mai 2026)

### Nouvelles annonces
- **[[Self-Hosted Sandboxes]]** (public beta) — exécution agents dans l'infra client
- **[[MCP Tunnels]]** (research preview) — accès sécurisé aux MCP servers privés

### Speakers London
- Boris Cherny (Head of Claude Code)
- Angela Jiang (Head of Product, Claude Platform)
- Lisa Crofoot (Research Product Management Lead)
- Katelyn Lesse (Head of Engineering, Claude Platform)
- Cat Wu (Head of Product, Claude Code)

### Framework 16 features (inaiwetrust)
Structuré en 3 couches : **Autonomy** (Auto Mode, Routines, CI Autofix, Work Trees, Auto Memory) · **Visibility** (Agent View, Remote Control, Desktop Rebuild, Full Screen TUI) · **Infrastructure** (Self-Hosted Sandboxes, MCP Tunnels, Claude Security, Advisor Strategy, Tool Search, Programmatic Tool Calling, Compaction)
