---
aliases:
  - stand-up
  - daily stand-up
  - daily scrum
  - walking-the-board
  - daily-meeting
  - stand-up-ia
resume: Stand-up quotidien — format walking-the-board > 3 questions Scrum classiques. Adapté équipe IA avec 2 swimlanes delivery/R&D, 15 min timebox strict.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/agile"
  - "#rituel/stand-up"
---

# Stand-up quotidien — au-delà des 3 questions

## TL;DR
- **Walking the board** (parcours kanban droite→gauche) > 3 questions Scrum classique
- **15 min strict**, debout (d'où le nom), caméra ON si distribué
- **2 swimlanes équipe IA** : Delivery (tickets/PRs/incidents) + R&D (expé en cours avec hypothèse + métrique + deadline timebox)
- **Pas un status report** — focus sur le flow, pas l'occupation individuelle

## Formats disponibles

### Walking the board (recommandé 2025)
Parcourir le board kanban **de droite à gauche** (Done → Doing → To Do), item par item, question : "comment fait-on avancer chaque ticket aujourd'hui ?"

**Avantages** : focus sur le **flow** et le **finish** plutôt que sur l'occupation individuelle.
**Inconvénients** : certains coéquipiers ne parlent jamais (tourner le facilitateur).

### 3 questions Scrum classique (déconseillé)
Qu'ai-je fait hier / aujourd'hui / blocages ? **Retiré du Scrum Guide 2020** car il dérive systématiquement en status report orienté micro-management.

Martin Fowler montre que ce format encourage le "reporting to the leader" plutôt que la coordination horizontale.

### Toyota Kata / Gemba
Faire le stand-up à l'endroit du travail (devant le board physique ou son équivalent virtuel). Les obstacles soulevés vont sur un **Improvement Board** séparé — pas discutés dans le stand-up.

## Anti-patterns à bannir

- **Status meeting déguisé** ("ce que j'ai fait hier" = feuille de présence)
- **Blocker rabbit hole** : un blocage dégénère en réunion d'1h. Règle = noter, traiter après en small group
- **Fake busyness** : tout le monde brode pour avoir l'air occupé
- **Tuning out** quand ce n'est pas son tour

## Spécificité équipe IA Neoteem — 2 swimlanes

Une équipe IA mélange **delivery** (features prod, fix bugs ia_back/neoteem-brain) et **R&D** (expé modèles, tuning RAG, evals).

### Lane Delivery
Format flow-oriented :
- Tickets en cours
- PRs en review
- Incidents / production
- Releases imminentes

### Lane R&D / Expé
**1 ligne par expérience en cours**, avec :
- Hypothèse testée
- Métrique de succès
- Date deadline du timebox
- Question : "Qu'as-tu appris hier ?" (pas "où en es-tu ?")

## Durée

**15 min STRICT timebox**, debout. Pour équipe distribuée :
- Caméra ON pour les rôles parlants
- Async-first via Geekbot/Slack si fuseaux divergents > 4h

## Agenda type (15 min)

| Temps | Activité |
|---|---|
| 0-1 min | Tour rapide énergie / état (optionnel) |
| 1-12 min | Walking the board (Done → Doing → To Do) |
| 12-14 min | Blockers à dispatcher post-meeting |
| 14-15 min | 1 thing : focus du jour équipe |

## Liens

- Format alternatif sprint : [[sprint-planning-ia-spike]]
- Si réunion non nécessaire : [[async-first-gitlab-basecamp]]
- Facilitation : [[facilitation-liberating-structures]]

## Sources

- [Martin Fowler – It's Not Just Standing Up](https://martinfowler.com/articles/itsNotJustStandingUp.html)
- [LogRocket – Daily Scrum anti-patterns](https://blog.logrocket.com/product-management/the-daily-scrum-meeting-overview-best-practices-anti-patterns/)
- [Medium – Walk the Board Standup](https://medium.com/the-pragmatic-agilists/the-walk-the-board-standup-122b97d5c707)
- [Scrum.org – The 3 questions won't die](https://www.scrum.org/resources/blog/three-daily-scrum-questions-wont-die-making-your-scrum-work-29)
