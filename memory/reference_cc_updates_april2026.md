---
name: cc-updates-april-2026
description: Toutes les mises à jour Claude Code post mars 2026 + best practices Boris/Cat/Lydia/Thariq/Noah. Mise à jour 8 mai 2026.
type: reference
originSessionId: 65cf98c5-1e62-497b-a9f3-568b895cf577
---
## Dépréciations

| Déprécié | Remplacement | Date |
|----------|-------------|------|
| `effort: max` (CLI) | `effort: high` + keyword `ultrathink` | v2.1.91 |
| `budget_tokens` dans thinking (API) | `thinking: {type: "adaptive"}` + `effort` | Opus/Sonnet 4.6 |
| `/output-style` | Un-deprecated (restauré suite feedback) | v2.1.x |
| `TaskOutput` tool | `Read` sur le fichier output | v2.1.x |
| Thinking summaries | Off par défaut. `showThinkingSummaries: true` pour restaurer | v2.1.x |
| `$ARGUMENTS.0` | `$ARGUMENTS[0]` | v2.1.x |
| Plugin manifests `themes`/`monitors` top-level | `"experimental": { ... }` | v2.1.129 (warning) |
| Gateway model discovery auto | Opt-in `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | v2.1.129 |
| Haiku 3 | haiku-4-5 | retiré 19 avril 2026 |
| Sonnet 4 / Opus 4 (2025) | Sonnet 4.6 / Opus 4.6 | retiré 15 juin 2026 |
| 1M context Sonnet 4/4.5 | Sonnet 4.6 (1M natif) | retiré 30 avril 2026 |
| `commands/` directory | `skills/` (commands still work but skills preferred) | v2.1.x |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK` | `ENABLE_PROMPT_CACHING_1H` | v2.1.108 |

## Features clés

| Feature | Commande | Usage |
|---------|----------|-------|
| `/btw` | `/btw question` | Question sidebar sans polluer contexte — COÛT ZÉRO |
| `/branch` | `/branch` | Fork la session courante |
| `/batch` | `/batch migrer X vers Y` | Centaines d'agents parallèles en worktrees |
| `/compact` | `/compact "garder le plan"` | Compaction ciblée avec instructions |
| `/voice` | `/voice` ou hold spacebar | Input vocal |
| `/tui` | `/tui fullscreen` | Mode fullscreen sans scintillement (v2.1.110) |
| `/recap` | `/recap` | Résumé de session au retour (v2.1.108) |
| `/focus` | `/focus` | Focus view (remplace ancien Ctrl+O focus) |
| `--bare` | `claude --bare` | Skip CLAUDE.md/settings/MCPs, 10x plus rapide |
| `--from-pr` | `claude --from-pr 123` | Session liée à un PR GitHub |
| `--add-dir` | `claude --add-dir /path` | Accès repo externe |
| `--channels` | `--channels` | Relay approbation permissions vers téléphone (v2.1.110) |
| `claude -w` | `claude -w` | Raccourci worktree |
| `/powerup` | `/powerup` | Leçons interactives avec démos animées |
| Cloud Auto-Fix | Toggle CI status | Fixe CI et review comments automatiquement |
| Computer Use | `/mcp` pour activer | Claude contrôle l'écran |
| Session sharing | Built-in | Partager conversation par lien |
| Plugin Marketplace | `/plugin` > Discover | Marketplace officiel |
| Routines | Research preview | Scheduled + API + Webhook automations cloud (v2.1.110) |
| Side Chat | `Cmd+;` (Desktop) | Question parallèle sans polluer thread principal |
| Push notifs | Config mobile | Claude envoie push notifications mobile |
| Dynamic Loop | `/loop` (sans intervalle) | Claude auto-programme le prochain tick |
| Auto Mode | Shift+Tab | Ask → Plan → Auto (classifier ML, Opus 4.7) |
| `/usage` | `/usage` | Fusionne /cost + /stats |
| `/theme` | `/theme` | Custom themes JSON |
| Hooks MCP | `type: "mcp_tool"` | Hooks invoquent outils MCP directement |
| `alwaysLoad` MCP | Config MCP server | Skip tool-search deferral, outils toujours dispo |
| `plugin prune` | `claude plugin prune` | Supprime deps orphelines auto-installées |
| PostToolUse output | `updatedToolOutput` | Replace output TOUS outils (plus MCP-only) |
| `ultrareview` CLI | `claude ultrareview` | Non-interactif pour CI/scripts (--json) |
| `${CLAUDE_EFFORT}` | Dans skills | Référence le niveau d'effort courant |
| `/resume` PR URL | Coller URL PR | Trouve session qui a créé le PR |
| Bedrock service tier | `ANTHROPIC_BEDROCK_SERVICE_TIER` | default/flex/priority |
| Web Search GA | API | Plus de beta header requis, dynamic filtering |
| Agent Memory | API beta | `managed-agents-2026-04-01` header |
| Claude Code Web | claude.ai/code | Coder sans terminal |
| Claude Code Desktop GUI | Plein ecran | Preview, images, rich outputs |
| Plan Mode | Plan mode | Review plan avant execution |
| Claude Security | Enterprise beta | Scan vulnerabilites repos |
| Dreaming | Research preview | Auto-review sessions overnight |

