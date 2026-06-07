---
titre: "Gotcha MCP — alias ambigu résout vers le mauvais fichier"
resume: "Tout outil MCP forge-brain qui prend file=<alias> résout par FTS sur stem+aliases. Si le stem est ambigu (log/index/CHANGELOG, présents dans ≥2 dossiers), l'écriture part dans le mauvais fichier. Workaround : read_note_by_path + Read/Edit chemin exact. Hook mcp-alias-guard couvre les outils file=."
aliases:
  - "mcp alias ambigu"
  - "file alias résout mauvais fichier"
  - "log index CHANGELOG stem ambigu"
  - "mcp-alias-guard hook"
  - "chemin exact vs alias MCP"
derniere-maj: 2026-06-07
auteur: claude
type: pattern
tags:
  - "#type/pattern"
  - "#domaine/mcp"
  - "#domaine/vault"
---

# Gotcha MCP — alias ambigu résout vers le mauvais fichier

> Tout outil MCP forge-brain qui accepte `file=<chaîne>` résout par FTS sur `stem + aliases`. Si le stem peut être ambigu, l'écriture part **silencieusement** dans le mauvais fichier.

## Le problème

Les outils `append_note`, `insert_section`, `read_section`, `update_note`, `update_property`, `delete_note`, `move_note`, `bulk_update_property` prennent un paramètre `file=`. Quand le stem visé existe dans **plusieurs dossiers** du vault (`log`, `index`, `CHANGELOG`, et tout stem présent dans ≥2 dossiers), la résolution FTS peut matcher le mauvais fichier.

Cas vécu : `append_note(file="log")` a écrit dans `2-Casquettes/responsable-ia/log.md` au lieu du `log.md` racine, car le log racine porte l'alias `"log vault"` (pas `"log"` seul). Même `file="log vault"` reste risqué (l'alias proscrit). Le pattern s'est répété **≥7 fois** sur des outils MCP différents (`append_note`, `insert_section`, `update_property`) malgré une règle textuelle — illustration de [[erreur-advisory-rules-insuffisantes]] (règle ré-violée → garde-fou structurel requis).

## Workaround définitif

- **Lire** : `read_note_by_path(path=<chemin exact>)` plutôt que `read_note(file=<alias>)`.
- **Écrire** sur un stem ambigu (`log`/`index`/`CHANGELOG`) : `Read` + `Edit` direct sur le filesystem au chemin exact — l'édition vault directe de ces fichiers d'orientation n'est **pas** bloquée par hook.
- Les outils MCP `file=<alias>` ne sont sûrs QUE pour des **stems vault-uniques** (vérifiable par `list_notes`).

## Garde-fou structurel

Le hook `mcp-alias-guard.py` (PreToolUse sur les outils MCP forge-brain à paramètre `file=`) bloque l'appel sur un stem ambigu et oriente vers le chemin exact. Ne JAMAIS contourner — corriger l'appel.

## Gotcha connexe — suffixe `.md` non supporté

`insert_section(file="log.md")` retourne "introuvable" : l'outil résout par nom/alias, pas par chemin avec extension. `insert_section(file="vault/claude-forge/log.md")` échoue aussi (le path n'est pas une signature d'alias). Si un outil `file=` retourne "introuvable" sur `log`/`index`/`CHANGELOG`, ne pas tenter l'alias court — passer en Read/Edit filesystem direct.

## Wikilinks

- [[mcp-vault-llm-design]] — design MCP vault LLM-optimized (gotchas résolution)
- [[erreur-advisory-rules-insuffisantes]] — règle textuelle ré-violée → garde-fou déterministe
