---
titre: "Context Engineering"
resume: "Paradigme dominant 2026 : 4 pilliers (composition, ranking, optimization, orchestration), sweet spot 150-300 mots, effort via API pas langage naturel"
aliases:
  - "context engineering"
  - "ingénierie de contexte"
  - "context management LLM"
  - "context window optimization"
  - "structuration du contexte"
  - "context engineering 2026"
domaine: technique
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#type/techniques"
---

## Description

Paradigme dominant en 2026. Shift de "prompt engineering" (comment formuler) vers "context engineering" (quoi mettre dans le contexte et comment le structurer).

## Quand utiliser

Toujours. Chaque interaction avec un LLM est un exercice de context engineering.

## Les 4 pilliers (2026)

1. **Composition** — Assembler les bons éléments de contexte pour la tâche
2. **Ranking** — Ordonner/sélectionner les informations par pertinence descendante
3. **Optimization** — Supprimer le bruit, garder uniquement les tokens à haute densité de signal
4. **Orchestration** — Coordonner comment le contexte est distribué entre agents/calls

## Principes

1. **Structure > Formulation** — L'arrangement de l'information compte plus que les mots exacts
2. **Assemblage dynamique** — Le contexte est construit conditionnellement selon la tâche
3. **Compression intelligente** — Garder le signal, supprimer le bruit
4. **Progressive disclosure** — Charger l'info au moment où elle est nécessaire

## Règles empiriques (mai 2026)

- **Sweet spot : 150-300 mots** de contexte — en dessous : trop peu, au-dessus de ~3000 tokens : dégradation des performances
- **CoT inutile sur les reasoning models** — les modèles avec extended thinking (Opus 4.7, o3) font le raisonnement internement, ajouter "think step by step" n'apporte rien
- **ALL-CAPS nuit à Claude** — les instructions en majuscules dégradent les performances sur Claude (résultat contre-intuitif)
- **Effort via API, pas langage naturel** — passer `effort.level` via la configuration plutôt que "please think very hard" dans le prompt

## Exemple

Le leak du code source Claude Code (31 mars 2026, 512K lignes) a révélé l'architecture de context engineering : assemblage dynamique conditionnel du system prompt.

## Liens

- [[Piebald-AI System Prompts]]
- [[MOC-Techniques]]
