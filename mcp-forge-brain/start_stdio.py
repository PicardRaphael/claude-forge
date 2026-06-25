"""Launcher stdio pour forge-brain MCP server (Claude Desktop Chat / Cowork).

Identique a start.py mais transport stdio au lieu de streamable-http.
En stdio, stdout est le canal du protocole MCP (JSON-RPC) : les logs DOIVENT
partir sur stderr, jamais sur stdout, sinon le handshake casse.
"""

import os
import sys
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))

from src.server import create_app


def main():
    # Logs sur stderr — stdout est reserve au protocole MCP en mode stdio.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [forge-brain] %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    # vault_path / db_path de config.yaml sont relatifs a la racine du repo.
    os.chdir(PROJECT_ROOT)
    config_path = SCRIPT_DIR / "config.yaml"
    app = create_app(config_path)
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
