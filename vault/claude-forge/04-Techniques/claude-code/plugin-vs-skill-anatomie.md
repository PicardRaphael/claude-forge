---
titre: "Plugin vs Skill (compétence) — anatomie, quand l'un quand l'autre, Claude Code vs Desktop"
resume: "Skill = unité atomique d'instructions (1 dossier + SKILL.md). Plugin = conteneur distribuable (skills + agents + hooks + MCP + LSP + monitors + bin + settings). CLAUDE.md dans un plugin = IGNORÉ. Claude Desktop/Web = upload .zip ; Claude Code = directory-based."
aliases:
  - "plugin vs skill"
  - "skill vs plugin"
  - "compétence vs plugin"
  - "qu'est-ce qu'un plugin claude"
  - "que contient un plugin claude code"
  - "claude.md dans un plugin"
  - "plugin claude desktop"
  - "skill claude desktop zip"
domaine: claude-code
type: technique
derniere-maj: 2026-06-04
auteur: claude
sources:
  - "https://code.claude.com/docs/en/plugins"
  - "https://code.claude.com/docs/en/plugins-reference"
  - "https://code.claude.com/docs/en/skills"
  - "https://www.mindstudio.ai/blog/claude-code-skills-vs-plugins-difference"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/plugins"
  - "#sujet/skills"
  - "#doctrine/2026"
---

# Plugin vs Skill (compétence) — anatomie

> Note canonique forge. Tranche : qu'est-ce qu'une compétence (skill), qu'est-ce qu'un plugin, ce qu'un plugin peut contenir, et la différence Claude Code vs Claude Desktop. Vérifié en source primaire Anthropic le 4 juin 2026.

## TL;DR

