---
titre: "Fine-Tuning Alignment — DPO, GRPO, ORPO, RLHF"
resume: "Techniques d'alignement et préférence pour LLM — DPO, SimPO, ORPO, GRPO, DAPO, PPO/RLHF, pipeline production 3 stages 2026"
aliases:
  - "DPO"
  - "GRPO"
  - "ORPO"
  - "RLHF"
  - "SimPO"
  - "DAPO"
  - "alignment fine-tuning"
  - "preference optimization"
  - "post-training"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://arxiv.org/abs/2305.18290"
  - "https://arxiv.org/abs/2403.07691"
  - "https://arxiv.org/abs/2503.14476"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/alignment"
---

## Comparatif Alignement (mai 2026)

| Technique | Créateur | Mémoire | Stabilité | Meilleur pour |
|-----------|----------|---------|-----------|---------------|
| **DPO** | [[Rafael Rafailov]] (Stanford) | 2 modèles (policy + ref) | Haute | Défaut alignement |
| **SimPO** | — | 1 modèle | Haute | DPO moins cher, +6.4 pts AlpacaEval |
| **ORPO** | KAIST (Corée) | 1 modèle | Haute | SFT + alignement en 1 pass |
| **KTO** | — | 1-2 modèles | Haute | Feedback binaire (thumbs up/down) |
| **PPO** (RLHF) | OpenAI | 3-4 modèles | Basse | Labs frontier, compute massif |
| **GRPO** | DeepSeek | -50% vs PPO | Moyenne | Raisonnement (math, code) |
| **DAPO** | — | ~GRPO | Haute | Chain-of-thought long, surpasse GRPO sur AIME |

## Pipeline Production 2026 (3 stages)

```
SFT (1-10M examples) → DPO/SimPO/ORPO → GRPO/DAPO
    instruction following    alignement valeurs    raisonnement
```

## RLVR — Le shift majeur 2025-2026

**Reinforcement Learning with Verifiable Rewards** : remplace les labels humains par une vérification automatisée (tests unitaires, proof checkers, math evaluators). DeepSeek-R1 a démontré que le RL pur avec récompenses vérifiables produit des capacités de raisonnement émergentes sans traces de raisonnement labellisées.

## DPO — Direct Preference Optimization

Traite l'alignement comme une classification sur des paires de préférence. Pas besoin d'ingénierie RL. Défaut pour la plupart des équipes.

## GRPO — Group Relative Policy Optimization

Développé par DeepSeek pour DeepSeekMath. Pas de value model, pas de reward model séparés. Technique dominante pour les modèles de raisonnement 2025-2026.

## ORPO — Odds Ratio Preference Optimization

Fusionne SFT + alignement en un seul pass via odds ratios. Zéro dépendance externe. Idéal single-GPU, petits modèles.

## Liens

- [[MOC-Techniques]]
- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, DoRA
- [[Nathan Lambert]] — expert RLHF, premier textbook
- [[fine-tuning-frameworks]] — implémentations dans TRL, Axolotl