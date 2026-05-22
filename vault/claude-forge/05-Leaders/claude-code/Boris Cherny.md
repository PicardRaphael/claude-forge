---
titre: "Boris Cherny"
resume: "Créateur de Claude Code, @bcherny, fleet commander workflow, 6 tips Opus 4.7"
aliases:
  - "bcherny"
  - "@bcherny"
  - "boris cherny"
  - "boris claude code"
  - "howborisusesclaudecode"
  - "expert Claude Code"
  - "fleet commander workflow"
  - "CC best practices"
role: "Creator of Claude Code"
affiliation: "Anthropic"
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://howborisusesclaudecode.com"
  - "x.com/bcherny"
  - "threads.com/@boris_cherny"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
type: ""
---

## Profil

Créateur de Claude Code. Travaille chez Anthropic. Workflow "Fleet Commander" — 5 terminaux + 5-10 sessions cloud en parallèle, chacun dans un worktree git. Ne code pas lui-même, orchestre les agents.

## Contributions clés

- Architecture Claude Code (skills, hooks, agents, plugins)
- "CLAUDE.md = advisory (~80%), hooks = déterministe (100%)"
- "Give Claude a way to verify its output" = tip #1
- Skill `/go` : test E2E + `/simplify` + PR auto
- "Document & Clear" pattern

## 6 Tips post-Opus 4.7 (16 avril 2026)

1. **Auto Mode** pour sessions parallèles
2. **`/fewer-permission-prompts`** skill
3. **Recaps** pour sessions longues
4. **Focus Mode** (`/focus`) cache étapes intermédiaires
5. **Effort levels** low/medium/high/xhigh/max
6. **Vérification systématique** — son skill `/go`

## Positions récentes

- 6 tips post-Opus 4.7 (16 avril 2026)
- Acquisition Bun / CC $1B ARR

## Liens

- [[workflow-claude-code-optimal]]
- [[MOC-Leaders]]


## Mise à jour mai 2026 (AI Ascent Sequoia)

- Setup : mobile-first (Claude app iOS), 5-10 sessions web, centaines d'agents, milliers la nuit
- Record : 150 PRs en 1 jour
- /loop = "the future" — dizaines de loops actifs (PRs, CI, feedback Twitter→Slack)
- "Coding is solved" — 0% code écrit à la main depuis oct 2025
- Routines = loops côté serveur (persistent)
- Vision : "by a couple years, the model does all the code, starts agents, builds environments"
- Claude Design = prochain product overhang
- Source : [[workflow-claude-code-optimal]]

## Application doctrine 22 mai 2026 sur Neoteem

Le 22 mai 2026, refonte ia_back + neo_ia inspirée directement par sa doctrine :
- **"Thinnest wrapper"** → suppression de 7 hooks workflow par repo (decision scaffolding obsolète)
- **"Claude decides when to invoke"** (Agent SDK) → la session principale juge quand appeler architect, pas un hook
- **Bitter lesson** → on n'encode pas la structure du repo dans des hooks (paths, patterns) qui deviennent obsolètes au prochain refacto

Voir [[raisonnement-22mai-doctrine-vs-enforcement]] pour les décisions concrètes et les sources web complètes.
