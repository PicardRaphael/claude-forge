"""FastMCP business-tool surface with a startup-fixed principal."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Callable

from fastmcp import FastMCP

from forge_cognition.application.service import CognitionService
from forge_cognition.domain.errors import CognitionError, ConflictError
from forge_cognition.domain.models import Principal

from .contracts import (
    CommitRequest,
    DeprecateRequest,
    FeedbackRequest,
    OutcomeRequest,
    ProjectCreateRequest,
    ProposalRequest,
    PublishPacketRequest,
    SearchRequest,
)


def _call(operation: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    try:
        return {"ok": True, "data": operation()}
    except CognitionError as exc:
        error: dict[str, Any] = {"code": exc.code, "message": str(exc)}
        if isinstance(exc, ConflictError):
            error["current_hash"] = exc.current_hash
        return {"ok": False, "error": error}
    except (TypeError, ValueError) as exc:
        return {"ok": False, "error": {"code": "validation_error", "message": str(exc)}}


def create_mcp(service: CognitionService) -> FastMCP:
    mcp = FastMCP(
        name=f"forge-cognition-{service.principal.value}",
        instructions=(
            "Operational cognition tools. The principal is fixed at startup; "
            "no tool accepts paths or identity overrides."
        ),
    )

    def register_for(*principals: Principal):
        def decorator(function):
            if not principals or service.principal in principals:
                return mcp.tool()(function)
            return function

        return decorator

    @register_for()
    def context_search(
        query: str,
        project_id: str | None = None,
        entity_types: list[str] | None = None,
        statuses: list[str] | None = None,
        valid_at: date | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search only the caller profile's pre-filtered lexical projection."""
        request = SearchRequest(
            query=query,
            project_id=project_id,
            entity_types=entity_types or [],
            statuses=statuses or [],
            valid_at=valid_at,
            limit=limit,
        )
        return _call(lambda: service.context_search(**request.model_dump()))

    @register_for()
    def context_get(id: str, revision: int | None = None) -> dict[str, Any]:
        """Get one authorized cognition document by immutable identifier."""
        return _call(lambda: service.context_get(id, revision))

    @register_for(
        Principal.FORGE_PRODUCT,
        Principal.ARCHITECT_BRAINSTORM,
        Principal.RED_TEAM,
    )
    def memory_propose(
        entity_type: str,
        project_id: str | None,
        title: str,
        content: str,
        provenance: list[dict[str, str]],
        confidence: float,
        idempotency_key: str,
        attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a candidate in the fixed principal's inbox; never writes shared memory."""
        request = ProposalRequest(
            entity_type=entity_type,
            project_id=project_id,
            title=title,
            content=content,
            provenance=provenance,
            confidence=confidence,
            idempotency_key=idempotency_key,
            attributes=attributes or {},
        )
        return _call(lambda: service.memory_propose(**request.model_dump()))

    @register_for(Principal.CURATOR)
    def memory_commit(
        candidate_id: str,
        decision: str,
        target_namespace: str,
        expected_hash: str,
        idempotency_key: str,
        reason: str,
    ) -> dict[str, Any]:
        """Curator-only validation, rejection or restriction of an inbox candidate."""
        request = CommitRequest(**locals())
        return _call(lambda: service.memory_commit(**request.model_dump()))

    @register_for()
    def memory_feedback(
        memory_id: str,
        outcome_id: str,
        feedback_type: str,
        evidence: str,
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Append immutable, outcome-linked feedback without logging full evidence."""
        request = FeedbackRequest(**locals())
        return _call(lambda: service.memory_feedback(**request.model_dump()))

    @register_for(Principal.CURATOR)
    def memory_deprecate(
        memory_id: str,
        reason: str,
        superseded_by: str | None,
        expected_hash: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Curator-only logical deprecation; never physically deletes a memory."""
        request = DeprecateRequest(**locals())
        return _call(lambda: service.memory_deprecate(**request.model_dump()))

    @register_for(Principal.FORGE_PRODUCT)
    def project_create(
        name: str,
        slug: str,
        objective: str,
        owner: str,
        initial_constraints: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Create a canonical project and its required artifact zones."""
        request = ProjectCreateRequest(**locals())
        return _call(lambda: service.project_create(**request.model_dump()))

    @register_for(Principal.FORGE_PRODUCT)
    def pipeline_project_create(
        name: str,
        slug: str,
        objective: str,
        owner: str,
        initial_constraints: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Create a project with append-only pipeline state and a Product owner grant."""
        arguments = locals()
        return _call(lambda: service.pipeline_project_create(**arguments))

    @register_for(Principal.FORGE_PRODUCT)
    def pipeline_publish_cdc(
        project_id: str,
        payload: dict[str, Any],
        idempotency_key: str,
        expected_previous_id: str | None = None,
        expected_previous_revision: int | None = None,
        expected_previous_hash: str | None = None,
    ) -> dict[str, Any]:
        """Append a strict CDC revision bound to any previous current revision."""
        arguments = locals()
        return _call(lambda: service.pipeline_publish_cdc(**arguments))

    @register_for(Principal.CURATOR)
    def pipeline_approve_cdc(
        project_id: str,
        cdc_id: str,
        cdc_revision: int,
        cdc_hash: str,
        human_decision_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Record explicit human CDC approval and grant the exact CDC to Architect."""
        arguments = locals()
        return _call(lambda: service.pipeline_approve_cdc(**arguments))

    @register_for(Principal.ARCHITECT_BRAINSTORM)
    def pipeline_publish_architecture(
        project_id: str,
        payload: dict[str, Any],
        cdc_id: str,
        cdc_revision: int,
        cdc_hash: str,
        idempotency_key: str,
        expected_previous_id: str | None = None,
        expected_previous_revision: int | None = None,
        expected_previous_hash: str | None = None,
    ) -> dict[str, Any]:
        """Append architecture only from the exact curator-approved CDC."""
        arguments = locals()
        return _call(lambda: service.pipeline_publish_architecture(**arguments))

    @register_for(Principal.CURATOR)
    def pipeline_approve_architecture(
        project_id: str,
        cdc_id: str,
        cdc_revision: int,
        cdc_hash: str,
        architecture_id: str,
        architecture_revision: int,
        architecture_hash: str,
        included_evidence_ids: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Approve exact inputs and publish a structurally neutral reviewer packet."""
        arguments = locals()
        return _call(lambda: service.pipeline_approve_architecture(**arguments))

    @register_for(Principal.RED_TEAM)
    def pipeline_record_verdict(
        project_id: str,
        packet_id: str,
        packet_revision: int,
        packet_hash: str,
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Record one closed verdict against the exact current review packet."""
        arguments = locals()
        return _call(lambda: service.pipeline_record_verdict(**arguments))

    @register_for(Principal.CURATOR)
    def pipeline_record_human_rework_decision(
        project_id: str,
        scope: str,
        decision_id: str,
        confirmed: bool,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Resume a gated rework only after an explicit scoped human decision."""
        arguments = locals()
        return _call(lambda: service.pipeline_record_human_rework_decision(**arguments))

    @register_for(Principal.CURATOR)
    def pipeline_create_development_handoff(
        project_id: str,
        verdict_id: str,
        verdict_revision: int,
        verdict_hash: str,
        adrs: list[str],
        slices: list[dict[str, Any]],
        risks: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Create an immutable DEV handoff only from a compatible current verdict."""
        arguments = locals()
        return _call(lambda: service.pipeline_create_development_handoff(**arguments))

    @register_for()
    def project_get(project_id: str) -> dict[str, Any]:
        """Return the profile-authorized project projection."""
        return _call(lambda: service.project_get(project_id))

    @register_for(Principal.FORGE_PRODUCT)
    def project_write_opportunity_brief(
        project_id: str,
        title: str,
        content: str,
        provenance: list[dict[str, str]],
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Forge Product writes a neutral opportunity brief without arbitrary file access."""
        return _call(
            lambda: service.project_write_opportunity_brief(
                project_id=project_id,
                title=title,
                content=content,
                provenance=provenance,
                confidence=confidence,
                idempotency_key=idempotency_key,
            )
        )

    @register_for(Principal.FORGE_PRODUCT)
    def project_publish_review_packet(
        project_id: str,
        source_brief_id: str,
        included_evidence_ids: list[str],
        included_hypothesis_ids: list[str],
        expected_hash: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Publish a traceable, deterministically neutralized review packet."""
        request = PublishPacketRequest(**locals())
        return _call(lambda: service.project_publish_review_packet(**request.model_dump()))

    @register_for(
        Principal.FORGE_PRODUCT,
        Principal.ARCHITECT_BRAINSTORM,
        Principal.RED_TEAM,
    )
    def episode_record(
        project_id: str,
        title: str,
        prediction: str,
        actual_outcome: str | None,
        error_types: list[str],
        procedures_used: list[str],
        candidate_lessons: list[str],
        confidence_before: float,
        confidence_after: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Record a private episode in the fixed Product or Red Team namespace."""
        payload = {
            "project_id": project_id,
            "title": title,
            "prediction": prediction,
            "actual_outcome": actual_outcome,
            "error_types": error_types,
            "procedures_used": procedures_used,
            "candidate_lessons": candidate_lessons,
            "confidence_before": confidence_before,
            "confidence_after": confidence_after,
            "idempotency_key": idempotency_key,
        }
        return _call(lambda: service.episode_record(**payload))

    @register_for(Principal.RED_TEAM)
    def review_record(
        project_id: str,
        packet_id: str,
        verdict: str,
        content: str,
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Red Team records a project review against an authorized review packet."""
        payload = {
            "project_id": project_id,
            "packet_id": packet_id,
            "verdict": verdict,
            "content": content,
            "confidence": confidence,
            "idempotency_key": idempotency_key,
        }
        return _call(lambda: service.review_record(**payload))

    @register_for(Principal.CURATOR)
    def project_record_outcome(
        project_id: str,
        experiment_id: str | None,
        outcome_type: str,
        metric: str,
        value: float | str,
        unit: str,
        observed_at: datetime,
        source: str,
        evidence: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Curator records an immutable real-world outcome."""
        request = OutcomeRequest(**locals())
        return _call(lambda: service.project_record_outcome(**request.model_dump()))

    @register_for()
    def procedure_search(
        query: str, project_id: str | None = None, limit: int = 10
    ) -> dict[str, Any]:
        """Search validated or restricted procedures visible to this profile."""
        return _call(lambda: service.procedure_search(query, project_id, limit))

    @register_for()
    def system_health() -> dict[str, Any]:
        """Return non-private store, index and migration health metadata."""
        return _call(service.system_health)

    return mcp
