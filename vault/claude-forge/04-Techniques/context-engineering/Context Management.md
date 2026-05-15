---
titre: "Context Management — Gestion du contexte LLM"
resume: "Techniques de gestion du contexte pour LLM — compaction, /clear entre taches, document & clear, delegation subagents, prompt caching."
aliases:
  - "Context Management"
  - "context management"
  - "gestion contexte"
  - "gestion contexte LLM"
type: technique
domaine: context-engineering
derniere-maj: 2026-05-15
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/context-engineering"
---

## Description

Techniques de gestion du contexte pour maximiser l'efficacite des LLM dans les sessions longues. Couvre la compaction, le /clear entre taches non liees, le pattern Document & Clear, la delegation aux subagents, et le prompt caching.

## Patterns cles

- **/clear entre taches** — eviter les sessions fourre-tout (piege #1 Boris)
- **/compact proactif** — a 70%, pas attendre l'auto-compact
- **Document & Clear** — dump plan → .md → /clear → nouvelle session
- **Delegation subagents** — garder le contexte principal propre

## Liens

- [[MOC-Techniques]]
- [[Context Engineering]]
- [[Workflow Boris]]
- [[context-management]]
