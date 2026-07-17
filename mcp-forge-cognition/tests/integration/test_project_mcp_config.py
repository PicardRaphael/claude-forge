"""Project MCP clients must launch only the trusted Curator profile."""

from __future__ import annotations

import json
import tomllib
from collections.abc import Mapping
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SERVER_NAME = "forge-cognition-curator"
EXPECTED_ARGS = [
    "run",
    "--project",
    "mcp-forge-cognition",
    "python",
    "mcp-forge-cognition/start_stdio.py",
    "--profile",
    "curator",
]


def _assert_curator_only(servers: Mapping[str, Mapping[str, object]]) -> None:
    cognition_servers = {name for name in servers if name.startswith("forge-cognition")}

    assert cognition_servers == {SERVER_NAME}
    assert servers[SERVER_NAME]["command"] == "uv"
    assert servers[SERVER_NAME]["args"] == EXPECTED_ARGS


def test_claude_project_config_launches_only_curator() -> None:
    config = json.loads((REPOSITORY_ROOT / ".mcp.json").read_text(encoding="utf-8"))

    _assert_curator_only(config["mcpServers"])


def test_codex_project_config_launches_only_curator() -> None:
    with (REPOSITORY_ROOT / ".codex" / "config.toml").open("rb") as config_file:
        config = tomllib.load(config_file)

    _assert_curator_only(config["mcp_servers"])
