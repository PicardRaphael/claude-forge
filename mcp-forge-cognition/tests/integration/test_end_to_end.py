from __future__ import annotations

from datetime import datetime, timezone

import pytest

from forge_cognition.domain.errors import NotFoundError
from forge_cognition.domain.models import Principal
from forge_cognition.bootstrap import build_service
from forge_cognition.config.loader import AppConfig


def test_full_product_review_curator_learning_cycle(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    reviewer = services[Principal.RED_TEAM]
    curator = services[Principal.CURATOR]

    # 1-2. Product creates and reads an authorized project projection.
    project = product.project_create(
        name="Outcome-grounded product",
        slug="outcome-grounded-product",
        objective="Test a paid workflow",
        owner="raphael",
        initial_constraints=["No external infrastructure"],
        idempotency_key="e2e-project",
    )
    project_id = project["project_id"]
    assert product.project_get(project_id)["objective"] == "Test a paid workflow"

    # 3. Private Product episode.
    product_episode = product.episode_record(
        project_id=project_id,
        title="Product prediction episode",
        prediction="A user will pay 20 EUR",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=["Test willingness to pay"],
        confidence_before=0.7,
        confidence_after=0.7,
        idempotency_key="e2e-product-episode",
    )

    # 4-5. Neutral brief and traceable review packet.
    brief = product.project_write_opportunity_brief(
        project_id=project_id,
        title="Opportunity brief",
        content="# Target\nOperators\n\n# Problem\nManual work\n\n# First test\nPaid pilot",
        provenance=[{"type": "user", "reference": "explicit-input"}],
        confidence=0.7,
        idempotency_key="e2e-brief",
    )
    packet = product.project_publish_review_packet(
        project_id=project_id,
        source_brief_id=brief["id"],
        included_evidence_ids=[],
        included_hypothesis_ids=[],
        expected_hash=brief["content_hash"],
        idempotency_key="e2e-packet",
    )

    # 6-8. Reviewer sees packet, not Product private memory, then records review + private episode.
    assert reviewer.context_get(packet["id"])["attributes"]["producer"] == "forge-product"
    with pytest.raises(NotFoundError):
        reviewer.context_get(product_episode["id"])
    review = reviewer.review_record(
        project_id=project_id,
        packet_id=packet["id"],
        verdict="GO_IF",
        content="GO IF a paid pilot occurs",
        confidence=0.65,
        idempotency_key="e2e-review",
    )
    reviewer_episode = reviewer.episode_record(
        project_id=project_id,
        title="Reviewer prediction episode",
        prediction="Paid pilot is unlikely",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=["Ask for payment early"],
        confidence_before=0.65,
        confidence_after=0.65,
        idempotency_key="e2e-reviewer-episode",
    )

    # 9-10. Curator records immutable real outcome; agents link predictions to it.
    outcome = curator.project_record_outcome(
        project_id=project_id,
        experiment_id=None,
        outcome_type="payment",
        metric="paid_pilot",
        value=20,
        unit="EUR",
        observed_at=datetime.now(timezone.utc),
        source="invoice-test-001",
        evidence="Payment received",
        idempotency_key="e2e-outcome",
    )
    feedback = reviewer.memory_feedback(
        memory_id=reviewer_episode["id"],
        outcome_id=outcome["id"],
        feedback_type="prediction_infirmed",
        evidence="Payment was received",
        confidence=1.0,
        idempotency_key="e2e-feedback",
    )
    assert feedback["outcome_id"] == outcome["id"]

    # 11-13. Candidate lesson stays out of procedure search until explicit Curator decision.
    lesson = reviewer.memory_propose(
        entity_type="lesson",
        project_id=project_id,
        title="Ask for payment early",
        content="Use a real payment test before declaring demand.",
        provenance=[{"type": "outcome", "reference": outcome["id"]}],
        confidence=0.8,
        idempotency_key="e2e-lesson",
    )
    assert curator.procedure_search("payment")["results"] == []
    committed = curator.memory_commit(
        candidate_id=lesson["id"],
        decision="validated",
        target_namespace="shared/context",
        expected_hash=lesson["content_hash"],
        idempotency_key="e2e-lesson-commit",
        reason="Outcome verified; retained as lesson, not procedure",
    )
    assert committed["status"] == "validated"

    # 14-15. Full rebuild preserves profile isolation and authorized retrieval.
    curator.rebuild_indexes()
    assert reviewer.context_search("payment")["results"]
    assert product.context_search("payment")["results"]
    assert reviewer.context_search("Product prediction episode")["results"] == []
    assert product.context_search("Reviewer prediction episode")["results"] == []
    assert review["id"] in {item["id"] for item in product.context_search("GO IF")["results"]}


def test_real_deny_by_default_profiles_preserve_legacy_workflow(tmp_path, services) -> None:
    store_path = services[Principal.CURATOR].store.root

    def real_service(principal: Principal):
        return build_service(AppConfig(store_path=store_path, profile=principal, allowed_projects=frozenset()))

    product = real_service(Principal.FORGE_PRODUCT)
    reviewer = real_service(Principal.RED_TEAM)
    project = product.project_create(
        name="Legacy profile",
        slug="legacy-real-profile",
        objective="Preserve the established review flow",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="legacy-real-profile-project",
    )
    brief = product.project_write_opportunity_brief(
        project_id=project["project_id"],
        title="Legacy brief",
        content="# Target\nOperators\n\n# Problem\nManual work\n\n# First test\nPilot",
        provenance=[{"type": "user", "reference": "explicit-input"}],
        confidence=0.7,
        idempotency_key="legacy-real-profile-brief",
    )
    packet = product.project_publish_review_packet(
        project_id=project["project_id"],
        source_brief_id=brief["id"],
        included_evidence_ids=[],
        included_hypothesis_ids=[],
        expected_hash=brief["content_hash"],
        idempotency_key="legacy-real-profile-packet",
    )
    assert reviewer.context_get(packet["id"])["id"] == packet["id"]
    review = reviewer.review_record(
        project_id=project["project_id"],
        packet_id=packet["id"],
        verdict="GO_IF",
        content="Proceed after review",
        confidence=0.7,
        idempotency_key="legacy-real-profile-review",
    )
    assert review["id"]
