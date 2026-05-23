---
titre: "Jerry Liu"
resume: "Co-fondateur et CEO LlamaIndex, framework leader pour applications LLM avec data privée — RAG, agents, structured extraction"
aliases:
  - Jerry Liu
  - LlamaIndex
  - LlamaIndex founder
  - GPT Index
  - jerry liu llamaindex
  - llamaindex CEO
role: "Co-fondateur & CEO LlamaIndex"
affiliation: "LlamaIndex (anciennement GPT Index)"
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.llamaindex.ai"
  - "https://twitter.com/jerryjliu0"
tags:
  - "#type/leader"
  - "#domaine/ia"
  - "#domaine/rag"
type: leader
---

## Profil

Co-fondateur et CEO de **LlamaIndex** (anciennement GPT Index, lancé fin 2022). LlamaIndex est devenu l'un des deux frameworks dominants pour les applications LLM avec données privées (avec [[Harrison Chase|LangChain]]), particulièrement positionné sur le **RAG** et la **structured extraction**.

Background : ML/data engineer (Uber ATG sur véhicules autonomes, Quora ML, Robust Intelligence). MS Stanford. A pivoté vers LLM-applications fin 2022 quand il a réalisé que ChatGPT débloquait une nouvelle catégorie de produits.

## Contributions clés

### LlamaIndex framework
- **Data Loaders** : 300+ connecteurs vers sources externes
- **Indices** : VectorStore, Summary, Tree, Keyword, Knowledge Graph
- **Query Engines** : retrieval + génération, sub-question, router
- **Composite Retrieval APIs** : `auto_routed` mode, routing multi-index
- **LlamaIndex Workflows** (2024) : orchestration agentic complexe
- **LlamaParse** : parsing PDF/documents avancé (10K crédits free/mois)

### Vision agentic RAG
Jerry Liu défend depuis 2024 la vision où le RAG évolue vers des **systèmes agentic** : query planning, multi-step retrieval, self-correction, tools. LlamaIndex est explicitement architecturé pour cette transition (vs LangChain qui démarre côté agents/chains).

### Talks et éducation
Conférences fréquentes (AI Engineer Summit, Ray Summit, etc.), threads techniques X très suivis, podcasts dédiés. Pédagogie technique reconnue.

## Tooling LlamaIndex pour RAG

- **VectorStoreIndex** — index vector standard
- **SubQuestionQueryEngine** — décomposition multi-hop
- **RouterQueryEngine** — routing classifieur entre indices
- **AutoMergingRetriever** — parent-child hierarchical
- **SentenceWindowRetriever** — fenêtre contextuelle
- **LlamaParse** — parsing PDF tables/layouts

## Liens

- [[MOC-Leaders]]
- Site : [llamaindex.ai](https://www.llamaindex.ai)
- X : [@jerryjliu0](https://twitter.com/jerryjliu0)
- [[RAG]] — [[rag-architecture]] — [[rag-metadata]]
- [[Harrison Chase]] — co-leader frameworks RAG (LangChain)
