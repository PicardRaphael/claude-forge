---
name: mcp-wildcard-syntax-officielle
description: "Wildcard mcp__server__* dans tools/allowed-tools = syntaxe officielle Anthropic. Préférer au listing explicite. Token cost négligeable, vrai risque = nombre de MCP servers actifs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f9514081-5b0f-4d0a-934a-9a3a4fee9a3e
---

Cf [[comment-creer-agent]] section "AJOUT 24 mai 2026 (suite)" (doctrine : wildcard `mcp__server__*` = syntaxe officielle Anthropic à préférer au listing explicite ; exception read-only ; analyse token cost = négligeable en frontmatter, vrai risque = nombre de MCP servers actifs). Voir aussi [[comment-creer-skill]].

**Cas empirique(s) :**

- Session 24 mai 2026 : j'avais listé 3-7 outils MCP forge-brain par agent (search_brain, read_note, get_backlinks...). Raphael : "pourquoi tu fais pas mcp__forge-brain__* en gros". Vérification doc Anthropic = syntaxe officielle verbatim (`mcp__puppeteer__*` dans exemples doc permissions). **36 frontmatters convertis (14 forge + 9 neo_ia + 13 ia_back).**
- Token cost analysis (Raphael a posé la question) : wildcard vs liste dans `tools:` = ~40 chars diff = négligeable. Le vrai risque token = nombre de MCP servers actifs dans `.mcp.json` (Thariq verbatim "50-100 tools → modèle se perd"). Définitions des outils MCP chargées une fois au démarrage server, pas re-chargées à chaque appel agent.
- Session 6 juin 2026 — `Plugin:*` invalide dans `permissions.allow` (settings.json user-scope) : le harness skipppe silencieusement cette entrée et /doctor la signale. **La règle** : dans `allow`, seul `mcp__<serveur>__*` est accepté (préfixe littéral + wildcard sur l'outil). Les scopes génériques (`Plugin:*`, `Skill:*`) ne sont autorisés qu'en `deny`/`ask`. Fix = supprimer la ligne. Les plugins s'auto-approuvent via `enableAllProjectMcpServers` ou marketplace, pas via ce pattern.
