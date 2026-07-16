---
name: cc-features-ref
description: ALWAYS load when user asks about Claude Code features, capabilities, or what exists. Covers 2026 features: /loop, /schedule, /batch, /simplify, /voice, worktrees, effort, Auto Memory, plugins, LSPs, Agent Teams, CLI flags.
user-invocable: false
---

# Fonctionnalités Claude Code 2026

_Mise à jour : 16 juillet 2026 (intègre v2.1.203-211 ; fenêtre 2.1.161-202 couverte par les notes changelog vault) — utiliser cc-news pour les nouveautés postérieures_

## Slash Commands

| Command                      | Rôle                                         |
| ---------------------------- | -------------------------------------------- |
| `/loop <interval> <skill>`   | Boucle automatique (ex: `/loop 5m /babysit`) |
| `/schedule "<cron>" <skill>` | Planifié jusqu'à 1 semaine                   |
| `/goal <condition>`          | Travaille en autonome jusqu'à condition vraie (ex: `/goal all tests pass`) — modes : interactif, `-p`, Remote Control |
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
| `/team-onboarding`           | Génère guide ramp-up pour nouveaux membres (v2.1.101) |
| `/ultraplan`                 | Auto-provisioning environnement cloud distant (v2.1.101) |
| `/autofix-pr`                | Envoie session+PR au cloud, fixer continue avec contexte (Noah, v2.1.97+) |
| `/tui fullscreen`            | Mode fullscreen sans scintillement (v2.1.110) |
| `/recap`                     | Résumé de session au retour (v2.1.108) |
| `/focus`                     | Focus view — remplace ancien Ctrl+O focus (v2.1.110) |
| `/doctor`                    | Checkup complet diagnose+fix, alias `/checkup` (v2.1.205) ; propose trimming des CLAUDE.md commités (v2.1.206) |
| `/usage`                     | Fusionne /cost + /stats — les deux restent comme alias (v2.1.119) |
| `/theme`                     | Créer/switcher custom themes JSON dans ~/.claude/themes/ (v2.1.119) |

## /loop — La plus puissante

```bash
/loop 5m /babysit          # babysit PRs toutes les 5min
/loop 30m /slack-feedback  # PRs depuis feedback Slack
/loop 1h /pr-pruner        # ferme les PRs stales
/loop /post-merge-sweeper  # commentaires de review manqués
```

Format interval : `5m`, `30m`, `1h`, `6h`, `1d`

### Dynamic Loop (v2.1.110, Noah)

```bash
/loop /babysit-prs          # SANS intervalle = Claude auto-programme le prochain tick
```

Claude utilise `ScheduleWakeup` pour décider dynamiquement quand revérifier (économie de tokens vs polling fixe).

## /schedule

```bash
/schedule "0 9 * * 1-5" /standup-post   # lundi-vendredi 9h
/schedule "0 * * * *" /monitor          # chaque heure
```

## Effort levels

| Niveau   | Effet (Opus 4.8)                                        |
| -------- | -------------------------------------------------------- |
| `low`    | ≈ medium 4.6. Routes simples, schémas, tests unitaires  |
| `medium` | Refactors multi-fichiers, migrations simples             |
| `high`   | **DÉFAUT Opus 4.8.** Migrations complexes, debug cross-layer, code review |
| `xhigh`  | Option agentique/coding long : design API, archi modules, refactors structurels |
| `max`    | Problèmes très durs. Diminishing returns, prone overthinking |

**`high` est le défaut Opus 4.8** ; `xhigh`/`extra`/`max` en option pour les tâches agentiques/coding longues. `high` reste aussi le défaut Sonnet 4.6.
À `xhigh`/`max` : mettre max_tokens à 64k+ minimum.

**Opus 4.8** (`claude-opus-4-8`, sorti 28 mai 2026) — défaut effort = **high** (recommandé), options `extra`/`xhigh`/`max`. Fast mode 3× moins cher qu'avant (vitesse 2.5×). ~4× moins susceptible de laisser passer une faille sans la signaler vs 4.7. C'est désormais le dernier Opus : le défaut forge `opus` = `claude-opus-4-8`.

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

