---
titre: "Context Engineering"
resume: "Paradigme dominant 2026 — structure autour de la tâche > formulation du prompt"
aliases:
  - "context engineering"
  - "ingénierie de contexte"
  - "context management LLM"
  - "context window optimization"
  - "structuration du contexte"
  - "context engineering 2026"
domaine: technique
type: technique
derniere-maj: 2026-04-21
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/techniques"
---

## Description

Paradigme dominant en 2026. Shift de "prompt engineering" (comment formuler) vers "context engineering" (quoi mettre dans le contexte et comment le structurer).

## Quand utiliser

Toujours. Chaque interaction avec un LLM est un exercice de context engineering.

## Principes

1. **Structure > Formulation** — L'arrangement de l'information compte plus que les mots exacts
2. **Assemblage dynamique** — Le contexte est construit conditionnellement selon la tâche
3. **Compression intelligente** — Garder le signal, supprimer le bruit
4. **Progressive disclosure** — Charger l'info au moment où elle est nécessaire

## Exemple

Le leak du code source Claude Code (31 mars 2026, 512K lignes) a révélé l'architecture de context engineering : assemblage dynamique conditionnel du system prompt.

## Liens

- [[Piebald-AI System Prompts]]
- [[MOC-Techniques]]
