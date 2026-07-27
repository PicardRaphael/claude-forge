---
titre: "Architecture du dossier .claude/ — composants, rôles, règles de chargement"
resume: "Référence complète du dossier .claude/ : structure, quand utiliser CLAUDE.md vs rules vs skills vs agents vs hooks, additionalDirectories, gotchas subagents."
aliases:
  - "architecture .claude"
  - "structure dossier claude"
  - "claude folder structure"
  - "rules vs skills vs agents"
  - "quand utiliser CLAUDE.md"
  - "additionalDirectories claude"
domaine: claude-code
type: reference
derniere-maj: 2026-07-27
auteur: claude
sources:
  - "memory/reference_claude_code_architecture.md (avril 2026)"
  - "shanraisshan/claude-code-best-practice"
tags:
  - "#type/reference"
  - "#domaine/claude-code"
---
# Architecture du dossier .claude/

> Référence canonique forge : structure complète du dossier `.claude/`, rôles de chaque composant, règles de chargement, et gotchas critiques. Validé avril 2026.

## Structure complète

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
  commands/               # DÉPRÉCIÉ → utiliser skills/
  hooks/                  # Scripts Python/JS pour les events lifecycle
  scripts/                # Scripts utilitaires (hooks, etc.)
  plans/                  # Plans d'implémentation
  workflows/              # Workflows nommés sauvegardés (slash commands, juil. 2026)
```

## Quand utiliser quel composant

| Besoin | Composant | Chargement |
|--------|-----------|------------|
| Contexte projet, config, standards | `CLAUDE.md` | Toujours, chaque session |
| Règles obligatoires, routing agents, workflows | `rules/*.md` | Toujours (ou path-scoped) |
| Workflow invocable (`/commande` ou auto-trigger) | `skills/*/SKILL.md` | Sur invocation ou description match |
| Worker spécialisé (code, debug, review) | `agents/*.md` | Quand dispatché par la session principale |
| Orchestration multi-agents rejouable | `workflows/*.js` | Sur invocation `/<nom>` (cf [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] AJOUT 27 juil.) |
| Accès repo externe | `settings.json` → `additionalDirectories` | Toujours |
| Scripts d'automation sur events | `hooks/`, `scripts/` | Sur events lifecycle |

## CLAUDE.md vs Rules vs Skills

| | CLAUDE.md | Rules | Skills |
|-|-----------|-------|--------|
| Chargé | Toujours | Toujours ou path-scoped | Sur demande |
| Pour | Contexte, config | Comportement obligatoire | Workflow, procédure |
| Frontmatter | Non | `paths:` seulement | Complet (name, model, etc.) |
| Arguments | Non | Non | Oui (`$ARGUMENTS`) |

Sweet spot taille : `CLAUDE.md` < 200 L · `SKILL.md` < 500 L (seuls seuils canoniques Anthropic — cf [[comment-ecrire-claudemd]] et [[comment-creer-skill]]).

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

- Dans `.claude/settings.json` pour le projet.
- **Bug connu** (#30064) : ne charge PAS les skills depuis les dirs ajoutés.
- **Alternative fiable** : alias shell `claude --add-dir /chemin`.

## Agents — gotchas critiques

- **Nesting de subagents : depth 3 par défaut depuis CC v2.1.219 (24 juil. 2026)** — un subagent peut spawner des subagents sur 3 niveaux (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` pour l'interdire ; caps 200 spawns/session, 20 concurrents). Recommandation forge inchangée : escalade vers la session principale par défaut, cf [[anti-reentrance-sub-agents-pattern-escalade]].
- Session principale = orchestrateur (lit rules, dispatch agents).
- `tools:` = allowlist stricte. Si un agent a `Bash`, il l'utilisera.
- `disallowedTools:` = denylist.
- `Agent(nom1, nom2)` = restreindre quels agents peuvent être spawnés.
- `memory: project` = mémoire persistante entre sessions (obligatoire sur tous agents forge).
- Skills listées dans `skills:` sont injectées EN ENTIER au démarrage — ne pas lister `Skill` dans `tools:` pour ça.
- **Subagents n'héritent PAS les skills du parent** → brief in-body obligatoire (cf [[pattern-mcp-brief-then-direct]]).

## Repos de référence

- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — structure complète
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — 135 agents, 35 skills
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — index curé

## WIKILINKS

- [[comment-ecrire-claudemd]] — écrire un CLAUDE.md efficace
- [[comment-creer-skill]] — créer une skill conforme
- [[comment-creer-agent]] — créer un subagent conforme
- [[comment-creer-hook]] — créer un hook lifecycle
- [[plugin-vs-skill-anatomie]] — skill vs plugin, anatomie et distribution
- [[mcp-vs-skills-doctrine]] — MCP data / skills how-to / Bash exploration
- [[pattern-mcp-brief-then-direct]] — brief in-body pour cross-repo et Agent Teams
- [[anti-reentrance-sub-agents-pattern-escalade]] — nesting subagents, escalade STOP
- [[methode-analyser-repo]] — méthode 6 étapes analyse repo + audit .claude/
