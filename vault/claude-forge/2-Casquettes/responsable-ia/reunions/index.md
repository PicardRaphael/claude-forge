---
aliases:
  - rituels-reunions-ia
  - index-reunions
  - reunions-lead-ia
  - rituels-agiles-ia
  - hub-reunions
resume: Hub réunions & rituels agiles adaptés équipe IA — stand-up, sprint, rétro, post-mortem, CODIR, client. Source canonique pour la casquette responsable-ia.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/management"
  - "#domaine/agile"
---

# Réunions & rituels — hub canonique

Synthèse complète + notes atomiques par format. Pour le contexte général, voir [[../index]].

## Les 10 formats canoniques

| Format | Note atomique | Quand l'utiliser |
|---|---|---|
| Stand-up quotidien | [[stand-up-walking-the-board]] | Daily 15 min, coordination flow |
| Sprint planning | [[sprint-planning-ia-spike]] | Démarrage sprint, capacity + commitment |
| Sprint review / Demo | [[sprint-review-demo-eval-ia]] | Fin sprint, feedback stakeholders |
| Rétrospective | [[retrospective-formats-rotation]] | Fin sprint, amélioration continue |
| Post-mortem incident | [[post-mortem-blameless-sre]] | Après incident, RCA |
| Réunion client | [[reunion-client-hype-management]] | Pitch, présentation, suivi |
| CODIR / reporting direction | [[codir-6-pager-bezos]] | Mensuel/trim, exec reporting |
| Réunions techniques inter-équipes | [[techniques-adr-rfc]] | Décisions architecture |
| Facilitation | [[facilitation-liberating-structures]] | Toutes réunions, dynamique groupe |
| Quand NE PAS faire de réunion | [[async-first-gitlab-basecamp]] | Default async, éviter sync |

## Règles d'or transversales

| Règle | Source |
|---|---|
| **Agenda + objectif + pre-read 24h avant** ou la réunion n'a pas lieu | GitLab |
| **Timeboxer chaque section** + parking lot pour les débordements | Liberating Structures |
| **Démos IA = eval, pas UI** ; metrics avant/après ; cas adverses montrés | Atlassian + Label Studio |
| **Blameless absolute** sur post-mortem ; 5 Whys → cause systémique | Google SRE |
| **6-pager > slides** pour reporting direction ; narration force la pensée | Bezos / Amazon |
| **ADR/RFC versionnés in-repo** pour toute décision architecture | adr.github.io |
| **Rotation rétro 3-4 sprints**, action items SMART ≤ 3, audit AIs précédents | Retrium / Parabol |
| **Spike R&D timeboxé**, max 20% capacité sprint, Go/No-Go documenté | Scrum.org |
| **Default async** ; sync seulement pour décision/trust/conflit/brainstorm | GitLab / Basecamp |
| **Honest AI communication** : limites en premier, ROI mesurable, augmenter > remplacer | Aspire / IBM |

## Spécificités équipe IA Neoteem (à retenir)

1. **Stand-up en 2 swimlanes** (Delivery + R&D) — voir [[stand-up-walking-the-board]]
2. **Sprint 70/30** — 70% delivery features, 30% spikes R&D timeboxés
3. **Sprint review = démo eval** — table avant/après métriques, cas adverses inclus
4. **Post-mortem IA spécifique** : hallucination, drift modèle, prompt injection
5. **CODIR 6-pager mensuel** — traduire chaque métrique technique en business
6. **Calendar hygiene** : max 4 meetings sync/semaine/personne, mardi/jeudi no-meeting

## Sources principales

- [Martin Fowler – It's Not Just Standing Up](https://martinfowler.com/articles/itsNotJustStandingUp.html)
- [Google SRE – Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [GitLab Handbook – Asynchronous communication](https://handbook.gitlab.com/handbook/company/culture/all-remote/asynchronous/)
- [adr.github.io](https://adr.github.io/) — ADR canonical
- [Liberating Structures](https://www.liberatingstructures.com/)
- [Working Backwards – Bryar & Carr](https://www.workingbackwards.com/) — méthode Amazon
- [Atlassian Agile Coach – Sprint Review](https://www.atlassian.com/agile/scrum/sprint-reviews)
