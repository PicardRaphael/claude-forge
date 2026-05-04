---
titre: "Claude Code v2.1.120"
resume: "Windows sans Git Bash, ultrareview CLI, ${CLAUDE_EFFORT} dans skills, PowerShell fallback"
aliases:
  - "CC 2.1.120"
  - "v2.1.120"
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

## Date : 25 avril 2026

## Nouveautes majeures

### Windows sans Git Bash
- Git for Windows (Git Bash) n'est plus requis
- Quand absent, Claude Code utilise PowerShell comme shell tool
- Simplifie l'installation Windows significativement

### ultrareview CLI
- `claude ultrareview [target]` — sous-commande non-interactive pour CI/scripts
- `--json` pour output brut, exit 0 = succes, exit 1 = echec
- Permet d'integrer ultrareview dans les pipelines CI/CD

### ${CLAUDE_EFFORT} dans skills
- Skills peuvent referencer le niveau d'effort courant avec `${CLAUDE_EFFORT}`
- Permet d'adapter le comportement des skills selon l'effort configure

## Ameliorations

- `AI_AGENT` env var pour subprocesses — `gh` attribue trafic a Claude Code
- Spinner tips masques quand desktop app/skills/agents deja presents
- Hint "use PgUp/PgDn to scroll" quand terminal envoie arrow keys
- Startup plus rapide avec nombreux claude.ai connectors non autorises
- Auto mode denial message linke vers docs config
- `claude plugin validate` accepte `$schema`, `version`, `description` dans `marketplace.json`
- Auto-compact en auto mode affiche `auto` (lowercase, sans token count trompeur)

## Bug fixes

- Fix Esc pendant tool call MCP stdio fermait la connexion serveur (regression 2.1.105)
- Fix `/rewind` et overlays interactifs non repondants apres `claude --resume`
- Fix duplication scrollback terminal en mode non-fullscreen
- Fix faux positifs "Dangerous rm" en auto mode pour commandes multi-lignes pipe+redirect
- Fix menus de selection longs clippes en fullscreen
- Fix Write tool output collapse au lieu d'expand en fullscreen
- Fix slash command picker sautant pendant la frappe
- Fix `/plugin` marketplace echec sur format source non reconnu
- [VSCode] `/usage` ouvre dialog native Account & Usage
- [VSCode] Voice dictation respecte `language` de settings.json
- Fix `find` Bash tool epuisant file descriptors sur gros repertoires (crash host macOS/Linux)
- Fix `DISABLE_TELEMETRY` ne supprimant pas usage metrics pour API/enterprise

## Liens

- [[CC v2.1.119]]
- [[CC v2.1.121]]
