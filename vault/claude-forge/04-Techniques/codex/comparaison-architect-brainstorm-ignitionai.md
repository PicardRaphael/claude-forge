---
titre: "Architect Brainstorm Codex vs IgnitionAI app-architect-brainstorm"
resume: "Comparaison et adaptation de la Skill IgnitionAI app-architect-brainstorm dans l'agent global Codex architect_brainstorm : capacités conservées, rigidités rejetées, références et validation."
aliases:
  - "IgnitionAI app architect brainstorm"
  - "architect brainstorm IgnitionAI"
  - "architecture brainstorm Codex"
  - "baseline architect_brainstorm"
derniere-maj: 2026-07-17
auteur: codex
type: technique
sources:
  - "https://github.com/IgnitionAI/skills/tree/main/app-architect-brainstorm"
  - "commit 30501712df75c7d93b538e48eeb00b911ec9436f"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/architecture"
  - "#doctrine/2026"
---
# Architect Brainstorm Codex vs IgnitionAI

## Décision

La Skill globale Codex `architect-brainstorm` prend `IgnitionAI/app-architect-brainstorm` comme baseline minimale de couverture, sans copie verbatim.

## Capacités conservées et adaptées

- modes greenfield et reverse engineering ;
- classification par archétype ;
- questionnement/challenge des décisions structurantes ;
- sélection de stack fondée sur exigences, équipe, opérations et coût ;
- modèles domaine/données, ER Mermaid, API/événements/jobs/fichiers ;
- diagrammes contexte, composants, séquence, état, données et déploiement ;
- ADR, migration incrémentale, slices, readiness ;
- architecture contract et guardian anti-dérive.

## Rigidités rejetées

La source rend universels Clean Architecture, repository interfaces, mappers, DI, entités riches, soft delete et structure verticale. Forge les traite comme patterns conditionnels : chaque couche/composant doit résoudre un problème vérifié. Le modular monolith reste une hypothèse de départ, jamais une réponse obligatoire.

## Implémentation

Installation active uniquement : `~/.codex/skills/architect-brainstorm/` et `~/.codex/agents/architect_brainstorm.toml`. La copie source sous `global-config/codex/` et son mécanisme d'installation ont été retirés le 17 juillet 2026 à la demande de Raphael. Les Skills brainstorm ont ensuite été centralisés sous `~/.codex/skills/`.

La Skill principale reste concise et route vers six références progressives : méthode, archétypes/stack, data/contrats/diagrammes, reverse architecture, guardian et template de handoff.

## Validation

Vérifier directement l'existence et la cohérence des composants dans les emplacements globaux actifs. Il n'existe plus de miroir versionné ni d'installateur dans `claude-forge`.
