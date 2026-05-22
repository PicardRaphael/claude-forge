---
titre: "Jeremy Hadfield"
resume: "Anthropic — porte la feature Dreaming (cross-session memory review, research preview mai 2026) présentée à Code with Claude London. Verbatim sondage salle : ~50% PRs entièrement écrites par Claude la semaine précédente."
aliases:
  - "jeremy hadfield"
  - "Jeremy Hadfield"
  - "hadfield"
  - "Jeremy"
  - "Dreaming Anthropic"
  - "Anthropic Dreaming feature"
  - "Claude Dreaming"
derniere-maj: 2026-05-22
auteur: claude
role: "Anthropic — Claude Code team"
affiliation: "Anthropic"
sources:
  - "https://www.youtube.com/watch?v=AgQ4cwL5eOM"
  - "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
  - "https://www.youtube.com/watch?v=6amLO7I9xdg"
type: "leader"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#org/anthropic"
---

## QUI

- **Rôle** : Anthropic, équipe Claude Code
- **Période d'activité observée** : Code with Claude London, 19 mai 2026 — porte-parole / présentateur de la feature **Dreaming**
- **Profil public** : voix Anthropic associée au pattern *cross-session memory review* (Dreaming), feature en research preview au moment du chantier

## POURQUOI IL EST PERTINENT

Jeremy Hadfield incarne le **shift async mai 2026** côté capacités modèles : Dreaming est la première feature Anthropic qui formalise l'auto-review entre sessions — Claude relit ses propres sessions pendant l'inactivité pour en extraire mémoire, patterns, erreurs.

C'est l'équivalent fonctionnel direct du pattern forge **`/dream + /schedule`** déjà documenté dans le vault (`reference_dreaming_pattern.md` côté memory). Sa présentation London et son sondage "qui a mergé une PR écrite à 100% par Claude la semaine dernière ?" (~50% des mains levées) sont devenus les chiffres canoniques de l'adoption mai 2026.

## CONTRIBUTIONS CLÉS

### Dreaming — cross-session memory review (research preview, mai 2026)

**Statut** : research preview annoncée à Code with Claude London (19 mai 2026).

**Spécifications techniques** (sources : recherche-x-twitter-leaders.md, recherche-youtube-talks.md du chantier) :
- **Header API** : `dreaming-2026-04-21`
- **Limite** : max 100 sessions par dream
- **Modèles supportés** : Opus 4.7 et Sonnet 4.6 uniquement
- **Famille** : Claude Managed Agents (avec Multi-agent orchestration et Outcomes)

**Principe** : Claude review ses sessions précédentes en arrière-plan (overnight typiquement), extrait apprentissages, met à jour mémoire/CLAUDE.md équivalent, propose améliorations workflow. Pattern aligné avec la philosophie "compounding" Boris Cherny et "engineer one time, agent runs forever" (Hashimoto).

> "The key principle is getting out of Claude's way. We like to say: 'Let it cook.'" — **Ravi Trivedi** (Anthropic) sur Dreaming, complétant la doctrine portée par Jeremy

### Sondage salle Code with Claude London

Verbatim Jeremy Hadfield, transcrit dans `recherche-youtube-talks.md` du chantier (source : MIT Tech Review) :

> "Who here has shipped a pull request in the last week that was completely written by Claude?" — **Jeremy Hadfield** (~50% des mains levées en salle)

**Pertinence** : c'est la métrique d'adoption la plus citée post-London. Référence directe pour la doctrine "leaf nodes" (Erik Schluntz) et "agentic engineering" (Karpathy) — la PR full-Claude n'est plus marginale en mai 2026 dans l'écosystème pro early-adopter.

### Lignée Dreaming dans la suite mai 2026

Dreaming s'inscrit dans une famille cohérente annoncée la même semaine :
- **Routines** (Boris) — higher-order prompts async
- **Managed Agents** — multi-agent orchestration (public beta)
- **Outcomes** — success criteria loops (public beta, +8.4% docx / +10.1% pptx)
- **CI auto-fix** — PRs auto-fixed sans intervention dev
- **Dreaming** (Jeremy) — overnight self-improvement via session review

## VERBATIM NOTABLES

> "Who here has shipped a pull request in the last week that was completely written by Claude?" — Jeremy Hadfield, Code with Claude London 2026 (~50% des mains levées)

Verbatim associé (équipe Dreaming, Ravi Trivedi) :

> "The key principle is getting out of Claude's way. We like to say: 'Let it cook.'"

## STATUT D'INFORMATION

- **Confirmé** : présence London 19 mai 2026, présentation Dreaming, sondage PRs Claude, header API et limites Dreaming
- **À confirmer** : titre exact (MTS / Product / Research ?), historique pré-Anthropic
- **Information non confirmée à date du chantier** : handle Twitter/X public, blog posts officiels co-signés sur Dreaming (probable post-event)

## ÉQUIVALENT FORGE

Le pattern Dreaming a un équivalent natif documenté côté forge :
- Skill `/dream` (review cross-session)
- `/schedule` pour automatisation overnight
- Référence : `reference_dreaming_pattern.md` (memory)

Tracer le parallèle dans la note canonique [[workflow-claude-code-optimal]] : Dreaming Anthropic = vision officielle du pattern forge.

## WIKILINKS

- [[comment-creer-agent]] — section "Agents long-running" et async
- [[workflow-claude-code-optimal]] — Dreaming dans la suite async (Routines + Managed Agents + CI auto-fix)
- [[Boris Cherny]] — Routines + keynote London "code written in an async way"
- [[Cat Wu]] — Head Product Claude Code, keynote London
- [[Daisy Hollman]] — "agents overnight" — doctrine complémentaire
- [[Andrej Karpathy]] — async / autoresearch / agentic engineering

## SOURCES

- [Code with Claude 2026 London — full livestream](https://www.youtube.com/watch?v=AgQ4cwL5eOM)
- [Code with Claude London opening keynote](https://www.youtube.com/watch?v=6amLO7I9xdg)
- [MIT Tech Review — coding's future (21 mai 2026)](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- Rapports chantier internes : `0-Inbox/_chantier-22mai/recherche-youtube-talks.md`, `recherche-x-twitter-leaders.md`
