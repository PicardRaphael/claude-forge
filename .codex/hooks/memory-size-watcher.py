#!/usr/bin/env python3
"""SessionStart hook: warns when memory/MEMORY.md approaches the 40k char system limit.

Trigger  : SessionStart
Threshold: 38000 chars (advisory, not blocking)
Behavior : Fail-open — any error (missing file, IO, JSON) → exit 0 silently.
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
_REPO_ROOT = os.path.dirname(_CLAUDE_DIR)
_MEMORY_PATH = os.path.join(_REPO_ROOT, "memory", "MEMORY.md")


def check_memory_size(memory_path: str, threshold: int = 38000) -> str | None:
    """Return a warning message if memory_path exceeds threshold chars, else None."""
    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None
    size = len(content)
    if size > threshold:
        size_k = round(size / 1000)
        return (
            f"[memory-size-watcher] MEMORY.md = {size_k}k chars ({size} chars)."
            " Approche seuil systeme 40k."
            " Planifier /clean-memory dans session courte dediee"
            " (rappel : tier-1 visible, tier-2 dans _index_archive.md)."
        )
    return None


if __name__ == "__main__":
    try:
        sys.stdin.read()  # consume stdin; SessionStart payload not needed
    except Exception:
        pass
    try:
        msg = check_memory_size(_MEMORY_PATH)
        if msg:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": msg,
                }
            }
            print(json.dumps(output))
    except Exception:
        pass
    sys.exit(0)
