"""One authorization path for canonical reads and derived indexes."""

from __future__ import annotations

from pathlib import PurePosixPath

from forge_cognition.domain.errors import NotFoundError
from forge_cognition.domain.models import CognitionDocument, Principal
from forge_cognition.domain.pipeline import ArtifactPointer, PipelineState
from forge_cognition.domain.policies import AccessPolicy
from forge_cognition.infrastructure.file_store import FileCanonicalStore


class PipelineAuthorization:
    def __init__(
        self,
        store: FileCanonicalStore,
        policies: dict[Principal, AccessPolicy],
    ) -> None:
        self.store = store
        self.policies = policies
        self._state_cache: dict[str, PipelineState | None] = {}

    def reset_snapshot(self) -> None:
        self._state_cache.clear()

    def state_for(self, project_id: str) -> PipelineState | None:
        if project_id not in self._state_cache:
            resolved = self.store.latest_pipeline_state(project_id)
            self._state_cache[project_id] = resolved[0] if resolved else None
        return self._state_cache[project_id]

    def can_read(
        self, principal: Principal, document: CognitionDocument, relative_path: str
    ) -> bool:
        policy = self.policies[principal]
        parts = PurePosixPath(relative_path).parts
        if principal == Principal.CURATOR:
            return True
        if parts and parts[0] == "private":
            return policy.can_read(relative_path, document.project_id)
        if not document.project_id:
            return policy.can_read(relative_path, document.project_id)
        state = self.state_for(document.project_id)
        if document.attributes.get("pipeline_managed") is not True:
            if policy.can_read(relative_path, document.project_id):
                return True
            if state is None and self._legacy_project_exists(document.project_id):
                legacy_policy = AccessPolicy(principal, frozenset({document.project_id}))
                return legacy_policy.can_read(relative_path, document.project_id)
            grant = state.active_grant(principal) if state else None
            pointer = ArtifactPointer(
                document_id=document.id,
                revision=document.revision,
                content_hash=document.content_hash,
                series_id=f"document:{document.id}",
            )
            return bool(grant and grant.permits(pointer))
        grant = state.active_grant(principal) if state else None
        if grant is None:
            return False
        pointer = ArtifactPointer(
            document_id=document.id,
            revision=document.revision,
            content_hash=document.content_hash,
            series_id=str(document.attributes.get("series_id", "")),
        )
        return grant.permits(pointer)

    def can_read_project(self, principal: Principal, project_id: str) -> bool:
        if principal == Principal.CURATOR:
            return True
        state = self.state_for(project_id)
        if state is None:
            return self.policies[principal].project_allowed(
                project_id
            ) or self._legacy_project_exists(project_id)
        grant = state.active_grant(principal)
        return bool(grant and grant.project_access)

    def can_write_project_zone(
        self, principal: Principal, zone: str, project_id: str
    ) -> bool:
        policy = self.policies[principal]
        if policy.can_write_project_zone(zone, project_id):
            return True
        if self.state_for(project_id) is not None or not self._legacy_project_exists(project_id):
            return False
        return AccessPolicy(principal, frozenset({project_id})).can_write_project_zone(
            zone, project_id
        )

    def _legacy_project_exists(self, project_id: str) -> bool:
        try:
            self.store.get_project(project_id)
        except NotFoundError:
            return False
        return True
