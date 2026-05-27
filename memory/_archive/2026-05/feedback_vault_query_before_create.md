---
name: vault-query-before-create
description: Hook deterministe vault-query-guard bloque Write sur vault/output/skills/agents si forge-brain pas consulte. Rules advisory insuffisantes seules.
type: feedback
originSessionId: 424370ce-3cf7-4ae9-bb8b-d6ff1e01fec1
---
Avant de créer un fichier dans vault/, output/, .claude/skills/, .claude/agents/, le vault forge-brain DOIT avoir été consulté dans la session (Knowledge/erreurs/, 04-Techniques/, 07-Prompts/).

**Why:** Erreur récurrente (3 fois : #7 avril, #8 avril, #9 mai). Les rules advisory sont ignorées sous pression conversationnelle ("fluency bias"). Seul un hook déterministe résiste.

**How to apply:** Deux hooks couplés dans claude-forge :
- `vault-query-tracker.py` (PostToolUse) : écrit marqueur quand Read/Grep/Glob/Skill cible vault/memory
- `vault-query-guard.py` (PreToolUse) : bloque Write si marqueur absent ou > 60 min
- Bypass : CLAUDE_AGENT = specialist (skill-creator, agent-creator, project-analyzer, etc.)
- Le marqueur dure 60 min = dans la même conversation, pas besoin de relire pour chaque fichier
