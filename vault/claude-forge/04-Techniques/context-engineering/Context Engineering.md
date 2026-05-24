---
titre: "Context Engineering"
resume: "Paradigme 2026 popularisé par Karpathy — composer/structurer le contexte LLM plutôt que formuler des prompts isolés"
aliases:
  - "context engineering"
  - "ingénierie de contexte"
  - "context management LLM"
  - "context window optimization"
  - "structuration du contexte"
  - "context engineering 2026"
domaine: technique
type: technique
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://x.com/karpathy/status/1937902205765607626"
  - "https://simonwillison.net/2025/jun/27/context-engineering/"
  - "https://www.keyvalue.systems/blog/pillars-of-context-engineering/"
  - "https://github.com/davidkimai/Context-Engineering"
tags:
  - "#type/technique"
  - "#domaine/context-engineering"
---

## Description

Shift conceptuel : de "prompt engineering" (comment formuler une instruction) vers "context engineering" (quoi mettre dans le contexte et comment le structurer).

> ✅ Verbatim Karpathy (X, 2026-04) : *"+1 for 'context engineering' over 'prompt engineering'. People associate prompts with short task descriptions you'd give an LLM in your day-to-day use. When in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step."*

## Quand utiliser

Toujours. Chaque interaction LLM substantielle est un exercice de context engineering. Karpathy l'a positionné comme paradigme prioritaire — la communauté (Simon Willison, LangChain, davidkimai handbook) l'a relayé largement.

## Les 4 piliers (formalisation communauté, pas Karpathy)

Les 4 piliers sont une **formalisation post-tweet par la communauté** (keyvalue.systems + handbook davidkimai/Context-Engineering "inspired by Karpathy"). Karpathy lui-même n'a pas listé "4 piliers" — il a juste tweeté l'endorsement initial.

1. **Composition** — Assembler les bons éléments pour la tâche
2. **Ranking** — Ordonner par pertinence
3. **Optimization** — Densité signal/bruit
4. **Orchestration** — Distribution entre agents/calls

## Principes empiriques (sources convergentes)

- **Dégradation des performances vers 4K tokens** — Stanford "lost-in-the-middle" : avec ~20 documents (~4000 tokens), précision LLM chute de 70-75% à 55-60%. Pas de seuil "3K" attesté.
- **CoT redondant sur reasoning models** — OpenAI Reasoning best practices : *"these models perform reasoning internally, prompting them to think step by step is unnecessary"* (concerne o3, GPT-5 thinking, Opus 4.7 extended thinking)
- **ALL-CAPS : effet limité sur Claude récents** — PromptHub/DreamHost notent que ALL-CAPS *"no longer guarantees compliance with newer Claude models"*. NUANCE : "ineffective" ≠ "harmful" — Anthropic l'utilise toujours dans le system prompt Claude 4.
- **Effort via API, pas langage naturel** — passer `effort.level` dans la config plutôt que "please think very hard" dans le prompt

## Pas de "sweet spot 150-300 mots"

Le chiffre "sweet spot 150-300 mots" cité dans des guides tiers (The AI Corner 2026) **n'est pas attesté chez Anthropic ni Karpathy**. À traiter comme heuristique de bloggers, pas comme standard canonique.

## Leak Claude Code — révélation d'architecture

Le leak du code source Claude Code (31 mars 2026, **512K+ lignes / 1900 fichiers TypeScript, 59.8 MB source map**) a révélé l'architecture de context engineering Anthropic : assemblage dynamique conditionnel du system prompt, deferred tools, compaction. Voir note `claude-code-source-leak` (à créer).

## Liens

- [[LLM Wiki]] — pattern Karpathy connexe
- [[Andrej Karpathy]]
- [[Context Management]]
- [[MOC-Techniques]]
