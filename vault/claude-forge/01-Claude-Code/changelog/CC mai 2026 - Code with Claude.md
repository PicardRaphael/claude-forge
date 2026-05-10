---
titre: "CC Mai 2026 — Code with Claude Drop"
resume: "Desktop GUI, web UI, Plan mode, Auto mode, Security, Dreaming, CLI updates, deprecations Sonnet 4/Opus 4"
aliases:
  - "Code with Claude mai 2026"
  - "CC mai 2026"
  - "claude code may 2026"
  - "CC changelog mai"
  - "code with claude drop"
  - "CC desktop GUI"
  - "v2.1.126"
  - "v2.1.128"
  - "v2.1.129"
  - "v2.1.132"
  - "v2.1.133"
  - "v2.1.136"
domaine: claude-code
type: changelog
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.anthropic.com/news"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Features majeures (6 mai)

- **Claude Code on the web** — coder sans terminal (claude.ai/code)
- **Claude Code on Desktop** — GUI plein ecran avec preview, images, rich outputs
- **Plan mode** — review du plan avant execution
- **Auto mode** (research preview Team) — alternative safe a --dangerously-skip-permissions
- **Claude Security** — scan vulnerabilites repos (public beta Enterprise)
- **Claude Design** — prototypes visuels
- **Claude Mythos Preview** — cybersecurite (Project Glasswing)
- **Dreaming** (research preview) — auto-review sessions passees overnight
- **Routines** (Boris) — "higher-order prompts", automations async

## CLI updates

- `CLAUDE_CODE_FORK_SUBAGENT=1` en sessions non-interactives
- Skill folder protection (skip-permissions ne prompt plus pour .claude/skills/)
- MCP auto-retry (3 tentatives) sur erreur transitoire
- `alwaysLoad` option MCP — skip tool-search deferral
- `claude plugin prune` — nettoyage dependances orphelines
- `/model` picker via gateway /v1/models

## Deprecations

- `TaskOutput` tool deprecie → utiliser Read
- **claude-sonnet-4-20250514** et **claude-opus-4-20250514** retirement API **15 juin 2026**
- 1M context beta Sonnet 4/4.5 retiree

## Metrics

- CC = 4% des commits GitHub publics (Boris, CNBC)
- Rate limits 5h doubles (Pro/Max/Enterprise)
- Suppression throttling peak hours

## Changelog CLI détaillé

### v2.1.126 (1er mai)

- `/model` picker via gateway `/v1/models`, `claude project purge`
- **PermissionDenied hook** (`{retry: true}`)
- **PowerShell principal Windows** (plus Bash par défaut)
- PowerShell 7 détection Microsoft Store/MSI/.NET
- `CLAUDE_CODE_NO_FLICKER=1`, OTel `skill_activated` event

### v2.1.128 (3 mai)

- `/color` random, `/mcp` tool count par serveur
- `EnterWorktree` branch depuis local HEAD (unpushed commits préservés)
- `--plugin-dir` accepte `.zip` archives
- Auto mode hints quand classifier échoue

### v2.1.129 (5 mai)

- `--plugin-url`, `skillOverrides` setting
- **CRITIQUE : cache TTL 1h silencieusement réduit à 5min**
- `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`
- Ctrl+R history = all projects, Ctrl+S pour narrower

### v2.1.132 (6 mai)

- `CLAUDE_CODE_SESSION_ID` env var
- **Fix fuite mémoire 10GB+** (MCP stdout non-drainé)
- Fix fullscreen après sleep/wake, mouse wheel Cursor/VS Code

### v2.1.133 (7 mai)

- `worktree.baseRef` (fresh/head), `$CLAUDE_EFFORT` dans hooks
- `sandbox.bwrapPath`/`sandbox.socatPath` configurables
- `parentSettingsBehavior` (admin), fix parallel sessions 401

### v2.1.136 (8 mai)

- `autoMode.hard_deny` (liste noire auto mode)
- @file picker >100, WSL2 image paste, plan mode fix
- Fix MCP après `/clear`, OAuth refresh fix

## Liens

- [[Code with Claude Conference]]
- [[Managed Agents]]
- [[Cowork GA]]
- [[MOC-Claude-Code]]
- [[CC avril 2026]]
