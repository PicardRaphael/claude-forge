---
name: cc-agents-ref
description: Référence complète du format YAML des subagents Claude Code — tous les champs frontmatter, tools, hooks inline, memory, isolation, maxTurns, effort, background. Charger quand on crée ou modifie un agent.
user-invokable: false
---

# Référence — Subagents Claude Code

## Format complet

```yaml
---
name: mon-agent # OBLIGATOIRE — kebab-case unique
description: Use this agent when [condition]. Use PROACTIVELY when [trigger]. Input must include [quoi]. # OBLIGATOIRE — UNE SEULE LIGNE
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet # haiku|sonnet|opus|inherit
color: blue # red|orange|yellow|green|blue|purple
skills:
  - ma-skill
memory: project # user|project|local
isolation: worktree
background: true
maxTurns: 50
effort: high # low|medium|high|max
permissionMode: acceptEdits # acceptEdits|plan|bypassPermissions
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 .claude/hooks/lint.py"
---
```

## Règles critiques

- Description **UNE SEULE LIGNE** en **anglais** — `>-` et `|` cassent l'indexeur
- Modèles 2026 : `haiku`=4-5, `sonnet`=4-6, `opus`=4-6
- `effort: high` = thinking étendu (**`max` supprimé depuis v2.1.91**)
- `memory: project` → persistance automatique via Auto Memory
- `isolation: worktree` → git worktree séparé pour agents parallèles
- **Un subagent NE PEUT PAS spawner de sub-agents** (GitHub #19077, by design)
- Skills listées dans `skills:` sont injectées EN ENTIER au démarrage du subagent
- Subagents **n'héritent PAS** les skills du parent — toujours lister explicitement

## Tools par profil

| Profil | Tools |
|--------|-------|
| Read-only / Analyse | `Read, Grep, Glob` |
| + shell | ajouter `Bash` |
| + web | ajouter `WebFetch, WebSearch` |
| Implémentation | ajouter `Write, Edit` |
| Orchestrateur | **UNIQUEMENT `Agent(nom1, nom2), Read`** — pas de Bash/Grep |

### Tools avancés

- `Agent(nom1, nom2)` → restreindre quels agents peuvent être spawnés
- `Bash(git *)` → restreindre Bash à des commandes spécifiques
- `disallowedTools: Bash, Write` → denylist (retire de la liste héritée)

### ATTENTION : un agent qui a Bash/Grep fera le travail lui-même au lieu de déléguer. Pour forcer la délégation, retirer ces outils.

## System prompt — ordre obligatoire

1. Rôle
2. Input reçu
3. Étapes numérotées
4. Règles strictes (dont "dit NON quand")
5. Format de sortie avec exemple exact
6. Section Apprentissage (si skill métier → sauvegarder en mémoire)

## Architecture — où va quoi

| Besoin | Composant |
|--------|-----------|
| Orchestration / routing | `.claude/rules/` (PAS un agent) |
| Worker spécialisé | `.claude/agents/` |
| Workflow invocable | `.claude/skills/` |
| Contexte projet | `CLAUDE.md` |
| Accès repo externe | `settings.json` → `additionalDirectories` |

**La session principale = l'orchestrateur.** Elle lit les rules et dispatch aux agents.
**NE JAMAIS créer d'agent orchestrateur/CTO.** Ça ne marche pas.

## Localisation

- `.claude/agents/` → projet ← PRIORITAIRE
- `~/.claude/agents/` → tous projets
