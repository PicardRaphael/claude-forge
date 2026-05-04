# MCP Obsidian Brain v2 — Spec

**Date :** 2026-04-29
**Auteur :** Raphael Picard + Claude Forge
**Statut :** En attente de validation

## Objectif

Remplacer la dependance Obsidian CLI du MCP obsidian-brain par un index SQLite FTS5 autonome. Le MCP tourne en mode HTTP sur une VM serveur, accessible via VPN par tous les postes Claude Code et Claude Desktop Neoteem. L'API MCP reste identique — les skills existantes marchent sans modification.

## Contraintes

- Zero perte de qualite de recherche vs CLI Obsidian (prouve par benchmark de parite)
- Performance x100 vs CLI (SQLite en memoire vs subprocess CLI)
- Le vault .md reste la source de verite — brain.db est un index jetable recalculable en 5s
- Aucune dependance a Obsidian (ni CLI, ni app desktop) sur le serveur
- Accessible via VPN, configurable via settings orga (Claude Code + Claude Desktop)
- Branches git par utilisateur pour les ecritures MCP

## Architecture

### Repos Bitbucket (2 repos separes)

| Repo | Contenu |
|------|---------|
| `neoteem-brain` | Vault Obsidian (850+ notes .md) |
| `mcp-obsidian-brain` | Service MCP Python (ce repo) |

### Deploiement serveur (VM Linux)

```
/opt/mcp-obsidian-brain/     <- git clone repo MCP
  src/
    server.py                <- FastMCP, mode HTTP, port 8080
    database.py              <- SQLite FTS5, BM25 pondere, snippets natifs
    watcher.py               <- Poll 30s, reindex au changement
    git_sync.py              <- Pull main/5min, commit par user, push/30min
    tools/brain.py           <- 9 tools MCP
  config.yaml                <- Tout configurable
  tests/
    test_database.py
    test_tools.py
    benchmark_parity.py      <- Comparaison CLI vs SQLite
  pyproject.toml

/data/neoteem-brain/         <- git clone repo vault
/data/brain.db               <- Index SQLite (~10 Mo, jetable)
```

### Flux

```
Claude (poste via VPN)
    |
    | HTTPS + header X-User
    v
MCP server (FastMCP HTTP, port 8080)
    |
    +-- search_brain  --> SQLite FTS5 (5ms)
    +-- read_note     --> fichier .md direct (1ms)
    +-- create_note   --> fichier .md + SQLite + git commit mcp/<user>
```

## API MCP — 9 tools

### Lecture (tout le monde)

| Tool | Params | Description |
|------|--------|-------------|
| `search_brain(query, limit, context)` | query: str, limit: int=5, context: bool=True | Recherche FTS5 avec BM25 pondere et snippets natifs |
| `read_note(file)` | file: str | Lit une note par nom OU alias (resolution wikilink) |
| `read_note_by_path(path)` | path: str | Lit une note par chemin exact |
| `get_backlinks(file)` | file: str | Notes qui pointent vers cette note + count |
| `get_tags()` | - | Tous les tags tries par frequence |
| `get_property(file, name)` | file: str, name: str | Lit une propriete du frontmatter |

### Ecriture (admin via la skill appropriee)

| Tool | Params | Description |
|------|--------|-------------|
| `create_note(path, content)` | path: str, content: str | Cree un .md + index + git commit |
| `append_note(file, content)` | file: str, content: str | Append au .md + reindex + git commit |
| `update_property(file, name, value)` | file: str, name: str, value: str | Modifie frontmatter + reindex + git commit |

### Tools supprimes (vs v1)

| Tool | Raison |
|------|--------|
| `daily_read` | Usage perso Obsidian, pas MCP |
| `daily_append` | Idem |
| `get_tasks` | Taches Obsidian != taches metier |

## SQLite FTS5 — Schema

```sql
PRAGMA journal_mode = WAL;  -- Multi-lecteurs simultanes

-- Table principale
CREATE TABLE notes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    file_stem     TEXT NOT NULL,
    path          TEXT UNIQUE NOT NULL,
    content       TEXT NOT NULL,
    frontmatter   TEXT,
    last_modified REAL NOT NULL
);

-- Aliases (resolution wikilink par nom OU alias)
CREATE TABLE aliases (
    note_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    alias    TEXT NOT NULL
);
CREATE INDEX idx_aliases_alias ON aliases(alias);
CREATE INDEX idx_aliases_note ON aliases(note_id);

-- Liens entre notes (backlinks)
CREATE TABLE links (
    source_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    target     TEXT NOT NULL
);
CREATE INDEX idx_links_target ON links(target);
CREATE INDEX idx_links_source ON links(source_id);

-- Tags
CREATE TABLE tags (
    note_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    tag      TEXT NOT NULL
);
CREATE INDEX idx_tags_tag ON tags(tag);

-- Index full-text FTS5
CREATE VIRTUAL TABLE notes_fts USING fts5(
    file_stem,
    content,
    aliases,
    content='notes',
    content_rowid='id',
    tokenize='unicode61 remove_diacritics 2'
);
```

### Requetes cles

**search_brain :**
```sql
SELECT
    n.path,
    n.file_stem,
    snippet(notes_fts, 1, '>>> ', ' <<<', '...', 32) as context,
    bm25(notes_fts, 10.0, 1.0, 8.0) as score
FROM notes_fts
JOIN notes n ON n.id = notes_fts.rowid
WHERE notes_fts MATCH ?
ORDER BY score
LIMIT ?
```

Poids BM25 : file_stem x10, content x1, aliases x8. Le nom et les aliases sont prioritaires sur le contenu brut.

