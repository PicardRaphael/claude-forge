---
titre: "MCP multi-client — ce que supportent Claude, ChatGPT et Gemini (juin 2026)"
resume: "État juin 2026 du support MCP des 3 clients majeurs : Claude (Desktop local stdio + Code + remote OAuth), ChatGPT/OpenAI (Responses API remote, Developer Mode read+write, framing remote pas de localhost documenté, OAuth+CIMD, write gaté par confirmation), Google (Gemini Enterprise Agent Platform + ADK supporte MCP shipped, A2A complémentaire). MCP gouverné par la Linux Foundation. Implications pour un serveur cross-client."
aliases:
  - "mcp multi-client"
  - "mcp claude chatgpt gemini"
  - "support mcp openai"
  - "support mcp google gemini"
  - "mcp cross-client"
  - "chatgpt developer mode mcp"
  - "gemini enterprise agent platform mcp"
  - "mcp localhost chatgpt"
derniere-maj: 2026-06-09
auteur: claude
type: technique
sources:
  - "developers.openai.com/api/docs/guides/developer-mode (fetché 2026-06-09 : write par confirmation, framing remote)"
  - "cloud.google.com/blog (ADK supporte MCP — shipped, vérifié 2026-06-09)"
  - "modelcontextprotocol.io/specification/draft/basic/authorization (fetché 2026-06-09)"
  - "openai.github.io/openai-agents-python/mcp"
  - "docs.claude.com (MCP client Claude Desktop + Code)"
tags:
  - "#type/technique"
  - "#domaine/mcp"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# MCP multi-client — Claude, ChatGPT, Gemini

> ⚠️ **Note la plus volatile du dossier.** Le support MCP des clients évolue chaque mois. Statuts datés **juin 2026**. Niveau de preuve indiqué par claim : *(doc primaire fetchée)* = vérifié sur la doc du provider ; *(recherche web)* = digest de recherche, à reconfirmer avant de citer. Au-delà de ~30 jours, revérifier sur la doc officielle du provider AVANT de citer — ne jamais répondre de mémoire.

MCP est devenu le standard de fait : OpenAI l'a adopté, Google l'a adopté, et il est désormais **gouverné par la Linux Foundation** *(recherche web)* (10 000+ serveurs publics actifs début 2026).

---

## Claude (Anthropic)

| Surface | Support MCP |
|---|---|
| **Claude Desktop** | client MCP complet, serveurs **locaux stdio** + remote. Le `fastmcp install` cible Claude Desktop. |
| **Claude Code** | client MCP, serveurs locaux + remote (forge en a 2 : forge-brain port 8091, obsidian-brain). |
| **Remote** | OAuth sur clients Claude (Cloudflare cite Claude comme client de ses serveurs managés via OAuth). |

Claude est le client le plus complet (local + remote, read + write), MCP étant une techno Anthropic.

---

## ChatGPT / OpenAI

OpenAI supporte MCP via deux voies :

### Responses API (développeurs)
- Connexion à des **serveurs MCP remote** supportant **Streamable HTTP** ou HTTP/SSE (legacy). OpenAI recommande Streamable HTTP ou stdio pour les nouvelles intégrations, SSE seulement pour le legacy. *(recherche web)*
- Auth : OAuth, No Auth, ou Mixed. **OAuth avec Client ID Metadata Documents (CIMD)** recommandé pour l'enregistrement client. *(recherche web)*
- Helper SDK : `MCPServerStreamableHttp` (OpenAI Agents SDK).

### Developer Mode (ChatGPT app)
- **Full MCP client support, read ET write**, pour tous les tools. Settings → Apps → Advanced Settings → Developer Mode. **Éligibilité : Pro, Plus, Business, Enterprise, Education** (web). *(doc primaire fetchée)*
- **Le write n'est PAS gaté par le plan** : les actions write sont disponibles sur tous les tiers éligibles, **gardées par une confirmation utilisateur** — verbatim doc : *« Write actions by default require confirmation »*. *(doc primaire fetchée — corrige un digest de recherche qui prétendait à tort Plus/Pro = read-only)*
- « Connectors » **renommés « Apps »** (17 déc 2025) — wrappers MCP maintenus par OpenAI + custom. *(recherche web)*

