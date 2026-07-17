"""MCP Obsidian Brain v2 — SQLite FTS5 backed, HTTP mode."""

import asyncio
import logging
import sys
import os
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

from fastmcp import FastMCP
from src.config import load_config
from src.database import BrainDB
from src.watcher import VaultWatcher
from src.sessions_db import SessionDB
from src.sessions_watcher import SessionWatcher
from src.tool_events_db import ToolEventsDB
from src.tool_events_watcher import ToolEventsWatcher
from src.git_sync import GitSync
from src.tools.brain import BrainTools, register_tools
from src import usage_log

logger = logging.getLogger("obsidian-brain")


def create_app(config_path: Path | None = None, profile_override: str | None = None) -> FastMCP:
    """Build the MCP app: load config, create DB, index vault, register tools."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    cfg = load_config(config_path)
    if profile_override is not None:
        if profile_override not in {"full", "read-only"}:
            raise ValueError("profile must be 'full' or 'read-only'")
        cfg.profile = profile_override

    db = BrainDB(cfg.db_path, cfg.fts.weights)
    db.create_schema()

    # Configure usage logging — store next to the MCP install (mcp-forge-brain/logs/)
    mcp_install_dir = Path(__file__).parent.parent
    usage_log.configure(mcp_install_dir / "logs")

    watcher = VaultWatcher(cfg.vault_path, db, cfg.excluded_dirs)
    git_sync = None if cfg.profile == "read-only" else GitSync(cfg.vault_path, cfg.git)

    # --- Sessions transcript index (optional) ---
    sessions_db = None
    sessions_watcher = None
    if cfg.sessions.enabled and cfg.profile != "read-only":
        sessions_db = SessionDB(db._conn)  # noqa: SLF001 — share the vault connection
        sessions_db.create_schema()
        sessions_watcher = SessionWatcher(
            cfg.sessions.path, sessions_db, cfg.sessions.include_subagents
        )

    # --- Tool events index (optional) ---
    tool_events_db = None
    tool_events_watcher = None
    if cfg.tool_events.enabled and cfg.profile != "read-only":
        tool_events_db = ToolEventsDB(db._conn)  # noqa: SLF001 — share the vault connection
        tool_events_db.create_schema()
        tool_events_watcher = ToolEventsWatcher(
            cfg.tool_events.path, tool_events_db, cfg.tool_events.include_subagents
        )

    brain_tools = BrainTools(db, cfg.vault_path, git_sync, sessions_db, tool_events_db)

    # --- Initial vault index ---
    logger.info("Indexing vault: %s", cfg.vault_path)
    result = watcher.scan()
    logger.info(
        "Indexed: %d added, %d modified, %d deleted",
        result.added, result.modified, result.deleted,
    )

    # --- Initial sessions index (eager, with timing) ---
    if sessions_watcher is not None:
        logger.info("Indexing sessions: %s", cfg.sessions.path)
        t0 = time.monotonic()
        s_result = sessions_watcher.scan()
        elapsed = time.monotonic() - t0
        logger.info(
            "Sessions indexed in %.2fs: %d files (+%d ~%d -%d), %d messages",
            elapsed, s_result.added + s_result.modified,
            s_result.added, s_result.modified, s_result.deleted, s_result.messages,
        )

    # --- Initial tool events index (eager, with timing) ---
    if tool_events_watcher is not None:
        logger.info("Indexing tool events: %s", cfg.tool_events.path)
        t0 = time.monotonic()
        te_result = tool_events_watcher.scan()
        elapsed = time.monotonic() - t0
        logger.info(
            "Tool events indexed in %.2fs: %d files (+%d ~%d -%d), %d events",
            elapsed, te_result.added + te_result.modified,
            te_result.added, te_result.modified, te_result.deleted, te_result.events,
        )

    # --- Lifespan: background loops (watcher poll, git pull, git push) ---
    @asynccontextmanager
    async def lifespan(app):
        """Start background tasks on startup, cancel them on shutdown."""
        tasks: list[asyncio.Task] = []

        async def _poll_watcher():
            while True:
                await asyncio.sleep(cfg.watcher.poll_interval_seconds)
                try:
                    r = watcher.scan()
                    if r.added or r.modified or r.deleted:
                        logger.info(
                            "Watcher: +%d ~%d -%d",
                            r.added, r.modified, r.deleted,
                        )
                except Exception:
                    logger.exception("Watcher poll error")

        async def _poll_sessions():
            while True:
                await asyncio.sleep(cfg.watcher.poll_interval_seconds)
                try:
                    r = sessions_watcher.scan()
                    if r.added or r.modified or r.deleted:
                        logger.info(
                            "Sessions watcher: +%d ~%d -%d (%d msgs)",
                            r.added, r.modified, r.deleted, r.messages,
                        )
                except Exception:
                    logger.exception("Sessions poll error")

        async def _poll_tool_events():
            while True:
                await asyncio.sleep(cfg.watcher.poll_interval_seconds)
                try:
                    r = tool_events_watcher.scan()
                    if r.added or r.modified or r.deleted:
                        logger.info(
                            "Tool events watcher: +%d ~%d -%d (%d events)",
                            r.added, r.modified, r.deleted, r.events,
                        )
                except Exception:
                    logger.exception("Tool events poll error")

        async def _git_pull():
            while True:
                await asyncio.sleep(cfg.git.pull_interval_seconds)
                try:
                    git_sync.pull()
                    r = watcher.scan()
                    if r.added or r.modified or r.deleted:
                        logger.info(
                            "Git pull reindex: +%d ~%d -%d",
                            r.added, r.modified, r.deleted,
                        )
                except Exception:
                    logger.exception("Git pull error")

        async def _git_push():
            while True:
                await asyncio.sleep(cfg.git.push_interval_seconds)
                try:
                    if git_sync.get_active_branches():
                        git_sync.push_all()
                        logger.info("Git push done")
                except Exception:
                    logger.exception("Git push error")

        tasks.append(asyncio.create_task(_poll_watcher()))
        if sessions_watcher is not None:
            tasks.append(asyncio.create_task(_poll_sessions()))
        if tool_events_watcher is not None:
            tasks.append(asyncio.create_task(_poll_tool_events()))
        if git_sync is not None:
            tasks.append(asyncio.create_task(_git_pull()))
            tasks.append(asyncio.create_task(_git_push()))
        logger.info(
            "Background loops started (watcher=%ds, git=%s)",
            cfg.watcher.poll_interval_seconds,
            "enabled" if git_sync is not None else "disabled",
        )

        try:
            yield
        finally:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            logger.info("Background loops stopped")

    # --- Build FastMCP app ---
    mcp = FastMCP(
        name="forge-brain",
        instructions=(
            "Acces au vault forge-brain — base de connaissances IA, techniques, projets, casquettes de vie. "
            "search_brain cherche dans TOUT le vault d'un coup."
        ),
        lifespan=lifespan,
    )

    register_tools(mcp, brain_tools, read_only=cfg.profile == "read-only")

    # Store config on the module for external access (tests, CLI)
    mcp._brain_cfg = cfg  # noqa: SLF001

    return mcp


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
    )
    app = create_app()
    app.run(transport="streamable-http", port=app._brain_cfg.port)  # noqa: SLF001


if __name__ == "__main__":
    main()
