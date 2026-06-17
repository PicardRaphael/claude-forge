---
name: mcp-brain-remote-status
description: "MCP obsidian-brain distant (mcp-brain.neoteem.fr) — v3.2.4 sur VM, OPÉRATIONNEL depuis le 3 juin 2026, 14 tools, chargé en Claude Code CLI"
metadata: 
  node_type: memory
  type: project
  originSessionId: 749255b3-3433-483a-9ccb-66bd623f0d4e
---

MCP distant neoteem-brain (`https://mcp-brain.neoteem.fr/mcp`) — **OPÉRATIONNEL** (3 juin 2026, déployé sur VM GCP par DevOps).

- Serveur obsidian-brain v3.2.4, Streamable HTTP, vault 850+ notes sur la VM (`/data/neoteem-brain`)
- **14 tools** exposés : search_brain, read_note, read_note_by_path, read_section, get_backlinks, get_tags, get_property, find_by_symbol, traverse_graph, find_concept_chain, create_note, append_note, update_property, usage_stats
- Chargé en Claude Code CLI après redémarrage session. Test réel validé : `search_brain` renvoie les notes du vault, accents OK (l'erreur d'encodage 0xe9 vue en test = curl Windows Latin-1, PAS le serveur — le vrai client MCP gère l'UTF-8).
- Config unifiée vers la VM dans `~/.claude.json` ET `~/.claude/.mcp.json` (avant : `~/.claude.json` pointait encore `localhost:8090` mort).

**Panne résolue le 3 juin** : le serveur était en crash loop (restart counter ~179, nginx 502). Cause = lancé en transport `stdio` au lieu de `http` (commit `cb06072` du 1er juin avait mis stdio en DÉFAUT pour Claude Desktop). Fix = commit `a516cee` repo `mcp-obsidian-brain` (Bitbucket master) : défaut redevenu `http`, stdio sur `--stdio` explicite. La VM pull le repo (pull=300s) → restart auto = HTTP. Cf [[feedback_mcp_transport_stdio_http_crashloop]].

**How to apply:** Pour basculer un poste sur la VM : enregistrer le MCP sous le nom EXACT `obsidian-brain` (les skills appellent `mcp__obsidian-brain__*`) → URL `https://mcp-brain.neoteem.fr/mcp` type http/url. Redémarrer la session (pas de hot reload). Les skills `neo-brain-*` n'ont AUCUNE URL/port en dur → bascule local↔VM transparente, rien à modifier dedans.

Lié à : [[mcp-obsidian-brain-v2]], [[neoteem-brain-plugin]]
