---
titre: "Audit MCP forge-brain — Inventaire, forces/faiblesses, optimisations, vs alternatives"
resume: "Audit complet du MCP server custom forge-brain (port 8091 SQLite FTS5) avec inventaire outils, archi technique, comparaison vs qmd/mcp-obsidian/skill+CLI, et roadmap d'optimisation"
aliases:
  - "audit mcp forge brain"
  - "mcp forge brain valorisation"
  - "forge brain mcp outils complet"
  - "mcp custom vs alternatives"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/mcp"
  - "#projet/forge"
---

# Audit MCP forge-brain — 22 mai 2026

> **TL;DR** — MCP server custom **975 LOC Python** (FastMCP 2 + SQLite FTS5), expose **exactement 11 outils** (pas un de plus, pas un de moins) sur 318 notes / 1774 aliases / 1508 wikilinks. Architecture saine, opinionated (BM25 pondéré 10/1/8, 4 stratégies de fallback search, content-hash short-circuit). **Forces uniques** vs alternatives : fallback multi-stratégie + alias expansion à stem variants + auto-start hook + write tools structurés. **Faiblesses** : watcher polling 30s (pas event-based), `git_sync` dead code en deployment forge, zero tests, `_alias_expansion` LIKE O(n). **Verdict** : GARDER, ne pas migrer vers CLI binaire (cf [[recherche-mcp-vs-skills-cli]]). Roadmap : event-based watcher, packaging plugin pour autres vaults, mesure token cost réelle.

---

## 0. Méta-info

| Métrique | Valeur | Source |
|---|---|---|
| Nom package | `mcp-forge-brain` v1.0.0 | `pyproject.toml` |
| Python requis | `>=3.11` | `pyproject.toml` |
| Dépendances runtime | `fastmcp>=2.0`, `pyyaml>=6.0` | `pyproject.toml` — minimaliste, 2 deps |
| LOC total source | **975 lignes** | `wc -l src/**/*.py` |
| Fichiers source | 7 modules (server, database, indexer, watcher, git_sync, config, tools/brain) | — |
| Transport | `streamable-http` | `server.py:128` |
| Port | **8091** | `config.yaml:3` |
| URL MCP | `http://localhost:8091/mcp` | `.mcp.json` |
| Taille DB | **5.18 MB** | `forge-brain.db` |
| Notes indexées | **318** | `vault_stats()` |
| Aliases | **1774** | `vault_stats()` |
| Wikilinks | **1508** | `vault_stats()` |
| Tags | **118** | `vault_stats()` |
| Lifecycle | Lifespan FastMCP avec 3 tâches asyncio (watcher / git pull / git push) | `server.py:44-102` |
| Auto-start | Hook `SessionStart` (`mcp-autostart.py`), socket check port 8091, Popen détaché Windows | `.claude/hooks/mcp-autostart.py` |
| Git history | 6 commits significatifs : v2 init (727d0ce), retrait CLI (764c6ab), gitignore artefacts (c59b97b), restruct vault + fix auto-commit (49c443c), bugs+optimisations (38fb4c5) | `git log` |

---

## 1. Inventaire complet outils MCP (exactement 11 — pas un de plus)

Surface API minimaliste **par design**. `register_tools` (`brain.py:156-257`) enregistre 11 outils, aucun outil caché.

### 1.1 Lecture — 5 outils

#### `search_brain(query: str, limit: int = 5, context: bool = True) -> str`
Recherche FTS5 full-text avec **4 stratégies de fallback** (cf §2.3). Retourne snippets balisés `>>> match <<<` (32 tokens contexte). Ranking via BM25 pondéré (file_stem ×10, content ×1, aliases ×8).

Exemple : `search_brain("opus 47 effort", limit=8)` → notes triées par score, chacune avec son extrait contextualisé.

#### `read_note(file: str, max_lines: int = 0) -> str`
Lit une note par **nom OU alias** (résolution wikilink). Si introuvable, retourne **suggestions automatiques** via `suggest_notes()`. Paramètre `max_lines` ajouté lors de la critique 10 mai pour économiser des tokens (cf [[critique-2026-05-10-mcp-forge-brain]]).

Résolution en 3 paliers (`database.py:235-258`) :
1. Exact match `file_stem` OU `alias`
2. Substring `%-{name}%` (ex: `bail` → `rm-bail-contrat`)
3. Prefix `{name}-%` (ex: `bail` → `bail-commercial`)

