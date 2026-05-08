---
titre: "Claude Code v2.1.129"
resume: "Plugin URL, sync output, auto-update package manager, skillOverrides, fix cache TTL 1h→5min critique"
aliases:
  - "CC 2.1.129"
  - "v2.1.129"
  - "plugin URL"
  - "sync output"
  - "skillOverrides"
  - "cache TTL fix CC"
domaine: claude-code
type: changelog
derniere-maj: 2026-05-06
auteur: claude
sources:
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Changements

## Nouveautes
- `--plugin-url <url>` charger plugin .zip depuis URL
- `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` force synchronized output (Emacs eat)
- `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` auto-update Homebrew/WinGet + prompt restart
- `skillOverrides` setting : `off`, `user-invocable-only`, `name-only`
- Plugin manifests : `themes`/`monitors` sous `"experimental": { ... }` (warning si top-level)
- Gateway model discovery opt-in `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`
- Ctrl+R history = all projects par defaut, Ctrl+S pour narrower
- Policy refusal errors incluent API Request ID
- OTel `claude_code.pull_request.count` compte PRs via MCP tools

## Bug fixes
- **1h prompt cache TTL silently downgraded to 5min** (CRITIQUE)
- `/context` dump ~1.6k tokens gaspilles par appel
- OAuth refresh race after wake-from-sleep (multi-sessions logout)
- Agent panel cache quand subagents running (regression 2.1.122)
- `Bash(mkdir *)` allow rules pas honorees in-project
- Cache-miss warning spurious apres `/clear`/compaction
- Ctrl+G blanking conversation history
- `/branch` success sans session id pour `/resume`
- **[VSCode]** `/clear` ne reset pas le contexte

## Liens
- Precedent : [[CC v2.1.128]]
- [[MOC-Claude-Code]]
