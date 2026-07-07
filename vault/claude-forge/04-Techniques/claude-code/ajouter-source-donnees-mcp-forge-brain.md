---
titre: "Ajouter une source de données au MCP forge-brain"
resume: "Pattern canonique pour brancher une nouvelle source de données indexable (transcripts session, autre vault, logs) sur le serveur MCP forge-brain : table FTS5 séparée + indexer robuste + watcher incrémental mtime + outil exposé. Validé par search_sessions (A1, 27 mai 2026)."
aliases:
  - "ajouter source mcp forge-brain"
  - "nouvelle source données mcp"
  - "pattern indexer fts5 forge-brain"
  - "search_sessions architecture"
  - "indexer transcripts session"
  - "étendre mcp forge-brain"
derniere-maj: 2026-05-27
auteur: claude
type: technique
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
  - "#projet/claude-forge"
---

# Ajouter une source de données au MCP forge-brain

> Pattern réutilisable pour brancher une nouvelle source indexable sur le serveur MCP forge-brain sans toucher l'index vault existant. Première application : `search_sessions` (recherche transcripts session, A1 roadmap Phase 4).

## QUOI

Le MCP forge-brain indexe à l'origine le vault Obsidian (`notes` + `notes_fts`). Quand on veut chercher dans une AUTRE source (transcripts `~/.claude/projects/*.jsonl`, logs, second vault), on ajoute un module parallèle plutôt que de polluer l'index vault.

## POURQUOI tables séparées

| Critère | Vault (`notes`) | Source ajoutée (ex: `session_messages`) |
|---------|-----------------|------------------------------------------|
| Durabilité | Notes curées, durables | Souvent éphémère / haute volumétrie |
| Schéma | file_stem, aliases, wikilinks, tags | propre à la source (session_id, role, timestamp) |
| Ranking BM25 | pondéré file_stem:10/aliases:8/content:1 | content seul en général |
| Risque | mélanger = `search_brain` retourne du bruit | isolé = chaque outil reste net |

Réutiliser `notes_fts` avec un champ `source` aurait cassé la pondération BM25 et brouillé `search_brain`. Tables séparées = concerns séparés.

## COMMENT — 5 fichiers, 1 connexion partagée

Application `search_sessions` (chemins réels) :

1. **`src/<source>_indexer.py`** — `parse_<source>(path, ...) -> list[ParsedX]`. Extraction + filtrage du bruit. **Ne JAMAIS lever sur données externes** (try/except autour de la lecture, skip lignes malformées). Ex : `sessions_indexer.py` filtre les types non-conversationnels, blocks tool_use/thinking, commandes locales, messages < 15 chars.

2. **`src/<source>_db.py`** — classe `XDB` qui REÇOIT la connexion sqlite du vault (`SessionDB(db._conn)`), crée ses propres tables + table FTS5 `unicode61 remove_diacritics 2`, expose `index_*`, `search`, `get_file_state`, `delete_path`, `known_paths`, `stats`. Sanitize les requêtes FTS (strip `'"-()*`, termes len>1) pour l'injection-safety.

3. **`src/<source>_watcher.py`** — `XWatcher.scan()` calqué sur `VaultWatcher` : incrémental par `st_mtime`, supprime les fichiers disparus (`known_paths() - seen`). Filtres d'inclusion configurables, JAMAIS hardcodés (ex: `include_subagents`).

4. **`src/config.py` + `config.yaml`** — dataclass `XConfig(enabled, path, ...)`. Activation par flag. Les chemins `~` via `.expanduser()`.

5. **`src/server.py`** — init conditionnel (`if cfg.x.enabled`), scan initial EAGER avec mesure de temps (`time.monotonic()`), boucle poll dans le lifespan asyncio existant. **`src/tools/brain.py`** — méthode sur `BrainTools` + enregistrement `@_tool` (log_call auto). Garde-fou si source désactivée.

## QUAND appliquer

- Nouvelle source cherchable plein-texte, volumétrie ≠ vault, schéma ≠ note.
- PAS pour ajouter un champ à une note (→ frontmatter + reindex vault).
- PAS pour une donnée déjà dans le repo accessible en 1 `Bash`/`Read`.

## Décisions tranchées (search_sessions)

- **Granularité** : 1 doc FTS = 1 message (snippet précis, filtres role/date, recompose via session_id).
- **Scan** : eager au boot, pas lazy. Mesuré 2.68s pour 243 fichiers / 15858 messages → sous le seuil 5s, optim lazy prématurée. Doctrine "mesurer avant optimiser".
- **Exclusions configurables** : `include_subagents: false` en default (1210 subagents = 80% bruit) mais option préservée — coût zéro maintenant.
- **Pas de symétrie artificielle** : filtre `until` écarté (usage marginal), `since` gardé.
- **< 15 tools/serveur** (doctrine [[mcp-vs-skills-doctrine]]) : on passe à 22, sous surveillance. 1 seul outil ajouté, pas une famille.

