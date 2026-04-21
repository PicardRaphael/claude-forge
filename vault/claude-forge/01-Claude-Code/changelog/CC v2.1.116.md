---
titre: "Claude Code v2.1.116"
resume: "Resume 67% faster, agent hooks, thinking spinner inline, MCP startup faster"
aliases: ["v2.1.116", "2.1.116"]
domaine: claude-code
type: changelog
derniere-maj: 2026-04-21
auteur: claude
sources: ["https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"]
tags: ["#type/changelog", "#domaine/claude-code"]
---

## Changements
- `/resume` jusqu'à **67% plus rapide** sur sessions 40MB+
- **MCP startup plus rapide** (multi stdio servers parallèles)
- **Thinking spinner inline** ("still thinking", "thinking more", "almost done thinking")
- **Agent frontmatter `hooks:`** fire quand `--agent`
- `/config` search matche valeurs d'options
- `/doctor` ouvrable pendant que Claude répond
- `/reload-plugins` auto-install deps manquantes
- Bash tool hint quand `gh` rate limit GitHub
- Usage tab montre 5h/weekly usage immédiatement
- Scrolling fullscreen fluide VS Code/Cursor/Windsurf via `/terminal-setup`

## Sécurité
- Sandbox auto-allow ne bypass plus dangerous-path check pour rm/rmdir sur `/`, `$HOME`

## Bug fixes
- Fix Devanagari rendering, Ctrl+- undo, Cmd+Left/Right, Ctrl+Z hang wrapper, scrollback duplication, modal overflow, VS Code blank cells, API 400 cache TTL, `/branch` >50MB, `/plugin` doublons, `/update` et `/tui` après worktree

## Liens
- Précédent : [[CC v2.1.114]]
- [[MOC-Claude-Code]]
