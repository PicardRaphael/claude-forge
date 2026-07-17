"""Deterministic store, reference, index and ACL verification."""

from __future__ import annotations

import sqlite3
from collections import Counter
from pathlib import PurePosixPath
from typing import Any

import yaml

from forge_cognition.domain.models import CognitionDocument, Principal, Project

from .file_store import FileCanonicalStore
from .lexical_index import SQLiteLexicalIndex


class StoreVerifier:
    def __init__(self, store: FileCanonicalStore, indexes: SQLiteLexicalIndex) -> None:
        self.store = store
        self.indexes = indexes

    def verify(self) -> dict[str, Any]:
        errors: set[str] = set()
        counts: Counter[str] = Counter()
        documents: dict[str, tuple[CognitionDocument, str]] = {}
        projects = self._projects(errors)

        for path in sorted(self.store.root.rglob("*.md")):
            relative = path.relative_to(self.store.root).as_posix()
            if path.name == "README.md" or relative.startswith("templates/"):
                continue
            try:
                document = self.store.parse_document(path)
            except Exception:
                errors.add("invalid_document_or_hash")
                continue
            if document.id in documents:
                errors.add("duplicate_document_id")
            documents[document.id] = (document, relative)
            counts[str(document.status)] += 1
            if not self._recognized_document_path(relative):
                errors.add("document_in_unrecognized_zone")
            if document.project_id:
                if document.project_id not in projects:
                    errors.add("orphan_project_reference")
                elif PurePosixPath(relative).parts[0] == "projects" and not PurePosixPath(
                    relative
                ).parts[1].startswith(document.project_id):
                    errors.add("project_path_mismatch")

        self._references(documents, errors)
        self._files(errors)
        self._indexes(documents, errors)
        version_path = self.store.root / "STORE_VERSION"
        store_version = (
            version_path.read_text(encoding="utf-8").strip() if version_path.exists() else "missing"
        )
        if store_version != "1":
            errors.add("unsupported_store_version")
        for schema in ("document-v1.yaml", "project-v1.yaml"):
            if not (self.store.root / "schemas" / schema).exists():
                errors.add("missing_schema")
        return {
            "store_version": store_version,
            "indexes": self.indexes.health(),
            "counts_by_status": dict(counts),
            "consistency_errors": sorted(errors),
            "pending_migrations": [],
        }

    def _projects(self, errors: set[str]) -> dict[str, Project]:
        projects: dict[str, Project] = {}
        for path in sorted((self.store.root / "projects").glob("*/project.yaml")):
            try:
                project = Project.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
                if project.content_hash != project.computed_hash():
                    raise ValueError("hash")
            except Exception:
                errors.add("invalid_project_or_hash")
                continue
            if project.id in projects:
                errors.add("duplicate_project_id")
            projects[project.id] = project
        return projects

    @staticmethod
    def _recognized_document_path(relative: str) -> bool:
        parts = PurePosixPath(relative).parts
        if not parts:
            return False
        if parts[0] == "inbox":
            return len(parts) == 3 and parts[1] in {"forge-product", "red-team"}
        if parts[0] == "shared":
            return len(parts) == 3 and parts[1] in {"context", "procedures", "calibration"}
        if parts[0] == "private":
            return (
                len(parts) == 4
                and parts[1] in {"forge-product", "red-team"}
                and parts[2] in {"episodes", "lessons", "calibration"}
            )
        if parts[0] == "projects":
            return len(parts) == 4 and parts[2] in {
                "neutral",
                "evidence",
                "hypotheses",
                "decisions",
                "experiments",
                "reviews",
                "outcomes",
                "retrospective",
            }
        return parts[0] == "archive" and len(parts) == 2

    @staticmethod
    def _references(documents: dict[str, tuple[CognitionDocument, str]], errors: set[str]) -> None:
        reference_keys = {
            "source_brief_id",
            "included_evidence_ids",
            "included_hypothesis_ids",
            "source_episode_ids",
            "source_outcome_ids",
            "episode_ids",
            "outcome_ids",
            "packet_id",
        }
        for document, _ in documents.values():
            references: list[str] = list(document.outcome_ids)
            references.extend(
                item for item in (document.supersedes, document.superseded_by) if item
            )
            for key in reference_keys:
                value = document.attributes.get(key)
                if isinstance(value, str):
                    references.append(value)
                elif isinstance(value, list):
                    references.extend(item for item in value if isinstance(item, str))
            if any(reference not in documents for reference in references):
                errors.add("broken_document_reference")
            if document.superseded_by and document.superseded_by in documents:
                replacement = documents[document.superseded_by][0]
                if replacement.supersedes != document.id:
                    errors.add("non_reciprocal_supersession")

    def _files(self, errors: set[str]) -> None:
        allowed_names = {"README.md", "STORE_VERSION", ".gitkeep", "project.yaml"}
        for path in self.store.root.rglob("*"):
            if path.is_dir() or path.name in allowed_names:
                continue
            relative = path.relative_to(self.store.root).as_posix()
            if relative.startswith("templates/") and path.suffix == ".md":
                continue
            if relative.startswith("schemas/") and path.suffix == ".yaml":
                continue
            if relative.startswith("audit/") and path.suffix == ".jsonl":
                continue
            if relative.startswith("indexes/") and path.suffix in {".sqlite", ".tmp", ".lock"}:
                continue
            if path.suffix == ".md" and self._recognized_document_path(relative):
                continue
            errors.add("unrecognized_file")

    def _indexes(
        self,
        documents: dict[str, tuple[CognitionDocument, str]],
        errors: set[str],
    ) -> None:
        for principal in Principal:
            path = self.indexes.path_for(principal)
            if not path.exists():
                errors.add("missing_profile_index")
                continue
            expected = {
                document_id
                for document_id, (document, relative) in documents.items()
                if self.indexes.policies[principal].can_read(relative, document.project_id)
            }
            connection = sqlite3.connect(path)
            try:
                actual = {row[0] for row in connection.execute("SELECT id FROM documents")}
            except sqlite3.DatabaseError:
                errors.add("invalid_profile_index")
                continue
            finally:
                connection.close()
            if actual != expected:
                errors.add("profile_index_acl_mismatch")
