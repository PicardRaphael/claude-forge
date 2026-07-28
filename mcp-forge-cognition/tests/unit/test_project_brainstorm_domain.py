from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError as PydanticValidationError

from forge_cognition.domain.models import CognitionDocument, Principal, Project
from forge_cognition.domain.pipeline import (
    ArchitectureHandoff,
    ArtifactPointer,
    CdcHandoff,
    PipelineStage,
    PipelineState,
    ProjectGrant,
    ReviewVerdict,
    canonical_payload_hash,
)


def test_v1_envelopes_remain_unchanged() -> None:
    assert "series_id" not in CognitionDocument.model_fields
    assert "grants" not in Project.model_fields
    assert "artifact_pointers" not in Project.model_fields


def test_brainstorm_principal_and_verdicts_are_closed() -> None:
    assert Principal.ARCHITECT_BRAINSTORM.value == "architect-brainstorm"
    assert {item.value for item in ReviewVerdict} == {
        "GO_DEV",
        "GO_DEV_WITH_CONDITIONS",
        "REWORK_CDC",
        "REWORK_ARCHITECTURE",
        "PARK",
        "KILL",
    }
    with pytest.raises(ValueError):
        ReviewVerdict("MAYBE")


def test_handoff_payloads_are_strict_and_hash_canonical() -> None:
    payload = CdcHandoff(
        problem="Manual project design is inconsistent",
        target_users=["project owners"],
        desired_outcomes=["reviewed delivery handoff"],
        constraints=["no application code"],
        acceptance_criteria=["human CDC approval"],
        assumptions=[],
        evidence=[],
        unknowns=[],
        non_goals=["implementation"],
    )
    first = canonical_payload_hash(payload)
    second = canonical_payload_hash(CdcHandoff.model_validate(payload.model_dump()))
    assert first == second and first.startswith("sha256:")
    with pytest.raises(PydanticValidationError):
        CdcHandoff.model_validate({**payload.model_dump(), "persuasion": "ship it"})


def test_pipeline_state_requires_unique_active_grants() -> None:
    pointer = ArtifactPointer(
        document_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        revision=1,
        content_hash="sha256:" + "a" * 64,
        series_id="PRJ-2026-001:cdc",
    )
    grant = ProjectGrant(
        principal=Principal.ARCHITECT_BRAINSTORM,
        project_id="PRJ-2026-001",
        artifact_bindings=[pointer],
    )
    with pytest.raises(PydanticValidationError, match="duplicate active grant"):
        PipelineState(
            project_id="PRJ-2026-001",
            stage=PipelineStage.CDC_APPROVED,
            pointers={"cdc": pointer},
            grants=[grant, grant],
        )


def test_architecture_payload_rejects_unstructured_metadata() -> None:
    with pytest.raises(PydanticValidationError):
        ArchitectureHandoff.model_validate(
            {
                "summary": "Design",
                "components": [],
                "data_contracts": [],
                "interfaces": [],
                "security": [],
                "failure_modes": [],
                "test_strategy": [],
                "rollout": [],
                "alternatives": [],
                "assumptions": [],
                "evidence": [],
                "unknowns": [],
                "file_impacts": [],
                "private_reasoning": "not allowed",
            }
        )


def test_versioned_pipeline_schemas_are_closed() -> None:
    schema_root = Path(__file__).resolve().parents[3] / "cognition-store" / "schemas"
    for name in (
        "cdc-handoff-v1.yaml",
        "architecture-handoff-v1.yaml",
        "review-packet-v1.yaml",
        "review-verdict-v1.yaml",
        "development-handoff-v1.yaml",
        "pipeline-state-v1.yaml",
    ):
        schema = yaml.safe_load((schema_root / name).read_text(encoding="utf-8"))
        assert schema["additionalProperties"] is False
