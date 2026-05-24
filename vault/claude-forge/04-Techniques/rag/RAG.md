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
derniere-maj: 2026-05-24
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

Le RAG (Retrieval-Augmented Generation) combine la recherche d'information dans une base de connaissances avec la génération par LLM. Introduit en **mai 2020 (NeurIPS 2020)** par **12 co-auteurs** dont [[Patrick Lewis]], Ethan Perez et [[Douwe Kiela]] (Meta/FAIR, UCL, NYU), c'est l'architecture IA la plus déployée en 2026.

**Marché** : projeté à **$11.0B en 2030** (Grand View Research, depuis $1.2B en 2024, CAGR 49.1%). MarketsAndMarkets donne $9.86B — deux estimations distinctes du même horizon.

**Stat retrieval** : la retrieval est la principale source d'échec d'un système RAG (consensus communauté, statistique non universellement sourcée — éviter le chiffre "73%" qui circule sans source primaire).

## Taxonomie

- **Naive RAG** — pipeline linéaire retrieve-read
- **Advanced RAG** — pré/post-retrieval (query expansion, reranking, contextual)
- **Modular RAG** — modules composables et indépendants
- **Agentic RAG** — systèmes itératifs et auto-correctifs (Self-RAG, CRAG)

Les benchmarks (FloTorch 2026, Chroma Research, NAACL 2025 Vectara) confirment des gains significatifs d'Advanced RAG vs Naive (typiquement 25-40 points selon métrique et domaine), mais les pourcentages absolus "65% vs 85-90%" circulant entre blogs ne sont pas sourcés en source primaire.

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
- [[Jerry Liu]] — co-fondateur & CEO LlamaIndex (data + agentic retrieval)
- [[Harrison Chase]] — co-fondateur & CEO LangChain (chains, agents, LangGraph, LangSmith)
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

1. Lewis et al. (mai 2020, NeurIPS 2020) — [RAG original](https://arxiv.org/abs/2005.11401)
2. Khattab & Zaharia (2020) — [ColBERT](https://arxiv.org/abs/2004.12832)
3. Reimers & Gurevych (2019) — Sentence-BERT (EMNLP)
4. Asai et al. (oct. 2023 arXiv, ICLR 2024) — [Self-RAG](https://arxiv.org/abs/2310.11511)
5. Yan et al. (2024) — [CRAG](https://arxiv.org/abs/2401.15884)
6. Sarthi et al. (2024, Stanford) — [RAPTOR](https://arxiv.org/abs/2401.18059)
7. Anthropic (2024) — [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
8. Jina AI (2024) — [Late Chunking](https://arxiv.org/pdf/2409.04701)
9. Microsoft (2024) — [GraphRAG + LazyGraphRAG](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)

## Liens

- [[MOC-Techniques]]
- [[Andrej Karpathy]] — pattern wiki-LLM cumulatif ([[pattern-vault-llm-karpathy]]) : *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* (Gist 4 avril 2026). Karpathy contraste le **wiki cumulatif** avec la **synthèse RAG stateless** (NotebookLM, ChatGPT file uploads) — différence philosophique, pas remplacement technique.
- [[sqlite-fts5-vault]] — Technique FTS5 utilisée dans notre MCP vault
- [[mcp-obsidian-brain-v2]] — Notre implémentation MCP de recherche vault


## Synthèses

- [[rag-obsidian-claude-video-analyse]] — Analyse critique du pipeline RAG 5 phases (extraction, chunking, vectorisation, MCP, routage local) proposé dans une vidéo YouTube, comparé aux best practices 2026.
