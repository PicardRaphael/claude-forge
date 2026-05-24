---
name: forge-brain
allowed-tools: mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__read_note_resolved, mcp__forge-brain__get_backlinks, mcp__forge-brain__get_tags, mcp__forge-brain__get_property, mcp__forge-brain__find_by_property, mcp__forge-brain__list_notes, mcp__forge-brain__vault_stats, mcp__forge-brain__lint_vault, mcp__forge-brain__usage_stats, mcp__forge-brain__create_note, mcp__forge-brain__append_note, mcp__forge-brain__insert_section, mcp__forge-brain__update_note, mcp__forge-brain__update_property, mcp__forge-brain__bulk_update_property, mcp__forge-brain__move_note, mcp__forge-brain__delete_note
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

### Outils MCP — Lecture

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `search_brain(query, limit, context)` | FTS5 BM25 pondéré file_stem:10 / aliases:8 / content:1 | Chercher info, défaut exploration |
| `read_note(file)` | **Lit la note ENTIÈRE** (frontmatter + body) | **Défaut pour lire une note** — pas de troncature |
| `read_note(file, offset, limit_chars)` | Pagination char-based | UNIQUEMENT si note > 50k chars (CHANGELOG, log) |
| `read_section(file, heading)` | Lit UNE section (header → prochain header même niveau) | Économie tokens 30x sur grosses notes (CHANGELOG) |
| `read_note_resolved(file, depth=1)` | Note + inline embeds récursivement | MOC avec embeds — 1 appel = N+1 notes en contexte |
| `read_note_by_path(path)` | Lire par chemin exact | Quand on a le path complet (pas le stem) |
| `get_backlinks(file)` | Notes pointant vers (case-insensitive) | Navigation graphe, audit orphelines |
| `get_tags()` | Tags triés par fréquence | Vue structurelle |
| `get_property(file, name)` | 1 propriété frontmatter | Vérif derniere-maj/type sur 1 note |
| `find_by_property(name, value, comparator, folder, limit)` | **Dataview-equivalent** : query frontmatter | Notes stales (`lt` date), doublons (`eq`), sources vides (`missing`). Comparateurs : eq/ne/lt/gt/contains/missing/present |
| `list_notes(folder, limit)` | Inventaire notes d'un dossier | Audit par cluster |
| `vault_stats()` | Stats vault complètes | Photo globale |
| `lint_vault(limit)` | Détecte aliases<4, orphelines, sans tag, YAML cassé, wikilinks brisés | Audit qualité vault |
| `usage_stats(days)` | Agrégation calls/total_ms/errors par tool | Décisions pruning outils MCP |

### Outils MCP — Écriture

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `create_note(path, content)` | Créer note | Capitaliser info |
| `append_note(file, content)` | Ajouter à la fin | Étoffer note existante |
| `insert_section(file, marker, content, position)` | Insérer avant/après un header | Insertion ciblée |
| `update_note(file, content)` | **Remplace EN ENTIER** | Refonte complète (rare) |
| `update_property(file, name, value)` | 1 prop sur 1 note | Update ciblé |
| `bulk_update_property(files, name, value)` | **Même prop sur N notes en 1 appel** | Pattern audit : derniere-maj 16 leaders = 1 appel |

### Outils MCP — Move / Delete

| Outil | Usage | Quand utiliser |
|-------|-------|----------------|
| `move_note(file, new_path, update_wikilinks=True)` | Déplace + réécrit wikilinks dans backlinks si stem change | Rename + déplacement atomique safe |
| `delete_note(file, force=False)` | Refuse si backlinks > 0 sauf force. `force=True` rapporte wikilinks brisés | Cleanup safe |

### Matrice décision rapide

| Tâche | Outil prioritaire |
|-------|-------------------|
| Chercher info | `search_brain` |
| Lire 1 note complète | `read_note(file)` |
| Lire section précise | `read_section(file, heading)` |
| Lire MOC avec embeds | `read_note_resolved(file)` |
| Lire grosse note par morceaux | `read_note(file, offset, limit_chars)` |
| Trouver notes par frontmatter | `find_by_property` |
| Update prop sur 1 note | `update_property` |
| Update prop sur N notes | `bulk_update_property` |
| Renommer + rewriting | `move_note` |
| Supprimer safe | `delete_note` |
| Audit qualité vault | `lint_vault` |
| Mesurer usage outils | `usage_stats(days=7)` |
### Format Obsidian Flavored Markdown

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
