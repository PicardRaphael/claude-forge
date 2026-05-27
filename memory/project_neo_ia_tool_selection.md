---
name: neo-ia-tool-selection-state
description: "État actuel du HybridToolSelector neo_ia — expansion ACTIVE en prod sur fresh queries, reranking LLM OFF, plan Lazy Expansion + OATS"
metadata: 
  node_type: memory
  type: project
  originSessionId: b4f87302-63a5-49aa-b656-0fddab6ec10d
---

HybridToolSelector de neo_ia — pipeline 10 étapes. État réel en prod :
- `use_llm_expansion=True` passé dynamiquement par ReAct engine sur fresh queries (react.py:400-402)
- `use_llm_rerank=False` sur les singletons (reranking LLM désactivé)
- `_CLEAR_KEYWORDS` = 4 sets de mots-clés maintenus à la main, fragiles
- Heuristique `_should_expand_query()` filtre AVANT l'expansion (< 3 mots = skip, keywords = skip, ≥ 6 mots = expand)

**Why:** L'expansion EST active mais gatée par une heuristique fragile. 3 paires de tools confusables identifiées par architect (recherche_membres_cs/lister_donnees, acteur_detail/recherche_document/lister_donnees sur "factures", recherche_acteur/acteur_detail).

**How to apply:** Plan validé avec Raphael :
1. Tester fix actuel en prod ("liste des baux" → lister_donnees)
2. Phase 1 Lazy Expansion : supprimer _CLEAR_KEYWORDS + heuristique, remplacer par search brut → score bas → LLM rewrite Re-Invoke → re-search
3. Phase 2 OATS : pipeline offline Langfuse → shift embeddings (post 2-3 semaines de traces)

Code : `packages/shared_utils/shared_utils/tools/selector.py` (L55-248 pour expansion, L545-1000 pour HybridToolSelector, L781-924 pour reranking)

Vault : [[tool-retrieval-query-expansion]] pour l'état de l'art complet
