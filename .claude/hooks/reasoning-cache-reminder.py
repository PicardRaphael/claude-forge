#!/usr/bin/env python3
"""Remind to use /reasoning-cache after complex multi-step agent tasks.

Triggered on: PostToolUse — Agent

When an agent completes whose description (or input) contains words indicating
complex investigation (debug, investigate, fix, resolve, architecture), print
a one-time-per-session reminder about /reasoning-cache.

One-shot: uses marker .claude/.reasoning-reminder-shown. Once the marker exists,
no further reminders are emitted for the rest of the session.

Always exits 0 — non-blocking reminder.
"""
import json
import os
import re
import sys

MARKER_PATH = "C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.reasoning-reminder-shown"

REMINDER_MSG = (
    "\n[reasoning-cache-reminder] Raisonnement complexe detecte. "
    "Penser a /reasoning-cache pour sauvegarder le chemin de resolution.\n"
)

# Word-boundary regex — avoids matching "prefix" for "fix", "architecture" for "arch", etc.
COMPLEX_PATTERN = re.compile(
    r"\b(debug|investigate|fix|resolve|architecture|diagnose|troubleshoot|analyse|analyze)\b",
    re.IGNORECASE,
)


def normalize(s: str) -> str:
    return s.replace("\\", "/")


def looks_complex(tool_input: dict) -> bool:
    """Check if the agent task description indicates complex multi-step reasoning."""
    # Try explicit description fields first
    for field in ("description", "prompt", "task", "instructions"):
        value = tool_input.get(field, "")
        if value and COMPLEX_PATTERN.search(str(value)):
            return True
    # Fallback: scan full serialized input
    haystack = json.dumps(tool_input)
    return bool(COMPLEX_PATTERN.search(haystack))


def write_marker() -> None:
    """Write marker to prevent repeat reminders this session."""
    try:
        marker_dir = os.path.dirname(MARKER_PATH)
        os.makedirs(marker_dir, exist_ok=True)
        with open(MARKER_PATH, "w", encoding="utf-8") as f:
            f.write("shown")
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

        if tool_name != "Agent":
            sys.exit(0)

        # Already reminded this session
        if os.path.exists(MARKER_PATH):
            sys.exit(0)

        if looks_complex(tool_input):
            print(REMINDER_MSG)
            write_marker()

    except Exception:
        pass  # Fail-open

    sys.exit(0)


if __name__ == "__main__":
    main()
