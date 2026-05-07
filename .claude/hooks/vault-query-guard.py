#!/usr/bin/env python3
"""Block Write to vault/output/.claude/skills/.claude/agents unless forge-brain was queried.

Triggered on: PreToolUse — Write

Protected target paths (any of these substrings in the normalized file_path):
  vault/          — Obsidian vault notes
  output/         — generated output files
  .claude/skills/ — forge skills
  .claude/agents/ — forge agents

Guard logic:
  1. If file_path is NOT in a protected path    → exit 0 (don't interfere)
  2. If marker file exists and is < 60 min old  → exit 0 (vault queried recently)
  3. Otherwise                                  → exit 2 (BLOCK)

There is NO specialist bypass. All agents (skill-creator, agent-creator, etc.) must
query vault/ or memory/ before writing to protected paths. If blocked, query the vault
then retry.

The marker file is written by vault-query-tracker.py when a Read/Grep/Glob/Skill
targets vault/ or memory/ paths.

Marker path: C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.session-vault-queried

Fail-open policy: ONLY on stdin parse errors. A missing/expired marker is NOT a
parse error — it means no vault query has occurred and the write must be blocked.
"""
import json
import os
import sys
from datetime import datetime, timedelta

MARKER_PATH = "C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.session-vault-queried"

PROTECTED_PATH_FRAGMENTS = [
    "vault/",
    "output/",
    ".claude/skills/",
    ".claude/agents/",
]

MARKER_MAX_AGE_MINUTES = 60


def normalize(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace("\\", "/")


def is_protected_path(norm_path: str) -> bool:
    return any(fragment in norm_path for fragment in PROTECTED_PATH_FRAGMENTS)


def marker_is_fresh() -> bool:
    """Return True if the marker file exists and was written less than 60 minutes ago.

    If the file is missing, unreadable, or timestamp is malformed → return False (not fresh).
    We intentionally do NOT swallow errors broadly here: missing marker = not queried = block.
    """
    if not os.path.isfile(MARKER_PATH):
        return False

    try:
        with open(MARKER_PATH, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        ts = datetime.fromisoformat(raw)
        age = datetime.now() - ts
        return age < timedelta(minutes=MARKER_MAX_AGE_MINUTES)
    except Exception:
        # Malformed/corrupt timestamp → treat as expired → block
        return False


def block(file_path: str) -> None:
    filename = normalize(file_path).rsplit("/", 1)[-1]
    print(
        f"BLOCKED: Write to '{filename}' requires querying forge-brain or memory first.\n"
        f"File: {file_path}\n"
        f"You MUST query the vault or memory BEFORE writing to protected paths:\n"
        f"  1. Read vault/ files (Knowledge/erreurs/, 04-Techniques/, 07-Prompts/)\n"
        f"  2. Or search vault/ with Grep/Glob\n"
        f"  3. Or invoke the /forge-brain skill\n"
        f"  4. Or read memory/ files\n"
        f"This applies to ALL agents, including specialists. Query first, then retry.",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        # Fail-open on stdin parse errors only
        sys.exit(0)

    try:
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if not file_path:
            sys.exit(0)

        norm_path = normalize(file_path)

        # Step 1: is this a protected path?
        if not is_protected_path(norm_path):
            sys.exit(0)

        # Step 2: vault was queried recently
        if marker_is_fresh():
            sys.exit(0)

        # Step 3: block
        block(file_path)

    except SystemExit:
        raise  # Let exit(2) propagate
    except Exception:
        # Unexpected error → fail-open (don't break Claude for a hook bug)
        sys.exit(0)


if __name__ == "__main__":
    main()
