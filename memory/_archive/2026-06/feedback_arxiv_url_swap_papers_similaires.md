---
name: arxiv-url-swap-entre-papers-meme-domaine
description: "Pattern double erreur — quand 2 papers similaires sont cités dans une même note, vérifier que les URLs ne sont pas swapées. Audit RAG 23 mai : MCP-Zero ↔ OATS (échange entre 2603.13426 et 2506.01056/2603.20313)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7960dab2-e6be-4b55-ba9e-1985dac06f32
---

Quand une note vault cite **plusieurs papers du même domaine** (tool retrieval, agents, RAG, etc.), vérifier que chaque URL pointe vers le BON paper, pas le voisin.

**Why** : Audit thématique RAG 23 mai 2026 a trouvé dans `tool-retrieval-query-expansion.md` :
- MCP-Zero pointait vers arXiv 2603.13426 (= en réalité OATS)
- OATS pointait vers arXiv 2603.20313 (= en réalité Semantic Tool Discovery)
- Vrai MCP-Zero = 2506.01056

Double swap = erreur Type 1 silencieuse, indétectable sans WebFetch des URLs.

**How to apply** :
- Audit thématique : WebFetch SYSTÉMATIQUE de chaque URL arXiv quand plusieurs papers du même domaine sont cités côte-à-côte
- Création note : copier l'URL depuis arXiv abstract page, pas reconstruire de mémoire
- Red flag : si une liste de sources contient N URLs arXiv du même domaine, probabilité de swap > 0
- Validation : Title du paper trouvé via WebFetch DOIT correspondre au nom cité dans la note

Lié : [[erreur-audit-rag-11-faux-2026-05-23]] [[feedback_audit_thematique_methode]] [[feedback_verify_exhaustive_claims]]
