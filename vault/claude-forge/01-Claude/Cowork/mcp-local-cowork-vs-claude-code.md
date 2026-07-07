---
titre: "MCP local : Cowork marche en stdio, pas en HTTP localhost (Claude Code HTTP/stdio, Desktop Chat stdio)"
resume: "MCP local en Cowork : marche en stdio (command/args, process lancé en local) mais PAS en HTTP localhost (VM cloud ne joint pas ta machine). Claude Code = http/stdio via ~/.claude.json, Desktop Chat = stdio. HTTPS public requis seulement pour du transport HTTP en Cowork."
aliases: ["mcp local cowork", "mcp localhost claude code", "cowork connecteur https", "mcp stdio vs http claude desktop", "claude_desktop_config vs claude.json"]
type: technique
derniere-maj: 2026-06-24
auteur: claude
tags: ["#type/technique", "#domaine/cowork", "#domaine/claude-code"]
---

# MCP local : Cowork vs Claude Code

> **AMENDEMENT 24 juin 2026 (retour terrain Raphael) — la prémisse « localhost impossible en Cowork » est FAUSSE pour le transport stdio.** Un MCP **stdio** (`command` + `args`) configuré en Cowork **marche** : Cowork lance le process **localement** sur la machine (comme Desktop Chat), il n'a donc pas besoin de joindre `localhost` par le réseau. Vérifié : forge-brain en stdio sur le Cowork d'un PO, puis sur celui de Raphael (launcher `mcp-forge-brain/start_stdio.py`, `transport="stdio"`). La vraie distinction n'est PAS « local vs cloud » mais **le transport** :
>
> | Transport en Cowork | Marche ? | Pourquoi |
> |---|---|---|
> | **stdio** (`command`/`args`) | ✅ OUI | Cowork spawn le process en local, pas d'accès réseau requis |
> | **HTTP `localhost:port`** | ❌ NON | la connexion HTTP partirait de la VM cloud Anthropic → ne joint pas ta machine |
> | **HTTP/HTTPS public** | ✅ OUI | URL publique joignable depuis le cloud |
>
> Donc : pour un MCP local en Cowork, **utiliser stdio** (pas besoin de tunnel HTTPS). Le HTTPS public ne reste nécessaire que si l'on veut absolument du transport HTTP. Le corps ci-dessous (écrit le 1er juin) raisonnait uniquement sur le cas HTTP-localhost et a sur-généralisé en « localhost impossible » — lire à travers ce prisme.

Un serveur MCP **local** (sur `localhost`) n'est PAS joignable depuis **Cowork** : le mode Cowork
tourne dans une **VM cloud Anthropic**, la connexion part des serveurs Anthropic, pas de la machine.
→ Cowork exige une **URL HTTPS publique** (tunnel ngrok / VM / reverse proxy) pour un custom connector.
Bug connu : un MCP HTTP "Connected" en Claude Code échoue silencieusement en Cowork.

Là où le MCP local **marche** :

| Surface | Fichier config | Transport |
|---|---|---|
| **Claude Code** (terminal ou onglet Code de l'app) | `~/.claude.json` | `type: http` + `url` (ou stdio) |
| **Desktop Chat** | `claude_desktop_config.json` | `command` + `args` (stdio) |
| **Cowork** | — | ❌ localhost impossible (HTTPS public requis) |

**Piège transport** : un serveur lancé via `command`/`args` (attendu stdio) mais qui démarre en HTTP

**Debug transport** : `claude mcp list` → statut **"Connected"** = seul indicateur fiable. "running" = process vivant, pas nécessairement connecté. Tout MCP "lancé mais inactif" → vérifier stdio vs http AVANT toute autre piste.
affiche "running" (process vivant) sans être **connecté** (mismatch). "running" ≠ "Connected".

**Conséquence** : pour faire tourner une automatisation à MCP local sans VM ni admin → utiliser
**Claude Code** (dans l'app Desktop), pas Cowork. Voir [[cowork-architecture]] et
[[automatisation-triage-tickets-support-suivi]].
