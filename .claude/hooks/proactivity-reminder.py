#!/usr/bin/env python3
"""Proactivity reminder — fires ONCE per session on Stop.

Reminds Claude (via JSON block) to make a Jarvis proposal before ending,
if the session was substantive (>= 5 turns).

Blocking is intentional: plain stdout on Stop is terminal-only and never
seen by Claude. The only way to surface this to Claude is {"decision":
"block", "reason": "..."}. Low friction — one short acknowledgement clears it.

Marker in %TEMP% prevents infinite loop (decision:block re-triggers Stop).
Marker is cleaned by session-reminder.py at SessionStart.
"""
import json
import os
import sys
import tempfile

MARKER = os.path.join(tempfile.gettempdir(), "claude-forge-proactivity-reminded")

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
TURN_COUNTER_FILE = os.path.join(_CLAUDE_DIR, ".session-turn-counter")

MIN_TURNS = 5

REMINDER = (
    "Avant de terminer — as-tu fait une proposition Jarvis ?\n"
    "Pattern : \"Proposition Jarvis : [quoi] — [pourquoi]. Je lance ?\"\n"
    "Si rien à proposer cette session, réponds 'rien à proposer' pour continuer."
)


def get_turn_count() -> int:
    try:
        with open(TURN_COUNTER_FILE, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return int(data.get("count", 0))
    except Exception:
        return 0


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        # Guard against infinite loop in stop-hook continuation
        if data.get("stop_hook_active"):
            sys.exit(0)

        # Already reminded this session — don't repeat
        if os.path.exists(MARKER):
            sys.exit(0)

        # Short session — no Jarvis proposal expected
        if get_turn_count() < MIN_TURNS:
            sys.exit(0)

        # Write marker before blocking (prevents loop if block re-triggers Stop)
        try:
            with open(MARKER, "w") as f:
                f.write("1")
        except Exception:
            pass

        print(json.dumps({"decision": "block", "reason": REMINDER}))
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
