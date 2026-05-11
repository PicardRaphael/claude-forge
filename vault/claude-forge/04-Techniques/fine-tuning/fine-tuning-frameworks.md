---
titre: "Fine-Tuning Frameworks — Unsloth, Axolotl, LLaMA-Factory, TRL"
resume: "Comparatif des frameworks de fine-tuning LLM 2026 — Unsloth (2-5x), LLaMA-Factory (GUI), Axolotl (production), TRL (alignement), Ludwig, MLX"
aliases:
  - "Unsloth"
  - "Axolotl"
  - "LLaMA-Factory"
  - "LlamaFactory"
  - "TRL"
  - "fine-tuning frameworks"
  - "outils fine-tuning"
  - "Ludwig fine-tuning"
  - "mlx-tune"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://unsloth.ai"
  - "https://github.com/hiyouga/LlamaFactory"
  - "https://github.com/axolotl-ai-cloud/axolotl"
  - "https://github.com/huggingface/trl"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/outils"
---

## Comparatif Frameworks (mai 2026)

| Framework | Stars | Vitesse | Forces | Créateur |
|-----------|-------|---------|--------|----------|
| **LLaMA-Factory** | ~68K | Bonne | Web UI, 300+ modèles, zero-code | [[Yaowei Zheng]] |
| **Unsloth** | ~54K | **2-5x faster** | Kernels Triton, -70% VRAM | [[Daniel Han]] |
| **TRL** (HuggingFace) | ~18K | Baseline | Réf SFT/DPO/GRPO, v1.0 mars 2026 | HuggingFace |
| **PEFT** (HuggingFace) | ~17K | Baseline | 20+ méthodes PEFT | HuggingFace |
| **Ludwig** | ~12K | Bonne | YAML déclaratif, multimodal, Ray | — |
| **Axolotl** | ~11K | Bonne | Config YAML, FSDP/DeepSpeed, multi-node | [[Wing Lian]] |
| **torchtune** | ~4K | Bonne | PyTorch-native, Meta-backed | Meta |
| **MLX / mlx-tune** | ~4K | Rapide Apple | Apple Silicon natif, 3-5 min | Apple |

## Recommandations par profil

| Profil | Framework |
|--------|-----------|
| Débutant, premier fine-tuning | LLaMA-Factory (web UI) |
| GPU unique, vitesse prioritaire | Unsloth |
| Alignement, recherche | TRL + PEFT |
| Production multi-GPU, reproductibilité | Axolotl |
| Apple Silicon (M1-M4) | mlx-lm / mlx-tune |

## Benchmark (Llama 3.1 8B, A100 40GB, QLoRA, 2 epochs)

- **Unsloth** : 3.2 heures
- **Axolotl** : 5.8 heures
- **TRL (stock)** : ~6-7 heures

## Multi-GPU

- **PyTorch FSDP** : défaut recommandé 2026, 5x plus rapide que DeepSpeed ZeRO-3 sur 100M-1B
- **DeepSpeed ZeRO** : avantage à 10B+, CPU/NVMe offloading

## Liens

- [[MOC-Techniques]]
- [[Daniel Han]] — créateur Unsloth
- [[Wing Lian]] — créateur Axolotl
- [[Yaowei Zheng]] — créateur LLaMA-Factory
- [[fine-tuning-techniques-peft]] — techniques PEFT
- [[fine-tuning-infrastructure]] — GPUs et cloud