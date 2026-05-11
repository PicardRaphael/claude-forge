---
titre: "NeoDoc Research Agent — LangGraph RAG Pipeline 5 Nœuds"
resume: "Agent RAG LangGraph : decompose (google-genai natif, JSON structuré) → retrieve (Vertex AI grounding parallèle) / full_doc_retrieve (broad questions) → generate (Gemini Pro streaming) → respond (citations JSONB), renumbering citations cross-queries"
aliases:
  - "neodoc research agent"
  - "research agent neodoc"
  - "neodoc rag pipeline"
  - "neodoc graph"
  - "query decomposition neodoc"
  - "neodoc grounding"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#type/technique"
  - "#projet/neo-ia"
  - "#domaine/rag"
---

## Concept

L'agent Research est le cœur de NeoDoc. C'est un pipeline LangGraph `StateGraph` de 5 nœuds qui décompose les questions complexes, recherche dans Vertex AI Discovery Engine avec grounding, et synthétise une réponse avec citations tracées.

## Graph

```
START
  │
  ▼
decompose ──→ [routing conditionnel]
  │                    │
  │ is_broad=False     │ is_broad=True
  ▼                    ▼
retrieve         full_doc_retrieve
  │                    │
  └───────┬────────────┘
          ▼
       generate
          │
          ▼
       respond
          │
          ▼
         END
```

## Les 5 Nœuds

### 1. decompose_node — Décomposition de question

**SDK** : google-genai natif (PAS LangChain) avec `response_mime_type="application/json"` et schema Pydantic.

```python
class _QueryDecomposition(BaseModel):
    sub_queries: list[str]     # Sous-questions (max NEODOC_MAX_SUB_QUERIES)
    is_broad_question: bool    # True = charger tous les chunks
    reasoning: str             # Explication du choix
```

**Prompt** : `DECOMPOSE_PROMPT` avec 6 exemples few-shot couvrant :
- Question simple → 1 sous-question, `is_broad=False`
- Question complexe → N sous-questions, `is_broad=False`
- Question large ("résume tout") → `is_broad=True`

**LLM** : `NEODOC_FAST_MODEL` (Gemini 2.5 Flash), temperature=0.

### 2. retrieve_node — Recherche grounding parallèle

Pour chaque sous-question, exécute `search_with_grounding()` **en parallèle** via `asyncio.gather()`.

**Vertex AI Discovery Engine** (v1alpha) :
- Filtre multi-tenant : `(acteur_id: ANY("X") OR shared = "true") AND customer_id: ANY("Y")`
- Filtre sélection : `document_id: ANY("id1", "id2", ...)` (docs sélectionnés par l'acteur)
- `summary_spec` avec `include_citations=True`, preamble FR, `summary_result_count=15`
- Retourne `GroundedSearchResult` : summary avec markers `[N]`, references, raw_results

**Merge cross-queries** :
- Déduplique les chunks par `document_id`
- `_renumber_markers()` : décale les `[N]` de chaque sous-query pour éviter les collisions

### 3. full_doc_retrieve_node — Chargement complet (broad questions)

Quand `is_broad_question=True`, bypass le grounding :
- Charge **tous les chunks** des documents sélectionnés via `ChunkServiceClient.list_chunks()`
- Exécution parallèle (`asyncio.gather`) par document
- Limite : `NEODOC_MAX_FULL_DOC_CHARS` (500K caractères)
- Set `grounding_skipped=True` → change le prompt de generation

### 4. generate_node — Synthèse LLM

**LLM** : `NEODOC_DEFAULT_MODEL` (Gemini 2.5 Flash) via LangChain `get_llm().astream()`.

Deux paths selon le mode de retrieval :

| Mode | Template | Contenu |
|------|----------|---------|
| Grounding | `<grounded_answer>` + `<grounding_references>` | Summary avec `[N]` préservés |
| Full doc | `<documents>` avec chunks | Contenu brut, pas de markers pré-existants |

Si `len(sub_queries) > 1` → injection de `SYNTHESIS_INSTRUCTION` (synthèse thématique, pas de duplication).

**Streaming** : via `astream()`, les tokens arrivent en SSE au frontend.

### 5. respond_node — Résolution citations + persistance

**Résolution citations** (`_resolve_references_to_citations()`) :
1. Extrait `vertex_id` depuis le resource path Vertex AI
2. Lookup PostgreSQL : `DocumentRepository.get_by_vertex_id(vertex_id, client_id)`
3. Résultat : `{marker: "[1]", doc_id: UUID, title: "...", snippet: "..."}`
4. Fallback : `vertex_id` ou `uri` si lookup BDD échoue

**Persistance** :
- Insert message utilisateur + message assistant dans `t_neodoc_message`
- Citations stockées en JSONB sur le message assistant

## ResearchState — 13+ champs

```python
class ResearchState(TypedDict):
    question: str
    customer_id: str
    workspace_id: str
    acteur_id: str
    selected_vertex_ids: list[str]    # docs sélectionnés
    history: list                      # messages précédents

    sub_queries: list[str]             # output decompose
    is_broad_question: bool            # routing flag
    retrieved_chunks: list[dict]       # output retrieve
    grounded_summary: str              # summary avec [N]
    grounding_references: list[dict]   # refs Vertex AI
    grounding_skipped: bool            # True si full_doc path

    response: str                      # output generate
    citations: list[dict]              # output respond (résolues)
    model: str                         # modèle utilisé
    decompose_input_tokens: int        # usage tracking
    decompose_output_tokens: int
```

## Prompts clés

| Prompt | Fichier | Rôle |
|--------|---------|------|
| `RESEARCH_SYSTEM_PROMPT` | `research_system.py` | Identité NeoDoc, core RAG rules, citation format, no-answer protocol |
| `DECOMPOSE_PROMPT` | `research_system.py` | Few-shot query decomposition (6 exemples) |
| `SYNTHESIS_INSTRUCTION` | `research_system.py` | Injecté si multi-query : synthèse thématique |
| `RAG_RULES` | `research_system.py` | 5 règles strictes (source exclusivity, fidelity, traceability, uncertainty, scope) |
| `NOTE_SYSTEM_PROMPT` | `note_system.py` | Format notes |
| `TITLE_GENERATION_PROMPT` | `note_system.py` | Auto-titre ≤80 chars via Gemini Flash |

## Vertex AI Discovery Engine — Détails techniques

**3 clients** (lazy-init) :
- `SearchServiceClient` (v1alpha) — search + grounding
- `DocumentServiceClient` (v1) — import + delete + index status
- `ChunkServiceClient` (v1alpha) — list_chunks (full-doc retrieve)

**Cache in-memory** : TTL=120s, max 50 entrées, LRU eviction.

**Grounding** : `summary_spec.include_citations=True` + `summary_spec.summary_result_count=15` + preamble FR.

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `agents/research/graph.py` | StateGraph assembly + checkpointer |
| `agents/research/nodes.py` | 5 nœuds async |
| `agents/research/state.py` | ResearchState TypedDict |
| `agents/prompts/research_system.py` | Tous les prompts RAG |
| `agents/prompts/note_system.py` | Prompts notes |
| `services/search_service.py` | Vertex AI Discovery Engine wrapper |
| `services/chat_service.py` | Orchestration graph + SSE streaming |

## Liens

- [[neodoc-architecture]]
- [[neodoc-ingestion-pipeline]]
- [[neochat-react-engine]]
