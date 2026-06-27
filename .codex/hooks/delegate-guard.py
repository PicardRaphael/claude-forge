#!/usr/bin/env python3
"""Block direct edits to protected files — enforce delegation to specialist skills.

Protected targets (ONLY inside claude-forge project) — modification only, not reads:
  CLAUDE.md              → claudemd-creator skill
  agents/*.md            → subagent-creator skill
  skills/<name>/SKILL.md → skill-creator skill   (except external/kepano skills)
  hooks/*.py             → hook-creator skill     (except this guard + test files)

Rationale: a specialist skill applies the perfect-writing checklist automatically.
Direct hand edits produced non-conformant components 3× (2026-04-26). Reads/analysis
are NOT blocked — only Write/Edit/MultiEdit. The vault + rules carry the same method;
only *modification* risks a broken format.

DETECTION (how we know a legit specialist skill is writing):
  Claude Code writes `attributionSkill: <skill-name>` on the assistant event in the
  session transcript when a skill is active. The hook receives agent_type/agent_id = null
  for skills (skills are NOT sub-agents), so we parse the transcript tail for
  attributionSkill instead. Empirically confirmed on CC 2.1.167 (2026-06-06).

  STRICT bypass: attributionSkill must match the REQUIRED specialist for THIS file type
  (claudemd-creator may only unlock CLAUDE.md, skill-creator only SKILL.md, etc.).
  Defense in depth — an active skill cannot unlock a file type it doesn't own.

NEVER bypass via spoofable signals (CLAUDE_AGENT env var injection, external scripts):
  those are circumvention attempts, not legitimate delegation. Removed deliberately.

Exceptions (bypass in order — first match wins):
  1. File outside the claude-forge project directory → always allowed
  2. File is this guard itself or a test_*.py → allowed (avoid self-lock)
  3. transcript attributionSkill == required specialist for this file → bypass
  4. Edit/MultiEdit with all changes < 20 chars → typo pass-through (warning)
  5. Any parse error → fail-open (exit 0)

Doctrine: hook = scope/enforcement only, never agentic workflow (pivot 22 mai).
Debug log (append): <tempdir>/delegate-guard-debug.log
"""
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


# basename CLAUDE.md → specialist skill that owns it
PROTECTED_BASENAMES = {
    "CLAUDE.md": "claudemd-creator",
}

TYPO_THRESHOLD = 20

# All specialist skills (used only to recognize a name as a known specialist if needed)
ALLOWED_SPECIALISTS = {
    "skill-creator",
    "subagent-creator",
    "hook-creator",
    "claudemd-creator",
}

# External/kepano skills — read-only copies, NOT authored via skill-creator → not protected
EXEMPT_SKILL_DIRS = {
    "json-canvas",
    "defuddle",
    "obsidian-cli",
    "obsidian-markdown",
    "obsidian-bases",
}

# Hook files that must never be self-locked
EXEMPT_HOOK_FILES = {
    "delegate-guard.py",
}

# How many trailing transcript lines to scan for attributionSkill
TRANSCRIPT_TAIL = 15

FORGE_PROJECT_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/").lower()

LOG_PATH = Path(tempfile.gettempdir()) / "delegate-guard-debug.log"


def debug_log(msg: str) -> None:
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
    return norm_path.lower().startswith(FORGE_PROJECT_DIR)


def _parts(norm_path: str) -> list[str]:
    return norm_path.split("/")


def is_exempt_skill(norm_path: str) -> bool:
    parts = _parts(norm_path)
    for i, part in enumerate(parts):
        if part == "skills" and i + 1 < len(parts) and parts[i + 1] in EXEMPT_SKILL_DIRS:
            return True
    return False


def is_agent_md(norm_path: str) -> bool:
    """True for .claude/agents/<name>.md (file directly under agents/)."""
    parts = _parts(norm_path)
    return "agents" in parts and norm_path.endswith(".md") and parts[-2:-1] == ["agents"]


