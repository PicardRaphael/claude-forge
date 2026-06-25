---
name: cowork-mcp-stdio-marche
description: MCP local stdio MARCHE en Cowork (retour terrain Raphael) — la vraie limite est le transport (HTTP-localhost échoue), pas local-vs-cloud
metadata:
  type: feedback
---

Un MCP **local en stdio** (`command` + `args`) **marche en Cowork** : le client lance le process localement (comme Desktop Chat), donc aucun accès réseau à `localhost` n'est requis. Vérifié terrain par Raphael (forge-brain en stdio sur le Cowork d'un PO puis le sien, via `mcp-forge-brain/start_stdio.py`, `transport="stdio"`).

**Why:** la note vault `[[mcp-local-cowork-vs-claude-code]]` (1er juin) affirmait « localhost impossible en Cowork → HTTPS public requis ». C'était une **sur-généralisation depuis le seul cas HTTP-localhost**. La vraie distinction est le TRANSPORT : stdio ✅ (process local) · HTTP `localhost:port` ❌ (la VM cloud ne joint pas ta machine) · HTTP/HTTPS public ✅. Note amendée le 24 juin.

**How to apply:** ne JAMAIS re-sortir le claim « MCP local impossible en Cowork » de façon catégorique. Pour un MCP local en Cowork → proposer **stdio** d'abord (pas de tunnel HTTPS nécessaire). Le HTTPS public n'est requis que si on veut spécifiquement du transport HTTP. Pattern launcher stdio : logs sur **stderr** (stdout = canal JSON-RPC), `os.chdir` vers la racine si les chemins de config sont relatifs. Cf [[mcp-local-cowork-vs-claude-code]] section AMENDEMENT 24 juin + `mcp-forge-brain/start_stdio.py`. Connexe : [[feedback_mcp_transport_stdio_http_crashloop]] (le piège inverse : lancé en stdio mais démarre en HTTP → "running" ≠ "Connected").
