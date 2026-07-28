from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from pydantic import ValidationError as PydanticValidationError

from forge_cognition.domain.errors import NotFoundError, ValidationError
from forge_cognition.domain.models import Principal
from forge_cognition.domain.policies import AccessPolicy
from forge_cognition.config.loader import AppConfig
from forge_cognition.infrastructure.paths import StorePathResolver
from forge_cognition.presentation.mcp.server import create_mcp


def _project(product) -> str:
    return product.project_create(
        name="Private ACL",
        slug="private-acl",
        objective="Test ACL",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="project-acl",
    )["project_id"]


def test_red_team_cannot_get_or_search_product_private_episode(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    reviewer = services[Principal.RED_TEAM]
    project_id = _project(product)
    episode = product.episode_record(
        project_id=project_id,
        title="SECRET-ORCHID",
        prediction="SECRET-ORCHID only private",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.4,
        confidence_after=0.5,
        idempotency_key="product-private",
    )
    with pytest.raises(NotFoundError, match="resource not found"):
        reviewer.context_get(episode["id"])
    with pytest.raises(NotFoundError, match="resource not found"):
        reviewer.context_get("SECRET-ORCHID")
    assert reviewer.context_search("SECRET-ORCHID")["results"] == []


def test_product_cannot_read_red_team_private_episode(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    reviewer = services[Principal.RED_TEAM]
    project_id = _project(product)
    episode = reviewer.episode_record(
        project_id=project_id,
        title="Reviewer private",
        prediction="risk",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.6,
        confidence_after=0.7,
        idempotency_key="review-private",
    )
    with pytest.raises(NotFoundError):
        product.context_get(episode["id"])


@pytest.mark.parametrize(
    ("owner", "reader"),
    [
        (owner, reader)
        for owner in (
            Principal.FORGE_PRODUCT,
            Principal.ARCHITECT_BRAINSTORM,
            Principal.RED_TEAM,
        )
        for reader in (
            Principal.FORGE_PRODUCT,
            Principal.ARCHITECT_BRAINSTORM,
            Principal.RED_TEAM,
        )
        if owner != reader
    ],
)
def test_all_role_pairs_keep_private_memory_isolated(services, owner, reader) -> None:
    project_id = _project(services[Principal.FORGE_PRODUCT])
    token = f"PRIVATE-{owner.value}-{reader.value}"
    episode = services[owner].episode_record(
        project_id=project_id,
        title=token,
        prediction=token,
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.5,
        confidence_after=0.5,
        idempotency_key=token,
    )
    with pytest.raises(NotFoundError, match="resource not found"):
        services[reader].context_get(episode["id"])
    assert services[reader].context_search(token)["results"] == []


def test_empty_query_is_refused(services) -> None:
    with pytest.raises(ValidationError, match="must not be empty"):
        services[Principal.RED_TEAM].context_search("   ")


@pytest.mark.parametrize(
    "path", ["../vault/claude-forge/secret.md", "/absolute.md", "C:/absolute.md"]
)
def test_store_path_escape_is_refused(tmp_path: Path, path: str) -> None:
    root = tmp_path / "cognition-store"
    root.mkdir()
    with pytest.raises(ValidationError):
        StorePathResolver(root).resolve(path)


def test_store_symlink_to_vault_is_refused(tmp_path: Path) -> None:
    root = tmp_path / "cognition-store"
    root.mkdir()
    vault = tmp_path / "vault" / "claude-forge"
    vault.mkdir(parents=True)
    secret = vault / "secret.md"
    secret.write_text("secret", encoding="utf-8")
    alias = root / "alias.md"
    try:
        alias.symlink_to(secret)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(ValidationError):
        StorePathResolver(root).resolve("alias.md", must_exist=True)


def test_mcp_tools_expose_no_path_or_principal_argument(services) -> None:
    mcp = create_mcp(services[Principal.RED_TEAM])
    tools = asyncio.run(mcp._list_tools())
    forbidden_tools = {
        "read_file",
        "write_file",
        "update_file",
        "delete_file",
        "move_file",
        "list_directory",
    }
    assert not forbidden_tools & {tool.name for tool in tools}
    for tool in tools:
        properties = tool.parameters.get("properties", {})
        assert "principal" not in properties
        assert "path" not in properties


def test_privileged_tools_are_absent_from_unprivileged_registries(services) -> None:
    product_names = {
        tool.name
        for tool in asyncio.run(create_mcp(services[Principal.FORGE_PRODUCT])._list_tools())
    }
    reviewer_names = {
        tool.name for tool in asyncio.run(create_mcp(services[Principal.RED_TEAM])._list_tools())
    }
    for names in (product_names, reviewer_names):
        assert "memory_commit" not in names
        assert "memory_deprecate" not in names
        assert "project_record_outcome" not in names
    assert "review_record" not in product_names
    assert "project_create" not in reviewer_names


def test_pipeline_tool_registries_are_role_exact(services) -> None:
    names = {
        principal: {
            tool.name for tool in asyncio.run(create_mcp(services[principal])._list_tools())
        }
        for principal in Principal
    }
    assert {
        "pipeline_project_create",
        "pipeline_publish_cdc",
    } <= names[Principal.FORGE_PRODUCT]
    assert "pipeline_publish_architecture" in names[Principal.ARCHITECT_BRAINSTORM]
    assert "pipeline_record_verdict" in names[Principal.RED_TEAM]
    assert {
        "pipeline_approve_cdc",
        "pipeline_approve_architecture",
        "pipeline_record_human_rework_decision",
        "pipeline_create_development_handoff",
    } <= names[Principal.CURATOR]
    curator_only = {
        "pipeline_approve_cdc",
        "pipeline_approve_architecture",
        "pipeline_record_human_rework_decision",
        "pipeline_create_development_handoff",
    }
    for principal in (
        Principal.FORGE_PRODUCT,
        Principal.ARCHITECT_BRAINSTORM,
        Principal.RED_TEAM,
    ):
        assert not curator_only & names[principal]


def test_attempt_to_override_principal_is_rejected_by_mcp_schema(services) -> None:
    mcp = create_mcp(services[Principal.RED_TEAM])
    with pytest.raises(Exception):
        asyncio.run(mcp.call_tool("context_get", {"id": "unknown", "principal": "curator"}))


def test_unknown_principal_is_rejected_by_typed_config(tmp_path: Path) -> None:
    with pytest.raises(PydanticValidationError):
        AppConfig(store_path=tmp_path, profile="unknown")


def test_project_scope_is_deny_by_default() -> None:
    policy = AccessPolicy(Principal.RED_TEAM, frozenset({"PRJ-2026-001"}))
    assert policy.can_read("projects/PRJ-2026-001-ok/neutral/x.md", "PRJ-2026-001")
    assert not policy.can_read("projects/PRJ-2026-002-no/neutral/x.md", "PRJ-2026-002")
