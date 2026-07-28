"""Authorized use cases for operational cognition."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime
from typing import Any

from forge_cognition.domain.errors import (
    AccessDeniedError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from forge_cognition.domain.learning import procedure_promotion_eligible
from forge_cognition.domain.models import (
    CognitionDocument,
    EntityType,
    MemoryType,
    Principal,
    Project,
    Provenance,
    Status,
    ValidationStatus,
)
from forge_cognition.domain.policies import AccessPolicy
from forge_cognition.application.authorization import PipelineAuthorization
from forge_cognition.domain.pipeline import (
    ArchitectureHandoff,
    ArtifactPointer,
    CdcHandoff,
    DevelopmentHandoff,
    HumanDecision,
    PipelineStage,
    PipelineState,
    ProjectGrant,
    ReviewPacket,
    ReviewVerdict,
    ReviewVerdictHandoff,
    canonical_payload,
    parse_payload,
)
from forge_cognition.infrastructure.clock import SystemClock
from forge_cognition.infrastructure.file_store import FileCanonicalStore
from forge_cognition.infrastructure.ids import UlidGenerator
from forge_cognition.infrastructure.lexical_index import SQLiteLexicalIndex
from forge_cognition.infrastructure.transactions import MutationCoordinator
from forge_cognition.infrastructure.verification import StoreVerifier


_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_FORBIDDEN_REVIEW_HEADERS = {
    "enthousiasme utilisateur",
    "classement initial",
    "réflexion privée",
    "reflexion privee",
    "arguments de vente",
    "tentatives de défense",
    "tentatives de defense",
}


class CognitionService:
    def __init__(
        self,
        principal: Principal,
        policy: AccessPolicy,
        store: FileCanonicalStore,
        indexes: SQLiteLexicalIndex,
        transactions: MutationCoordinator,
        authorization: PipelineAuthorization | None = None,
        *,
        clock: SystemClock | None = None,
        ids: UlidGenerator | None = None,
    ) -> None:
        self.principal = principal
        self.policy = policy
        self.store = store
        self.indexes = indexes
        self.transactions = transactions
        self.authorization = authorization
        self.clock = clock or SystemClock()
        self.ids = ids or UlidGenerator()

    def context_search(
        self,
        query: str,
        project_id: str | None = None,
        entity_types: list[str] | None = None,
        statuses: list[str] | None = None,
        valid_at: date | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        if valid_at is not None:
            self._validate_iso_date(valid_at)
        rows = self.indexes.search(
            self.principal,
            query,
            {
                "project_id": [project_id] if project_id else [],
                "entity_type": entity_types or [],
                "status": statuses or [],
                "limit": limit,
            },
        )
        if valid_at is not None:
            rows = [
                row
                for row in rows
                if self._document_valid_at(self.store.get_document(row["id"])[0], valid_at)
            ]
        return {
            "results": [
                {
                    "id": row["id"],
                    "entity_type": row["entity_type"],
                    "title": row["title"],
                    "excerpt": row["excerpt"],
                    "status": row["status"],
                    "confidence": row["confidence"],
                    "provenance_summary": row["provenance_summary"],
                    "revision": row["revision"],
                }
                for row in rows
            ]
        }

    def context_get(self, document_id: str, revision: int | None = None) -> dict[str, Any]:
        document, relative_path = self._get_authorized_document(document_id)
        if revision is not None and revision != document.revision:
            raise NotFoundError("resource not found")
        return document.model_dump(mode="json")

    def memory_propose(
        self,
        *,
        entity_type: str,
        project_id: str | None,
        title: str,
        content: str,
        provenance: list[dict[str, str]],
        confidence: float,
        idempotency_key: str,
        attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.principal == Principal.CURATOR:
            raise AccessDeniedError("resource not found")
        if project_id and not self._project_allowed(project_id):
            raise AccessDeniedError("resource not found")
        kind = EntityType(entity_type)
        if kind == EntityType.OUTCOME:
            raise ValidationError("use project_record_outcome for immutable outcomes")
        namespace = self.policy.proposal_namespace()
        document = self._new_document(
            entity_type=kind,
            memory_type=self._memory_type(kind),
            project_id=project_id,
            owner=self.principal.value,
            namespace=namespace,
            visibility="restricted",
            title=title,
            body=content,
            provenance=provenance,
            confidence=confidence,
            attributes=attributes,
        )
        path = self.store.document_path(namespace, document.id)
        payload = {
            "entity_type": entity_type,
            "project_id": project_id,
            "title": title,
            "content": content,
            "provenance": provenance,
            "confidence": confidence,
            "attributes": attributes or {},
        }
        return self.transactions.execute(
            action="memory_propose",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload=payload,
            mutate=lambda tx: self._write_document(tx, path, document),
            result_payload=self._document_result,
        )

    def memory_commit(
        self,
        *,
        candidate_id: str,
        decision: str,
        target_namespace: str,
        expected_hash: str,
        idempotency_key: str,
        reason: str,
    ) -> dict[str, Any]:
        self._require_curator()
        if decision not in {"validated", "rejected", "restricted"}:
            raise ValidationError("invalid curator decision")

        def mutate(tx):
            candidate, source_path = self.store.get_document(candidate_id)
            if not source_path.startswith("inbox/"):
                raise NotFoundError("resource not found")
            allowed_target = self._commit_target(candidate)
            if target_namespace != allowed_target:
                raise ValidationError(f"target_namespace must be {allowed_target}")
            self._require_hash(candidate, expected_hash)
            if candidate.entity_type == EntityType.PROCEDURE and decision == "validated":
                self._require_procedure_evidence(candidate)
            if (
                candidate.entity_type == EntityType.PROCEDURE
                and decision == "restricted"
                and not candidate.attributes.get("security_exception")
            ):
                raise ValidationError(
                    "immediate procedure restriction requires a security incident"
                )
            now = self.clock.now()
            status = Status(decision)
            validation = (
                ValidationStatus.REJECTED
                if status == Status.REJECTED
                else ValidationStatus.APPROVED
            )
            namespace = target_namespace if status != Status.REJECTED else "archive"
            committed = candidate.next_revision(
                now,
                namespace=namespace,
                owner="shared" if status != Status.REJECTED else candidate.owner,
                visibility="shared" if status == Status.VALIDATED else "restricted",
                status=status,
                validation_status=validation,
                attributes={**candidate.attributes, "curator_reason": reason},
            )
            target = self.store.document_path(namespace, committed.id)
            tx.move(source_path, target)
            return self._write_document(tx, target, committed)

        return self.transactions.execute(
            action="memory_commit",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "candidate_id": candidate_id,
                "decision": decision,
                "target_namespace": target_namespace,
                "expected_hash": expected_hash,
                "reason": reason,
            },
            mutate=mutate,
            result_payload=self._document_result,
        )

    def memory_deprecate(
        self,
        *,
        memory_id: str,
        reason: str,
        superseded_by: str | None,
        expected_hash: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        self._require_curator()

        def mutate(tx):
            document, path = self.store.get_document(memory_id)
            self._require_hash(document, expected_hash)
            if superseded_by:
                replacement, replacement_path = self.store.get_document(superseded_by)
                if replacement.entity_type == EntityType.OUTCOME:
                    raise ValidationError("an immutable outcome cannot supersede a memory")
                replacement = replacement.next_revision(self.clock.now(), supersedes=document.id)
                self._write_document(tx, replacement_path, replacement)
            updated = document.next_revision(
                self.clock.now(),
                status=Status.SUPERSEDED if superseded_by else Status.DEPRECATED,
                superseded_by=superseded_by,
                attributes={**document.attributes, "deprecation_reason": reason},
            )
            return self._write_document(tx, path, updated)

        return self.transactions.execute(
            action="memory_deprecate",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "memory_id": memory_id,
                "reason": reason,
                "superseded_by": superseded_by,
                "expected_hash": expected_hash,
            },
            mutate=mutate,
            result_payload=self._document_result,
        )

    def memory_feedback(
        self,
        *,
        memory_id: str,
        outcome_id: str,
        feedback_type: str,
        evidence: str,
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        memory, _ = self._get_authorized_document(memory_id)
        outcome, outcome_path = self.store.get_document(outcome_id)
        if outcome.entity_type != EntityType.OUTCOME or not self.policy.can_read(
            outcome_path, outcome.project_id
        ):
            raise NotFoundError("resource not found")
        evidence_hash = f"sha256:{hashlib.sha256(evidence.encode('utf-8')).hexdigest()}"
        event = {
            "memory_id": memory.id,
            "outcome_id": outcome.id,
            "feedback_type": feedback_type,
            "evidence_hash": evidence_hash,
            "confidence": confidence,
            "observed_at": self.clock.now().isoformat(),
        }

        def mutate(tx):
            relative = "audit/feedback.jsonl"
            path = self.store.paths.resolve(relative, must_exist=False)
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            tx.write_text(relative, existing + json.dumps(event, sort_keys=True) + "\n")
            return event

        return self.transactions.execute(
            action="memory_feedback",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={**event, "evidence": evidence},
            mutate=mutate,
            result_payload=lambda value: value,
        )

    def project_create(
        self,
        *,
        name: str,
        slug: str,
        objective: str,
        owner: str,
        initial_constraints: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.FORGE_PRODUCT:
            raise AccessDeniedError("resource not found")
        if not _SLUG.fullmatch(slug):
            raise ValidationError("slug must be lowercase kebab-case")

        def mutate(tx):
            year = self.clock.now().year
            existing = list((self.store.root / "projects").glob(f"PRJ-{year}-*"))
            numbers = []
            for path in existing:
                try:
                    numbers.append(int(path.name.split("-", 3)[2]))
                except (IndexError, ValueError):
                    continue
            project_id = f"PRJ-{year}-{max(numbers, default=0) + 1:03d}"
            project = Project(
                id=project_id,
                name=name,
                slug=slug,
                owner=owner,
                objective=objective,
                created_at=self.clock.now(),
                initial_constraints=initial_constraints,
            ).with_hash()
            folder = f"projects/{project_id}-{slug}"
            for zone in (
                "neutral",
                "evidence",
                "hypotheses",
                "decisions",
                "experiments",
                "reviews",
                "outcomes",
                "retrospective",
            ):
                tx.mkdir(f"{folder}/{zone}")
            tx.write_text(f"{folder}/project.yaml", self.store.serialize_project(project))
            return project

        return self.transactions.execute(
            action="project_create",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "name": name,
                "slug": slug,
                "objective": objective,
                "owner": owner,
                "initial_constraints": initial_constraints,
            },
            mutate=mutate,
            result_payload=lambda project: {
                "project_id": project.id,
                "name": project.name,
                "status": project.status,
                "content_hash": project.content_hash,
            },
        )

    def pipeline_project_create(
        self,
        *,
        name: str,
        slug: str,
        objective: str,
        owner: str,
        initial_constraints: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.FORGE_PRODUCT:
            raise AccessDeniedError("resource not found")
        if not _SLUG.fullmatch(slug):
            raise ValidationError("slug must be lowercase kebab-case")

        def mutate(tx):
            project = self._create_project_value(name, slug, objective, owner, initial_constraints)
            folder = f"projects/{project.id}-{slug}"
            self._create_project_folders(tx, folder)
            tx.write_text(f"{folder}/project.yaml", self.store.serialize_project(project))
            state = PipelineState(
                project_id=project.id,
                grants=[
                    ProjectGrant(
                        principal=Principal.FORGE_PRODUCT,
                        project_id=project.id,
                        project_access=True,
                    )
                ],
            )
            state_document = self._append_pipeline_state(tx, folder, state, None)
            return project, state_document

        return self.transactions.execute(
            action="pipeline_project_create",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "name": name,
                "slug": slug,
                "objective": objective,
                "owner": owner,
                "initial_constraints": initial_constraints,
            },
            mutate=mutate,
            result_payload=lambda value: {
                "project_id": value[0].id,
                "name": value[0].name,
                "status": value[0].status,
                "content_hash": value[0].content_hash,
                "pipeline_state_id": value[1].id,
            },
        )

    def pipeline_publish_cdc(
        self,
        *,
        project_id: str,
        payload: dict[str, Any],
        idempotency_key: str,
        expected_previous_id: str | None = None,
        expected_previous_revision: int | None = None,
        expected_previous_hash: str | None = None,
    ) -> dict[str, Any]:
        if self.principal != Principal.FORGE_PRODUCT:
            raise AccessDeniedError("resource not found")
        handoff = CdcHandoff.model_validate(payload)

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage not in {
                PipelineStage.DISCOVERY,
                PipelineStage.CDC_DRAFT,
                PipelineStage.REWORK_CDC,
            }:
                raise ValidationError("CDC cannot be published in the current stage")
            self._require_human_gate_clear(state)
            previous = state.pointers.get("cdc")
            self._require_previous_binding(
                previous,
                expected_previous_id,
                expected_previous_revision,
                expected_previous_hash,
            )
            folder = self._project_folder(project_id)
            document = self._new_pipeline_artifact(
                project_id=project_id,
                namespace=f"{folder}/neutral",
                artifact_type="cdc",
                entity_type=EntityType.CONTEXT,
                payload=handoff,
                previous=previous,
            )
            document = self._write_document(
                tx, self.store.document_path(document.namespace, document.id), document
            )
            pointer = self._pipeline_pointer(document)
            product_grant = ProjectGrant(
                principal=Principal.FORGE_PRODUCT,
                project_id=project_id,
                project_access=True,
                artifact_bindings=[pointer],
            )
            updated = state.model_copy(
                update={
                    "stage": PipelineStage.CDC_DRAFT,
                    "pointers": {"cdc": pointer},
                    "grants": [product_grant],
                }
            )
            self._append_pipeline_state(tx, folder, updated, state_document)
            return document, updated

        return self._pipeline_transaction(
            "pipeline_publish_cdc",
            idempotency_key,
            {
                "project_id": project_id,
                "payload": handoff.model_dump(mode="json"),
                "expected_previous_id": expected_previous_id,
                "expected_previous_revision": expected_previous_revision,
                "expected_previous_hash": expected_previous_hash,
            },
            mutate,
        )

    def pipeline_approve_cdc(
        self,
        *,
        project_id: str,
        cdc_id: str,
        cdc_revision: int,
        cdc_hash: str,
        human_decision_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        self._require_curator()

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage != PipelineStage.CDC_DRAFT:
                raise ValidationError("CDC approval requires CDC_DRAFT")
            cdc = self._require_current_pointer(state, "cdc", cdc_id, cdc_revision, cdc_hash)
            architect_grant = ProjectGrant(
                principal=Principal.ARCHITECT_BRAINSTORM,
                project_id=project_id,
                project_access=True,
                artifact_bindings=[cdc],
            )
            updated = state.model_copy(
                update={
                    "stage": PipelineStage.CDC_APPROVED,
                    "grants": self._replace_grant(state.grants, architect_grant),
                    "human_decision": HumanDecision(
                        decision_id=human_decision_id,
                        scope="CDC",
                        confirmed=True,
                        recorded_at=self.clock.now(),
                    ),
                }
            )
            appended_state = self._append_pipeline_state(
                tx, self._project_folder(project_id), updated, state_document
            )
            return appended_state, updated

        return self._pipeline_transaction(
            "pipeline_approve_cdc",
            idempotency_key,
            {
                "project_id": project_id,
                "cdc_id": cdc_id,
                "cdc_revision": cdc_revision,
                "cdc_hash": cdc_hash,
                "human_decision_id": human_decision_id,
            },
            mutate,
        )

    def pipeline_publish_architecture(
        self,
        *,
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
        if self.principal != Principal.ARCHITECT_BRAINSTORM:
            raise AccessDeniedError("resource not found")
        handoff = ArchitectureHandoff.model_validate(payload)

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage not in {
                PipelineStage.CDC_APPROVED,
                PipelineStage.REWORK_ARCHITECTURE,
            }:
                raise AccessDeniedError("resource not found")
            self._require_human_gate_clear(state)
            cdc = self._require_current_pointer(state, "cdc", cdc_id, cdc_revision, cdc_hash)
            grant = state.active_grant(self.principal)
            if grant is None or not grant.permits(cdc):
                raise AccessDeniedError("resource not found")
            previous = state.pointers.get("architecture")
            self._require_previous_binding(
                previous,
                expected_previous_id,
                expected_previous_revision,
                expected_previous_hash,
            )
            folder = self._project_folder(project_id)
            document = self._new_pipeline_artifact(
                project_id=project_id,
                namespace=f"{folder}/decisions",
                artifact_type="architecture",
                entity_type=EntityType.DECISION,
                payload=handoff,
                previous=previous,
            )
            document = self._write_document(
                tx, self.store.document_path(document.namespace, document.id), document
            )
            architecture = self._pipeline_pointer(document)
            architect_grant = ProjectGrant(
                principal=self.principal,
                project_id=project_id,
                project_access=True,
                artifact_bindings=[cdc, architecture],
            )
            updated = state.model_copy(
                update={
                    "stage": PipelineStage.ARCHITECTURE_DRAFT,
                    "pointers": {"cdc": cdc, "architecture": architecture},
                    "grants": self._replace_grant(state.grants, architect_grant),
                }
            )
            self._append_pipeline_state(tx, folder, updated, state_document)
            return document, updated

        return self._pipeline_transaction(
            "pipeline_publish_architecture",
            idempotency_key,
            {
                "project_id": project_id,
                "payload": handoff.model_dump(mode="json"),
                "cdc_id": cdc_id,
                "cdc_revision": cdc_revision,
                "cdc_hash": cdc_hash,
                "expected_previous_id": expected_previous_id,
                "expected_previous_revision": expected_previous_revision,
                "expected_previous_hash": expected_previous_hash,
            },
            mutate,
        )

    def pipeline_approve_architecture(
        self,
        *,
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
        self._require_curator()

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage != PipelineStage.ARCHITECTURE_DRAFT:
                raise ValidationError("architecture approval requires ARCHITECTURE_DRAFT")
            cdc = self._require_current_pointer(state, "cdc", cdc_id, cdc_revision, cdc_hash)
            architecture = self._require_current_pointer(
                state,
                "architecture",
                architecture_id,
                architecture_revision,
                architecture_hash,
            )
            cdc_document, _ = self.store.get_document(cdc.document_id)
            architecture_document, _ = self.store.get_document(architecture.document_id)
            cdc_payload = parse_payload(cdc_document.body, "cdc-handoff-v1")
            architecture_payload = parse_payload(
                architecture_document.body, "architecture-handoff-v1"
            )
            if not isinstance(cdc_payload, CdcHandoff) or not isinstance(
                architecture_payload, ArchitectureHandoff
            ):
                raise ValidationError("invalid approved handoff payload")
            evidence_bindings = [self._document_pointer(item) for item in included_evidence_ids]
            packet_payload = ReviewPacket(
                cdc=cdc_payload,
                architecture=architecture_payload,
                evidence_ids=included_evidence_ids,
                factual_constraints=cdc_payload.constraints,
                unknowns=[*cdc_payload.unknowns, *architecture_payload.unknowns],
            )
            previous = self._latest_pipeline_pointer(project_id, "review_packet")
            folder = self._project_folder(project_id)
            packet = self._new_pipeline_artifact(
                project_id=project_id,
                namespace=f"{folder}/neutral",
                artifact_type="review_packet",
                entity_type=EntityType.REVIEW,
                payload=packet_payload,
                previous=previous,
            )
            packet = self._write_document(
                tx, self.store.document_path(packet.namespace, packet.id), packet
            )
            packet_pointer = self._pipeline_pointer(packet)
            reviewer_grant = ProjectGrant(
                principal=Principal.RED_TEAM,
                project_id=project_id,
                project_access=True,
                artifact_bindings=[packet_pointer, *evidence_bindings],
            )
            pointers = dict(state.pointers)
            pointers.pop("verdict", None)
            pointers.pop("development_handoff", None)
            pointers["review_packet"] = packet_pointer
            updated = state.model_copy(
                update={
                    "stage": PipelineStage.REVIEW,
                    "pointers": pointers,
                    "grants": self._replace_grant(state.grants, reviewer_grant),
                }
            )
            self._append_pipeline_state(tx, folder, updated, state_document)
            return packet, updated

        return self._pipeline_transaction(
            "pipeline_approve_architecture",
            idempotency_key,
            {
                "project_id": project_id,
                "cdc_id": cdc_id,
                "cdc_revision": cdc_revision,
                "cdc_hash": cdc_hash,
                "architecture_id": architecture_id,
                "architecture_revision": architecture_revision,
                "architecture_hash": architecture_hash,
                "included_evidence_ids": included_evidence_ids,
            },
            mutate,
        )

    def pipeline_record_verdict(
        self,
        *,
        project_id: str,
        packet_id: str,
        packet_revision: int,
        packet_hash: str,
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.RED_TEAM:
            raise AccessDeniedError("resource not found")
        verdict_payload = ReviewVerdictHandoff.model_validate(payload)

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage != PipelineStage.REVIEW:
                raise ValidationError("verdict requires REVIEW")
            packet = self._require_current_pointer(
                state, "review_packet", packet_id, packet_revision, packet_hash
            )
            grant = state.active_grant(self.principal)
            if grant is None or not grant.permits(packet):
                raise AccessDeniedError("resource not found")
            previous = self._latest_pipeline_pointer(project_id, "review_verdict")
            folder = self._project_folder(project_id)
            document = self._new_pipeline_artifact(
                project_id=project_id,
                namespace=f"{folder}/reviews",
                artifact_type="review_verdict",
                entity_type=EntityType.REVIEW,
                payload=verdict_payload,
                previous=previous,
            )
            document = self._write_document(
                tx, self.store.document_path(document.namespace, document.id), document
            )
            verdict_pointer = self._pipeline_pointer(document)
            pointers = dict(state.pointers)
            pointers["verdict"] = verdict_pointer
            rework = verdict_payload.verdict in {
                ReviewVerdict.REWORK_CDC,
                ReviewVerdict.REWORK_ARCHITECTURE,
            }
            rework_count = state.consecutive_reworks + 1 if rework else 0
            human_gate = rework_count >= 2
            if verdict_payload.verdict == ReviewVerdict.REWORK_CDC:
                pointers = {
                    key: value for key, value in pointers.items() if key in {"cdc", "verdict"}
                }
            elif verdict_payload.verdict == ReviewVerdict.REWORK_ARCHITECTURE:
                pointers = {
                    key: value
                    for key, value in pointers.items()
                    if key in {"cdc", "architecture", "verdict"}
                }
            target_stage = PipelineStage(verdict_payload.verdict.value)
            grants = [grant for grant in state.grants if grant.principal != Principal.RED_TEAM]
            if target_stage == PipelineStage.REWORK_CDC:
                product = next(
                    grant for grant in grants if grant.principal == Principal.FORGE_PRODUCT
                )
                grants = self._replace_grant(
                    grants,
                    product.model_copy(
                        update={
                            "artifact_bindings": [pointers["cdc"], verdict_pointer]
                        }
                    ),
                )
            elif target_stage == PipelineStage.REWORK_ARCHITECTURE:
                architect = next(
                    grant
                    for grant in grants
                    if grant.principal == Principal.ARCHITECT_BRAINSTORM
                )
                grants = self._replace_grant(
                    grants,
                    architect.model_copy(
                        update={
                            "artifact_bindings": [
                                pointers["cdc"],
                                pointers["architecture"],
                                verdict_pointer,
                            ]
                        }
                    ),
                )
            updated = state.model_copy(
                update={
                    "stage": target_stage,
                    "pointers": pointers,
                    "grants": grants,
                    "consecutive_reworks": rework_count,
                    "human_gate_required": human_gate,
                    "human_decision": None if human_gate else state.human_decision,
                }
            )
            self._append_pipeline_state(tx, folder, updated, state_document)
            return document, updated

        return self._pipeline_transaction(
            "pipeline_record_verdict",
            idempotency_key,
            {
                "project_id": project_id,
                "packet_id": packet_id,
                "packet_revision": packet_revision,
                "packet_hash": packet_hash,
                "payload": verdict_payload.model_dump(mode="json"),
            },
            mutate,
        )

    def pipeline_record_human_rework_decision(
        self,
        *,
        project_id: str,
        scope: str,
        decision_id: str,
        confirmed: bool,
        idempotency_key: str,
    ) -> dict[str, Any]:
        self._require_curator()
        decision = HumanDecision(
            decision_id=decision_id,
            scope=scope,
            confirmed=confirmed,
            recorded_at=self.clock.now(),
        )

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if not state.human_gate_required:
                raise ValidationError("no human rework decision is required")
            expected_scope = (
                "CDC" if state.stage == PipelineStage.REWORK_CDC else "ARCHITECTURE"
            )
            if decision.scope != expected_scope or not decision.confirmed:
                raise ValidationError("human decision does not authorize current rework")
            updated = state.model_copy(
                update={"human_gate_required": False, "human_decision": decision}
            )
            appended_state = self._append_pipeline_state(
                tx, self._project_folder(project_id), updated, state_document
            )
            return appended_state, updated

        return self._pipeline_transaction(
            "pipeline_record_human_rework_decision",
            idempotency_key,
            {
                "project_id": project_id,
                "scope": scope,
                "decision_id": decision_id,
                "confirmed": confirmed,
            },
            mutate,
        )

    def pipeline_create_development_handoff(
        self,
        *,
        project_id: str,
        verdict_id: str,
        verdict_revision: int,
        verdict_hash: str,
        adrs: list[str],
        slices: list[dict[str, Any]],
        risks: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        self._require_curator()

        def mutate(tx):
            state, state_document = self._require_pipeline_state(project_id)
            if state.stage not in {
                PipelineStage.GO_DEV,
                PipelineStage.GO_DEV_WITH_CONDITIONS,
            }:
                raise ValidationError("development handoff requires a compatible verdict")
            verdict = self._require_current_pointer(
                state, "verdict", verdict_id, verdict_revision, verdict_hash
            )
            cdc = state.pointers["cdc"]
            architecture = state.pointers["architecture"]
            verdict_document, _ = self.store.get_document(verdict.document_id)
            verdict_payload = parse_payload(verdict_document.body, "review-verdict-v1")
            if not isinstance(verdict_payload, ReviewVerdictHandoff):
                raise ValidationError("invalid verdict payload")
            handoff = DevelopmentHandoff(
                project_id=project_id,
                cdc=cdc,
                architecture=architecture,
                verdict=verdict,
                adrs=adrs,
                slices=slices,
                risks=risks,
                reviewer_conditions=verdict_payload.conditions,
            )
            folder = self._project_folder(project_id)
            document = self._new_pipeline_artifact(
                project_id=project_id,
                namespace=f"{folder}/decisions",
                artifact_type="development_handoff",
                entity_type=EntityType.DECISION,
                payload=handoff,
                previous=None,
            )
            document = self._write_document(
                tx, self.store.document_path(document.namespace, document.id), document
            )
            pointers = {**state.pointers, "development_handoff": self._pipeline_pointer(document)}
            updated = state.model_copy(
                update={"stage": PipelineStage.DEVELOPMENT_READY, "pointers": pointers}
            )
            self._append_pipeline_state(tx, folder, updated, state_document)
            return document, updated

        return self._pipeline_transaction(
            "pipeline_create_development_handoff",
            idempotency_key,
            {
                "project_id": project_id,
                "verdict_id": verdict_id,
                "verdict_revision": verdict_revision,
                "verdict_hash": verdict_hash,
                "adrs": adrs,
                "slices": slices,
                "risks": risks,
            },
            mutate,
        )

    def project_get(self, project_id: str) -> dict[str, Any]:
        allowed = (
            self.authorization.can_read_project(self.principal, project_id)
            if self.authorization
            else self.policy.project_allowed(project_id)
        )
        if not allowed:
            raise NotFoundError("resource not found")
        return self.store.get_project(project_id).model_dump(mode="json")

    def project_write_opportunity_brief(
        self,
        *,
        project_id: str,
        title: str,
        content: str,
        provenance: list[dict[str, str]],
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.FORGE_PRODUCT or not self.authorization.can_write_project_zone(
            self.principal, "neutral", project_id
        ):
            raise AccessDeniedError("resource not found")
        namespace = f"{self._project_folder(project_id)}/neutral"
        document = self._new_document(
            entity_type=EntityType.CONTEXT,
            memory_type=MemoryType.SEMANTIC,
            project_id=project_id,
            owner="shared",
            namespace=namespace,
            visibility="shared",
            title=title,
            body=content,
            provenance=provenance,
            confidence=confidence,
            attributes={"artifact_type": "opportunity-brief"},
        )
        path = self.store.document_path(namespace, document.id)
        return self.transactions.execute(
            action="project_write_opportunity_brief",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={"project_id": project_id, "title": title, "content": content},
            mutate=lambda tx: self._write_document(tx, path, document),
            result_payload=self._document_result,
        )

    def episode_record(
        self,
        *,
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
        if self.principal == Principal.CURATOR or not self._project_allowed(project_id):
            raise AccessDeniedError("resource not found")
        namespace = f"{self.policy.private_namespace()}/episodes"
        document = self._new_document(
            entity_type=EntityType.EPISODE,
            memory_type=MemoryType.EPISODIC,
            project_id=project_id,
            owner=self.principal.value,
            namespace=namespace,
            visibility="private",
            title=title,
            body=f"Prediction: {prediction}",
            provenance=[{"type": "agent", "reference": self.principal.value}],
            confidence=confidence_after,
            attributes={
                "prediction": prediction,
                "actual_outcome": actual_outcome,
                "error_types": error_types,
                "procedures_used": procedures_used,
                "candidate_lessons": candidate_lessons,
                "confidence_before": confidence_before,
                "confidence_after": confidence_after,
            },
        )
        path = self.store.document_path(namespace, document.id)
        return self.transactions.execute(
            action="episode_record",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload=document.model_dump(mode="json", exclude={"id", "content_hash"}),
            mutate=lambda tx: self._write_document(tx, path, document),
            result_payload=self._document_result,
        )

    def project_publish_review_packet(
        self,
        *,
        project_id: str,
        source_brief_id: str,
        included_evidence_ids: list[str],
        included_hypothesis_ids: list[str],
        expected_hash: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.FORGE_PRODUCT:
            raise AccessDeniedError("resource not found")

        def mutate(tx):
            brief, brief_path = self.store.get_document(source_brief_id)
            if brief.project_id != project_id or "/neutral/" not in f"/{brief_path}":
                raise NotFoundError("resource not found")
            self._require_hash(brief, expected_hash)
            evidence = self._load_project_documents(
                included_evidence_ids, project_id, EntityType.EVIDENCE
            )
            hypotheses = self._load_project_documents(
                included_hypothesis_ids, project_id, EntityType.HYPOTHESIS
            )
            neutral_body = self._neutralize(brief.body)
            packet_body = (
                f"# Brief neutralisé\n\n{neutral_body}\n\n"
                "# Preuves\n\n"
                + "\n".join(f"- {item.title} ({item.id})" for item in evidence)
                + "\n\n# Hypothèses\n\n"
                + "\n".join(f"- {item.title} ({item.id})" for item in hypotheses)
            )
            namespace = f"{self._project_folder(project_id)}/neutral"
            packet = self._new_document(
                entity_type=EntityType.REVIEW,
                memory_type=MemoryType.SEMANTIC,
                project_id=project_id,
                owner="shared",
                namespace=namespace,
                visibility="shared",
                title=f"Review packet — {brief.title}",
                body=packet_body,
                provenance=[{"type": "document", "reference": source_brief_id}],
                confidence=brief.confidence,
                attributes={
                    "artifact_type": "review-packet",
                    "version": 1,
                    "source_brief_id": source_brief_id,
                    "included_evidence_ids": included_evidence_ids,
                    "included_hypothesis_ids": included_hypothesis_ids,
                    "producer": self.principal.value,
                    "excluded": sorted(_FORBIDDEN_REVIEW_HEADERS),
                },
            )
            path = self.store.document_path(namespace, packet.id)
            return self._write_document(tx, path, packet)

        return self.transactions.execute(
            action="project_publish_review_packet",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "project_id": project_id,
                "source_brief_id": source_brief_id,
                "included_evidence_ids": included_evidence_ids,
                "included_hypothesis_ids": included_hypothesis_ids,
                "expected_hash": expected_hash,
            },
            mutate=mutate,
            result_payload=self._document_result,
        )

    def review_record(
        self,
        *,
        project_id: str,
        packet_id: str,
        verdict: str,
        content: str,
        confidence: float,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if self.principal != Principal.RED_TEAM or not self.authorization.can_write_project_zone(
            self.principal, "reviews", project_id
        ):
            raise AccessDeniedError("resource not found")
        packet, _ = self._get_authorized_document(packet_id)
        if (
            packet.project_id != project_id
            or packet.attributes.get("artifact_type") != "review-packet"
        ):
            raise NotFoundError("resource not found")
        namespace = f"{self._project_folder(project_id)}/reviews"
        document = self._new_document(
            entity_type=EntityType.REVIEW,
            memory_type=MemoryType.EPISODIC,
            project_id=project_id,
            owner=self.principal.value,
            namespace=namespace,
            visibility="shared",
            title=f"Red Team review — {verdict}",
            body=content,
            provenance=[{"type": "review-packet", "reference": packet_id}],
            confidence=confidence,
            attributes={"verdict": verdict, "packet_id": packet_id},
        )
        path = self.store.document_path(namespace, document.id)
        return self.transactions.execute(
            action="review_record",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload={
                "project_id": project_id,
                "packet_id": packet_id,
                "verdict": verdict,
                "content": content,
            },
            mutate=lambda tx: self._write_document(tx, path, document),
            result_payload=self._document_result,
        )

    def project_record_outcome(
        self,
        *,
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
        self._require_curator()
        namespace = f"{self._project_folder(project_id)}/outcomes"
        document = self._new_document(
            entity_type=EntityType.OUTCOME,
            memory_type=MemoryType.EPISODIC,
            project_id=project_id,
            owner="shared",
            namespace=namespace,
            visibility="shared",
            title=f"Outcome — {metric}",
            body=evidence,
            provenance=[{"type": "source", "reference": source}],
            confidence=1.0,
            observed_at=observed_at,
            status=Status.VALIDATED,
            validation_status=ValidationStatus.APPROVED,
            attributes={
                "experiment_id": experiment_id,
                "outcome_type": outcome_type,
                "metric": metric,
                "value": value,
                "unit": unit,
            },
        )
        path = self.store.document_path(namespace, document.id)
        return self.transactions.execute(
            action="project_record_outcome",
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload=document.model_dump(mode="json", exclude={"id", "content_hash"}),
            mutate=lambda tx: self._write_document(tx, path, document),
            result_payload=self._document_result,
        )

    def procedure_search(
        self, query: str, project_id: str | None = None, limit: int = 10
    ) -> dict[str, Any]:
        return self.context_search(
            query=query,
            project_id=project_id,
            entity_types=[EntityType.PROCEDURE.value],
            statuses=[Status.VALIDATED.value, Status.RESTRICTED.value],
            limit=limit,
        )

    def system_health(self) -> dict[str, Any]:
        return StoreVerifier(self.store, self.indexes).verify()

    def rebuild_indexes(self) -> dict[str, Any]:
        self._require_curator()
        self.indexes.rebuild_all()
        return {"indexes": self.indexes.health()}

    def _create_project_value(
        self,
        name: str,
        slug: str,
        objective: str,
        owner: str,
        initial_constraints: list[str],
    ) -> Project:
        year = self.clock.now().year
        existing = list((self.store.root / "projects").glob(f"PRJ-{year}-*"))
        numbers = []
        for path in existing:
            try:
                numbers.append(int(path.name.split("-", 3)[2]))
            except (IndexError, ValueError):
                continue
        return Project(
            id=f"PRJ-{year}-{max(numbers, default=0) + 1:03d}",
            name=name,
            slug=slug,
            owner=owner,
            objective=objective,
            created_at=self.clock.now(),
            initial_constraints=initial_constraints,
        ).with_hash()

    @staticmethod
    def _create_project_folders(tx, folder: str) -> None:
        for zone in (
            "neutral",
            "evidence",
            "hypotheses",
            "decisions",
            "experiments",
            "reviews",
            "outcomes",
            "retrospective",
        ):
            tx.mkdir(f"{folder}/{zone}")

    def _require_pipeline_state(
        self, project_id: str
    ) -> tuple[PipelineState, CognitionDocument]:
        resolved = self.store.latest_pipeline_state(project_id)
        if resolved is None:
            raise NotFoundError("resource not found")
        return resolved

    @staticmethod
    def _require_human_gate_clear(state: PipelineState) -> None:
        if state.human_gate_required:
            raise ValidationError("curator-recorded human decision is required")

    @staticmethod
    def _replace_grant(
        grants: list[ProjectGrant], replacement: ProjectGrant
    ) -> list[ProjectGrant]:
        return [
            grant for grant in grants if grant.principal != replacement.principal
        ] + [replacement]

    @staticmethod
    def _require_previous_binding(
        previous: ArtifactPointer | None,
        document_id: str | None,
        revision: int | None,
        content_hash: str | None,
    ) -> None:
        supplied = (document_id, revision, content_hash)
        if previous is None:
            if any(item is not None for item in supplied):
                raise ConflictError("no previous artifact exists")
            return
        if (
            document_id != previous.document_id
            or revision != previous.revision
            or content_hash != previous.content_hash
        ):
            raise ConflictError("stale previous artifact", current_hash=previous.content_hash)

    @staticmethod
    def _require_current_pointer(
        state: PipelineState,
        key: str,
        document_id: str,
        revision: int,
        content_hash: str,
    ) -> ArtifactPointer:
        pointer = state.pointers.get(key)
        if pointer is None:
            raise ValidationError(f"missing current {key}")
        if (
            pointer.document_id != document_id
            or pointer.revision != revision
            or pointer.content_hash != content_hash
        ):
            raise ConflictError(f"stale {key}", current_hash=pointer.content_hash)
        return pointer

    def _document_pointer(self, document_id: str) -> ArtifactPointer:
        document, _ = self.store.get_document(document_id)
        return ArtifactPointer(
            document_id=document.id,
            revision=document.revision,
            content_hash=document.content_hash,
            series_id=str(document.attributes.get("series_id") or f"document:{document.id}"),
        )

    @staticmethod
    def _pipeline_pointer(document: CognitionDocument) -> ArtifactPointer:
        return ArtifactPointer(
            document_id=document.id,
            revision=document.revision,
            content_hash=document.content_hash,
            series_id=str(document.attributes["series_id"]),
        )

    def _latest_pipeline_pointer(
        self, project_id: str, artifact_type: str
    ) -> ArtifactPointer | None:
        series_id = f"{project_id}:{artifact_type.replace('_', '-')}"
        series = self.store.resolve_pipeline_series(project_id, series_id)
        return self._pipeline_pointer(series[-1][0]) if series else None

    def _new_pipeline_artifact(
        self,
        *,
        project_id: str,
        namespace: str,
        artifact_type: str,
        entity_type: EntityType,
        payload,
        previous: ArtifactPointer | None,
    ) -> CognitionDocument:
        series_id = f"{project_id}:{artifact_type.replace('_', '-')}"
        document = self._new_document(
            entity_type=entity_type,
            memory_type=self._memory_type(entity_type),
            project_id=project_id,
            owner=self.principal.value,
            namespace=namespace,
            visibility="restricted",
            title=artifact_type.replace("_", " ").title(),
            body=canonical_payload(payload),
            provenance=[{"type": "pipeline", "reference": project_id}],
            confidence=1.0,
            attributes={
                "pipeline_managed": True,
                "artifact_type": artifact_type,
                "series_id": series_id,
                "payload_schema": payload.payload_schema,
                "minimum_runtime_version": 1,
            },
        )
        return document.model_copy(
            update={
                "revision": previous.revision + 1 if previous else 1,
                "supersedes": previous.document_id if previous else None,
                "content_hash": "",
            }
        ).with_hash()

    def _append_pipeline_state(
        self,
        tx,
        folder: str,
        state: PipelineState,
        previous: CognitionDocument | None,
    ) -> CognitionDocument:
        document = self._new_document(
            entity_type=EntityType.DECISION,
            memory_type=MemoryType.SEMANTIC,
            project_id=state.project_id,
            owner=Principal.CURATOR.value,
            namespace=f"{folder}/decisions",
            visibility="restricted",
            title="Pipeline state",
            body=canonical_payload(state),
            provenance=[{"type": "pipeline", "reference": state.project_id}],
            confidence=1.0,
            attributes={
                "pipeline_managed": True,
                "artifact_type": "pipeline_state",
                "series_id": f"{state.project_id}:pipeline-state",
                "payload_schema": "pipeline-state-v1",
                "minimum_runtime_version": 1,
            },
        )
        document = document.model_copy(
            update={
                "revision": previous.revision + 1 if previous else 1,
                "supersedes": previous.id if previous else None,
                "content_hash": "",
            }
        ).with_hash()
        path = self.store.document_path(document.namespace, document.id)
        return self._write_document(tx, path, document)

    def _pipeline_transaction(
        self,
        action: str,
        idempotency_key: str,
        request_payload: dict[str, Any],
        mutate,
    ) -> dict[str, Any]:
        return self.transactions.execute(
            action=action,
            principal=self.principal,
            idempotency_key=idempotency_key,
            request_payload=request_payload,
            mutate=mutate,
            result_payload=lambda value: {
                **self._document_result(value[0]),
                "stage": value[1].stage.value,
                "human_gate_required": value[1].human_gate_required,
            },
        )

    def _new_document(
        self,
        *,
        entity_type: EntityType,
        memory_type: MemoryType,
        project_id: str | None,
        owner: str,
        namespace: str,
        visibility: str,
        title: str,
        body: str,
        provenance: list[dict[str, str]],
        confidence: float,
        attributes: dict[str, Any] | None = None,
        observed_at: datetime | None = None,
        status: Status = Status.CANDIDATE,
        validation_status: ValidationStatus = ValidationStatus.PENDING,
    ) -> CognitionDocument:
        now = self.clock.now()
        return CognitionDocument(
            id=self.ids.new(),
            entity_type=entity_type,
            memory_type=memory_type,
            project_id=project_id,
            owner=owner,
            namespace=namespace,
            visibility=visibility,
            status=status,
            validation_status=validation_status,
            created_at=now,
            updated_at=now,
            observed_at=observed_at,
            valid_from=now.date(),
            confidence=confidence,
            confidence_basis="explicit-provenance",
            provenance=[Provenance.model_validate(item) for item in provenance],
            title=title,
            summary=body.splitlines()[0][:240],
            attributes=attributes or {},
            body=body,
        ).with_hash()

    def _write_document(self, tx, path: str, document: CognitionDocument) -> CognitionDocument:
        hashed = self.store.canonical_document(document)
        tx.write_text(path, self.store.serialize_document(hashed))
        return hashed

    @staticmethod
    def _document_result(document: CognitionDocument) -> dict[str, Any]:
        return {
            "id": document.id,
            "entity_type": str(document.entity_type),
            "status": str(document.status),
            "revision": document.revision,
            "content_hash": document.content_hash,
        }

    def _get_authorized_document(self, document_id: str) -> tuple[CognitionDocument, str]:
        document, path = self.store.get_document(document_id)
        allowed = (
            self.authorization.can_read(self.principal, document, path)
            if self.authorization
            else self.policy.can_read(path, document.project_id)
        )
        if not allowed:
            raise NotFoundError("resource not found")
        return document, path

    def _project_allowed(self, project_id: str) -> bool:
        return (
            self.authorization.can_read_project(self.principal, project_id)
            if self.authorization
            else self.policy.project_allowed(project_id)
        )

    def _project_folder(self, project_id: str) -> str:
        return self.store.project_path(project_id).rsplit("/", 1)[0]

    def _load_project_documents(
        self, ids: list[str], project_id: str, expected_type: EntityType
    ) -> list[CognitionDocument]:
        documents = []
        for document_id in ids:
            document, _ = self._get_authorized_document(document_id)
            if document.project_id != project_id or document.entity_type != expected_type:
                raise NotFoundError("resource not found")
            documents.append(document)
        return documents

    def _require_procedure_evidence(self, candidate: CognitionDocument) -> None:
        attributes = candidate.attributes
        if attributes.get("security_exception"):
            required = {"expires_at", "review_required", "evidence_level", "incident_id"}
            if not required <= attributes.keys():
                raise ValidationError("restricted safety procedure metadata incomplete")
            return
        if "counterexamples" not in attributes:
            raise ValidationError("procedure promotion requires a counterexample search result")
        episodes = [
            self.store.get_document(item)[0] for item in attributes.get("source_episode_ids", [])
        ]
        outcomes = [
            self.store.get_document(item)[0] for item in attributes.get("source_outcome_ids", [])
        ]
        if not procedure_promotion_eligible(
            episodes,
            outcomes,
            contradictions_searched=bool(attributes.get("contradictions_searched")),
        ):
            raise ValidationError("procedure promotion evidence threshold not met")

    @staticmethod
    def _require_hash(document: CognitionDocument, expected_hash: str) -> None:
        if document.content_hash != expected_hash:
            raise ConflictError("content changed", current_hash=document.content_hash)

    def _require_curator(self) -> None:
        if self.principal != Principal.CURATOR:
            raise AccessDeniedError("resource not found")

    def _commit_target(self, candidate: CognitionDocument) -> str:
        if candidate.entity_type == EntityType.PROCEDURE:
            return "shared/procedures"
        if candidate.entity_type == EntityType.CALIBRATION:
            return "shared/calibration"
        project_zones = {
            EntityType.EVIDENCE: "evidence",
            EntityType.HYPOTHESIS: "hypotheses",
            EntityType.DECISION: "decisions",
            EntityType.EXPERIMENT: "experiments",
            EntityType.RETROSPECTIVE: "retrospective",
        }
        if candidate.project_id and candidate.entity_type in project_zones:
            return f"{self._project_folder(candidate.project_id)}/{project_zones[candidate.entity_type]}"
        return "shared/context"

    @staticmethod
    def _memory_type(entity_type: EntityType) -> MemoryType:
        if entity_type in {
            EntityType.EPISODE,
            EntityType.EXPERIMENT,
            EntityType.OUTCOME,
            EntityType.REVIEW,
            EntityType.RETROSPECTIVE,
        }:
            return MemoryType.EPISODIC
        if entity_type in {EntityType.LESSON, EntityType.PROCEDURE}:
            return MemoryType.PROCEDURAL
        if entity_type == EntityType.CALIBRATION:
            return MemoryType.CALIBRATION
        return MemoryType.SEMANTIC

    @staticmethod
    def _neutralize(content: str) -> str:
        lines = content.splitlines()
        output = []
        skipping = False
        skip_level = 0
        for line in lines:
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                heading = line.lstrip("#").strip().casefold()
                if heading in _FORBIDDEN_REVIEW_HEADERS:
                    skipping = True
                    skip_level = level
                    continue
                if skipping and level <= skip_level:
                    skipping = False
            if not skipping:
                output.append(line)
        return "\n".join(output).strip()

    @staticmethod
    def _validate_iso_date(value: date) -> None:
        if not isinstance(value, date):
            raise ValidationError("valid_at must be an ISO date")

    @staticmethod
    def _document_valid_at(document: CognitionDocument, valid_at: date) -> bool:
        return (document.valid_from is None or document.valid_from <= valid_at) and (
            document.valid_until is None or valid_at <= document.valid_until
        )
