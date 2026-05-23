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
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://arxiv.org/abs/2305.18290"
  - "https://arxiv.org/abs/2403.07691"
  - "https://arxiv.org/abs/2503.14476"
  - "https://arxiv.org/abs/2405.14734"
  - "https://arxiv.org/abs/2402.01306"
  - "https://arxiv.org/abs/2402.03300"
  - "https://arxiv.org/abs/2501.12948"
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
| **SimPO** | Yu Meng, Xia, Chen (Princeton) | 1 modèle | Haute | DPO moins cher, +6.4 pts AlpacaEval 2 |
| **ORPO** | Hong, Lee, Thorne (KAIST) | 1 modèle | Haute | SFT + alignement en 1 pass |
| **KTO** | Ethayarajh et al. (Contextual AI, ICML 2024) | 1-2 modèles | Haute | Feedback binaire (thumbs up/down) |
| **PPO** (RLHF) | OpenAI | 3-4 modèles | Basse | Labs frontier, compute massif |
| **GRPO** | DeepSeek | Réduit mémoire vs PPO (chiffre non sourcé dans paper) | Moyenne | Raisonnement (math, code) |
| **DAPO** | ByteDance Seed et al. | ~GRPO | Haute | 50 pts AIME 2024 (Qwen2.5-32B), CoT long |

## Pipeline Production 2026 (3 stages)

```
SFT (1-10M examples) → DPO/SimPO/ORPO → GRPO/DAPO
    instruction following    alignement valeurs    raisonnement
```

## RLVR — Le shift majeur 2025-2026

**Reinforcement Learning with Verifiable Rewards** : remplace les labels humains par une vérification automatisée (tests unitaires, proof checkers, math evaluators). DeepSeek-R1 a démontré que le RL pur avec récompenses vérifiables produit des capacités de raisonnement émergentes sans traces de raisonnement labellisées.

## DPO — Direct Preference Optimization

[Rafailov, Sharma, Mitchell, Ermon, Manning, Finn (Stanford), arXiv 2305.18290](https://arxiv.org/abs/2305.18290). Traite l'alignement comme une classification sur des paires de préférence. Pas besoin d'ingénierie RL. Défaut pour la plupart des équipes.

## SimPO — Simple Preference Optimization

[Yu Meng, Mengzhou Xia, Danqi Chen (Princeton NLP), arXiv 2405.14734](https://arxiv.org/abs/2405.14734). Reference-free reward, 1 seul modèle. Verbatim : *"by as much as 6.4 points on AlpacaEval 2"* vs DPO.

## KTO — Kahneman-Tversky Optimization

[Ethayarajh, Xu, Muennighoff, Jurafsky, Kiela (Contextual AI), arXiv 2402.01306, ICML 2024](https://arxiv.org/abs/2402.01306). Feedback binaire (thumbs up/down) au lieu de paires de préférence.

## DAPO — Decoupled Clip and Dynamic Sampling Policy Optimization

["DAPO: An Open-Source LLM Reinforcement Learning System at Scale", arXiv 2503.14476](https://arxiv.org/abs/2503.14476). Atteint 50 pts AIME 2024 avec Qwen2.5-32B.

## GRPO — Group Relative Policy Optimization

[DeepSeek, arXiv 2402.03300](https://arxiv.org/abs/2402.03300), introduit avec DeepSeekMath. Pas de value model, pas de reward model séparés. Le paper évoque "optimizing the memory usage of PPO" sans chiffrer le gain. Technique dominante pour les modèles de raisonnement 2025-2026.

## ORPO — Odds Ratio Preference Optimization

[Jiwoo Hong, Noah Lee, James Thorne (KAIST), arXiv 2403.07691](https://arxiv.org/abs/2403.07691). Fusionne SFT + alignement en un seul pass via odds ratios. Zéro dépendance externe. Idéal single-GPU, petits modèles.

## Liens

- [[MOC-Techniques]]
- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, DoRA
- [[Nathan Lambert]] — expert RLHF, premier textbook
- [[fine-tuning-frameworks]] — implémentations dans TRL, Axolotl