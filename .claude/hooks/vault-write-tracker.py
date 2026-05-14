#!/usr/bin/env python3
"""Track Write/Edit operations targeting vault/claude-forge/ and flag for devil's advocate.

Triggered on: PostToolUse — Write|Edit|MultiEdit

Logic:
  1. Extract file_path from tool_input (normalized to forward slashes)
  2. If path does NOT contain vault/claude-forge/ → exit 0 (not a vault write)
  3. Read counter from .vault-write-count; reset to 0 if file missing or mtime > 2h old
  4. Increment counter; write back
  5. If counter >= 3 AND .devil-advocate-needed not present → create the marker
  6. Print info to stdout (Claude sees it in context):
       - < 3: "[vault-write-tracker] N vault writes this session."
       - >= 3: "[vault-write-tracker] N vault writes this session. Devil's advocate will be required before Stop."
  7. Always exit 0 (fail-open)

Marker path: <project_root>/.claude/.devil-advocate-needed
Counter path: <project_root>/.claude/.vault-write-count
Both resolved at runtime via __file__ for portability.

NOTE: The .vault-write-count file is also cleaned up by session-reminder.py at SessionStart.
The 2-hour mtime check is a secondary safety net in case the SessionStart cleanup was missed.
"""
import json
import os
import sys
import time

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)

COUNTER_PATH = os.path.join(_CLAUDE_DIR, ".vault-write-count")
NEEDED_MARKER = os.path.join(_CLAUDE_DIR, ".devil-advocate-needed")

VAULT_FRAGMENT = "vault/claude-forge/"
THRESHOLD = 3
SESSION_MAX_AGE_SECONDS = 2 * 60 * 60  # 2 hours


def normalize(path: str) -> str:
    return path.replace("\\", "/").lower()


def read_counter() -> int:
    """Read counter from file; return 0 if file missing, too old, or unreadable."""
    if not os.path.isfile(COUNTER_PATH):
        return 0
    try:
        age = time.time() - os.path.getmtime(COUNTER_PATH)
        if age > SESSION_MAX_AGE_SECONDS:
            return 0
        with open(COUNTER_PATH, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return 0


def write_counter(count: int) -> None:
    """Write counter to file. Failure is silent (fail-open)."""
    try:
        with open(COUNTER_PATH, "w", encoding="utf-8") as f:
            f.write(str(count))
    except Exception:
        pass


def ensure_needed_marker() -> None:
    """Create .devil-advocate-needed marker if not already present."""
    if not os.path.exists(NEEDED_MARKER):
        try:
            with open(NEEDED_MARKER, "w") as f:
                f.write("1")
        except Exception:
            pass


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        tool_input = data.get("tool_input", {})

        # MultiEdit uses 'edits' list; Write and Edit use 'file_path'
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
        norm_path = normalize(file_path)

        if not file_path or VAULT_FRAGMENT not in norm_path:
            sys.exit(0)

        # Read mtime BEFORE parsing to ensure consistent ordering
        current_count = read_counter()
        new_count = current_count + 1
        write_counter(new_count)

        if new_count >= THRESHOLD:
            ensure_needed_marker()
            print(
                f"[vault-write-tracker] {new_count} vault writes this session. "
                "Devil's advocate will be required before Stop."
            )
        else:
            print(f"[vault-write-tracker] {new_count} vault write(s) this session.")

    except Exception:
        pass  # Fail-open — PostToolUse hooks must never block

    sys.exit(0)


if __name__ == "__main__":
    main()
