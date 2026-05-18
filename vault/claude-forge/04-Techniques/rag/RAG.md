---
titre: "RAG — Retrieval-Augmented Generation"
resume: "Index principal (MOC) de toutes les notes RAG : chunking, embeddings, architecture, évaluation, production, experts"
aliases:
  - RAG
  - Retrieval-Augmented Generation
  - retrieval augmented generation
  - génération augmentée par récupération
  - RAG pipeline
  - RAG system
domaine: ia
type: index
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://arxiv.org/abs/2005.11401"
  - "https://www.anthropic.com/news/contextual-retrieval"
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Vue d'ensemble

Le RAG (Retrieval-Augmented Generation) combine la recherche d'information dans une base de connaissances avec la génération par LLM. Inventé en 2020 par [[Patrick Lewis]] et [[Douwe Kiela]] (Meta/UCL/NYU), c'est l'architecture IA la plus déployée en 2026. Marché projeté à $11B en 2030.

**Stat clé** : quand le RAG échoue, le problème vient de la **retrieval 73% du temps**, pas de la génération.

## Taxonomie

- **Naive RAG** — pipeline linéaire retrieve-read, ~65% de pertinence
- **Advanced RAG** — pré/post-retrieval (query expansion, reranking), 85-90%
- **Modular RAG** — modules composables et indépendants
- **Agentic RAG** — systèmes itératifs et auto-correctifs (Self-RAG, CRAG)

## Notes techniques

### Pipeline d'ingestion
- [[rag-chunking]] — Stratégies de découpage (recursive, semantic, late, contextual, AST)
- [[rag-embeddings]] — Modèles d'embedding 2026, fine-tuning, Matryoshka, quantization
- [[rag-metadata]] — Métadonnées, preprocessing, parsing, indexation

### Retrieval et génération
- [[rag-architecture]] — Patterns avancés (GraphRAG, RAPTOR, Self-RAG, CRAG, Agentic)
- [[rag-reranking]] — Modèles de reranking, hybrid search, fusion
- [[rag-vector-databases]] — Comparatif vector DBs 2026
- [[tool-retrieval-query-expansion]] — Query expansion/rewriting pour tool selection (Re-Invoke, OATS, TOOLQP)

### Production
- [[rag-evaluation]] — RAGAS, métriques, testing
- [[rag-production]] — Pipelines prod, monitoring, coûts, caching

## Experts et leaders

### Fondateurs et pionniers
- [[Douwe Kiela]] — co-auteur du paper RAG original, CEO Contextual AI
- [[Omar Khattab]] — ColBERT, DSPy, MIT
- [[Nils Reimers]] — Sentence-BERT, BEIR, VP Search Cohere

### Frameworks et outils
- [[Jerry Liu]] — fondateur LlamaIndex
- [[Harrison Chase]] — fondateur LangChain
- [[Han Xiao]] — fondateur Jina AI, late chunking
- [[Greg Kamradt]] — ChunkViz, 5 Levels of Text Splitting

### Production et éducation
- [[Jonas Roman]] — IA en prod, RAG pragmatique (FR)
- [[Chip Huyen]] — AI Engineering (O'Reilly), ML systems
- [[James Briggs]] — Aurelio AI, ex-Pinecone, tutoriels RAG

## Décision rapide (2026)

| Besoin | Pattern |
|--------|---------|
| Prototype | Naive RAG |
| Production | Advanced RAG (hybrid + reranking + contextual) |
| Multi-hop complexe | GraphRAG ou RAPTOR |
| Auto-correctif | Agentic RAG (CRAG + Self-RAG via LangGraph) |
| Petit corpus (<200K tokens) | Long context + prompt caching |
| Grand corpus dynamique | RAG + semantic caching |
| Comportement cohérent | Fine-tuning (complément au RAG) |

## Papers fondamentaux

1. Lewis et al. (2020) — [RAG original](https://arxiv.org/abs/2005.11401)
2. Khattab & Zaharia (2020) — [ColBERT](https://arxiv.org/abs/2004.12832)
3. Reimers & Gurevych (2019) — Sentence-BERT (EMNLP)
4. Asai et al. (2023) — Self-RAG
5. Yan et al. (2024) — CRAG
6. Anthropic (2024) — [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
7. Jina AI (2024) — [Late Chunking](https://arxiv.org/pdf/2409.04701)
8. Microsoft (2024) — GraphRAG + LazyGraphRAG

## Liens

- [[MOC-Techniques]]
- [[agentic-engineering-karpathy]] — Karpathy utilise Obsidian comme alternative au RAG
- [[sqlite-fts5-vault]] — Technique FTS5 utilisée dans notre MCP vault
- [[mcp-obsidian-brain-v2]] — Notre implémentation MCP de recherche vault
