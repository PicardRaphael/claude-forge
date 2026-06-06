#!/usr/bin/env python3
"""Skill Activation Hook — UserPromptSubmit.

Checks user prompt against .skill-triggers.json. If a match is found,
injects an additionalContext recommendation so Claude knows a relevant
skill/command is available.

Design decisions:
- Word-boundary regex (avoids "done" matching "abandoned")
- Extended trigger map: {"skill-name": {"type", "triggers"|"triggers_by_subject", "description"}}
- type "skill" → Skill(name) | type "command" → /name | type "agent" → Agent(name)
- Multi-match: one combined additionalContext, all matched skills tracked
- Bypass prefixes: *, /, #, ! (system prompts, slash commands, directives)
- Fail-open: any exception → exit 0 silently
- Session tracker: .skill-recommendations-session (reset by session-reminder.py)
- Two tracker formats:
    - Legacy (triggers list): key = skill_name (once per session)
    - by_subject (triggers_by_subject dict): key = "skill_name::subject" (once per subject per session)
      Subject priority: specific subjects first, "general" last (dict insertion order).
      Re-fires when SUBJECT changes, deduped when same subject repeats.
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
    """Return set of tracker keys already recommended this session."""
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


def _match_subject(prompt: str, triggers_by_subject: dict) -> str | None:
    """Return the first subject whose triggers match the prompt (priority order).

    Subjects are evaluated in dict insertion order — specific subjects before
    'general'. Returns None if no subject matches.
    """
    for subject, trig_list in triggers_by_subject.items():
        for trigger in trig_list:
            pattern = rf"\b{re.escape(trigger)}\b"
            if re.search(pattern, prompt, re.IGNORECASE):
                return subject
    return None


def find_matches(prompt: str, triggers: dict, already_recommended: set) -> list[dict]:
    """Return list of matched entries not yet recommended, with _tracker_key attached.

    For legacy entries (triggers list):
        tracker_key = skill_name (once per session)
    For by_subject entries (triggers_by_subject dict):
        tracker_key = "skill_name::subject" (once per subject per session)
        Subject is determined FIRST by priority, THEN checked against tracker.
    """
    matches = []
    for skill_name, entry in triggers.items():
        if not isinstance(entry, dict):
            continue

        triggers_by_subject = entry.get("triggers_by_subject")
        if triggers_by_subject:
            # by_subject format: determine subject by priority (independent of tracker)
            subject = _match_subject(prompt, triggers_by_subject)
            if subject is None:
                continue
            tracker_key = f"{skill_name}::{subject}"
            if tracker_key in already_recommended:
                continue
            matches.append({"name": skill_name, "_tracker_key": tracker_key, **entry})
        else:
            # Legacy flat-list format
            if skill_name in already_recommended:
                continue
            skill_triggers = entry.get("triggers", [])
            for trigger in skill_triggers:
                pattern = rf"\b{re.escape(trigger)}\b"
                if re.search(pattern, prompt, re.IGNORECASE):
                    matches.append({"name": skill_name, "_tracker_key": skill_name, **entry})
                    break  # One trigger per skill is enough

    return matches


def format_recommendation(match: dict) -> str:
    """Format one recommendation line based on skill type."""
    name = match["name"]
    description = match.get("description", "")
    skill_type = match.get("type", "skill")

    if skill_type == "command":
        invoke = f"/{name}"
    elif skill_type == "agent":
        invoke = f"Agent({name})"
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

        # Persist all matched tracker keys as recommended this session
        newly_recommended = already_recommended | {m["_tracker_key"] for m in matches}
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