Subagents qui se communiquent directement via task board partagé. Equipe implicite : spawn teammate via le param `name` du tool Agent, plus de `TeamCreate`/`TeamDelete`, `team_name` ignoré.

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
| `PermissionDenied` hook | Se déclenche après refus auto mode, `{retry: true}` (v2.1.89) |
| `PostCompact` hook | Se déclenche après compression du contexte |
| Deferred hooks | `PreToolUse` peut retourner `permissionDecision: "defer"` |
| `InstructionsLoaded` hook | Quand un CLAUDE.md ou rule se charge |
| `hookSpecificOutput.sessionTitle` | Nommer sessions depuis hook `UserPromptSubmit` (v2.1.94) |
| `keep-coding-instructions` | Nouveau frontmatter pour output styles de plugins (v2.1.94) |
| Bedrock via Mantle | `CLAUDE_CODE_USE_MANTLE=1` (v2.1.94) |
| `NO_FLICKER` mode | `CLAUDE_CODE_NO_FLICKER=1` renderer expérimental + support souris (v2.1.89) |
| Opus 4.6 output | 64k tokens par défaut, 128k max (Cat Wu) |
| `--resume` cross-worktree | Reprend sessions d'autres worktrees du même repo (v2.1.94) |
| Write tool 60% faster | Diff computation optimisée sur gros fichiers (v2.1.94) |
| OS CA cert store | Trusted par défaut, `CLAUDE_CODE_CERT_STORE=bundled` pour revenir (v2.1.101) |
| Settings resilience | Typos hook events ne cassent plus settings.json (v2.1.101) |
| Monitor tool | Suit logs/PR par script, remplace le polling agent — gros savings tokens (Noah, v2.1.97+) |
| Managed Agents | Beta publique, sandboxing, SSE, $0.08/session-hour (8 avril) |
| Cowork GA | Tous plans payés, RBAC, OpenTelemetry, usage analytics Enterprise (avril) |
| Dispatch + CC | Lance sessions Claude Code + Computer Use intégré (avril) |
| **Routines** | **Research preview** — Scheduled + API + Webhook automations cloud (v2.1.110) |
| **Desktop Redesign** | Multi-sessions sidebar, terminal intégré, Side Chat `Cmd+;`, 3 modes vue (14 avril) |
| **Push notifications** | Claude envoie notifs push mobiles (Remote Control + config, v2.1.110) |
| **`--channels`** | Relay approbation permissions vers téléphone (v2.1.80) |
| `PreCompact` hook | Avant compression contexte, blocage possible exit code 2 (v2.1.105) |
| `ENABLE_PROMPT_CACHING_1H` | Opt-in cache 1h (API key, Bedrock, Vertex, Foundry) — remplace `_BEDROCK` (v2.1.108) |
| `FORCE_PROMPT_CACHING_5M` | Force TTL 5 minutes (v2.1.108) |
| `autoScrollEnabled` | Désactiver auto-scroll en fullscreen (v2.1.110) |
| Session recap | Active même sans télémétrie, opt-out `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` (v2.1.110) |
| Advisor Tool | Beta — Sonnet consulte Opus mid-generation, 1 seul appel API (9 avril) |
| Claude for Word | Beta publique, sidebar native Mac + Windows (10 avril) |
| MCP 500K chars | Tool result override jusqu'à 500K chars (v2.1.91) |
| Auto Mode | Shift+Tab cycle Ask → Plan → Auto. Auto-approve via classifier ML (Opus 4.7, Max/Teams/Enterprise) |
| Hooks MCP direct | `type: "mcp_tool"` — hooks invoquent outils MCP directement (v2.1.119) |
| Custom Themes | Créer themes JSON dans ~/.claude/themes/, plugins peuvent shipper des themes (v2.1.119) |
| /config persiste | Settings /config persistent dans ~/.claude/settings.json avec precedence override (v2.1.119) |
| Fix Opus 4.7 context | Corrigé calcul 200K → 1M natif, plus de faux auto-compact (v2.1.119) |
| DISABLE_UPDATES | Env var bloque tout update y compris claude update manuel (v2.1.119) |
| WSL managed settings | wslInheritsWindowsSettings hérite settings Windows (v2.1.119) |
| /fork optimisé | Écrit pointeur au lieu de copier toute la conversation (v2.1.119) |
| **Agent View** | **`claude agents` — dashboard sessions concurrentes groupées par état (attend input / en cours / terminé). Control plane lancé 11 mai 2026.** |
| **Dynamic Workflows** | **Research preview (v2.1.154, 28 mai 2026) — Claude rédige dynamiquement un script JS d'orchestration lançant jusqu'à 1000 sous-agents (16 concurrents). Coordination hors-contexte : plan dans le code, résultats en variables, seul l'output final revient en contexte. Vérification adversariale intégrée. Déclenché par mot-clé dans un prompt OU le réglage `ultracode`. Requiert v2.1.154+, plans Max/Team/Enterprise. Visible via `/workflows`.** |
| **`ultracode`** | **Réglage (v2.1.160, 2 juin 2026) qui fixe l'effort à `xhigh` ET laisse Claude décider automatiquement de lancer un Dynamic Workflow. Depuis v2.1.160, `ultracode` remplace `workflow` comme mot-clé déclencheur des Dynamic Workflows.** |
| Screen reader mode | Rendu plain-text opt-in pour lecteurs d'écran (v2.1.208) |
| Auto mode gateways | Sans opt-in sur Bedrock/Vertex/Foundry, désactivable `disableAutoMode` (v2.1.207) |
| `--forward-subagent-text` | + env `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` — inclut le texte des sub-agents (v2.1.211) |
| Always-allow au repo root | Règles « always allow » sauvegardées à la racine du repo, plus au dossier courant (v2.1.211) |
| `CLAUDE_CODE_PROCESS_WRAPPER` | Launcher corporate obligatoire pour tous les self-spawns (v2.1.208) |
| `vimInsertModeRemaps` | Séquences 2 touches en insert-mode, ex. `jj`→Escape (v2.1.208) |
| Transcripts -79x | Taille des transcripts de session réduite jusqu'à 79x, sessions edit-heavy (v2.1.208) |
| Classifier Sonnet 5 | Auto mode — classifier de permissions par défaut Sonnet 5, sessions externes (v2.1.210) |
| Hardening tool Agent | Anti prompt-injection indirecte via contenu lu par un sub-agent (v2.1.210) |

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

