---
titre: "Boris Cherny"
resume: "Créateur de Claude Code, @bcherny, fleet commander workflow, 6 tips Opus 4.7"
aliases:
  - "bcherny"
  - "@bcherny"
  - "boris cherny"
  - "boris-cherny"
  - "boris claude code"
  - "howborisusesclaudecode"
  - "expert Claude Code"
  - "fleet commander workflow"
  - "CC best practices"
role: "Creator of Claude Code"
affiliation: "Anthropic"
derniere-maj: 2026-06-07
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
- **Anthropic acquiert Bun** (1ère acquisition Anthropic, annonce corporate 2 déc 2025) + **Claude Code atteint $1B ARR** ("fastest B2B product ramp in history", 6 mois après GA mai 2025, $2.5B annualisé fév 2026, $2B+ rev mai 2026)

## Liens

- [[workflow-claude-code-optimal]]
- [[MOC-Leaders]]


## Mise à jour mai 2026 (AI Ascent Sequoia)

- Setup : mobile-first (Claude app iOS), 5-10 sessions web, centaines d'agents, milliers la nuit
- Record : 150 PRs en 1 jour
- /loop = "the future" — dizaines de loops actifs (PRs, CI, feedback Twitter→Slack)
- "Coding is solved" — n'écrit plus de code à la main depuis **late 2025 / entering 2026** (transition documentée par Frontend Mentor + Sequoia AI Ascent 2026)
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


## Interview Acquired (juin 2026) — "My job is to write loops"

Source primaire transcrite (podcast Acquired, partagé via @0xCodez 4 juin 2026). Détail doctrinal complet : [[pre-compute-vs-inference-loops-boris]].

- **3 niveaux d'abstraction** : écrire le code → prompter Claude (5-10 en //) → **écrire des loops qui promptent Claude**. Verbatim : *"I don't prompt Claude anymore. I have loops that are running. They're the ones that are prompting Claude... My job is to write loops."*
- **Setup actuel** : *"a couple hundred Claudes running"* qui surveillent Twitter / GitHub issues / Slack et décident quoi build. ~20% des idées sont bonnes aujourd'hui, « most will be good » dans 3-6 mois.
- **Uninstall IDE en novembre 2025** (plus utilisé depuis un mois).
- **Pre-compute > inference** (fondement) : faire écrire au modèle un programme rejouable gratuitement plutôt que re-sampler à chaque tâche = "pre-compiling", raise upfront cost / decrease ongoing cost. Les principes d'entreprise → **skills** réutilisables.
- **Conseil org** : "give everyone as many tokens as possible", "the more you buy the more you save" (Jensen), **"under-fund everything a little bit"** (2 ingénieurs + tokens au lieu de 4).
- **Taste s'érode** : son dogme "no classes only functions" abandonné car le modèle écrivait des classes et "the business outcome is met faster". Dernier rempart humain = **enseigner les valeurs au modèle**.
- **Co-work** construit en ~8-9 jours, 100% Claude Code.