def is_skill_md(norm_path: str) -> bool:
    """True for .claude/skills/<name>/SKILL.md (non-exempt)."""
    if basename(norm_path) != "SKILL.md":
        return False
    if "skills" not in _parts(norm_path):
        return False
    return not is_exempt_skill(norm_path)


def is_hook_py(norm_path: str) -> bool:
    """True for .claude/hooks/*.py (excluding the guard itself and test files)."""
    parts = _parts(norm_path)
    name = basename(norm_path)
    if "hooks" not in parts or not name.endswith(".py"):
        return False
    if name in EXEMPT_HOOK_FILES or name.startswith("test_"):
        return False
    return parts[-2:-1] == ["hooks"]


def required_specialist(norm_path: str) -> str | None:
    """Return the specialist skill required to edit this file, or None if unprotected."""
    name = basename(norm_path)
    if name in PROTECTED_BASENAMES:
        return PROTECTED_BASENAMES[name]
    if is_skill_md(norm_path):
        return "skill-creator"
    if is_agent_md(norm_path):
        return "subagent-creator"
    if is_hook_py(norm_path):
        return "hook-creator"
    return None


def active_skill_from_transcript(transcript_path: str) -> str | None:
    """Return the attributionSkill of the most recent assistant event, or None.

    CC writes `attributionSkill: <name>` on assistant events when a skill is active.
    We scan the tail in reverse and return the first attributionSkill found.
    Fail-open → None on any error.
    """
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines[-TRANSCRIPT_TAIL:]):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except Exception:
                continue
            attr = event.get("attributionSkill")
            if attr:
                return attr
    except Exception:
        pass
    return None


def is_typo_change(tool_name: str, tool_input: dict) -> bool:
    if tool_name == "Edit":
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        return len(old) < TYPO_THRESHOLD and len(new) < TYPO_THRESHOLD
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        if not edits:
            return False
        return all(
            len(e.get("old_string", "")) < TYPO_THRESHOLD
            and len(e.get("new_string", "")) < TYPO_THRESHOLD
            for e in edits
        )
    return False


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    try:
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        transcript_path = data.get("transcript_path", "")

        debug_log(
            "stdin="
            + json.dumps(
                {
                    "tool_name": tool_name,
                    "agent_type": data.get("agent_type"),
                    "file_path": file_path,
                    "has_transcript": bool(transcript_path),
                }
            )
        )

        if not file_path:
            sys.exit(0)

        norm_path = normalize(file_path)

        if not is_inside_forge(norm_path):
            sys.exit(0)

        required = required_specialist(norm_path)
        if required is None:
            sys.exit(0)

        # STRICT bypass: the active attributionSkill must be the specialist that owns this file
        active_skill = active_skill_from_transcript(transcript_path) if transcript_path else None
        if active_skill == required:
            debug_log(f"BYPASS attributionSkill={active_skill!r} matches required for {basename(norm_path)}")
            sys.exit(0)

        if tool_name in ("Edit", "MultiEdit") and is_typo_change(tool_name, tool_input):
            print(
                f"WARNING: delegate-guard bypassed for trivial edit (<{TYPO_THRESHOLD} chars) "
                f"on protected file '{basename(norm_path)}'. For real changes, use {required}.",
                file=sys.stderr,
            )
            sys.exit(0)

        print(
            f"BLOCKED: direct {tool_name} of '{basename(norm_path)}' is not allowed.\n"
            f"File: {file_path}\n"
            f"Required specialist skill: {required}\n"
            f"Active attributionSkill detected: {active_skill!r}\n"
            f"Invoke the '{required}' skill to make this change (it applies the perfect-writing checklist).\n"
            f"Reads/analysis are NOT blocked — only modifications. Do NOT attempt to bypass via env vars or external scripts.\n"
            f"Debug log: {LOG_PATH}",
            file=sys.stderr,
        )
        debug_log(
            f"BLOCKED file={file_path} required={required} active_skill={active_skill!r}"
        )
        sys.exit(2)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()