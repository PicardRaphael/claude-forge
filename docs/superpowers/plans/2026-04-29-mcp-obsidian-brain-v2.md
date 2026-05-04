# MCP Obsidian Brain v2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Obsidian CLI dependency with SQLite FTS5 index, serve MCP over HTTP from a server VM.

**Architecture:** FastMCP HTTP server backed by SQLite FTS5 for search, direct filesystem reads for note content, git sync per-user branches for writes. Config via YAML, watcher polls for changes.

**Tech Stack:** Python 3.11+, FastMCP 2.x, SQLite FTS5, PyYAML, pytest

**Repo:** `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/mcp-obsidian-brain/`

**Spec:** `docs/superpowers/specs/2026-04-29-mcp-obsidian-brain-v2-design.md`

---

## File Structure

```
mcp-obsidian-brain/
  pyproject.toml              <- dependencies + entry point
  config.yaml                 <- vault path, port, git intervals, FTS weights
  src/
    __init__.py
    server.py                 <- FastMCP app, HTTP mode, startup hooks
    config.py                 <- Load + validate config.yaml
    database.py               <- SQLite FTS5: create schema, index, search, resolve
    indexer.py                <- Parse .md files: frontmatter, aliases, tags, wikilinks
    watcher.py                <- Poll filesystem, detect changes, trigger reindex
    git_sync.py               <- Pull main, commit per-user branch, push on schedule
    tools/
      __init__.py
      brain.py                <- 9 MCP tools (search, read, backlinks, tags, write)
  tests/
    __init__.py
    conftest.py               <- Shared fixtures (temp vault, test db)
    test_indexer.py            <- Parse frontmatter, aliases, tags, wikilinks
    test_database.py           <- Schema, search, resolve, backlinks
    test_tools.py              <- MCP tools integration tests
    test_watcher.py            <- File change detection
    test_git_sync.py           <- Git operations
    benchmark_parity.py        <- CLI vs SQLite comparison script
  test/
    queries.yaml               <- Golden set queries for parity benchmark
```

---

### Task 1: Project setup + config loader

**Files:**
- Modify: `pyproject.toml`
- Create: `config.yaml`
- Create: `src/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write test for config loading**

```python
# tests/test_config.py
import pytest
from pathlib import Path


def test_load_config_from_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "vault_path: /data/neoteem-brain\n"
        "db_path: /data/brain.db\n"
        "port: 8080\n"
        "git:\n"
        "  pull_interval_seconds: 300\n"
        "  push_interval_seconds: 1800\n"
        "  remote: origin\n"
        "  main_branch: main\n"
        "watcher:\n"
        "  poll_interval_seconds: 30\n"
        "fts:\n"
        "  weights:\n"
        "    file_stem: 10.0\n"
        "    content: 1.0\n"
        "    aliases: 8.0\n"
        "excluded_dirs:\n"
        "  - .obsidian\n"
        "  - .claude\n"
        "  - Templates\n"
    )
    from src.config import load_config

    cfg = load_config(config_file)
    assert cfg.vault_path == Path("/data/neoteem-brain")
    assert cfg.db_path == Path("/data/brain.db")
    assert cfg.port == 8080
    assert cfg.git.pull_interval_seconds == 300
    assert cfg.fts.weights.file_stem == 10.0
    assert ".obsidian" in cfg.excluded_dirs


