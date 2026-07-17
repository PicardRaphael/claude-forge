"""Ports keeping domain and use cases independent of storage engines."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Protocol, TypeVar

from forge_cognition.domain.models import CognitionDocument, Principal, Project


T = TypeVar("T")


class CanonicalStorePort(Protocol):
    def get_document(self, document_id: str) -> tuple[CognitionDocument, str]: ...
    def list_documents(self) -> Iterable[tuple[CognitionDocument, str]]: ...
    def get_project(self, project_id: str) -> Project: ...
    def document_path(self, namespace: str, document_id: str) -> str: ...
    def serialize_document(self, document: CognitionDocument) -> str: ...
    def serialize_project(self, project: Project) -> str: ...


class LexicalIndexPort(Protocol):
    def rebuild_all(self) -> None: ...
    def search(
        self, principal: Principal, query: str, filters: dict[str, Any]
    ) -> list[dict[str, Any]]: ...
    def health(self) -> dict[str, Any]: ...


class SemanticIndexPort(Protocol):
    """Future semantic retrieval contract; no v1 implementation."""


class TemporalGraphPort(Protocol):
    """Future temporal graph contract; no v1 implementation."""


class AuditLogPort(Protocol):
    def find_idempotent(self, key: str) -> dict[str, Any] | None: ...
    def append(self, event: dict[str, Any]) -> None: ...


class OutcomeRepositoryPort(Protocol):
    def list_outcomes(self, project_id: str | None = None) -> Iterable[CognitionDocument]: ...


class ProcedureRepositoryPort(Protocol):
    def list_procedures(self) -> Iterable[CognitionDocument]: ...


class MutationPort(Protocol):
    def write_text(self, relative_path: str, content: str) -> None: ...
    def move(self, source: str, target: str) -> None: ...


class TransactionPort(Protocol):
    def execute(
        self,
        *,
        action: str,
        principal: Principal,
        idempotency_key: str,
        request_payload: dict[str, Any],
        mutate: Callable[[MutationPort], T],
        result_payload: Callable[[T], dict[str, Any]],
    ) -> dict[str, Any]: ...


class ClockPort(Protocol):
    def now(self): ...


class IdGeneratorPort(Protocol):
    def new(self) -> str: ...
