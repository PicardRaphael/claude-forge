---
name: neoteem-brain-plugin
description: 3 plugins neoteem-brain v2.0.0 (support, dev, dev-ia) — marketplace locale, install.bat unifie 3 profils, MCP auto pour Cowork. Deploye 2026-04-21.
type: project
originSessionId: d55234b8-f33e-4de6-acb1-6bda9799e651
---
## Plugins neoteem-brain v2.0.0

Split du plugin monolithique en 3 plugins standalone le 2026-04-21. Marketplace locale pointant vers `neoteem-brain/plugin/`.

**Structure :**
```
plugin/
├── .claude-plugin/marketplace.json (3 plugins)
├── neoteem-brain-support/ (equipe support — CLI + MCP adaptive)
├── neoteem-brain-dev/ (devs — CLI direct, vault complet)
└── neoteem-brain-dev-ia/ (devs IA — CLI + cross-ref 4 repos)
```

**Install equipe :** `mcp-obsidian-brain\install.bat` — 3 profils (support/dev/dev-ia).
- Support : installe MCP + configure `claude_desktop_config.json` (lance auto par Cowork)
- Dev : installe Obsidian + repos Bitbucket + plugin dev
- Dev IA : idem + plugin dev-ia

**Scope :** user (global machine)
**Repos connectes :** neo_ia (dev + dev-ia), ia_back (dev + dev-ia), neoteem-brain (dev local)

**Why:** Le plugin monolithique forcait a installer 3 skills quand on en voulait 1. Novices ne savaient pas quoi utiliser. Le split par role + install.bat guide permet un onboarding autonome.

**How to apply:**
- Modifier le plugin → bumper version dans plugin.json correspondant
- Bug cache connu : toujours bumper version pour forcer refresh
- Support = MCP tools (lecture seule) + CLI si dispo. Devs = CLI direct
- Ancien plugin `neoteem-brain@neoteem` desinstalle, cache purge