def test_load_config_missing_file():
    from src.config import load_config

    with pytest.raises(FileNotFoundError):
        load_config(Path("/nonexistent/config.yaml"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/mcp-obsidian-brain && python -m pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.config'`

- [ ] **Step 3: Update pyproject.toml**

```toml
[project]
name = "mcp-obsidian-brain"
version = "2.0.0"
description = "MCP server for neoteem-brain vault — SQLite FTS5 backed, HTTP mode"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=2.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]

[project.scripts]
mcp-obsidian-brain = "src.server:main"
```

- [ ] **Step 4: Write config.py**

```python
# src/config.py
"""Load and validate config.yaml."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class GitConfig:
    pull_interval_seconds: int = 300
    push_interval_seconds: int = 1800
    remote: str = "origin"
    main_branch: str = "main"


@dataclass
class WatcherConfig:
    poll_interval_seconds: int = 30


@dataclass
class FTSWeights:
    file_stem: float = 10.0
    content: float = 1.0
    aliases: float = 8.0


@dataclass
class FTSConfig:
    weights: FTSWeights = field(default_factory=FTSWeights)


@dataclass
class AppConfig:
    vault_path: Path = field(default_factory=lambda: Path("/data/neoteem-brain"))
    db_path: Path = field(default_factory=lambda: Path("/data/brain.db"))
    port: int = 8080
    git: GitConfig = field(default_factory=GitConfig)
    watcher: WatcherConfig = field(default_factory=WatcherConfig)
    fts: FTSConfig = field(default_factory=FTSConfig)
    excluded_dirs: list[str] = field(
        default_factory=lambda: [
            ".obsidian", ".claude", "Templates", "Daily",
            "plugin", "claude-chat-plugins", "doc", "mcp-obsidian-brain",
        ]
    )


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        raw = yaml.safe_load(f)
    git_raw = raw.get("git", {})
    watcher_raw = raw.get("watcher", {})
    fts_raw = raw.get("fts", {})
    weights_raw = fts_raw.get("weights", {})
    return AppConfig(
        vault_path=Path(raw["vault_path"]),
        db_path=Path(raw["db_path"]),
        port=raw.get("port", 8080),
        git=GitConfig(**git_raw),
        watcher=WatcherConfig(**watcher_raw),
        fts=FTSConfig(weights=FTSWeights(**weights_raw)),
        excluded_dirs=raw.get("excluded_dirs", AppConfig.excluded_dirs),
    )
```

- [ ] **Step 5: Write config.yaml**

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

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_config.py -v`
Expected: 2 PASSED

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml config.yaml src/config.py tests/test_config.py
git commit -m "feat: config loader with dataclasses + YAML"
```

---

### Task 2: Markdown indexer (parse frontmatter, aliases, tags, wikilinks)

**Files:**
- Create: `src/indexer.py`
- Create: `tests/test_indexer.py`

- [ ] **Step 1: Write tests for frontmatter parsing**

```python
# tests/test_indexer.py
import pytest
from src.indexer import parse_note


SAMPLE_NOTE = """---
titre: Charges de copropriete
aliases:
  - charges CC
  - appels de fonds
tags:
  - domaine/syndic
  - type/concept
derniere-maj: 2026-04-15
---

# Charges de copropriete

Les charges sont reparties entre les [[coproprietaire]]s selon les [[tantieme]]s.

## Calcul

La fonction [[f_calc_charges]] effectue le calcul.
"""


def test_parse_frontmatter():
    result = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", SAMPLE_NOTE)
    assert result.file_stem == "charges-copropriete"
    assert result.path == "01-Domaines/charges-copropriete.md"
    assert result.frontmatter_raw.startswith("titre:")
    assert result.aliases == ["charges CC", "appels de fonds"]
    assert result.tags == ["domaine/syndic", "type/concept"]


def test_parse_wikilinks():
    result = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", SAMPLE_NOTE)
    assert set(result.wikilinks) == {"coproprietaire", "tantieme", "f_calc_charges"}


def test_parse_note_no_frontmatter():
    content = "# Simple note\n\nJust some content with a [[link]].\n"
    result = parse_note("simple", "simple.md", content)
    assert result.aliases == []
    assert result.tags == []
    assert result.wikilinks == ["link"]


def test_parse_aliases_string_format():
    content = "---\naliases: single-alias\n---\n\nContent.\n"
    result = parse_note("test", "test.md", content)
    assert result.aliases == ["single-alias"]


def test_parse_wikilinks_with_display_text():
    content = "See [[bail|le bail en cours]] and [[lot]].\n"
    result = parse_note("test", "test.md", content)
    assert set(result.wikilinks) == {"bail", "lot"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_indexer.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.indexer'`

- [ ] **Step 3: Write indexer.py**

```python
# src/indexer.py
"""Parse Obsidian .md files: frontmatter, aliases, tags, wikilinks."""

import re
from dataclasses import dataclass, field

import yaml


@dataclass
class ParsedNote:
    file_stem: str
    path: str
    content: str
    frontmatter_raw: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def parse_note(file_stem: str, path: str, content: str) -> ParsedNote:
    frontmatter_raw = ""
    aliases: list[str] = []
    tags: list[str] = []

    fm_match = _FRONTMATTER_RE.match(content)
    if fm_match:
        frontmatter_raw = fm_match.group(1)
        try:
            fm = yaml.safe_load(frontmatter_raw)
            if isinstance(fm, dict):
                raw_aliases = fm.get("aliases", [])
                if isinstance(raw_aliases, str):
                    aliases = [raw_aliases]
                elif isinstance(raw_aliases, list):
                    aliases = [str(a) for a in raw_aliases]

                raw_tags = fm.get("tags", [])
                if isinstance(raw_tags, str):
                    tags = [raw_tags]
                elif isinstance(raw_tags, list):
                    tags = [str(t) for t in raw_tags]
        except yaml.YAMLError:
            pass

    wikilinks = _WIKILINK_RE.findall(content)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_links: list[str] = []
    for link in wikilinks:
        link_stem = link.strip()
        if link_stem not in seen:
            seen.add(link_stem)
            unique_links.append(link_stem)

    return ParsedNote(
        file_stem=file_stem,
        path=path,
        content=content,
        frontmatter_raw=frontmatter_raw,
        aliases=aliases,
        tags=tags,
        wikilinks=unique_links,
    )
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_indexer.py -v`
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/indexer.py tests/test_indexer.py
git commit -m "feat: markdown indexer — parse frontmatter, aliases, tags, wikilinks"
```

---

### Task 3: SQLite FTS5 database (schema + CRUD + search)

**Files:**
- Create: `src/database.py`
- Create: `tests/test_database.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write shared fixtures**

```python
# tests/conftest.py
import pytest
from pathlib import Path
from src.database import BrainDB
from src.config import FTSWeights


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test.db"
    brain = BrainDB(db_path, FTSWeights())
    brain.create_schema()
    yield brain
    brain.close()


@pytest.fixture
def vault(tmp_path):
    vault_dir = tmp_path / "vault"
    vault_dir.mkdir()
    note1 = vault_dir / "01-Domaines"
    note1.mkdir()
    (note1 / "charges-copropriete.md").write_text(
        "---\ntitre: Charges\naliases:\n  - charges CC\n  - appels de fonds\n"
        "tags:\n  - domaine/syndic\n---\n\n# Charges\n\nLes [[coproprietaire]]s paient.\n",
        encoding="utf-8",
    )
    (note1 / "bail.md").write_text(
        "---\ntitre: Bail\naliases:\n  - contrat de location\ntags:\n  - domaine/gerance\n"
        "---\n\n# Bail\n\nLe bail lie le [[proprietaire]] et le [[locataire]].\n"
        "Voir aussi les [[charges-copropriete]].\n",
        encoding="utf-8",
    )
    (note1 / "coproprietaire.md").write_text(
        "---\ntitre: Coproprietaire\ntags:\n  - domaine/syndic\n---\n\n# Coproprietaire\n",
        encoding="utf-8",
    )
    return vault_dir
```

- [ ] **Step 2: Write database tests**

```python
# tests/test_database.py
import pytest
from src.database import BrainDB
from src.indexer import parse_note


def test_create_schema(db):
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    names = {row[0] for row in tables}
    assert "notes" in names
    assert "aliases" in names
    assert "links" in names
    assert "tags" in names
    assert "notes_fts" in names


def test_index_and_search(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    results = db.search("charges", limit=5)
    assert len(results) >= 1
    assert results[0]["file_stem"] == "charges-copropriete"


def test_search_by_alias(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    results = db.search("appels de fonds", limit=5)
    assert len(results) >= 1
    assert results[0]["file_stem"] == "charges-copropriete"


def test_resolve_by_name(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    path = db.resolve_note("charges-copropriete")
    assert path == "01-Domaines/charges-copropriete.md"


def test_resolve_by_alias(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    path = db.resolve_note("charges CC")
    assert path == "01-Domaines/charges-copropriete.md"


def test_resolve_unknown_returns_none(db):
    path = db.resolve_note("nonexistent")
    assert path is None


def test_backlinks(db, vault):
    for name in ["charges-copropriete", "bail", "coproprietaire"]:
        content = (vault / "01-Domaines" / f"{name}.md").read_text(encoding="utf-8")
        parsed = parse_note(name, f"01-Domaines/{name}.md", content)
        db.index_note(parsed, 1000.0)

    backlinks = db.get_backlinks("charges-copropriete")
    assert any(bl["file_stem"] == "bail" for bl in backlinks)


def test_get_tags(db, vault):
    for name in ["charges-copropriete", "bail", "coproprietaire"]:
        content = (vault / "01-Domaines" / f"{name}.md").read_text(encoding="utf-8")
        parsed = parse_note(name, f"01-Domaines/{name}.md", content)
        db.index_note(parsed, 1000.0)

    tags = db.get_tags()
    tag_names = [t["tag"] for t in tags]
    assert "domaine/syndic" in tag_names


def test_delete_note(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    db.delete_note("01-Domaines/charges-copropriete.md")
    assert db.resolve_note("charges-copropriete") is None
    assert db.resolve_note("charges CC") is None


def test_prefix_search(db, vault):
    content = (vault / "01-Domaines" / "charges-copropriete.md").read_text(encoding="utf-8")
    parsed = parse_note("charges-copropriete", "01-Domaines/charges-copropriete.md", content)
    db.index_note(parsed, 1000.0)

    results = db.search("charg", limit=5)
    assert len(results) >= 1
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python -m pytest tests/test_database.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.database'`

- [ ] **Step 4: Write database.py**

```python
# src/database.py
"""SQLite FTS5 database for neoteem-brain vault index."""

import sqlite3
from pathlib import Path
from src.config import FTSWeights
from src.indexer import ParsedNote


class BrainDB:
    def __init__(self, db_path: Path, weights: FTSWeights):
        self._path = db_path
        self._weights = weights
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")

    def create_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS notes (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                file_stem     TEXT NOT NULL,
                path          TEXT UNIQUE NOT NULL,
                content       TEXT NOT NULL,
                frontmatter   TEXT,
                last_modified REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS aliases (
                note_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
                alias    TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_aliases_alias ON aliases(alias);
            CREATE INDEX IF NOT EXISTS idx_aliases_note ON aliases(note_id);

            CREATE TABLE IF NOT EXISTS links (
                source_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
                target     TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_links_target ON links(target);
            CREATE INDEX IF NOT EXISTS idx_links_source ON links(source_id);

            CREATE TABLE IF NOT EXISTS tags (
                note_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
                tag      TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);
        """)
        # FTS5 table — created separately (no IF NOT EXISTS for virtual tables in some SQLite versions)
        try:
            self._conn.execute("""
                CREATE VIRTUAL TABLE notes_fts USING fts5(
                    file_stem,
                    content,
                    aliases,
                    tokenize='unicode61 remove_diacritics 2'
                )
            """)
        except sqlite3.OperationalError:
            pass  # Already exists
        self._conn.commit()

    def index_note(self, note: ParsedNote, last_modified: float):
        cur = self._conn.cursor()
        # Delete existing if re-indexing
        cur.execute("SELECT id FROM notes WHERE path = ?", (note.path,))
        existing = cur.fetchone()
        if existing:
            self._delete_by_id(existing[0])

        cur.execute(
            "INSERT INTO notes (file_stem, path, content, frontmatter, last_modified) VALUES (?, ?, ?, ?, ?)",
            (note.file_stem, note.path, note.content, note.frontmatter_raw, last_modified),
        )
        note_id = cur.lastrowid

        aliases_joined = " ".join(note.aliases)
        cur.execute(
            "INSERT INTO notes_fts (rowid, file_stem, content, aliases) VALUES (?, ?, ?, ?)",
            (note_id, note.file_stem, note.content, aliases_joined),
        )

        for alias in note.aliases:
            cur.execute("INSERT INTO aliases (note_id, alias) VALUES (?, ?)", (note_id, alias))

        for link in note.wikilinks:
            cur.execute("INSERT INTO links (source_id, target) VALUES (?, ?)", (note_id, link))

        for tag in note.tags:
            cur.execute("INSERT INTO tags (note_id, tag) VALUES (?, ?)", (note_id, tag))

        self._conn.commit()

    def search(self, query: str, limit: int = 5, context: bool = True) -> list[dict]:
        fts_query = " ".join(f"{term}*" for term in query.split())
        w = self._weights
        if context:
            sql = """
                SELECT
                    n.path,
                    n.file_stem,
                    snippet(notes_fts, 1, '>>> ', ' <<<', '...', 32) as context,
                    bm25(notes_fts, ?, ?, ?) as score
                FROM notes_fts
                JOIN notes n ON n.id = notes_fts.rowid
                WHERE notes_fts MATCH ?
                ORDER BY score
                LIMIT ?
            """
            rows = self._conn.execute(sql, (w.file_stem, w.content, w.aliases, fts_query, limit)).fetchall()
        else:
            sql = """
                SELECT
                    n.path,
                    n.file_stem,
                    bm25(notes_fts, ?, ?, ?) as score
                FROM notes_fts
                JOIN notes n ON n.id = notes_fts.rowid
                WHERE notes_fts MATCH ?
                ORDER BY score
                LIMIT ?
            """
            rows = self._conn.execute(sql, (w.file_stem, w.content, w.aliases, fts_query, limit)).fetchall()
        return [dict(row) for row in rows]

    def resolve_note(self, name: str) -> str | None:
        row = self._conn.execute(
            "SELECT path FROM notes WHERE file_stem = ? "
            "UNION "
            "SELECT n.path FROM notes n JOIN aliases a ON a.note_id = n.id WHERE a.alias = ? "
            "LIMIT 1",
            (name, name),
        ).fetchone()
        return row[0] if row else None

    def get_backlinks(self, file_stem: str) -> list[dict]:
        rows = self._conn.execute(
            "SELECT n.file_stem, COUNT(*) as count "
            "FROM links l "
            "JOIN notes n ON n.id = l.source_id "
            "WHERE l.target = ? "
            "GROUP BY n.file_stem "
            "ORDER BY count DESC",
            (file_stem,),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_tags(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT tag, COUNT(*) as count FROM tags GROUP BY tag ORDER BY count DESC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_property(self, file_stem: str, name: str) -> str | None:
        import yaml
        row = self._conn.execute(
            "SELECT frontmatter FROM notes WHERE file_stem = ? "
            "UNION "
            "SELECT n.frontmatter FROM notes n JOIN aliases a ON a.note_id = n.id WHERE a.alias = ? "
            "LIMIT 1",
            (file_stem, file_stem),
        ).fetchone()
        if not row or not row[0]:
            return None
        try:
            fm = yaml.safe_load(row[0])
            return str(fm.get(name, "")) if isinstance(fm, dict) else None
        except yaml.YAMLError:
            return None

    def get_last_modified(self, path: str) -> float | None:
        row = self._conn.execute(
            "SELECT last_modified FROM notes WHERE path = ?", (path,)
        ).fetchone()
        return row[0] if row else None

    def delete_note(self, path: str):
        row = self._conn.execute("SELECT id FROM notes WHERE path = ?", (path,)).fetchone()
        if row:
            self._delete_by_id(row[0])
            self._conn.commit()

    def _delete_by_id(self, note_id: int):
        self._conn.execute("DELETE FROM notes_fts WHERE rowid = ?", (note_id,))
        self._conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    def execute(self, sql: str, params=()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def close(self):
        self._conn.close()
```

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/test_database.py -v`
Expected: 10 PASSED

- [ ] **Step 6: Commit**

```bash
git add src/database.py tests/conftest.py tests/test_database.py
git commit -m "feat: SQLite FTS5 database — schema, index, search, resolve, backlinks"
```

---

### Task 4: File watcher (detect changes, trigger reindex)

**Files:**
- Create: `src/watcher.py`
- Create: `tests/test_watcher.py`

- [ ] **Step 1: Write watcher tests**

```python
# tests/test_watcher.py
import time
from pathlib import Path
from src.watcher import VaultWatcher
from src.database import BrainDB
from src.config import FTSWeights


def test_initial_scan(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    watcher = VaultWatcher(vault, db, excluded_dirs=[".obsidian"])

    changes = watcher.scan()
    assert changes.added >= 3  # charges-copropriete, bail, coproprietaire
    assert changes.modified == 0
    assert changes.deleted == 0
    db.close()


def test_detect_modified_file(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    watcher = VaultWatcher(vault, db, excluded_dirs=[".obsidian"])

    watcher.scan()  # Initial
    time.sleep(0.1)
    # Modify a file
    note = vault / "01-Domaines" / "charges-copropriete.md"
    note.write_text(note.read_text(encoding="utf-8") + "\nNouvelle ligne.", encoding="utf-8")

    changes = watcher.scan()
    assert changes.modified >= 1
    db.close()


def test_detect_new_file(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    watcher = VaultWatcher(vault, db, excluded_dirs=[".obsidian"])

    watcher.scan()  # Initial
    # Add a new file
    (vault / "01-Domaines" / "new-note.md").write_text("# New\n\nContent.\n", encoding="utf-8")

    changes = watcher.scan()
    assert changes.added >= 1
    db.close()


def test_detect_deleted_file(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    watcher = VaultWatcher(vault, db, excluded_dirs=[".obsidian"])

    watcher.scan()  # Initial
    # Delete a file
    (vault / "01-Domaines" / "coproprietaire.md").unlink()

    changes = watcher.scan()
    assert changes.deleted >= 1
    db.close()


def test_excluded_dirs(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    excluded = vault / ".obsidian"
    excluded.mkdir()
    (excluded / "config.md").write_text("# Config\n", encoding="utf-8")
    watcher = VaultWatcher(vault, db, excluded_dirs=[".obsidian"])

    changes = watcher.scan()
    # Should not index .obsidian/config.md
    assert db.resolve_note("config") is None
    db.close()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_watcher.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.watcher'`

- [ ] **Step 3: Write watcher.py**

```python
# src/watcher.py
"""Poll filesystem for .md changes, trigger reindex."""

from dataclasses import dataclass
from pathlib import Path
from src.database import BrainDB
from src.indexer import parse_note


@dataclass
class ScanResult:
    added: int = 0
    modified: int = 0
    deleted: int = 0


class VaultWatcher:
    def __init__(self, vault_path: Path, db: BrainDB, excluded_dirs: list[str]):
        self._vault = vault_path
        self._db = db
        self._excluded = set(excluded_dirs)

    def _iter_notes(self):
        for md_file in self._vault.rglob("*.md"):
            rel = md_file.relative_to(self._vault)
            if any(part in self._excluded for part in rel.parts):
                continue
            yield md_file, str(rel).replace("\\", "/")

    def scan(self) -> ScanResult:
        result = ScanResult()
        seen_paths: set[str] = set()

        for md_file, rel_path in self._iter_notes():
            seen_paths.add(rel_path)
            file_mtime = md_file.stat().st_mtime
            db_mtime = self._db.get_last_modified(rel_path)

            if db_mtime is None:
                self._index_file(md_file, rel_path, file_mtime)
                result.added += 1
            elif file_mtime > db_mtime:
                self._index_file(md_file, rel_path, file_mtime)
                result.modified += 1

        # Detect deleted files
        all_db_paths = {
            row[0]
            for row in self._db.execute("SELECT path FROM notes").fetchall()
        }
        for db_path in all_db_paths - seen_paths:
            self._db.delete_note(db_path)
            result.deleted += 1

        return result

    def _index_file(self, md_file: Path, rel_path: str, mtime: float):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        file_stem = md_file.stem
        parsed = parse_note(file_stem, rel_path, content)
        self._db.index_note(parsed, mtime)
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_watcher.py -v`
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/watcher.py tests/test_watcher.py
git commit -m "feat: vault watcher — poll filesystem, detect add/modify/delete, reindex"
```

---

### Task 5: Git sync (pull, commit per-user, push)

**Files:**
- Create: `src/git_sync.py`
- Create: `tests/test_git_sync.py`

- [ ] **Step 1: Write git sync tests**

```python
# tests/test_git_sync.py
import subprocess
from pathlib import Path
from src.git_sync import GitSync
from src.config import GitConfig


def _init_repo(path: Path) -> Path:
    subprocess.run(["git", "init", str(path)], capture_output=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "test@test.com"], capture_output=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "Test"], capture_output=True)
    (path / "README.md").write_text("# Test\n")
    subprocess.run(["git", "-C", str(path), "add", "."], capture_output=True)
    subprocess.run(["git", "-C", str(path), "commit", "-m", "init"], capture_output=True)
    return path


def test_commit_on_branch(tmp_path):
    repo = _init_repo(tmp_path / "vault")
    cfg = GitConfig(remote="origin", main_branch="main")
    sync = GitSync(repo, cfg)

    (repo / "new-note.md").write_text("# New\n")
    sync.commit_file("new-note.md", "raphael", "create", "new-note")

    result = subprocess.run(
        ["git", "-C", str(repo), "branch"],
        capture_output=True, text=True,
    )
    assert "mcp/raphael" in result.stdout


def test_commit_message_format(tmp_path):
    repo = _init_repo(tmp_path / "vault")
    cfg = GitConfig(remote="origin", main_branch="main")
    sync = GitSync(repo, cfg)

    (repo / "test.md").write_text("# Test\n")
    sync.commit_file("test.md", "julie", "append", "test")

    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--oneline", "-1"],
        capture_output=True, text=True,
    )
    assert "mcp(julie): append test" in result.stdout


def test_two_users_different_branches(tmp_path):
    repo = _init_repo(tmp_path / "vault")
    cfg = GitConfig(remote="origin", main_branch="main")
    sync = GitSync(repo, cfg)

    (repo / "note-a.md").write_text("# A\n")
    sync.commit_file("note-a.md", "raphael", "create", "note-a")

    (repo / "note-b.md").write_text("# B\n")
    sync.commit_file("note-b.md", "julie", "create", "note-b")

    result = subprocess.run(
        ["git", "-C", str(repo), "branch"],
        capture_output=True, text=True,
    )
    assert "mcp/raphael" in result.stdout
    assert "mcp/julie" in result.stdout
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_git_sync.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.git_sync'`

- [ ] **Step 3: Write git_sync.py**

```python
# src/git_sync.py
"""Git operations: pull main, commit per-user branch, push on schedule."""

import subprocess
from pathlib import Path
from src.config import GitConfig


class GitSync:
    def __init__(self, vault_path: Path, config: GitConfig):
        self._vault = vault_path
        self._cfg = config
        self._active_branches: set[str] = set()

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self._vault), *args],
            capture_output=True,
            text=True,
            timeout=60,
        )

    def pull(self):
        self._git("checkout", self._cfg.main_branch)
        self._git("pull", self._cfg.remote, self._cfg.main_branch)

    def commit_file(self, rel_path: str, username: str, action: str, note_name: str):
        branch = f"mcp/{username}"
        self._active_branches.add(branch)

        # Create branch from main if it doesn't exist
        result = self._git("branch", "--list", branch)
        if branch not in result.stdout:
            self._git("branch", branch, self._cfg.main_branch)

        self._git("checkout", branch)
        self._git("add", rel_path)
        self._git("commit", "-m", f"mcp({username}): {action} {note_name}")

    def push_all(self):
        current = self._git("branch", "--show-current").stdout.strip()
        for branch in self._active_branches:
            self._git("push", self._cfg.remote, branch)
        if current:
            self._git("checkout", current)

    def get_active_branches(self) -> set[str]:
        return self._active_branches.copy()
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_git_sync.py -v`
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/git_sync.py tests/test_git_sync.py
git commit -m "feat: git sync — pull main, commit per-user branch, push schedule"
```

---

### Task 6: MCP tools (9 tools, brain.py rewrite)

**Files:**
- Modify: `src/tools/brain.py`
- Create: `tests/test_tools.py`

- [ ] **Step 1: Write tools integration tests**

```python
# tests/test_tools.py
import pytest
from pathlib import Path
from src.database import BrainDB
from src.config import FTSWeights, GitConfig, AppConfig
from src.watcher import VaultWatcher
from src.tools.brain import BrainTools


@pytest.fixture
def brain_tools(vault, tmp_path):
    db = BrainDB(tmp_path / "test.db", FTSWeights())
    db.create_schema()
    watcher = VaultWatcher(vault, db, excluded_dirs=[])
    watcher.scan()
    tools = BrainTools(db, vault)
    yield tools
    db.close()


def test_search_brain(brain_tools):
    result = brain_tools.search_brain("charges", limit=5, context=True)
    assert "charges-copropriete" in result


def test_read_note_by_name(brain_tools):
    result = brain_tools.read_note("charges-copropriete")
    assert "Charges" in result


def test_read_note_by_alias(brain_tools):
    result = brain_tools.read_note("charges CC")
    assert "Charges" in result


def test_read_note_not_found(brain_tools):
    result = brain_tools.read_note("nonexistent")
    assert "introuvable" in result.lower() or "not found" in result.lower()


def test_read_note_by_path(brain_tools):
    result = brain_tools.read_note_by_path("01-Domaines/bail.md")
    assert "Bail" in result


def test_get_backlinks(brain_tools):
    result = brain_tools.get_backlinks("charges-copropriete")
    assert "bail" in result


def test_get_tags(brain_tools):
    result = brain_tools.get_tags()
    assert "domaine/syndic" in result


def test_get_property(brain_tools):
    result = brain_tools.get_property("charges-copropriete", "titre")
    assert "Charges" in result


def test_create_note(brain_tools, vault):
    content = "---\ntitre: Test\n---\n\n# Test\n\nContenu.\n"
    result = brain_tools.create_note("test-note.md", content)
    assert "cree" in result.lower() or "created" in result.lower()
    assert (vault / "test-note.md").exists()


def test_append_note(brain_tools, vault):
    result = brain_tools.append_note("bail", "\n## Nouveau\n\nAjout.\n")
    content = (vault / "01-Domaines" / "bail.md").read_text(encoding="utf-8")
    assert "Nouveau" in content


def test_update_property(brain_tools, vault):
    result = brain_tools.update_property("bail", "derniere-maj", "2026-04-29")
    content = (vault / "01-Domaines" / "bail.md").read_text(encoding="utf-8")
    assert "2026-04-29" in content
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_tools.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.tools.brain'` or ImportError

- [ ] **Step 3: Write brain.py (tools layer)**

```python
# src/tools/brain.py
"""MCP tools for neoteem-brain vault — backed by SQLite FTS5."""

import re
from pathlib import Path
from src.database import BrainDB
from src.indexer import parse_note

import yaml


class BrainTools:
    def __init__(self, db: BrainDB, vault_path: Path, git_sync=None):
        self._db = db
        self._vault = vault_path
        self._git = git_sync

    def search_brain(self, query: str, limit: int = 5, context: bool = True) -> str:
        results = self._db.search(query, limit=limit, context=context)
        if not results:
            return f"Aucun resultat pour '{query}'."
        lines = []
        for r in results:
            if context and r.get("context"):
                lines.append(f"### {r['file_stem']} ({r['path']})\n{r['context']}\n")
            else:
                lines.append(f"- {r['file_stem']} ({r['path']})")
        return "\n".join(lines)

    def read_note(self, file: str) -> str:
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable (ni par nom, ni par alias)."
        full_path = self._vault / path
        if not full_path.exists():
            return f"Note '{file}' indexee mais fichier manquant: {path}"
        return full_path.read_text(encoding="utf-8", errors="replace")

    def read_note_by_path(self, path: str) -> str:
        full_path = self._vault / path
        if not full_path.exists():
            return f"Fichier introuvable: {path}"
        return full_path.read_text(encoding="utf-8", errors="replace")

    def get_backlinks(self, file: str) -> str:
        backlinks = self._db.get_backlinks(file)
        if not backlinks:
            return f"Aucun backlink vers '{file}'."
        lines = [f"- {bl['file_stem']} ({bl['count']} liens)" for bl in backlinks]
        return "\n".join(lines)

    def get_tags(self) -> str:
        tags = self._db.get_tags()
        if not tags:
            return "Aucun tag dans le vault."
        lines = [f"- {t['tag']} ({t['count']})" for t in tags]
        return "\n".join(lines)

    def get_property(self, file: str, name: str) -> str:
        value = self._db.get_property(file, name)
        if value is None:
            return f"Propriete '{name}' introuvable pour '{file}'."
        return value

    def create_note(self, path: str, content: str, username: str = "anonymous") -> str:
        full_path = self._vault / path
        if full_path.exists():
            return f"Note existe deja: {path}"
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git:
            self._git.commit_file(path, username, "create", full_path.stem)
        return f"Note creee: {path}"

    def append_note(self, file: str, content: str, username: str = "anonymous") -> str:
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(content)
        new_content = full_path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_note(full_path.stem, path, new_content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git:
            self._git.commit_file(path, username, "append", full_path.stem)
        return f"Contenu ajoute a: {path}"

    def update_property(self, file: str, name: str, value: str, username: str = "anonymous") -> str:
        path = self._db.resolve_note(file)
        if not path:
            return f"Note '{file}' introuvable."
        full_path = self._vault / path
        content = full_path.read_text(encoding="utf-8", errors="replace")

        fm_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
        fm_match = fm_re.match(content)
        if fm_match:
            try:
                fm = yaml.safe_load(fm_match.group(1))
                if not isinstance(fm, dict):
                    fm = {}
            except yaml.YAMLError:
                fm = {}
            fm[name] = value
            new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            content = f"---\n{new_fm}\n---\n{content[fm_match.end():]}"
        else:
            fm = {name: value}
            new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            content = f"---\n{new_fm}\n---\n\n{content}"

        full_path.write_text(content, encoding="utf-8")
        parsed = parse_note(full_path.stem, path, content)
        self._db.index_note(parsed, full_path.stat().st_mtime)
        if self._git:
            self._git.commit_file(path, username, "update", full_path.stem)
        return f"Propriete '{name}' mise a jour dans: {path}"


def register_tools(mcp, tools: BrainTools):
    """Register all brain tools on the MCP server."""

    @mcp.tool()
    def search_brain(query: str, limit: int = 5, context: bool = True) -> str:
        """Recherche dans le vault neoteem-brain.

        Args:
            query: terme de recherche (ex: "charges copropriete", "f_calc_charges")
            limit: nombre max de resultats (default 5)
            context: si True, retourne les lignes autour de chaque match
        """
        return tools.search_brain(query, limit, context)

    @mcp.tool()
    def read_note(file: str) -> str:
        """Lit une note par son nom ou alias (resolution wikilink).

        Args:
            file: nom de la note ou alias (ex: "charges-copropriete", "charges CC")
        """
        return tools.read_note(file)

    @mcp.tool()
    def read_note_by_path(path: str) -> str:
        """Lit une note par son chemin exact dans le vault.

        Args:
            path: chemin relatif (ex: "02-BDD/tables/t-acteur.md")
        """
        return tools.read_note_by_path(path)

    @mcp.tool()
    def get_backlinks(file: str) -> str:
        """Liste les notes qui pointent vers cette note.

        Args:
            file: nom de la note sans chemin ni extension
        """
        return tools.get_backlinks(file)

    @mcp.tool()
    def get_tags() -> str:
        """Liste tous les tags du vault tries par frequence."""
        return tools.get_tags()

    @mcp.tool()
    def get_property(file: str, name: str) -> str:
        """Lit une propriete du frontmatter YAML d'une note.

        Args:
            file: nom de la note ou alias
            name: nom de la propriete (ex: "derniere-maj")
        """
        return tools.get_property(file, name)

    @mcp.tool()
    def create_note(path: str, content: str) -> str:
        """Cree une nouvelle note dans le vault.

        Args:
            path: chemin relatif (ex: "07-Support/faq/faq-sujet.md")
            content: contenu complet (frontmatter YAML + body markdown)
        """
        return tools.create_note(path, content)

    @mcp.tool()
    def append_note(file: str, content: str) -> str:
        """Ajoute du contenu a la fin d'une note existante.

        Args:
            file: nom de la note ou alias
            content: contenu markdown a ajouter
        """
        return tools.append_note(file, content)

    @mcp.tool()
    def update_property(file: str, name: str, value: str) -> str:
        """Modifie une propriete du frontmatter YAML d'une note.

        Args:
            file: nom de la note ou alias
            name: nom de la propriete
            value: nouvelle valeur
        """
        return tools.update_property(file, name, value)
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_tools.py -v`
Expected: 11 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/tools/brain.py tests/test_tools.py
git commit -m "feat: 9 MCP tools — search, read, backlinks, tags, property, create, append, update"
```

---

### Task 7: Server (FastMCP HTTP + startup + watcher loop)

**Files:**
- Modify: `src/server.py`

- [ ] **Step 1: Rewrite server.py**

```python
# src/server.py
"""MCP Obsidian Brain v2 — SQLite FTS5 backed, HTTP mode."""

import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from src.config import load_config, AppConfig
from src.database import BrainDB
from src.watcher import VaultWatcher
from src.git_sync import GitSync
from src.tools.brain import BrainTools, register_tools


def create_app(config_path: Path | None = None) -> FastMCP:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    cfg = load_config(config_path)

    db = BrainDB(cfg.db_path, cfg.fts.weights)
    db.create_schema()

    watcher = VaultWatcher(cfg.vault_path, db, cfg.excluded_dirs)
    git_sync = GitSync(cfg.vault_path, cfg.git)
    brain_tools = BrainTools(db, cfg.vault_path, git_sync)

    mcp = FastMCP(
        name="obsidian-brain",
        instructions=(
            "Acces au vault neoteem-brain — base de connaissances Neoteem (850+ notes). "
            "Contient : regles metier (01-Domaines/), tables et fonctions PG (02-BDD/), "
            "apps et modules (03-Apps/), regles metier (06-Regles-Metier/), "
            "FAQ et procedures support (07-Support/), syntheses (Knowledge/)."
            "\n\n"
            "search_brain cherche dans TOUT le vault d'un coup. Les dossiers sont un "
            "ordre de preference pour UTILISER les resultats, PAS un filtre."
        ),
    )

    register_tools(mcp, brain_tools)

    # Initial index
    print(f"Indexing vault: {cfg.vault_path}")
    result = watcher.scan()
    print(f"Indexed: {result.added} notes")

    # Background tasks
    async def watcher_loop():
        while True:
            await asyncio.sleep(cfg.watcher.poll_interval_seconds)
            changes = watcher.scan()
            if changes.added or changes.modified or changes.deleted:
                print(f"Watcher: +{changes.added} ~{changes.modified} -{changes.deleted}")

    async def git_pull_loop():
        while True:
            await asyncio.sleep(cfg.git.pull_interval_seconds)
            try:
                git_sync.pull()
            except Exception as e:
                print(f"Git pull error: {e}")

    async def git_push_loop():
        while True:
            await asyncio.sleep(cfg.git.push_interval_seconds)
            try:
                if git_sync.get_active_branches():
                    git_sync.push_all()
            except Exception as e:
                print(f"Git push error: {e}")

    @mcp.on_event("startup")
    async def on_startup():
        asyncio.create_task(watcher_loop())
        asyncio.create_task(git_pull_loop())
        asyncio.create_task(git_push_loop())

    return mcp


def main():
    app = create_app()
    app.run(transport="streamable-http")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test server starts without error**

Run: `python -c "from src.server import create_app; print('OK')"`
Expected: `OK` (verifies imports work, doesn't start the server)

- [ ] **Step 3: Commit**

```bash
git add src/server.py
git commit -m "feat: server — FastMCP HTTP mode, startup indexing, background watcher + git sync"
```

---

### Task 8: Clean up old files

**Files:**
- Delete: `src/cli.py`
- Delete: `scripts/` (if exists)
- Delete: `run-server.bat`
- Delete: `install.bat`
- Delete: `install-mcp-config.bat`

- [ ] **Step 1: Remove old CLI dependency files**

```bash
cd C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/mcp-obsidian-brain
git rm src/cli.py
git rm -f run-server.bat install.bat install-mcp-config.bat
git rm -rf scripts/ 2>/dev/null; true
```

- [ ] **Step 2: Verify no remaining references to Obsidian CLI**

Run: `grep -r "obsidian" src/ --include="*.py" -l`
Expected: No results (or only in comments/instructions)

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove Obsidian CLI dependency files"
```

---

### Task 9: Golden set capture + benchmark script

**Files:**
- Create: `test/queries.yaml`
- Create: `tests/benchmark_parity.py`

- [ ] **Step 1: Create golden set queries file**

```yaml
# test/queries.yaml
# Golden set — captured from Obsidian CLI before migration.
# Each query has expected top-5 results (file_stems).
# Run benchmark_parity.py to verify MCP v2 matches.

queries:
  - query: "charges copropriete"
    expected:
      - charges-copropriete
      # Fill remaining from CLI output before migration

  - query: "f_calc_charges"
    expected:
      - fonctions-suivi-copro
      # Fill remaining from CLI output

  - query: "bail gerance"
    expected:
      - bail

  - query: "vote AG"
    expected:
      - windev-ag

  - query: "encaissement"
    expected:
      - fonctions-encaissement

  - query: "suivi locataire"
    expected:
      - fonctions-suivi-locataire

  - query: "neomail"
    expected:
      - neomail

  # Add 20-40 more queries from real support/dev usage before migration.
  # Run: obsidian vault="neoteem-brain" search:context query="<term>" limit=5
  # Record the file_stems of top-5 results.
```

NOTE: Before migration, run the capture script below to fill in the expected results from the live CLI.

- [ ] **Step 2: Create benchmark script**

```python
# tests/benchmark_parity.py
"""Benchmark: compare MCP v2 search results vs golden set from CLI."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config
from src.database import BrainDB
from src.watcher import VaultWatcher


def run_benchmark(config_path: Path, queries_path: Path):
    cfg = load_config(config_path)
    db = BrainDB(cfg.db_path, cfg.fts.weights)
    db.create_schema()

    watcher = VaultWatcher(cfg.vault_path, db, cfg.excluded_dirs)
    result = watcher.scan()
    print(f"Indexed {result.added} notes")

    with open(queries_path) as f:
        data = yaml.safe_load(f)

    total = 0
    matches = 0
    details = []

    for entry in data["queries"]:
        query = entry["query"]
        expected = set(entry.get("expected", []))
        if not expected:
            continue

        results = db.search(query, limit=5)
        actual = {r["file_stem"] for r in results}

        overlap = expected & actual
        score = len(overlap) / len(expected) if expected else 0
        total += 1
        if score >= 0.8:
            matches += 1

        status = "PASS" if score >= 0.8 else "FAIL"
        details.append(f"  [{status}] '{query}': {score:.0%} overlap")
        if status == "FAIL":
            details.append(f"    Expected: {expected}")
            details.append(f"    Got:      {actual}")

    parity = matches / total if total else 0
    print(f"\nParity: {matches}/{total} queries pass ({parity:.0%})")
    print(f"Gate: {'PASS' if parity >= 0.8 else 'FAIL'} (threshold: 80%)\n")
    print("\n".join(details))

    db.close()
    return parity >= 0.8


if __name__ == "__main__":
    config_path = Path(__file__).parent.parent / "config.yaml"
    queries_path = Path(__file__).parent.parent / "test" / "queries.yaml"
    success = run_benchmark(config_path, queries_path)
    sys.exit(0 if success else 1)
```

- [ ] **Step 3: Commit**

```bash
mkdir -p test
git add test/queries.yaml tests/benchmark_parity.py
git commit -m "feat: golden set queries + benchmark parity script"
```

---

### Task 10: Run all tests + integration validation

- [ ] **Step 1: Run full test suite**

Run: `python -m pytest tests/ -v --tb=short`
Expected: All tests PASSED (test_config, test_indexer, test_database, test_watcher, test_git_sync, test_tools)

- [ ] **Step 2: Test against real vault (manual)**

```bash
cd C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/mcp-obsidian-brain
# Create a local config pointing to real vault
cat > config.local.yaml << 'EOF'
vault_path: C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain
db_path: C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/mcp-obsidian-brain/brain.db
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
EOF

python -c "
from src.config import load_config
from src.database import BrainDB
from src.watcher import VaultWatcher
from pathlib import Path

cfg = load_config(Path('config.local.yaml'))
db = BrainDB(cfg.db_path, cfg.fts.weights)
db.create_schema()
watcher = VaultWatcher(cfg.vault_path, db, cfg.excluded_dirs)
r = watcher.scan()
print(f'Indexed: {r.added} notes')

results = db.search('charges copropriete', limit=5)
for res in results:
    print(f'  {res[\"file_stem\"]} ({res[\"path\"]})')

print()
path = db.resolve_note('charges CC')
print(f'Resolve alias \"charges CC\": {path}')

backlinks = db.get_backlinks('bail')
print(f'Backlinks bail: {[bl[\"file_stem\"] for bl in backlinks]}')

db.close()
"
```

Expected: Indexes 800+ notes, search returns relevant results, alias resolution works.

- [ ] **Step 3: Commit final state**

```bash
git add -A
git commit -m "feat: MCP Obsidian Brain v2 — SQLite FTS5, ready for deployment"
```

---

## Post-implementation

### Before migration to production:

1. **Capture golden set** — run each query in `test/queries.yaml` against CLI Obsidian, fill in expected top-5
2. **Run benchmark** — `python tests/benchmark_parity.py` → gate must PASS (≥80%)
3. **Update 5 skills** — remove CLI mode, keep MCP mode only
4. **Deploy to VM** — clone repo, install deps, configure systemd service
5. **Configure orga settings** — add MCP endpoint for Claude Code + Claude Desktop
