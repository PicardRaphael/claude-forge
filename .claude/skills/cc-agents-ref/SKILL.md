---
name: cc-agents-ref
description: Référence complète du format YAML des subagents Claude Code — tous les champs frontmatter, tools, hooks inline, memory, isolation, maxTurns, effort, background. Charger quand on crée ou modifie un agent.
user-invocable: false
---

# Référence — Subagents Claude Code

## Format complet

```yaml
---
name: mon-agent                    # OBLIGATOIRE — kebab-case unique
description: Use this agent when [condition]. Use PROACTIVELY when [trigger]. Input must include [quoi].  # OBLIGATOIRE — UNE SEULE LIGNE
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet                      # haiku|sonnet|opus|inherit
color: blue                        # red|orange|yellow|green|blue|purple
skills:
  - ma-skill
memory: project                    # user|project|local
isolation: worktree
background: true
maxTurns: 50
effort: high                       # low|medium|high|max
permissionMode: acceptEdits        # acceptEdits|plan|bypassPermissions
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 .claude/hooks/lint.py"
---
```

## Règles critiques

- Description **UNE SEULE LIGNE** — `>-` et `|` cassent l'indexeur
- Modèles 2026 : `haiku`=4-5, `sonnet`=4-6, `opus`=4-6
- `effort: max` = thinking étendu automatiquement
- `memory: project` → `.claude/agent-memory/<nom>/MEMORY.md`
- `isolation: worktree` → git worktree séparé pour agents parallèles

## Tools par profil

| Profil | Tools |
|--------|-------|
| Read-only | `Read, Grep, Glob` |
| + shell lecture | ajouter `Bash` |
| + web | ajouter `WebFetch, WebSearch` |
| Écrivain | ajouter `Write, Edit` |

Bash restreint : `Bash(git *)`, `Bash(bun run *)`

## System prompt — ordre obligatoire

1. Rôle
2. Input reçu
3. Étapes numérotées
4. Règles strictes
5. Format de sortie avec exemple exact

## Localisation

- `.claude/agents/` → projet ← PRIORITAIRE
- `~/.claude/agents/` → tous projets