## Tests — cœur MCP, ratio adverse

> ⚠️ **Gotcha couche wrapper** (7 juin 2026) : tester l'outil via `BrainTools` directement n'exerce PAS la couche `register_tools` (wrappers `@_tool` : enregistrement FastMCP, validation/passage d'args, `log_call`). Une faute de wrapper (ordre/nom d'args, oubli d'enregistrement) passe les tests verts et casse l'outil en prod. Ajouter ≥1 test qui construit un `FastMCP` réel et exerce `register_tools` via l'API publique — `asyncio.run(mcp._list_tools())` (outils enregistrés) + `asyncio.run(mcp.call_tool("nom", {args}))` (dispatch de bout en bout) — **sans binder le port** (`register_tools` ne le touche pas ; seul `app.run()` dans `main()` le fait). Détail : `memory/reference_mcp_forge_brain_lifecycle_gotchas.md`.

Sur le modèle de `test_search.py` : fixture déterministe, chaque filtre + edge case. ~60% adverse pour une source de données externe : JSONL malformé, fichier vide, message sans content, encodage cassé, FTS operators hostiles, query vide, projet inexistant, incrémental sans rescan, suppression fichier disparu. 18 + 19 = 37 tests, 0 régression.

## Cycle de vie — gotchas opérationnels

### Gotcha #1 — Recharger le code = KILL port 8091 + NOUVELLE session

Après modification du code serveur (`mcp-forge-brain/src/...`), les changements ne sont PAS visibles dans la session courante : le handshake MCP (liste des outils) est figé au SessionStart. `mcp-autostart.py` fait `if port_open(8091): exit(0)` → tant que l'ancien process tient le port, même une nouvelle session relance l'ANCIEN code.

Séquence correcte : **`taskkill` le process Python sur le port 8091 → PUIS ouvrir une NOUVELLE session** (son SessionStart voit le port fermé → autostart lance le code à jour). Tuer mid-session ne relance rien. Oublier le kill = reconnexion silencieuse à l'ancien code → tests "live" contre des outils périmés = faux résultat déroutant.

**Wrinkle élévation** : `taskkill /PID <pid> /F` peut échouer « Accès refusé » si le process a été lancé par une session à privilège différent. Symptôme : outils absents de la session ET `taskkill` refusé = serveur périmé non-tuable sans élévation → kill revient à l'utilisateur (PowerShell admin ou Gestionnaire des tâches).

### Gotcha #2 — `register_tools` non testé si les tests appellent `BrainTools` directement

Déjà couvert dans la section Tests ci-dessus.

### Gotcha #3 — Changement du PARSER = supprimer la DB (le watcher incrémental ne suffit pas)

`VaultWatcher.scan()` est incrémental : il ne reparse une note que si son `mtime`/hash a changé. Quand on modifie le CODE de parsing (`indexer.py` — ex. ajout de `_strip_code` pour ignorer les wikilinks en code spans), les notes existantes inchangées **gardent leurs données parsées à l'ancienne façon**, même après kill + nouvelle session.

Fix : `kill serveur → Remove-Item forge-brain.db* (+ -wal + -shm) → NOUVELLE session → rebuild complet`. La DB est 100 % reconstructible depuis les `.md` (vérité = les notes). Preuve 14 juin 2026 : après rebuild, `broken_wikilinks` 88 → 75 (13 faux positifs en code spans éliminés).

Distinction nette : changement de **NOTE** → watcher suffit (≤ 30 s) ; changement de **CODE serveur** (nouveaux outils) → kill + nouvelle session (gotcha #1) ; changement de **PARSER** → delete DB en plus (gotcha #3).
## ANTI-PATTERNS

- Réutiliser `notes_fts` avec un champ discriminant → casse BM25 vault, brouille `search_brain`.
- Indexer le bruit (tool_result, thinking, commandes locales) → résultats pollués.
- Indexer sans filtrage configurable hardcodé → impossible d'ajuster sans patcher le code.
- Parser qui lève sur données externes → crash du watcher en prod.
- Lazy par défaut "au cas où ce serait lent" → optim prématurée, mesurer d'abord.

## APPELS

- [[mcp-vs-skills-doctrine]] — pourquoi MCP (data) et pas skill (how-to) pour l'indexation
- [[pattern-vault-llm-karpathy]] — l'architecture 3-layers que le MCP sert
- [[comment-creer-skill]] — si on veut exposer la source via une skill plutôt qu'un outil brut
