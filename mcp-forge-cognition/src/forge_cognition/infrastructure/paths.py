"""Internal store confinement; no path is supplied by an MCP caller."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from forge_cognition.domain.errors import ValidationError


class StorePathResolver:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve(strict=True)

    def resolve(self, relative_path: str, *, must_exist: bool = False) -> Path:
        pure = PurePosixPath(relative_path)
        if (
            not relative_path
            or pure.is_absolute()
            or re.match(r"^[A-Za-z]:[/\\]", relative_path)
            or ".." in pure.parts
        ):
            raise ValidationError("invalid internal store path")
        candidate = self.root.joinpath(*pure.parts)
        try:
            resolved = candidate.resolve(strict=must_exist)
            resolved.relative_to(self.root)
        except (FileNotFoundError, OSError, ValueError) as exc:
            raise ValidationError("internal path escapes cognition-store") from exc
        return resolved

    def relative(self, path: Path) -> str:
        try:
            return path.resolve(strict=True).relative_to(self.root).as_posix()
        except (FileNotFoundError, OSError, ValueError) as exc:
            raise ValidationError("path is outside cognition-store") from exc
