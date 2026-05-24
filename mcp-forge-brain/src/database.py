"""SQLite FTS5 database for forge-brain vault index."""

import hashlib
import re
import sqlite3
from pathlib import Path
from src.config import FTSWeights
from src.indexer import ParsedNote


STOP_WORDS_FR = frozenset({
    "le", "la", "les", "un", "une", "des", "de", "du", "au", "aux",
    "ce", "ces", "cette", "mon", "ma", "mes", "ton", "ta", "tes",
    "son", "sa", "ses", "notre", "nos", "votre", "vos", "leur", "leurs",
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on",
    "qui", "que", "quoi", "dont", "ou",
    "et", "ou", "mais", "donc", "car", "ni", "ne", "pas", "plus",
    "en", "dans", "sur", "sous", "par", "pour", "avec", "sans",
    "est", "sont", "a", "ont", "fait", "faire", "etre", "avoir",
    "comment", "pourquoi", "quand", "quel", "quelle", "quels", "quelles",
})


class BrainDB:
    def __init__(self, db_path: Path, weights: FTSWeights):
        self._path = db_path
        self._weights = weights
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
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
                last_modified REAL NOT NULL,
                content_hash  TEXT
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
            pass
        # Migration: add content_hash column to existing DBs
        try:
            self._conn.execute("ALTER TABLE notes ADD COLUMN content_hash TEXT")
        except sqlite3.OperationalError:
            pass
        self._conn.commit()

    @staticmethod
    def _hash_content(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def index_note(self, note: ParsedNote, last_modified: float):
        cur = self._conn.cursor()
        cur.execute("SELECT id FROM notes WHERE path = ?", (note.path,))
        existing = cur.fetchone()
        if existing:
            self._delete_by_id(existing[0])

        content_hash = self._hash_content(note.content)
        cur.execute(
            "INSERT INTO notes (file_stem, path, content, frontmatter, last_modified, content_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (note.file_stem, note.path, note.content, note.frontmatter_raw, last_modified, content_hash),
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

    def _fts_query(self, fts_expr: str, limit: int, context: bool) -> list[dict]:
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
        rows = self._conn.execute(sql, (w.file_stem, w.content, w.aliases, fts_expr, limit)).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _like_variants(term: str) -> list[str]:
        """Generate LIKE patterns: original + without trailing e/s/es/ee/ees."""
        patterns = [f"%{term}%"]
        for suffix in ("ees", "ee", "es", "s", "e"):
            if term.endswith(suffix) and len(term) - len(suffix) >= 3:
                patterns.append(f"%{term[:-len(suffix)]}%")
                break
        return patterns

    def _alias_expansion(self, terms: list[str], limit: int, context: bool) -> list[dict]:
        """Find notes whose aliases contain query terms — ranked by distinct terms matched."""
        search_terms = [t for t in terms if len(t) >= 3]
        if not search_terms:
            return []
        case_parts = []
        params = []
        for t in search_terms:
            variants = self._like_variants(t)
            or_clause = " OR ".join("LOWER(a.alias) LIKE ?" for _ in variants)
            case_parts.append(f"MAX(CASE WHEN {or_clause} THEN 1 ELSE 0 END)")
            params.extend(variants)
        score_expr = " + ".join(case_parts)
        sql = f"""
            SELECT n.id, n.path, n.file_stem,
                   ({score_expr}) as term_hits
            FROM aliases a
            JOIN notes n ON n.id = a.note_id
            GROUP BY n.id
            HAVING term_hits > 0
            ORDER BY term_hits DESC, n.file_stem
            LIMIT ?
        """
        params.append(limit)
        note_ids = self._conn.execute(sql, params).fetchall()
        if not note_ids:
            return []
        stems = [row[2] for row in note_ids]
        fts_terms = " OR ".join(f'"{s}"' for s in stems)
        try:
            return self._fts_query(fts_terms, limit, context)
        except Exception:
            return [{"path": row[1], "file_stem": row[2], "score": -row[3]} for row in note_ids]

    def search(self, query: str, limit: int = 5, context: bool = True) -> list[dict]:
        clean = re.sub(r"['\"\-()]", " ", query)
        terms = [t for t in clean.lower().split() if t not in STOP_WORDS_FR and len(t) > 1]
        if not terms:
            terms = [t for t in clean.lower().split() if len(t) > 1]
        if not terms:
            return []
        alias_terms = terms

        # Strategy 1: AND with prefix wildcard (strictest)
        fts_and_prefix = " ".join(f'"{t}"*' for t in terms)
        rows = self._fts_query(fts_and_prefix, limit, context)
        if rows:
            return self._merge_alias_hits(rows, alias_terms, limit, context)

        # Strategy 2: OR with prefix wildcard (looser)
        fts_or_prefix = " OR ".join(f'"{t}"*' for t in terms)
        rows = self._fts_query(fts_or_prefix, limit, context)
        if rows:
            return self._merge_alias_hits(rows, alias_terms, limit, context)

        # Strategy 3: OR without wildcard (exact subwords)
        fts_or_exact = " OR ".join(f'"{t}"' for t in terms)
        rows = self._fts_query(fts_or_exact, limit, context)
        if rows:
            return self._merge_alias_hits(rows, alias_terms, limit, context)

        # Strategy 4: Alias expansion only (with stem variants) — last resort
        return self._alias_expansion(alias_terms, limit, context)

    def _merge_alias_hits(self, fts_rows: list[dict], terms: list[str], limit: int, context: bool) -> list[dict]:
        """Merge FTS results with alias-expanded results, deduped by path."""
        alias_rows = self._alias_expansion(terms, limit, context)
        if not alias_rows:
            return fts_rows
        seen = {r["path"] for r in fts_rows}
        merged = list(fts_rows)
        for ar in alias_rows:
            if ar["path"] not in seen:
                merged.append(ar)
                seen.add(ar["path"])
        return merged[:limit]

    def resolve_note(self, name: str) -> str | None:
        # 1. Exact match by name or alias
        row = self._conn.execute(
            "SELECT path FROM notes WHERE file_stem = ? "
            "UNION "
            "SELECT n.path FROM notes n JOIN aliases a ON a.note_id = n.id WHERE a.alias = ? "
            "LIMIT 1",
            (name, name),
        ).fetchone()
        if row:
            return row[0]
        # 2. Substring match on file_stem (e.g. "bail" matches "rm-bail-contrat")
        row = self._conn.execute(
            "SELECT path FROM notes WHERE file_stem LIKE ? ORDER BY LENGTH(file_stem) LIMIT 1",
            (f"%-{name}%",),
        ).fetchone()
        if row:
            return row[0]
        # 3. Substring at start (e.g. "bail" matches "bail-commercial")
        row = self._conn.execute(
            "SELECT path FROM notes WHERE file_stem LIKE ? ORDER BY LENGTH(file_stem) LIMIT 1",
            (f"{name}-%",),
        ).fetchone()
        return row[0] if row else None

    def suggest_notes(self, name: str, limit: int = 5) -> list[str]:
        """Search for notes similar to the given name."""
        results = self.search(name, limit=limit, context=False)
        return [r["file_stem"] for r in results]

    def get_backlinks(self, file_stem: str) -> list[dict]:
        # Case-insensitive exact match (Obsidian resolves [[Alpha]] -> alpha.md)
        # + substring match for partial wikilinks
        # Use LOWER() on both sides; for the # variant, normalize the link target
        # by truncating before # to compare stems.
        rows = self._conn.execute(
            "SELECT n.file_stem, COUNT(*) as count "
            "FROM links l "
            "JOIN notes n ON n.id = l.source_id "
            "WHERE LOWER(l.target) = LOWER(?) "
            "   OR LOWER(SUBSTR(l.target, 1, INSTR(l.target, '#') - 1)) = LOWER(?) "
            "   OR LOWER(l.target) LIKE LOWER(?) "
            "GROUP BY n.file_stem "
            "ORDER BY count DESC",
            (file_stem, file_stem, f"%-{file_stem}%"),
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
            if not isinstance(fm, dict):
                return None
            val = fm.get(name, "")
            if isinstance(val, list):
                return ", ".join(str(v) for v in val)
            return str(val)
        except yaml.YAMLError:
            return None

    def get_last_modified(self, path: str) -> float | None:
        row = self._conn.execute(
            "SELECT last_modified FROM notes WHERE path = ?", (path,)
        ).fetchone()
        return row[0] if row else None

    def get_note_state(self, path: str) -> tuple[float, str] | None:
        row = self._conn.execute(
            "SELECT last_modified, content_hash FROM notes WHERE path = ?", (path,)
        ).fetchone()
        return (row[0], row[1] or "") if row else None

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
