"""Atomic mutation coordinator with rollback and canonical idempotency."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any, TypeVar

from forge_cognition.domain.errors import IdempotencyConflictError
from forge_cognition.domain.models import Principal

from .audit import JsonlAuditLog
from .clock import SystemClock
from .file_store import AtomicMutation, FileCanonicalStore
from .ids import UlidGenerator
from .lexical_index import SQLiteLexicalIndex
from .locking import FileLock


T = TypeVar("T")


class MutationCoordinator:
    def __init__(
        self,
        store: FileCanonicalStore,
        indexes: SQLiteLexicalIndex,
        audit: JsonlAuditLog,
        *,
        timeout_seconds: float = 5,
        clock: SystemClock | None = None,
        ids: UlidGenerator | None = None,
    ) -> None:
        self.store = store
        self.indexes = indexes
        self.audit = audit
        self.timeout_seconds = timeout_seconds
        self.clock = clock or SystemClock()
        self.ids = ids or UlidGenerator()

    def execute(
        self,
        *,
        action: str,
        principal: Principal,
        idempotency_key: str,
        request_payload: dict[str, Any],
        mutate: Callable[[AtomicMutation], T],
        result_payload: Callable[[T], dict[str, Any]],
    ) -> dict[str, Any]:
        if not idempotency_key.strip():
            raise ValueError("idempotency_key is required")
        request_hash = self._request_hash(action, principal, request_payload)
        existing = self.audit.find_idempotent(idempotency_key)
        if existing is not None:
            if existing["request_hash"] != request_hash:
                raise IdempotencyConflictError("idempotency key reused with different data")
            return existing["result"]

        lock_path = self.store.root / "indexes" / ".mutation.lock"
        with FileLock(lock_path, self.timeout_seconds):
            existing = self.audit.find_idempotent(idempotency_key)
            if existing is not None:
                if existing["request_hash"] != request_hash:
                    raise IdempotencyConflictError("idempotency key reused with different data")
                return existing["result"]

            mutation = AtomicMutation(self.store.paths)
            audit_size = self.audit.path.stat().st_size
            try:
                value = mutate(mutation)
                self.indexes.rebuild_all()
                result = result_payload(value)
                self.audit.append(
                    {
                        "event_id": self.ids.new(),
                        "timestamp": self.clock.now().isoformat(),
                        "principal": principal.value,
                        "action": action,
                        "idempotency_key": idempotency_key,
                        "request_hash": request_hash,
                        "result": result,
                    }
                )
                return result
            except BaseException:
                mutation.rollback()
                with open(self.audit.path, "r+b") as stream:
                    stream.truncate(audit_size)
                self.indexes.rebuild_all()
                raise

    @staticmethod
    def _request_hash(action: str, principal: Principal, payload: dict[str, Any]) -> str:
        encoded = json.dumps(
            {"action": action, "principal": principal.value, "payload": payload},
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
