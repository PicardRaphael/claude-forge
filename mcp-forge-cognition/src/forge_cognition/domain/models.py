"""Typed domain entities and lifecycle rules."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .errors import ImmutableEntityError, ValidationError


class Principal(StrEnum):
    FORGE_PRODUCT = "forge-product"
    RED_TEAM = "red-team"
    CURATOR = "curator"


class EntityType(StrEnum):
    CONTEXT = "context"
    EVIDENCE = "evidence"
    HYPOTHESIS = "hypothesis"
    DECISION = "decision"
    EPISODE = "episode"
    EXPERIMENT = "experiment"
    OUTCOME = "outcome"
    REVIEW = "review"
    LESSON = "lesson"
    PROCEDURE = "procedure"
    CALIBRATION = "calibration"
    RETROSPECTIVE = "retrospective"


class MemoryType(StrEnum):
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    CALIBRATION = "calibration"


class Status(StrEnum):
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REJECTED = "rejected"
    RESTRICTED = "restricted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class ValidationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    reference: str


class CognitionDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    id: str = Field(pattern=r"^[0-9A-HJKMNP-TV-Z]{26}$")
    schema_version: int = 1
    entity_type: EntityType
    memory_type: MemoryType
    project_id: str | None = None
    owner: str
    namespace: str
    visibility: str
    status: Status = Status.CANDIDATE
    validation_status: ValidationStatus = ValidationStatus.PENDING
    created_at: datetime
    updated_at: datetime
    observed_at: datetime | None = None
    valid_from: date | None = None
    valid_until: date | None = None
    review_after: date | None = None
    confidence: float = Field(ge=0, le=1)
    confidence_basis: str
    provenance: list[Provenance] = Field(min_length=1)
    supersedes: str | None = None
    superseded_by: str | None = None
    outcome_ids: list[str] = Field(default_factory=list)
    content_hash: str = ""
    revision: int = Field(default=1, ge=1)
    title: str = Field(min_length=1, max_length=200)
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)
    body: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_business_rules(self) -> CognitionDocument:
        if self.entity_type == EntityType.HYPOTHESIS and self.status == Status.VALIDATED:
            if not self.attributes.get("evidence_ids"):
                raise ValueError("a validated hypothesis requires evidence_ids")
        if self.entity_type == EntityType.PROCEDURE:
            if self.attributes.get("security_exception"):
                required = {"expires_at", "review_required", "evidence_level", "incident_id"}
                if not required <= self.attributes.keys():
                    raise ValueError("a security exception procedure requires review metadata")
            else:
                if not self.attributes.get("source_episode_ids"):
                    raise ValueError("a procedure requires source_episode_ids")
                if not self.attributes.get("source_outcome_ids"):
                    raise ValueError("a procedure requires source_outcome_ids")
        return self

    def computed_hash(self) -> str:
        payload = self.model_dump(mode="json", exclude={"content_hash"})
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return f"sha256:{hashlib.sha256(encoded).hexdigest()}"

    def with_hash(self) -> CognitionDocument:
        return self.model_copy(update={"content_hash": self.computed_hash()})

    def verify_hash(self) -> None:
        if self.content_hash != self.computed_hash():
            raise ValidationError(f"content hash mismatch for {self.id}")

    def next_revision(self, now: datetime, **changes: Any) -> CognitionDocument:
        if self.entity_type == EntityType.OUTCOME:
            raise ImmutableEntityError("outcomes are immutable")
        if "status" in changes:
            current = Status(self.status)
            target = Status(changes["status"])
            allowed = {
                Status.CANDIDATE: {
                    Status.VALIDATED,
                    Status.REJECTED,
                    Status.RESTRICTED,
                    Status.ARCHIVED,
                },
                Status.VALIDATED: {
                    Status.RESTRICTED,
                    Status.DEPRECATED,
                    Status.SUPERSEDED,
                    Status.ARCHIVED,
                },
                Status.RESTRICTED: {
                    Status.VALIDATED,
                    Status.DEPRECATED,
                    Status.SUPERSEDED,
                    Status.ARCHIVED,
                },
                Status.REJECTED: {Status.ARCHIVED},
                Status.DEPRECATED: {Status.ARCHIVED},
                Status.SUPERSEDED: {Status.ARCHIVED},
                Status.ARCHIVED: set(),
            }
            if target != current and target not in allowed[current]:
                raise ValidationError(f"invalid status transition: {current} -> {target}")
        payload = self.model_dump()
        payload.update(
            {"revision": self.revision + 1, "updated_at": now, **changes, "content_hash": ""}
        )
        updated = CognitionDocument.model_validate(payload)
        return updated.with_hash()


class Project(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^PRJ-[0-9]{4}-[0-9]{3}$")
    schema_version: int = 1
    name: str
    slug: str
    status: str = "active"
    owner: str
    objective: str
    created_at: datetime
    current_stage: str = "discovery"
    success_criteria: list[str] = Field(default_factory=list)
    stop_criteria: list[str] = Field(default_factory=list)
    initial_constraints: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    revision: int = 1
    content_hash: str = ""

    def computed_hash(self) -> str:
        payload = self.model_dump(mode="json", exclude={"content_hash"})
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return f"sha256:{hashlib.sha256(encoded).hexdigest()}"

    def with_hash(self) -> Project:
        return self.model_copy(update={"content_hash": self.computed_hash()})
