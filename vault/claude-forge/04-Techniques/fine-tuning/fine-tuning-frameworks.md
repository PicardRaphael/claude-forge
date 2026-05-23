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
derniere-maj: 2026-05-23
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
| **LLaMA-Factory** | ~71.5K | Bonne | Web UI, 300+ modèles, zero-code | [[Yaowei Zheng]] |
| **Unsloth** | ~65K | **2-5x faster** | Kernels Triton, -70% VRAM | [[Daniel Han]] |
| **MLX** (Apple) | ~26.4K | Rapide Apple | Apple Silicon natif, framework array | Apple ml-explore |
| **TRL** (HuggingFace) | ~18K | Baseline | Réf SFT/DPO/GRPO, **v1.0 mars 2026** | HuggingFace |
| **PEFT** (HuggingFace) | ~17K | Baseline | 20+ méthodes PEFT | HuggingFace |
| **Ludwig** | ~12K | Bonne | YAML déclaratif, multimodal, Ray | — |
| **Axolotl** | ~12K | Bonne | Config YAML, FSDP/DeepSpeed, multi-node | [[Wing Lian]] |
| **torchtune** | ~5.8K | ⚠️ **No longer maintained (2025)** | PyTorch-native, archivé | Meta |

## Recommandations par profil

| Profil | Framework |
|--------|-----------|
| Débutant, premier fine-tuning | LLaMA-Factory (web UI) |
| GPU unique, vitesse prioritaire | Unsloth |
| Alignement, recherche | TRL + PEFT |
| Production multi-GPU, reproductibilité | Axolotl |
| Apple Silicon (M1-M4) | mlx-lm / MLX |

⚠️ **torchtune** : ne pas recommander en 2026, le développement a pris fin en 2025 (README officiel).

## Benchmark (Llama 3.1 8B, A100 40GB, QLoRA, 2 epochs, 512 tokens)

- **Unsloth** : 3.2 heures (confirmé via comparatif communauté)
- **Axolotl** : 5.8 heures (confirmé)
- **TRL (stock)** : ~similaire à Axolotl (chiffre exact non sourcé en source primaire)

## Multi-GPU

- **PyTorch FSDP** : défaut recommandé 2026 sur 100M-1B (GPU util ~60% vs ~45% DeepSpeed, mémoire légèrement inférieure — [HF docs](https://huggingface.co/docs/accelerate/en/concept_guides/fsdp_and_deepspeed))
- **DeepSpeed ZeRO** : avantage au-delà ~10B grâce à CPU/NVMe offloading et ZeRO-Infinity

## Liens

- [[MOC-Techniques]]
- [[Daniel Han]] — créateur Unsloth
- [[Wing Lian]] — créateur Axolotl
- [[Yaowei Zheng]] — créateur LLaMA-Factory
- [[fine-tuning-techniques-peft]] — techniques PEFT
- [[fine-tuning-infrastructure]] — GPUs et cloud