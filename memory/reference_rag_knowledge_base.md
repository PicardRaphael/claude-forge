---
name: rag-knowledge-base
description: Vault forge-brain contient un dossier RAG complet (7 notes techniques + 10 leaders + 2 synthèses) créé le 2026-05-08 — interroger avant toute question RAG
type: reference
originSessionId: e2998299-6d67-4a1c-bb82-77a11d94ae66
---
Le vault forge-brain contient une base de connaissances RAG complète dans `04-Techniques/rag/` :

**Notes techniques** (7) :
- `RAG.md` — MOC principal, taxonomie, décisions, papers
- `rag-chunking.md` — recursive, semantic, late, contextual, AST + benchmarks
- `rag-embeddings.md` — top modèles 2026, fine-tuning, Matryoshka, quantization
- `rag-architecture.md` — GraphRAG, RAPTOR, Self-RAG, CRAG, Agentic RAG
- `rag-metadata.md` — preprocessing, parsing, indexation, monitoring
- `rag-reranking.md` — cross-encoders, hybrid search, fusion RRF
- `rag-vector-databases.md` — Pinecone, Qdrant, Weaviate, pgvector comparatif

**Leaders RAG** (10 fiches dans `05-Leaders/`) :
Jonas Roman, Omar Khattab, Douwe Kiela, Jerry Liu, Harrison Chase, Han Xiao, Chip Huyen, Greg Kamradt, Nils Reimers, James Briggs

**Synthèses** (2) :
- `rag-obsidian-claude-video-analyse.md` — analyse vidéo YouTube RAG+Obsidian vs state-of-the-art
- `outils-portabilite-forge.md` — liste outils à installer sur nouveau PC (defuddle, yt-dlp)

**cc-news** mis à jour avec section RAG & Embeddings leaders (9 sources à monitorer).

**Notes techniques Agents IA** (6 dans `04-Techniques/agents/`) :
- `Agents IA.md` — MOC principal, taxonomie, benchmarks, papers
- `agents-frameworks.md` — LangGraph, CrewAI, Claude SDK, OpenAI SDK, Google ADK, no-code
- `agents-architecture.md` — ReAct, multi-agent, memory, MCP, A2A, LATS, context engineering
- `agents-automation.md` — workflows, CI/CD, scheduling, Computer Use, browser agents, coûts
- `agents-evaluation.md` — SWE-bench, GAIA, WebArena, TAU-bench, testing, deploy
- `agents-securite.md` — OWASP agentic, sandboxing, dual-LLM, permissions

**Leaders Agents** (6 fiches dans `05-Leaders/`) :
Shunyu Yao, Andrew Ng, Lilian Weng, Jim Fan, Simon Willison, Ethan Mollick

**Synthèse innovation** : `techniques-inedites.md` — 8 combinaisons RAG × Agents inédites

**Comment utiliser** : toute question RAG/Agents → chercher dans le vault d'abord via CLI Obsidian, puis compléter par recherche web si info > 7 jours.
