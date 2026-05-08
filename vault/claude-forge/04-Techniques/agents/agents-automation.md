---
titre: "Agents Automation — Workflows et production"
resume: "Automation agents IA 2026 : workflows (n8n, Zapier), CI/CD, scheduling, Computer Use, browser agents, coûts production"
aliases:
  - agent automation
  - automation agents
  - AI workflow automation
  - Claude routines
  - browser agents
  - computer use
domaine: ia
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://www.shareuhack.com/en/posts/claude-code-routines-2026"
  - "https://www.browserbase.com/blog/stagehand-v3"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Workflow automation

| Outil | Force | Usage |
|-------|-------|-------|
| **n8n** | 8000+ intégrations, open-source, $2.5B valuation | High volume, APIs stables |
| **Claude Code /schedule** | Routines cloud, zero infra | Tâches IA complexes, scheduling |
| **Make.com** | Cloud-locked, per-operation | Workflows visuels simples |
| **Zapier AI** | 8000+ apps | Automations simples, écosystème max |

Décision simple : high volume + APIs stables = n8n/Make. Ambiguë + non-structuré = Claude Code.

## Claude Code Scheduling

### Routines (avril 2026)
Unifient cron + webhook + GitHub events :
- **Cron** : hourly, daily, weekdays, weekly, custom. Min 1h.
- **Webhook** : endpoint HTTP unique + bearer token. Pas de cap daily.
- **GitHub events** : PR, push, issue, check run, release. Filtres auteur/titre/branche/labels.

### Always-on pattern
Trigger /schedule toutes les heures = heartbeat agent. Wake up → read state → decide → act → sleep. Cloud = state persistent.

### Dispatch & Channels
Dispatch : tâches depuis mobile/tablet. Channels : Telegram/Discord/webhooks → sessions.

## CI/CD avec agents

Claude Code en GitHub Actions : 1 workflow file + 1 secret + CLAUDE.md. **Code Review Plugin** : 4 agents review parallèles, confidence scoring >= 80%.

Pattern : morning PR reviews, overnight CI failure analysis, weekly dependency audits — tout en Routines.

**GitHub Agent HQ** (`gh aw`) : visibilité org-wide agents (Copilot, Claude, Codex).

## Computer Use / Browser agents

| Agent | Approche | Score | Prix |
|-------|---------|-------|------|
| **Claude Computer Use** | Screenshot + mouse/keyboard, VMs | 44% OSWorld (3x vs 2024) | $20/mo |
| **OpenAI Operator** | Browser-natif, achats/réservations | — | $200/mo |
| **Google Mariner** | Chrome extension, DOM-aware | — | Research |
| **Stagehand** (Browserbase) | Open-source, 4 primitives, Playwright | 89% fiabilité | Free + ~$0.003/action |

**RPA vs AI agents** : RPA = fragile (bouge un bouton, cassé). AI agents gèrent le drift UI. Marché browser agents : **$12B en 2026**, +200% YoY.

Pattern hybride production : **Playwright (80% steps prévisibles) + Stagehand/AI (20% dynamiques)**. Fiabilité : Playwright+Claude 92%, Stagehand 89%, Computer Use 78%.

## Coûts production

### Trois leviers majeurs

| Stratégie | Économie |
|-----------|---------|
| Prompt caching | 50-90% input tokens |
| Batch API | 50% off standard |
| Model routing | 40-60% blended |

Combiné caching + batching = **-70-90%** vs standard.

### Pricing tokens (mai 2026)

| Modèle | Input/Output per M tokens |
|--------|--------------------------|
| Opus 4.6 | $5/$25 |
| Sonnet 4.6 | $3/$15 |
| Haiku 4.5 | $1/$5 |
| GPT-5.4 Mini | $0.75/$4.50 |

### Observabilité
Top stack : Braintrust (eval-first), LangSmith (LangChain), Langfuse (open-source), Arize Phoenix (embedding viz), Helicone (multi-provider cost).

79% des orgs ont adopté des agents mais la plupart ne peuvent pas tracer les échecs multi-step.

## Liens

- [[Agents IA]] — Index principal
- [[agents-evaluation]] — Testing et benchmarks
- [[agents-securite]] — Sécurité production
- [[Boris Cherny]] — Claude Code Routines
