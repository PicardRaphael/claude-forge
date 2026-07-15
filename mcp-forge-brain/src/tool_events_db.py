"""SQLite FTS5 store for Claude Code tool_use / tool_result events.

Separate tables from both the vault index (notes/notes_fts) and the sessions
index (session_messages/session_messages_fts): tool events are a third,
distinct concern (skill-friction analysis: recurring errors, tool collisions),
not conversational text. One FTS5 doc = one tool event, with session_id /
project / event_kind / tool_name / is_error / timestamp / path kept as
filterable columns (not in the FTS index, to keep BM25 ranking on text only).

Unlike SessionDB.search, an empty query string is a VALID call here: the
central use case is a filter-only query (e.g. "all errors for tool X", no
text term at all). Empty terms fall back to a plain SELECT with the same
WHERE filters instead of returning [].
"""

import re
import sqlite3

from src.tool_events_indexer import ToolEvent, parse_transcript


class ToolEventsDB:
    def __init__(self, conn: sqlite3.Connection):
        # Reuse the vault DB connection (same SQLite file, separate tables).
        self._conn = conn

    def create_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS tool_event_files (
                path          TEXT PRIMARY KEY,
                project       TEXT NOT NULL,
                last_modified REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tool_events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                path        TEXT NOT NULL,
                session_id  TEXT NOT NULL,
                project     TEXT NOT NULL,
                event_kind  TEXT NOT NULL,
                tool_name   TEXT NOT NULL,
                is_error    INTEGER,
                timestamp   TEXT,
                text        TEXT NOT NULL,
                line_no     INTEGER
            );
            CREATE INDEX IF NOT EXISTS idx_tevt_path ON tool_events(path);
            CREATE INDEX IF NOT EXISTS idx_tevt_project ON tool_events(project);
            CREATE INDEX IF NOT EXISTS idx_tevt_tool_name ON tool_events(tool_name);
            CREATE INDEX IF NOT EXISTS idx_tevt_event_kind ON tool_events(event_kind);
            CREATE INDEX IF NOT EXISTS idx_tevt_is_error ON tool_events(is_error);
        """)
        try:
            self._conn.execute("""
                CREATE VIRTUAL TABLE tool_events_fts USING fts5(
                    text,
                    tool_name,
                    tokenize='unicode61 remove_diacritics 2'
                )
            """)
        except sqlite3.OperationalError:
            pass
        self._conn.commit()

    def get_file_state(self, path: str) -> float | None:
        row = self._conn.execute(
            "SELECT last_modified FROM tool_event_files WHERE path = ?", (path,)
        ).fetchone()
        return row[0] if row else None

    def index_transcript(self, path: str, project: str, last_modified: float) -> int:
        """(Re)index one transcript. Removes prior rows for the path first.

        Returns the number of events indexed.
        """
        self._delete_path(path)
        events = parse_transcript(path, project)
        cur = self._conn.cursor()
        for e in events:
            cur.execute(
                "INSERT INTO tool_events "
                "(path, session_id, project, event_kind, tool_name, is_error, timestamp, text, line_no) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    path, e.session_id, e.project, e.event_kind, e.tool_name,
                    None if e.is_error is None else int(e.is_error),
                    e.timestamp, e.text, e.line_no,
                ),
            )
            cur.execute(
                "INSERT INTO tool_events_fts (rowid, text, tool_name) VALUES (?, ?, ?)",
                (cur.lastrowid, e.text, e.tool_name),
            )
        cur.execute(
            "INSERT INTO tool_event_files (path, project, last_modified) VALUES (?, ?, ?) "
            "ON CONFLICT(path) DO UPDATE SET project = excluded.project, "
            "last_modified = excluded.last_modified",
            (path, project, last_modified),
        )
        self._conn.commit()
        return len(events)

    def _delete_path(self, path: str):
        rows = self._conn.execute(
            "SELECT id FROM tool_events WHERE path = ?", (path,)
        ).fetchall()
        for (eid,) in rows:
            self._conn.execute("DELETE FROM tool_events_fts WHERE rowid = ?", (eid,))
        self._conn.execute("DELETE FROM tool_events WHERE path = ?", (path,))

    def delete_path(self, path: str):
        self._delete_path(path)
        self._conn.execute("DELETE FROM tool_event_files WHERE path = ?", (path,))
        self._conn.commit()

    def known_paths(self) -> set[str]:
        return {
            row[0] for row in self._conn.execute("SELECT path FROM tool_event_files").fetchall()
        }

    @staticmethod
    def _sanitize(query: str) -> list[str]:
        """Strip FTS operators / punctuation, return bare terms (injection-safe)."""
        clean = re.sub(r"['\"\-()*]", " ", query)
        return [t for t in clean.lower().split() if len(t) > 1]

    def search(
        self,
        query: str = "",
        limit: int = 20,
        project: str = "",
        tool_name: str = "",
        event_kind: str = "",
        is_error: bool | None = None,
        since: str = "",
    ) -> list[dict]:
        """Search / filter tool events.

        `query` is optional: filter-only calls (e.g. all errors for a given
        tool, no text term) are the central use case and must return rows, not
        an empty list — so an empty/whitespace query branches to a plain
        SELECT over tool_events instead of an FTS MATCH.
        """
        where = []
        params: list = []
        if project:
            where.append("project LIKE ?")
            params.append(f"%{project}%")
        if tool_name:
            where.append("tool_name = ?")
            params.append(tool_name)
        if event_kind:
            where.append("event_kind = ?")
            params.append(event_kind)
        if is_error is not None:
            where.append("is_error = ?")
            params.append(int(is_error))
        if since:
            where.append("timestamp >= ?")
            params.append(since)

        terms = self._sanitize(query)

        if not terms:
            sql = f"""
                SELECT session_id, project, event_kind, tool_name, is_error, timestamp, path,
                       text AS snippet, 0.0 AS score
                FROM tool_events
                {"WHERE " + " AND ".join(where) if where else ""}
                ORDER BY id DESC
                LIMIT ?
            """
            params2 = params + [limit]
            try:
                rows = self._conn.execute(sql, params2).fetchall()
            except sqlite3.OperationalError:
                return []
            return [dict(r) for r in rows]

        fts_expr = " OR ".join(f'"{t}"*' for t in terms)
        fts_where = ["e.id = f.rowid", "f.tool_events_fts MATCH ?"]
        fts_params: list = [fts_expr]
        for clause, val in zip(where, params):
            fts_where.append(clause.replace("project", "e.project").replace("tool_name", "e.tool_name")
                              .replace("event_kind", "e.event_kind").replace("is_error", "e.is_error")
                              .replace("timestamp", "e.timestamp"))
            fts_params.append(val)

        sql = f"""
            SELECT
                e.session_id, e.project, e.event_kind, e.tool_name, e.is_error, e.timestamp, e.path,
                snippet(tool_events_fts, 0, '>>> ', ' <<<', '...', 24) AS snippet,
                bm25(tool_events_fts) AS score
            FROM tool_events_fts f, tool_events e
            WHERE {' AND '.join(fts_where)}
            ORDER BY score
            LIMIT ?
        """
        fts_params.append(limit)
        try:
            rows = self._conn.execute(sql, fts_params).fetchall()
        except sqlite3.OperationalError:
            return []
        return [dict(r) for r in rows]

    def stats(self) -> dict:
        files = self._conn.execute("SELECT COUNT(*) FROM tool_event_files").fetchone()[0]
        events = self._conn.execute("SELECT COUNT(*) FROM tool_events").fetchone()[0]
        errors = self._conn.execute(
            "SELECT COUNT(*) FROM tool_events WHERE is_error = 1"
        ).fetchone()[0]
        return {"files": files, "events": events, "errors": errors}
