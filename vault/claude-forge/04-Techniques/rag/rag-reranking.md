---
titre: "RAG Reranking — Modèles et hybrid search"
resume: "Reranking cross-encoder 2026, hybrid search (BM25+dense), fusion RRF, benchmarks latence et coût"
aliases:
  - RAG reranking
  - reranking models
  - cross-encoder
  - hybrid search
  - recherche hybride
  - reciprocal rank fusion
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025"
  - "https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Le reranking est l'ajout **le plus impactant** après hybrid search. Études Databricks/Pinecone : jusqu'à **+48% qualité retrieval** (hybrid+rerank vs single-method). ZeroEntropy zerank-1 : **+28% NDCG@10**.

## Leaderboard ELO 2026

Évaluation pairwise GPT-5 ([leaderboard Agentset/ZeroEntropy](https://agentset.ai/rerankers)) :

1. **ZeroEntropy Zerank 2** — 1638 ELO
2. **Cohere Rerank v4.0 Pro** — 1629 ELO
3. zerank-1 — 1573 ELO
4. Voyage AI 2.5 — 1544 ELO
5. Cohere Rerank v4.0 Fast — 1510 ELO
6. Cohere Rerank v3.5 — 1451 ELO

NB : leaderboard pairwise GPT-5, non un standard neutre.

## Modèles disponibles (panorama)

**API managées** :
- **Cohere Rerank v3.5/v4** : 100+ langues, JSON semi-structuré, auto-chunking 4096 tokens
- **ZeroEntropy Zerank 2** : meilleur ELO actuel
- **Jina Reranker v3** : top-tier latence sub-200ms, multilingue
- **Voyage AI rerank-2.5**

**Self-hosted** :
- **BGE-reranker-large v2 / base v2** ([BAAI/HuggingFace](https://huggingface.co/BAAI)) : open-source, multilingue
- **FlashRank** : viable CPU-only pour latence critique

Latences et tarifs varient fortement selon provider et infrastructure self-hosted — benchmarker sur son propre traffic plutôt que se fier à des tableaux comparatifs (chiffres souvent non traçables en source primaire).

## Hybrid Search

Dense seul : 78% recall@10. BM25 seul : 65%. **Hybrid : 91% recall@10.**

Pure vector search rate 30-50% des queries keyword-specific (codes erreur, noms produits, IDs).

### Stratégie de fusion

**Reciprocal Rank Fusion (RRF)** à k=60 = défaut zero-config. Pondération typique : 60% semantic / 40% keyword.

- Petits corpus (<100 docs) : k=10
- 50+ queries labellisées : combinaison convexe avec alpha tuné
- Toujours reranker après fusion

### Pipeline recommandé

```
Query → Hybrid Search (BM25 + Dense, top-50) → RRF fusion → Reranker (top-5) → LLM
```

Amélioration : **+15-30% sur métriques RAGAS**.

## Contextual Retrieval (Anthropic)

Contexte LLM prepended à chaque chunk à l'indexation ([anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval), verbatim) :

- Contextual Embeddings seuls : **-35%** échecs retrieval (5.7% → 3.7%)
- + Contextual BM25 : **-49%** (5.7% → 2.9%)
- + Reranking : **-67%** (5.7% → 1.9%)
- Coût ingestion : **$1.02 par million de tokens** avec prompt caching (réduction *"up to 90%"* via caching)

## Quand utiliser

| Situation | Stratégie |
|-----------|-----------|
| Tout RAG production | Hybrid search minimum |
| Budget API | Cohere Rerank v3.5/v4 |
| Self-hosted, multilingue | Jina v3 ou BGE-reranker-large |
| CPU only, latence critique | FlashRank |
| Meilleur score absolu | ZeroEntropy Zerank 2 |

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[rag-embeddings]] — Dense vs sparse
- [[rag-vector-databases]] — Support hybrid natif
- [[Nils Reimers]] — BEIR benchmark
- [[Omar Khattab]] — ColBERT late interaction
