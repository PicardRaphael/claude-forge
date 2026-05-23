---
titre: "GitHub Spec Kit — Framework SDD ~105K stars (mai 2026)"
resume: "Framework SDD GitHub (~105K stars mai 2026). 6 commandes core + 3 optionnelles, Constitution.md pour règles non-négociables, dossiers specs/001-feature/ avec 7 fichiers, 40+ extensions community"
aliases:
  - spec kit
  - github spec kit
  - speckit
  - spec-kit
  - constitution.md
  - speckit framework
domaine: development
type: technique
derniere-maj: 2026-05-23
sources:
  - "https://github.com/github/spec-kit"
  - "https://github.github.com/spec-kit/"
  - "https://developer.microsoft.com/blog/spec-driven-development-spec-kit"
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/framework"
auteur: claude
---

## Vue d'ensemble

Framework SDD le plus populaire de 2026. **~105K stars GitHub** (API au 2026-05-23, en croissance rapide — était à 93K il y a peu). Agnostique de stack et de coding agent (30+ AI agents supportés : Copilot, Claude Code, Gemini CLI, Cursor, Windsurf, etc.).

## Pipeline — 6 core + 3 optionnelles (9 total)

**Core (6)** :
1. `/speckit.constitution` — principes de gouvernance (tech, testing, style)
2. `/speckit.specify` — QUOI construire et POURQUOI
3. `/speckit.plan` — stack technique + architecture
4. `/speckit.tasks` — décomposition en tâches
5. `/speckit.taskstoissues` — conversion en GitHub issues
6. `/speckit.implement` — exécution TDD

**Optionnelles (3)** :
- `/speckit.clarify` — clarification structurée AVANT planning
- `/speckit.analyze` — analyse cross-référence
- `/speckit.checklist` — checklists d'acceptation

## Structure de dossier (7 fichiers post-plan)

```
specs/001-feature-name/
  spec.md
  plan.md
  data-model.md
  research.md
  quickstart.md
  contracts/api-spec.json
  contracts/signalr-spec.md
```

Note : le claim "8 fichiers" parfois cité dans la littérature est inexact — 7 fichiers observés post-plan.

## Constitution.md

Fichier `.specify/memory/constitution.md` = règles non-négociables vérifiées en continu par l'agent. Librairies interdites, coverage minimum requis, patterns obligatoires → flaggés automatiquement.

## Avertissements (Böckeler/Fowler)

> Verbatim Böckeler (martinfowler.com) : *"Are we making something worse in the attempt of making it better?"* — invoque **Verschlimmbesserung** (aggravation par tentative d'amélioration).

- Les 7 fichiers peuvent causer de la **review fatigue** (volume)
- L'agent peut ignorer les `research.md` et régénérer des classes en doublon
- Risque de **Verschlimmbesserung**

## Marketplace community

**40+ extensions** community (Hidde de Smet catalog) — pas 80+ comme parfois cité. Catalog community en croissance.

## Ce qu'on a pris pour /spec Neoteem

- Concept de clarification APRÈS exploration (pas avant)
- Structure numérotée des specs (00-vision, 01-architecture, etc.)
- Calibration gate pour adapter la quantité d'output à la complexité

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]]
- [[pattern-gsd-framework]]
- [[Birgitta Böckeler]]
- [[over-specification-paradox]]
