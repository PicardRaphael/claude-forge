---
name: cc-features-ref
description: 'ALWAYS load when user asks about Claude Code features, capabilities, or what exists. Covers 2026 features: /loop, /schedule, /batch, /simplify, /voice, worktrees, effort, Auto Memory, plugins, LSPs, Agent Teams, CLI flags.'
user-invocable: false
---

# FonctionnalitÃ©s Claude Code 2026

_Mise Ã  jour : 4 juin 2026 (intÃ¨gre des Ã©lÃ©ments jusqu'Ã  juin 2026, v2.1.160) â€” utiliser cc-news pour les nouveautÃ©s postÃ©rieures_

## Slash Commands

| Command                      | RÃ´le                                         |
| ---------------------------- | -------------------------------------------- |
| `/loop <interval> <skill>`   | Boucle automatique (ex: `/loop 5m /babysit`) |
| `/schedule "<cron>" <skill>` | PlanifiÃ© jusqu'Ã  1 semaine                   |
| `/goal <condition>`          | Travaille en autonome jusqu'Ã  condition vraie (ex: `/goal all tests pass`) â€” modes : interactif, `-p`, Remote Control |
| `/batch <instruction>`       | ParallÃ¨le via worktrees (5-30 unitÃ©s)        |
| `/simplify [focus]`          | 3 agents parallÃ¨les de review qualitÃ©        |
| `/debug`                     | Troubleshoot via logs de session             |
| `/voice`                     | ContrÃ´le vocal                               |
| `/teleport`                  | Push session local â†” claude.ai/code          |
| `/btw <note>`                | Question sidebar COÃ›T ZÃ‰RO (pas de pollution contexte) |
| `/branch`                    | Fork la session courante                     |
| `/compact "instructions"`    | Compaction ciblÃ©e avec instructions           |
| `/config`                    | ThÃ¨me, output style, modÃ¨le                  |
| `/agents`                    | GÃ¨re les subagents                           |
| `/skills`                    | Liste les skills                             |
| `/permissions`               | PrÃ©-approuve les permissions                 |
| `/memory`                    | GÃ¨re la mÃ©moire auto                         |
| `/model`                     | Change de modÃ¨le en cours de session         |
| `/compact`                   | Compacte le contexte                         |
| `/context`                   | Inspecte le contexte                         |
| `/team-onboarding`           | GÃ©nÃ¨re guide ramp-up pour nouveaux membres (v2.1.101) |
| `/ultraplan`                 | Auto-provisioning environnement cloud distant (v2.1.101) |
| `/autofix-pr`                | Envoie session+PR au cloud, fixer continue avec contexte (Noah, v2.1.97+) |
| `/tui fullscreen`            | Mode fullscreen sans scintillement (v2.1.110) |
| `/recap`                     | RÃ©sumÃ© de session au retour (v2.1.108) |
| `/focus`                     | Focus view â€” remplace ancien Ctrl+O focus (v2.1.110) |
| `/doctor`                    | Diagnostique MCP, alertes dupliquÃ©s cross-scopes (v2.1.110) |
| `/usage`                     | Fusionne /cost + /stats â€” les deux restent comme alias (v2.1.119) |
| `/theme`                     | CrÃ©er/switcher custom themes JSON dans ~/.claude/themes/ (v2.1.119) |

## /loop â€” La plus puissante

```bash
/loop 5m /babysit          # babysit PRs toutes les 5min
/loop 30m /slack-feedback  # PRs depuis feedback Slack
/loop 1h /pr-pruner        # ferme les PRs stales
/loop /post-merge-sweeper  # commentaires de review manquÃ©s
```

Format interval : `5m`, `30m`, `1h`, `6h`, `1d`

### Dynamic Loop (v2.1.110, Noah)

```bash
/loop /babysit-prs          # SANS intervalle = Claude auto-programme le prochain tick
```

Claude utilise `ScheduleWakeup` pour dÃ©cider dynamiquement quand revÃ©rifier (Ã©conomie de tokens vs polling fixe).

## /schedule

```bash
/schedule "0 9 * * 1-5" /standup-post   # lundi-vendredi 9h
/schedule "0 * * * *" /monitor          # chaque heure
```

## Effort levels

| Niveau   | Effet (Opus 4.7)                                        |
| -------- | -------------------------------------------------------- |
| `low`    | â‰ˆ medium 4.6. Routes simples, schÃ©mas, tests unitaires  |
| `medium` | Refactors multi-fichiers, migrations simples             |
| `high`   | Migrations complexes, debug cross-layer, code review     |
| `xhigh`  | **DÃ‰FAUT Opus 4.7.** Design API, archi modules, refactors structurels, tÃ¢ches agentiques longues |
| `max`    | ProblÃ¨mes trÃ¨s durs. Diminishing returns, prone overthinking |

**`xhigh` est le nouveau dÃ©faut** pour Opus 4.7 (v2.1.111+). `high` reste le dÃ©faut pour Sonnet 4.6.
Effort plus important sur 4.7 que tout modÃ¨le prÃ©cÃ©dent â€” il contrÃ´le directement le nombre de tool calls et la profondeur de raisonnement.
Ã€ `xhigh`/`max` : mettre max_tokens Ã  64k+ minimum.

**Opus 4.8** (`claude-opus-4-8`, sorti 28 mai 2026) â€” dÃ©faut effort = **high** (recommandÃ©), options `extra`/`xhigh`/`max`. Fast mode 3Ã— moins cher qu'avant (vitesse 2.5Ã—). ~4Ã— moins susceptible de laisser passer une faille sans la signaler vs 4.7. C'est dÃ©sormais le dernier Opus : le dÃ©faut forge `opus` = `claude-opus-4-8`.

## Git Worktrees â€” #1 productivitÃ©

```bash
claude --worktree ma-feature
claude --worktree ma-feature --tmux
```

Lancer 3-5 en parallÃ¨le avec aliases `za`, `zb`, `zc`.

## Auto Memory (v2.1.59+)

```
~/.claude/projects/<project>/memory/
â”œâ”€â”€ MEMORY.md          â† index chargÃ© Ã  chaque session
â””â”€â”€ fichiers-thÃ©matiques.md
```

Configurer via `/memory`. DÃ©sactiver : `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

## Agent Teams (expÃ©rimental)

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

Subagents qui se communiquent directement via task board partagÃ©.

## FonctionnalitÃ©s rÃ©centes (avril 2026)

| Feature | Description |
|---------|-------------|
| Cloud Auto-Fix | Fixe CI failures et review comments automatiquement |
| Computer Use | Claude contrÃ´le l'Ã©cran (research preview) |
| Session sharing | Partager conversation par lien |
| Plugin Marketplace | `/plugin` > Discover â€” marketplace officiel |
| Plugin executables | `bin/` dans plugin â†’ commandes callable depuis Bash |
| `additionalDirectories` | Dans settings.json pour accÃ¨s repos externes permanent |
| `disableSkillShellExecution` | Bloquer exÃ©cution shell dans les skills |
| `PermissionDenied` hook | Se dÃ©clenche aprÃ¨s refus auto mode |
| `PostCompact` hook | Se dÃ©clenche aprÃ¨s compression du contexte |
| Deferred hooks | `PreToolUse` peut retourner `permissionDecision: "defer"` |
| `InstructionsLoaded` hook | Quand un CLAUDE.md ou rule se charge |
| `hookSpecificOutput.sessionTitle` | Nommer sessions depuis hook `UserPromptSubmit` (v2.1.94) |
| `keep-coding-instructions` | Nouveau frontmatter pour output styles de plugins (v2.1.94) |
| Bedrock via Mantle | `CLAUDE_CODE_USE_MANTLE=1` (v2.1.94) |
| `NO_FLICKER` mode | `CLAUDE_CODE_NO_FLICKER=1` renderer expÃ©rimental + support souris (Boris) |
| Opus 4.6 output | 64k tokens par dÃ©faut, 128k max (Cat Wu) |
| `--resume` cross-worktree | Reprend sessions d'autres worktrees du mÃªme repo (v2.1.94) |
| Write tool 60% faster | Diff computation optimisÃ©e sur gros fichiers (v2.1.94) |
| OS CA cert store | Trusted par dÃ©faut, `CLAUDE_CODE_CERT_STORE=bundled` pour revenir (v2.1.101) |
| Settings resilience | Typos hook events ne cassent plus settings.json (v2.1.101) |
| Monitor tool | Suit logs/PR par script, remplace le polling agent â€” gros savings tokens (Noah, v2.1.97+) |
| Managed Agents | Beta publique, sandboxing, SSE, $0.08/session-hour (8 avril) |
| Cowork GA | Tous plans payÃ©s, RBAC, OpenTelemetry, usage analytics Enterprise (avril) |
| Dispatch + CC | Lance sessions Claude Code + Computer Use intÃ©grÃ© (avril) |
| **Routines** | **Research preview** â€” Scheduled + API + Webhook automations cloud (v2.1.110) |
| **Desktop Redesign** | Multi-sessions sidebar, terminal intÃ©grÃ©, Side Chat `Cmd+;`, 3 modes vue (14 avril) |
| **Push notifications** | Claude envoie notifs push mobiles (Remote Control + config, v2.1.110) |
| **`--channels`** | Relay approbation permissions vers tÃ©lÃ©phone (v2.1.110) |
| `PreCompact` hook | Avant compression contexte, blocage possible exit code 2 (v2.1.110) |
| `ENABLE_PROMPT_CACHING_1H` | Opt-in cache 1h (API key, Bedrock, Vertex, Foundry) â€” remplace `_BEDROCK` (v2.1.108) |
| `FORCE_PROMPT_CACHING_5M` | Force TTL 5 minutes (v2.1.108) |
| `autoScrollEnabled` | DÃ©sactiver auto-scroll en fullscreen (v2.1.110) |
| Session recap | Active mÃªme sans tÃ©lÃ©mÃ©trie, opt-out `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` (v2.1.110) |
| Advisor Tool | Beta â€” Sonnet consulte Opus mid-generation, 1 seul appel API (9 avril) |
| Claude for Word | Beta publique, sidebar native Mac + Windows (10 avril) |
| MCP 500K chars | Tool result override jusqu'Ã  500K chars (v2.1.110) |
| Auto Mode | Shift+Tab cycle Ask â†’ Plan â†’ Auto. Auto-approve via classifier ML (Opus 4.7, Max/Teams/Enterprise) |
| Hooks MCP direct | `type: "mcp_tool"` â€” hooks invoquent outils MCP directement (v2.1.119) |
| Custom Themes | CrÃ©er themes JSON dans ~/.claude/themes/, plugins peuvent shipper des themes (v2.1.119) |
| /config persiste | Settings /config persistent dans ~/.claude/settings.json avec precedence override (v2.1.119) |
| Fix Opus 4.7 context | CorrigÃ© calcul 200K â†’ 1M natif, plus de faux auto-compact (v2.1.119) |
| DISABLE_UPDATES | Env var bloque tout update y compris claude update manuel (v2.1.119) |
| WSL managed settings | wslInheritsWindowsSettings hÃ©rite settings Windows (v2.1.119) |
| /fork optimisÃ© | Ã‰crit pointeur au lieu de copier toute la conversation (v2.1.119) |
| **Agent View** | **`claude agents` â€” dashboard sessions concurrentes groupÃ©es par Ã©tat (attend input / en cours / terminÃ©). Control plane lancÃ© 11 mai 2026.** |
| **Dynamic Workflows** | **Research preview (v2.1.154, 28 mai 2026) â€” Claude rÃ©dige dynamiquement un script JS d'orchestration lanÃ§ant jusqu'Ã  1000 sous-agents (16 concurrents). Coordination hors-contexte : plan dans le code, rÃ©sultats en variables, seul l'output final revient en contexte. VÃ©rification adversariale intÃ©grÃ©e. DÃ©clenchÃ© par mot-clÃ© dans un prompt OU le rÃ©glage `ultracode`. Requiert v2.1.154+, plans Max/Team/Enterprise. Visible via `/workflows`.** |
| **`ultracode`** | **RÃ©glage (v2.1.160, 2 juin 2026) qui fixe l'effort Ã  `xhigh` ET laisse Claude dÃ©cider automatiquement de lancer un Dynamic Workflow. Depuis v2.1.160, `ultracode` remplace `workflow` comme mot-clÃ© dÃ©clencheur des Dynamic Workflows.** |

## .claude/rules/ (v2.0.64+)

Fichiers `.md` auto-chargÃ©s Ã  chaque session. Alternative modulaire au CLAUDE.md monolithique.

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# RÃ¨gles uniquement pour les fichiers API TypeScript
```

- Sans `paths:` â†’ chargÃ© Ã  chaque session
- Avec `paths:` â†’ chargÃ© uniquement quand Claude lit un fichier matchant
- Sous-dossiers supportÃ©s
- Bon endroit pour : routing agents, workflows, rÃ¨gles obligatoires

## Claude Cowork + Dispatch

| Feature | Description |
|---------|-------------|
| Cowork | Claude Code power pour knowledge workers, dans Claude Desktop |
| Dispatch | Remote control mobile â†’ desktop, taches persistantes et planifiees |
| Agent Teams | Teammates Claude Code independants avec task board + mailbox |
| Skills cross-compat | Meme format SKILL.md partout (Code, Cowork, plugins) |
| Connecteurs | Google Drive, Gmail, Slack, Jira, Linear, M365... |
| agentskills.io | Standard ouvert, skills portables |

Voir `cc-cowork-ref` pour la reference complete.

## Best practices (Boris + Ã©quipe)

- **`/clear` entre tÃ¢ches non liÃ©es** â€” sessions fourre-tout = piÃ¨ge #1
- **`/compact` proactif sous 40-60%** â€” pas attendre l'auto-compact (~83.5%). Tips Thariq via howborisusesclaudecode.com
- **"Document & Clear"** â€” dump plan dans un .md, /clear, nouvelle session
- **CLAUDE.md concis** â€” pour chaque ligne : "si je l'enlÃ¨ve, Ã§a casse ?" sinon couper
- **Hooks = 100% dÃ©terministe. CLAUDE.md = ~80%.** (Boris)
- **VÃ©rification = tip #1** â€” toujours donner Ã  Claude un moyen de vÃ©rifier son output

## Plugins

```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
```

LSPs disponibles pour tous les langages majeurs.

## Flags CLI clÃ©s

| Flag               | Usage                              |
| ------------------ | ---------------------------------- |
| `--worktree <n>`   | Worktree isolÃ©                     |
| `--tmux`           | Session tmux dÃ©diÃ©e                |
| `--bare`           | 10x plus rapide, sans UI           |
| `--agent <n>`      | Agent custom comme agent principal |
| `--resume <id>`    | Reprend une session                |
| `--continue`       | Continue la derniÃ¨re session       |
| `--from-pr <url>`  | Worktree depuis une PR             |
| `--add-dir <path>` | Ajoute un dossier au contexte      |
| `-w`               | Raccourci worktree                 |
| `--teleport`       | Push vers claude.ai/code           |
| `-p <prompt>`      | Mode headless                      |
| `--channels`       | Relay approbation permissions vers mobile (v2.1.110) |
| `--resume <name>`  | Reprend tÃ¢ches planifiÃ©es non expirÃ©es (v2.1.110) |
| `--console`        | Auth login pour Anthropic Console (API billing) (v2.1.119) |

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

## Gotchas

- **Date de rÃ©fÃ©rence** â€” ce fichier intÃ¨gre des Ã©lÃ©ments jusqu'Ã  juin 2026 (v2.1.160). Utiliser `cc-news` si l'info semble datÃ©e ou si la feature demandÃ©e est postÃ©rieure Ã  cette date.
- **`effort: max`** â€” toujours disponible mai 2026 (verbatim docs Anthropic 23 mai), mais prone Ã  l'overthinking. RÃ©server Ã  cas justifiÃ©s ; doctrine forge = `high` par dÃ©faut, `xhigh` pour architect/dev-lead/refactor-pg.

## Apprentissage

AprÃ¨s chaque usage significatif, sauvegarder en mÃ©moire projet les patterns efficaces et erreurs rencontrÃ©es.

_Aucune entrÃ©e pour le moment._
