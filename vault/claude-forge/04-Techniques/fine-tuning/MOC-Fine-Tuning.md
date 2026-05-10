---
titre: "MOC Fine-Tuning — Index complet"
resume: "Index de toutes les notes fine-tuning — techniques PEFT, alignement, frameworks, modèles, datasets, évaluation, infrastructure, privacy"
aliases:
  - "MOC Fine-Tuning"
  - "index fine-tuning"
  - "fine-tuning LLM"
  - "guide fine-tuning"
type: index
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
---

# Fine-Tuning LLM — Guide Complet

## Techniques

- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, DoRA, Spectrum, IA3, configs recommandées
- [[fine-tuning-alignment]] — DPO, GRPO, ORPO, SimPO, DAPO, RLHF, pipeline 3 stages
- [[rag-vs-fine-tuning]] — quand RAG, quand fine-tuning, quand hybride, RAFT

## Outils

- [[fine-tuning-frameworks]] — Unsloth, Axolotl, LLaMA-Factory, TRL, Ludwig, MLX
- [[fine-tuning-datasets]] — préparation données, qualité, synthétique, Argilla, Distilabel
- [[fine-tuning-evaluation]] — benchmarks, LLM-as-judge, métriques post-FT

## Infrastructure

- [[fine-tuning-infrastructure]] — GPUs, cloud providers, serving (vLLM, SGLang, Ollama), coûts
- [[fine-tuning-models]] — meilleurs modèles open-source par taille et cas d'usage
- [[fine-tuning-privacy]] — on-premise, RGPD, VaultGemma, federated learning, TEE

## Leaders

### Chercheurs
- [[Edward Hu]] — inventeur LoRA
- [[Tim Dettmers]] — créateur QLoRA, bitsandbytes
- [[Tri Dao]] — FlashAttention
- [[Song Han]] — AWQ (MIT)

### Créateurs d'outils
- [[Daniel Han]] — Unsloth
- [[Wing Lian]] — Axolotl
- [[Yaowei Zheng]] — LLaMA-Factory
- [[Georgi Gerganov]] — llama.cpp, GGUF
- [[Philipp Schmid]] — guides fine-tuning HuggingFace

### Éducateurs
- [[Sebastian Raschka]] — "Build a LLM From Scratch"
- [[Maxime Labonne]] — LLM Course (70K+ stars)
- [[Nathan Lambert]] — textbook RLHF, Interconnects
- [[Hamel Husain]] — Mastering LLMs course

### Modèles open-source
- [[Arthur Mensch]] — Mistral AI
- [[Liang Wenfeng]] — DeepSeek

## Connexions

- [[RAG]] — MOC RAG (complémentaire au fine-tuning)
- [[Expertise-IA]] — roadmap expertise (fine-tuning = gap prioritaire)
- [[rag-architecture]] — patterns RAG avancés, section RAG vs FT