### ⚠️ Contraintes structurantes ChatGPT
- **Framing remote, localhost non documenté.** La doc Developer Mode décrit systématiquement des « remote MCP server » et ne mentionne **aucun** support localhost (ni autorisé, ni explicitement interdit dans la page fetchée). *(doc primaire fetchée)* Des sources tierces *(recherche web)* affirment que ChatGPT ne peut pas se connecter à localhost et qu'un tunnel est requis (Secure MCP Tunnel / ngrok) — **cohérent avec le framing mais non confirmé verbatim sur la doc**. En pratique : viser remote pour ChatGPT.

---

## Google (Gemini)

- **Vertex AI** rebrandé en **Gemini Enterprise Agent Platform** (22 avril 2026). *(recherche web)*
- **ADK (Agent Development Kit) supporte MCP** — capacité **shipped, pas roadmap**. Verbatim Google Cloud blog : *« ADK also supports Model Context Protocol (MCP), enabling secure connections between your data and agents »* et *« ADK supports MCP, so your agents connect to the vast and diverse data sources… by leveraging the growing ecosystem of MCP-compatible tools »*. *(doc primaire fetchée)*
- ADK stable v1.0 sur **Python, TypeScript, Go, Java** (Python le plus mature). Connecte aussi LangGraph, LangChain, CrewAI, OpenAPI. *(recherche web)*
- **Serveurs MCP managés** : Google adopte MCP à travers ses services (déc 2025) ; un Remote MCP Server managé pour **AlloyDB** est cité GA, et des managés Maps/BigQuery/Compute/Kubernetes sont rapportés. *(recherche web — la page ADK fetchée parle de « connect to », pas de « host »)* À reconfirmer côté hosting managé.
- **Registres** : MCP Servers registry + Agent Registry (catalogue MCP servers/tools/agents). *(recherche web)*

### MCP vs A2A (à ne pas confondre)
Google pousse **A2A (Agent-to-Agent)** comme **complément**, pas concurrent de MCP : *(recherche web)*
- **MCP** = comment un agent se connecte aux **tools et données**.
- **A2A** = comment les agents **communiquent entre eux** à travers les frontières d'orga/plateforme.

---

## Implications pour un serveur MCP cross-client

Pour qu'un serveur fonctionne avec les 3 :

1. **Transport** : **Streamable HTTP** (commun aux 3 en remote). Pas de SSE pur. stdio en bonus pour le local (Claude, et Gemini ADK en dev).
2. **Remote pour viser ChatGPT** : le framing OpenAI est remote — pour ChatGPT, prévoir un serveur remote accessible. Donc OAuth 2.1 + Streamable HTTP dès le départ si cross-client visé.
3. **OAuth 2.1 + CIMD** : recommandé par OpenAI, supporté par Cloudflare/Claude. Dénominateur commun d'auth remote (cf [[mcp-securite-oauth-remote]]). Note : l'autorisation est **OPTIONAL** dans le spec MCP (SHOULD pour HTTP, SHOULD NOT pour stdio → stdio prend les credentials de l'environnement).
4. **JSON Schema portable** : tester les tools sur plusieurs clients — les différences de validation cassent des tools (optional fields, `$ref`) d'un client à l'autre (cf [[mcp-tool-design-scaling]]).
5. **Read-only élargit la surface sans friction** : un serveur read-only évite les confirmations write côté ChatGPT et l'exposition d'actions destructives. Le write reste possible sur tous les tiers éligibles, mais sous confirmation.

---

## ANTI-PATTERNS

- ❌ **Supposer que ChatGPT lit un serveur localhost** — non documenté, le framing est remote ; prévoir un tunnel/remote.
- ❌ **Affirmer « Plus/Pro = read-only »** — FAUX (digest de recherche erroné) : le write est dispo sur tous les tiers éligibles, gardé par confirmation, pas par plan.
- ❌ **Bâtir cross-client en SSE** — déprécié, fragile.
- ❌ **Confondre MCP et A2A** côté Google — MCP = agent↔tools, A2A = agent↔agent.
- ❌ **Affirmer un statut de support de mémoire** — vérifier la doc du provider (cette note se périme vite).

---

## WIKILINKS

- [[MOC-MCP]] — point d'entrée
- [[construire-mcp-production]] — transport Streamable HTTP, le commun cross-client
- [[mcp-securite-oauth-remote]] — OAuth 2.1 + CIMD, dénominateur d'auth remote
- [[mcp-tool-design-scaling]] — portabilité JSON Schema cross-client
- [[mcp-vs-skills-doctrine]] — agentskills.io, la spec skills aussi cross-produit
