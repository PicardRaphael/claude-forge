#!/usr/bin/env python3
"""Block specialist agent launch if forge-brain vault was not queried first.

Triggered on: PreToolUse — Agent

Specialist agents (skill-creator, agent-creator, claudemd-optimizer, hook-creator,
devils-advocate) MUST have vault context before they create/modify components.
The vault-query-tracker.py writes a marker when vault is queried.
This hook checks the marker exists before allowing specialist launch.

Non-specialist agents (Explore, general-purpose, Plan, etc.) are NOT blocked.
"""
import json
import os
import sys
from datetime import datetime, timedelta

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
MARKER_PATH = os.path.join(_CLAUDE_DIR, ".session-vault-queried")

SPECIALIST_AGENTS = [
    "skill-creator",
    "agent-creator",
    "claudemd-optimizer",
    "hook-creator",
    "devils-advocate",
    "project-analyzer",
    "project-auditor",
    "vault-maintainer",
    "python-dev",
    "self-updater",
]

MARKER_MAX_AGE_MINUTES = 60


def marker_is_fresh():
    if not os.path.isfile(MARKER_PATH):
        return False
    try:
        with open(MARKER_PATH, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        ts = datetime.fromisoformat(raw)
        age = datetime.now() - ts
        return age < timedelta(minutes=MARKER_MAX_AGE_MINUTES)
    except Exception:
        return False


def is_specialist(data):
    tool_input = data.get("tool_input", {})
    agent_type = tool_input.get("subagent_type", "").lower()
    if agent_type in SPECIALIST_AGENTS:
        return True
    prompt = tool_input.get("prompt", "").lower()
    description = tool_input.get("description", "").lower()
    for name in SPECIALIST_AGENTS:
        if name in prompt or name in description:
            return True
    return False


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Agent":
        sys.exit(0)

    if not is_specialist(data):
        sys.exit(0)

    if marker_is_fresh():
        sys.exit(0)

    agent_type = data.get("tool_input", {}).get("subagent_type", "unknown")
    print(
        f"BLOCKED: Agent '{agent_type}' requires querying forge-brain vault first.\n"
        f"Before launching specialist agents, you MUST:\n"
        f"  1. mcp__forge-brain__search_brain(query=\"<sujet>\") — best practices\n"
        f"  2. mcp__forge-brain__search_brain(query=\"erreur <sujet>\") — past mistakes\n"
        f"  3. Then retry launching the agent.\n"
        f"This is the check-before-create rule enforced as a hook.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
