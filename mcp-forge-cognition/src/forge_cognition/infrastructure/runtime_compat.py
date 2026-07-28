"""Fail-closed compatibility guard for pipeline-managed cognition."""

from __future__ import annotations

from forge_cognition.domain.errors import ValidationError

from .file_store import FileCanonicalStore


PIPELINE_RUNTIME_VERSION = 1


def require_pipeline_runtime(
    store: FileCanonicalStore, runtime_version: int = PIPELINE_RUNTIME_VERSION
) -> None:
    required = max(
        (
            int(document.attributes.get("minimum_runtime_version", 1))
            for document, _ in store.list_documents()
            if document.attributes.get("pipeline_managed") is True
        ),
        default=0,
    )
    if required > runtime_version:
        raise ValidationError("pipeline_runtime_too_old")
