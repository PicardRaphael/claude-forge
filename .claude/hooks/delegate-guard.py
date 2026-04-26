#!/usr/bin/env python3
"""Block direct edits to protected files — enforce delegation to specialist agents.

Protected targets:
  SKILL.md          → must use skill-creator agent
  .claude/agents/*.md → must use agent-creator agent
  CLAUDE.md         → must use claudemd-optimizer agent

Exceptions:
  - CLAUDE_AGENT env var contains the expected specialist → bypass
  - Edit tool with both old_string and new_string < 20 chars → typo pass-through (with warning)
  - Any parse error → fail-open (exit 0)

Note: CLAUDE_AGENT inheritance to subagents is partially fixed in CC v2.1.101 (worktrees, MCP),
but `permissions.allow` may not propagate. If specialist agents fail to bypass, that is a CC
limitation not a hook bug.
"""
import json
import os
import sys


PROTECTED = {
    "SKILL.md": "skill-creator",
    "CLAUDE.md": "claudemd-optimizer",
}

TYPO_THRESHOLD = 20

FORGE_PATH = "claude-forge/"


def normalize(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace("\\", "/")


def basename(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[-1]


def is_agent_md(norm_path: str) -> bool:
    """Check that path matches .claude/agents/<filename>.md (single level, not recursive)."""
    parts = norm_path.split("/")
    if len(parts) < 3:
        return False
    # The segment before the file must be 'agents', and before that '.claude'
    return (
        parts[-1].endswith(".md")
        and parts[-2] == "agents"
        and parts[-3] == ".claude"
    )


def required_agent(norm_path: str) -> str | None:
    """Return the name of the agent required, or None if not protected."""
    name = basename(norm_path)

    # Exact filename match (not endswith, to avoid vault false positives)
    if name in PROTECTED:
        return PROTECTED[name]

    if is_agent_md(norm_path):
        return "agent-creator"

    return None


def agent_bypass_active(expected_agent: str) -> bool:
    """Check if CLAUDE_AGENT env var signals we are inside a specialist agent."""
    claude_agent = os.environ.get("CLAUDE_AGENT", "")
    allowed = {"skill-creator", "agent-creator", "hook-creator", "claudemd-optimizer"}
    # Check both the expected agent and any specialist agent (belt and suspenders)
    return claude_agent in allowed


def is_typo_edit(tool_input: dict) -> bool:
    """Return True if old_string and new_string are both very short (likely a typo fix)."""
    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    return len(old) < TYPO_THRESHOLD and len(new) < TYPO_THRESHOLD


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Fail-open: a crashing hook must not block Claude
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if not file_path:
            sys.exit(0)

        norm_path = normalize(file_path)

        # Only protect files inside claude-forge — external projects manage themselves
        if FORGE_PATH not in norm_path:
            sys.exit(0)

        agent = required_agent(norm_path)

        if agent is None:
            # Not a protected file
            sys.exit(0)

        # Check if a specialist agent is already handling this
        if agent_bypass_active(agent):
            sys.exit(0)

        # Typo exception: only for Edit, not Write
        if tool_name == "Edit" and is_typo_edit(tool_input):
            print(
                f"WARNING: delegate-guard bypassed for short edit (<{TYPO_THRESHOLD} chars) "
                f"on protected file '{basename(norm_path)}'. "
                f"For real changes, use {agent}.",
                file=sys.stderr,
            )
            sys.exit(0)

        # Block
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
        # Fail-open on any unexpected error
        sys.exit(0)


if __name__ == "__main__":
    main()
