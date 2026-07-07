---
titre: "enableAllProjectMcpServers + permissions.allow — couverture tool-level sans prompt"
resume: "enableAllProjectMcpServers:true dans settings.json/settings.local.json auto-approuve les outils MCP au niveau tool sans prompt — lister mcp__server__tool individuellement dans permissions.allow est redondant."
aliases:
  - "enableAllProjectMcpServers"
  - "mcp permissions allow redondant"
  - "mcp tool level auto-approve"
  - "permissions allow mcp settings"
  - "mcp sans prompt permission"
  - "enableAllProjectMcpServers tool level"
type: technique
domaine: claude-code
derniere-maj: 2026-07-07
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
---

# enableAllProjectMcpServers + permissions.allow — couverture tool-level sans prompt

> Vérifié empiriquement le 27 mai 2026 (nettoyage settings.local.json forge). Source : `memory/reference_enableallprojectmcp_couvre_tool_level.md`.

## Comportement

`"enableAllProjectMcpServers": true` (dans `settings.local.json` ou `settings.json`) + le serveur déclaré dans `.mcp.json` + listé dans `enabledMcpjsonServers` = les outils du serveur sont **auto-approuvés au niveau tool, sans prompt de permission**.

Lister chaque `mcp__forge-brain__read_note`, `mcp__forge-brain__list_notes`… dans `permissions.allow` est alors **redondant** — l'appel passe même si l'entrée est absente du allow.

**Preuve empirique (27 mai 2026)** : retiré `mcp__forge-brain__list_notes` du allow → appel `list_notes` réussi sans prompt. Idem `vault_stats` (jamais dans le allow, appel OK sans prompt). Couverture confirmée.

## Nuance — re-sédimentation harness

Après un appel `search_brain`, le harness a **ré-ajouté** `mcp__forge-brain__search_brain` dans le allow automatiquement (fichier passé de 11→12 entrées). Comportement non uniforme : `list_notes`/`vault_stats` non ré-ajoutés, `search_brain` ré-ajouté — timing watcher probable.

**Conséquence pratique** : supprimer les entrées MCP du allow réduit le bruit à l'instant T, mais certaines peuvent **repousser** au fil de l'usage. Ce n'est pas une régression (aucun prompt), juste une re-sédimentation cosmétique à re-nettoyer périodiquement.

## Comment appliquer

- Si `enableAllProjectMcpServers: true` est présent → **ne pas lister** les `mcp__server__tool` dans `permissions.allow` (redondant, bruit).
- Si `enableAllProjectMcpServers` est un jour retiré → le prompt par tool réapparaît. Le **flag est le porteur de la couverture**, pas le allow.

## Distinction importante — deux mécanismes séparés

| Mécanisme | Fichier | Rôle |
|---|---|---|
| `permissions.allow` + `enableAllProjectMcpServers` | `settings.json` / `settings.local.json` | Éviter le prompt en **session principale** |
| `tools:` / `allowed-tools:` frontmatter | `agents/*.md` / `SKILL.md` | Donner accès MCP à un **sous-agent ou skill** |

Ces deux mécanismes sont orthogonaux. [[comment-creer-skill]] porte le second (frontmatter agent/skill) ; cette note porte le premier (settings).

## Wikilinks

- [[mcp-vs-skills-doctrine]] — doctrine MCP data / skill how-to / bash exploration
- [[comment-creer-skill]] — `tools:`/`allowed-tools:` frontmatter = mécanisme distinct
- [[plugin-vs-skill-anatomie]] — `.mcp.json` et MCP bundlés dans un plugin
- [[trail-of-bits-config]] — setup sécu entreprise, MCP minimaux
