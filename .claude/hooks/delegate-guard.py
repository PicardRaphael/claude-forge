#!/usr/bin/env python3
"""Block direct edits to protected files — enforce delegation to specialist agents.

Protected targets (ONLY inside claude-forge project):
  SKILL.md          → must use skill-creator agent
  .claude/agents/*.md → must use agent-creator agent
  CLAUDE.md         → must use claudemd-optimizer agent

Exceptions (bypass in order — first match wins):
  1. File is outside the claude-forge project directory → always allowed
  2. data.get("agent_type") contains a specialist → bypass
  3. data.get("agent_id") equals a specialist name → bypass
  4. CLAUDE_AGENT env var contains a specialist → bypass (legacy fallback)
  5. transcript_path present AND parsing reveals active sub-agent specialist → bypass
  6. Edit tool with both old_string and new_string < 20 chars → typo pass-through (warning)
  7. Any parse error → fail-open (exit 0)

Debug log (append): <tempdir>/delegate-guard-debug.log
"""
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


PROTECTED = {
    "SKILL.md": "skill-creator",
    "CLAUDE.md": "claudemd-optimizer",
}

TYPO_THRESHOLD = 20

ALLOWED_SPECIALISTS = {"skill-creator", "agent-creator", "hook-creator", "claudemd-optimizer"}

# Skills externes (kepano/Obsidian) — copies read-only, pas protégées par delegate-guard
EXEMPT_SKILL_DIRS = {"json-canvas", "defuddle", "obsidian-cli", "obsidian-markdown", "obsidian-bases"}

FORGE_PROJECT_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/").lower()

LOG_PATH = Path(tempfile.gettempdir()) / "delegate-guard-debug.log"


def debug_log(msg: str) -> None:
    """Append timestamped message to debug log. Fail silently."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


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


def detect_subagent_from_transcript(transcript_path: str) -> str | None:
    """Parse last 50 lines of transcript to find innermost active sub-agent.

    Walk lines in reverse order. First event found determines state:
      - agent_end (or type ending the agent context) → not inside a sub-agent → None
      - agent_start / subagent_type present → inside sub-agent → return its type

    Returns the subagent_type string if we are currently inside a specialist sub-agent,
    None otherwise (including on any error → fail-open).
    """
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines[-50:]):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except Exception:
                continue
            event_type = event.get("type", "")
            # If we see an agent completion marker first → no active sub-agent
            if event_type in ("agent_end", "subagent_end", "agent_complete"):
                return None
            # If we see an agent start or subagent_type field → active sub-agent
            if event_type in ("agent_start", "subagent_start") or "subagent_type" in event:
                return event.get("subagent_type") or event.get("agent_type") or ""
    except Exception:
        pass
    return None


def agent_bypass_active(data: dict) -> tuple[bool, str]:
    """Return (bypass, source) where source describes which check triggered the bypass."""
    # Source 1: agent_type field (primary Anthropic field for sub-agent identity)
    agent_type = data.get("agent_type", "")
    if agent_type in ALLOWED_SPECIALISTS:
        return True, f"agent_type={agent_type!r}"

    # Source 2: agent_id field (may contain specialist name in some CC versions)
    agent_id = data.get("agent_id", "")
    if agent_id in ALLOWED_SPECIALISTS:
        return True, f"agent_id={agent_id!r}"
    # Source 3: CLAUDE_AGENT env var (legacy fallback — always dead code per vault, kept for safety)
    claude_agent = os.environ.get("CLAUDE_AGENT", "")
    if claude_agent in ALLOWED_SPECIALISTS:
        return True, f"CLAUDE_AGENT={claude_agent!r}"

    # Source 4: transcript parsing (only if transcript_path is present)
    transcript_path = data.get("transcript_path", "")
    if transcript_path:
        detected = detect_subagent_from_transcript(transcript_path)
        if detected and detected in ALLOWED_SPECIALISTS:
            return True, f"transcript_path detected subagent_type={detected!r}"

    return False, ""


def is_typo_edit(tool_input: dict) -> bool:
    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    return len(old) < TYPO_THRESHOLD and len(new) < TYPO_THRESHOLD


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    try:
        # Always log stdin for empirical observation of what Anthropic sends
        debug_log(
            f"stdin={json.dumps({'tool_name': data.get('tool_name'), 'agent_type': data.get('agent_type'), 'agent_id': data.get('agent_id'), 'transcript_path': data.get('transcript_path'), 'file_path': data.get('tool_input', {}).get('file_path')})}"
        )

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

        bypassed, bypass_source = agent_bypass_active(data)
        if bypassed:
            debug_log(f"BYPASS via {bypass_source} for {basename(norm_path)}")
            sys.exit(0)

        if tool_name == "Edit" and is_typo_edit(tool_input):
            print(
                f"WARNING: delegate-guard bypassed for short edit (<{TYPO_THRESHOLD} chars) "
                f"on protected file '{basename(norm_path)}'. "
                f"For real changes, use {agent}.",
                file=sys.stderr,
            )
            sys.exit(0)

        agent_type_recv = data.get("agent_type", "<absent>")
        agent_id_recv = data.get("agent_id", "<absent>")
        print(
            f"BLOCKED: Direct edit of '{basename(norm_path)}' is not allowed.\n"
            f"File: {file_path}\n"
            f"Required agent: {agent}\n"
            f"Received agent_type={agent_type_recv!r}, agent_id={agent_id_recv!r}\n"
            f"Invoke the '{agent}' agent to make this change.\n"
            f"Debug log: {LOG_PATH}",
            file=sys.stderr,
        )
        debug_log(f"BLOCKED file={file_path} agent_type={agent_type_recv!r} agent_id={agent_id_recv!r}")
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
