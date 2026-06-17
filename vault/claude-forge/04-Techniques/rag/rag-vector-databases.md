---
titre: "RAG Vector Databases — Comparatif 2026"
resume: "Comparatif vector DBs 2026 : Pinecone, Qdrant, Weaviate, Milvus, Chroma, pgvector, Vespa — benchmarks et cas d'usage"
aliases:
  - vector databases
  - bases de données vectorielles
  - vector DB
  - vector store
  - RAG vector databases
  - Pinecone vs Qdrant
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://www.datacamp.com/blog/the-top-5-vector-databases"
  - "https://www.firecrawl.dev/blog/best-vector-databases"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Le choix de la vector DB dépend de l'échelle, du budget, de l'écosystème existant, et du besoin en hybrid search.

## Comparatif 2026

| Base | Spécialité | Stat clé 2026 |
|------|-----------|---------------|
| **Pinecone** | Managed cloud, zero ops | Serverless (storage/compute découplés), pricing RU/WU, Inference + Assistant intégrés. Détail → [[pinecone-vector-database]] |
| **Qdrant** | Speed-critical, open-source | **p99 ~12ms à 10M vecteurs** (vs Weaviate 16ms, Milvus 18ms) |
| **Weaviate** | Hybrid search, GraphQL | Meilleur vector+BM25+metadata natif |
| **Milvus** | Billion-scale, GPU | Production au-dessus de 1B vecteurs |
| **Chroma** | Prototyping, local dev | Limité au-delà de 100M vecteurs |
| **pgvector** | Équipes Postgres, <50M | Production-grade 2026 (Supabase, Neon, Instacart) |
| **Vespa** | Large-scale hybrid search | Co-leader avec Milvus au-dessus de 1B |

> [!note] Mise à jour Pinecone (juin 2026)
> Le « metadata filtering limitée » des comparatifs antérieurs est **largement périmé** depuis l'archi serverless : métadonnées plates jusqu'à 40 KB/record, opérateurs `$eq/$in/$and/$or`…, hybrid sparse-dense, + Pinecone Inference (embeddings/rerank hébergés) et Pinecone Assistant (RAG managé). Voir la note dédiée [[pinecone-vector-database]].

## Tiers d'échelle

| Échelle | Options |
|---------|---------|
| < 10M vecteurs | Tous fonctionnent |
| 10M - 1B | Pinecone (managed), Qdrant/Weaviate/Milvus (self-hosted) |
| > 1B | Vespa et Milvus distribué |

## Insight critique

**Pure vector search < hybrid search** sur la plupart des workloads production. Les agents ont besoin d'exact-match pour noms propres, numéros de version, IDs + semantic matching.

Hybrid search natif : Weaviate, Vespa, Qdrant, **Milvus 2.6** (dense+sparse même collection, single API).

**pgvector** = défaut recommandé si Postgres existant. Bornes techniques : vanilla pgvector < 10-20M vecteurs, pgvectorscale (Timescale) < 50M+. Usage prod confirmé : Instacart (migration FAISS+Elasticsearch → pgvector, 14M utilisateurs/jour, [blog Instacart 2025](https://tech.instacart.com/how-instacart-built-a-modern-search-infrastructure-on-postgres-c528fa601d54)), Supabase, Neon. Nécessite composition manuelle pour hybrid.

## Quand utiliser quoi

| Besoin | Choix |
|--------|-------|
| Zero ops, startup | Pinecone |
| Performance brute, self-hosted | Qdrant |
| Hybrid search natif complet | Weaviate ou Milvus 2.6 |
| Déjà sur Postgres, < 50M | pgvector |
| Prototype rapide | Chroma |
| Scale > 1B | Milvus distribué ou Vespa |

> **À noter** : [[onyx-enterprise-search|Onyx]] (RAG entreprise open-source) utilise **OpenSearch** comme index hybride depuis sa v4.0 (mai 2026, ex-Vespa) ; [[memoire-agent-mem0|mem0]] supporte Qdrant (défaut), pgvector, Pinecone… comme backends.

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[pinecone-vector-database]] — Pinecone en profondeur (serverless, RU/WU, Inference, Assistant)
- [[onyx-enterprise-search]] — plateforme RAG entreprise (index OpenSearch)
- [[rag-embeddings]] — Modèles à stocker
- [[rag-reranking]] — Post-retrieval reranking
- [[rag-metadata]] — Metadata filtering
- [[sqlite-fts5-vault]] — Notre approche FTS5 pour le vault
