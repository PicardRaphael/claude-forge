---
titre: "Chain of Thought (CoT)"
resume: "Forcer le raisonnement étape par étape — efficace sur tâches logiques, mathématiques, code complexe. Moins utile sur frontier 2026."
aliases:
  - "chain of thought"
  - "CoT"
  - "raisonnement étape par étape"
  - "let's think step by step"
  - "chain-of-thought prompting"
type: technique
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Principe

Demander au modèle de raisonner étape par étape avant de donner sa réponse. Force la décomposition du problème.

## Quand utiliser

- Problèmes mathématiques ou logiques
- Debugging code complexe
- Raisonnement multi-étapes
- Modèles non-frontier (Haiku, petits modèles)

## Quand NE PAS utiliser

- Modèles frontier 2026 (Opus 4.7, GPT-5.x) — ils raisonnent déjà nativement
- Tâches simples (classification, extraction) — ajoute de la latence sans gain
- Avec [[Adaptive Thinking]] activé — le modèle gère déjà son budget de réflexion

## Variantes

- **Zero-shot CoT** : "Let's think step by step"
- **Few-shot CoT** : exemples avec raisonnement montré
- **Auto-CoT** : le modèle génère ses propres exemples

## Liens

- [[index-prompting]]
- [[Adaptive Thinking]]
- [[deprecated-techniques-2026]]
