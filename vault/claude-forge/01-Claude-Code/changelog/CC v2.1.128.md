---
tags: [claude-code, changelog]
date: 2026-05-04
derniere-maj: 2026-05-06
---
# CC v2.1.128

## Nouveautes
- `/color` sans args = random session color
- `/mcp` montre tool count par serveur + flag 0 tools
- `--plugin-dir` accepte `.zip` plugin archives
- `--channels` fonctionne avec console (API key) auth
- `EnterWorktree` branch depuis local HEAD (unpushed commits plus perdus)
- `workspace` = reserved MCP server name (skip avec warning)
- MCP reconnect : tools re-announced summarizes par prefix (plus de flood)
- Auto mode : hint quand classifier echoue (retry, /compact, --debug)

## Fixes critiques
- Focus mode dimming response precedente
- Crash >10MB stdin via `claude -p`
- Parallel shell calls : read-only fail ne cancel plus siblings
- Sub-agent summaries idle = token cost cappe
- `/plugin update` ne detecte jamais nouvelles versions npm
- Terminal OSC 9 notification stray on `/exit`
- Vim Space en NORMAL mode
- `/fast` sur 3P providers fuzzy-match vers skill

## Liens
- [[CC v2.1.126]]
- [[CC v2.1.129]]