## Best practices confirmées (Boris + équipe)

### Context management
- `/clear` entre tâches non liées — sessions "fourre-tout" = piège #1
- `/compact` proactif à 70% — pas attendre l'auto-compact
- `/compact "instructions"` — compaction ciblée préservant ce qui compte
- "Document & Clear" — dump plan dans un .md, /clear, nouvelle session qui lit le .md
- `/btw` pour questions sans polluer le contexte
- Déléguer la recherche aux subagents pour garder le contexte principal propre

### CLAUDE.md
- Doit être CONCIS — pour chaque ligne : "si je l'enlève, Claude fait des erreurs ?" sinon couper
- CLAUDE.md = advisory (~80% compliance). Hooks = déterministe (100%). Boris.
- Compounding : après chaque erreur, `@claude add to CLAUDE.md so you don't make that mistake again`

### Hooks
- JSON sur stdin, pas de variables d'environnement
- Garder rapide — synchrone
- `|| true` pour éviter que les échecs bloquent
- Re-injecter le contexte après compaction avec un hook `Notification` + compact matcher
- **PreCompact** (v2.1.110) : nouveau hook, blocage possible via exit code 2

### Workflow Boris
- 5 terminaux + 5-10 sessions cloud en parallèle
- Chacun dans son worktree git
- "Fleet commander" — ne code pas lui-même
- Plan Mode → itérer → auto-accept → one-shot
- Code principalement à la voix (/voice)
- "Give Claude a way to verify its output" = tip #1
- Thread features cachées (~15 avril) : voice coding, mobile, /batch, worktrees, session hooks

### Skills (Thariq)
- Dossiers avec scripts/assets, pas juste du markdown
- Section Gotchas = contenu le plus important
- Progressive disclosure — pointer vers des fichiers, Claude lit à la demande
- Ne pas être trop spécifique — laisser de la flexibilité
- 1 skill = 1 catégorie propre
- Workflow Figma MCP + Claude Code : sketch rough → Claude flesh out → edit → renvoi CC

## Hooks events récents

| Event | Description |
|-------|-------------|
| `PermissionDenied` | Après refus auto mode. Return `{retry: true}` pour relancer |
| `PostCompact` | Après compression du contexte |
| `PreCompact` | Avant compression, blocage possible exit code 2 (v2.1.110) |
| Deferred hooks | `PreToolUse` peut return `permissionDecision: "defer"` |
| `InstructionsLoaded` | Quand un CLAUDE.md ou rule se charge |

## Settings récents

