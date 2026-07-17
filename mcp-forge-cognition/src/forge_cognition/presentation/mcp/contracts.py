"""Pydantic contracts for every mutation exposed over MCP."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SearchRequest(Contract):
    query: str
    project_id: str | None = None
    entity_types: list[str] = Field(default_factory=list)
    statuses: list[str] = Field(default_factory=list)
    valid_at: date | None = None
    limit: int = Field(default=10, ge=1, le=50)


class ProposalRequest(Contract):
    entity_type: str
    project_id: str | None = None
    title: str
    content: str
    provenance: list[dict[str, str]]
    confidence: float = Field(ge=0, le=1)
    idempotency_key: str
    attributes: dict = Field(default_factory=dict)


class CommitRequest(Contract):
    candidate_id: str
    decision: str
    target_namespace: str
    expected_hash: str
    idempotency_key: str
    reason: str


class DeprecateRequest(Contract):
    memory_id: str
    reason: str
    superseded_by: str | None = None
    expected_hash: str
    idempotency_key: str


class FeedbackRequest(Contract):
    memory_id: str
    outcome_id: str
    feedback_type: str
    evidence: str
    confidence: float = Field(ge=0, le=1)
    idempotency_key: str


class ProjectCreateRequest(Contract):
    name: str
    slug: str
    objective: str
    owner: str
    initial_constraints: list[str] = Field(default_factory=list)
    idempotency_key: str


class PublishPacketRequest(Contract):
    project_id: str
    source_brief_id: str
    included_evidence_ids: list[str] = Field(default_factory=list)
    included_hypothesis_ids: list[str] = Field(default_factory=list)
    expected_hash: str
    idempotency_key: str


class OutcomeRequest(Contract):
    project_id: str
    experiment_id: str | None = None
    outcome_type: str
    metric: str
    value: float | str
    unit: str
    observed_at: datetime
    source: str
    evidence: str
    idempotency_key: str
