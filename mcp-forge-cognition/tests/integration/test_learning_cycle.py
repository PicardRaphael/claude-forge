from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError as PydanticValidationError

from forge_cognition.domain.models import Principal


def create_project(product, key: str) -> str:
    return product.project_create(
        name=key,
        slug=key,
        objective="Learning",
        owner="raphael",
        initial_constraints=[],
        idempotency_key=f"project-{key}",
    )["project_id"]


def episode(service, project_id: str, key: str) -> str:
    return service.episode_record(
        project_id=project_id,
        title=key,
        prediction="prediction",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.5,
        confidence_after=0.5,
        idempotency_key=key,
    )["id"]


def test_procedure_requires_real_cross_project_evidence_and_curator(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    reviewer = services[Principal.RED_TEAM]
    curator = services[Principal.CURATOR]
    project_a = create_project(product, "learning-a")
    project_b = create_project(product, "learning-b")
    episodes = [
        episode(product, project_a, "episode-a1"),
        episode(reviewer, project_a, "episode-a2"),
        episode(product, project_b, "episode-b1"),
    ]
    outcome = curator.project_record_outcome(
        project_id=project_b,
        experiment_id=None,
        outcome_type="usage",
        metric="retention",
        value=1,
        unit="user",
        observed_at=datetime.now(timezone.utc),
        source="usage-log",
        evidence="User retained",
        idempotency_key="learning-outcome",
    )
    candidate = product.memory_propose(
        entity_type="procedure",
        project_id=None,
        title="Validated learning procedure",
        content="Run the real outcome test.",
        provenance=[{"type": "outcome", "reference": outcome["id"]}],
        confidence=0.8,
        idempotency_key="procedure-candidate",
        attributes={
            "source_episode_ids": episodes,
            "source_outcome_ids": [outcome["id"]],
            "contradictions_searched": True,
            "counterexamples": ["No retention measurement"],
        },
    )
    assert product.procedure_search("outcome")["results"] == []
    committed = curator.memory_commit(
        candidate_id=candidate["id"],
        decision="validated",
        target_namespace="shared/procedures",
        expected_hash=candidate["content_hash"],
        idempotency_key="procedure-commit",
        reason="Threshold met",
    )
    assert committed["status"] == "validated"
    assert product.procedure_search("outcome")["results"][0]["id"] == committed["id"]


def test_three_episodes_without_outcome_cannot_form_procedure(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = create_project(product, "no-outcome")
    episodes = [episode(product, project, f"no-outcome-{index}") for index in range(3)]
    with pytest.raises(PydanticValidationError):
        product.memory_propose(
            entity_type="procedure",
            project_id=None,
            title="Unsupported procedure",
            content="No outcome",
            provenance=[{"type": "agent", "reference": "test"}],
            confidence=0.5,
            idempotency_key="unsupported-procedure",
            attributes={
                "source_episode_ids": episodes,
                "source_outcome_ids": [],
                "contradictions_searched": True,
            },
        )


def test_severe_security_exception_can_be_restricted_then_deprecated(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    curator = services[Principal.CURATOR]
    candidate = product.memory_propose(
        entity_type="procedure",
        project_id=None,
        title="Immediate incident restriction",
        content="Do not repeat the unsafe operation.",
        provenance=[{"type": "incident", "reference": "INC-001"}],
        confidence=0.9,
        idempotency_key="security-procedure",
        attributes={
            "security_exception": True,
            "expires_at": "2026-08-01",
            "review_required": True,
            "evidence_level": "incident-confirmed",
            "incident_id": "INC-001",
        },
    )
    restricted = curator.memory_commit(
        candidate_id=candidate["id"],
        decision="restricted",
        target_namespace="shared/procedures",
        expected_hash=candidate["content_hash"],
        idempotency_key="security-restrict",
        reason="Severe incident",
    )
    deprecated = curator.memory_deprecate(
        memory_id=restricted["id"],
        reason="Reviewed and retired",
        superseded_by=None,
        expected_hash=restricted["content_hash"],
        idempotency_key="security-deprecate",
    )
    assert deprecated["status"] == "deprecated"
