---
name: vault-query-pair-hooks
description: Paire tracker+guard pour forcer la query forge-brain avant tout Write sur vault/output/.claude/skills/.claude/agents
type: project
---

Deux hooks complémentaires déployés le 2026-05-06 :

- `vault-query-tracker.py` (PostToolUse Read|Grep|Glob|Skill) — écrit un marker ISO timestamp dans `.claude/.session-vault-queried` si le tool cible vault/, memory/, Knowledge/, forge-brain, 04-Techniques/, 07-Prompts/.
- `vault-query-guard.py` (PreToolUse Write) — bloque avec exit 2 tout Write vers vault/, output/, .claude/skills/, .claude/agents/ si le marker est absent ou > 60 min.

**Why:** Les advisory rules (check-before-create, forge-brain-proactive) avaient un taux d'échec documenté. Failure #8 dans feedback_major_mistakes. Les hooks sont déterministes.

**How to apply:**
- Marker path hardcodé en absolu : `.claude/.session-vault-queried`
- Bypass : `CLAUDE_AGENT` dans `{skill-creator, agent-creator, hook-creator, claudemd-optimizer}` → exit 0
- Fail-open uniquement sur stdin parse error — marker absent = BLOCK (pas fail-open)
- `.claude/.session-vault-queried` ajouté au `.gitignore` racine
- Pour Skill tool : sérialiser tout `tool_input` en JSON string (field name variable selon CC version)
