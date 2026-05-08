# Memory Index

- [delegate-guard-hook](hook_delegate_guard.md) — PreToolUse Edit|Write hook bloquant les edits directs de SKILL.md, agents/*.md, CLAUDE.md
- [vault-query-pair-hooks](hook_vault_query_pair.md) — Paire tracker+guard forçant query forge-brain avant Write sur vault/output/.claude/skills/.claude/agents
- [session-health-hook](hook_session_health.md) — UserPromptSubmit hook compteur tours, rappel /compact à 20 et 40 tours via additionalContext
- [devil-advocate-pair-hooks](hook_devil_advocate_pair.md) — PostToolUse Agent: tracker+guard devils-advocate (existence marker, one-shot) + reasoning-cache-reminder (word-boundary regex, once-per-session)
