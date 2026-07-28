from __future__ import annotations

import pytest

from forge_cognition.domain.errors import AccessDeniedError, ConflictError, ValidationError
from forge_cognition.domain.models import Principal


def cdc_payload(label: str = "v1") -> dict:
    return {
        "problem": f"Unreviewed design {label}",
        "target_users": ["project owners"],
        "desired_outcomes": ["development-ready handoff"],
        "constraints": ["no product implementation"],
        "acceptance_criteria": ["independent review"],
        "assumptions": [],
        "evidence": ["explicit user request"],
        "unknowns": [],
        "non_goals": ["application code"],
    }


def architecture_payload(label: str = "v1") -> dict:
    return {
        "summary": f"Bounded architecture {label}",
        "components": ["existing cognition MCP"],
        "data_contracts": ["append-only handoffs"],
        "interfaces": ["role-scoped MCP tools"],
        "security": ["deny by default"],
        "failure_modes": ["stale artifact"],
        "test_strategy": ["ACL and state tests"],
        "rollout": ["preflight then install"],
        "alternatives": ["no second MCP"],
        "assumptions": [],
        "evidence": ["repository inspection"],
        "unknowns": [],
        "file_impacts": ["mcp-forge-cognition"],
    }


def start_review(services, suffix: str = "one") -> tuple[str, dict, dict, dict]:
    product = services[Principal.FORGE_PRODUCT]
    architect = services[Principal.ARCHITECT_BRAINSTORM]
    curator = services[Principal.CURATOR]
    project = product.pipeline_project_create(
        name="Pipeline",
        slug=f"pipeline-{suffix}",
        objective="Reach reviewed design",
        owner="raphael",
        initial_constraints=[],
        idempotency_key=f"{suffix}-project",
    )
    project_id = project["project_id"]
    cdc = product.pipeline_publish_cdc(
        project_id=project_id,
        payload=cdc_payload(),
        idempotency_key=f"{suffix}-cdc",
    )
    with pytest.raises(AccessDeniedError):
        architect.pipeline_publish_architecture(
            project_id=project_id,
            payload=architecture_payload(),
            cdc_id=cdc["id"],
            cdc_revision=cdc["revision"],
            cdc_hash=cdc["content_hash"],
            idempotency_key=f"{suffix}-premature-architecture",
        )
    approval = curator.pipeline_approve_cdc(
        project_id=project_id,
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        human_decision_id=f"human-{suffix}",
        idempotency_key=f"{suffix}-approve-cdc",
    )
    latest_state, latest_document = curator.store.latest_pipeline_state(project_id)
    assert approval["id"] == latest_document.id
    assert approval["revision"] == latest_document.revision
    assert approval["content_hash"] == latest_document.content_hash
    assert latest_state.stage.value == "CDC_APPROVED"
    architecture = architect.pipeline_publish_architecture(
        project_id=project_id,
        payload=architecture_payload(),
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        idempotency_key=f"{suffix}-architecture",
    )
    packet = curator.pipeline_approve_architecture(
        project_id=project_id,
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        architecture_id=architecture["id"],
        architecture_revision=architecture["revision"],
        architecture_hash=architecture["content_hash"],
        included_evidence_ids=[],
        idempotency_key=f"{suffix}-approve-architecture",
    )
    return project_id, cdc, architecture, packet


def test_go_pipeline_creates_immutable_development_handoff(services) -> None:
    reviewer = services[Principal.RED_TEAM]
    curator = services[Principal.CURATOR]
    project_id, cdc, architecture, packet = start_review(services)
    verdict = reviewer.pipeline_record_verdict(
        project_id=project_id,
        packet_id=packet["id"],
        packet_revision=packet["revision"],
        packet_hash=packet["content_hash"],
        payload={
            "verdict": "GO_DEV_WITH_CONDITIONS",
            "findings": [],
            "conditions": ["run security tests"],
            "cdc_rework": [],
            "architecture_rework": [],
        },
        idempotency_key="one-verdict",
    )
    handoff = curator.pipeline_create_development_handoff(
        project_id=project_id,
        verdict_id=verdict["id"],
        verdict_revision=verdict["revision"],
        verdict_hash=verdict["content_hash"],
        adrs=["Use existing cognition store"],
        slices=[
            {
                "id": "slice-1",
                "objective": "Implement bounded change",
                "acceptance_criteria": ["all tests pass"],
                "tests": ["unit and integration"],
            }
        ],
        risks=["runtime compatibility"],
        idempotency_key="one-development-handoff",
    )
    body = curator.context_get(handoff["id"])
    assert body["attributes"]["artifact_type"] == "development_handoff"
    assert cdc["id"] in body["body"]
    assert architecture["id"] in body["body"]


def test_stale_packet_cannot_authorize_verdict(services) -> None:
    reviewer = services[Principal.RED_TEAM]
    project_id, _, _, packet = start_review(services, "stale")
    with pytest.raises(ConflictError):
        reviewer.pipeline_record_verdict(
            project_id=project_id,
            packet_id=packet["id"],
            packet_revision=packet["revision"],
            packet_hash="sha256:" + "0" * 64,
            payload={
                "verdict": "GO_DEV",
                "findings": [],
                "conditions": [],
                "cdc_rework": [],
                "architecture_rework": [],
            },
            idempotency_key="stale-verdict",
        )


