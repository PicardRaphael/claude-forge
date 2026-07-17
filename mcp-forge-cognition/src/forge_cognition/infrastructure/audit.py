"""Append-only JSONL audit log, also the canonical idempotency ledger."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class JsonlAuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def find_idempotent(self, key: str) -> dict[str, Any] | None:
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("idempotency_key") == key:
                return event
        return None

    def append(self, event: dict[str, Any]) -> None:
        payload = json.dumps(event, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        with open(self.path, "a", encoding="utf-8", newline="\n") as stream:
            stream.write(payload + "\n")
            stream.flush()
            os.fsync(stream.fileno())
