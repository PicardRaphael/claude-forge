---
titre: "Effort Levels Guide"
resume: "5 niveaux d'effort Claude Code : low, medium, high, xhigh (défaut Opus 4.7), max"
aliases:
  - "effort levels"
  - "effort"
domaine: technique
type: technique
derniere-maj: 2026-04-21
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/technique"
---

## Description

Contrôle du niveau de réflexion de Claude dans Claude Code. 5 niveaux disponibles.

## Niveaux

| Niveau | Usage | Notes |
|--------|-------|-------|
| `low` | Questions simples, lookups | Minimal thinking |
| `medium` | Tâches routinières | **JAMAIS pour Sonnet** — toujours `high` |
| `high` | Sessions concurrentes, coding standard | Minimum pour Sonnet |
| `xhigh` | Défaut Opus 4.7, coding agentique | Sweet spot |
| `max` | Problèmes très durs | Diminishing returns |

## Quand utiliser

Pour configurer le niveau d'effort des agents Claude Code selon leur role (analyste, dev, gate, securite) et le modele utilise (Opus vs Sonnet).

## Règles Claude-Forge

- **Sonnet : `effort: high` OBLIGATOIRE** — jamais medium
- **Opus 4.7 : `effort: xhigh`** = défaut (la plupart du coding agentique)
- `high` pour sessions concurrentes
- `max` uniquement pour problèmes très durs

## Commande

```
/effort
```
Ouvre un slider interactif sans arguments (depuis v2.1.111).

## Liens

- [[Opus 4.7]]
- [[Adaptive Thinking]]
- [[MOC-Techniques]]
