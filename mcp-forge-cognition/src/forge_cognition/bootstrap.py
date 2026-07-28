"""Composition root for CLI and MCP transports."""

from __future__ import annotations

from pathlib import Path

import yaml

from forge_cognition.application.service import CognitionService
from forge_cognition.application.authorization import PipelineAuthorization
from forge_cognition.config.loader import AppConfig
from forge_cognition.domain.models import Principal
from forge_cognition.domain.policies import AccessPolicy
from forge_cognition.infrastructure.audit import JsonlAuditLog
from forge_cognition.infrastructure.file_store import FileCanonicalStore
from forge_cognition.infrastructure.lexical_index import SQLiteLexicalIndex
from forge_cognition.infrastructure.transactions import MutationCoordinator
from forge_cognition.infrastructure.runtime_compat import require_pipeline_runtime


def build_service(config: AppConfig) -> CognitionService:
    store = FileCanonicalStore(config.store_path, config.max_document_bytes)
    require_pipeline_runtime(store)
    profile_dir = Path(__file__).resolve().parents[2] / "profiles"
    policies = {}
    for principal in Principal:
        profile = yaml.safe_load(
            (profile_dir / f"{principal.value}.yaml").read_text(encoding="utf-8")
        )
        policies[principal] = AccessPolicy(
            principal, frozenset(profile.get("allowed_projects", ["*"]))
        )
    policies[config.profile] = AccessPolicy(config.profile, config.allowed_projects)
    authorization = PipelineAuthorization(store, policies)
    indexes = SQLiteLexicalIndex(store, policies, authorization)
    audit = JsonlAuditLog(store.root / "audit" / "events.jsonl")
    transactions = MutationCoordinator(
        store,
        indexes,
        audit,
        timeout_seconds=config.lock_timeout_seconds,
    )
    return CognitionService(
        config.profile,
        policies[config.profile],
        store,
        indexes,
        transactions,
        authorization,
    )
