---
titre: "Serving & optimisation d'inférence LLM — vLLM, SGLang, quantification, désagrégation P/D"
resume: "Choix et tuning du serving LLM en production : continuous batching, PagedAttention vs RadixAttention, quantification FP8/AWQ/GPTQ, speculative decoding EAGLE-3, désagrégation prefill/decode, métriques TTFT/TPOT"
aliases:
  - serving inference
  - vLLM tuning
  - SGLang RadixAttention
  - speculative decoding EAGLE-3
  - quantification FP8 AWQ GPTQ
  - désagrégation prefill decode
domaine: ia
type: technique
derniere-maj: 2026-06-07
auteur: claude
sources:
  - "https://blog.vllm.ai/2023/06/20/vllm.html"
  - "https://arxiv.org/abs/2503.01840"
  - "[[reference-technique-stack-ia]]"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/infrastructure"
---

## Description

Le serving d'inférence générale (distinct du serving d'adaptateurs fine-tunés, cf [[fine-tuning-infrastructure]]) optimise débit et latence d'un LLM en production. Le levier dominant : la gestion du KV-cache et le batching. Référence exhaustive sourcée VÉRIFIÉ/RAPPORTÉ : [[reference-technique-stack-ia]] §2.

## Moteurs — décision

| Moteur | Défaut pour | Bascule si |
|--------|-------------|------------|
| **vLLM** (PagedAttention) | Batch de prompts uniques, multi-hardware (TPU/Trainium/Gaudi), compatibilité modèle large | — |
| **SGLang** (RadixAttention) | DeepSeek, conversationnel multi-tours, structured output, préfixes partagés | +29 % à 6,4× débit sur fort partage de préfixe (RAG/agents) |
| **TensorRT-LLM** | Hopper/Blackwell, exploiter FP8/FP4 à fond, backend XGrammar | accepter le coût de compilation des moteurs |

> SGLang ~29 % > vLLM sur H100 (16 200 vs 12 500 tok/s, Llama-3.1-8B, ShareGPT) ; écart réduit à 3-5 % à 70B. Sous très haute concurrence, le routage Python SGLang souffre de la contention GIL → vLLM (routage C++/CUDA) peut scaler mieux (GitHub #21061). Benchmarker sur charge réelle, jamais sur le chiffre de tête. Chiffres RAPPORTÉS (benchmarks tiers).

## PagedAttention vs RadixAttention

- **PagedAttention (vLLM, papier Kwon et al., SOSP 2023)** : KV-cache en blocs de taille fixe (16 tokens/bloc par défaut), alloués à la demande comme la pagination mémoire d'un OS. Fragmentation 60-80 % → <4 %. Prefix caching par hash de blocs.
- **RadixAttention (SGLang, LMSYS)** : KV-cache en arbre radix (trie compressé) indexé au token, découverte auto des préfixes partagés, éviction LRU des feuilles. Priorise les requêtes à plus long préfixe partagé.

## Paramètres vLLM clés (VÉRIFIÉ-SOURCE docs)

- `--gpu-memory-utilization` : 0,90-0,95 (jamais >0,95 : marge activations + contexte CUDA). Bare-metal dédié = 0,95.
- `--max-num-seqs` : nombre max de séquences concurrentes (256-512 pour API à fort trafic).
- `--max-num-batched-tokens` : 8 192-16 384 sur grande VRAM. **Augmenter `max-num-seqs` sans l'augmenter affame le scheduler**.
- `--tensor-parallel-size` = nb GPU. **Piège : TP=4 quand le modèle tient sur 1 GPU réduit le débit** (overhead NCCL AllReduce à chaque couche).
- **Chunked prefill** : découpe les longs prefills pour ne pas bloquer le decode (compromis TTFT/TPOT).
- Continuous batching actif par défaut (niveau itération, hérité ORCA/OSDI 2022). Le moteur **V1** supprime la distinction prefill/decode au scheduling, intègre FlashAttention 3, transferts DMA zero-copy.

## Quantification

| Format | Qualité | Débit | Quand |
|--------|---------|-------|-------|
| **FP8 (W8A8-FP)** | quasi-intacte, sans calibration | — | défaut Hopper/Blackwell |
| **AWQ / GPTQ (INT4, W4A16)** | quasi identique (GPTQ léger + sur tâches réelles) | ≈3× BF16 | VRAM contrainte |
| INT8 SmoothQuant | nécessaire pour W8A8-INT à 70B | — | sinon chute précision |
| GGUF | overhead vLLM (~93 tok/s) | — | réserver à llama.cpp/Ollama |

- **Les kernels comptent plus que l'algo** : Marlin-AWQ 741 tok/s (10,9× vs AWQ naïf), Marlin-GPTQ 712 tok/s (RAPPORTÉ JarvisLabs).
- **Éviter INT4 pour maths/code/raisonnement** (perte la plus visible). FP8 si hardware le permet (ZeroQuant-FP : FP8 > INT8 pour les activations).
- **KV-cache** : vLLM supporte FP8 (E4M3/E5M2), **pas INT8**. 4-bit/2-bit KV dégrade (chute MMLU). Cf [[prompt-caching-kv-cache]].
- **multi-LoRA sur INT4** : utiliser **GPTQ-Int4** (NVFP4/MXFP8 Blackwell ne supportent pas encore les adaptateurs LoRA).

## Speculative decoding

Métrique reine : **taux d'acceptation α** (et longueur d'acceptation moyenne τ). À α=0,6-0,8 (réaliste avec un draft EAGLE3) → 2-3×. **α<0,5 nuit** (cycles gaspillés). α dépend de la tâche (0,75-0,85 sur code/écriture formelle). **N'activer que si α mesuré >0,6 sur le trafic réel.**

