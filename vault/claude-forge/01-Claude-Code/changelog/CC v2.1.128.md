---
titre: "Claude Code v2.1.128"
resume: "/color random, MCP tool count, plugin zip, EnterWorktree local HEAD, Auto mode hints, focus mode fix"
aliases:
  - "CC 2.1.128"
  - "v2.1.128"
  - "color random"
  - "worktree unpushed"
  - "plugin zip"
  - "auto mode hints"
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
- `/color` sans args = random session color
- `/mcp` montre tool count par serveur + flag 0 tools
- `--plugin-dir` accepte `.zip` plugin archives
- `--channels` fonctionne avec console (API key) auth
- `EnterWorktree` branch depuis local HEAD (unpushed commits plus perdus)
- `workspace` = reserved MCP server name (skip avec warning)
- MCP reconnect : tools re-announced summarizes par prefix (plus de flood)
- Auto mode : hint quand classifier echoue (retry, /compact, --debug)

## Bug fixes
- Focus mode dimming response precedente
- Crash >10MB stdin via `claude -p`
- Parallel shell calls : read-only fail ne cancel plus siblings
- Sub-agent summaries idle = token cost cappe
- `/plugin update` ne detecte jamais nouvelles versions npm
- Terminal OSC 9 notification stray on `/exit`
- Vim Space en NORMAL mode
- `/fast` sur 3P providers fuzzy-match vers skill

## Liens
- Precedent : [[CC v2.1.126]]
- Suivant : [[CC v2.1.129]]
- [[MOC-Claude-Code]]
