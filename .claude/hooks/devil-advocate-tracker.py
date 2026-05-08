#!/usr/bin/env python3
"""Track when the devils-advocate agent completes.

Triggered on: PostToolUse — Agent

When the completed agent is 'devils-advocate' (by subagent_type or serialized input),
write the marker file .claude/.devil-advocate-done (existence only, no TTL).

This marker is consumed by devil-advocate-guard.py to confirm the devil's advocate
step ran before a skill-creator or agent-creator delivers its output.

Always exits 0 — PostToolUse hooks must never block.
"""
import json
import os
import sys
from datetime import datetime, timezone

MARKER_PATH = "C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.devil-advocate-done"

# Substrings that identify the devils-advocate agent in tool_input
DEVIL_MARKERS = [
    "devils-advocate",
    "devil-advocate",
    "devils_advocate",
    "devil_advocate",
]


def normalize(s: str) -> str:
    return s.replace("\\", "/").lower()


def is_devils_advocate(tool_input: dict) -> bool:
    """Check subagent_type first (canonical field), then full JSON scan (fallback for CC version variance)."""
    subagent_type = tool_input.get("subagent_type", "")
    if subagent_type and any(m in normalize(subagent_type) for m in DEVIL_MARKERS):
        return True
    # Fallback: scan the entire serialized input
    haystack = normalize(json.dumps(tool_input))
    return any(m in haystack for m in DEVIL_MARKERS)


def write_marker() -> None:
    """Write ISO timestamp to marker (existence is what matters, timestamp aids debugging)."""
    try:
        marker_dir = os.path.dirname(MARKER_PATH)
        os.makedirs(marker_dir, exist_ok=True)
        with open(MARKER_PATH, "w", encoding="utf-8") as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception:
        pass  # Fail-open


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name == "Agent" and is_devils_advocate(tool_input):
            write_marker()

    except Exception:
        pass  # Fail-open — PostToolUse hooks must never surface errors as blocks

    sys.exit(0)


if __name__ == "__main__":
    main()
