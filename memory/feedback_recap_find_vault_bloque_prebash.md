---
name: recap-find-vault-bloque-prebash
description: "/recap collecte find vault/ bloquée par pre-bash-guards — skill à fixer (MCP)"
metadata:
  type: feedback
---

La skill `/recap` lance des `find vault/claude-forge -name "*.md" -mtime -7` pour ses collectes "notes modifiées <7j / Knowledge / contexte", en les documentant comme « seul usage acceptable de find ». Mais le hook `pre-bash-guards.py` bloque tout accès Bash au vault → ces collectes échouent silencieusement (le rapport recap n'a pas la liste des notes récentes).

**Why:** contradiction interne skill↔hook : `/recap` prescrit une commande que la doctrine MCP-only interdit. Observé 2026-06-27.
**How to apply:** quand on touche `/recap` (ou tout besoin "notes par date de modif"), remplacer le `find` par MCP `find_by_property(name="derniere-maj", comparator="gt", ...)` ou `list_notes`. Ne pas se fier au rapport recap pour les notes récentes tant que la skill n'est pas fixée.
