#!/usr/bin/env python3
"""PreToolUse Write|Edit|MultiEdit — dispatcher : 1 spawn Python au lieu de 3.

Exécute en séquence les gardes existantes INCHANGÉES (delegate-guard,
meta-commentary-detector, vault-write-guard) via runpy dans le même process.
Chaque garde lit le payload rejoué sur stdin et garde sa sémantique exit 0/2.
"""

import io
import os
import runpy
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDS = [
    "delegate-guard.py",
    "meta-commentary-detector.py",
    "vault-write-guard.py",
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
            pass  # fail-open par garde
        finally:
            sys.stdin = real_stdin
    sys.exit(0)


if __name__ == "__main__":
    main()
