---
name: claude-code-complete-architecture
description: Architecture complete .claude/ — rules, agents, skills, hooks, settings, commands. Quand utiliser quoi. Recherche validée avril 2026.
type: reference
---

## Structure complète .claude/

```
.claude/
  settings.json           # Permissions, hooks, additionalDirectories
  settings.local.json     # Overrides perso (gitignored)
  .mcp.json               # MCP servers
  CLAUDE.md               # Contexte projet (config, standards, conventions)
  rules/                  # Comportements OBLIGATOIRES (auto-loaded)
  skills/                 # Workflows on-demand (invoqués ou auto-triggered)
  agents/                 # Subagents spécialisés
  agent-memory/           # Mémoire persistante des agents
  commands/               # DÉPRÉCIÉ → utiliser skills
  hooks/                  # Scripts Python/JS pour les events
  scripts/                # Scripts utilitaires (hooks, etc.)
  plans/                  # Plans d'implémentation
```

## Quand utiliser quoi

| Besoin | Composant | Chargement |
|--------|-----------|-----------|
| Contexte projet, config, standards | `CLAUDE.md` | Toujours, chaque session |
| Règles obligatoires, routing agents, workflows | `rules/*.md` | Toujours (ou path-scoped) |
| Workflow invocable (/commande ou auto-trigger) | `skills/*/SKILL.md` | Sur invocation ou description match |
| Worker spécialisé (code, debug, review) | `agents/*.md` | Quand dispatché par la session principale |
| Accès repo externe | `settings.json` → `additionalDirectories` | Toujours |
| Scripts d'automation | `hooks/`, `scripts/` | Sur events lifecycle |

## Rules vs CLAUDE.md vs Skills

| | CLAUDE.md | Rules | Skills |
|-|-----------|-------|--------|
| Chargé | Toujours | Toujours ou path-scoped | Sur demande |
| Pour | Contexte, config | Comportement obligatoire | Workflow, procédure |
| Frontmatter | Non | `paths:` seulement | Complet (name, model, etc.) |
| Arguments | Non | Non | Oui ($ARGUMENTS) |

## Rules — path-scoped

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# Ces règles s'appliquent uniquement aux fichiers API TypeScript
```

## additionalDirectories

```json
{
  "permissions": {
    "additionalDirectories": ["/chemin/vers/repo-externe"]
  }
}
```
- Dans `.claude/settings.json` pour le projet
- Bug connu : ne charge pas les skills depuis les dirs ajoutés (#30064)
- Alternative fiable : alias shell `claude --add-dir /chemin`

## Agents — rappels critiques

- Un subagent NE PEUT PAS spawner de sub-agents (#19077)
- Session principale = orchestrateur (lit rules, dispatch agents)
- `tools:` = allowlist stricte. Si un agent a Bash, il l'utilisera.
- `disallowedTools:` = denylist
- `Agent(nom1, nom2)` = restreindre quels agents peuvent être spawnés
- `memory: project` = mémoire persistante entre sessions
- Skills listées dans `skills:` sont injectées EN ENTIER au démarrage
- Subagents n'héritent PAS les skills du parent

## Repos de référence

- shanraisshan/claude-code-best-practice — structure complète
- rohitg00/awesome-claude-code-toolkit — 135 agents, 35 skills
- hesreallyhim/awesome-claude-code — index curé
