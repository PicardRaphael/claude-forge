from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError as PydanticValidationError

from forge_cognition.domain.calibration import brier_score, confusion_matrix, recurrence_rate
from forge_cognition.domain.errors import ImmutableEntityError, ValidationError
from forge_cognition.domain.learning import procedure_promotion_eligible, smoothed_reliability
from forge_cognition.domain.models import (
    CognitionDocument,
    EntityType,
    MemoryType,
    Provenance,
    Status,
)


def document(entity_type: EntityType, *, project_id: str = "PRJ-2026-001") -> CognitionDocument:
    now = datetime.now(timezone.utc)
    return CognitionDocument(
        id="01J00000000000000000000000",
        entity_type=entity_type,
        memory_type=MemoryType.EPISODIC,
        project_id=project_id,
        owner="shared",
        namespace="projects/x/outcomes",
        visibility="shared",
        created_at=now,
        updated_at=now,
        confidence=0.7,
        confidence_basis="user-confirmed",
        provenance=[Provenance(type="user", reference="test")],
        title="Test",
        body="Body",
    ).with_hash()


def test_hash_and_revision_are_explicit() -> None:
    item = document(EntityType.EVIDENCE)
    updated = item.next_revision(datetime.now(timezone.utc), body="Changed")
    assert updated.id == item.id
    assert updated.revision == 2
    assert updated.content_hash != item.content_hash


def test_outcome_is_immutable() -> None:
    with pytest.raises(ImmutableEntityError):
        document(EntityType.OUTCOME).next_revision(datetime.now(timezone.utc), body="Changed")


def test_invalid_status_transition_is_refused() -> None:
    item = document(EntityType.EVIDENCE).model_copy(update={"status": Status.REJECTED})
    with pytest.raises(ValidationError, match="invalid status transition"):
        item.next_revision(datetime.now(timezone.utc), status=Status.VALIDATED)


def test_hypothesis_cannot_be_validated_without_evidence() -> None:
    item = document(EntityType.HYPOTHESIS).model_dump()
    item["status"] = Status.VALIDATED
    with pytest.raises(PydanticValidationError):
        CognitionDocument.model_validate(item)


def test_procedure_promotion_requires_three_episodes_two_projects_and_outcome() -> None:
    episodes = [
        document(EntityType.EPISODE, project_id=f"PRJ-2026-00{1 + (i % 2)}").model_copy(
            update={"id": f"01J0000000000000000000000{i}"}
        )
        for i in range(3)
    ]
    assert not procedure_promotion_eligible(episodes, [], contradictions_searched=True)
    assert procedure_promotion_eligible(
        episodes,
        [document(EntityType.OUTCOME)],
        contradictions_searched=True,
    )


def test_calibration_does_not_fabricate_metrics_without_outcomes() -> None:
    assert brier_score([]) is None
    assert confusion_matrix([]) is None
    assert brier_score([(0.8, 1), (0.3, 0)]) == pytest.approx(0.065)
    assert confusion_matrix([(True, True), (True, False), (False, True)]) == {
        "true_positive": 1,
        "true_negative": 0,
        "false_positive": 1,
        "false_negative": 1,
    }


def test_smoothed_reliability() -> None:
    assert smoothed_reliability(3, 1) == pytest.approx(4 / 6)
    assert recurrence_rate(2, 5) == pytest.approx(0.4)
    assert recurrence_rate(0, 0) is None
