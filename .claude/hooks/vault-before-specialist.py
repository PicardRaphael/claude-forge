#!/usr/bin/env python3
"""Block specialist agent launch if forge-brain vault was not queried this session.

Triggered on: PreToolUse — Agent

Specialist agents that CREATE or MODIFY .claude/ components (skill-creator,
agent-creator, hook-creator, claudemd-optimizer) MUST have vault context
before they run. The vault-query-tracker.py writes a marker when vault is
queried (Read/Grep/Glob on vault paths, Skill on forge-brain/neo-brain,
or any mcp__forge-brain__* call).

Marker = existence-only (no TTL). Reset by session-reset-vault-marker.py
on SessionStart.

is_specialist() reads ONLY tool_input.subagent_type — never matches against
prompt/description (which produces false positives).
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
MARKER_PATH = os.path.join(_CLAUDE_DIR, ".session-vault-queried")

# Only agents that CREATE/MODIFY .claude/ components. Scope tightened
# 2026-05-21 after advisor+DA review (was 10, now 4).
SPECIALIST_AGENTS = {
    "skill-creator",
    "agent-creator",
    "hook-creator",
    "claudemd-optimizer",
}


def marker_exists() -> bool:
    return os.path.isfile(MARKER_PATH)


def is_specialist(data: dict) -> bool:
    # Read ONLY the structured subagent_type field. Matching against prompt
    # or description produces false positives (mentioning "skill-creator" in
    # a general-purpose dispatch would wrongly trigger this hook).
    tool_input = data.get("tool_input", {})
    agent_type = tool_input.get("subagent_type", "").lower()
    return agent_type in SPECIALIST_AGENTS


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    if data.get("tool_name", "") != "Agent":
        sys.exit(0)

    if not is_specialist(data):
        sys.exit(0)

    if marker_exists():
        sys.exit(0)

    agent_type = data.get("tool_input", {}).get("subagent_type", "unknown")
    print(
        f"BLOCKED: Agent '{agent_type}' requires querying forge-brain vault first.\n"
        f"Before launching specialist agents, you MUST call (in main session, not via sub-agent):\n"
        f"  mcp__forge-brain__search_brain(query=\"<sujet>\")\n"
        f"Then retry. This is the check-before-create rule enforced as a hook.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
