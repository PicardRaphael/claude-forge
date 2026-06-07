---
titre: "NeoChat Tool RAG — HybridToolSelector pgvector"
resume: "Sélection dynamique de tools par hybrid search pgvector (full-text + semantic + RRF fusion), LLM query expansion, LLM reranking, domain router, dependency BFS, workflow reordering"
aliases:
  - "neochat tool rag"
  - "tool rag"
  - "HybridToolSelector"
  - "hybrid tool selector"
  - "tool selection neochat"
  - "tool selector pgvector"
  - "sélection outils neochat"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#type/technique"
  - "#projet/neo_ia"
  - "#domaine/rag"
  - "#domaine/agents"
---

## Concept

NeoChat ne hardcode PAS les tools disponibles par agent. Un **Tool RAG** sélectionne dynamiquement les tools pertinents pour chaque requête utilisateur, via recherche hybride dans une base pgvector. C'est le pattern recommandé par LangGraph pour gérer > 10 tools.

## Pipeline complet (10 étapes)

```
Query utilisateur
    │
    ▼
1. LLM Query Expansion (optionnel)
   Gemini Flash extrait mots-clés + synonymes
   Skip si query courte (<3 mots) ou contient des keywords clairs
    │
    ▼
2. Normalize Query
   Suppression accents (NFKD), lowercase, strip
    │
    ▼
3. Embed Query
   VertexAI text-embedding-004, cache TTL 1h (TTLCache maxsize=100)
    │
    ▼
4. Domain Pre-Filter (optionnel)
   CentroidDomainRouter : classifie le domaine via embedding
   Coût zéro (réutilise le query embedding de l'étape 3)
    │
    ▼
5. Hybrid Search pgvector
   Full-text (tsvector) + Semantic (cosine) + RRF fusion
   Tables : t_tool_embedding, t_tool_agent
    │
    ▼
6. LLM Reranking (optionnel)
   Skip si ≤5 candidats OU scores bien séparés (≤3 dans zone ambiguë)
   Gemini EXTRACTION preset (temp=0), score 0.0-1.0
   Filtre tools < 0.4
    │
    ▼
7. Score Filtering
   Ratio filter : garder tools avec score ≥ top_score × 0.8
   Absolute filter : garder tools avec score ≥ 0.025
    │
    ▼
8. Workflow Reordering
   Final actions (sent/organized/draft) → déplacées en fin de liste
   Aide le LLM à comprendre la séquence : collecter data → agir
    │
    ▼
9. Dependency Resolution (BFS)
   resolve_dependencies() ajoute les tools prérequis
   Ex: recherche_document → ajoute recherche_acteur
    │
    ▼
10. Dynamic Loading
    ToolLoader.load(names) → importlib.import_module
    @lru_cache(maxsize=200) sur _import_tool()
```

## config.yaml — Le contrat tool ↔ agent

Chaque tool déclare dans `config.yaml` :

```yaml
name: recherche_acteur
agents: [lojii, universal]     # Quels agents peuvent l'utiliser
description: >                  # Texte embedé dans pgvector
  Recherche un acteur NEOTEEM par nom...
examples:                       # Exemples positifs (embedés aussi)
  - qui est Jean Dupont
  - mail de l'entreprise ABC SARL
negative_examples:              # Exemples négatifs (anti-confusion)
  - combien doit M. Martin
confusable_with:                # Signaux de disambiguation
  recherche_document: "Veut des DOCUMENTS, pas juste un contact"
response_type: contact          # Type pour response template
```

**Sync** : `scripts/sync_tool_embeddings.py` lit tous les `config.yaml`, construit le texte `"{name}: {description} Exemples: {examples}"`, et upsert dans `t_tool_embedding` + `t_tool_agent`.

## LLM Query Expansion — Heuristique intelligente

La décision d'expand est prise par `_should_expand_query()` :

| Condition | Expand ? | Raison |
|-----------|----------|--------|
| < 3 mots | Non | Déjà précis |
| Contient keyword clair (mail, acteur, solde…) | Non | Pas besoin |
| Contient référence contextuelle (son, sa, idem…) | Oui | Besoin de clarifier |
| ≥ 6 mots sans keyword | Oui | Long et vague |

Keywords par agent : `_CLEAR_KEYWORDS` dict avec sets différents pour lojii vs universal.

## Tool Coverage Check (Functional Intent Overlap)

Quand on reprend un interrupt, on vérifie que les tools cachés couvrent encore la nouvelle query :

```python
coverage = await check_tool_coverage(query, cached_tool_names, agent_name)
if coverage < 0.40:  # Changement de domaine fonctionnel
    force_reselection()
```

Compare l'embedding de la query vs chaque tool embedding en cache. Plus précis que query-to-query car les tool embeddings encodent l'intent fonctionnel (SEARCH contact ≠ SEND email).

## Stratégies de sélection par contexte

| Contexte | LLM Expansion | Cache | Notes |
|----------|--------------|-------|-------|
| Fresh query | Oui | Non | Pipeline complet |
| Follow-up (acteurs en cache) | Non | context_hint | Plus rapide, pas d'expansion |
| Resume avec state | Skip complet | Reload tools | Juste `ToolLoader.load()` |
| Resume sans state | Non | context_hint | Re-sélection sans expansion |

## Architecture DB

| Table | Colonnes clés |
|-------|--------------|
| `t_tool_embedding` | tool_name, tool_description, tool_examples, tool_embedding (vector), tsvector |
| `t_tool_agent` | tool_name, agent_name (M2M) |
| `t_domain_centroid` | domain, centroid_embedding (pour CentroidDomainRouter) |
| `t_tool_recipe` | Recettes pre-compiled (combinaisons de tools courantes) |

## Fallback

Si la sélection retourne 0 résultats, le `create_tool_selector` factory (dans `selector_factory.py`) retourne des core tools hardcodés :
- Lojii : `LOJII_CORE_TOOLS`
- Universal : `UNIVERSAL_CORE_TOOLS`

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `shared_utils/tools/selector.py` | HybridToolSelector + ToolSelector (legacy) |
| `shared_utils/tools/repository.py` | ToolEmbeddingRepository (pgvector queries) |
| `shared_utils/tools/loader.py` | ToolLoader (importlib dynamic) |
| `shared_utils/tools/dependencies.py` | resolve_dependencies (BFS) |
| `shared_utils/tools/registry.py` | ToolRegistry (legacy, in-memory) |
| `shared_utils/tools/selector_factory.py` | create_tool_selector (fallback wrapper) |
| `shared_utils/tools/recipe_repository.py` | ToolRecipeRepository |
| `shared_utils/engine/domain_router.py` | CentroidDomainRouter |
| `scripts/sync_tool_embeddings.py` | Script de sync config.yaml → pgvector |

## Liens

- [[neochat-architecture]]
- [[neochat-react-engine]]
- [[neochat-adaptive-prompt]]
- [[agents-architecture]]
