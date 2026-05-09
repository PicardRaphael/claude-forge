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

# Agents that PRODUCE major deliverables (new skill, agent, hook, architecture)
DELIVERABLE_AGENTS = [
    "skill-creator",
    "agent-creator",
    "hook-creator",
    "claudemd-optimizer",
]

# Keywords in description that signal a major deliverable (CREATION, not modification)
DELIVERABLE_KEYWORDS = [
    "create", "crée", "nouveau", "new",
    "architecture", "archi",
    "proposal", "proposition",
    "innovation",
]

# Keywords that signal a NON-deliverable (modification, fix, migration)
NON_DELIVERABLE_KEYWORDS = [
    "fix", "update", "migrate", "migration", "modify", "modifie",
    "remove", "supprime", "clean", "refactor", "rename",
    "test", "check", "verify", "audit", "search", "read",
    "explore", "analyze", "quick",
]

# Always excluded regardless
ALWAYS_EXCLUDED = [
    "devils-advocate",
    "devil-advocate",
]


def normalize(s: str) -> str:
    return s.replace("\\", "/").lower()


def is_deliverable_agent(tool_input: dict) -> bool:
    """Check if agent produces a major deliverable that needs devil's advocate review."""
    subagent_type = normalize(tool_input.get("subagent_type", ""))
    name = normalize(tool_input.get("name", ""))
    description = normalize(tool_input.get("description", ""))

    if any(m in subagent_type for m in ALWAYS_EXCLUDED):
        return False
    if any(m in name for m in ALWAYS_EXCLUDED):
        return False

    # Non-deliverable keywords override everything
    if any(kw in description for kw in NON_DELIVERABLE_KEYWORDS):
        return False

    if any(m in subagent_type for m in DELIVERABLE_AGENTS):
        return True
    if any(m in name for m in DELIVERABLE_AGENTS):
        return True
    if any(kw in description for kw in DELIVERABLE_KEYWORDS):
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

        if not is_deliverable_agent(tool_input):
            sys.exit(0)

        # Deliverable agent completed — track that review is needed
        deliverable_path = os.path.join(_CLAUDE_DIR, ".devil-advocate-needed")
        if not os.path.exists(deliverable_path):
            with open(deliverable_path, "w") as f:
                f.write("1")

        if os.path.exists(MARKER_PATH):
            pass
        else:
            print(WARNING_MSG)

    except Exception:
        pass  # Fail-open — PostToolUse hooks must never block

    sys.exit(0)


if __name__ == "__main__":
    main()