- **Skill (= compétence)** = unité atomique. Un dossier `<nom>/SKILL.md` (+ `references/`, `scripts/`). Enseigne à Claude COMMENT faire une tâche. Progressive disclosure (~30-50 tokens chargés au départ, body à l'activation).
- **Plugin** = conteneur distribuable. Bundle plusieurs composants (skills, agents, hooks, MCP, LSP, monitors, bin, settings) en une unité versionnée et partageable. Manifest `.claude-plugin/plugin.json` obligatoire pour l'identité/distribution.
- **Règle simple** : 1 tâche réutilisable → skill. Distribuer/partager un setup (≥1 skill + autres composants, ou versionné équipe) → plugin.

## Ce qu'un plugin PEUT contenir (table officielle)

Source : [plugins-reference](https://code.claude.com/docs/en/plugins-reference). Tout sauf `plugin.json` est à la **racine du plugin**, JAMAIS dans `.claude-plugin/`.

| Composant | Emplacement | Rôle |
|---|---|---|
| **Manifest** | `.claude-plugin/plugin.json` | Métadonnées (name, description, version, author...). Le seul dans `.claude-plugin/` |
| **Skills** | `skills/<nom>/SKILL.md` | Compétences (model-invoked ou `/plugin:nom`) |
| **Commands** | `commands/*.md` | Skills en fichiers plats (déprécié, préférer `skills/`) |
| **Agents** | `agents/*.md` | Subagents. ⚠️ `hooks`, `mcpServers`, `permissionMode` NON supportés en frontmatter d'agent shippé par plugin (sécu) |
| **Hooks** | `hooks/hooks.json` | Event handlers (même format que settings.json) |
| **MCP servers** | `.mcp.json` | Serveurs MCP bundlés |
| **LSP servers** | `.lsp.json` | Language servers (intelligence code) |
| **Monitors** | `monitors/monitors.json` | Watchers background (logs, fichiers) |
| **Executables** | `bin/` | Binaires ajoutés au PATH du tool Bash quand le plugin est actif |
| **Output styles** | `output-styles/` | Styles de sortie |
| **Themes** | `themes/` | Thèmes couleur |
| **Settings** | `settings.json` | Config par défaut quand activé. Seules clés `agent` + `subagentStatusLine` supportées |

## ⚠️ CLAUDE.md dans un plugin = IGNORÉ (point critique)

Verbatim Anthropic ([plugins-reference](https://code.claude.com/docs/en/plugins-reference)) :

> "A `CLAUDE.md` file at the plugin root is **not loaded as project context**. Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md. To ship instructions that load into Claude's context, put them in a **skill**."

**Conséquence pratique** : on ne livre PAS d'instructions persistantes via un CLAUDE.md embarqué dans un plugin — il serait silencieusement ignoré. Pour shipper des instructions dans un plugin :
- **Skill knowledge** (`user-invocable: false` ou auto-invoquée par description) = l'équivalent d'un "contexte" chargé à la demande.
- Le CLAUDE.md reste un artefact **projet/repo** (racine du repo, versionné), séparé du plugin. Chaque utilisateur/projet a le sien.

Note connexe : le hook `InstructionsLoaded` (event) se déclenche quand un CLAUDE.md ou `.claude/rules/*.md` est chargé — confirme que le chargement CLAUDE.md est un mécanisme repo, pas plugin.

## README.md dans un plugin = doc humaine, JAMAIS affiché par Claude

Vérifié source primaire ([plugins-reference](https://code.claude.com/docs/en/plugins-reference), 4 juin 2026) : le `README.md` à la racine d'un plugin n'est **ni requis, ni chargé comme contexte, ni affiché dans l'UI** (`/plugin`, marketplace). C'est de la doc humaine pure (lecture GitHub / install manuelle).

Les **seuls champs affichés à l'utilisateur** viennent du manifeste `plugin.json` :

| Champ plugin.json | Affiché où |
|---|---|
| `displayName` | Nom lisible dans le menu `/plugin` (fallback sur `name` si absent) |
| `description` | Phrase descriptive dans `/plugin` et le marketplace |
| `version`, `author`, `keywords`, `homepage`, `repository`, `license` | Métadonnées marketplace |

Le manifeste lui-même est *techniquement* optionnel (Claude Code auto-découvre les composants et dérive le `name` du dossier), MAIS sans lui → pas de `description`/`displayName` dans l'UI. Donc **toujours fournir un plugin.json soigné** ; le README est optionnel et orthogonal.

**Conséquence pratique (Neoteem, 4 juin 2026)** : décision de ne PAS embarquer de README dans les 4 plugins `output/lojii/` (neoteem-po, neoteem-support, neoteem-brain-admin, neoteem-brain) — à la place, `displayName` + `description` soignés dans chaque plugin.json (seuls champs que le PO/support verra dans `/plugin`).

## Claude Code vs Claude Desktop / Web — mécanismes différents

| Aspect | Claude Code (CLI) | Claude Desktop / Web |
|---|---|---|
| Install skill/plugin | Directory-based (`~/.claude/skills/`, `/plugin`) ou `--plugin-dir` | **Upload `.zip`** via Settings UI (`claude.ai/directory`) |
| Distribution | Marketplace `/plugin marketplace`, git | Directory unifié (3 onglets : Skills / Connectors / Plugins, depuis 31 mars 2026) |
| MCP | Local via settings.json OU URL/VM | **Connectors** (MCP distant OAuth, géré par partenaire) |
| Slash commands custom | Complet | Limité |
| Versioning git | Oui (commit `.claude/`) | Non natif |

**Pour Neoteem** : les PO/support sur Claude Desktop installent les plugins en **uploadant un .zip** (cf [[plugin-structure-cowork-claude-code]] mémoire forge : zipper le CONTENU du dossier, pas le dossier). Le MCP vault passe par une **Connector / URL distante** (VM `mcp-brain.neoteem.fr`), pas un MCP local.

## Quand skill, quand plugin — arbre de décision

```
Tâche réutilisable unique (1 workflow, 1 domaine) ?
  → SKILL (dans .claude/skills/ pour soi, ou dans un plugin pour partager)

Tu veux DISTRIBUER à une équipe / plusieurs projets / versionner ?
  → PLUGIN (conteneur)
     - même si le plugin ne contient qu'1 skill : OK, c'est le véhicule de distribution
     - si plusieurs skills + veux des hooks/MCP/agents groupés : PLUGIN évident

Besoin d'instructions persistantes chargées au démarrage ?
  → CLAUDE.md du REPO (pas dans le plugin — ignoré)
  → OU skill knowledge dans le plugin (chargée à la demande)
```

**Namespacing** : une skill dans un plugin est toujours préfixée `/<plugin>:<skill>` (ex `/po-lojii:spec`), pour éviter les collisions. Une skill standalone `.claude/skills/` garde un nom court (`/spec`).

## Application — cas po-lojii (Neoteem)

Le setup PO (`spec` + `review-ticket`) = **un plugin** `po-lojii` (2 skills → conteneur justifié, distribution équipe via .zip Desktop). Décisions qui découlent de cette note :
- Le CLAUDE.md de chaque PO reste dans SON repo `ws`, PAS dans le plugin (sinon ignoré). Chacun a son CLAUDE.md (≠ par personne).
- Les skills brain (`neo-brain-support-admin` / `neo-brain-dev-admin`) sont des **plugins séparés** installés à côté ; po-lojii les invoque via le tool Skill.
- Mémoire des PO : Auto-Memory locale par PC (`~/.claude/projects/<repo>/memory/`) par défaut, OU `memory/` versionné dans le repo si capitalisation équipe voulue (décision ouverte).

## Anti-patterns

- ❌ Mettre un CLAUDE.md dans un plugin en croyant qu'il charge le contexte → ignoré (verbatim Anthropic)
- ❌ Mettre `skills/` `agents/` `hooks/` DANS `.claude-plugin/` → seul `plugin.json` y va, le reste à la racine
- ❌ Zipper le dossier plugin lui-même au lieu de son contenu (Desktop) → niveau de dossier en trop, plugin invalide (cf [[plugin-structure-cowork-claude-code]])
- ❌ `author` en string dans plugin.json → doit être un objet `{ "name": "..." }`
- ❌ Confondre Connector (Desktop, MCP OAuth distant) et MCP local (Claude Code settings.json)

## WIKILINKS

- [[comment-creer-skill]] — création d'une skill (unité)
- [[comment-creer-agent]] — agents (composant plugin)
- [[comment-creer-hook]] — hooks (composant plugin)
- [[mcp-vs-skills-doctrine]] — MCP data / skill how-to / bash exploration
- [[comment-ecrire-claudemd]] — CLAUDE.md = artefact repo, pas plugin
- [[cowork-architecture]] — Cowork / Desktop
