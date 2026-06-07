---
titre: "Erik Schluntz"
resume: "Co-fondateur Anthropic, 4 stratégies vibe coding prod (PM guidance, leaf nodes, human core, verifiable checkpoints), talk Code with Claude SF mai 2026"
aliases:
  - "schluntz"
  - "erik schluntz"
  - "erik-schluntz"
  - "@ErikSchluntz"
  - "vibe coding in production"
  - "Erik Anthropic"
  - "Anthropic co-founder"
  - "building effective agents co-author"
  - "PM guidance pattern"
role: "Member of Technical Staff & Co-founder"
affiliation: "Anthropic"
derniere-maj: 2026-06-07
auteur: claude
sources:
  - "https://youtube.com/watch?v=fHWFF_pnqDk"
  - "https://x.com/ErikSchluntz"
  - "https://www.latent.space/p/claude-sonnet"
  - "Code with Claude SF, 6-7 mai 2026 — talk 'Vibe Coding in Production'"
  - "Paper 'Building Effective Agents' (co-auteur Barry Zhang)"
type: leader
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#org/anthropic"
---
## QUI

Erik Schluntz — Member of Technical Staff et co-fondateur Anthropic. Travaille sur tool use, computer use, SWE-bench. Co-auteur (avec **Barry Zhang**, pas Amanda Askell) du paper de référence "Building Effective Agents" — architecture canonique des agents Anthropic.

Avant Anthropic : CTO/co-fondateur Cobalt Robotics, ex-SpaceX, ex-Google[x], Harvard. Forbes 30 Under 30 (2018).

Twitter/X : [@ErikSchluntz](https://x.com/ErikSchluntz).

## POURQUOI EST PERTINENT

Schluntz est la voix d'Anthropic la plus claire sur **comment faire du vibe coding en production sans casser** le système. Son talk Code with Claude SF (6-7 mai 2026) "Vibe Coding in Production" formalise 4 stratégies qui passent du yolo individuel au workflow d'équipe défendable.

Il est aussi le co-auteur du paper foundationnel "Building Effective Agents" — c'est-à-dire que sa parole pèse autant sur la théorie (architecture agents) que sur la pratique (workflow vibe coding).

## CONTRIBUTIONS CLÉS

### Les 4 stratégies vibe coding en production (Code with Claude SF, mai 2026)

Verbatim du talk "Vibe Coding in Production" :

1. **PM guidance** — l'humain agit comme product manager, pas comme développeur. On guide l'agent par intention produit, pas par implémentation ligne à ligne.
2. **Leaf nodes** — modifier les feuilles de l'arbre de code (features isolées, endpoints terminaux), pas les racines (core/design system/abstractions partagées). L'IA écrit les leaves, l'humain garde les racines.
3. **Human core** — l'humain garde le contrôle des décisions clés : architecture, sécurité, contrats d'API, schéma de données. Tout ce qui est cher à corriger reste humain.
4. **Verifiable checkpoints** — chaque étape doit être vérifiable mécaniquement (tests, lint, type-check, smoke E2E). Pas de checkpoint vérifiable = pas de progress mesurable.

Ces 4 stratégies sont la grille de décision : si une tâche ne coche pas les 4, elle n'est pas prête pour le vibe coding non-supervisé.

### "Building Effective Agents" — paper Anthropic

Co-écrit avec **Barry Zhang** (correction d'attribution — pas Amanda Askell). Le paper formalise les patterns d'agents Anthropic : prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. Référence pour quiconque conçoit un agent au-delà du simple chat loop.

### Case study "22 000 LOC en 1 jour" — à manipuler en analogie cognitive

> "22 000 lignes mergées en prod (codebase RL Anthropic), 2 semaines compressées en 1 jour."
— Talk Code with Claude SF, mai 2026

**ATTENTION** : ce chiffre est à utiliser comme **analogie cognitive**, pas comme métrique brute. Le framing exact est "2 semaines → 1 jour" — c'est la compression du temps cognitif d'un humain expert, pas une cadence reproductible "22k LOC/jour". Citer le chiffre nu sans le framing est trompeur.

### Citation pivot (LinkedIn, février 2025)

> "Since I started using Claude Code a few weeks ago I literally stopped writing code manually."

Posture qui anticipe celle de Boris Cherny ("0% code écrit à la main depuis oct 2025") d'un an.

## VERBATIM NOTABLES

> "Forget the code, focus on the product."

> "Demanding to read every line of code will make you the bottleneck."
— Analogie LLM = compilateur (comme on a arrêté d'écrire de l'assembly).

> "15-20 minutes of planning before each task — explore the codebase, create a plan, merge context into one prompt."
— Tip de pré-planification systématique.

## WIKILINKS

- [[comment-ecrire-claudemd]]
- [[comment-creer-skill]]
- [[mcp-vs-skills-doctrine]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[Boris Cherny]] — même posture "100% code par Claude"
- [[Andrej Karpathy]] — framework "agentic engineering" confirme la même direction
- [[Code with Claude Conference]]
- [[MOC-Leaders]]

## SOURCES

- Talk YouTube : https://youtube.com/watch?v=fHWFF_pnqDk
- Twitter : https://x.com/ErikSchluntz
- Latent Space Podcast : https://www.latent.space/p/claude-sonnet ("The new Claude 3.5 Sonnet, Computer Use, and Building SOTA Agents")
- Code with Claude SF, 6-7 mai 2026 — talk "Vibe Coding in Production"
- Paper "Building Effective Agents", Anthropic (co-auteur Barry Zhang)
- Recherche vault : `0-Inbox/_chantier-22mai/recherche-youtube-watch-vibe-coding.md`
