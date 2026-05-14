#!/usr/bin/env python3
"""Skill Activation Hook — UserPromptSubmit.

Checks user prompt against .skill-triggers.json. If a match is found,
injects an additionalContext recommendation so Claude knows a relevant
skill/command is available.

Design decisions:
- Word-boundary regex (avoids "done" matching "abandoned")
- Extended trigger map: {"skill-name": {"type", "triggers", "description"}}
- type "skill" → Skill(name) | type "command" → /name
- Multi-match: one combined additionalContext, all matched skills tracked
- Bypass prefixes: *, /, #, ! (system prompts, slash commands, directives)
- Fail-open: any exception → exit 0 silently
- Session tracker: .skill-recommendations-session (reset by session-reminder.py)
"""
import json
import os
import re
import sys

# --- Paths (all via __file__, never hardcoded) ---
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)

TRIGGERS_PATH = os.path.join(_CLAUDE_DIR, ".skill-triggers.json")
SESSION_TRACKER = os.path.join(_CLAUDE_DIR, ".skill-recommendations-session")

# Prefixes that mean "skip entirely" — slash commands, directives, system markers
BYPASS_PREFIXES = ("*", "/", "#", "!")


def load_triggers() -> dict:
    """Load trigger map from JSON. Returns {} if missing or malformed."""
    try:
        with open(TRIGGERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_session_tracker() -> set:
    """Return set of skills already recommended this session."""
    try:
        if os.path.exists(SESSION_TRACKER):
            with open(SESSION_TRACKER, "r", encoding="utf-8") as f:
                return set(json.load(f))
    except Exception:
        pass
    return set()


def save_session_tracker(recommended: set) -> None:
    """Persist updated recommended set."""
    try:
        with open(SESSION_TRACKER, "w", encoding="utf-8") as f:
            json.dump(list(recommended), f)
    except Exception:
        pass


def find_matches(prompt: str, triggers: dict, already_recommended: set) -> list[dict]:
    """Return list of matched entries not yet recommended this session."""
    matches = []
    for skill_name, entry in triggers.items():
        if skill_name in already_recommended:
            continue
        if not isinstance(entry, dict):
            continue
        skill_triggers = entry.get("triggers", [])
        for trigger in skill_triggers:
            pattern = rf"\b{re.escape(trigger)}\b"
            if re.search(pattern, prompt, re.IGNORECASE):
                matches.append({"name": skill_name, **entry})
                break  # One trigger per skill is enough
    return matches


def format_recommendation(match: dict) -> str:
    """Format one recommendation line based on skill type."""
    name = match["name"]
    description = match.get("description", "")
    skill_type = match.get("type", "skill")

    if skill_type == "command":
        invoke = f"/{name}"
    else:
        invoke = f"Skill({name})"

    if description:
        return f"- {invoke} — {description}"
    return f"- {invoke}"


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    try:
        prompt = data.get("prompt", "")
        if not isinstance(prompt, str):
            sys.exit(0)

        # Skip bypass prefixes (check after stripping leading whitespace)
        prompt_stripped = prompt.lstrip()
        if any(prompt_stripped.startswith(p) for p in BYPASS_PREFIXES):
            sys.exit(0)

        triggers = load_triggers()
        if not triggers:
            sys.exit(0)

        already_recommended = load_session_tracker()
        matches = find_matches(prompt_stripped, triggers, already_recommended)

        if not matches:
            sys.exit(0)

        # Build combined additionalContext
        lines = ["[skill-activation] Compétences disponibles pour ce contexte :"]
        for match in matches:
            lines.append(format_recommendation(match))

        context_message = "\n".join(lines)

        # Persist all matched skills as recommended this session
        newly_recommended = already_recommended | {m["name"] for m in matches}
        save_session_tracker(newly_recommended)

        # Emit additionalContext (same shape as session-health.py)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context_message,
            }
        }
        print(json.dumps(output))

    except Exception:
        pass  # Fail-open — never block on UserPromptSubmit

    sys.exit(0)


if __name__ == "__main__":
    main()