**read_note (resolution alias) :**
```sql
SELECT path FROM notes
WHERE file_stem = ?
UNION
SELECT n.path FROM notes n
JOIN aliases a ON a.note_id = n.id
WHERE a.alias = ?
LIMIT 1
```

**get_backlinks :**
```sql
SELECT n.file_stem, COUNT(*) as count
FROM links l
JOIN notes n ON n.id = l.source_id
WHERE l.target = ?
GROUP BY n.file_stem
ORDER BY count DESC
```

### Tokenizer

`unicode61 remove_diacritics 2` — supprime les accents pour la recherche ("gerance" trouve "gerance"). Pas de stemming (Obsidian n'en fait pas, on veut la parite).

### Prefix matching

`search_brain("encaiss")` → requete `encaiss*` — trouve "encaissement", "encaisser", etc.

## Indexation

### Au demarrage

1. Scanner tous les .md du vault (exclure `.obsidian/`, `.claude/`, `Templates/`, `Daily/`, `plugin/`, `claude-chat-plugins/`, `doc/`)
2. Pour chaque fichier : extraire frontmatter (YAML), aliases, tags, wikilinks `[[...]]`
3. INSERT dans notes, aliases, links, tags, notes_fts
4. Duree : ~5 secondes pour 850 notes

### En continu (watcher.py)

- Poll toutes les 30 secondes : comparer `last_modified` de chaque .md vs valeur en base
- Fichier modifie → reindex cette note uniquement (~5ms)
- Nouveau fichier (apres git pull) → INSERT
- Fichier supprime → DELETE (cascade sur aliases, links, tags, fts)

## Git Sync

### Pull (recuperer les modifs de main)

- Toutes les 5 minutes : `git pull origin main`
- Apres pull : watcher detecte les fichiers modifies et reindexe

### Commit (ecritures MCP)

- A chaque create/append/update : `git add <fichier> && git commit -m "mcp(<user>): <action> <note>"`
- Branche : `mcp/<username>` (une branche par utilisateur)
- Username : header HTTP `X-User` envoye par la skill, ou variable `$USERNAME`

### Push (vers Bitbucket)

- Toutes les 30 minutes : `git push origin mcp/<username>` pour chaque branche active
- Raphael merge `mcp/<username>` dans `main` quand il veut (controle total)

## Identification utilisateur

La skill envoie le `X-User` automatiquement :
- Claude Code : variable `$USERNAME` du systeme
- Claude Desktop : la skill pose la question une fois au premier lancement, memorise en memory project

## Configuration postes

Aucune installation par poste. Configuration via settings orga :
- Claude Code : MCP dans les settings orga
- Claude Desktop : MCP dans les settings orga
- Les skills neoteem-brain-dev/support sont deja installees via les plugins

## Skills a modifier (5 fichiers)

| Skill | Modification |
|-------|-------------|
| `plugin/neoteem-brain-dev/skills/neo-brain/SKILL.md` | Supprimer mode CLI, garder mode MCP |
| `plugin/neoteem-brain-support/skills/neo-brain-support/SKILL.md` | Idem |
| `plugin/neoteem-brain-dev-ia/skills/neo-brain-dev-ia/SKILL.md` | Idem |
| `claude-chat-plugins/neoteem-brain-dev/SKILL.md` | Idem |
| `claude-chat-plugins/neoteem-brain-support/SKILL.md` | Idem |

L'API MCP ne change pas (memes noms de tools, memes parametres). Seules les references a la CLI Obsidian et au wrapper `obsidian-cli.sh` sont supprimees.

## Skill test-brain (benchmark de parite)

Skill dans `neoteem-brain/.claude/skills/test-brain/` :
1. Lit un fichier de requetes de reference `test/queries.yaml` (30-50 requetes reelles)
2. Execute chaque requete sur le MCP
3. Compare les top-5 resultats aux resultats attendus (golden set capture une fois depuis la CLI)
4. Affiche le score de parite et les ecarts
5. **Gate : overlap >= 80% sur les top-5** → OK pour prod

Le golden set est capture AVANT la migration depuis la CLI Obsidian actuelle.

## Config serveur

`config.yaml` :
```yaml
vault_path: /data/neoteem-brain
db_path: /data/brain.db
port: 8080

git:
  pull_interval_seconds: 300
  push_interval_seconds: 1800
  remote: origin
  main_branch: main

watcher:
  poll_interval_seconds: 30

fts:
  weights:
    file_stem: 10.0
    content: 1.0
    aliases: 8.0

excluded_dirs:
  - .obsidian
  - .claude
  - Templates
  - Daily
  - plugin
  - claude-chat-plugins
  - doc
  - mcp-obsidian-brain
```

## Fiche devops

- VM Linux, Python 3.11+, git
- Port 8080 entrant (HTTPS via reverse proxy)
- Port 22 entrant (SSH admin)
- Port 443 sortant (git push Bitbucket)
- Accessible via VPN
- Service systemd pour le MCP (auto-restart)

## Dependances Python

```
fastmcp>=2.0
pyyaml
```

Pas de dependance lourde. SQLite est integre a Python (module `sqlite3`).

## Risques et mitigations

| Risque | Mitigation |
|--------|-----------|
| Perte brain.db | Jetable, reconstruit en 5s au redemarrage |
| Crash MCP | Service systemd avec auto-restart |
| Conflit git branches | Une branche par user, jamais de conflit |
| Qualite recherche inferieure a CLI | Benchmark de parite obligatoire avant prod |
| Vault corrompu | 3 copies : serveur + Bitbucket + poste Raphael |
