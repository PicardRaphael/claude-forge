---
titre: "Fine-Tuning PEFT — LoRA, QLoRA, DoRA, Spectrum"
resume: "Techniques parameter-efficient pour fine-tuner des LLM — LoRA, QLoRA, DoRA, Spectrum, IA3, comparatifs VRAM et configs recommandées 2026"
aliases:
  - "PEFT"
  - "LoRA"
  - "QLoRA"
  - "DoRA"
  - "parameter efficient fine-tuning"
  - "fine-tuning techniques"
  - "rsLoRA"
  - "Spectrum fine-tuning"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://arxiv.org/abs/2106.09685"
  - "https://arxiv.org/abs/2305.14314"
  - "https://arxiv.org/abs/2402.09353"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
---

## Comparatif PEFT (mai 2026)

| Technique | Params entraînés | VRAM (7B) | Overhead inférence | Créateur |
|-----------|-----------------|-----------|-------------------|----------|
| **LoRA** | 0.1-1% | 16-24 GB FP16 | Zéro (merged) | [[Edward Hu]] |
| **QLoRA** | 0.1-1% | 6-12 GB | Zéro (merged) | [[Tim Dettmers]] |
| **DoRA** | ~0.1-1% | LoRA +5-10% | Zéro (merged) | — |
| **rsLoRA** | = LoRA | = LoRA | Zéro | — |
| **IA3** | 0.01-0.02% | Minimal | Zéro | — |
| **Spectrum** | 25-50% couches | -36% vs full FT | Zéro | — |
| **Prefix Tuning** | ~0.1% | Faible | Léger (virtual tokens) | — |
| **Full Fine-Tuning** | 100% | 56+ GB (7B FP16) | Zéro | — |

## LoRA — Low-Rank Adaptation

Injecte des matrices de faible rang (A, B) dans les couches attention. Poids base gelés. Standard industriel depuis 2021.

**Config recommandée 2026 :** `r=16, alpha=16, target_modules="all-linear", 2-3 epochs, lr=2e-4`

**Insight NeurIPS 2025 :** LoRA produit des "intruder dimensions" — LoRA match les perfs sur la tâche cible mais dégrade la distribution de pré-entraînement. Dataset size ≈ trainable LoRA params = sweet spot.

## QLoRA — Quantized LoRA

LoRA + quantization NF4 4-bit du modèle base. Réduit VRAM de ~75%. Fine-tune un 65B sur un seul GPU 48GB.

## DoRA — Weight-Decomposed LoRA

Décompose les mises à jour en magnitude + direction. Maintient la qualité à rank 8 là où LoRA nécessite rank 32.

## Spectrum — SNR-Based Layer Selection

Entraîne seulement les couches à haut Signal-to-Noise Ratio. Alternative à la quantization : précision complète sur les couches qui comptent.

## Quand utiliser quoi

| Situation | Technique |
|-----------|-----------|
| Défaut, la plupart des cas | LoRA (DoRA enabled) |
| GPU consumer (RTX 4090) | QLoRA |
| Qualité maximale, gros dataset | Full Fine-Tuning |
| Très peu de params, multi-task | IA3 |
| Rank élevé sans instabilité | rsLoRA |

## Liens

- [[MOC-Techniques]]
- [[fine-tuning-alignment]] — techniques d'alignement (DPO, GRPO)
- [[fine-tuning-frameworks]] — Unsloth, Axolotl, LLaMA-Factory
- [[Edward Hu]] — inventeur LoRA
- [[Tim Dettmers]] — créateur QLoRA