def test_two_reworks_require_curator_human_decision(services) -> None:
    architect = services[Principal.ARCHITECT_BRAINSTORM]
    reviewer = services[Principal.RED_TEAM]
    curator = services[Principal.CURATOR]
    project_id, cdc, architecture, packet = start_review(services, "rework")
    first = reviewer.pipeline_record_verdict(
        project_id=project_id,
        packet_id=packet["id"],
        packet_revision=packet["revision"],
        packet_hash=packet["content_hash"],
        payload={
            "verdict": "REWORK_ARCHITECTURE",
            "findings": ["missing failure mode"],
            "conditions": [],
            "cdc_rework": [],
            "architecture_rework": ["add failure mode"],
        },
        idempotency_key="rework-first-verdict",
    )
    assert first["stage"] == "REWORK_ARCHITECTURE"
    architecture2 = architect.pipeline_publish_architecture(
        project_id=project_id,
        payload=architecture_payload("v2"),
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        expected_previous_id=architecture["id"],
        expected_previous_revision=architecture["revision"],
        expected_previous_hash=architecture["content_hash"],
        idempotency_key="rework-architecture-v2",
    )
    packet2 = curator.pipeline_approve_architecture(
        project_id=project_id,
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        architecture_id=architecture2["id"],
        architecture_revision=architecture2["revision"],
        architecture_hash=architecture2["content_hash"],
        included_evidence_ids=[],
        idempotency_key="rework-approve-v2",
    )
    assert packet2["revision"] == 2
    second = reviewer.pipeline_record_verdict(
        project_id=project_id,
        packet_id=packet2["id"],
        packet_revision=packet2["revision"],
        packet_hash=packet2["content_hash"],
        payload={
            "verdict": "REWORK_ARCHITECTURE",
            "findings": ["still incomplete"],
            "conditions": [],
            "cdc_rework": [],
            "architecture_rework": ["complete it"],
        },
        idempotency_key="rework-second-verdict",
    )
    assert second["revision"] == 2
    assert second["human_gate_required"] is True
    with pytest.raises(ValidationError, match="human decision"):
        architect.pipeline_publish_architecture(
            project_id=project_id,
            payload=architecture_payload("v3"),
            cdc_id=cdc["id"],
            cdc_revision=cdc["revision"],
            cdc_hash=cdc["content_hash"],
            expected_previous_id=architecture2["id"],
            expected_previous_revision=architecture2["revision"],
            expected_previous_hash=architecture2["content_hash"],
            idempotency_key="rework-architecture-blocked",
        )
    decision = curator.pipeline_record_human_rework_decision(
        project_id=project_id,
        scope="ARCHITECTURE",
        decision_id="human-rework-approved",
        confirmed=True,
        idempotency_key="rework-human-decision",
    )
    latest_state, latest_document = curator.store.latest_pipeline_state(project_id)
    assert decision["id"] == latest_document.id
    assert decision["revision"] == latest_document.revision
    assert decision["content_hash"] == latest_document.content_hash
    assert latest_state.human_gate_required is False
    resumed = architect.pipeline_publish_architecture(
        project_id=project_id,
        payload=architecture_payload("v3"),
        cdc_id=cdc["id"],
        cdc_revision=cdc["revision"],
        cdc_hash=cdc["content_hash"],
        expected_previous_id=architecture2["id"],
        expected_previous_revision=architecture2["revision"],
        expected_previous_hash=architecture2["content_hash"],
        idempotency_key="rework-architecture-v3",
    )
    assert resumed["revision"] == 3


@pytest.mark.parametrize(
    ("verdict", "conditions", "cdc_rework", "architecture_rework"),
    [
        ("GO_DEV", [], [], []),
        ("GO_DEV_WITH_CONDITIONS", ["condition"], [], []),
        ("REWORK_CDC", [], ["clarify scope"], []),
        ("REWORK_ARCHITECTURE", [], [], ["add failure mode"]),
        ("PARK", [], [], []),
        ("KILL", [], [], []),
    ],
)
def test_every_closed_verdict_is_routed_server_side(
    services, verdict, conditions, cdc_rework, architecture_rework
) -> None:
    suffix = f"verdict-{verdict.lower().replace('_', '-')}"
    reviewer = services[Principal.RED_TEAM]
    project_id, _, _, packet = start_review(services, suffix)
    result = reviewer.pipeline_record_verdict(
        project_id=project_id,
        packet_id=packet["id"],
        packet_revision=packet["revision"],
        packet_hash=packet["content_hash"],
        payload={
            "verdict": verdict,
            "findings": [],
            "conditions": conditions,
            "cdc_rework": cdc_rework,
            "architecture_rework": architecture_rework,
        },
        idempotency_key=f"{suffix}-record",
    )
    assert result["stage"] == verdict


def test_pipeline_artifact_and_state_roll_back_together_on_index_failure(
    services, monkeypatch
) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = product.pipeline_project_create(
        name="Rollback",
        slug="pipeline-rollback",
        objective="Remain atomic",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="pipeline-rollback-project",
    )
    original = product.indexes.rebuild_all
    calls = 0

    def fail_once():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("injected index failure")
        original()

    monkeypatch.setattr(product.indexes, "rebuild_all", fail_once)
    with pytest.raises(RuntimeError, match="injected index failure"):
        product.pipeline_publish_cdc(
            project_id=project["project_id"],
            payload=cdc_payload(),
            idempotency_key="pipeline-rollback-cdc",
        )
    state, _ = product.store.latest_pipeline_state(project["project_id"])
    assert state.stage.value == "DISCOVERY"
    assert product.store.resolve_pipeline_series(
        project["project_id"], f"{project['project_id']}:cdc"
    ) == []
