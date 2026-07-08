---
aliases:
  - async-first
  - asynchronous
  - async communication
  - GitLab handbook
  - shape up basecamp
  - no meeting day
  - quand pas faire reunion
resume: Async-first comme default — GitLab handbook + Basecamp Shape Up. Heuristique "réunion ou pas", max 4 meetings sync/sem, mardi/jeudi no-meeting day.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/management"
  - "#culture/async"
---

# Quand NE PAS faire de réunion — async-first

## TL;DR
- **Calendrier qui se remplit = work qui se vide**
- **Default async**, sync seulement pour décision/trust/conflit/brainstorm
- **Max 4 meetings sync/semaine/personne** (équipe 1-5)
- **Mardi & jeudi = no-meeting day** (deep work)
- **Si agenda vide 30 min avant** → réunion annulée (règle GitLab)

## Doctrine GitLab

GitLab : 1600+ employés, 60+ pays, **all-remote**.

Règle absolue : le **Handbook est la single source of truth**. Tout est documenté avant d'être discuté.

> *"The future of work isn't just remote; it's documented."* — GitLab

**Principe pratique GitLab** : si l'agenda d'une réunion est vide 30 min avant, **la réunion est annulée**.

## Doctrine Basecamp / Shape Up

Shape Up : le travail est **shaped** dans un **pitch écrit** (4-8 pages) AVANT toute affectation à une équipe.

- Cycles de 6 semaines + 2 semaines cooldown
- **Pas de daily standup**, pas de sprint planning
- Le **pitch IS la planification**

## Heuristique "réunion ou pas ?"

Une réunion est **justifiée** si :

1. **Décision** nécessitant arbitrage temps réel multi-personnes
2. **Build trust** / création de lien (1:1, kickoff)
3. **Conflit** à résoudre
4. **Brainstorm** avec dynamique de rebond rapide nécessaire

Sinon → **async** :

| Besoin | Format async |
|---|---|
| Mise à jour status | Slack/Notion/issue thread |
| Question technique | Thread écrit + Loom si visuel |
| Décision avec data dispo | RFC async (cf [[techniques-adr-rfc]]) |
| Onboarding | Handbook + Loom recordings |
| Reporting hebdo | Status report écrit |
| Brainstorm initial | Notion/Miro async board |

## Outils async-first

### Loom
Screencast 3-5 min remplace 30 min de meeting.
- Démo rapide d'une fonctionnalité
- Walkthrough technique
- Réponse à question complexe
- Pitch d'idée

### Notion / Confluence / Handbook GitLab-style
- Single source of truth
- Documenté avant d'être discuté
- Versionné, searchable

### GitHub issues / Linear
- Decisions in-thread
- Liés au code, à l'historique
- Searchable

### Geekbot / Range
Daily standup async dans Slack — chaque membre poste réponse à 9h, le bot agrège.

## Règles proposées Neoteem (équipe 1-5)

### Calendar hygiene
1. **Max 4 meetings synchrones / semaine / personne** (stand-up x3 + 1 sync)
2. **Mardi & jeudi = no-meeting day** (deep work protégé)
3. **Pas de meeting < 30 min** ou > 1h (sauf 1:1 hebdo 30 min)
4. **Default async** : Loom + thread pour toute info, sync seulement si bloquant

### Meeting protocol
1. **Agenda obligatoire 24h avant** ou meeting annulée
2. **Pre-read si > 2 personnes** doivent décider
3. **Objectif explicite** : info / décision / co-construction
4. **Owner décideur** clair (DACI : qui décide)
5. **CR partagé J+1** max (cf cr-meeting-template)

### Meeting cancellation rule (GitLab)
Si agenda vide 30 min avant le meeting → **annulé automatiquement**.

## Le piège des petites équipes

> "On se réunit parce qu'on est peu nombreux et c'est rapide."

**Faux**. Les petites équipes ont MOINS de tolérance aux interruptions, pas plus.

Coût d'un meeting 1h pour 5 personnes = **5 heures-personne**.

## Mesurer la maturité async

Indicateurs équipe Neoteem :
- **% temps en meetings** : objectif < 30%
- **Time-to-decision** sur RFC async : objectif < 1 semaine
- **Handbook docs created/month** : croissance documentée
- **Meeting cancelation rate** : OK si non-zéro

## Async ne veut PAS dire

- ❌ Pas de communication (le contraire : MORE documentation)
- ❌ Pas de proximité (les 1:1 sync restent)
- ❌ Pas de spontanéité (Slack/Loom pour ça)
- ❌ Pas de team building (offsites, kickoffs, retros sync)

## Liens

- [[reunions/index]]
- handbook-gitlab-style (à venir)
- team-rituals-async (à venir)

## Sources

- [GitLab Handbook – Asynchronous communication](https://handbook.gitlab.com/handbook/company/culture/all-remote/asynchronous/)
- [Async Twist – How GitLab's Head of Remote works](https://async.twist.com/how-darren-murph-works-async/)
- [Async Agile – Write a handbook](https://www.asyncagile.org/blog/write-a-handbook-avoid-the-scenic-route)
- [Shape Up – Basecamp](https://basecamp.com/shapeup) (gratuit en ligne)
