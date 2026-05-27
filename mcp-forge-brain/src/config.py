"""Load and validate config.yaml."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class GitConfig:
    auto_commit: bool = False
    pull_interval_seconds: int = 300
    push_interval_seconds: int = 1800
    remote: str = "origin"
    main_branch: str = "main"


@dataclass
class WatcherConfig:
    poll_interval_seconds: int = 30


@dataclass
class FTSWeights:
    file_stem: float = 10.0
    content: float = 1.0
    aliases: float = 8.0


@dataclass
class FTSConfig:
    weights: FTSWeights = field(default_factory=FTSWeights)


@dataclass
class SessionsConfig:
    enabled: bool = False
    path: Path = field(default_factory=lambda: Path.home() / ".claude" / "projects")
    include_subagents: bool = False


@dataclass
class AppConfig:
    vault_path: Path = field(default_factory=lambda: Path("/data/neoteem-brain"))
    db_path: Path = field(default_factory=lambda: Path("/data/brain.db"))
    port: int = 8080
    git: GitConfig = field(default_factory=GitConfig)
    watcher: WatcherConfig = field(default_factory=WatcherConfig)
    fts: FTSConfig = field(default_factory=FTSConfig)
    sessions: SessionsConfig = field(default_factory=SessionsConfig)
    excluded_dirs: list[str] = field(
        default_factory=lambda: [
            ".obsidian", ".claude", "Templates", "Daily",
            "plugin", "claude-chat-plugins", "doc", "mcp-obsidian-brain",
        ]
    )


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        raw = yaml.safe_load(f)
    git_raw = raw.get("git", {})
    watcher_raw = raw.get("watcher", {})
    fts_raw = raw.get("fts", {})
    weights_raw = fts_raw.get("weights", {})
    sessions_raw = dict(raw.get("sessions", {}))
    if "path" in sessions_raw:
        sessions_raw["path"] = Path(sessions_raw["path"]).expanduser()
    return AppConfig(
        vault_path=Path(raw["vault_path"]),
        db_path=Path(raw["db_path"]),
        port=raw.get("port", 8080),
        git=GitConfig(**git_raw),
        watcher=WatcherConfig(**watcher_raw),
        fts=FTSConfig(weights=FTSWeights(**weights_raw)),
        sessions=SessionsConfig(**sessions_raw),
        excluded_dirs=raw.get("excluded_dirs", [
            ".obsidian", ".claude", "Templates", "Daily",
            "plugin", "claude-chat-plugins", "doc", "mcp-obsidian-brain",
        ]),
    )
