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


def main() -> None:
    payload = sys.stdin.read()
    real_stdin = sys.stdin
    for guard in GUARDS:
        path = os.path.join(_HOOK_DIR, guard)
        if not os.path.isfile(path):
            continue
        sys.stdin = io.StringIO(payload)
        try:
            runpy.run_path(path, run_name="__main__")
        except SystemExit as exc:
            if exc.code == 2:
                sys.exit(2)  # stderr de la garde déjà émis
        except Exception:
            # fail-open par garde (les gardes sécu gèrent leur fail-closed en interne)
            pass
        finally:
            sys.stdin = real_stdin
    sys.exit(0)


if __name__ == "__main__":
    main()
