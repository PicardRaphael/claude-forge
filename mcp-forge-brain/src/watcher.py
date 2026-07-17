"""Poll filesystem for .md changes, trigger reindex."""

import hashlib
from dataclasses import dataclass
from pathlib import Path

from src.path_security import PathSecurityError, VaultPathResolver
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
        self._paths = VaultPathResolver(vault_path)
        self._db = db
        self._excluded = set(excluded_dirs)

    def _iter_notes(self):
        for md_file in self._vault.rglob("*.md"):
            rel = md_file.relative_to(self._vault)
            try:
                md_file = self._paths.resolve(rel.as_posix(), must_exist=True)
            except PathSecurityError:
                continue
            if any(part in self._excluded for part in rel.parts):
                continue
            yield md_file, str(rel).replace("\\", "/")

    def scan(self) -> ScanResult:
        result = ScanResult()
        seen_paths: set[str] = set()

        for md_file, rel_path in self._iter_notes():
            seen_paths.add(rel_path)
            file_mtime = md_file.stat().st_mtime
            db_state = self._db.get_note_state(rel_path)

            if db_state is None:
                self._index_file(md_file, rel_path, file_mtime)
                result.added += 1
            elif file_mtime != db_state[0]:
                content = md_file.read_text(encoding="utf-8", errors="replace")
                content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                if content_hash != db_state[1]:
                    parsed = parse_note(md_file.stem, rel_path, content)
                    self._db.index_note(parsed, file_mtime)
                    result.modified += 1
                else:
                    self._db.execute(
                        "UPDATE notes SET last_modified = ? WHERE path = ?",
                        (file_mtime, rel_path),
                    )
                    self._db._conn.commit()

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