#### `read_note_by_path(path: str) -> str`
Lit par chemin exact (ex: `1-Projets/Neoteem/Neoteem.md`). Pas de résolution, pas d'indirection.

#### `get_backlinks(file: str) -> str`
Notes pointant vers `file`. Match exact + substring `%-{file_stem}%` pour les partial wikilinks.

#### `get_property(file: str, name: str) -> str`
Lit une propriété frontmatter via `yaml.safe_load` du raw stocké en colonne `notes.frontmatter`. Listes sérialisées en `", ".join(...)` (fix critique mai 2026).

### 1.2 Navigation — 3 outils

#### `get_tags() -> str`
Tous les tags triés par fréquence. Vue structurelle du vault.

#### `list_notes(folder: str = "", limit: int = 50) -> str`
SQL `WHERE path LIKE 'folder%'` ordonné par `file_stem`. Folder vide = tout le vault.

#### `vault_stats() -> str`
Stats agrégées : nb notes, tags, wikilinks, aliases + tableau markdown répartition par dossier.

### 1.3 Écriture — 3 outils

#### `create_note(path: str, content: str) -> str`
Crée le fichier, parse, indexe **immédiatement** (pas d'attente du watcher polling). Warning si `< 4 aliases` (`brain.py:81`) — enforce le standard qualité. Si `auto_commit` actif → commit git automatique sur branche `mcp/{username}`.

#### `append_note(file: str, content: str) -> str`
Résolution par nom/alias puis `open(..., "a")`. Reparse + réindexe la note entière (pas d'append incrémental côté DB).

#### `update_property(file, name, value) -> str`
Édite le frontmatter via **regex ciblée** (pas `yaml.dump`). Fix critique du 10 mai 2026 — avant ça, `yaml.dump` round-trippait tout : réordonnait clés, re-quotait dates, wrappait résumés, détruisait commentaires (cf [[critique-2026-05-10-mcp-forge-brain]] bug 2).

Pattern :
```python
fm_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
prop_re = re.compile(rf"^{re.escape(name)}:.*$", re.MULTILINE)
```
Si la propriété existe → substitution ligne. Sinon → append en fin de frontmatter. Aucune autre clé n'est touchée.

### 1.4 Verdict surface API

**11 outils est sous le seuil Thariq de "50-100 tools where the model gets confused"** (cf [[recherche-mcp-vs-skills-cli]] §1.3). Surface volontairement étroite — l'absence de tools "exotiques" (semantic search, embedding query, batch ops, full-text replace) est un choix, pas un manque.

---

## 2. Architecture technique

### 2.1 Stack

```
FastMCP 2.0  (transport streamable-http)
    │
    ├─ lifespan (asyncio) — 3 background loops
    │     ├─ VaultWatcher.scan()    every 30s
    │     ├─ GitSync.pull()         every {pull_interval}s
    │     └─ GitSync.push_all()     every {push_interval}s
    │
    └─ BrainTools (11 @mcp.tool wrappers)
          │
          └─ BrainDB
                ├─ sqlite3 (WAL mode)
                └─ tables: notes / aliases / links / tags / notes_fts (FTS5 virtual)
```

Dépendances totales : `fastmcp`, `pyyaml`, stdlib (`sqlite3`, `hashlib`, `re`, `asyncio`, `pathlib`, `subprocess`). **Pas de Obsidian, pas de Node, pas d'ORM, pas de framework web.**

### 2.2 Schéma SQLite

Source : `database.py:33-81`.

| Table | Colonnes | Index | Rôle |
|---|---|---|---|
| `notes` | id PK, file_stem, path UNIQUE, content, frontmatter, last_modified, content_hash | UNIQUE(path) | Stockage canonique |
| `aliases` | note_id FK CASCADE, alias | idx_aliases_alias, idx_aliases_note | Résolution wikilink |
| `links` | source_id FK CASCADE, target | idx_links_target, idx_links_source | Backlinks graph |
| `tags` | note_id FK CASCADE, tag | idx_tags_tag | Filtrage par tag |
| `notes_fts` | file_stem, content, aliases (FTS5 virtual) | unicode61 remove_diacritics=2 | Recherche BM25 |

Pragmas : `journal_mode=WAL` (multi-lecteurs), `foreign_keys=ON` (cascade delete propre).

Migration progressive : `ALTER TABLE notes ADD COLUMN content_hash` enveloppé dans try/except — la DB existante n'est jamais cassée (`database.py:77-80`).

### 2.3 Stratégie de recherche — 4 fallbacks séquentiels

Source : `database.py:192-220`. **C'est la pièce la plus opinionated du code.**

```python
def search(self, query: str, limit: int = 5, context: bool = True):
    # Pré-traitement : strip ponctuation, lowercase, drop stop words FR, len > 1
    # Strategy 1 : AND avec prefix wildcard      "foo"* "bar"*    (strictest)
    # Strategy 2 : OR  avec prefix wildcard      "foo"* OR "bar"* (looser)
    # Strategy 3 : OR  sans wildcard             "foo" OR "bar"   (exact subwords)
    # Strategy 4 : alias expansion + stem variants (last resort)
    # Chaque résultat FTS est ensuite mergé avec alias hits (dédupliqué par path).
```

**Alias expansion avec stem variants** (`database.py:148-156`) :
```python
def _like_variants(term):
    patterns = [f"%{term}%"]
    for suffix in ("ees", "ee", "es", "s", "e"):
        if term.endswith(suffix) and len(term) - len(suffix) >= 3:
            patterns.append(f"%{term[:-len(suffix)]}%")
            break
    return patterns
```
Pas de vrai stemming (Snowball, etc.) — règles ad-hoc FR sur 5 suffixes. Pragmatique, suffisant pour 318 notes.

**BM25 pondéré** (`database.py:118-146`) : `bm25(notes_fts, 10.0, 1.0, 8.0)` → file_stem ×10, content ×1, aliases ×8. Les notes canoniques battent les méta-notes qui mentionnent le terme en passant.

**Stop words FR** (`database.py:11-21`) : 60+ articles, prépositions, pronoms, conjugaisons "être/avoir". **Crucialement n'inclut PAS "erreur", "probleme", "bug", "souci"** — fix du 10 mai 2026 après bug intention filtrée silencieusement.

### 2.4 Frontmatter parsing

Source : `indexer.py`. Regex `^---\s*\n(.*?)\n---\s*\n` (DOTALL), parsing via `yaml.safe_load`, robust à `aliases: str|list` et `tags: str|list`. Frontmatter raw stocké en colonne `notes.frontmatter` pour `get_property` later.

Wikilinks : `\[\[([^\]|]+)(?:\|[^\]]+)?\]\]` — strip pipe alias, dédup ordered.

### 2.5 Indexation incrémentale

Source : `watcher.py`. Polling `rglob("*.md")` avec exclusion `.obsidian`, `Templates`, `Excalidraw` (`config.yaml:21-24`).

**Optimisation non-obvious — content-hash short-circuit** (`watcher.py:42-54`) :
```python
elif file_mtime != db_state[0]:
    content = md_file.read_text(...)
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if content_hash != db_state[1]:
        # vraie modif → reindex
        parse_note(...); db.index_note(...)
    else:
        # mtime touché sans changement de contenu → update mtime seul
        db.execute("UPDATE notes SET last_modified = ? WHERE path = ?", ...)
```
Évite les reindex inutiles quand Git/sync/touch met à jour mtime sans modifier le contenu.

**Delete propagation** : `set(seen_paths) - set(db_paths)` → notes supprimées du FS sont effacées via `delete_note()` (cascade FK supprime aliases/links/tags).

### 2.6 Auto-start

Hook SessionStart `mcp-autostart.py` :
1. Socket check `127.0.0.1:8091` (timeout 1s)
2. Si KO → résout chemin via `__file__` (pas de chemin en dur)
3. `subprocess.Popen` avec flags Windows `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW` + `close_fds=True`
4. Toujours `exit(0)` — non bloquant

**Pattern propre** : pas de PID file, pas de daemon, pas de service Windows. Le socket check suffit pour idempotence.

---

## 3. Forces uniques vs alternatives

Anchored sur le code lu, pas mémoire.

### 3.1 Fallback multi-stratégie (unique)

`mcp-server-obsidian` et `qmd` n'ont pas cette logique. Soit la query matche, soit elle ne matche pas. Notre MCP dégrade progressivement : strict → tolérant → alias expansion. **Conséquence pratique** : `search_brain("opus 47 sessions concurrentes")` trouve des résultats même si aucune note n'a tous les mots. C'est ce qui fait que `search_brain` "marche presque toujours" en pratique.

### 3.2 Alias expansion avec stem variants

Variantes FR ad-hoc (`ees/ee/es/s/e`). Permet à `read_note("technique")` de matcher `techniques`. Aucune alternative connue ne le fait sans dépendance stemming externe (NLTK, snowballstemmer, etc.).

### 3.3 BM25 pondéré opinionated (10/1/8)

Les défauts FTS5 traitent toutes les colonnes à poids égal. Ici, on encode l'intuition : "le nom de la note compte 10× plus que son contenu, les aliases comptent 8×". C'est ce qui fait que `search_brain("Opus 4.7")` ramène la note canonique `opus-47.md` en premier, pas une note random qui la mentionne en passant.

### 3.4 Content-hash short-circuit

Optimisation non-évidente : `mtime` changé sans `hash` changé = juste update mtime, pas de réindex. Aucun MCP Obsidian community ne le fait. Vital quand git/sync touche les fichiers.

### 3.5 Auto-start hook session-level

Pas de service Windows à installer, pas de docker compose, pas de manual start. SessionStart hook → MCP up. Plus simple que tous les MCP Obsidian community qui demandent install + run manuel.

### 3.6 Write tools structurés (atomic + non-reversible)

`create_note`, `append_note`, `update_property` = exactement le pattern Thariq pour "tools" (atomic, non-reversible, UX d'approbation). Aucun MCP Obsidian community n'expose `update_property` ciblé non-destructif (cf §1.3 bug yaml.dump fix).

### 3.7 Warning qualité à la création

`create_note` warne si `< 4 aliases` — enforce le standard de qualité côté API. Innovation propre forge, non documentée ailleurs.

### 3.8 Self-contained (zero infra)

`fastmcp + pyyaml + stdlib`. Pas de Redis, pas de Postgres, pas de vector DB, pas d'embedding API. Tourne sur n'importe quel Python 3.11+. **Total : 975 LOC.** L'équivalent en Node + LangChain + Chroma serait 10× plus.

---

## 4. Faiblesses + bugs connus

### 4.1 Watcher polling, pas event-based (limitation principale)

`server.py:49-60` : `await asyncio.sleep(30)` puis `watcher.scan()`. Donc une note créée hors MCP (Obsidian app, éditeur externe) n'apparaît dans la recherche qu'**après 0-30s**. Aucune alternative (watchdog/inotify) implémentée.

Impact réel : faible (vault personnel, peu de races) mais à savoir.

### 4.2 `git_sync` est dead code en deployment forge

`config.yaml:7-8` :
```yaml
pull_interval_seconds: 9999
push_interval_seconds: 9999
auto_commit: false
```
Le module `GitSync` (47 LOC) tourne en background pour ne rien faire toutes les ~3h. C'est conçu pour les déploiements multi-tenant (Cowork, branches par utilisateur `mcp/{username}`), mais en local forge → bruit. Soit l'activer, soit le rendre opt-in via `git: enabled: false`.

### 4.3 Zero tests

`pyproject.toml:20-22` déclare `testpaths = ["tests"]` mais le dossier n'existe pas. Refactor sur `database.search()` (4 stratégies, alias expansion, merge) est risqué sans suite de tests. Le bug stop words (10 mai) aurait été détecté par un test simple.

### 4.4 `_alias_expansion` LIKE `%term%` — O(n) sur aliases

`database.py:158-190` génère un SQL `LIKE` par variant × par term, sur la table aliases entière (1774 rows). Pas d'index utilisable (LIKE avec wildcard en début). À 318 notes / 1774 aliases : invisible. À 10k notes / 50k aliases : commence à se sentir. Pas un problème immédiat, à surveiller.

### 4.5 Append réindexe la note entière

`append_note` re-parse + re-indexe **tout le contenu** de la note, pas juste le delta. Pour des notes courtes c'est gratuit. Pour des MOCs gros (`MOC-Techniques`, etc.) ça reparse 200L à chaque append. Optimisation possible : append incrémental côté FTS.

### 4.6 Subprocess git_sync sans gestion d'erreur fine

`git_sync._git` capture stdout/stderr mais le code appelant ne vérifie jamais `returncode`. Si un push échoue (auth, conflict), c'est logué (`logger.exception`) mais ignoré. OK car `auto_commit: false` aujourd'hui, mais dangereux si activé.

### 4.7 Bugs historiques (corrigés, à mémoriser)

- **Bug stop words sémantiques** (10 mai) — "erreur/probleme/bug/souci" étaient filtrés. Fix : retirés. Backlinks : [[critique-2026-05-10-mcp-forge-brain]] §"Bug 1".
- **Bug `yaml.dump` corrompait frontmatter** (10 mai) — round-trip réordonnait clés, re-quotait dates. Fix : regex ciblée. Backlinks : même note, "Bug 2".
- **Bug ranking pollué par aliases "knowledge"/"synthese"** (10 mai) — auto-boost retiré. Même note, "Amélioration 4".

### 4.8 Absence de semantic search (choix, pas oubli)

Pas d'embeddings, pas de reranking LLM. **Décision documentée** : à 318 notes, FTS5 BM25 + alias expansion suffit. Seuil estimé : embeddings pertinents à 1000-5000+ notes (cf critique 10 mai). À reconsidérer si vault dépasse ce seuil.

---

## 5. Tableau comparatif

| Critère | **MCP forge-brain** (custom) | **mcp-server-obsidian** (community) | **Karpathy qmd** (CLI+MCP) | **Skill+CLI minimaliste** |
|---|---|---|---|---|
| Architecture | FastMCP 2 + SQLite FTS5 self-contained | Node TS, dépend de Local REST API plugin Obsidian | Binaire Go/Rust, BM25 + vector + LLM rerank | bash + grep + ripgrep + jq |
| Dépendances | 2 (fastmcp, pyyaml) | Obsidian app + Local REST API plugin + Node | Aucune (single binary) | Aucune |
| Stockage index | SQLite FTS5 jetable | Pas d'index — délègue à Obsidian Search | Hybrid BM25 + vector on-disk | Aucun (live grep) |
| Recherche | BM25 pondéré 10/1/8 + 4-strategy fallback + alias stem variants | Délègue à Obsidian Search (closed-source) | BM25 + vector cosine + LLM rerank | regex/grep |
| Wikilink resolution | Aliases (FR/EN/variantes) + 3 paliers substring | Limité à exact match | Exact match | Manuel |
| Backlinks | Oui (`get_backlinks` SQL JOIN) | Oui (via Obsidian) | Non | Non (à scripter) |
| Frontmatter property edit | Regex non-destructive (`update_property`) | Non | Non | sed/awk (risqué) |
| Auto-start | Hook SessionStart Windows-aware | Manual | Manual | N/A |
| Cost tokens (par session) | 11 tool defs ~3-5k estimé | ~5-8k estimé | ~3k (4 tools : search/get/list/index) | ~0 (just SKILL.md text) |
| Sécurité | Local-only, surface 11 tools | Dépend du plugin Obsidian (HTTP REST) | Local-only | Local-only |
| Multi-tenant Cowork | Pré-câblé (`git_sync` branches `mcp/{username}`) | Non | Non | Non |
| Composabilité | Faible (tools structurés) | Faible | Élevée (binaire shell-friendly) | **Maximale** |
| Discoverability | Tools auto-listés | Tools auto-listés | Auto-listés (MCP) + `qmd --help` (CLI) | Description-driven (lazy) |
| LOC | **975** Python | ~2000+ TS + Obsidian plugin | inconnu (binaire) | ~50 (juste SKILL.md) |
| Forces uniques | Fallback 4-strat, alias stem, content-hash short-circuit, write tools structurés non-destructifs | Intégration native Obsidian (templates, dataview, plugins) | LLM rerank, vector search, packagé proprement | Token cost ~0, composable au max |
| Idéal pour | Vault personnel/équipe < 5k notes avec write structurés | User qui vit dans Obsidian app | Vault > 5k notes ou hétérogène multi-format | Vault read-only consulté occasionnellement |
| Anti-pattern | "écrire en bash heredoc en bypass" (cf gotcha vault) | "compromised REST plugin" | "vouloir aussi écrire structuré" | "écrire frontmatter en sed" |

---

## 6. Doctrine "quand MCP vs skill" — application forge

Cf [[recherche-mcp-vs-skills-cli]] pour la doctrine complète et verbatim sources (Anthropic, Thariq, Willison, Karpathy, Ronacher, Boris, Trail of Bits).

**Application spécifique forge-brain — ce qui ne figure PAS dans la note recherche** :

- **Les 11 outils MCP couvrent les 3 catégories Thariq** :
  - **atomic non-reversible** → `create_note`, `update_property`, `append_note` (✓ légitimement MCP)
  - **structured reads** → `get_backlinks`, `get_property`, `vault_stats` (✓ légitimement MCP — query DB, mal composable en bash)
  - **search** → `search_brain` (✓ MCP car index FTS5 in-process, subprocess CLI à chaque query = perte du cache)

- **Aucun outil n'est mal placé**. Tous remplissent un critère Thariq pour "tool". Pas de candidat évident à migrer vers skill+CLI.

- **Skill descriptor `forge-brain` existe déjà** (`.claude/skills/forge-brain/SKILL.md`, ~150L) avec decision tree quand utiliser quel outil → pattern progressive disclosure validé.

- **Hook `vault-query-guard`** complète l'advisory rule par enforcement déterministe — c'est ce qui fait passer la compliance de ~80% à 100% (cf [[feedback_enforce_not_advise]] révisé 22 mai).

**Verdict** : pas de refactor à faire. La structure actuelle (MCP + skill + hook) est cohérente avec la doctrine 2026.

---

## 7. Optimisations proposées — ranked valeur/effort

| # | Optimisation | Valeur | Effort | Priorité |
|---|---|---|---|---|
| 1 | **Tests pytest** sur `database.search()` (4 stratégies, alias expansion, merge, stop words) | Haute (prévient régressions du type bug 10 mai) | Bas (1-2j) | **P0** |
| 2 | **Watcher event-based** via `watchdog` (FS events, fallback poll) | Moyenne (latence 0-30s → instant) | Moyen (1j) | P1 |
| 3 | **Mesurer token cost réel** au démarrage session via Langfuse trace | Haute (validation hypothèse 3-5k tokens) | Bas (½j) | **P0** |
| 4 | **`git_sync` opt-in** via `git: enabled: false` config + skip lifespan loops si disabled | Basse (cleanup) | Bas (1h) | P2 |
| 5 | **Packaging plugin Cowork** réutilisable (template `mcp-{name}` avec config.yaml-driven) | Haute (réutilisable neoteem-brain, lojii, futurs vaults) | Moyen (2j) | P1 |
| 6 | **Append incrémental FTS** au lieu de réindex complet | Basse à 318 notes, haute à 5k+ | Moyen (1j) | P3 |
| 7 | **Hybrid search semantic** (sentence-transformers + rerank) — seulement si vault > 1000 notes | Haute (au-dessus du seuil) | Élevé (3-5j) | **NOT NOW** |
| 8 | **MCP cross-vault** (un seul MCP qui sert forge-brain + neoteem-brain + lojii via config multi-vault) | Moyenne (UX simpler) | Élevé (3j) | P3 |
| 9 | **`search_brain` paramètre `folder` filter** (limiter au sous-vault `Knowledge/erreurs/`) | Moyenne (queries plus ciblées) | Bas (½j) | P2 |
| 10 | **`bulk_create_notes`** pour init vault massif | Basse | Bas | P3 |
| 11 | **`delete_note(file)` tool MCP** — actuellement seul le watcher delete | Basse (rare besoin) | Bas | P3 |
| 12 | **`get_orphans()` / `get_dead_links()`** tools de maintenance vault | Moyenne (vault-audit automatisé) | Bas (1j) | P2 |
| 13 | **Rate limiting / observability** (compteur appels par tool, latence p50/p99) via FastMCP middleware | Basse aujourd'hui, haute en multi-tenant | Moyen | P3 |

**Top 3 actionnables court terme** : #1 (tests), #3 (mesure tokens), #5 (packaging plugin).

---

## 8. Réutilisabilité — packaging plugin pour autres vaults

### 8.1 État actuel — déjà presque générique

Le code est **déjà 95% générique**. Tout est driven par `config.yaml` :
- `vault_path` (chemin du vault)
- `db_path` (où stocker l'index)
- `port` (8091 forge, autre port pour autre vault)
- `excluded_dirs` (templates, daily, etc.)
- `fts.weights` (BM25 ajustable)
- `git.*` (multi-tenant Cowork)

Aucun hardcoding "forge-brain" significatif côté logique. Le seul truc forge-spécifique : nom du module (`mcp-forge-brain`), nom du serveur (`name="forge-brain"` dans `server.py:106`), config par défaut.

### 8.2 Pattern existant — `mcp-obsidian-brain-v2` Neoteem

Cf [[mcp-obsidian-brain-v2]] : MCP **dérivé** de forge-brain pour le vault `neoteem-brain`, déployé sur VM serveur, accessible via VPN, intégré aux 5 plugins Cowork. La généralisation a déjà été faite une fois → preuve de réutilisabilité.

### 8.3 Roadmap packaging

**Étape 1 — Extraction template** :
- Renommer `mcp-forge-brain/` en `mcp-vault-brain/` (générique)
- Variables d'environnement override : `VAULT_BRAIN_NAME`, `VAULT_BRAIN_PATH`, `VAULT_BRAIN_PORT`
- `pyproject.toml` : `mcp-vault-brain = "start:main"`

**Étape 2 — Plugin Cowork** :
- Structure `.claude-plugin/plugin.json` + `skills/` + `hooks/` + `mcp/`
- Hook `mcp-autostart-{name}.py` paramétré
- Skill descriptor `{name}-brain/SKILL.md` template

**Étape 3 — Installation 1-shot** :
- `install.bat <vault_path> <name> <port>` qui :
  1. Clone le template MCP
  2. Génère `config.yaml`
  3. Installe le hook SessionStart adapté
  4. Génère le skill descriptor avec le bon nom

**Étape 4 — Multi-vault sur même instance** (futur) :
- Refactor server : 1 process, plusieurs `BrainDB` montés à des paths différents
- Tool param `vault: str` pour sélectionner
- Évite N processes Python pour N vaults

### 8.4 Candidats internes

| Vault | Actuel | Packaging cible |
|---|---|---|
| `forge-brain` | MCP custom (port 8091) | Source de vérité du pattern |
| `neoteem-brain` | MCP dérivé (port différent, VM) | Déjà packagé v2 |
| `lojii` | Pas de vault | À créer si knowledge base apparaît |
| Vault perso non-Neoteem (futur) | — | Drop-in via template |

### 8.5 Distribution

- Repo : `mcp-vault-brain` (extraction de `mcp-forge-brain/`)
- Versioning : sem-ver propre, breaking changes documentés
- Doc minimale : README + `config.yaml` annoté + exemples 3 vaults
- Plugin Cowork distribué via marketplace interne Neoteem

---

## 9. Conclusion + actions

### 9.1 Verdict global

**Le MCP forge-brain est un asset stratégique sous-valorisé.** 975 LOC Python qui fait mieux que `mcp-server-obsidian` (community) sur 4 axes uniques : fallback multi-stratégie, alias stem variants, content-hash short-circuit, write tools non-destructifs. Architecture saine, dépendances minimales (2), packageable.

### 9.2 Top 3 actions immédiates

1. **Tests pytest** sur `database.search()` (P0) — prévient régression type bug stop words du 10 mai
2. **Mesure token cost réel** via Langfuse (P0) — valide ou invalide l'hypothèse 3-5k tokens
3. **Packaging plugin `mcp-vault-brain`** (P1) — capitalise sur la généralisation déjà faite avec neoteem-brain

### 9.3 Ne PAS faire

- ❌ Migrer vers CLI binaire — coût migration > bénéfice (cf [[recherche-mcp-vs-skills-cli]] §4)
- ❌ Ajouter semantic search/embeddings — vault < 1000 notes, FTS5 suffit largement
- ❌ Supprimer `git_sync` — utile pour packaging Cowork futur, juste le rendre opt-in

### 9.4 Liens vault

- [[recherche-mcp-vs-skills-cli]] — doctrine MCP vs Skills (sources verbatim Anthropic/Thariq/Willison/Karpathy)
- [[critique-2026-05-10-mcp-forge-brain]] — devil's advocate mai 2026, 2 bugs + 4 optimisations
- [[architecture-cerveau-obsidian-mcp]] — guide pédagogique du pattern complet
- [[sqlite-fts5-vault]] — pattern FTS5 réutilisable
- [[mcp-obsidian-brain-v2]] — version Neoteem-brain (preuve réutilisabilité)
- [[karpathy-llm-wiki-pattern]] — pattern qmd verbatim Karpathy
- [[reference_obsidian_query_brain]] — pattern neo-brain wrapper CLI + skill

---

*Audit réalisé 22 mai 2026, source primary = code lu intégralement (`mcp-forge-brain/src/` 975 LOC) + critique 10 mai 2026 + recherche doctrine MCP vs Skills 22 mai 2026.*
