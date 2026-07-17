from __future__ import annotations

import sqlite3

from forge_cognition.domain.models import Principal


def test_review_packet_removes_private_persuasion_sections(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    curator = services[Principal.CURATOR]
    project = product.project_create(
        name="Neutral",
        slug="neutral",
        objective="Neutralize",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="neutral-project",
    )
    brief = product.project_write_opportunity_brief(
        project_id=project["project_id"],
        title="Brief",
        content=(
            "# Executive summary\nFacts stay.\n\n"
            "## Enthousiasme utilisateur\nSECRET CHEER\n\n"
            "## Problem\nProblem stays.\n\n"
            "## Classement initial\nRank one\n"
        ),
        provenance=[{"type": "user", "reference": "confirmed"}],
        confidence=0.7,
        idempotency_key="neutral-brief",
    )
    evidence_candidate = product.memory_propose(
        entity_type="evidence",
        project_id=project["project_id"],
        title="Confirmed interview",
        content="A user confirmed the manual workflow.",
        provenance=[{"type": "user", "reference": "interview-001"}],
        confidence=0.9,
        idempotency_key="neutral-evidence",
    )
    evidence = curator.memory_commit(
        candidate_id=evidence_candidate["id"],
        decision="validated",
        target_namespace=f"projects/{project['project_id']}-neutral/evidence",
        expected_hash=evidence_candidate["content_hash"],
        idempotency_key="neutral-evidence-commit",
        reason="Interview verified",
    )
    hypothesis_candidate = product.memory_propose(
        entity_type="hypothesis",
        project_id=project["project_id"],
        title="Users will pay",
        content="A paid pilot will convert.",
        provenance=[{"type": "document", "reference": evidence["id"]}],
        confidence=0.6,
        idempotency_key="neutral-hypothesis",
        attributes={"evidence_ids": [evidence["id"]]},
    )
    hypothesis = curator.memory_commit(
        candidate_id=hypothesis_candidate["id"],
        decision="validated",
        target_namespace=f"projects/{project['project_id']}-neutral/hypotheses",
        expected_hash=hypothesis_candidate["content_hash"],
        idempotency_key="neutral-hypothesis-commit",
        reason="Supported hypothesis, still falsifiable",
    )
    packet = product.project_publish_review_packet(
        project_id=project["project_id"],
        source_brief_id=brief["id"],
        included_evidence_ids=[evidence["id"]],
        included_hypothesis_ids=[hypothesis["id"]],
        expected_hash=brief["content_hash"],
        idempotency_key="neutral-packet",
    )
    body = services[Principal.RED_TEAM].context_get(packet["id"])["body"]
    assert "Facts stay" in body and "Problem stays" in body
    assert "Confirmed interview" in body and "Users will pay" in body
    assert "SECRET CHEER" not in body and "Rank one" not in body


def test_profile_indexes_are_physically_separate_and_filtered(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = product.project_create(
        name="Indexes",
        slug="indexes",
        objective="Separate",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="index-project",
    )
    product.episode_record(
        project_id=project["project_id"],
        title="PRIVATE-INDEX-TOKEN",
        prediction="private",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.5,
        confidence_after=0.5,
        idempotency_key="index-episode",
    )
    paths = [product.indexes.path_for(principal) for principal in Principal]
    assert len(set(paths)) == 3 and all(path.exists() for path in paths)
    reviewer = sqlite3.connect(product.indexes.path_for(Principal.RED_TEAM))
    try:
        assert (
            reviewer.execute(
                "SELECT COUNT(*) FROM documents WHERE title = 'PRIVATE-INDEX-TOKEN'"
            ).fetchone()[0]
            == 0
        )
    finally:
        reviewer.close()


def test_ranking_is_deterministic(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = product.project_create(
        name="Rank",
        slug="rank",
        objective="Rank",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="rank-project",
    )
    product.episode_record(
        project_id=project["project_id"],
        title="Lexical Alpha",
        prediction="alpha",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.5,
        confidence_after=0.5,
        idempotency_key="rank-a",
    )
    first = product.context_search("alpha")
    product.indexes.rebuild_all()
    second = product.context_search("alpha")
    assert [item["id"] for item in first["results"]] == [item["id"] for item in second["results"]]
