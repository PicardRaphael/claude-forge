---
name: mcp-brain-remote-status
description: "MCP obsidian-brain distant (mcp-brain.neoteem.fr) — v3.2.4, fonctionnel mais pas chargé dans Claude Code CLI, vault_stats absent"
metadata: 
  node_type: memory
  type: project
  originSessionId: 749255b3-3433-483a-9ccb-66bd623f0d4e
---

MCP distant neoteem-brain (`https://mcp-brain.neoteem.fr/mcp`) testé le 2026-05-13 :
- Serveur **opérationnel** : obsidian-brain v3.2.4, protocol Streamable HTTP, 850+ notes
- 9 tools exposés : search_brain, read_note, read_note_by_path, get_backlinks, get_tags, get_property, create_note, append_note, update_property
- `vault_stats` **ABSENT** de cette version (présent sur forge-brain local uniquement)
- Config `~/.claude/.mcp.json` correcte (`type: "url"`) mais tools `mcp__obsidian-brain__*` **non chargés** dans la session Claude Code CLI — à investiguer (handshake initial échoué ?)

**Why:** Le skill `neoteem-brain-dev` (repo neoteem-brain) référence `mcp__obsidian-brain__*` — sans chargement MCP, le skill est inutilisable depuis Claude Code CLI.

**How to apply:** Vérifier au démarrage si les tools `mcp__obsidian-brain__*` sont disponibles avant d'invoquer les skills neoteem-brain-*. Si absent, relancer la session ou diagnostiquer le handshake MCP.

Lié à : [[mcp-obsidian-brain-v2]], [[neoteem-brain-plugin]]
