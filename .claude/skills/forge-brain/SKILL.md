---
name: forge-brain
description: Search, read, and write to the forge-brain Obsidian vault — persistent infinite memory for AI tools, techniques, prompts, industry news, mistakes, and everything learned. Use PROACTIVELY at session start, before creating any skill/agent/hook/prompt, before answering technical questions, after cc-news, and after significant mistakes. ALWAYS invoke when the user asks about vault content, past decisions, or knowledge base.
---

# Forge Brain

Knowledge base Obsidian de claude-forge. Stocke tout ce que j'apprends : Claude Code, concurrents, modèles, techniques, leaders, industrie.

**Vault** : `vault/claude-forge/`

## Quand utiliser — Le vault est un RÉFLEXE

| Situation | Action |
|-----------|--------|
| Début de session | Chercher les notes récentes pour rappel contexte |
| **Avant de créer skill/agent/hook/prompt** | **Chercher best practices + erreurs passées + prompts réutilisables** |
| **Analyse de repo / projet** | **Chercher patterns, concurrents, techniques pertinentes** |
| Question sur feature/outil | Chercher dans le vault AVANT de répondre |
| Après cc-news | Créer/mettre à jour les notes avec les découvertes |
| Nouvelle info apprise | Créer une note atomique |
| **Erreur significative commise** | **Créer note dans `Knowledge/erreurs/` avec template `erreur.md`** |
| Info potentiellement datée | Vérifier la note existante + `derniere-maj` |

## Accès au vault — MCP forge-brain (OBLIGATOIRE)

Le MCP forge-brain (auto-start SessionStart, port 8091) est le SEUL moyen d'accès au vault.
Ne JAMAIS utiliser la CLI Obsidian, Grep, Read ou Glob brut sur le vault.

### Outils MCP

| Outil | Usage |
|-------|-------|
| `search_brain(query, limit)` | Recherche full-text FTS5 |
| `read_note(file)` | Lire par nom ou alias |
| `read_note_by_path(path)` | Lire par chemin exact |
| `get_backlinks(file)` | Naviguer le graphe |
| `get_tags()` | Vue structurelle |
| `get_property(file, name)` | Lire propriété frontmatter |
| `list_notes(folder, limit)` | Lister notes d'un dossier |
| `vault_stats()` | Stats vault complètes |
| `create_note(path, content)` | Créer une note |
| `append_note(file, content)` | Ajouter à une note |
| `update_property(file, name, value)` | Modifier propriété |

### Écriture — format Obsidian Flavored Markdown

Quand on CRÉE une note via MCP `create_note`, le contenu doit respecter la skill `obsidian-markdown` :
- Frontmatter YAML (titre, resume, aliases 4-6, type, derniere-maj, tags)
- Wikilinks `[[Note]]` (pas de markdown links pour les notes internes)
- Minimum 2 wikilinks par note
- Résumé spécifique dans le frontmatter

### Fallback (si MCP crash)

Read/Glob direct sur `vault/claude-forge/`. Ne devrait jamais arriver.

## Créer une note

1. Lire le template correspondant via MCP : `read_note(file="<type>")` dans `Templates/`
2. Créer la note avec `create_note(path="...", content="...")` en suivant le template
3. Ajouter le wikilink dans le MOC correspondant via `append_note`

## Structure du vault

```
0-Inbox/          — Capture rapide, à trier par /done
1-Projets/        — Notes de contexte par projet (Neoteem, Claude-Forge, etc.)
2-Casquettes/     — Aires de responsabilité de vie (profil holistique, famille, gaming)
00-Hub/           — Home + 6 MOCs (index par thème)
01-Claude/Code/   — features/, changelog/, best-practices/, hooks/, skills/, agents/
02-Concurrents/   — gemini-cli/, codex/, copilot/, cursor/, xai/
03-Modeles/       — claude/, gpt/, gemini/, grok/
04-Techniques/    — prompt-engineering/, context-engineering/, patterns/
05-Leaders/       — Fiches personnes clés
06-Industrie/     — Market, funding, événements, tendances
07-Prompts/       — system-prompts/, agent-prompts/, skill-prompts/, templates-prompts/
Knowledge/        — explorations/, syntheses/
Templates/        — 12 templates (+context-projet, +context-casquette)
```

## Templates (OBLIGATOIRE)

Toujours lire le template AVANT de créer une note :

| Dossier cible | Template |
|---|---|
| `01-Claude/Code/features/` | `Templates/feature.md` |
| `01-Claude/Code/changelog/` | `Templates/changelog.md` |
| `01-Claude/Code/best-practices/` | `Templates/best-practice.md` |
| `02-Concurrents/` | `Templates/concurrent.md` |
| `03-Modeles/` | `Templates/modele.md` |
| `04-Techniques/` | `Templates/technique.md` |
| `05-Leaders/` | `Templates/leader.md` |
| `06-Industrie/` | `Templates/knowledge.md` |
| `07-Prompts/` | `Templates/prompt.md` |
| `Knowledge/` | `Templates/knowledge.md` |
| `1-Projets/` | `Templates/context-projet.md` |
| `2-Casquettes/` | `Templates/context-casquette.md` |

## Frontmatter obligatoire

```yaml
---
titre: "Titre lisible"
resume: "1 ligne"
aliases:
  - "synonyme"
domaine: claude-code | gemini | openai | copilot | cursor | xai | technique | industrie
type: feature | changelog | deprecation | best-practice | technique | leader | modele | concurrent | knowledge
derniere-maj: YYYY-MM-DD
auteur: claude
sources:
  - "URL ou [[wikilink]]"
tags:
  - "#type/<type>"
  - "#domaine/<domaine>"
---
```

## Règles

1. **1 concept = 1 note** — atomique, jamais de dump monolithique
2. **Wikilinks** partout — `[[Opus 4.7]]`, `[[Boris Cherny]]`
3. **MOC à jour** — chaque nouvelle note doit être linkée dans son MOC
4. **derniere-maj** — mettre à jour à chaque édition
5. **Ne jamais modifier Templates/** — lecture seule
6. **Vault ≠ mémoire projet** — le vault stocke du savoir référence, pas du feedback/projet

## Gotchas

- **MCP auto-start** — le hook SessionStart lance le MCP automatiquement. Si les outils MCP ne répondent pas, vérifier que `mcp-forge-brain/start.py` existe et que le port 8091 est libre.
- **Écriture via MCP, format via obsidian-markdown** — le MCP gère le transport (create/append/update), la skill obsidian-markdown gère le format (wikilinks, frontmatter, callouts).
- **Aliases minimum 4-6 par note** — standard neoteem-brain : inclure synonymes FR/EN et variantes techniques (ex : "Opus 4.7", "claude-opus-4-7", "opus47", "Claude Opus").

## Apprentissage

Après chaque session significative utilisant le vault :
- Vérifier que les notes créées/modifiées sont correctement linkées
- Mettre à jour les MOCs si de nouvelles notes ont été ajoutées
- Si un pattern de recherche revient souvent, créer une note synthèse dans `Knowledge/syntheses/`
