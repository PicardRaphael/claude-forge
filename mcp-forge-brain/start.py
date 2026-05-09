"""Launcher for forge-brain MCP server — self-contained, no external deps."""

import os
import sys
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))

from src.server import create_app

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [forge-brain] %(levelname)s %(message)s",
    )
    os.chdir(PROJECT_ROOT)
    config_path = SCRIPT_DIR / "config.yaml"
    app = create_app(config_path)
    app.run(transport="streamable-http", port=app._brain_cfg.port)

if __name__ == "__main__":
    main()
