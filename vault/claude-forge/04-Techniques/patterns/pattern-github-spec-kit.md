---
titre: "GitHub Spec Kit — Framework SDD 93K stars"
resume: "6 commandes slash (constitution → specify → clarify → plan → tasks → implement), Constitution.md pour règles non-négociables, dossiers specs/001-feature/ avec 8 fichiers, 80+ extensions marketplace"
aliases:
  - spec kit
  - github spec kit
  - speckit
  - spec-kit
  - constitution.md
  - speckit framework
domaine: development
type: technique
derniere-maj: 2026-05-12
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/framework"
auteur: claude
---

## Vue d'ensemble

Framework SDD le plus populaire (93K+ GitHub stars). 6 commandes slash pour un pipeline complet de spec-driven development. Agnostique de stack.

## Pipeline

1. `/speckit.constitution` — établit les principes de gouvernance (choix tech, testing, style)
2. `/speckit.specify` — décrit QUOI construire et POURQUOI (user stories, behaviors)
3. `/speckit.clarify` — clarification structurée AVANT planning (réponses enregistrées dans la spec)
4. `/speckit.plan` — introduit le stack technique et l'architecture, génère `plan.md` + `research.md` + `data-model.md`
5. `/speckit.tasks` — décompose en `tasks.md` ordonnées avec marqueurs parallèles `[P]`
6. `/speckit.implement` — exécute la task list en ordre de dépendance avec TDD

## Structure de dossier

```
specs/001-feature-name/
  spec.md
  plan.md
  tasks.md
  research.md
  data-model.md
  contracts/api-spec.json
  checklists/manual-testing.md
```

## Concept de Constitution

Fichier `.specify/memory/constitution.md` = règles non-négociables vérifiées en continu par l'agent. Librairies interdites, coverage minimum requis, patterns obligatoires → flaggés automatiquement.

## Avertissements (Böckeler/Fowler)

- Les 8 fichiers peuvent causer de la **review fatigue** (trop de volume)
- L'agent peut ignorer les `research.md` et régénérer des classes en doublon
- Risque de **Verschlimmbesserung** (aggravation par tentative d'amélioration)

## Ce qu'on a pris pour /spec Neoteem

- Concept de clarification APRÈS exploration (pas avant)
- Structure numérotée des specs (00-vision, 01-architecture, etc.)
- Calibration gate pour adapter la quantité d'output à la complexité

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]] — Pattern SDD complet
- [[pattern-gsd-framework]] — Framework concurrent (GSD)
- [[over-specification-paradox]] — Risque de sur-spécification