| Setting | But |
|---------|-----|
| `additionalDirectories` | Accès repos externes permanent |
| `allowedMcpServers` / `deniedMcpServers` | Contrôle MCP granulaire |
| `showThinkingSummaries` | Restaurer les summaries (off par défaut) |
| `disableSkillShellExecution` | Bloquer exécution shell dans les skills |
| `sandbox.network.deniedDomains` | Bloquer des domaines réseau dans sandbox (v2.1.113) |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | Activer Agent Teams |
| `forceRemoteSettingsRefresh` | Fail-closed : bloque démarrage si fetch échoue |
| `cleanupPeriodDays: 0` | INTERDIT — erreur de validation depuis v2.1.92 |
| `ENABLE_PROMPT_CACHING_1H` | Opt-in cache 1h (API key, Bedrock, Vertex, Foundry) |
| `FORCE_PROMPT_CACHING_5M` | Force le TTL 5 minutes |
| `autoScrollEnabled` | Désactiver auto-scroll en fullscreen (v2.1.110) |

## Versions post 12 avril 2026

### v2.1.129 (6 mai)
- `--plugin-url <url>` — charger plugin .zip depuis URL pour la session
- `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` — force synchronized output (Emacs eat, etc.)
- `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` — auto-update Homebrew/WinGet + prompt restart
- `skillOverrides` setting : `off` (cache), `user-invocable-only` (cache du model), `name-only` (collapse description)
- Plugin manifests : `themes`/`monitors` sous `"experimental": { ... }` (warning si top-level)
- Gateway model discovery opt-in via `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`
- Ctrl+R history = all projects par defaut, Ctrl+S pour narrower
- Policy refusal errors incluent API Request ID
- 3P deployments : plus de spinner tips pointant vers surfaces first-party
- OTel : `claude_code.pull_request.count` compte PRs via MCP tools aussi
- Fix **1h prompt cache TTL silently downgraded to 5min** (CRITIQUE)
- Fix `/context` dump ~1.6k tokens gaspilles par appel
- Fix OAuth refresh race after wake-from-sleep (multi-sessions logout)
- Fix agent panel cache quand subagents running (regression 2.1.122)
- Fix `Bash(mkdir *)` allow rules pas honorees pour in-project paths
- Fix cache-miss warning spurious apres `/clear`/compaction
- Fix Ctrl+G blanking conversation history
- Fix `/branch` success sans session id pour `/resume`
- **[VSCode]** Fix `/clear` ne reset pas le contexte

### v2.1.128 (4 mai)
- `/color` sans args = random session color
- `/mcp` montre tool count par serveur + flag 0 tools
- `--plugin-dir` accepte `.zip` plugin archives
- `--channels` fonctionne avec console (API key) auth
- `EnterWorktree` branch depuis local HEAD (unpushed commits plus perdus!)
- `workspace` = reserved MCP server name (skip avec warning)
- MCP reconnect : tools re-announced summarized par prefix (plus de flood)
- Auto mode : hint quand classifier echoue (retry, /compact, --debug)
- Fix focus mode dimming, crash >10MB stdin, parallel shell calls (read-only fail ne cancel plus siblings)
- Fix sub-agent summaries idle token cost cappe
- Fix `/plugin update` ne detecte jamais nouvelles versions npm
- Fix terminal OSC 9 notification stray on `/exit`
- Fix vim Space en NORMAL mode
- Fix `/fast` sur 3P providers fuzzy-match vers skill au lieu de "not available"

