"""MCP Obsidian Brain v2 — SQLite FTS5 backed, HTTP mode."""

import asyncio
import logging
import sys
import os
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from src.config import load_config
from src.database import BrainDB
from src.watcher import VaultWatcher
from src.git_sync import GitSync
from src.tools.brain import BrainTools, register_tools
from src import usage_log

logger = logging.getLogger("obsidian-brain")


def create_app(config_path: Path | None = None) -> FastMCP:
    """Build the MCP app: load config, create DB, index vault, register tools."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    cfg = load_config(config_path)

    db = BrainDB(cfg.db_path, cfg.fts.weights)
    db.create_schema()

    # Configure usage logging — store next to the MCP install (mcp-forge-brain/logs/)
    mcp_install_dir = Path(__file__).parent.parent
    usage_log.configure(mcp_install_dir / "logs")

    watcher = VaultWatcher(cfg.vault_path, db, cfg.excluded_dirs)
    git_sync = GitSync(cfg.vault_path, cfg.git)
    brain_tools = BrainTools(db, cfg.vault_path, git_sync)

    # --- Initial vault index ---
    logger.info("Indexing vault: %s", cfg.vault_path)
    result = watcher.scan()
    logger.info(
        "Indexed: %d added, %d modified, %d deleted",
        result.added, result.modified, result.deleted,
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
        tasks.append(asyncio.create_task(_git_pull()))
        tasks.append(asyncio.create_task(_git_push()))
        logger.info(
            "Background loops started (watcher=%ds, pull=%ds, push=%ds)",
            cfg.watcher.poll_interval_seconds,
            cfg.git.pull_interval_seconds,
            cfg.git.push_interval_seconds,
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

    register_tools(mcp, brain_tools)

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
