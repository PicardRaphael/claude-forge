"""Strict project-brainstorm payloads and append-only workflow state."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .models import Principal


class StrictPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PipelineStage(StrEnum):
    DISCOVERY = "DISCOVERY"
    CDC_DRAFT = "CDC_DRAFT"
    CDC_APPROVED = "CDC_APPROVED"
    ARCHITECTURE_DRAFT = "ARCHITECTURE_DRAFT"
    REVIEW = "REVIEW"
    REWORK_CDC = "REWORK_CDC"
    REWORK_ARCHITECTURE = "REWORK_ARCHITECTURE"
    GO_DEV = "GO_DEV"
    GO_DEV_WITH_CONDITIONS = "GO_DEV_WITH_CONDITIONS"
    PARK = "PARK"
    KILL = "KILL"
    DEVELOPMENT_READY = "DEVELOPMENT_READY"


class ReviewVerdict(StrEnum):
    GO_DEV = "GO_DEV"
    GO_DEV_WITH_CONDITIONS = "GO_DEV_WITH_CONDITIONS"
    REWORK_CDC = "REWORK_CDC"
    REWORK_ARCHITECTURE = "REWORK_ARCHITECTURE"
    PARK = "PARK"
    KILL = "KILL"


class ArtifactPointer(StrictPayload):
    document_id: str = Field(pattern=r"^[0-9A-HJKMNP-TV-Z]{26}$")
    revision: int = Field(ge=1)
    content_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    series_id: str = Field(min_length=1)


class ProjectGrant(StrictPayload):
    principal: Principal
    project_id: str = Field(pattern=r"^PRJ-[0-9]{4}-[0-9]{3}$")
    project_access: bool = False
    artifact_bindings: list[ArtifactPointer] = Field(default_factory=list)
    status: Literal["active", "revoked"] = "active"

    def permits(self, pointer: ArtifactPointer) -> bool:
        if self.status != "active":
            return False
        return any(
            binding.document_id == pointer.document_id
            and binding.revision == pointer.revision
            and binding.content_hash == pointer.content_hash
            and binding.series_id == pointer.series_id
            for binding in self.artifact_bindings
        )


class HumanDecision(StrictPayload):
    decision_id: str = Field(min_length=1)
    scope: Literal["CDC", "ARCHITECTURE", "RESET"]
    confirmed: bool
    recorded_at: datetime


class PipelineState(StrictPayload):
    payload_schema: Literal["pipeline-state-v1"] = "pipeline-state-v1"
    project_id: str = Field(pattern=r"^PRJ-[0-9]{4}-[0-9]{3}$")
    stage: PipelineStage = PipelineStage.DISCOVERY
    pointers: dict[str, ArtifactPointer] = Field(default_factory=dict)
    grants: list[ProjectGrant] = Field(default_factory=list)
    consecutive_reworks: int = Field(default=0, ge=0)
    human_gate_required: bool = False
    human_decision: HumanDecision | None = None

    @model_validator(mode="after")
    def validate_grants(self) -> PipelineState:
        active = [grant.principal for grant in self.grants if grant.status == "active"]
        if len(active) != len(set(active)):
            raise ValueError("duplicate active grant for principal")
        if any(grant.project_id != self.project_id for grant in self.grants):
            raise ValueError("cross-project grant is forbidden")
        return self

    def active_grant(self, principal: Principal) -> ProjectGrant | None:
        return next(
            (
                grant
                for grant in self.grants
                if grant.principal == principal and grant.status == "active"
            ),
            None,
        )


class CdcHandoff(StrictPayload):
    payload_schema: Literal["cdc-handoff-v1"] = "cdc-handoff-v1"
    problem: str = Field(min_length=1)
    target_users: list[str] = Field(min_length=1)
    desired_outcomes: list[str] = Field(min_length=1)
    constraints: list[str]
    acceptance_criteria: list[str] = Field(min_length=1)
    assumptions: list[str]
    evidence: list[str]
    unknowns: list[str]
    non_goals: list[str]


class ArchitectureHandoff(StrictPayload):
    payload_schema: Literal["architecture-handoff-v1"] = "architecture-handoff-v1"
    summary: str = Field(min_length=1)
    components: list[str]
    data_contracts: list[str]
    interfaces: list[str]
    security: list[str]
    failure_modes: list[str]
    test_strategy: list[str]
    rollout: list[str]
    alternatives: list[str]
    assumptions: list[str]
    evidence: list[str]
    unknowns: list[str]
    file_impacts: list[str]


class ReviewPacket(StrictPayload):
    payload_schema: Literal["review-packet-v1"] = "review-packet-v1"
    cdc: CdcHandoff
    architecture: ArchitectureHandoff
    evidence_ids: list[str]
    factual_constraints: list[str]
    unknowns: list[str]


class ReviewVerdictHandoff(StrictPayload):
    payload_schema: Literal["review-verdict-v1"] = "review-verdict-v1"
    verdict: ReviewVerdict
    findings: list[str]
    conditions: list[str]
    cdc_rework: list[str]
    architecture_rework: list[str]

    @model_validator(mode="after")
    def validate_targeted_rework(self) -> ReviewVerdictHandoff:
        if self.verdict == ReviewVerdict.REWORK_CDC and not self.cdc_rework:
            raise ValueError("REWORK_CDC requires cdc_rework")
        if self.verdict == ReviewVerdict.REWORK_ARCHITECTURE and not self.architecture_rework:
            raise ValueError("REWORK_ARCHITECTURE requires architecture_rework")
        if self.verdict == ReviewVerdict.GO_DEV_WITH_CONDITIONS and not self.conditions:
            raise ValueError("conditional GO requires conditions")
        return self


class DevelopmentSlice(StrictPayload):
    id: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    acceptance_criteria: list[str] = Field(min_length=1)
    tests: list[str] = Field(min_length=1)


class DevelopmentHandoff(StrictPayload):
    payload_schema: Literal["development-handoff-v1"] = "development-handoff-v1"
    project_id: str
    cdc: ArtifactPointer
    architecture: ArtifactPointer
    verdict: ArtifactPointer
    adrs: list[str]
    slices: list[DevelopmentSlice] = Field(min_length=1)
    risks: list[str]
    reviewer_conditions: list[str]


PAYLOAD_MODELS = {
    "pipeline-state-v1": PipelineState,
    "cdc-handoff-v1": CdcHandoff,
    "architecture-handoff-v1": ArchitectureHandoff,
    "review-packet-v1": ReviewPacket,
    "review-verdict-v1": ReviewVerdictHandoff,
    "development-handoff-v1": DevelopmentHandoff,
}


def canonical_payload(value: BaseModel) -> str:
    return json.dumps(
        value.model_dump(mode="json"), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )


def canonical_payload_hash(value: BaseModel) -> str:
    digest = hashlib.sha256(canonical_payload(value).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def parse_payload(body: str, schema: str) -> StrictPayload:
    model = PAYLOAD_MODELS.get(schema)
    if model is None:
        raise ValueError(f"unsupported pipeline payload schema: {schema}")
    return model.model_validate_json(body)
