"""Markdown/YAML canonical store implementation."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

import yaml

from forge_cognition.domain.errors import NotFoundError, ValidationError
from forge_cognition.domain.models import CognitionDocument, Project

from .paths import StorePathResolver


class FileCanonicalStore:
    def __init__(self, root: Path, max_document_bytes: int = 1_048_576) -> None:
        self.root = root.resolve(strict=True)
        self.paths = StorePathResolver(self.root)
        self.max_document_bytes = max_document_bytes

    def document_path(self, namespace: str, document_id: str) -> str:
        if not document_id or any(
            char not in "0123456789ABCDEFGHJKMNPQRSTVWXYZ" for char in document_id
        ):
            raise ValidationError("invalid document id")
        return f"{namespace.rstrip('/')}/{document_id}.md"

    def serialize_document(self, document: CognitionDocument) -> str:
        hashed = self.canonical_document(document)
        frontmatter = hashed.model_dump(mode="json", exclude={"body"})
        yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
        rendered = f"---\n{yaml_text}\n---\n\n{hashed.body.rstrip()}\n"
        if len(rendered.encode("utf-8")) > self.max_document_bytes:
            raise ValidationError("document exceeds configured size limit")
        return rendered

    @staticmethod
    def canonical_document(document: CognitionDocument) -> CognitionDocument:
        normalized = document.model_copy(
            update={"body": document.body.rstrip(), "content_hash": ""}
        )
        return normalized.with_hash()

    def parse_document(self, path: Path) -> CognitionDocument:
        raw = path.read_text(encoding="utf-8")
        if len(raw.encode("utf-8")) > self.max_document_bytes:
            raise ValidationError("document exceeds configured size limit")
        if not raw.startswith("---\n") or "\n---\n" not in raw[4:]:
            raise ValidationError(f"missing frontmatter: {path.name}")
        frontmatter_text, body = raw[4:].split("\n---\n", 1)
        frontmatter = yaml.safe_load(frontmatter_text) or {}
        document = CognitionDocument.model_validate({**frontmatter, "body": body.strip()})
        document.verify_hash()
        return document

    def get_document(self, document_id: str) -> tuple[CognitionDocument, str]:
        matches = []
        for document, relative_path in self.list_documents():
            if document.id == document_id:
                matches.append((document, relative_path))
        if len(matches) != 1:
            raise NotFoundError("resource not found")
        return matches[0]

    def list_documents(self) -> Iterable[tuple[CognitionDocument, str]]:
        excluded = {"templates", "schemas"}
        for path in sorted(self.root.rglob("*.md")):
            relative = path.relative_to(self.root).as_posix()
            if path.name == "README.md" or relative.split("/", 1)[0] in excluded:
                continue
            secured = self.paths.resolve(relative, must_exist=True)
            yield self.parse_document(secured), relative

    def project_path(self, project_id: str) -> str:
        if not project_id.startswith("PRJ-") or "/" in project_id or "\\" in project_id:
            raise ValidationError("invalid project id")
        matches = list((self.root / "projects").glob(f"{project_id}-*/project.yaml"))
        if len(matches) != 1:
            raise NotFoundError("resource not found")
        return matches[0].relative_to(self.root).as_posix()

    def get_project(self, project_id: str) -> Project:
        path = self.paths.resolve(self.project_path(project_id), must_exist=True)
        project = Project.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
        if project.content_hash != project.computed_hash():
            raise ValidationError(f"project hash mismatch for {project.id}")
        return project

    def serialize_project(self, project: Project) -> str:
        data = project.with_hash().model_dump(mode="json")
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


class AtomicMutation:
    def __init__(self, resolver: StorePathResolver) -> None:
        self._resolver = resolver
        self._snapshots: dict[Path, bytes | None] = {}
        self._created_directories: list[Path] = []

    def mkdir(self, relative_path: str) -> None:
        target = self._resolver.resolve(relative_path, must_exist=False)
        missing = []
        current = target
        while current != self._resolver.root and not current.exists():
            missing.append(current)
            current = current.parent
        target.mkdir(parents=True, exist_ok=True)
        self._created_directories.extend(reversed(missing))

    def _snapshot(self, path: Path) -> None:
        if path not in self._snapshots:
            self._snapshots[path] = path.read_bytes() if path.exists() else None

    def write_text(self, relative_path: str, content: str) -> None:
        target = self._resolver.resolve(relative_path, must_exist=False)
        self._snapshot(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, target)
        finally:
            temp = Path(temp_name)
            if temp.exists():
                temp.unlink()

    def move(self, source: str, target: str) -> None:
        source_path = self._resolver.resolve(source, must_exist=True)
        target_path = self._resolver.resolve(target, must_exist=False)
        self._snapshot(source_path)
        self._snapshot(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source_path, target_path)

    def rollback(self) -> None:
        for path, content in reversed(list(self._snapshots.items())):
            if content is None:
                if path.exists():
                    path.unlink()
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        for path in reversed(self._created_directories):
            try:
                path.rmdir()
            except OSError:
                pass
