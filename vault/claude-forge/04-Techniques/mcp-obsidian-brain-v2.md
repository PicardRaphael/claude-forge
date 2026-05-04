---
titre: "MCP Obsidian Brain v2 — SQLite FTS5"
resume: "Remplace la CLI Obsidian par SQLite FTS5 autonome, deploye sur VM serveur, accessible via VPN"
aliases:
  - "MCP v2"
  - "obsidian-brain v2"
  - "MCP SQLite"
domaine: technique
type: technique
derniere-maj: 2026-04-29
auteur: claude
sources:
  - "[[neoteem-brain-plugins]]"
tags:
  - "#type/technique"
  - "#domaine/neoteem"
  - "#projet/neoteem-brain"
---

## Description

Reecriture complete du MCP obsidian-brain. L'ancien dependait de la CLI Obsidian (subprocess, Obsidian ouvert obligatoire). Le v2 utilise SQLite FTS5 comme moteur de recherche autonome — zero dependance Obsidian sur le serveur.

Architecture : FastMCP HTTP sur VM Linux, accessible via VPN par tous les postes Claude Code et Claude Desktop.

## Specs techniques

- **Moteur** : SQLite FTS5 avec BM25 pondere (nom x10, aliases x8, contenu x1)
- **Tokenizer** : `unicode61 remove_diacritics 2` (accents, pas de stemming)
- **Snippets** : natifs FTS5 (`snippet()`)
- **Stop words** : filtre francais (50+ mots)
- **Indexation** : 836 notes en 3.35s, reindex poll 30s
- **Tests** : 38 tests unitaires, benchmark parite 24/24 PASS
- **9 tools MCP** : search_brain, read_note, read_note_by_path, get_backlinks, get_tags, get_property, create_note, append_note, update_property
- **Git sync** : pull main/5min, commit par branche mcp/<user>, push/30min

## Quand utiliser

Tout acces au vault neoteem-brain passe par ce MCP — sauf en local avec Obsidian ouvert (CLI skill gardee).

## Architecture serveur

```
VM Linux
├── /opt/mcp-obsidian-brain/   (repo MCP)
├── /data/neoteem-brain/       (vault git)
└── /data/brain.db             (index SQLite, jetable)
```

Service systemd + nginx reverse proxy HTTPS. Config via `config.yaml`.

## Repos

- MCP : `bitbucket.org/neot-v2/mcp-obsidian-brain`
- Vault : `bitbucket.org/neot-v2/neoteem-brain`
- Spec : `claude-forge/docs/superpowers/specs/2026-04-29-mcp-obsidian-brain-v2-design.md`

## Liens

- [[neoteem-brain-plugins]]
- [[SQLite FTS5 pour vault]]
