---
titre: "Workflow Boris — Fleet Commander"
resume: "5 terminaux + 5-10 sessions cloud en parallèle, chacun en worktree, ne code pas lui-même"
aliases:
  - "fleet commander"
  - "workflow boris"
domaine: technique
type: technique
derniere-maj: 2026-04-21
auteur: claude
sources:
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/techniques"
---

## Description

Pattern de travail de [[Boris Cherny]], créateur de Claude Code. Orchestre les agents comme un "fleet commander".

## Quand utiliser

Projets avec beaucoup de tâches parallèles indépendantes. Refactoring multi-fichiers. Features complexes.

## Pattern

1. **5 terminaux** + **5-10 sessions cloud** en parallèle
2. Chacun dans son **worktree git** isolé
3. Ne code pas lui-même — orchestre
4. **Plan Mode** → itérer → auto-accept → one-shot
5. Code principalement à la **voix** (`/voice`)
6. "Give Claude a way to verify its output" = tip #1

## Best Practices associées

- `/clear` entre tâches non liées
- `/compact` proactif à 70%
- "Document & Clear" — dump plan dans .md, /clear, nouvelle session lit le .md
- `/btw` pour questions sans polluer le contexte
- Déléguer la recherche aux subagents

## Liens

- [[Boris Cherny]]
- [[Context Management]]
- [[MOC-Techniques]]
