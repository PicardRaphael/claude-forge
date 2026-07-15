"""Scan ~/.claude/projects for transcript changes, trigger tool_events reindex.

Mirrors SessionWatcher: incremental by mtime, deletes vanished files. The
project name is the encoded directory name (e.g. C--Users-...-claude-forge).
"""

from dataclasses import dataclass
from pathlib import Path

from src.tool_events_db import ToolEventsDB


@dataclass
class ToolEventsScanResult:
    added: int = 0
    modified: int = 0
    deleted: int = 0
    events: int = 0


class ToolEventsWatcher:
    def __init__(self, sessions_path: Path, db: ToolEventsDB, include_subagents: bool = False):
        self._root = sessions_path
        self._db = db
        self._include_subagents = include_subagents

    def _iter_transcripts(self):
        """Yield (Path, project_name) for each transcript .jsonl.

        project_name = the top-level encoded directory under projects/.
        Subagent transcripts live in `<project>/<uuid>/subagents/*.jsonl` and are
        skipped unless include_subagents is True.
        """
        if not self._root.exists():
            return
        for jsonl in self._root.rglob("*.jsonl"):
            parts = jsonl.relative_to(self._root).parts
            if not parts:
                continue
            if not self._include_subagents and "subagents" in parts:
                continue
            project = parts[0]
            yield jsonl, project

    def scan(self) -> ToolEventsScanResult:
        result = ToolEventsScanResult()
        seen: set[str] = set()

        for jsonl, project in self._iter_transcripts():
            path = str(jsonl)
            seen.add(path)
            mtime = jsonl.stat().st_mtime
            prev = self._db.get_file_state(path)
            if prev is None:
                n = self._db.index_transcript(path, project, mtime)
                result.added += 1
                result.events += n
            elif mtime != prev:
                n = self._db.index_transcript(path, project, mtime)
                result.modified += 1
                result.events += n

        for gone in self._db.known_paths() - seen:
            self._db.delete_path(gone)
            result.deleted += 1

        return result
