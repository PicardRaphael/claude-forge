#!/usr/bin/env python3
"""
SessionStart hook — auto-démarre le MCP forge-brain si le port 8091 ne répond pas.
Toujours exit 0, jamais bloquant.
"""
import json
import os
import socket
import subprocess
import sys
from pathlib import Path


def port_open(host: str = "127.0.0.1", port: int = 8091, timeout: float = 1.0) -> bool:
    """Vérifie si le port répond via socket — pas de curl, pas de subprocess."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, socket.timeout):
        return False


def main() -> None:
    # Consommer stdin (SessionStart envoie du JSON) — ne pas laisser le pipe en attente
    try:
        sys.stdin.read()
    except Exception:
        pass

    # Résoudre les chemins via __file__ — jamais de chemin en dur
    hook_path = Path(__file__).resolve()
    project_root = hook_path.parents[2]  # .claude/hooks/mcp-autostart.py → root
    start_py = project_root / "mcp-forge-brain" / "start.py"

    if port_open():
        print("MCP forge-brain déjà actif sur port 8091")
        sys.exit(0)

    # MCP non joignable — tenter le démarrage
    if not start_py.exists():
        print(
            f"[mcp-autostart] WARNING: {start_py} introuvable — MCP forge-brain non démarré",
            flush=True,
        )
        sys.exit(0)

    # Flags Windows pour processus détaché qui survit à la fin du hook
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NO_WINDOW = 0x08000000

    try:
        subprocess.Popen(
            [sys.executable, str(start_py)],
            cwd=str(project_root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
            close_fds=True,
        )
        print("MCP forge-brain démarré sur port 8091")
    except Exception as exc:
        print(f"[mcp-autostart] WARNING: échec du démarrage MCP — {exc}", flush=True)

    sys.exit(0)


if __name__ == "__main__":
    main()
