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
derniere-maj: 2026-05-08
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

Le reranking est l'ajout **le plus impactant** après hybrid search. Databricks : jusqu'à **+48% qualité retrieval**. ZeroEntropy : +28% NDCG@10.

## Leaderboard 2026 (ELO)

1. ZeroEntropy Zerank 2 — **1638 ELO**
2. Cohere Rerank v4.0 Pro — **1629 ELO**

## Benchmarks pratiques

| Modèle | nDCG@10 | Latence p95 | ~$/1K queries |
|--------|---------|-------------|---------------|
| Cohere Rerank v3.5 | 0.735 | 210ms | $2.40 |
| BGE-reranker-large v2 | 0.715 | 145ms | ~$0.35 (self-hosted) |
| Jina Reranker v3 | 81.33% Hit@1 | 188ms | ~$0.30 (self-hosted) |
| BGE-reranker-base v2 | 0.699 | 92ms | ~$0.18 (self-hosted) |
| FlashRank (CPU) | lower | 55ms | ~$0.08 (self-hosted) |

**Jina v3** = seul top-tier sous 200ms. **FlashRank** = viable pour CPU-only latency-critical. Cohere v3.5 = 100+ langues, JSON semi-structuré, auto-chunking 4096 tokens.

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

Contexte LLM prepended à chaque chunk à l'indexation. -49% échecs retrieval (hybrid + contextual). Avec reranking : **-67%**. Coût contextualisation 50K chunks : $12 avec caching vs $94 sans (87% réduction).

## Quand utiliser

| Situation | Stratégie |
|-----------|-----------|
| Tout RAG production | Hybrid search minimum |
| Budget API | Cohere Rerank v3.5/v4 |
| Self-hosted, multilingue | Jina v3 ou BGE-reranker-large |
| CPU only, latence critique | FlashRank |
| Meilleur score absolu | ZeroEntropy Zerank 2 |

## Liens

- [[RAG]] — Index principal
- [[rag-embeddings]] — Dense vs sparse
- [[rag-vector-databases]] — Support hybrid natif
- [[Nils Reimers]] — BEIR benchmark
- [[Omar Khattab]] — ColBERT late interaction
