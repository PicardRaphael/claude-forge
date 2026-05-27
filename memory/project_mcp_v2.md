---
name: mcp-obsidian-brain-v2
description: MCP v2 SQLite FTS5, repo separe, 5 plugins Cowork, VM serveur, benchmark 24/24
type: project
originSessionId: 0189dcca-363c-4f81-ae4e-e4860a4bfc24
---
MCP obsidian-brain v2 deploye — remplace la CLI Obsidian par SQLite FTS5 autonome.

**Why:** La CLI Obsidian necessitait Obsidian ouvert sur chaque poste. Le MCP v2 tourne sur un serveur VM, accessible via VPN par tous les postes Claude Code et Claude Desktop sans installation.

**How to apply:**
- Repo MCP : `neot-v2/mcp-obsidian-brain` (Bitbucket)
- Vault : `neot-v2/neoteem-brain` (inchange)
- 38 tests, 836 notes indexees en 3.35s
- BM25 pondere (nom x10, aliases x8, contenu x1), stop words FR, snippets FTS5 natifs
- Benchmark parite 24/24 PASS
- Git sync : pull main/5min, commit par branche mcp/<user>, push/30min
- 5 plugins Cowork (dev, dev-admin, dev-ia, support, support-admin)
- 4 skills Claude Chat (dev, dev-admin, support, support-admin)
- Budget reads : 3-4 sur tous les flux (dev + support)
- Config postes via settings orga, zero install par poste
- CLI Obsidian reste disponible en local (skill obsidian-cli gardee)
- Spec : `claude-forge/docs/superpowers/specs/2026-04-29-mcp-obsidian-brain-v2-design.md`
- Plan : `claude-forge/docs/superpowers/plans/2026-04-29-mcp-obsidian-brain-v2.md`
- Deploiement VM : voir README du repo MCP (systemd + nginx)