### v2.1.126 (1er mai)
- `/model` picker liste modeles depuis gateway `/v1/models` quand `ANTHROPIC_BASE_URL` pointe vers gateway compatible
- `claude project purge [path]` — supprime tout etat CC d'un projet (`--dry-run`, `-y`, `-i`, `--all`)
- `--dangerously-skip-permissions` bypass writes `.claude/`, `.git/`, `.vscode/`, shell configs
- `claude auth login` accepte OAuth code colle (WSL2, SSH, containers)
- **OpenTelemetry** `claude_code.skill_activated` avec `invocation_trigger` (user-slash, claude-proactive, nested-skill)
- Auto mode spinner rouge quand permission check bloque
- **PermissionDenied hook** — fire apres deny auto mode, `{retry: true}` pour retry
- `X-Claude-Code-Session-Id` header API, `.jj`/`.sl` exclus VCS
- `CLAUDE_CODE_NO_FLICKER=1` — alt-screen sans scintillement
- **Windows** : PowerShell shell principal, PS7 Store/MSI/.NET detecte, clipboard EDR-safe, CJK fix
- **Security** : fix `allowManagedDomainsOnly`/`allowManagedReadPathsOnly` ignores sans bloc sandbox
- 20+ bug fixes (images >2000px, OAuth timeout, stream idle, deferred tools fork, Agent SDK hang)

### v2.1.123 (29 avril)
- Fix OAuth authentication 401 retry loop quand `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`

### v2.1.122 (28 avril)
- **`ANTHROPIC_BEDROCK_SERVICE_TIER`** — Env var pour tier Bedrock (`default`, `flex`, `priority`)
- **`/resume` par PR URL** — Coller URL PR dans recherche, trouve la session (GitHub/GitLab/Bitbucket)
- **MCP dedup** — `/mcp` montre connectors cachés par doublon manuel
- OTEL : attributs numériques (nombres pas strings), event `claude_code.at_mention`
- Fix `/branch` forks échouant avec timelines rewound, `/model` effort Bedrock ARN, Vertex structured-output, ToolSearch MCP nonblocking

### v2.1.121 (28 avril)
- **`alwaysLoad`** option MCP server — Skip tool-search deferral, outils toujours disponibles
- **`claude plugin prune`** — Supprime deps orphelines, `uninstall --prune` cascade
- **PostToolUse output replace ALL tools** — `hookSpecificOutput.updatedToolOutput` (était MCP-only)
- **Type-to-filter** dans `/skills`
- **Fullscreen** : scroll up stable, dialogs overflow scrollables, URLs wrappées cliquables
- **`CLAUDE_CODE_FORK_SUBAGENT=1`** fonctionne en non-interactif
- **`--dangerously-skip-permissions`** ne prompt plus pour `.claude/skills/`, `.claude/agents/`, `.claude/commands/`
- **MCP retry** 3x sur erreur transitoire startup, connectors dedupliqués
- **Vertex AI** X.509 mTLS ADC
- **OTEL** `stop_reason`, `gen_ai.response.finish_reasons`, `user_system_prompt`
- **3 memory leak fixes** : images multi-GB, /usage ~2GB, long-running tools
- Fix Bash tool inutilisable après dir supprimé, --resume crash/corrupt, scrollback duplication

### v2.1.120 (25 avril)
- **Windows sans Git Bash** — PowerShell comme fallback shell tool
- **`claude ultrareview [target]`** — Sous-commande non-interactive pour CI/scripts (`--json`, exit codes)
- **`${CLAUDE_EFFORT}`** — Skills peuvent référencer le niveau d'effort courant
- **`AI_AGENT`** env var pour `gh` attribution
- Auto-compact auto mode affiche `auto` (lowercase)
- Fix Esc fermant connexion MCP stdio, /rewind après --resume, faux positifs "Dangerous rm" auto mode, find file descriptors exhaustion

