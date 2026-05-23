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
derniere-maj: 2026-05-23
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

## Sources canoniques

- **Few-shot CoT** : Wei et al 2022 — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* ([arxiv 2201.11903](https://arxiv.org/abs/2201.11903))
- **Zero-shot CoT** : Kojima et al 2022 — *Large Language Models are Zero-Shot Reasoners* ([arxiv 2205.11916](https://arxiv.org/abs/2205.11916)) — papier qui introduit "Let's think step by step"

## Variantes

- **Zero-shot CoT** : "Let's think step by step" (Kojima 2022)
- **Few-shot CoT** : exemples avec raisonnement montré (Wei 2022)
- **Auto-CoT** : le modèle génère ses propres exemples (Zhang et al 2023)
- **Self-Consistency** : Wang et al 2022 ([arxiv 2203.11171](https://arxiv.org/abs/2203.11171))

## Liens

- [[MOC-Prompts]]
- [[index-prompting]]
- [[Adaptive Thinking]]
- [[deprecated-techniques-2026]]
