#!/usr/bin/env python3
"""PreToolUse Bash|Read|PowerShell — dispatcher : 1 spawn Python au lieu de 3.

Exécute en séquence les gardes existantes INCHANGÉES (commit-herestring-guard,
security-guard, vault-cat-guard) via runpy dans le même process. Chaque garde
lit le payload rejoué sur stdin et garde sa propre sémantique exit 0/2.
"""

import io
import os
import runpy
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDS = [
    "commit-herestring-guard.py",
    "security-guard.py",
    "vault-cat-guard.py",
]


class SecurityGuardFailure(RuntimeError):
    """Raised when the critical destructive-command guard cannot execute."""


def run_guard(name: str, payload: str, *, critical: bool = False) -> int:
    path = os.path.join(_HOOK_DIR, name)
    if not os.path.isfile(path):
        if critical:
            raise SecurityGuardFailure(f"critical guard missing: {name}")
        return 0
    real_stdin = sys.stdin
    sys.stdin = io.StringIO(payload)
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1
    except Exception as exc:
        if critical:
            raise SecurityGuardFailure(f"critical guard crashed: {name}") from exc
        return 0
    finally:
        sys.stdin = real_stdin
    return 0


def main() -> None:
    payload = sys.stdin.read()
    for guard in GUARDS:
        try:
            code = run_guard(guard, payload, critical=(guard == "security-guard.py"))
        except SecurityGuardFailure as exc:
            print(f"BLOCKED: {exc}", file=sys.stderr)
            sys.exit(2)
        if code == 2:
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
