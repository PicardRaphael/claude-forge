"""Profile-scoped access policies with deny-by-default semantics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from .models import Principal


@dataclass(frozen=True)
class AccessPolicy:
    principal: Principal
    allowed_projects: frozenset[str]

    def project_allowed(self, project_id: str | None) -> bool:
        return bool(project_id) and (
            "*" in self.allowed_projects or project_id in self.allowed_projects
        )

    def can_read(self, relative_path: str, project_id: str | None = None) -> bool:
        parts = PurePosixPath(relative_path).parts
        if not parts:
            return False
        if self.principal == Principal.CURATOR:
            return True
        if parts[0] == "shared":
            return len(parts) >= 2 and parts[1] in {"context", "procedures", "calibration"}
        if parts[0] == "private":
            return len(parts) >= 2 and parts[1] == self.principal.value
        if parts[0] == "projects" and self.project_allowed(project_id):
            if len(parts) < 3:
                return False
            zone = parts[2]
            if self.principal == Principal.FORGE_PRODUCT:
                return zone != "brainstorming"
            return zone in {"neutral", "evidence", "hypotheses", "outcomes", "reviews"}
        return False

    def proposal_namespace(self) -> str:
        if self.principal == Principal.CURATOR:
            raise ValueError("curator has no proposal inbox")
        return f"inbox/{self.principal.value}"

    def private_namespace(self) -> str:
        if self.principal == Principal.CURATOR:
            raise ValueError("curator has no private namespace")
        return f"private/{self.principal.value}"

    def can_write_project_zone(self, zone: str, project_id: str) -> bool:
        if not self.project_allowed(project_id):
            return False
        if self.principal == Principal.CURATOR:
            return True
        if self.principal == Principal.FORGE_PRODUCT:
            return zone == "neutral"
        return zone == "reviews"
