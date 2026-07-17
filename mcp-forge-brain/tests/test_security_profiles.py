"""Negative security tests for path confinement and the server read-only profile."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from fastmcp import FastMCP

from src.config import FTSWeights
from src.database import BrainDB
from src.path_security import PathSecurityError, VaultPathResolver
from src.tools.brain import BrainTools, register_tools


def _tools(tmp_path: Path) -> tuple[BrainTools, Path]:
    vault = tmp_path / "vault" / "claude-forge"
    vault.mkdir(parents=True)
    db = BrainDB(tmp_path / "brain.db", FTSWeights())
    db.create_schema()
    return BrainTools(db, vault), vault


@pytest.mark.parametrize(
    "candidate",
    ["../cognition-store/secret.md", "/tmp/secret.md", r"C:\secret.md"],
)
def test_resolver_rejects_escape_forms(tmp_path: Path, candidate: str) -> None:
    _, vault = _tools(tmp_path)
    with pytest.raises(PathSecurityError):
        VaultPathResolver(vault).resolve(candidate)


def test_resolver_rejects_forbidden_extension(tmp_path: Path) -> None:
    _, vault = _tools(tmp_path)
    with pytest.raises(PathSecurityError, match="extension"):
        VaultPathResolver(vault).resolve("note.json")


def test_symlink_to_cognition_store_is_refused(tmp_path: Path) -> None:
    tools, vault = _tools(tmp_path)
    cognition = tmp_path / "cognition-store"
    cognition.mkdir()
    secret = cognition / "private.md"
    secret.write_text("secret", encoding="utf-8")
    link = vault / "alias.md"
    try:
        link.symlink_to(secret)
    except OSError:
        pytest.skip("symlinks unavailable on this Windows environment")

    result = tools.read_note_by_path("alias.md")
    assert result.startswith("REFUS:")
    assert "secret" not in result


def test_read_only_profile_has_no_mutation_or_transcript_tools(tmp_path: Path) -> None:
    tools, _ = _tools(tmp_path)
    mcp = FastMCP(name="forge-brain-read-only-test")
    register_tools(mcp, tools, read_only=True)
    names = {tool.name for tool in asyncio.run(mcp._list_tools())}

    assert {"search_brain", "read_note", "read_note_by_path"} <= names
    assert not {
        "create_note",
        "append_note",
        "update_note",
        "move_note",
        "delete_note",
        "bulk_update_property",
        "search_sessions",
        "search_tool_events",
    } & names


def test_full_profile_keeps_mutation_tools(tmp_path: Path) -> None:
    tools, _ = _tools(tmp_path)
    mcp = FastMCP(name="forge-brain-full-test")
    register_tools(mcp, tools)
    names = {tool.name for tool in asyncio.run(mcp._list_tools())}
    assert {"create_note", "move_note", "search_sessions"} <= names


def test_read_only_app_never_constructs_git_mutation_adapter(tmp_path: Path, monkeypatch) -> None:
    from src import server

    vault = tmp_path / "vault"
    vault.mkdir()
    config = tmp_path / "config.yaml"
    config.write_text(
        f"vault_path: '{vault.as_posix()}'\n"
        f"db_path: '{(tmp_path / 'brain.db').as_posix()}'\n"
        "profile: read-only\n"
        "sessions:\n  enabled: false\n"
        "tool_events:\n  enabled: false\n",
        encoding="utf-8",
    )

    def forbidden_git(*_args, **_kwargs):
        raise AssertionError("read-only profile constructed GitSync")

    monkeypatch.setattr(server, "GitSync", forbidden_git)
    app = server.create_app(config)
    names = {tool.name for tool in asyncio.run(app._list_tools())}
    assert "create_note" not in names
