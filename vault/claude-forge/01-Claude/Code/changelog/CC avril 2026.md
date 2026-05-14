---
titre: "CC Avril 2026 — Changelog consolidé"
resume: "Opus 4.7, Auto Mode, CLI binaire natif, Windows sans Git Bash, hooks MCP, ultrareview CLI, 3 memory leak fixes, 100+ bug fixes"
aliases:
  - "CC avril 2026"
  - "changelog avril 2026"
  - "v2.1.110"
  - "v2.1.111"
  - "v2.1.113"
  - "v2.1.114"
  - "v2.1.116"
  - "v2.1.119"
  - "v2.1.120"
  - "v2.1.121"
  - "v2.1.122"
  - "v2.1.123"
domaine: claude-code
type: changelog
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## v2.1.110 (15 avril)

- TUI fullscreen sans scintillement, push notifications mobiles
- PreCompact hook (blocage via exit 2), `--channels` relay permissions
- Remote Control élargi, `--resume`/`--continue` pour tâches planifiées
- MCP tool result override jusqu'à 500K chars

## v2.1.111 (16 avril) — Opus 4.7

- **[[Opus 4.7]]** avec effort `xhigh`
- **Auto Mode** pour Max subscribers (plus besoin de flag)
- `/effort` slider interactif, `/ultrareview` revue cloud
- Windows PowerShell en déploiement progressif

## v2.1.113 (17 avril) — Breaking

- **CLI binaire natif per-platform** (npm path = deprecation notice)
- Sandbox security : `find -exec`/`-delete` plus auto-approuvés
- macOS /private/* traités comme dangerous pour rm
- Subagents stall → fail après 10 min

## v2.1.114 (18 avril)

- Fix crash permission dialog [[Agent Teams]]

## v2.1.116 (20 avril)

- `/resume` **67% plus rapide** sur sessions 40MB+
- MCP startup parallélisé, thinking spinner inline
- Agent frontmatter `hooks:` fire quand `--agent`
- Sandbox auto-allow ne bypass plus dangerous-path check

## v2.1.119 (23 avril) — Auto Mode GA

- **Auto Mode** : Shift+Tab cycle Ask → Plan → Auto, classifier ML
- **Hooks MCP direct** : `type: "mcp_tool"` handler
- Custom themes via `/theme` (JSON dans `~/.claude/themes/`)
- `/usage` fusionne `/cost` + `/stats`
- Fix Opus 4.7 context 200K → 1M natif (faux auto-compact)
- ~80MB RAM en moins au startup, vim visual mode

## v2.1.120 (25 avril)

- **Windows sans Git Bash** — PowerShell fallback quand Git for Windows absent
- `claude ultrareview [target]` — sous-commande CLI non-interactive pour CI
- `${CLAUDE_EFFORT}` dans skills
- Fix `find` épuisant file descriptors (crash macOS/Linux)

## v2.1.121 (28 avril)

- `alwaysLoad: true` MCP — outils toujours disponibles sans ToolSearch
- `claude plugin prune` — supprime deps orphelines
- PostToolUse output replace étendu à TOUS les outils built-in
- Recherche type-to-filter dans `/skills`
- **3 memory leak fixes** : images multi-GB, /usage 2GB, outils long-running
- Vertex X.509 mTLS, OTel spans enrichis

## v2.1.122 (28 avril)

- `ANTHROPIC_BEDROCK_SERVICE_TIER` (default/flex/priority)
- `/resume` trouve sessions par PR URL (GitHub, GitLab, Bitbucket)
- MCP deduplication claude.ai connectors

## v2.1.123 (29 avril)

- Fix OAuth 401 retry loop avec `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`

## Liens

- [[MOC-Claude-Code]]
- [[Opus 4.7]]
