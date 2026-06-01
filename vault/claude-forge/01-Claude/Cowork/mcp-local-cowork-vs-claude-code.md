---
titre: "MCP local : marche en Claude Code (HTTP/stdio), PAS en Cowork (localhost bloqué)"
resume: "Un MCP local localhost ne marche PAS dans Cowork (VM cloud Anthropic) — seulement en Claude Code (~/.claude.json type:http) ou Desktop Chat (stdio command/args). Cowork exige une URL HTTPS publique."
aliases: ["mcp local cowork", "mcp localhost claude code", "cowork connecteur https", "mcp stdio vs http claude desktop", "claude_desktop_config vs claude.json"]
type: technique
derniere-maj: 2026-06-01
auteur: claude
tags: ["#type/technique", "#domaine/cowork", "#domaine/claude-code"]
---

# MCP local : Cowork vs Claude Code

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
affiche "running" (process vivant) sans être **connecté** (mismatch). "running" ≠ "Connected".

**Conséquence** : pour faire tourner une automatisation à MCP local sans VM ni admin → utiliser
**Claude Code** (dans l'app Desktop), pas Cowork. Voir [[cowork-architecture]] et
[[automatisation-triage-tickets-support-suivi]].
