---
name: search-brain-context-defaut
description: search_brain renvoie déjà context=true avec highlights ">>> term <<<" — pas besoin d'ajouter snippets
metadata:
  type: reference
---

L'outil MCP `mcp__forge-brain__search_brain` a `context: true` en paramètre par défaut. Chaque résultat contient déjà des extraits autour des matches avec highlights `>>> term <<<` (FTS5 BM25 pondéré file_stem:10 / aliases:8 / content:1). Aucun besoin d'ajouter une couche "snippets" pour permettre tri avant `read_note` — c'est déjà là.

**Why:** Phase 1 forge 28 mai — l'audit consolidé externe 4 sources proposait "ajouter snippets 150 chars dans search_brain". Vérification empirique (1 appel `search_brain`) a montré que c'était déjà fait. ~1h économisée à ne pas modifier mcp-forge-brain.
**How to apply:** Avant d'optimiser un outil MCP existant, lancer 1 appel test pour vérifier le comportement actuel. Pattern verify-empirique-avant-modif. L'audit externe peut prescrire un fix dont la cible est déjà résolue.
