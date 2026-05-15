---
name: cc-agents-ref
description: ALWAYS load this reference when creating or modifying a Claude Code subagent. Covers all YAML frontmatter fields: tools, hooks inline, memory, isolation, maxTurns, effort, background. Do NOT create agents without loading this first.
user-invokable: false
derniere-maj: 2026-05-14
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
color: blue # red|orange|yellow|green|blue|purple|pink|cyan
skills:
  - ma-skill
memory: project # user|project|local
isolation: worktree
initialPrompt: "Premier message soumis automatiquement comme premier tour utilisateur (via --agent)"
background: true
maxTurns: 50
effort: high # low|medium|high|xhigh|max
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
- Modèles 2026 : `haiku`=4-5, `sonnet`=4-6, `opus`=4-7
- Effort : `xhigh` = défaut Opus 4.7 (coding agentique). `high` = sessions concurrentes. `medium`/`low` = coût/latence. `max` = problèmes très durs (diminishing returns, overthinking)
- Opus 4.7 : instructions plus littérales, moins de subagents spontanés, moins de tool calls. Être explicite sur le scope, le parallélisme, et la lecture exhaustive des fichiers
- `memory: project` → persistance automatique via Auto Memory
- `isolation: worktree` → git worktree séparé pour agents parallèles
- **Un subagent NE PEUT PAS spawner de sub-agents** (GitHub #19077, by design)
- Skills listées dans `skills:` sont injectées EN ENTIER au démarrage du subagent
- Subagents **n'héritent PAS** les skills du parent — toujours lister explicitement
- `CLAUDE_CODE_FORK_SUBAGENT=1` (v2.1.117+) — le subagent hérite du contexte complet de la conversation parente et réutilise le prompt cache parent. Chaque spawn tourne en background automatiquement.

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

## Best practices (Boris + Thariq + Anthropic)

- **permissionMode OBLIGATOIRE** : `plan` sur read-only, `acceptEdits` sur write
- **disallowedTools sur read-only** : `disallowedTools: Write, Edit` = double protection (Boris)
- **effort: high sur TOUS les sonnet** — JAMAIS medium (Boris: "high for everything")
- **memory: project sur TOUS les agents** — accumulation cross-sessions
- **Writer/Reviewer pattern** : un agent ecrit, un autre review (contexte frais = pas de biais)
- **Description = trigger** : "Use PROACTIVELY when..." pour que CC sache quand dispatcher
- **Verification agents** : investir du temps sur code-reviewer, validator, test-writer (Thariq: "spend a week")
- **Opus 4.7 subagent management** : 4.7 spawn moins de subagents → fan-out doit etre EXPLICITE dans les rules
- **Plan-driven** : "the plan IS the prompt" — inclure intent + fichiers + criteres acceptance dans le prompt du Task
- **Generator/Evaluator pattern** : pour les agents complexes ou long-running, séparer le générateur (fait le travail) de l'évaluateur (juge le résultat). Les agents skewent systématiquement positif quand ils notent leur propre travail — la séparation est critique. L'évaluateur doit avoir ses propres outils (ex: Playwright MCP pour tests UI).

## Gotchas

- **`memory: project` obligatoire** — sur TOUS les agents sans exception. Sans ça, pas d'accumulation cross-sessions et chaque run repart de zéro.
- **`skills:` obligatoire** — les subagents n'héritent PAS des skills du parent. Toujours lister explicitement chaque skill nécessaire dans le frontmatter de l'agent.
- **Pas de `Agent` dans les tools d'un subagent** — les subagents ne peuvent pas spawner d'autres sub-agents (GitHub #19077, by design). Un agent qui a besoin d'un autre worker doit être redesigné comme orchestrateur au niveau rules.

## Localisation

- `.claude/agents/` → projet ← PRIORITAIRE
- `~/.claude/agents/` → tous projets

## Vault

[[agents-orchestration]], [[context-management]] — isolation, orchestration patterns, worktree usage.
