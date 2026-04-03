---
name: cc-features-ref
description: Référence de toutes les fonctionnalités Claude Code 2026 — /loop, /schedule, /batch, /simplify, /voice, /teleport, worktrees, effort levels, Auto Memory, plugins, LSPs, Agent Teams, flags CLI. Charger quand l'utilisateur demande les nouveautés ou veut savoir ce qui existe.
user-invocable: false
---

# Fonctionnalités Claude Code 2026

*Référence au 31 mars 2026 — utiliser cc-news pour les nouveautés postérieures*

## Slash Commands

| Command | Rôle |
|---------|------|
| `/loop <interval> <skill>` | Boucle automatique (ex: `/loop 5m /babysit`) |
| `/schedule "<cron>" <skill>` | Planifié jusqu'à 1 semaine |
| `/batch <instruction>` | Parallèle via worktrees (5-30 unités) |
| `/simplify [focus]` | 3 agents parallèles de review qualité |
| `/debug` | Troubleshoot via logs de session |
| `/voice` | Contrôle vocal |
| `/teleport` | Push session local ↔ claude.ai/code |
| `/btw <note>` | Note sans interrompre Claude |
| `/config` | Thème, output style, modèle |
| `/agents` | Gère les subagents |
| `/skills` | Liste les skills |
| `/permissions` | Pré-approuve les permissions |
| `/memory` | Gère la mémoire auto |
| `/model` | Change de modèle en cours de session |
| `/compact` | Compacte le contexte |
| `/context` | Inspecte le contexte |

## /loop — La plus puissante

```bash
/loop 5m /babysit          # babysit PRs toutes les 5min
/loop 30m /slack-feedback  # PRs depuis feedback Slack
/loop 1h /pr-pruner        # ferme les PRs stales
/loop /post-merge-sweeper  # commentaires de review manqués
```

Format interval : `5m`, `30m`, `1h`, `6h`, `1d`

## /schedule

```bash
/schedule "0 9 * * 1-5" /standup-post   # lundi-vendredi 9h
/schedule "0 * * * *" /monitor          # chaque heure
```

## Effort levels

| Niveau | Effet |
|--------|-------|
| `low` | Rapide, simple |
| `medium` | Défaut |
| `high` | Analyse approfondie |
| `max` | Thinking étendu activé |

Dans le contenu d'une skill : le mot `ultrathink` active le thinking étendu.

## Git Worktrees — #1 productivité

```bash
claude --worktree ma-feature
claude --worktree ma-feature --tmux
```

Lancer 3-5 en parallèle avec aliases `za`, `zb`, `zc`.

## Auto Memory (v2.1.59+)

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          ← index chargé à chaque session
└── fichiers-thématiques.md
```

Configurer via `/memory`. Désactiver : `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

## Agent Teams (expérimental)

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```
Subagents qui se communiquent directement via task board partagé.

## Plugins

```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```
LSPs disponibles pour tous les langages majeurs.

## Flags CLI clés

| Flag | Usage |
|------|-------|
| `--worktree <n>` | Worktree isolé |
| `--tmux` | Session tmux dédiée |
| `--bare` | 10x plus rapide, sans UI |
| `--agent <n>` | Agent custom comme agent principal |
| `--resume <id>` | Reprend une session |
| `--continue` | Continue la dernière session |
| `--from-pr <url>` | Worktree depuis une PR |
| `--add-dir <path>` | Ajoute un dossier au contexte |
| `--teleport` | Push vers claude.ai/code |
| `-p <prompt>` | Mode headless |

## Hooks Boris en production

```json
{
  "SessionStart": [{"hooks": [{"type": "command", "command": "./hooks/load-context.sh"}]}],
  "PermissionRequest": [{"hooks": [{"type": "agent", "agent": "permission-judge"}]}],
  "Stop": [{"hooks": [{"type": "command", "command": "./hooks/check-if-done.sh"}]}]
}
```
