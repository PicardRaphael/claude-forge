---
titre: "NeoDoc Architecture — Vue d'ensemble"
resume: "App RAG documentaire B2B : ingestion Google Drive/upload → GCS → Vertex AI Discovery Engine, agent Research LangGraph 5 nœuds (decompose → retrieve → generate → respond), query decomposition, grounding citations, workspaces multi-tenant, notes indexables"
aliases:
  - "neodoc architecture"
  - "architecture neodoc"
  - "neodoc overview"
  - "neodoc archi"
  - "neodoc rag"
  - "vertex ai search neodoc"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#projet/neo_ia"
  - "#domaine/rag"
  - "#domaine/agents"
  - "#domaine/ia"
---

## Vue d'ensemble

NeoDoc est l'app RAG documentaire du monorepo [[neo_ia]]. Contrairement à [[neochat-architecture]] (ReAct + tools) et [[neomail-architecture]] (webhook + classification), NeoDoc est un **système RAG pur** construit sur Vertex AI Discovery Engine pour l'indexation/recherche et un agent LangGraph pour la décomposition de questions et la synthèse.

**Stack spécifique** : google-cloud-discoveryengine (v1alpha), google-genai (SDK natif, pas LangChain pour decompose), GCS, Google Drive API.

## Architecture en couches

```
┌──────────────────────────────────────────────────┐
│  API FastAPI (apps/neodoc/api/)                  │
│  SSE streaming, auth JWT, quota enforcement      │
├──────────────────────────────────────────────────┤
│  Research Agent (LangGraph StateGraph)           │
│  decompose → retrieve/full_doc → generate → respond │
│  → voir [[neodoc-research-agent]]                │
├──────────────────────────────────────────────────┤
│  Services métier                                 │
│  Ingestion | Search | Chat | Note | Drive | GCS  │
│  → voir [[neodoc-ingestion-pipeline]]            │
├──────────────────────────────────────────────────┤
│  Vertex AI Discovery Engine                      │
│  Indexation, chunking, grounding + citations     │
├──────────────────────────────────────────────────┤
│  Infrastructure                                  │
│  GCS (stockage), PostgreSQL (schema neodoc),     │
│  shared_utils (auth, billing, LLM, Langfuse)     │
└──────────────────────────────────────────────────┘
```

## Différences clés avec NeoChat/NeoMail

| Aspect | NeoChat/NeoMail | NeoDoc |
|--------|----------------|--------|
| Engine | Declarative ReAct Engine | LangGraph StateGraph custom |
| LLM tools | 26 tools LangChain @tool | Pas de tools — RAG pur |
| Tool selection | HybridToolSelector pgvector | Pas de sélection — pipeline fixe |
| Prompt builder | AdaptivePromptBuilderV2 4 layers | create_adaptive_builder (RAG_RULES) |
| Source de données | API NEOTEEM + Gmail | Documents utilisateur (Drive/upload) |
| Indexation | Pas d'indexation | Vertex AI Discovery Engine |
| Décomposition | Pas de décomposition | Query decomposition LLM |
| Citations | Pas de citations | Grounding citations `[N]` |
| Multi-tenant | Par user_email | Par workspace + acteur_id + customer_id |
| Notes | Non | Oui (manuelles + from-response, indexables) |

## Concepts clés

### Workspaces
Espace de travail isolé contenant des documents et des conversations. Un acteur peut avoir plusieurs workspaces. Multi-tenant via `customer_id` (= PG_DBNAME).

### Documents
Fichiers importés depuis Google Drive ou uploadés. Pipeline d'ingestion 7 étapes → stockage GCS → indexation Vertex AI Discovery Engine. Statuts : pending → downloading → uploading → imported → indexed → error.

### Sélection
Un acteur sélectionne quels documents d'un workspace sont actifs pour la recherche. Filtre appliqué dans les requêtes Vertex AI.

### Notes
Contenus créés manuellement ou sauvegardés depuis les réponses de l'agent. Indexables dans Vertex AI Discovery Engine pour être retrouvables dans les futures recherches.

### Conversations
1 conversation par (workspace, acteur). Soft reset via `conv_reset_at` (ne supprime pas les messages, mais le LangGraph thread repart à zéro).

## Schéma BDD (schema `neodoc`)

| Table | Rôle |
|-------|------|
| `t_neodoc_workspace` | Espaces de travail (customer_id, name, description) |
| `t_neodoc_document` | Documents (vertex_id, ingestion_status, source_type, gcs_path) |
| `t_neodoc_workspace_document` | N:N workspace ↔ document |
| `t_neodoc_selection` | Sélection acteur ↔ document (unique workspace+acteur+doc) |
| `t_neodoc_conversation` | 1 par workspace+acteur (reset_at pour soft reset) |
| `t_neodoc_message` | Messages avec citations JSONB |
| `t_neodoc_note` | Notes (manual/response), citations JSONB, is_indexed |
| `t_neodoc_quota` | Quotas mensuels (EUR, search calls) par client |
| `t_neodoc_usage` | Usage tokens + coût EUR par appel agent |

## API Endpoints principaux

| Catégorie | Endpoints clés |
|-----------|---------------|
| **Workspaces** | CRUD + `/documents` (list avec statut sélection) + `/selection` (bulk update) |
| **Documents** | Upload (max 5, 100MB), ingest Drive, ingest batch, ingest folder, retry, delete |
| **Chat** | POST `/chat` (SSE), POST `/chat/reset`, GET `/chat/conversations` |
| **Notes** | CRUD + POST `/from-response` (auto-titre LLM) + POST `/{id}/index` |
| **Usage** | Billing endpoints |

Quota enforced sur le chat (HTTP 429). Rate limits via SlowAPI.

## Configuration clé

| Variable | Défaut | Rôle |
|----------|--------|------|
| `NEODOC_DEFAULT_MODEL` | gemini-2.5-flash | LLM generate node |
| `NEODOC_FAST_MODEL` | gemini-2.5-flash | LLM decompose node |
| `NEODOC_MAX_SUB_QUERIES` | 5 | Max sous-questions |
| `NEODOC_MAX_FULL_DOC_CHARS` | 500 000 | Limite contexte broad questions |
| `NEODOC_SUMMARY_RESULT_COUNT` | 15 | Sources grounding |
| `VERTEX_SEARCH_DATA_STORE_ID` | — | Discovery Engine data store |
| `GCS_TEMP_BUCKET` | neodoc-temp | Bucket GCS stockage |

## Tests

- **Unit** : couverture complète (nodes, services, repos, API, streaming, billing)
- **Functional** : pipeline complet avec DeepEval faithfulness (score ≥ 0.8)
- **Integration** : repos contre PostgreSQL réel
- Target : `fail_under = 80`

## Liens

- [[neo_ia]]
- [[neodoc-research-agent]]
- [[neodoc-ingestion-pipeline]]
- [[neochat-architecture]]
