---
titre: neoteem-brain
resume: Vault Obsidian métier Neoteem — 682+ notes, knowledge base métier, pipeline vault-workflow
aliases:
  - neoteem-brain
  - neoteem brain
  - brain neoteem
  - vault neoteem
  - vault métier
type: context
status: active
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/neoteem-brain"
---

## Description

Vault Obsidian de [[Neoteem|Neoteem]]. 682+ notes, 2245+ wikilinks. Base de connaissances métier centralisée (Confluence, Jira, code, fonctions PG).

## Domaines métier

Syndic de copropriété, gérance locative, comptabilité immobilière.

## Stack

- Obsidian + skills kepano (obsidian-cli, obsidian-markdown, obsidian-bases, json-canvas)
- Sources : Confluence (MCP Atlassian), Jira, repos Bitbucket, PostgreSQL
- Kit standalone `neo-brain/` copiable dans .claude/skills/ des autres repos

## Composants Claude Code

- **4 agents** : vault-enricher (Confluence→vault), repo-analyzer (code→doc), sync-checker (audit), vault-linker (structure)
- Pipeline vault obligatoire : repo-analyzer → vault-linker → sync-checker
- Hook read-only : guard-external-writes.py
- 07-Support/ : section non-technique (FAQ, procédures, glossaire)
- Aliases = semantic search : minimum 3, couvrir technique + non-technique

## Contraintes

- Chemin : `neot-v2/neoteem-brain` (PAS `Documents/neoteem-brain`)
- Git : Bitbucket `neot-v2/neoteem-brain`, branche `master`
- Seuil réévaluation : 2000-3000 notes → envisager hybrid FTS+vector
- Organisation : `neofront` (~68 repos frontends) + `neot-v2` (~60 repos backends)

## Liens

- [[Neoteem|Neoteem]]
- [[Claude-Forge|Claude-Forge]]
- [[neoteem-brain-plugins]] — Architecture 5 plugins Cowork role-based
- [[mcp-obsidian-brain-v2]] — MCP SQLite FTS5, remplace CLI Obsidian
