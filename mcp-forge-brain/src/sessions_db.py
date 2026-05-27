"""SQLite FTS5 store for Claude Code session transcripts.

Separate tables from the vault index (notes/notes_fts): transcripts are
ephemeral and high-volume, vault notes are durable and curated. One FTS5 doc =
one conversational message, with session_id / role / project / timestamp /
transcript_path kept as filterable columns (not in the FTS index, to keep BM25
ranking on content only).
"""

import re
import sqlite3

from src.sessions_indexer import ParsedMessage, parse_transcript


class SessionDB:
    def __init__(self, conn: sqlite3.Connection):
        # Reuse the vault DB connection (same SQLite file, separate tables).
        self._conn = conn

    def create_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS session_files (
                path          TEXT PRIMARY KEY,
                project       TEXT NOT NULL,
                last_modified REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS session_messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                path        TEXT NOT NULL,
                session_id  TEXT NOT NULL,
                project     TEXT NOT NULL,
                role        TEXT NOT NULL,
                timestamp   TEXT,
                content     TEXT NOT NULL,
                line_no     INTEGER
            );
            CREATE INDEX IF NOT EXISTS idx_smsg_path ON session_messages(path);
            CREATE INDEX IF NOT EXISTS idx_smsg_project ON session_messages(project);
            CREATE INDEX IF NOT EXISTS idx_smsg_role ON session_messages(role);
        """)
        try:
            self._conn.execute("""
                CREATE VIRTUAL TABLE session_messages_fts USING fts5(
                    content,
                    tokenize='unicode61 remove_diacritics 2'
                )
            """)
        except sqlite3.OperationalError:
            pass
        self._conn.commit()

    def get_file_state(self, path: str) -> float | None:
        row = self._conn.execute(
            "SELECT last_modified FROM session_files WHERE path = ?", (path,)
        ).fetchone()
        return row[0] if row else None

    def index_transcript(self, path: str, project: str, last_modified: float) -> int:
        """(Re)index one transcript. Removes prior rows for the path first.

        Returns the number of messages indexed.
        """
        self._delete_path(path)
        messages = parse_transcript(path, project)
        cur = self._conn.cursor()
        for m in messages:
            cur.execute(
                "INSERT INTO session_messages "
                "(path, session_id, project, role, timestamp, content, line_no) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (path, m.session_id, m.project, m.role, m.timestamp, m.content, m.line_no),
            )
            cur.execute(
                "INSERT INTO session_messages_fts (rowid, content) VALUES (?, ?)",
                (cur.lastrowid, m.content),
            )
        cur.execute(
            "INSERT INTO session_files (path, project, last_modified) VALUES (?, ?, ?) "
            "ON CONFLICT(path) DO UPDATE SET project = excluded.project, "
            "last_modified = excluded.last_modified",
            (path, project, last_modified),
        )
        self._conn.commit()
        return len(messages)

    def _delete_path(self, path: str):
        rows = self._conn.execute(
            "SELECT id FROM session_messages WHERE path = ?", (path,)
        ).fetchall()
        for (mid,) in rows:
            self._conn.execute("DELETE FROM session_messages_fts WHERE rowid = ?", (mid,))
        self._conn.execute("DELETE FROM session_messages WHERE path = ?", (path,))

    def delete_path(self, path: str):
        self._delete_path(path)
        self._conn.execute("DELETE FROM session_files WHERE path = ?", (path,))
        self._conn.commit()

    def known_paths(self) -> set[str]:
        return {
            row[0] for row in self._conn.execute("SELECT path FROM session_files").fetchall()
        }

    @staticmethod
    def _sanitize(query: str) -> list[str]:
        """Strip FTS operators / punctuation, return bare terms (injection-safe)."""
        clean = re.sub(r"['\"\-()*]", " ", query)
        return [t for t in clean.lower().split() if len(t) > 1]

    def search(
        self,
        query: str,
        limit: int = 20,
        project: str = "",
        role: str = "",
        since: str = "",
    ) -> list[dict]:
        """Full-text search over indexed messages.

        Each query term is quoted and prefix-wildcarded, joined with OR. Filters
        (project / role / since) are applied as SQL WHERE clauses. Returns dict
        rows with a highlighted snippet.
        """
        terms = self._sanitize(query)
        if not terms:
            return []
        fts_expr = " OR ".join(f'"{t}"*' for t in terms)

        where = ["m.id = f.rowid", "f.session_messages_fts MATCH ?"]
        params: list = [fts_expr]
        if project:
            where.append("m.project LIKE ?")
            params.append(f"%{project}%")
        if role:
            where.append("m.role = ?")
            params.append(role)
        if since:
            where.append("m.timestamp >= ?")
            params.append(since)

        sql = f"""
            SELECT
                m.session_id, m.project, m.role, m.timestamp, m.path,
                snippet(session_messages_fts, 0, '>>> ', ' <<<', '...', 24) AS snippet,
                bm25(session_messages_fts) AS score
            FROM session_messages_fts f, session_messages m
            WHERE {' AND '.join(where)}
            ORDER BY score
            LIMIT ?
        """
        params.append(limit)
        try:
            rows = self._conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            return []
        return [dict(r) for r in rows]

    def stats(self) -> dict:
        files = self._conn.execute("SELECT COUNT(*) FROM session_files").fetchone()[0]
        msgs = self._conn.execute("SELECT COUNT(*) FROM session_messages").fetchone()[0]
        return {"files": files, "messages": msgs}
