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
derniere-maj: 2026-06-17
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

## Variantes DPO 2026

Famille de variantes corrigeant des limites du DPO original (cf [[dpo-derivation]] pour la loss de base).

| Variante | Source | Apport | Cible |
|----------|--------|--------|-------|
| **TDPO** (Token-level DPO) | [arXiv 2404.11999](https://arxiv.org/abs/2404.11999) | KL forward par token + termes KL séquentiels | Alignement + diversité de génération |
| **R-DPO** (Regularized DPO) | [arXiv 2403.19159](https://arxiv.org/abs/2403.19159) « Disentangling Length from Quality » (Park et al.) | Terme de longueur $\alpha|y|$ dans l'objectif | Anti-verbosité (length bias) |
| **Iterative DPO** | survey [arXiv 2503.06072](https://arxiv.org/abs/2503.06072) | Multi-rounds, préférences ré-évaluées (souvent self-judge) | Raffinement continu |
| **Step-wise DPO** | survey 2503.06072 | Partitionne le dataset, politique du round N = baseline du round N+1 | Updates itératifs stables |
| **SimPO** | (déjà au comparatif) | Reference-free, normalise la longueur | DPO moins cher, 1 modèle |

## Nouveautés GRPO 2026

Le cluster GRPO s'est densifié fin 2025 / 2026 autour de deux axes : **réduire le coût** et **corriger le biais de longueur / l'assignation de crédit**.

| Méthode | Source | Apport clé | Résultat sourcé |
|---------|--------|-----------|-----------------|
| **Dr. GRPO** | [arXiv 2503.20783](https://arxiv.org/abs/2503.20783) (Liu et al., sail-sg) | Retire la normalisation de longueur ET d'écart-type → estimateur non biaisé | 43.3 % AIME 2024 (7B), 27h sur 8×A100 |
| **2-GRPO** « Your GRPO Is Secretly DPO » | [arXiv 2510.00977](https://arxiv.org/abs/2510.00977) (Wu et al.) | GRPO = objectif contrastif implicite ≈ DPO ; 2 rollouts suffisent | 97.6 % de la perf de 16-GRPO, 12.5 % des rollouts, 21 % du temps |
| **λ-GRPO** | [arXiv 2510.06870](https://arxiv.org/abs/2510.06870) (Wang et al.) | Paramètre $\lambda$ **apprenable** pour le poids token-level (unifie les variantes) | +1–2 % vs GRPO vanilla (Qwen2.5 1.5/3/7B), sans coût ajouté |
| **GRPO-λ** | [arXiv 2510.00194](https://arxiv.org/abs/2510.00194) (Parthasarathi et al.) | λ-return + eligibility traces, approximation critic-free du TD-error | +3 pts moyenne (AIME24/Math500/Olympiad/Minerva/AMC), +4.5 pts en 7B |
| **RLOO** (REINFORCE Leave-One-Out) | [arXiv 2402.14740](https://arxiv.org/abs/2402.14740) (Ahmadian et al., « Back to Basics ») | Baseline REINFORCE par leave-one-out → estimateur d'avantage non biaisé | Surpasse DPO/PPO quand on génère plus d'échantillons on-policy |

⚠️ **Ne pas confondre** : `λ-GRPO` (2510.06870, token preferences apprenables) et `GRPO-λ` (2510.00194, credit assignment) sont **deux papiers distincts** — noms quasi identiques, contributions différentes.

## Le problème du Length Bias (transversal)

Les méthodes modernes de policy/preference optimization exhibent presque toutes un **biais de longueur** : tendance à générer des réponses inutilement longues même quand une réponse concise suffirait.

- Une grande part des gains de récompense en RLHF vient de l'**augmentation de longueur**, pas d'une amélioration substantielle de qualité.
- Le problème persiste dans GRPO car l'avantage est appliqué uniformément sur tous les tokens d'une réponse.
- Corrections directes : **Dr. GRPO** (retire la normalisation de longueur), **R-DPO** (pénalité $\alpha|y|$), **λ-GRPO** (poids token apprenable).

## Liens
- [[dpo-derivation]] — dérivation mathématique complète de la loss DPO

- [[MOC-Techniques]]
- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, DoRA
- [[Nathan Lambert]] — expert RLHF, premier textbook
- [[fine-tuning-frameworks]] — implémentations dans TRL, Axolotl