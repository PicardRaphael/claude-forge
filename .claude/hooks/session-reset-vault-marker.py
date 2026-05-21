#!/usr/bin/env python3
"""Reset the vault-queried marker at SessionStart.

Triggered on: SessionStart

Removes <project>/.claude/.session-vault-queried so each new session starts
fresh and the next specialist launch requires a real vault query.

Marker uses existence-only semantics (no TTL) — this is the reset point.
"""
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
MARKER_PATH = os.path.join(_CLAUDE_DIR, ".session-vault-queried")


def main() -> None:
    try:
        if os.path.isfile(MARKER_PATH):
            os.remove(MARKER_PATH)
    except Exception:
        pass  # Fail-open — SessionStart hooks should never block startup
    sys.exit(0)


if __name__ == "__main__":
    main()
