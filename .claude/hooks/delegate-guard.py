#!/usr/bin/env python3
"""Block direct edits to protected files — enforce delegation to specialist agents.

Protected targets (ONLY inside claude-forge project):
  SKILL.md          → must use skill-creator agent
  .claude/agents/*.md → must use agent-creator agent
  CLAUDE.md         → must use claudemd-optimizer agent

Exceptions:
  - File is outside the claude-forge project directory → always allowed
  - CLAUDE_AGENT env var contains the expected specialist → bypass
  - Edit tool with both old_string and new_string < 20 chars → typo pass-through (with warning)
  - Any parse error → fail-open (exit 0)
"""
import json
import os
import sys
from pathlib import Path


PROTECTED = {
    "SKILL.md": "skill-creator",
    "CLAUDE.md": "claudemd-optimizer",
}

TYPO_THRESHOLD = 20

# Skills externes (kepano/Obsidian) — copies read-only, pas protégées par delegate-guard
EXEMPT_SKILL_DIRS = {"json-canvas", "defuddle", "obsidian-cli", "obsidian-markdown", "obsidian-bases"}

FORGE_PROJECT_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/").lower()


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def basename(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[-1]


def is_inside_forge(norm_path: str) -> bool:
    """Check if the file is inside the claude-forge project directory."""
    return norm_path.lower().startswith(FORGE_PROJECT_DIR)


def is_agent_md(norm_path: str) -> bool:
    parts = norm_path.split("/")
    if len(parts) < 3:
        return False
    return (
        parts[-1].endswith(".md")
        and parts[-2] == "agents"
        and parts[-3] == ".claude"
    )


def is_exempt_skill(norm_path: str) -> bool:
    """Check if the file is in an exempt skill directory (external/kepano skills)."""
    parts = norm_path.split("/")
    for i, part in enumerate(parts):
        if part == "skills" and i + 1 < len(parts) and parts[i + 1] in EXEMPT_SKILL_DIRS:
            return True
    return False


def required_agent(norm_path: str) -> str | None:
    name = basename(norm_path)
    if is_exempt_skill(norm_path):
        return None
    if name in PROTECTED:
        return PROTECTED[name]
    if is_agent_md(norm_path):
        return "agent-creator"
    return None


def agent_bypass_active(expected_agent: str) -> bool:
    claude_agent = os.environ.get("CLAUDE_AGENT", "")
    allowed = {"skill-creator", "agent-creator", "hook-creator", "claudemd-optimizer"}
    return claude_agent in allowed


def is_typo_edit(tool_input: dict) -> bool:
    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    return len(old) < TYPO_THRESHOLD and len(new) < TYPO_THRESHOLD


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if not file_path:
            sys.exit(0)

        norm_path = normalize(file_path)

        if not is_inside_forge(norm_path):
            sys.exit(0)

        agent = required_agent(norm_path)

        if agent is None:
            sys.exit(0)

        if agent_bypass_active(agent):
            sys.exit(0)

        if tool_name == "Edit" and is_typo_edit(tool_input):
            print(
                f"WARNING: delegate-guard bypassed for short edit (<{TYPO_THRESHOLD} chars) "
                f"on protected file '{basename(norm_path)}'. "
                f"For real changes, use {agent}.",
                file=sys.stderr,
            )
            sys.exit(0)

        print(
            f"BLOCKED: Direct edit of '{basename(norm_path)}' is not allowed.\n"
            f"File: {file_path}\n"
            f"Required agent: {agent}\n"
            f"Invoke the '{agent}' agent to make this change.\n"
            f"Bypass: set CLAUDE_AGENT={agent} in your environment.",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
