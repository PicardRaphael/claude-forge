---
aliases:
  - sprint planning
  - planning sprint
  - spike R&D
  - no-estimates
  - capacity planning
  - sprint IA
resume: Sprint planning adapté équipe IA — gérer l'inestimable via spikes timeboxés, sprint 70/30 delivery/R&D, no-estimates pour équipes matures.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/agile"
  - "#rituel/sprint"
---

# Sprint Planning — estimer l'inestimable

## TL;DR
- **Spike R&D timeboxé** pour ce qu'on ne peut pas estimer (1 jour, 3 jours, 1 semaine MAX)
- **Sprint 70/30** : 70% features avec AC binaires, 30% spikes R&D explicites
- **Plafond spikes : 20% capacité max** — au-delà, plus de delivery
- **No-estimates > story points** dans les équipes matures (compter les items, pas les points)

## Mécaniques de base

### Capacity planning
```
velocity moyenne 3 derniers sprints × disponibilité réelle
                                       (sans congés, sans on-call, sans support)
```

### Definition of Ready (DoR)
Critères qu'une story doit remplir AVANT d'entrer en sprint :
- User value claire
- Acceptance criteria définis
- Dépendances identifiées
- Estimable (taille connue)
- Pas de blocker externe non résolu

### Story points vs No-Estimates
Le débat 2020-2025 a basculé vers le **no-estimates** dans les équipes matures :
- Découper en items "1 jour max"
- Compter les items, plus les points
- Plus simple, plus rapide, force le découpage

## Spécifique IA / R&D — l'inestimable

**Problème** : on ne peut PAS estimer une tâche dont on ignore le résultat (entraînement, choix d'archi, test hypothèse RAG).

### Solutions canoniques

#### 1. Spike timeboxé
Product Backlog Item dont le but est *apprendre* (proof-of-concept jetable).
- **Estimer = allouer un timebox fixe** (1 jour, 3 jours, 1 semaine MAX)
- Pas de story points
- À la fin du timebox : **décision Go/No-Go documentée**

#### 2. Anti-pattern majeur
> "Spike pour que les devs estiment mieux" = peur du failure déguisée.

Vrai spike = réduire un risque concret, pas se rassurer.

#### 3. Slippery slope
Sprints qui finissent tous avec 1 spike → sprints entiers de spikes → plus de delivery.

**Plafond Neoteem recommandé : max 20% de la capacité sprint en spikes**.

#### 4. Sprint à 2 vitesses
- **70% capacity** pour features avec acceptance criteria binaires
- **30% capacity** pour spikes R&D explicitement timeboxés

## Agenda type (2h pour sprint de 2 semaines)

| Temps | Activité |
|---|---|
| 0-5 min | Rappel sprint goal candidate + capacité |
| 5-35 min | Revue backlog top-N, Q/R sur chaque item (DoR check) |
| 35-80 min | Estimation (planning poker OU consensus rapide no-estimates) |
| 80-110 min | Découpage technique, identification dépendances, qui prend quoi |
| 110-120 min | Engagement final sur sprint goal + commitment équipe |

## Sprint goal — formulation

Pas une liste de tickets. Une **phrase courte** qui résume le but business du sprint.

**Mauvais** : "Faire les tickets NEO-123, NEO-124, NEO-125"
**Bon** : "Réduire le taux d'hallucination du chatbot client de 5% à 2%"

## Spike — template ticket Jira

```markdown
# [SPIKE] Réduire latence retrieval RAG sous 300ms p95

## Hypothèse à valider
Le retrieval actuel (Cohere reranker + FAISS) peut être remplacé par
un retrieval hybride (BM25 + embedding) sans dégrader la qualité,
en divisant la latence par 3.

## Timebox
**3 jours** (du JJ/MM au JJ/MM)

## Success criteria (décision Go/No-Go)
- ✅ Latence p95 < 300ms sur eval set 500 queries
- ✅ Recall@5 ≥ 0.85 (baseline actuel 0.87)
- ✅ Doc ADR rédigée si Go

## Livrable
- Notebook eval avec résultats
- ADR de décision (Go = roadmap implémentation / No-Go = doc raisons)
- Présentation 5 min en sprint review

## Non-objectifs
- Pas d'implémentation production
- Pas de refacto code existant
```

## Liens

- [[reunions/index]]
- [[stand-up-walking-the-board]]
- [[sprint-review-demo-eval-ia]]
- template-spike-ia

## Sources

- [ONES – Mastering the Agile Spike](https://ones.com/blog/mastering-the-agile-spike/)
- [Scrum.org – How to estimate spikes](https://www.scrum.org/forum/scrum-forum/30937/how-estimate-spike-stories)
- [V2Solutions – AI-Driven Sprint Planning](https://medium.com/@v2solutions/ai-driven-sprint-planning-revolutionizing-capacity-modeling-and-estimation-with-predictive-52ec3d125c3b)
