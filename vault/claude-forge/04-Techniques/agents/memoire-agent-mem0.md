---
titre: "mem0 — Couche mémoire long-terme pour agents IA"
resume: "mem0 (mem0ai/mem0, Apache 2.0) extrait/consolide/récupère les faits saillants des conversations cross-session ; v3 avril 2026 a retiré le graph store externe de l'OSS au profit d'un entity-linking spaCy natif."
aliases:
  - "mem0"
  - "mem-zero"
  - "mem0ai"
  - "mem0 memory"
  - "mémoire agent mem0"
  - "memory-as-a-service"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://github.com/mem0ai/mem0"
  - "https://docs.mem0.ai/components/vectordbs/overview"
  - "https://github.com/mem0ai/mem0-mcp"
  - "https://arxiv.org/abs/2504.19413"
  - "https://mem0.ai/blog/state-of-ai-agent-memory-2026"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Description

**mem0** (« mem-zero », repo `mem0ai/mem0`, Apache 2.0) = couche de mémoire long-terme universelle pour agents IA / LLM. Sans mémoire persistante, chaque session repart à froid. mem0 **extrait, consolide, stocke et récupère les faits saillants** des conversations à travers les sessions, sans rejouer tout l'historique (économie tokens + latence).

Deux offres :
- **OSS self-host** (Apache 2.0) : `pip install mem0ai` / `npm install mem0ai`. Modes library / self-hosted server (Docker, dashboard, HTTP).
- **Mem0 Platform** (managed, `app.mem0.ai`) : zero-ops, conserve des features retirées de l'OSS (**graph memory**, time-based decay), compliance SOC 2 + HIPAA (rapporté).

> [!warning] Point de datation critique (vérifié source primaire, juin 2026)
> mem0 a été **réécrit en avril 2026 (« v3 », nouvel algorithme)**. La majorité des tutoriels 2026 décrivent encore l'ancienne archi (graph store Neo4j optionnel) et des chiffres ⭐ périmés (« 41k »/« 48k » vs **58.7k réels**). Toute lecture doit dater l'état et distinguer **OSS (plus de graphe traversable) vs Platform (graphe conservé)**.

## Comment ça marche (technique)

**Pipeline 3 phases** (papier arXiv 2504.19413) : **Extraction** (faits + entités tirés des messages) → **Update/Consolidation** (fusion avec l'existant, résolution de conflits — *self-editing* : corriger une préférence met à jour l'enregistrement au lieu de dupliquer) → **Retrieval** (récupération ciblée injectée dans le prompt).

**Algorithme v3 (avril 2026)** — extraction ADD-only en une passe (1 appel LLM, rien écrasé) · faits agent au même poids que faits user · **entity linking** (entités embeddées + cross-liées) · récupération **multi-signaux** (sémantique + BM25 + entity matching fusionnés en un score) · raisonnement **temporel** (ranking time-aware).

**Scopes d'identité** (composables au retrieval) : `user_id` (cross-session), `agent_id`, `run_id`/`session_id` (une conversation), `app_id`/`org_id`. Catégories : épisodique / sémantique / procédurale.

**Stockage** : vector store + key-value (+ graph historiquement).
- Vector stores (Python) : **Qdrant (défaut)**, pgvector, Pinecone, Chroma, Milvus, Weaviate, Redis, Elasticsearch, MongoDB, Supabase, FAISS, etc. TS : Qdrant/Redis/Valkey/Vectorize/in-memory. Dim défaut 1536.
- **Graph memory — changement majeur v3** : l'ancien `graph_store` externe (Neo4j, Memgraph, Kuzu, Neptune) + flag `enable_graph` **retiré de l'OSS**. Remplacé par **entity linking natif** (entités extraites via **spaCy**, pas LLM, stockées dans `{collection}_entities`, utilisées pour booster le ranking). Ce n'est **plus une interface graphe traversable** (champ `relations` supprimé). Raison : la variante graphe `Mem0g` ne battait `Mem0` que de ~2 % mais tournait ~3× plus lent et coûtait ~2× les tokens. **La Platform managed conserve le graphe.**

**LLM/embedder** : LLM défaut `gpt-5-mini`, embedder `text-embedding-3-small`. Pipeline LLM-agnostique.

**API cœur** :
```python
from mem0 import Memory
memory = Memory()
memory.add(messages, user_id="alice")                              # store (= appels LLM)
memory.search(query="...", filters={"user_id": "alice"}, top_k=3)  # retrieve
memory.get_all(...)  # + update / delete
```
SDK Python + TS (Node v3.0.8 le 13 juin 2026). **MCP server** (`mem0ai/mem0-mcp`) wrappe l'API Platform : `add_memory`, `search_memories`, `get_memories`, `update_memory`, `delete_memory`… (clé `MEM0_API_KEY` requise, `MEM0_ENABLE_GRAPH_DEFAULT=false` par défaut). Intégrations : LangGraph, CrewAI, OpenAI, Agent Skills (Claude Code, Codex, Cursor, Windsurf).

## Quand utiliser

| Idéal | Overkill / inadapté |
|---|---|
| Chatbots/assistants persistants | Conversations sans état / one-shot |
| Agents multi-users avec isolation (`user_id`) | Quand un simple historique en base suffit |
| Personnalisation long-terme, support client | Latence/coût ultra-sensibles (chaque `add()` = appels LLM) |
| Réduire les coûts tokens (retrieval ciblé vs full-context) | **Besoin d'un vrai graphe traversable** → OSS v3 ne le fait plus (préférer Zep/Graphiti, ou Platform mem0) |

## Optimisation

- **LLM extracteur** : `gpt-5-mini` (défaut) = bon compromis coût/qualité ; modèle plus fort = meilleure extraction mais plus cher par `add()`.
- **Écritures async** par défaut : ne pas bloquer la génération de réponse sur l'écriture mémoire.
- **Scoping** : `user_id`/`agent_id`/`run_id` + metadata filtering pour requêtes multi-tenant.
- **Reranking** (Cohere, HF) en 2e passe avant injection.
- **v3** : l'entity linking est inclus gratuitement — ne plus chercher à activer un graph store externe en OSS.
- **Coûts** : ~7k tokens/requête au retrieval (vs ~26k full-context). Batcher les `add`.
- **Pièges** : staleness (faits très retrouvés devenus faux), résolution d'identité cross-device, migration v2→v3 si code dépendait de `relations`/`enable_graph`.

## Maturité (source primaire GitHub, juin 2026)

- **⭐ 58.7k**, 6.8k forks, 340 releases. Node SDK v3.0.8 (13 juin 2026). Apache 2.0.
- **Financement** : $24M Series A (oct. 2025), Y Combinator + Peak XV (rapporté).
- **Papier** : *Mem0: Building Production-Ready AI Agents…* arXiv:2504.19413 (avril 2025, ECAI 2025). LOCOMO : +26 % vs OpenAI Memory, latence p95 −91 %, tokens −90 % vs full-context.
- **Benchmarks v3 (avril 2026, source mem0, à recouper)** : LoCoMo 91.6 (vs 71.4), LongMemEval ~94.8 (vs 67.8).

## Liens

- [[memoire-agent-langmem]] — alternative LangChain-native (mémoire procédurale, lock-in LangGraph)
- [[agents-architecture]] — modèle mémoire short/long/episodic/procedural
- [[rag-vector-databases]] — backends vector de mem0 (Qdrant défaut, pgvector, Pinecone…)
- [[stack-python-ia]] — tableau Memory frameworks
- [[MOC-Techniques]]