- **EAGLE-3** (arXiv 2503.01840, repo SafeAILab) : 3,0-6,5× vs autoregressif vanilla, +20-40 % vs EAGLE-2. Entraîné en « training-time test » → α quasi constant selon la position du token.
- **Medusa** : têtes de décodage indépendantes (K=6), self-distillation, setup simple mono-GPU, pas lossless à T=1.
- **MTP** : DeepSeek-V3 embarque un module natif (tête de brouillon fine-tunable).
- **n-gram / PLD (prompt lookup)** : brouillon par copie du contexte, utile quand la génération répète le prompt (code), inutile sinon.
- **Cursor « speculative edits »** (blog Cursor/Fireworks) : ~1000 tok/s (~3500 char/s) sur 70B, ~13× vs vanilla Llama-3-70b. Tous les gains diminuent à très grand batch (le cible devient compute-bound).

## Désagrégation prefill/decode & métriques

- **Prefill** = compute-bound (traitement parallèle du prompt, produit le KV) ; **decode** = memory-bound (génération token par token). Les co-localiser crée de l'interférence.
- **Désagrégation P/D** (DistServe OSDI 2024, Splitwise) : pools GPU dédiés, transfert KV via NVLink (600 GB/s) / InfiniBand. **DeepSeek-V3 en prod** (Hao AI Lab @ UCSD) : 3 nœuds prefill + 9 nœuds decode (8×H100 chacun), EP decode ≈256, lib 3FS pour le transfert KV. Devenu standard (vLLM, SGLang, TensorRT-LLM, NVIDIA Dynamo, LMDeploy).
- **Arbitrage SLO (papier TaiChi)** : agrégation P/D optimale sous TTFT serré + TPOT relâché ; désagrégation optimale sous TPOT serré + TTFT relâché. DistServe : 1,6-7,4× débit à SLO tenu vs DeepSpeed-MII.
- **Métriques** : **TTFT** (time-to-first-token, latence prefill), **TPOT/ITL** (time-per-output-token, latence decode). Optimiser le débit agrégé se fait souvent au détriment du TTFT/TPOT individuel — arbitrer selon l'usage (chat = TPOT, batch = débit).

## Liens

- [[reference-technique-stack-ia]] — référence exhaustive sourcée §2
- [[prompt-caching-kv-cache]] — optimisation tokens côté API + KV-cache serveur
- [[fine-tuning-infrastructure]] — serving d'adaptateurs LoRA, GPUs, coûts cloud
- [[stack-python-ia]] — où le serving s'insère dans la stack Python
- [[MOC-Techniques]]
