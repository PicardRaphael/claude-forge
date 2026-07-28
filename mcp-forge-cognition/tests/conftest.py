from __future__ import annotations

from pathlib import Path

import pytest

from forge_cognition.application.service import CognitionService
from forge_cognition.application.authorization import PipelineAuthorization
from forge_cognition.domain.models import Principal
from forge_cognition.domain.policies import AccessPolicy
from forge_cognition.infrastructure.audit import JsonlAuditLog
from forge_cognition.infrastructure.file_store import FileCanonicalStore
from forge_cognition.infrastructure.lexical_index import SQLiteLexicalIndex
from forge_cognition.infrastructure.transactions import MutationCoordinator


def _make_store(root: Path) -> None:
    for relative in (
        "schemas",
        "templates",
        "inbox/forge-product",
        "inbox/red-team",
        "inbox/architect-brainstorm",
        "shared/context",
        "shared/procedures",
        "shared/calibration",
        "projects",
        "private/forge-product/episodes",
        "private/forge-product/lessons",
        "private/forge-product/calibration",
        "private/red-team/episodes",
        "private/red-team/lessons",
        "private/red-team/calibration",
        "private/architect-brainstorm/episodes",
        "private/architect-brainstorm/lessons",
        "private/architect-brainstorm/calibration",
        "audit",
        "indexes",
        "archive",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)
    (root / "STORE_VERSION").write_text("1\n", encoding="utf-8")
    (root / "schemas" / "document-v1.yaml").write_text("schema_version: 1\n", encoding="utf-8")
    (root / "schemas" / "project-v1.yaml").write_text("schema_version: 1\n", encoding="utf-8")


@pytest.fixture
def services(tmp_path: Path) -> dict[Principal, CognitionService]:
    root = tmp_path / "cognition-store"
    _make_store(root)
    store = FileCanonicalStore(root)
    policies = {principal: AccessPolicy(principal, frozenset({"*"})) for principal in Principal}
    authorization = PipelineAuthorization(store, policies)
    indexes = SQLiteLexicalIndex(store, policies, authorization)
    indexes.rebuild_all()
    audit = JsonlAuditLog(root / "audit" / "events.jsonl")
    transactions = MutationCoordinator(store, indexes, audit, timeout_seconds=0.3)
    return {
        principal: CognitionService(
            principal,
            policies[principal],
            store,
            indexes,
            transactions,
            authorization,
        )
        for principal in Principal
    }
