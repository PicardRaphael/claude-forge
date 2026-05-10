---
titre: "Fine-Tuning Infrastructure — GPUs, Cloud, Serving, Coûts"
resume: "Guide infrastructure fine-tuning LLM 2026 — GPUs (RTX 5090, A100, H100), cloud providers (RunPod, Lambda, Vast.ai, Together AI), serving (vLLM, SGLang, Ollama), prix comparés"
aliases:
  - "GPU fine-tuning"
  - "cloud fine-tuning"
  - "infrastructure LLM"
  - "RTX 5090 fine-tuning"
  - "H100 fine-tuning"
  - "vLLM"
  - "SGLang"
  - "serving LLM"
  - "Ollama serving"
  - "RunPod"
  - "Lambda Labs"
  - "Together AI"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/"
  - "https://www.runpod.io/articles/guides/top-cloud-gpu-providers"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/infrastructure"
---

## GPUs Recommandés

### Consumer

| GPU | VRAM | Bande passante | Prix | Meilleur pour |
|-----|------|---------------|------|---------------|
| **RTX 5090** | 32 GB GDDR7 | 1,792 GB/s | $1,999 | Meilleur consumer. 70B Q4, 13B FP16 LoRA |
| **RTX 4090** | 24 GB GDDR6X | 1,008 GB/s | $1,599 | Excellent. 7-13B QLoRA |
| RTX 3090 (occasion) | 24 GB | 936 GB/s | ~$700 | Budget, 13B FP16 + 70B Q4 |

### Data Center

| GPU | VRAM | Cloud $/hr (neocloud) | Cloud $/hr (hyperscaler) |
|-----|------|----------------------|-------------------------|
| **A100 80GB** | 80 GB HBM2e | $1.07-1.89 | $3.43-5.78 |
| **H100 SXM** | 80 GB HBM3 | $2.10-2.69 | $6.88-12.29 |
| **H200** | 141 GB HBM3e | $2.60-3.59 | $4.98-13.78 |
| **B200** | 192 GB HBM3e | $4.00-6.02 | $14.24 |

## Cloud Providers — Prix mai 2026

### Managed Fine-Tuning

| Provider | Prix (70B LoRA, 10M tokens) | Forces |
|----------|-----------------------------|--------|
| **Together AI** | ~$29 ($2.90/M) | Meilleur rapport qualité/prix, 200+ modèles |
| **Vertex AI** | ~$30 ($3/M, Gemini Flash) | Pas de surcoût hosting |
| **AWS Bedrock** | ~$80 ($7.99/M) | Écosystème AWS |

### GPU Rental

| Provider | H100/hr | RTX 4090/hr | Type |
|----------|---------|-------------|------|
| **Vast.ai** | ~$1.49 | $0.35 | P2P marketplace |
| **RunPod** | $2.69 | $0.34 | Balance prix/fiabilité |
| **Lambda Labs** | $2.49 | — | ML-focused |
| **Nebius** | $2.95 | — | Neocloud ($6B+ cash) |
| **CoreWeave** | Premium | — | Top tier, InfiniBand |

**Règle :** Neoclouds = 40-70% moins cher que hyperscalers pour le même GPU.

## Serving / Inférence

| Engine | Throughput (H100, 70B) | Statut 2026 | Meilleur pour |
|--------|----------------------|-------------|---------------|
| **SGLang** | ~16,200 tok/s | Rising | Raisonnement, shared-prefix |
| **vLLM** | ~12,500 tok/s | Safe default | Batch, multi-hardware |
| **TGI** | ~2,500 tok/s | **MAINTENANCE** | Ne plus utiliser |
| **Ollama** | Consumer | Actif | Local, simple |
| **llama.cpp** | CPU + GPU | Actif | Fondation écosystème local |

### Quantization GGUF recommandée

- **Q4_K_M** : défaut (~4.5 GB pour 7B), meilleur rapport qualité/taille
- **Q5_K_M** : 20% plus gros, qualité notablement meilleure
- **Q8_0** : quasi-FP16, bon pour validation

## TCO Local vs Cloud

**Seuil de rentabilité local :** >500,000 tokens/jour, ROI 12-18 mois.

**Recommandation :** Hybride — local pour throughput prévisible, cloud pour overflow et expérimentation.

## Liens

- [[fine-tuning-models]] — quel modèle pour quel GPU
- [[fine-tuning-privacy]] — solutions on-premise
- [[Georgi Gerganov]] — créateur llama.cpp
- [[Daniel Han]] — créateur Unsloth