### v2.1.119 (23 avril)
- **Auto Mode** — Shift+Tab cycle Ask → Plan → Auto. Auto-approve via classifier ML (Opus 4.7, Max/Teams/Enterprise)
- **Hooks MCP direct** — `type: "mcp_tool"` invoque outils MCP depuis hooks
- **Custom Themes** — `/theme`, JSON dans `~/.claude/themes/`, plugins shipper themes
- **`/usage`** — Fusionne `/cost` + `/stats` (alias restent)
- **`/config` persiste** — Settings dans `~/.claude/settings.json` avec precedence override
- **Vim visual modes** (v, V)
- **`--console`** flag sur `claude auth login` pour Anthropic Console
- **Plugin install** sur existant → installe deps manquantes
- **Fix Opus 4.7 context** — Corrigé 200K → 1M natif (plus de faux auto-compact)
- **`/fork` optimisé** — Pointeur au lieu de copie complète
- **~80MB RAM** en moins startup repos 250k+ fichiers
- **`DISABLE_UPDATES`** env var — Bloque tout update y compris manuel
- **WSL** hérite managed settings Windows via `wslInheritsWindowsSettings`
- Fix credential save crash Linux/Windows, PowerShell permission checks, Bedrock 400 Opus 4.7

### v2.1.116 (20 avril)
- **`/resume` 67% plus rapide** sur sessions 40MB+
- **MCP startup plus rapide** (multi stdio servers parallèles)
- **Thinking spinner inline** ("still thinking", "thinking more", "almost done thinking")
- **Agent frontmatter `hooks:`** fire quand `--agent`
- `/config` search matche valeurs d'options
- `/doctor` ouvrable pendant que Claude répond
- `/reload-plugins` auto-install deps manquantes
- Bash tool hint quand `gh` rate limit GitHub
- Usage tab montre 5h/weekly usage immédiatement
- Scrolling fullscreen fluide VS Code/Cursor/Windsurf via `/terminal-setup`
- **Sécurité** : sandbox auto-allow ne bypass plus dangerous-path check pour rm/rmdir sur `/`, `$HOME`
- Fix Devanagari rendering, Ctrl+- undo, Cmd+Left/Right, Ctrl+Z hang wrapper, scrollback duplication, modal overflow, VS Code blank cells, API 400 cache TTL, `/branch` >50MB, `/plugin` doublons, `/update` et `/tui` après worktree

### v2.1.114 (18 avril)
- Fix crash permission dialog Agent Teams

