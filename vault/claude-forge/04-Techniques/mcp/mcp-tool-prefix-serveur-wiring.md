---
titre: "MCP tool prefix — câblage dans skills/agents et déduplication d'URL"
resume: "Le préfixe mcp__<x>__* d'un tool MCP = la clé exacte du serveur dans .mcp.json (jamais le nom d'affichage). Deux serveurs sur la même URL → Claude Code masque l'un des deux (deduplication)."
aliases:
  - "mcp tool prefix nom serveur"
  - "préfixe tool mcp"
  - "mcp allowed-tools prefix"
  - "mcp deduplication url"
  - "câbler un mcp skill agent"
  - "doublon url mcp masquage"
derniere-maj: 2026-07-07
auteur: claude
type: technique
tags:
  - "#type/technique"
  - "#domaine/mcp"
  - "#domaine/claude-code"
  - "#pattern/gotcha"
---

# MCP tool prefix — câblage dans skills/agents et déduplication d'URL

## Règle : préfixe = clé `.mcp.json`, jamais le nom d'affichage

Quand on câble un outil MCP dans `allowed-tools` (skill) ou `tools:` (agent), le préfixe est :

```
mcp__<nom-serveur>__*
```

où `<nom-serveur>` = la **clé exacte du serveur dans `.mcp.json`** (ou le nom interne du connector claude.ai), **jamais** le nom d'affichage humain.

**Cas vécu 18 juin 2026 (ia-workbench)** : `.mcp.json` déclarait `"neobrain": {url: ...}` → le tool est `mcp__neobrain__*`. Câblé à la place `mcp__claude_ai_MCP_NeoBrain_-_NEOTEEM__*` (le nom d'affichage du connector claude.ai) → tools jamais résolus. Le connector claude.ai a son propre préfixe `mcp__claude_ai_MCP_NeoBrain_-_NEOTEEM__*` ; le serveur `.mcp.json` a `mcp__neobrain__*`. **Deux serveurs distincts, deux préfixes, même URL.**

## Corollaire — doublon d'URL = masquage

Deux serveurs MCP déclarés sur la même URL (`https://mcp-brain.example.com/mcp`) → Claude Code en **masque un** (message : « hidden — same URL as ... »). Comportement documenté dans le changelog CC (avril 2026) sous « MCP deduplication claude.ai connectors ».

**Symptôme** : un serveur configuré dans `.mcp.json` dont les tools n'apparaissent pas dans `claude mcp list`.

**Fix** : retirer le doublon — garder soit le serveur `.mcp.json` local, soit le connector claude.ai, et aligner tous les préfixes dans `.claude/` sur celui qui reste.

## Réflexe avant de câbler

```bash
claude mcp list   # vérifie le nom réel + les tools exposés
```

1. Vérifier la **clé** dans `.mcp.json` (pas le champ `name` d'affichage).
2. En cas de connector claude.ai + serveur local sur la même URL → choisir l'un, retirer l'autre.
3. Vérification empirique **en session fraîche** uniquement — les MCP ne se rechargent pas en cours de session.

## Audit post-refonte — préfixe mort

Lors d'un audit `.claude/` post-renommage de serveur : croiser `allowed-tools` ⨯ `claude mcp list`. Si une déclaration `.mcp.json` a été supprimée/renommée, son ancien préfixe `mcp__<ancien>__*` survit en frontmatter — tool jamais résolu en silence. Cf [[audit-claude-folder-pattern]] section « Gotcha — refonte interne ».

---

## Wikilinks

- [[MOC-MCP]] — point d'entrée dossier MCP
- [[construire-mcp-production]] — recipe serveur complet
- [[mcp-tool-design-scaling]] — concevoir les tools (JSON Schema, annotations)
- [[audit-claude-folder-pattern]] — audit complet .claude/ (section gotcha préfixe mort)
- [[comment-creer-skill]] — `mcp__server__*` wildcard dans allowed-tools