## Claude Cowork + Dispatch

| Feature | Description |
|---------|-------------|
| Cowork | Claude Code power pour knowledge workers, dans Claude Desktop |
| Dispatch | Remote control mobile → desktop, taches persistantes et planifiees |
| Agent Teams | Teammates Claude Code independants avec task board + mailbox |
| Skills cross-compat | Meme format SKILL.md partout (Code, Cowork, plugins) |
| Connecteurs | Google Drive, Gmail, Slack, Jira, Linear, M365... |
| agentskills.io | Standard ouvert, skills portables |

Voir `cc-cowork-ref` pour la reference complete.

## Best practices (Boris + équipe)

- **`/clear` entre tâches non liées** — sessions fourre-tout = piège #1
- **`/compact` proactif sous 40-60%** — pas attendre l'auto-compact (~83.5%). Tips Thariq via howborisusesclaudecode.com
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
| `--channels`       | Relay approbation permissions vers mobile (v2.1.110) |
| `--resume <name>`  | Reprend tâches planifiées non expirées (v2.1.110) |
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

- **Date de référence** — ce fichier intègre des éléments jusqu'au 15 juillet 2026 (v2.1.211). Utiliser `cc-news` si l'info semble datée ou si la feature demandée est postérieure à cette date.
- **`effort: max`** — toujours disponible mai 2026 (verbatim docs Anthropic 23 mai), mais prone à l'overthinking. Réserver à cas justifiés ; doctrine forge (option C) = `xhigh` agentique/coding, `high` comparatif/jugement, `medium`/`low` extraction.

## Apprentissage

Après chaque usage significatif, sauvegarder en mémoire projet les patterns efficaces et erreurs rencontrées.

_Aucune entrée pour le moment._
