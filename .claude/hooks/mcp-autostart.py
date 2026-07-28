#!/usr/bin/env python3
"""
SessionStart hook — auto-démarre le MCP forge-brain si le port 8091 ne répond pas.
Toujours exit 0, jamais bloquant.
"""
import socket
import subprocess
import sys
import time
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

    # Sortie de l'enfant vers un log — jamais DEVNULL : une panne de boot doit
    # rester diagnosticable (silence = 11 jours d'indisponibilité non détectés,
    # 17-28 juil. 2026).
    log_path = project_root / "mcp-forge-brain" / "logs" / "startup.log"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        child_out = open(log_path, "ab")
    except Exception:
        child_out = subprocess.DEVNULL

    # Interpréteur : le venv du projet d'abord. `sys.executable` est l'interpréteur
    # AMBIANT — ses deps ne sont pas garanties selon le contexte d'appel du hook
    # (ModuleNotFoundError: fastmcp observé 28 juil. 2026 alors que le même
    # interpréteur réussissait en direct). Fallback ambiant si pas de venv.
    venv_dir = project_root / "mcp-forge-brain" / ".venv"
    python_exe = next(
        (
            str(c)
            for c in (venv_dir / "Scripts" / "python.exe", venv_dir / "bin" / "python")
            if c.exists()
        ),
        sys.executable,
    )

    try:
        subprocess.Popen(
            [python_exe, str(start_py)],
            cwd=str(project_root),
            stdin=subprocess.DEVNULL,
            stdout=child_out,
            stderr=child_out,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
            close_fds=True,
        )
    except Exception as exc:
        print(f"[mcp-autostart] WARNING: échec du démarrage MCP — {exc}", flush=True)
        sys.exit(0)

    # Ne PAS annoncer le succès sur la base du Popen : il rend la main au fork,
    # avant tout bind. Le port s'ouvre en ~2s (mesuré) — vérifier réellement.
    # Budget borné par DEADLINE, pas par un compteur d'itérations : chaque tour
    # coûte sleep + timeout du check, donc compter les tours sous-estime
    # (13,3s mesurés pour un « budget 6s » naïf, au-delà du timeout 10s).
    deadline = time.monotonic() + 6.0
    while time.monotonic() < deadline:
        if port_open(timeout=0.25):
            print("MCP forge-brain démarré sur port 8091")
            sys.exit(0)
        time.sleep(0.25)

    print(
        f"[mcp-autostart] WARNING: MCP forge-brain lancé mais port 8091 toujours "
        f"fermé — vault indisponible. Voir {log_path}",
        flush=True,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
