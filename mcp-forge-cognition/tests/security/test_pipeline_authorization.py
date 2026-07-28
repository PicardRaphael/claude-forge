from __future__ import annotations

import sqlite3

import pytest

from forge_cognition.domain.errors import NotFoundError, ValidationError
from forge_cognition.domain.models import EntityType, MemoryType, Principal
from forge_cognition.domain.pipeline import (
    ArtifactPointer,
    PipelineStage,
    PipelineState,
    ProjectGrant,
    canonical_payload,
)
from forge_cognition.infrastructure.runtime_compat import require_pipeline_runtime


def _write(service, document) -> None:
    relative = service.store.document_path(document.namespace, document.id)
    path = service.store.paths.resolve(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(service.store.serialize_document(document), encoding="utf-8")


def _pipeline_document(service, project_id: str, folder: str):
    namespace = f"{folder}/neutral"
    document = service._new_document(
        entity_type=EntityType.REVIEW,
        memory_type=MemoryType.SEMANTIC,
        project_id=project_id,
        owner="shared",
        namespace=namespace,
        visibility="shared",
        title="Pipeline review packet",
        body='{"payload_schema":"review-packet-v1"}',
        provenance=[{"type": "pipeline", "reference": project_id}],
        confidence=1.0,
        attributes={
            "pipeline_managed": True,
            "artifact_type": "review_packet",
            "series_id": f"{project_id}:review-packet",
            "payload_schema": "review-packet-v1",
        },
    )
    _write(service, document)
    return service.store.get_document(document.id)[0]


def _state_document(service, project_id: str, folder: str, state: PipelineState, *, previous=None):
    document = service._new_document(
        entity_type=EntityType.DECISION,
        memory_type=MemoryType.SEMANTIC,
        project_id=project_id,
        owner=Principal.CURATOR.value,
        namespace=f"{folder}/decisions",
        visibility="restricted",
        title="Pipeline state",
        body=canonical_payload(state),
        provenance=[{"type": "pipeline", "reference": project_id}],
        confidence=1.0,
        attributes={
            "pipeline_managed": True,
            "artifact_type": "pipeline_state",
            "series_id": f"{project_id}:pipeline-state",
            "payload_schema": "pipeline-state-v1",
        },
    )
    if previous is not None:
        document = document.model_copy(
            update={"revision": previous.revision + 1, "supersedes": previous.id}
        ).with_hash()
    _write(service, document)
    return service.store.get_document(document.id)[0]


def test_legacy_access_remains_while_pipeline_access_is_grant_scoped(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    reviewer = services[Principal.RED_TEAM]
    project = product.project_create(
        name="Authorization",
        slug="authorization",
        objective="Test central ACL",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="pipeline-auth-project",
    )
    project_id = project["project_id"]
    folder = product._project_folder(project_id)
    legacy = product.project_write_opportunity_brief(
        project_id=project_id,
        title="Legacy packet",
        content="Legacy remains readable",
        provenance=[{"type": "test", "reference": "legacy"}],
        confidence=1.0,
        idempotency_key="pipeline-auth-legacy",
    )
    packet = _pipeline_document(product, project_id, folder)
    product.indexes.rebuild_all()

    assert reviewer.context_get(legacy["id"])["title"] == "Legacy packet"
    with pytest.raises(NotFoundError, match="resource not found"):
        reviewer.context_get(packet.id)

    pointer = ArtifactPointer(
        document_id=packet.id,
        revision=packet.revision,
        content_hash=packet.content_hash,
        series_id=packet.attributes["series_id"],
    )
    state = PipelineState(
        project_id=project_id,
        stage=PipelineStage.REVIEW,
        pointers={"review_packet": pointer},
        grants=[
            ProjectGrant(
                principal=Principal.RED_TEAM,
                project_id=project_id,
                artifact_bindings=[pointer],
            )
        ],
    )
    first_state = _state_document(product, project_id, folder, state)
    product.indexes.rebuild_all()
    assert reviewer.context_get(packet.id)["id"] == packet.id

    revoked = state.model_copy(
        update={"grants": [state.grants[0].model_copy(update={"status": "revoked"})]}
    )
    _state_document(product, project_id, folder, revoked, previous=first_state)
    product.indexes.rebuild_all()
    with pytest.raises(NotFoundError):
        reviewer.context_get(packet.id)

    connection = sqlite3.connect(product.indexes.path_for(Principal.RED_TEAM))
    try:
        assert connection.execute(
            "SELECT COUNT(*) FROM documents WHERE id = ?", (packet.id,)
        ).fetchone()[0] == 0
    finally:
        connection.close()


def test_older_runtime_is_rejected_before_serving_pipeline_store(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = product.pipeline_project_create(
        name="Runtime guard",
        slug="runtime-guard",
        objective="Fail closed",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="runtime-guard-project",
    )
    assert project["project_id"]
    with pytest.raises(ValidationError, match="pipeline_runtime_too_old"):
        require_pipeline_runtime(product.store, runtime_version=0)
