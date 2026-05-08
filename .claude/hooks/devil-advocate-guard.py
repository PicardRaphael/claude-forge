#!/usr/bin/env python3
"""Remind to run devils-advocate when ANY deliverable-producing agent completes.

Triggered on: PostToolUse — Agent

Guard logic:
  1. If completed agent is in EXCLUDED list (research/explore/read-only) → exit 0 (not concerned)
  2. If completed agent is devils-advocate itself → exit 0 (don't guard the guardian)
  3. If .claude/.devil-advocate-done marker exists:
       → consume it (delete — one-shot per deliverable) → exit 0 silently
  4. If marker does NOT exist:
       → print a WARNING reminder to stdout (Claude sees it in context) → exit 0

NOTE: This is a REMINDER, not a blocker (exit 0). The user decides whether
to run devils-advocate. The reminder appears after every unchecked delivery.

Marker path: <project_root>/.claude/.devil-advocate-done (resolved at runtime via __file__)
Written by: devil-advocate-tracker.py
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
MARKER_PATH = os.path.join(_CLAUDE_DIR, ".devil-advocate-done")

WARNING_MSG = (
    "\n[devil-advocate-guard] ATTENTION — Le devil's advocate n'a pas encore ete execute "
    "sur ce livrable.\n"
    "Lancer l'agent `devils-advocate` avant de presenter a Raphael.\n"
    "Pipeline : architect-first → implementation → test/review → devils-advocate → livraison\n"
)

# Agents EXCLUDED from the guard (read-only, research, non-deliverable)
EXCLUDED_AGENTS = [
    "explore",
    "plan",
    "claude-code-guide",
    "vault-maintainer",
    "project-analyzer",
    "project-auditor",
    "statusline-setup",
    "self-updater",
    "devils-advocate",
    "devil-advocate",
]


def normalize(s: str) -> str:
    return s.replace("\\", "/").lower()


def is_excluded_agent(tool_input: dict) -> bool:
    """Check if agent is in the exclusion list (read-only/research agents)."""
    subagent_type = tool_input.get("subagent_type", "")
    if subagent_type and any(m in normalize(subagent_type) for m in EXCLUDED_AGENTS):
        return True
    name = tool_input.get("name", "")
    if name and any(m in normalize(name) for m in EXCLUDED_AGENTS):
        return True
    description = normalize(tool_input.get("description", ""))
    if any(kw in description for kw in ["search", "explore", "audit", "analyze", "read"]):
        return True
    return False


def consume_marker() -> None:
    """Delete the marker (one-shot consumption)."""
    try:
        os.remove(MARKER_PATH)
    except Exception:
        pass  # Already gone or not writable — fine


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

        if is_excluded_agent(tool_input):
            sys.exit(0)

        # Guarded agent completed — check marker
        if os.path.exists(MARKER_PATH):
            # Devil's advocate already ran → consume marker, silent pass
            consume_marker()
        else:
            # No marker → remind
            print(WARNING_MSG)

    except Exception:
        pass  # Fail-open — PostToolUse hooks must never block

    sys.exit(0)


if __name__ == "__main__":
    main()
