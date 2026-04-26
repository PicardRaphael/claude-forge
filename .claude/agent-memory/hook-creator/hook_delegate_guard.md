---
name: delegate-guard-hook
description: PreToolUse hook bloquant les edits directs sur fichiers proteges — SKILL.md, .claude/agents/*.md, CLAUDE.md — pour forcer delegation aux agents specialises
type: project
---

Hook `delegate-guard.py` cree le 2026-04-26. Fonctionne en production, 10/10 tests passes.

## Fichiers
- Script : `C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/hooks/delegate-guard.py`
- Config : `.claude/settings.json`, PreToolUse, matcher `Edit|Write`

## Comportement
- SKILL.md → bloque, indique `skill-creator`
- .claude/agents/*.md (direct children seulement, pas recursif) → bloque, indique `agent-creator`
- CLAUDE.md → bloque, indique `claudemd-optimizer`
- settings.json, rules/*.md → laisse passer
- CLAUDE_AGENT env var = specialist connu → bypass
- Edit avec old_string + new_string < 20 chars → typo pass-through avec WARNING
- Write court sur fichier protege → toujours BLOCK (pas d'exception typo pour Write)

## Edge cases importants
- Normalisation backslash Windows obligatoire (`path.replace("\\", "/")`)
- Comparaison `basename == "SKILL.md"` exacte (pas endswith) pour eviter faux positifs vault
- Agents subdirectory check : `parts[-2] == "agents" and parts[-3] == ".claude"` (single level)
- Fail-open sur exception (`except Exception: sys.exit(0)`)

**Why:** Rules advisory = Claude les ignore. Hook = deterministe a 100%.
**How to apply:** Modele ce pattern pour tout hook de delegation.
