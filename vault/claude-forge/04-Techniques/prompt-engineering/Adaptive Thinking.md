---
titre: "Adaptive Thinking"
resume: "Opus 4.7 adaptive thinking — off par défaut, thinking: {type: adaptive} requis, budget_tokens supprimé"
aliases:
  - "adaptive thinking"
  - "extended thinking"
domaine: technique
type: technique
derniere-maj: 2026-04-21
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7"
tags:
  - "#type/technique"
  - "#domaine/techniques"
---

## Description

Mode de réflexion étendu de Claude. Dans Opus 4.7, off par défaut — doit être activé explicitement.

## Quand utiliser

Problèmes complexes nécessitant un raisonnement en étapes : math, code architecture, debugging, analysis.

## Exemple

```json
{
  "thinking": {
    "type": "adaptive"
  }
}
```

## Changements Opus 4.7

- **Off par défaut** — `thinking: {type: "adaptive"}` explicite requis
- **`budget_tokens` SUPPRIMÉ** — retourne 400 error
- Remplacé par les [[Effort Levels Guide]]

## Liens

- [[Opus 4.7]]
- [[Effort Levels Guide]]
- [[MOC-Techniques]]
