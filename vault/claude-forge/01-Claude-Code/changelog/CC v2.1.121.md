---
titre: "Claude Code v2.1.121"
resume: "alwaysLoad MCP, plugin prune, PostToolUse output replace all tools, fullscreen UX, memory leaks fixes"
aliases:
  - "CC 2.1.121"
  - "v2.1.121"
  - "alwaysLoad MCP"
  - "plugin prune"
  - "PostToolUse output"
  - "fullscreen UX CC"
domaine: claude-code
type: changelog
derniere-maj: 2026-04-29
auteur: claude
sources:
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Date : 28 avril 2026

## Nouveautes majeures

### alwaysLoad pour MCP servers
- Option `alwaysLoad: true` dans config MCP server
- Quand active, tous les outils du serveur sautent le tool-search deferral
- Outils toujours disponibles sans besoin de ToolSearch

### Plugin prune
- `claude plugin prune` supprime deps orphelines auto-installees
- `plugin uninstall --prune` cascade la suppression

### PostToolUse output replace etendu
- PostToolUse hooks peuvent maintenant remplacer l'output de TOUS les outils via `hookSpecificOutput.updatedToolOutput`
- Avant : MCP-only. Maintenant : tous les outils built-in aussi

### Recherche dans /skills
- Boite de recherche type-to-filter dans `/skills`
- Trouve une skill sans scroller dans les longues listes

## Ameliorations

### Fullscreen
- Taper dans le prompt ne saute plus au bas de la page apres scroll up
- Dialogues overflow scrollables (arrow keys, PgUp/PgDn, home/end, mouse wheel)
- Cliquer sur une URL longue wrappee ouvre l'URL complete

### SDK / Headless
- `CLAUDE_CODE_FORK_SUBAGENT=1` fonctionne dans sessions non-interactives
- `--dangerously-skip-permissions` ne prompt plus pour `.claude/skills/`, `.claude/agents/`, `.claude/commands/`

### MCP
- MCP servers avec erreur transitoire au startup : auto-retry 3x
- Claude.ai connectors avec meme URL dedupliques
- `mcp_authenticate` supporte `redirectUri` pour custom scheme

### Terminal
- `/terminal-setup` active "Applications in terminal may access clipboard" iTerm2 (pour `/copy` + tmux)
- Tab session title generee dans la `language` configuree
- LSP diagnostic summaries expandent au click/ctrl+o

### Vertex AI
- Support X.509 certificate-based Workload Identity Federation (mTLS ADC)

### OpenTelemetry
- `stop_reason`, `gen_ai.response.finish_reasons`, `user_system_prompt` (gate `OTEL_LOG_USER_PROMPTS`) dans spans LLM

### VSCode
- Voice dictation respecte `accessibility.voice.speechLanguage`
- `/context` ouvre dialog native token usage

### Startup
- Plus rapide : Recent Activity panel retire du splash release-notes

## Bug fixes critiques

### Memory leaks (3 fixes)
- Fix croissance memoire non bornee (multi-GB RSS) avec beaucoup d'images
- Fix `/usage` leakant ~2GB sur machines avec gros historiques
- Fix leak sur outils long-running sans progress event

### Stabilite
- Fix Bash tool devenant inutilisable quand repertoire de demarrage supprime/deplace
- Fix `--resume` crash au startup dans builds externes
- Fix `--resume` echec sur grosses sessions avec ligne transcript corrompue (skip la ligne)
- Fix `thinking.type.enabled is not supported` avec Bedrock inference profile ARNs
- Fix MS 365 MCP OAuth echec avec parametre `prompt` duplique/non supporte
- Fix scrollback duplication (Ctrl+L, tmux, GNOME Terminal, Windows Terminal, Konsole)
- Fix claude.ai MCP connectors disparaissant quand fetch auth transitoire echoue
- Fix "Always allow" rules ne survivant pas aux worker restarts en sessions remote
- Fix `NO_PROXY` non respecte pour tous HTTP clients dans managed-settings.json (native build)
- Fix managed settings approval prompt quittant la session meme quand accepte
- Fix `/usage` "rate limited" apres stale OAuth token (auto-refresh maintenant)
- Fix valeurs enum legacy invalides dans settings.json invalidant tout le fichier
- Fix `/usage` dialog clippee quand no-flicker off
- Fix `/focus` "Unknown command" quand fullscreen renderer off
- Fix grep/find/rg shell wrappers echec quand binary supprime mid-session
- Reduction utilisation file descriptors peak pendant `find`

## Liens

- Precedent : [[CC v2.1.120]]
- Suivant : [[CC v2.1.122]]
- [[MOC-Claude-Code]]
