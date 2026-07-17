"""Central path confinement for the forge-brain vault."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath


_WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[/\\]")


class PathSecurityError(ValueError):
    """Raised when a requested path is outside the configured vault policy."""


class VaultPathResolver:
    """Resolve relative paths while proving they remain inside the vault."""

    def __init__(self, vault_root: Path) -> None:
        self._root = vault_root.resolve(strict=True)

    @property
    def root(self) -> Path:
        return self._root

    def resolve(
        self,
        raw_path: str,
        *,
        allowed_extensions: frozenset[str] | None = frozenset({".md"}),
        must_exist: bool = False,
    ) -> Path:
        normalized = raw_path.replace("\\", "/")
        pure = PurePosixPath(normalized)
        if not normalized or pure.is_absolute() or _WINDOWS_ABSOLUTE.match(normalized):
            raise PathSecurityError("absolute paths are refused")
        if any(part == ".." for part in pure.parts):
            raise PathSecurityError("parent path segments are refused")
        if any(part in {"", "."} for part in pure.parts):
            raise PathSecurityError("non-canonical path segments are refused")

        candidate = self._root.joinpath(*pure.parts)
        try:
            canonical = candidate.resolve(strict=must_exist)
            canonical.relative_to(self._root)
        except (FileNotFoundError, OSError, ValueError) as exc:
            raise PathSecurityError("path escapes the vault or does not exist") from exc

        if allowed_extensions is not None and canonical.suffix.lower() not in allowed_extensions:
            allowed = ", ".join(sorted(allowed_extensions))
            raise PathSecurityError(f"extension must be one of: {allowed}")
        return canonical

    def relative(
        self,
        raw_path: str,
        *,
        allowed_extensions: frozenset[str] | None = frozenset({".md"}),
        must_exist: bool = False,
    ) -> str:
        resolved = self.resolve(
            raw_path,
            allowed_extensions=allowed_extensions,
            must_exist=must_exist,
        )
        return resolved.relative_to(self._root).as_posix()
