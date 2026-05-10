#!/usr/bin/env python3
"""Ensure MCP forge-brain is running before automated tasks."""
import socket
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
START_PY = PROJECT_ROOT / "mcp-forge-brain" / "start.py"


def port_open(port: int = 8091, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, socket.timeout):
        return False


def main() -> None:
    if port_open():
        print("[ensure-mcp] MCP forge-brain already running on :8091")
        return

    if not START_PY.exists():
        print(f"[ensure-mcp] WARNING: {START_PY} not found", file=sys.stderr)
        sys.exit(1)

    DETACHED = 0x00000008
    CREATE_NEW_GROUP = 0x00000200
    NO_WINDOW = 0x08000000

    subprocess.Popen(
        [sys.executable, str(START_PY)],
        cwd=str(PROJECT_ROOT),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=DETACHED | CREATE_NEW_GROUP | NO_WINDOW,
        close_fds=True,
    )
    print("[ensure-mcp] MCP forge-brain started, waiting 3s...")
    import time
    time.sleep(3)

    if port_open():
        print("[ensure-mcp] MCP forge-brain confirmed on :8091")
    else:
        print("[ensure-mcp] WARNING: MCP not responding after start", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
