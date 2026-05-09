#!/usr/bin/env python3
"""Stop hook — block session end if devil's advocate was not run.

Triggered on: Stop

Logic:
  1. If stop_hook_active in payload → exit 0 (already in continuation, avoid infinite loop)
  2. If .claude/.devil-advocate-needed does NOT exist → exit 0 (no productive agent ran)
  3. If .claude/.devil-advocate-done EXISTS → exit 0 (devil's advocate was run)
  4. Otherwise → print JSON block decision to stdout, exit 0

JSON block format (stdout):
  {"decision": "block", "reason": "..."}

NOTE: Stop hooks block via JSON + exit 0. exit 2 has no special meaning here.
Markers are reset at SessionStart by session-reminder.py.
Marker .devil-advocate-done is written by devil-advocate-tracker.py.
Marker .devil-advocate-needed is written by devil-advocate-guard.py.
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)

NEEDED_MARKER = os.path.join(_CLAUDE_DIR, ".devil-advocate-needed")
DONE_MARKER = os.path.join(_CLAUDE_DIR, ".devil-advocate-done")

BLOCK_REASON = (
    "Devil's advocate non lance sur les livrables de cette session. "
    "Lancer l'agent `devils-advocate` avant de terminer. "
    "Pipeline : architect-first -> implementation -> test/review -> devils-advocate -> livraison."
)


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        # Guard against infinite loop in stop-hook continuation
        if data.get("stop_hook_active"):
            sys.exit(0)

        # No productive agent ran this session — nothing to advocate for
        if not os.path.exists(NEEDED_MARKER):
            sys.exit(0)

        # Devil's advocate was already run — all good
        if os.path.exists(DONE_MARKER):
            sys.exit(0)

        # Needed but not done — block
        print(json.dumps({"decision": "block", "reason": BLOCK_REASON}))
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
