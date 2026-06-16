---
titre: "Gotcha MCP — alias ambigu résout vers le mauvais fichier"
resume: "Tout outil MCP forge-brain qui prend file=<alias> résout par FTS sur stem+aliases. Si le stem est ambigu (log/index/CHANGELOG, présents dans ≥2 dossiers), l'écriture part dans le mauvais fichier. Workaround : les variantes *_by_path (jamais Edit disque direct, qui désync l'index SQLite). Hook mcp-alias-guard couvre les outils file=."
aliases:
  - "mcp alias ambigu"
  - "file alias résout mauvais fichier"
  - "log index CHANGELOG stem ambigu"
  - "mcp-alias-guard hook"
  - "chemin exact vs alias MCP"
  - "read_note_by_path pas de pagination note massive"
derniere-maj: 2026-06-16
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

## Workaround définitif — les variantes `*_by_path`

Le serveur expose des jumeaux à **chemin exact** qui ne résolvent jamais de travers : `read_note_by_path`, `update_note_by_path`, `append_note_by_path`, `insert_section_by_path`, `update_property_by_path`.

- **Lire** : `read_note_by_path(path=<chemin exact>)`.
- **Écrire** sur un stem ambigu (`log`/`index`/`CHANGELOG`) : la variante `*_by_path` correspondante (`insert_section_by_path`, `update_note_by_path`…).
- **NE PAS** retomber sur `Read` + `Edit` disque direct : l'édition filesystem d'une note vault **désynchronise l'index SQLite** (réindex au poll 30s seulement) et est refusée par le harness si la note a été lue via MCP et non via le tool Read. Toujours rester côté MCP. Cf [[vault-edit-gotchas-outillage]].
- Les outils MCP `file=<alias>` ne sont sûrs QUE pour des **stems vault-uniques** (vérifiable par `list_notes`).

## Gotcha — `read_note_by_path` n'a PAS de pagination (mur sur note massive)

Découvert 16 juin 2026. Seul `read_note(file=…)` accepte `offset` / `limit_chars` / `max_lines` ; **`read_note_by_path(path=…)` ne prend QUE `path`**. Donc sur une note volumineuse à stem ambigu (le `CHANGELOG.md` racine fait ~190k chars), `read_note_by_path` dépasse le cap tokens du résultat et **n'a aucun paramètre pour paginer** → impasse. Issues en cascade observées : `read_section(file="CHANGELOG")` est bloqué par `mcp-alias-guard` (stem ambigu), et `read_section` n'a pas de variante `_by_path`.

Workarounds pour lire/cibler une grosse note à stem ambigu :
1. **`read_note(file=<alias UNIQUE du frontmatter>, offset=N, limit_chars=M)`** — la pagination existe sur `read_note` ; il faut juste un alias non ambigu (pas le stem nu).
2. **Pour une simple insertion ciblée** : pas besoin de relire toute la note — récupérer le **marker exact** (la ligne de header) depuis un petit extrait, puis `insert_section_by_path(path=…, marker=…, position="after")`. C'est la voie utilisée pour ajouter une entrée datée au CHANGELOG.
3. **Extraire une zone depuis le fichier tool-result sauvegardé** : quand un résultat MCP dépasse le cap, le harness l'écrit dans un `.txt`. Le parser en Python (`json.load`, chercher le header) — penser `sys.stdout.reconfigure(encoding="utf-8")` car la console Windows est cp1252 et plante sur `→`/accents.

## Gotcha connexe — suffixe `.md` non supporté sur `file=`

`insert_section(file="log.md")` retourne "introuvable" : l'outil `file=` résout par nom/alias, pas par chemin avec extension. `insert_section(file="vault/claude-forge/log.md")` échoue aussi. Si un outil `file=` retourne "introuvable" sur `log`/`index`/`CHANGELOG`, ne pas tenter l'alias court — passer à la variante `*_by_path`.

## Garde-fou structurel

Le hook `mcp-alias-guard.py` (PreToolUse sur les outils MCP forge-brain à paramètre `file=`) bloque l'appel sur un stem ambigu et oriente vers le chemin exact / la variante `*_by_path`. Ne JAMAIS contourner — corriger l'appel.

## Wikilinks

- [[mcp-vault-llm-design]] — design MCP vault LLM-optimized (gotchas résolution)
- [[vault-edit-gotchas-outillage]] — Edit disque direct désync l'index SQLite + insert_section misparente
- [[erreur-advisory-rules-insuffisantes]] — règle textuelle ré-violée → garde-fou déterministe
