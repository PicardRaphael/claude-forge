---
name: cc-features-ref
description: Référence de toutes les fonctionnalités Claude Code 2026 — /loop, /schedule, /batch, /simplify, /voice, /teleport, worktrees, effort levels, Auto Memory, plugins, LSPs, Agent Teams, flags CLI. Charger quand l'utilisateur demande les nouveautés ou veut savoir ce qui existe.
user-invokable: false
---

# Fonctionnalités Claude Code 2026

_Mise à jour : 3 avril 2026 — utiliser cc-news pour les nouveautés postérieures_

## Slash Commands

| Command                      | Rôle                                         |
| ---------------------------- | -------------------------------------------- |
| `/loop <interval> <skill>`   | Boucle automatique (ex: `/loop 5m /babysit`) |
| `/schedule "<cron>" <skill>` | Planifié jusqu'à 1 semaine                   |
| `/batch <instruction>`       | Parallèle via worktrees (5-30 unités)        |
| `/simplify [focus]`          | 3 agents parallèles de review qualité        |
| `/debug`                     | Troubleshoot via logs de session             |
| `/voice`                     | Contrôle vocal                               |
| `/teleport`                  | Push session local ↔ claude.ai/code          |
| `/btw <note>`                | Question sidebar COÛT ZÉRO (pas de pollution contexte) |
| `/branch`                    | Fork la session courante                     |
| `/compact "instructions"`    | Compaction ciblée avec instructions           |
| `/config`                    | Thème, output style, modèle                  |
| `/agents`                    | Gère les subagents                           |
| `/skills`                    | Liste les skills                             |
| `/permissions`               | Pré-approuve les permissions                 |
| `/memory`                    | Gère la mémoire auto                         |
| `/model`                     | Change de modèle en cours de session         |
| `/compact`                   | Compacte le contexte                         |
| `/context`                   | Inspecte le contexte                         |

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

| Niveau   | Effet                  |
| -------- | ---------------------- |
| `low`    | Rapide, simple         |
| `medium` | Défaut (Opus/Sonnet 4.6) |
| `high`   | Thinking étendu activé |

**`max` supprimé depuis v2.1.91.** Utiliser `high`. Keyword `ultrathink` dans le contenu active le thinking étendu ponctuellement.

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

## Fonctionnalités récentes (avril 2026)

| Feature | Description |
|---------|-------------|
| Cloud Auto-Fix | Fixe CI failures et review comments automatiquement |
| Computer Use | Claude contrôle l'écran (research preview) |
| Session sharing | Partager conversation par lien |
| Plugin Marketplace | `/plugin` > Discover — marketplace officiel |
| Plugin executables | `bin/` dans plugin → commandes callable depuis Bash |
| `additionalDirectories` | Dans settings.json pour accès repos externes permanent |
| `disableSkillShellExecution` | Bloquer exécution shell dans les skills |
| `PermissionDenied` hook | Se déclenche après refus auto mode |
| `PostCompact` hook | Se déclenche après compression du contexte |
| Deferred hooks | `PreToolUse` peut retourner `permissionDecision: "defer"` |
| `InstructionsLoaded` hook | Quand un CLAUDE.md ou rule se charge |

## .claude/rules/ (v2.0.64+)

Fichiers `.md` auto-chargés à chaque session. Alternative modulaire au CLAUDE.md monolithique.

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# Règles uniquement pour les fichiers API TypeScript
```

- Sans `paths:` → chargé à chaque session
- Avec `paths:` → chargé uniquement quand Claude lit un fichier matchant
- Sous-dossiers supportés
- Bon endroit pour : routing agents, workflows, règles obligatoires

## Best practices (Boris + équipe)

- **`/clear` entre tâches non liées** — sessions fourre-tout = piège #1
- **`/compact` proactif à 70%** — pas attendre l'auto-compact
- **"Document & Clear"** — dump plan dans un .md, /clear, nouvelle session
- **CLAUDE.md concis** — pour chaque ligne : "si je l'enlève, ça casse ?" sinon couper
- **Hooks = 100% déterministe. CLAUDE.md = ~80%.** (Boris)
- **Vérification = tip #1** — toujours donner à Claude un moyen de vérifier son output

## Plugins

```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```

LSPs disponibles pour tous les langages majeurs.

## Flags CLI clés

| Flag               | Usage                              |
| ------------------ | ---------------------------------- |
| `--worktree <n>`   | Worktree isolé                     |
| `--tmux`           | Session tmux dédiée                |
| `--bare`           | 10x plus rapide, sans UI           |
| `--agent <n>`      | Agent custom comme agent principal |
| `--resume <id>`    | Reprend une session                |
| `--continue`       | Continue la dernière session       |
| `--from-pr <url>`  | Worktree depuis une PR             |
| `--add-dir <path>` | Ajoute un dossier au contexte      |
| `-w`               | Raccourci worktree                 |
| `--teleport`       | Push vers claude.ai/code           |
| `-p <prompt>`      | Mode headless                      |

## Hooks Boris en production

```json
{
  "SessionStart": [
    { "hooks": [{ "type": "command", "command": "./hooks/load-context.sh" }] }
  ],
  "PermissionRequest": [
    { "hooks": [{ "type": "agent", "agent": "permission-judge" }] }
  ],
  "Stop": [
    { "hooks": [{ "type": "command", "command": "./hooks/check-if-done.sh" }] }
  ]
}
```
