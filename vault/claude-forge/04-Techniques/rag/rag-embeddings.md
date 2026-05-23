---
titre: "RAG Embeddings — Modèles et optimisation"
resume: "Comparatif modèles d'embedding 2026, fine-tuning, Matryoshka, quantization, multimodal, sparse vs dense vs hybrid"
aliases:
  - RAG embeddings
  - embedding models
  - modèles d'embedding
  - text embeddings
  - vector embeddings
  - embedding optimization
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://milvus.io/blog/choose-embedding-model-rag-2026.md"
  - "https://huggingface.co/blog/embedding-quantization"
  - "https://sbert.net/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Les embeddings transforment le texte en vecteurs numériques pour la recherche sémantique. Le choix du modèle et de la stratégie d'embedding est critique pour la qualité du RAG.

## Top modèles 2026

### API commerciales

| Modèle | MTEB | Dims | Context | Prix/1M tokens |
|--------|------|------|---------|----------------|
| Voyage AI voyage-3-large | 65.1 | 1024 | 32K | $0.06 |
| Cohere embed-v4 (multimodal) | 65.2 | 1536 | 128K | $0.12 |
| Jina embeddings v3 | 65.5 | 1024 | 8K | $0.02 |
| OpenAI text-embedding-3-large | 64.6 | 3072 | 8K | $0.13 |
| Gemini Embedding 2 | top cross-lingual | variable (MRL) | varies | $0.006 |

### Open-source

| Modèle | MTEB v2 | Dims | Context | Licence |
|--------|---------|------|---------|---------|
| Microsoft Harrier-OSS-v1 (27B, mars 2026) | 74.3 (MMTEB v2) | varies | 32K | MIT |
| NV-Embed-v2 | 72.31 (MTEB v1 EN, 2024) | 4096 | 32K | CC-BY-NC-4.0 |
| Jina v5-text-small (677M, fév 2026) | 71.7 (MTEB EN v2) | 1024 | 8K | Apache 2.0 |
| Qwen3-Embedding-8B | 70.58 (MTEB Multilingual) | 1024 | 32K | Apache 2.0 |
| BGE-M3 | 63.0-64.2 | 1024 | 8K | MIT |
| Nomic Embed v1.5 (137M) | 62.39 | 768 | 8K | Apache 2.0 |

**Voyage AI** domine le domain-specific (+4-6 pts MTEB sur **code/legal** — [voyage-law-2 blog](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) ; "médical" non attesté pour Voyage). **BGE-M3** = seul modèle combinant dense+sparse+multi-vector ColBERT dans un seul modèle (Jina v4 = dense+multi-vector sans sparse). **Nomic** = seul avec weights+code+data ouverts.

## Fine-tuning

