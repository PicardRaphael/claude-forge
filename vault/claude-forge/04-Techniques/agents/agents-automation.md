---
titre: "Agents Automation — Workflows et production"
resume: "Automation agents IA 2026 : workflows (n8n, Zapier), CI/CD, scheduling, Computer Use, browser agents, couts production"
aliases:
  - agent automation
  - automation agents
  - AI workflow automation
  - Claude routines
  - browser agents
  - computer use
domaine: ia
type: technique
derniere-maj: 2026-05-23
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
| **n8n** | 8000+ integrations, open-source, $2.5B valuation | High volume, APIs stables |
| **Claude Code /schedule** | Routines cloud, zero infra | Taches IA complexes, scheduling |
| **Make.com** | Cloud-locked, per-operation | Workflows visuels simples |
| **Zapier AI** | 8000+ apps | Automations simples, ecosysteme max |

Decision simple : high volume + APIs stables = n8n/Make. Ambigue + non-structure = Claude Code.

> [!tip] Choix forge / Neoteem — n8n en priorité (2026-06-27)
> Pour toute **automatisation externe**, proposer **n8n self-host en priorité** : souveraineté des données, coût maîtrisé, workflows pilotables par Claude via MCP — recette opérationnelle dans [[n8n-self-host-mcp-claude]]. Zapier/Make restent listés ci-dessus pour **connaître le marché**, mais sont écartés par défaut (cloud propriétaire, facturation par tâche/opération, données hors UE — point RGPD pour le pro).

## Claude Code Scheduling

### Isolation des routines remote — contrainte critique

Les routines `/schedule` tournent dans un **sandbox cloud Anthropic isolé** (git checkout du repo uniquement). Elles n'ont PAS accès à :
- `~/.claude/agents/` user-scope local (ex : will-auditor, ecc-auditor, boris-auditor)
- Vault forge-brain local
- MCP locaux non déclarés explicitement dans la routine
- Tout fichier hors du repo GitHub checkouté

**Critère de décision** : "Ce que ferait la routine peut-il fonctionner avec UNIQUEMENT git checkout du repo + MCP connecté ?" Si non → skill locale ou Task Scheduler Windows.

**Cas d'usage valides** pour routines remote : check PRs, lint schedulé, deploy monitoring — tâches autonomes sans dépendances locales.

**Anti-pattern** : proposer une routine sans vérifier les dépendances locales (agents user-scope, vault, MCP non connecté). Erreur observée 26 mai 2026 : routine `/schedule` pour spawner Agent Team with user-scope auditors → impossible par construction.

Alternatif pour review/audit cyclique : skill `/forge-review` manuelle, ou Task Scheduler Windows (cf [[org-blocks-github]]). Cf aussi [[skills-user-scope-pas-cross-repo]].

### Routines (avril 2026)
Unifient cron + webhook + GitHub events :
- **Cron** : hourly, daily, weekdays, weekly, custom. Min 1h.
- **Webhook** : endpoint HTTP unique + bearer token. Pas de cap daily.
- **GitHub events** : PR, push, issue, check run, release. Filtres auteur/titre/branche/labels.

### Always-on pattern
Trigger /schedule toutes les heures = heartbeat agent. Wake up → read state → decide → act → sleep. Cloud = state persistent.

### Dispatch & Channels
Dispatch : taches depuis mobile/tablet. Channels : Telegram/Discord/webhooks → sessions.

## CI/CD avec agents

Claude Code en GitHub Actions : 1 workflow file + 1 secret + CLAUDE.md. **Code Review Plugin** : 4 agents review paralleles, confidence scoring >= 80%.

Pattern : morning PR reviews, overnight CI failure analysis, weekly dependency audits — tout en Routines.

**GitHub Agent HQ** (`gh aw`) : visibilite org-wide agents (Copilot, Claude, Codex).

## Computer Use / Browser agents

| Agent | Approche | Score | Prix |
|-------|---------|-------|------|
| **Claude Computer Use** | Screenshot + mouse/keyboard, VMs | 44% OSWorld (Sonnet 3.5, oct 2024, +3x vs 2024 initial) — Sonnet 4.5 et Mythos atteignent plus, chiffre exact a remettre a jour | $20/mo |
| **OpenAI Operator** | Browser-natif, achats/reservations | — | $200/mo |
| **Google Mariner** | Chrome extension, DOM-aware | — | Research |
| **Stagehand** (Browserbase) | Open-source, 4 primitives, Playwright | 89% fiabilite (single source DigitalApplied) | Free + ~$0.003/action |

> ⚠️ Audit 23 mai : Computer Use Claude "44% OSWorld" est le chiffre de Sonnet 3.5 (oct 2024). Sonnet 4.5 progresse au-dela ; chiffre exact mai 2026 a verifier dans la fiche modele Anthropic.

**RPA vs AI agents** : RPA = fragile (bouge un bouton, casse). AI agents gerent le drift UI.

> Marche browser agents en forte croissance ; chiffres precis (single source "$12B +200% YoY") retires audit 23 mai (non sourcables).

Pattern hybride production : **Playwright (80% steps previsibles) + Stagehand/AI (20% dynamiques)**. Fiabilites Playwright+Claude 92%, Stagehand 89%, Computer Use 78% = single source DigitalApplied, a confirmer.

## Couts production

### Trois leviers majeurs

| Strategie | Economie |
|-----------|---------|
| Prompt caching | 50-90% input tokens |
| Batch API | 50% off standard |
| Model routing | 40-60% blended |

Combine caching + batching = **jusqu'a 95% reduction** (verbatim Anthropic).

### Pricing tokens (mai 2026)

| Modele | Input/Output per M tokens |
|--------|--------------------------|
| Opus 4.6 | $5/$25 |
| Sonnet 4.6 | $3/$15 |
| Haiku 4.5 | $1/$5 |
| GPT-5.4 Mini | $0.75/$4.50 |

### Observabilite
Top stack : Braintrust (eval-first), LangSmith (LangChain), Langfuse (open-source), Arize Phoenix (embedding viz), Helicone (multi-provider cost).

**79% des orgs ont adopte des agents** (Cisco State of AI Security). Tracabilite des echecs multi-step = challenge ouvert.

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-evaluation]] — Testing et benchmarks
- [[agents-securite]] — Securite production
- [[Boris Cherny]] — Claude Code Routines
