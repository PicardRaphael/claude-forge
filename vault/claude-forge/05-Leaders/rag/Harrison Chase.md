---
titre: "Harrison Chase"
resume: "Co-fondateur et CEO LangChain, framework le plus utilisé pour applications LLM — chains, agents, RAG, LangGraph pour workflows agentic, LangSmith observabilité"
aliases:
  - Harrison Chase
  - LangChain
  - LangChain founder
  - harrison chase langchain
  - LangGraph
  - LangSmith
  - langchain CEO
role: "Co-fondateur & CEO LangChain"
affiliation: "LangChain"
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.langchain.com"
  - "https://twitter.com/hwchase17"
tags:
  - "#type/leader"
  - "#domaine/ia"
  - "#domaine/rag"
  - "#domaine/agents"
type: leader
---

## Profil

Co-fondateur et CEO de **LangChain** (lancé octobre 2022, peu après ChatGPT). LangChain est devenu le framework le plus utilisé pour construire des applications LLM, particulièrement positionné sur les **chains**, les **agents** et l'orchestration.

Background : ex-ML engineer Robust Intelligence, BS Harvard. A créé LangChain comme side project qui a explosé en open-source viral fin 2022 — la communauté l'a adopté massivement.

## Contributions clés

### LangChain framework
- **Chains** : composition de prompts + LLM + parsers
- **Agents** : LLM avec accès aux tools (ReAct, OpenAI functions)
- **Retrievers** : abstraction unifiée over vector stores
- **Document Loaders** : 200+ formats
- **LCEL (LangChain Expression Language)** : composition déclarative

### LangGraph (2024) — Agentic workflows
Évolution majeure : graphe dirigé cyclique avec branching conditionnel, checkpoints, human-in-the-loop. Standard production 2026 pour systèmes agentic RAG complexes ([[rag-architecture#Agentic RAG]]).

### LangSmith — Observabilité LLM
Plateforme observabilité native LangChain : tracing, evaluation, debugging. Devenue référence pour debug pipelines RAG/agents en production. Concurrents : Arize Phoenix, Maxim AI, Langfuse.

### LangChain Hub
Marketplace de prompts versionnés, partage communautaire.

## Approche RAG

LangChain démarre **côté agents/chains** (vs [[Jerry Liu|LlamaIndex]] qui démarre côté RAG/data). Les deux convergent en 2026 vers les **systèmes agentic** mais avec philosophies différentes :
- LangChain = orchestration générale, RAG comme cas d'usage
- LlamaIndex = data ingestion/retrieval premier, agents construits dessus

## Talks et éducation

Conférences (AI Engineer World's Fair, Ray Summit), tutorials YouTube/Twitter, podcasts dédiés (Latent Space, Cognitive Revolution). Pédagogie sur les patterns LLM apps.

## Liens

- [[MOC-Leaders]]
- Site : [langchain.com](https://www.langchain.com)
- X : [@hwchase17](https://twitter.com/hwchase17)
- [[RAG]] — [[rag-architecture]] — [[rag-production]]
- [[Jerry Liu]] — co-leader frameworks RAG (LlamaIndex)
