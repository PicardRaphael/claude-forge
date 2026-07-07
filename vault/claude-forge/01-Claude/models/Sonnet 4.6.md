---
titre: "Claude Sonnet 4.6"
resume: "Modèle rapide, effort high obligatoire dans Claude Code, 1M context natif"
aliases:
  - "sonnet-4-6"
  - "claude-sonnet-4-6"
  - "sonnet 4.6"
  - "claude sonnet"
  - "modele sonnet"
domaine: claude-code
type: modele
derniere-maj: 2026-04-21
auteur: claude
sources: []
tags:
  - "#type/modele"
  - "#domaine/claude"
---

## Specifications

| Propriété | Valeur |
|-----------|--------|
| Context window | 200K (standard) / 1M (beta) |
| Thinking | Adaptive supporté |

## Quand utiliser
## Paramètre effort

Sonnet 4.6 est le **premier Sonnet à supporter `effort`**. Niveaux : `low` / `medium` / `high` / `max`. Défaut = `high`.

> *"Effort is supported on Opus 4.7, Opus 4.6, and Sonnet 4.6. Sonnet 4.6 is the first Sonnet model to support the effort parameter."* — Anthropic

- `xhigh` exclusif Opus — si posé sur Sonnet → fallback automatique vers `high`
- Précédence : env var > `--effort` flag > frontmatter > parent default
- Agents Sonnet **mécaniques** (scan, maintenance, inspection) → `medium` ou `low` (économie tokens)
- Agents Sonnet **code complexe** (dev) → garder `high`
- JAMAIS retirer `effort:` du frontmatter Sonnet (paramètre actif, pas ignoré)

Voir aussi [[Opus 4.7]] pour `xhigh` et calibrage par type de tâche.

- Subagents Claude Code par defaut (`model: sonnet`)
- **effort: high OBLIGATOIRE** — jamais medium
- Sessions concurrentes ou taches de complexite moderee

## Liens

- [[Opus 4.7]]
- [[MOC-Modeles]]
