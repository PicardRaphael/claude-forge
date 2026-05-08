---
name: session-health-hook
description: UserPromptSubmit hook counting turns via session_id-scoped counter, reminds /compact or /clear at 20 and 40 turns
type: project
---

# session-health.py — Turn counter hook

## Pattern

- Event: `UserPromptSubmit` (fires exactly once per user turn)
- Output: `additionalContext` via `hookSpecificOutput` JSON (v2.1.94+) — Claude sees it in context
- Counter: `.claude/.session-turn-counter` JSON file with `{session_id, count}` — resets on session_id change, no TTL
- Exit: always 0, never blocks

## Behavior

| Turn | Message |
|------|---------|
| 1-2 | /recap suggestion (new session detected) |
| every 20 | Document & Clear reminder |
| every 40 | Urgent /compact reminder |
| other | Silent (no output) |

## Key decisions

- `UserPromptSubmit` chosen over `Notification` (Notification fires on permission prompts, not turns) and `PostToolUse` (overcounts)
- session_id scoping avoids TTL antipattern (see erreur-marker-ttl-blocage-agents in vault)
- `additionalContext` output format makes Claude aware of the reminder, not just the terminal user

## File paths

- Script: `.claude/hooks/session-health.py`
- Counter: `.claude/.session-turn-counter`