Améliore le retrieval in-domain de **10-30%**. Atlassian sur JIRA : Recall@60 de **0.751 → 0.951 (+26%)** ([HuggingFace/NVIDIA](https://huggingface.co/blog/nvidia/domain-specific-embedding-finetune)). Démontré possible avec **6300 samples synthétiques en 3 min sur GPU consumer** ([Philipp Schmid](https://philschmid.de/fine-tune-embedding-model-for-rag)).

Techniques clés :
1. **Synthetic data** — LLM génère paires (query, document)
2. **Hard negative mining** — passages proches mais non-pertinents
3. **MultipleNegativesRankingLoss** — objective standard bi-encoder
4. **MRL-aware fine-tuning** — loss Matryoshka multi-dimensions

**Quand fine-tuner** : jargon domaine (legal, médical, financier), min 500-1000 paires. Sinon, hybrid search d'abord.

## Matryoshka Embeddings

Front-load l'information sémantique dans les premières dimensions. Un seul modèle, troncable à l'inférence :

| Dimensions | Économie stockage | Perte précision |
|-----------|-------------------|-----------------|
| 1024 (full) | 0% | 0% |
| 512 | ~50% | Minimale |
| 256 | ~75% | 2-3% |
| 64-128 | 85-94% | Modérée |

À 100M vecteurs : ~$6000/mois en float32, ~$1500/mois en 256d avant quantization.

Standard en 2026 : OpenAI, Cohere, Jina, Nomic, Qwen3.

## Quantization

| Type | Compression | Précision | Usage |
|------|------------|-----------|-------|
| Scalar (int8) | 4x | ~96% avec rescoring | Défaut production |
| Binary (1-bit) | 32x | ~92.5% sans rescoring, ~96% avec | Shortlisting rapide |
| Product (PQ) | Jusqu'à 97% | Dataset-dépendant | Complexe à tuner |

**MRL + int8** combinés = ~16x compression totale depuis 1024d float32.

2026 : Better Binary Quantization (BBQ, Elasticsearch 8.16 nov 2024), Qdrant v1.15.0 1.5-bit (24x compression) et 2-bit (16x).

## Multimodal

- **ColPali** (ICLR 2025) : PaliGemma + ColBERT late interaction sur images de pages. Élimine OCR.
- **[[jina-embeddings-v4|Jina Embeddings v4]]** (3.8B) : text+image, single et multi-vector, LoRA adapters. **JinaVDR 72.19** vs ColPali-v1.2 **64.50** ; **ViDoRe 84.11** mode single-vector (multi-vector = 90.17) ([blog Jina + arXiv 2506.18902](https://jina.ai/news/jina-embeddings-v4)).
- **Jina CLIP v2** : 89 langues, 512x512 images. 75% réduction dimensionnelle → 99% performance.

## Sparse vs Dense vs Hybrid

Dense seul : **78% recall@10**. BM25 seul : **65%**. **Hybrid : 91% recall@10**.

- **BM25** : zero training, parfait pour termes rares/identifiants. Échoue sur mismatch vocabulaire.
- **SPLADE** : sparse appris avec expansion vocabulaire. Pré-calculer à l'indexation.
- **ColBERT** : matrices per-token + MaxSim. PLAID indexing pour le scale. **FastPlaid (LightOn, ACL 2025)** : jusqu'à **554% speedup vs PLAID sur Quora** (H100 GPU). Speedup moyen autres datasets : 174-211%. ([Khattab tweet](https://x.com/lateinteraction/status/1930268106213216734), [github.com/lightonai/fast-plaid](https://github.com/lightonai/fast-plaid))

Fusion : **Reciprocal Rank Fusion (RRF) à k=60** comme défaut (paper [Cormack et al. SIGIR 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf), défaut OpenSearch / Elasticsearch / Azure AI Search / MongoDB Atlas / Weaviate). Petits corpus : k=10. Avec 50+ queries labellisées : combinaison convexe avec alpha tuné. Toujours reranker après fusion.

## Contextual Embeddings (Anthropic)

Préfixe LLM-généré par chunk avant embedding. Impact cumulatif :
- Contextual Embeddings seuls : -35% échecs
- + Contextual BM25 : -49%
- + Reranking : **-67%**

Coût ingestion : une fois par document via prompt caching.

## Quand utiliser quoi

| Besoin | Choix |
|--------|-------|
| Défaut API, bon rapport qualité/prix | Jina v3 ($0.02/M) |
| Meilleur score absolu (API) | Voyage AI voyage-3-large |
| Multimodal text+image (API) | Cohere embed-v4 |
| Open-source, self-hosted | Qwen3-Embedding-8B ou BGE-M3 |
| Budget minimal | Nomic Embed v1.5 (137M) |
| Domain-specific | Fine-tune sur base Voyage/Jina |

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[rag-chunking]] — Impact chunking sur embeddings
- [[rag-reranking]] — Reranking post-retrieval
- [[rag-vector-databases]] — Stockage des vecteurs
- [[Nils Reimers]] — Sentence-BERT, sentence-transformers
- [[Omar Khattab]] — ColBERT
- [[Han Xiao]] — Jina AI embeddings
