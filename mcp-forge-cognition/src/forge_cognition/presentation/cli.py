"""Serve, rebuild-index and verify-store commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forge_cognition.bootstrap import build_service
from forge_cognition.config.loader import load_config
from forge_cognition.domain.models import Principal
from forge_cognition.presentation.mcp.server import create_mcp


def main(default_transport: str | None = None) -> None:
    project_dir = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(prog="forge-cognition")
    parser.add_argument(
        "command", nargs="?", choices=("serve", "rebuild-index", "verify-store"), default="serve"
    )
    parser.add_argument("--config", type=Path, default=project_dir / "config.example.yaml")
    parser.add_argument("--profile", choices=[item.value for item in Principal], required=True)
    parser.add_argument(
        "--transport", choices=("stdio", "streamable-http"), default=default_transport
    )
    args = parser.parse_args()

    profile_path = project_dir / "profiles" / f"{args.profile}.yaml"
    config = load_config(args.config, profile_path)
    if args.transport:
        config = config.model_copy(update={"transport": args.transport})
    service = build_service(config)

    if args.command == "rebuild-index":
        service.indexes.rebuild(config.profile)
        print(json.dumps(service.indexes.health(), indent=2, sort_keys=True))
        return
    if args.command == "verify-store":
        health = service.system_health()
        print(json.dumps(health, indent=2, sort_keys=True))
        if health["consistency_errors"]:
            raise SystemExit(1)
        return

    app = create_mcp(service)
    if config.transport == "streamable-http":
        app.run(transport="streamable-http", host=config.host, port=config.port)
    else:
        app.run(transport="stdio")
