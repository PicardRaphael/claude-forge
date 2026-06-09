---
titre: "MOC MCP — construire des serveurs MCP de qualité production"
resume: "Point d'entrée du dossier MCP forge : protocole, transports, SDK TS/Python, design des tools, scaling (le problème trop-de-tools), sécurité OAuth 2.1, multi-client Claude/ChatGPT/Gemini, maintenance. État vérifié juin 2026, sources primaires."
aliases:
  - "MOC MCP"
  - "dossier MCP"
  - "construire un MCP"
  - "créer un serveur MCP"
  - "MCP de production"
  - "hub MCP forge"
derniere-maj: 2026-06-09
auteur: claude
type: moc
sources:
  - "modelcontextprotocol.io/specification/2025-11-25"
  - "blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate"
  - "anthropic.com/engineering/code-execution-with-mcp"
  - "developers.cloudflare.com/agents/model-context-protocol"
  - "github.com/github/github-mcp-server"
tags:
  - "#type/moc"
  - "#domaine/mcp"
  - "#domaine/claude-code"
---

# MOC MCP — construire des serveurs MCP de qualité production

> Point d'entrée du dossier MCP forge. Objectif : créer des serveurs MCP **parfaits** — peu de tools, sécurisés, fonctionnant cross-client (Claude, ChatGPT, Gemini), en TypeScript ou Python. État vérifié **juin 2026** sur sources primaires (le sujet bouge vite, ne jamais répondre de mémoire pré-cutoff).

---

## Le dossier en 1 phrase

Un bon MCP n'expose **pas** ton API entière ; il expose **peu de tools bien conçus orientés objectif**, sécurisés par OAuth 2.1 (jamais de token passthrough), et scale par **découverte dynamique / code execution** plutôt qu'en empilant 100 tools qui noient le modèle.

---

## Notes du dossier

### Doctrine arbitrage (préalable)
- [[mcp-vs-skills-doctrine]] — MCP connecte la donnée, Skills enseignent le how-to, Bash explore. **Lire en premier** : quand un MCP est-il seulement le bon outil.

### Construire
- [[construire-mcp-production]] — recipe TS + Python à parité : stack, structure projet, transport, lifecycle, du minimal au production-ready.
- [[mcp-tool-design-scaling]] — **note cœur** : design des tools (JSON Schema, annotations readOnly/destructive), le problème « trop de tools » et ses réponses 2026 (Code Execution, Tool Search, Dynamic Discovery, Codemode).

### Sécuriser
- [[mcp-securite-oauth-remote]] — OAuth 2.1 Resource Server, confused deputy, token passthrough interdit, RFC 8707, lethal trifecta, patterns Cloudflare.

### Distribuer
- [[mcp-multi-client-claude-chatgpt-gemini]] — ce que supportent RÉELLEMENT les 3 clients majeurs en juin 2026 (transport, remote vs local, OAuth, write).

### Maintenir
- Section « Maintenance / debug / observabilité » dans [[construire-mcp-production]] — MCP Inspector, evals, logging, versioning.

### Appliqué forge (exemples vivants)
- [[mcp-vault-llm-design]] — design d'un MCP qui sert un vault à un LLM (forge-brain, 21 outils, FastMCP, SQLite FTS5). Cas concret de tout ce dossier.
- [[architecture-cerveau-obsidian-mcp]] — l'archi cerveau Obsidian + MCP de bout en bout.
- [[reference-technique-stack-ia]] — section MCP au niveau protocole dans la stack IA globale.

---

## Les 5 décisions structurantes (résumé)

| Décision | Réponse 2026 vérifiée |
|---|---|
| **Transport** | `stdio` en local, **Streamable HTTP** en remote. SSE déprécié (spec 2025-03-26), gardé pour rétrocompat seulement. |
| **SDK Python** | **FastMCP 3.0** (GA 18 fév 2026, `PrefectHQ/fastmcp`) par défaut ; SDK officiel `mcp` pour contrôle bas niveau. |
| **SDK TypeScript** | `@modelcontextprotocol/sdk` v1.x (prod ; v2 pre-alpha Q3 2026). |
| **Nombre de tools** | Peu, orientés objectif. Au-delà → découverte dynamique / code execution, jamais 50-100 chargés upfront. |
| **Sécurité remote** | OAuth 2.1, audience binding (RFC 8707), **token passthrough INTERDIT**, PKCE S256. |

---

## Gotcha transverse — le sujet bouge vite

État du spec au moment de l'écriture : **courant = 2025-11-25**, **RC = 2026-07-28** (headline : MCP devient *stateless* au niveau protocole, schemas → JSON Schema 2020-12). Toute note de ce dossier porte une `derniere-maj` ; au-delà de ~30 jours, revérifier sur `modelcontextprotocol.io` avant de citer un statut.

---

## Wikilinks

- [[mcp-vs-skills-doctrine]]
- [[construire-mcp-production]]
- [[mcp-tool-design-scaling]]
- [[mcp-securite-oauth-remote]]
- [[mcp-multi-client-claude-chatgpt-gemini]]
- [[mcp-vault-llm-design]]
- [[architecture-cerveau-obsidian-mcp]]
- [[reference-technique-stack-ia]]
- [[Context Engineering]]
