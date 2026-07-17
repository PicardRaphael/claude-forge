"""Strict YAML configuration for a fixed MCP principal."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from forge_cognition.domain.models import Principal


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    store_path: Path
    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = Field(default=8092, ge=1, le=65535)
    lock_timeout_seconds: float = Field(default=5, gt=0)
    max_document_bytes: int = Field(default=1_048_576, ge=1024)
    profile: Principal
    allowed_projects: frozenset[str] = frozenset({"*"})


def load_config(config_path: Path, profile_path: Path | None = None) -> AppConfig:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if profile_path is not None:
        profile_raw = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
        raw["profile"] = profile_raw["principal"]
        raw["allowed_projects"] = profile_raw.get("allowed_projects", ["*"])
    config = AppConfig.model_validate(raw)
    base = config_path.resolve().parent.parent
    store_path = config.store_path
    if not store_path.is_absolute():
        store_path = (base / store_path).resolve()
    return config.model_copy(update={"store_path": store_path})
