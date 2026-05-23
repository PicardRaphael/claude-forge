---
titre: "Daisy Hollman"
resume: "MTS Anthropic — talk 'Beyond the Basics with Claude Code' à Code with Claude London (19 mai 2026). Métaphore 'red squigglies for agents' (hooks = linter d'agent), doctrine overnight agents."
aliases:
  - "daisy hollman"
  - "Daisy Hollman"
  - "hollman"
  - "Daisy"
  - "@dhollman"
  - "MTS Anthropic Daisy"
  - "beyond the basics claude code"
derniere-maj: 2026-05-22
auteur: claude
role: "Member of Technical Staff (MTS)"
affiliation: "Anthropic"
sources:
  - "https://www.youtube.com/watch?v=AgQ4cwL5eOM"
  - "https://www.youtube.com/watch?v=6amLO7I9xdg"
  - "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
type: "leader"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#org/anthropic"
---

## QUI

- **Rôle** : Member of Technical Staff (MTS), Anthropic
- **Équipe** : Claude Code
- **Période d'activité observée dans le chantier** : présente sur scène à Code with Claude London (19 mai 2026) — talk individuel "Beyond the Basics with Claude Code"
- **Profil public** : speaker reconnu pour ses métaphores pédagogiques sur le harness Claude Code (hooks, agents long-running)

## POURQUOI ELLE EST PERTINENTE

Daisy Hollman est l'une des voix Anthropic qui rend **concrète** la doctrine harness-engineering :

1. Sa métaphore **"red squigglies for agents"** est devenue le raccourci canonique pour expliquer pourquoi les hooks remplacent (souvent) les rules : un hook = un linter en ligne pour Claude, comme l'IDE souligne en rouge le code humain.
2. Son talk **"Beyond the Basics with Claude Code"** est cité comme un des highlights London — il s'adresse aux utilisateurs qui ont déjà saisi les bases et veulent passer au tier suivant (harness, agents, async).
3. Elle pousse la doctrine **"agents overnight"** dans la lignée des annonces Routines / Dreaming / Managed Agents de mai 2026.

Pertinence forge : ses verbatim cadrent deux notes canoniques du chantier — `comment-creer-hook.md` (red squigglies) et `workflow-claude-code-optimal.md` (async / overnight).

## CONTRIBUTIONS CLÉS

### Hooks = "red squigglies for agents"

Métaphore canonique **coinée par Daisy Hollman** au workshop "Beyond the Basics with Claude Code" (CwC London 19 mai 2026). _Note : mention "également utilisée par Alex Albert" retirée 23 mai 2026 — non sourcée._ Référencée dans `audit-notes-existantes-vs-fraiches.md` du chantier :

> "Daisy Hollman dit aussi 'red squigglies for agents' (CwC SF) — métaphore canonique pour expliquer rôle hooks"

**Interprétation** : les hooks PreToolUse/PostToolUse jouent pour l'agent le rôle que joue le souligné rouge d'un linter pour un développeur humain. Ils sont visibles, déterministes, et corrigent le tir avant la propagation de l'erreur. C'est la formulation la plus pédagogique disponible aujourd'hui pour expliquer pourquoi un workflow critique doit être un hook, pas une rule advisory.

### "You should be running agents overnight"

Verbatim Daisy Hollman, Code with Claude London (cf. `recherche-youtube-talks.md` du chantier) :

> "You should be running agents overnight." — **Daisy Hollman**

**Contexte** : énoncé dans le cadre des annonces Managed Agents (Multi-agent orchestration, Outcomes, **Dreaming** — research preview) et **Routines** (higher-order prompts async). Le shift architectural mai 2026 — "a lot of code is going to be written in an async way" (Boris Cherny SF) — est repris et opérationnalisé par Daisy dans son talk London.

### Talk "Beyond the Basics with Claude Code" — London (19 mai 2026)

- **Source** : playlist Code with Claude London, transcription complète attendue dans 5-7 jours (cf. `recherche-youtube-talks.md` §10)
- **Positionnement** : tier intermédiaire/avancé — au-delà des bases CLI, vers les hooks, agents long-running, routines async, Dreaming
- **Lignée** : Boris keynote "Routines are a higher order prompt" → Daisy approfondit avec patterns concrets pour utilisateurs déjà familiers du CLI

## VERBATIM NOTABLES

> "red squigglies for agents" — Daisy Hollman (en parlant des hooks comme linter d'agent)

> "You should be running agents overnight." — Daisy Hollman, Code with Claude London 2026

## STATUT D'INFORMATION

- **Confirmé** : présence London 19 mai 2026, talk "Beyond the Basics with Claude Code", verbatim "red squigglies" et "agents overnight"
- **À confirmer** : transcription complète du talk individuel London (upload YouTube attendu post-événement)
- **Information non confirmée à date du chantier** : bio détaillée (background pré-Anthropic, dates), handle Twitter/X exact, contributions code GitHub explicites

## WIKILINKS

- [[comment-creer-agent]] — référencer la doctrine async/overnight dans la section "Quand utiliser un agent long-running"
- [[workflow-claude-code-optimal]] — "agents overnight" comme pratique canonique
- [[Boris Cherny]] — keynote London, complémentarité Routines / overnight
- [[Alex Albert]] — co-auteur de la métaphore "red squigglies"
- [[Lisa Crofoot]] — autre voix London Anthropic (scaffolding)
- [[Cat Wu]] — Head Product Claude Code, keynote London

## SOURCES

- [Code with Claude 2026 London — full livestream YouTube](https://www.youtube.com/watch?v=AgQ4cwL5eOM)
- [Code with Claude London opening keynote](https://www.youtube.com/watch?v=6amLO7I9xdg)
- [MIT Tech Review — coding's future (21 mai 2026)](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- Rapports chantier internes : `0-Inbox/_chantier-22mai/recherche-youtube-talks.md`, `audit-notes-existantes-vs-fraiches.md`
