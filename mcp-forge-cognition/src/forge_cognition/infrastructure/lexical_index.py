"""Disposable per-profile SQLite FTS5 projections."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from forge_cognition.domain.errors import ValidationError
from forge_cognition.domain.models import Principal
from forge_cognition.domain.policies import AccessPolicy

from .file_store import FileCanonicalStore


class SQLiteLexicalIndex:
    def __init__(
        self,
        store: FileCanonicalStore,
        policies: dict[Principal, AccessPolicy],
    ) -> None:
        self.store = store
        self.policies = policies
        self.index_dir = store.root / "indexes"
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, principal: Principal) -> Path:
        return self.index_dir / f"{principal.value}.sqlite"

    def rebuild_all(self) -> None:
        for principal in Principal:
            self.rebuild(principal)

    def rebuild(self, principal: Principal) -> None:
        target = self.path_for(principal)
        temporary = target.with_suffix(".sqlite.tmp")
        temporary.unlink(missing_ok=True)
        connection = sqlite3.connect(temporary)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.executescript(
                """
                CREATE TABLE documents (
                    id TEXT PRIMARY KEY,
                    path TEXT NOT NULL UNIQUE,
                    project_id TEXT,
                    entity_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    provenance_summary TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    content_hash TEXT NOT NULL
                );
                CREATE VIRTUAL TABLE documents_fts USING fts5(
                    id UNINDEXED, title, aliases, tags, summary, body,
                    tokenize='unicode61 remove_diacritics 2'
                );
                CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                """
            )
            policy = self.policies[principal]
            for document, relative_path in self.store.list_documents():
                if not policy.can_read(relative_path, document.project_id):
                    continue
                provenance_summary = ", ".join(
                    f"{item.type}:{item.reference}" for item in document.provenance[:3]
                )
                cursor = connection.execute(
                    "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        document.id,
                        relative_path,
                        document.project_id,
                        str(document.entity_type),
                        document.title,
                        str(document.status),
                        document.confidence,
                        provenance_summary,
                        document.revision,
                        document.content_hash,
                    ),
                )
                rowid = cursor.lastrowid
                connection.execute(
                    "INSERT INTO documents_fts(rowid, id, title, aliases, tags, summary, body) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        rowid,
                        document.id,
                        document.title,
                        " ".join(document.aliases),
                        " ".join(document.tags),
                        document.summary,
                        document.body,
                    ),
                )
            connection.execute(
                "INSERT INTO metadata VALUES ('built_at', ?)",
                (datetime.now(timezone.utc).isoformat(),),
            )
            connection.commit()
        finally:
            connection.close()
        os.replace(temporary, target)

    def search(
        self,
        principal: Principal,
        query: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        terms = [term for term in query.split() if term]
        if not terms:
            raise ValidationError("query must not be empty")
        match_query = " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)
        clauses = ["documents_fts MATCH ?"]
        parameters: list[Any] = [match_query]
        for field in ("project_id", "entity_type", "status"):
            values = filters.get(field)
            if values:
                if not isinstance(values, list):
                    values = [values]
                clauses.append(f"d.{field} IN ({','.join('?' for _ in values)})")
                parameters.extend(values)
        parameters.append(min(int(filters.get("limit", 10)), 50))
        connection = sqlite3.connect(self.path_for(principal))
        connection.row_factory = sqlite3.Row
        try:
            rows = connection.execute(
                "SELECT d.*, snippet(documents_fts, 5, '', '', ' … ', 20) AS excerpt, "
                "bm25(documents_fts, 0.0, 10.0, 5.0, 3.0, 2.0, 1.0) AS rank "
                "FROM documents_fts JOIN documents d ON d.rowid = documents_fts.rowid "
                f"WHERE {' AND '.join(clauses)} ORDER BY rank, d.id LIMIT ?",
                parameters,
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            connection.close()

    def health(self) -> dict[str, Any]:
        profiles: dict[str, Any] = {}
        for principal in Principal:
            path = self.path_for(principal)
            if not path.exists():
                profiles[principal.value] = {"status": "missing"}
                continue
            connection = sqlite3.connect(path)
            try:
                count = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                profiles[principal.value] = {"status": integrity, "documents": count}
            finally:
                connection.close()
        return profiles
