#!/usr/bin/env python3
"""Track when the forge-brain vault or project memory has been queried this session.

Triggered on: PostToolUse — Read | Grep | Glob | Skill

For Read/Grep/Glob: checks if the path/pattern targets vault/, memory/, Knowledge/,
forge-brain, 04-Techniques/, or 07-Prompts/ (and a few other forge-brain paths).
For Skill: serializes the full tool_input and checks for forge-brain / neo-brain keywords.

When a match is found, writes an ISO timestamp to the marker file
  C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.session-vault-queried

This marker is consumed by vault-query-guard.py to allow protected writes.
Always exits 0 — PostToolUse hooks must never block.
"""
import json
import os
import sys
from datetime import datetime

MARKER_PATH = "C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/.session-vault-queried"

# Substrings that indicate a vault / memory query
VAULT_MARKERS = [
    "vault/",
    "memory/",
    "Knowledge/",
    "forge-brain",
    "04-Techniques/",
    "07-Prompts/",
    "Knowledge/erreurs/",
    "agent-memory/",
]

# For Skill tool: skill names that represent a vault query
SKILL_MARKERS = [
    "forge-brain",
    "neo-brain",
]


def normalize(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace("\\", "/")


def build_haystack_for_file_tool(tool_input: dict) -> str:
    """Build a searchable string from all path-like fields used by Read/Grep/Glob."""
    parts = [
        tool_input.get("file_path", ""),
        tool_input.get("path", ""),
        tool_input.get("pattern", ""),
    ]
    return normalize(" ".join(filter(None, parts)))


def is_vault_query_file(tool_input: dict) -> bool:
    haystack = build_haystack_for_file_tool(tool_input)
    return any(marker in haystack for marker in VAULT_MARKERS)


def is_vault_query_skill(tool_input: dict) -> bool:
    # Serialize the whole input dict — field name varies across CC versions
    haystack = normalize(json.dumps(tool_input))
    return any(marker in haystack for marker in SKILL_MARKERS)


def write_marker() -> None:
    """Write current ISO timestamp to the marker file."""
    try:
        marker_dir = os.path.dirname(MARKER_PATH)
        os.makedirs(marker_dir, exist_ok=True)
        with open(MARKER_PATH, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
    except Exception:
        # Fail-open: if we cannot write the marker we just skip silently
        pass


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        matched = False

        if tool_name in ("Read", "Grep", "Glob"):
            matched = is_vault_query_file(tool_input)
        elif tool_name == "Skill":
            matched = is_vault_query_skill(tool_input)

        if matched:
            write_marker()

    except Exception:
        pass  # Fail-open — PostToolUse hooks must never surface errors as blocks

    sys.exit(0)


if __name__ == "__main__":
    main()
