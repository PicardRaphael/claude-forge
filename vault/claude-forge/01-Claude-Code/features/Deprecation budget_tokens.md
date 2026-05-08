---
titre: "Dépréciation budget_tokens (thinking)"
resume: "thinking.budget_tokens supprimé dans Opus 4.7 — retourne 400 error, utiliser adaptive thinking"
aliases:
  - "budget_tokens deprecated"
  - "budget tokens deprecation"
  - "thinking budget"
  - "adaptive thinking migration"
  - "thinking budget_tokens removed"
  - "deprecation thinking tokens"
domaine: claude-code
type: deprecation
date-deprecation: 2026-04-16
date-retirement: 2026-04-16
remplacement: "thinking: {type: 'adaptive'}"
derniere-maj: 2026-04-21
auteur: claude
sources: []
tags:
  - "#type/deprecation"
  - "#domaine/claude-code"
---

## Ce qui est déprécié

`thinking.budget_tokens` dans l'API Claude pour Opus 4.7. Retourne une erreur 400 immédiatement.

## Remplacement

```json
{
  "thinking": {
    "type": "adaptive"
  }
}
```

Combiné avec les [[Effort Levels Guide]] pour contrôler la profondeur de réflexion.

## Migration

1. Supprimer `budget_tokens` des appels API
2. Ajouter `thinking: {type: "adaptive"}` si thinking étendu nécessaire
3. Utiliser `effort` pour contrôler le niveau

## Liens

- [[Adaptive Thinking]]
- [[Effort Levels Guide]]
- [[Opus 4.7]]
- [[MOC-Claude-Code]]
