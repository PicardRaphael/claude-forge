---
name: mcp-wildcard-syntax-officielle
description: "Wildcard mcp__server__* dans tools/allowed-tools = syntaxe officielle Anthropic. Préférer au listing explicite. Token cost négligeable, vrai risque = nombre de MCP servers actifs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f9514081-5b0f-4d0a-934a-9a3a4fee9a3e
---

Pour donner accès à un MCP entier dans `tools:` (agent) ou `allowed-tools:` (skill), utiliser le wildcard `mcp__server__*` au lieu de lister chaque outil.

**Why:** session 24 mai 2026, j'avais listé 3-7 outils MCP forge-brain par agent (search_brain, read_note, get_backlinks...). Raphael : "pourquoi tu fais pas mcp__forge-brain__* en gros". Vérification doc Anthropic = syntaxe officielle verbatim (`mcp__puppeteer__*` dans exemples doc permissions). 36 frontmatters convertis (14 forge + 9 neo_ia + 13 ia_back).

**How to apply:**
- ✅ `tools: ..., mcp__forge-brain__*` (1 token wildcard)
- ❌ `tools: ..., mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__get_backlinks` (restrictif, oublie potentiel)
- Exception : sub-agent vraiment read-only → lister explicite + `disallowedTools: Write, Edit`

**Token cost analysis (Raphael a posé la question)** :
- Wildcard vs liste dans frontmatter `tools:` = ~40 chars diff = négligeable
- Le vrai risque token = **nombre de MCP servers actifs** dans `.mcp.json` / `mcpServers` (Thariq verbatim "50-100 tools → modèle se perd")
- Definitions des outils MCP chargées **une fois** au démarrage server, pas re-chargées à chaque appel agent
- Restreindre `tools:` ne réduit PAS le payload tool defs, seulement l'accès du sub-agent

Source verbatim : [code.claude.com/docs/en/permissions#mcp](https://code.claude.com/docs/en/permissions#mcp).
Vault canonique : sections "AJOUT 24 mai 2026 suite" dans [[comment-creer-agent]] + [[comment-creer-skill]].