### v2.1.113 (17 avril) — **Breaking**
- **CLI spawn binary natif per-platform** au lieu de bundled JS (npm path = deprecation notice)
- `sandbox.network.deniedDomains` setting
- Shift+Up/Down scroll fullscreen
- Ctrl+A/Ctrl+E = début/fin ligne logique (readline)
- Windows: Ctrl+Backspace = delete mot précédent
- URLs longues restent cliquables quand elles wrappent
- `/loop` Esc annule les wakeups
- `/extra-usage` fonctionne depuis Remote Control
- Remote Control supporte `@`-file autocomplete
- `/ultrareview` plus rapide (checks parallélisés, diffstat, animation)
- Subagents qui stall = fail après 10 min au lieu de hang
- **Sécurité** : macOS /private/* dangerous pour rm. Bash deny rules matchent `env`/`sudo`/`watch`/`setsid` wrappers. `find -exec`/`-delete` plus auto-approuvés. 22 bug fixes

### v2.1.112 (16 avril) — Bugfix
- Fix "claude-opus-4-7 is temporarily unavailable" en auto mode

### v2.1.111 (16 avril) — Opus 4.7
- **Claude Opus 4.7** avec niveau d'effort `xhigh` (entre `high` et `max`)
- **Auto mode** disponible pour Max subscribers avec Opus 4.7 (plus besoin de `--enable-auto-mode`)
- `/effort` ouvre un slider interactif sans arguments
- `/ultrareview` — revue de code parallèle dans le cloud
- `/less-permission-prompts` — skill pour gérer les allowlists de permissions
- Thème "Auto (match terminal)" via `/theme`
- **Windows PowerShell** en déploiement progressif
- Commandes bash read-only avec glob ne déclenchent plus de prompts de permission
- Suggestions de typo pour sous-commandes proches
- Fichiers plan nommés d'après le prompt (plus de mots aléatoires)

### v2.1.110 (15 avril) — Release majeure
- **`/tui fullscreen`** — Mode fullscreen sans scintillement
- **Push notifications** mobiles (Remote Control + config "Push when Claude decides")
- **`autoScrollEnabled`** — Désactiver auto-scroll en fullscreen
- **Ctrl+G** — Montre dernière réponse Claude en commentaire dans éditeur externe
- **Ctrl+O** — Bascule uniquement normal ↔ verbose. Focus view → `/focus`
- **`--resume`/`--continue`** — Ressuscite tâches planifiées non expirées
- **Remote Control élargi** : `/autocompact`, `/context`, `/exit`, `/reload-plugins` depuis mobile/web
- **Write tool amélioré** — Informe quand on édite le diff IDE avant d'accepter
- **Bash timeout** — Applique timeout max documenté
- **SDK/headless** — Lit `TRACEPARENT`/`TRACESTATE` pour distributed tracing
- **Session recap** — Active même sans télémétrie. Opt-out `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0`
- **`/plugin` amélioré** — Favoris en haut, items désactivés cachés, `f` pour favoriser
- **`/doctor` amélioré** — Alerte MCP dupliqués cross-scopes
- **PreCompact hook** — Blocage possible via exit code 2
- **`--channels`** — Relay approbation permissions vers téléphone
- **MCP tool result** — Override jusqu'à 500K chars
- **Background monitors** pour plugins
- **25+ fixes** : MCP hanging, plugin deps, skills `disable-model-invocation`, PermissionRequest hooks + `updatedInput`, garbled macOS Terminal.app, Remote Control session renames, etc.

### v2.1.109 (15 avril)
- Indicateur de thinking étendu avec hint de progression rotatif

### v2.1.108 (14 avril)
- **`ENABLE_PROMPT_CACHING_1H`** — Nouveau env var cache 1h (remplace `_BEDROCK`)
- **`FORCE_PROMPT_CACHING_5M`** — Force TTL 5 min
- **`/recap`** — Feature recap de session
- **Skill Tool** — Découvre et invoque slash commands built-in (`/init`, `/review`, `/security-review`)
- **`/model`** — Alerte avant changement mid-conversation (cache invalide)
- **`/resume`** — Défaut = sessions du dossier courant, `Ctrl+A` pour tout voir
- **Erreurs améliorées** — Rate limits serveur vs limites plan distinguées, lien status.claude.com

### Routines (14 avril) — Research Preview
- Automatisations cloud sans laptop allumé
- **3 types** : Scheduled (cron intelligent), API (webhook HTTP), GitHub (PR, commits, issues)
- **Quotas** : Pro 5/jour, Max 15/jour, Team/Enterprise 25/jour
- Alternative cloud à `/schedule` + Task Scheduler local

### Desktop Redesign (14 avril)
- **Multi-sessions** — Sidebar pour gérer plusieurs sessions en parallèle
- **Outils intégrés** — Terminal, éditeur, diff viewer, preview HTML/PDF
- **Side Chat** `Cmd+;` — Question annexe sans polluer le thread
- **3 modes de vue** — Verbose, Normal, Summary
- **Auto-archive** quand PR mergée/fermée
- **Plugin parity CLI** — Plugins identiques Desktop et CLI
- **SSH Mac** — Support étendu (était Linux only)
- **Mac + Windows** — Linux arrive bientôt

## Versions 3-12 avril 2026

### v2.1.101 (10 avril) — Release majeure
- **`/team-onboarding`** — Guide ramp-up nouveaux membres
- **OS CA cert store trusted** — Proxies TLS enterprise just work
- **`/ultraplan`** — Auto-provisioning cloud distant
- **`disableSkillShellExecution`** — Bloque shell dans skills
- **Security fix** : command injection dans POSIX `which` fallback
- **Memory leak fix** : sessions longues retenaient copies historiques
- Nombreux bug fixes (voir mémoire complète)

### v2.1.97 (8 avril) — 46 changements
- **Ctrl+O Focus view** NO_FLICKER
- **`/agents` live counter** `● N running`
- **`refreshInterval` status line**
- **Fix crash subagents parallèles** (critique Agent Teams)
- **~3× plus rapide** suggestions `@` mention
- Voir mémoire pour liste complète

### v2.1.94-96 (7 avril)
- Effort par défaut `medium` → `high`
- Support Bedrock via Mantle
- Write tool diff 60% plus rapide
- `/vim` et `/tag` supprimés (v2.1.92)

## Plateforme

- **Cowork GA** (9 avril) : tous plans payés, RBAC, OpenTelemetry, Computer Use Pro+Max
- **Managed Agents** (8 avril) : beta publique, $0.08/session-hour, Notion/Rakuten/Asana
- **Dispatch** : sessions Claude Code (pas juste Cowork), Computer Use intégré
- **Plugins marketplace** : 101 officiels, 2400+ communauté
- **Advisor Tool** (9 avril) : beta publique, Sonnet consulte Opus mid-generation, 1 seul appel API
- **Claude for Word** (10 avril) : beta publique, sidebar native Mac + Windows
- **Agent Memory** (avril) : public beta sous `managed-agents-2026-04-01`
- **Web Search GA** : plus de beta header requis, dynamic filtering via code execution
- **Project Glasswing** : Claude Mythos Preview pour zero-day autonome, $100M credits
- **Managed Agents update** (6 mai) : Multi-agent orchestration, Outcomes (criteres succes), Dreaming (research preview)
- **Cowork update** (mai) : Connecteur Zoom, add-ins Microsoft 365, templates finance, Microsoft Copilot Cowork integre Opus 4.7
- **Google $10B** (24 avril) : + $30B conditionnel, valorisation $350B
- **Claude Security** (1er mai) : public beta Enterprise, scans schedulés, directory-level, triage, export CSV/MD, webhooks Slack/Jira. Partenaires : CrowdStrike, Microsoft Security, Palo Alto, SentinelOne, Wiz
- **Bun acquisition** : Jarred Sumner + équipe rejoignent Anthropic. Bun reste open source MIT. Infrastructure CC/Agent SDK
- **$1.5B JV** (5 mai) : Blackstone + Goldman Sachs + Hellman & Friedman — firme enterprise AI-native mid-market
- **Revenue** : ARR >$30B (vs $9B fin 2025). CC seul = $1B ARR en 6 mois
- **Funding** : round en cours, valorisation potentielle $900B, $50B capital
- **Computer Use dans CC** : `/mcp` > computer-use, contrôle souris/clavier, apps spécifiques
- **Excel & PowerPoint** : Skills support, context sharing (Felix)
- **Voice STT** : 10 nouvelles langues (20 total), incl. russe, polonais, turc, suédois

## Équipe (post 12 avril)

- **Cat Wu** (16 avril) : Opus 4.7 est un modèle "delegation" — contexte complet upfront, effort `xhigh`
- **Boris** (16 avril) : 6 tips post-Opus 4.7 — Auto Mode parallèle, `/fewer-permission-prompts`, Recaps, Focus Mode, effort levels, `/go` skill (E2E + simplify + PR auto)
- **Noah** (~15-16 avril) : Dynamic Looping (`/loop` sans intervalle), cloud auto-fix suit PRs automatiquement, **Routines** lancées (14 avril)
- **Thariq** (~14-15 avril) : Workflow Figma MCP + Claude Code, `/rewind`, différence `/compact` vs `/clear`, seuil auto-compact configurable. Article LinkedIn "Lessons from Building Claude Code: How We Use Skills" viral
- **Lydia** (21 avril) : Workshop Frontend Masters (CLAUDE.md, permissions, skills, MCP). Annonce Agent Teams (research preview) + Session Sharing (web/desktop/mobile). Investigue usage limits
- **Jarred** (~mi-avril) : Controverse cache TTL (1h → 5min). Anthropic confirme quota drain pas directement causé
- **Amanda Askell** (mi-avril) : Mise à jour system prompt claude.ai "en collaboration avec Claude"
- **Alex Albert** (avril) : "L'expérience Claude Code pour tous les knowledge workers arrive"
- **Boris** (23 avril) : Postmortem qualité CC — 3 causes identifiées (effort medium, cache bug, verbosity prompt), fix v2.1.116+, usage limits reset
- **Cat Wu** (23 avril) : Interview Lenny Rachitsky — product velocity, PM role shifting, future of work
- **Felix** (16 avril) : Bluetooth API pour Claude Cowork/Code Desktop (makers & developers)
- **Felix** (27 mars) : PowerShell natif dans CC. Computer Use dans CC (30 mars). Dispatch sur tous plans Teams. Cowork Windows on Arm.
- **Lydia** (30 mars) : Enquete usage limits trop vite atteints. Claude for Open Source (6 mois Max 20x gratuit maintainers)
- **Boris** : Code Review feature (equipe d'agents par PR). 259 PRs/30 jours tout via CC+Opus. Podcast Lenny's + Lightcone Pod
- **Thariq** : Talk Code with Claude Extended 7 mai "eval engineers vs eval sets"
- **Thariq** (~30 avril) : Article architecture prompt caching — "pour un agent long-running, le caching est l'architecture de base, pas une optimisation"
- **Felix** (mai) : Computer Use dans Claude Code (`/mcp` > computer-use). Excel & PowerPoint avec Skills. Dispatch lance sessions CC
- **Lydia** (mai) : Best Practices ajoutées aux docs officielles CC, invite communauté à partager patterns
- **Boris** (6 mai) : Keynote Code with Claude SF. 100% code par CC depuis nov. 2025. "Build for the model of 6 months from now". Routines = "higher-order prompts". CC = 4% des commits GitHub publics (CNBC interview)
- **Cat Wu** (6 mai) : Keynote — Claude Code on the web, Plan mode, Dreaming (research preview), doublement rate limits 5h, suppression throttling peak hours
- **Thariq** (7 mai) : Talk Extended SF "Designing multi-agent systems: when to split, when to sandbox, what to ship"
- **Alex Albert** (6 mai) : Talk "The capability curve" — CC pour tous les knowledge workers
- **Jarred** (5 mai) : Explore port Bun Zig→Rust (no-AI policy Zig problematique pour Anthropic)

## Incidents

- **23 avril** : Postmortem officiel — 3 regressions quality mars-avril, fix v2.1.116+, usage limits reset
- **21 avril** : Test retrait Claude Code du plan Pro $20/mois (2% nouveaux signups, revert rapide)
- **~23 avril** : Sessions web CC perdent accès connectors MCP claude.ai
- **15 avril 2026** : Panne ~3h (10h53-13h42 ET), claude.ai + API + CC. 5100+ reports Down Detector.
- **31 mars** : Leak code source 512K lignes TS via source map npm v2.1.88

## Événements

- **19 avril** : Retirement Haiku 3 ✅ effectif
- **21 avril** : Workshop Lydia Hallie, Frontend Masters ✅ effectif
- **23 avril** : Opus 4.7 modèle par défaut Enterprise ✅ effectif
- **24 avril** : Google investit $10B dans Anthropic ($350B valorisation)
- **30 avril** : Retirement 1M context Sonnet 4/4.5 ✅ effectif
- **1er mai** : Claude Security beta publique Enterprise
- **1er mai** : CC v2.1.126
- **4 mai** : CC v2.1.128
- **6 mai** : CC v2.1.129 + Code with Claude SF (1ere conference dev Anthropic)
- **7 mai** : Code with Claude Extended SF (indie devs/founders)
- **19 mai** : Code with Claude Londres
- **1er juin** : GitHub Copilot billing migration AI Credits + model deprecations
- **10 juin** : Code with Claude Tokyo
- **15 juin** : Retirement Sonnet 4 / Opus 4 (2025)
