---
titre: "Architecture Cerveau Obsidian + MCP — Guide complet"
resume: "Construire un cerveau persistant pour agents IA avec Obsidian + SQLite FTS5 + MCP : indexation, recherche, skills, auto-start, qualite"
aliases:
  - "cerveau obsidian MCP"
  - "obsidian brain architecture"
  - "vault MCP guide"
  - "construire cerveau IA"
  - "MCP obsidian from scratch"
  - "brain architecture agents"
type: technique
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/rag"
  - "#domaine/claude-code"
---

## Pourquoi

Les agents IA (Claude Code, Gemini CLI, etc.) perdent leur contexte entre sessions. Un vault Obsidian + MCP donne une memoire persistante infinie : chaque session lit et ecrit dans le vault, chaque erreur est documentee, chaque technique est retrouvable.

## Architecture

```
Projet Claude Code
├── vault/<nom>/              ← fichiers .md (le cerveau)
│   ├── 00-Hub/               ← MOCs (index navigables)
│   ├── 01-..../              ← dossiers thematiques
│   └── Knowledge/            ← erreurs, syntheses, raisonnements
├── mcp-<nom>/                ← serveur MCP
│   ├── src/
│   │   ├── server.py         ← FastMCP HTTP
│   │   ├── database.py       ← SQLite FTS5 (index jetable)
│   │   ├── indexer.py        ← parse frontmatter + wikilinks
│   │   ├── watcher.py        ← poll filesystem 30s
│   │   └── tools/brain.py    ← 9+ outils MCP
│   ├── config.yaml           ← chemins, poids BM25, port
│   └── start.py              ← launcher
└── .claude/
    ├── hooks/mcp-autostart.py ← auto-demarre le MCP au SessionStart
    ├── rules/forge-brain-proactive.md ← quand/comment interroger
    └── skills/forge-brain/SKILL.md    ← skill pour les agents
```

## Etape 1 — Le vault (fichiers .md)

Obsidian Flavored Markdown avec frontmatter YAML :

```yaml
---
titre: "Nom de la note"
resume: "1 phrase specifique"
aliases: ["alias1", "alias2", "alias3", "alias4"]
tags: ["#type/technique", "#domaine/rag"]
derniere-maj: 2026-05-10
---
```

Regles : 1 concept = 1 note, max 5 sections H2, aliases min 4-6 (FR + EN + variantes + domaine), wikilinks min 2.

Voir : obsidian-markdown (skill forge) pour le format.

## Etape 2 — L index SQLite FTS5

Schema 5 tables : `notes`, `aliases`, `links`, `tags`, `notes_fts` (virtual FTS5).

BM25 pondere : file_stem x10, aliases x8, content x1. Les noms et aliases sont les signaux les plus forts.

**Pas d embeddings** a moins de 1000 notes — voir [[pattern-fts5-aliases-vs-embeddings]].

Tokenizer : `unicode61 remove_diacritics 2` (pas de stemming, parite avec Obsidian).

Stop words : articles + prepositions uniquement. **Jamais** de mots d intention (erreur, probleme, bug) — voir [[erreur-mcp-stopwords-semantiques]].

Voir : [[sqlite-fts5-vault]] pour le detail technique.

## Etape 3 — Le serveur MCP

FastMCP en mode HTTP (`streamable-http`). 9 outils minimum :

| Outil | Lecture/Ecriture | Usage |
|-------|-----------------|-------|
| `search_brain` | R | Recherche FTS5 |
| `read_note` | R | Lire par nom ou alias |
| `read_note_by_path` | R | Lire par chemin |
| `get_backlinks` | R | Naviguer le graphe |
| `get_tags` | R | Vue structurelle |
| `get_property` | R | Lire frontmatter |
| `list_notes` | R | Lister un dossier |
| `vault_stats` | R | Stats globales |
| `create_note` | W | Creer une note |
| `append_note` | W | Ajouter du contenu |
| `update_property` | W | Modifier frontmatter (regex, PAS yaml.dump) |

**Piege** : `update_property` ne doit PAS round-tripper le YAML — voir [[erreur-mcp-yaml-dump-corruption]].

**Git sync desactive** : les commits sont geres par l agent, pas par le MCP. Sinon → branches parasites — voir `config.yaml : git.auto_commit: false`.

Voir : [[mcp-obsidian-brain-v2]] pour l implementation.

## Etape 4 — Integration Claude Code

### Auto-start (hook SessionStart)
```python
# .claude/hooks/mcp-autostart.py
# Verifie si le port repond, sinon lance start.py en process detache
```

### Rules (quand interroger)
```markdown
# .claude/rules/forge-brain-proactive.md
- Debut de session → search_brain contexte
- Avant de creer un composant → chercher erreurs + best practices
- Apres une erreur → creer note Knowledge/erreurs/
- Apres cc-news → capitaliser en notes atomiques
```

### Skill (pour les agents)
```yaml
# .claude/skills/forge-brain/SKILL.md
# Expose search, read, write aux agents
# Description = trigger ("Search, read, and write to the vault...")
```

## Etape 5 — Standard qualite

Le cerveau ne vaut que si les notes sont bien ecrites :

| Standard | Minimum | Pourquoi |
|----------|---------|----------|
| Aliases | 4-6 (FR + EN + domaine) | Les aliases = embeddings gratuits |
| Resume | 1 phrase specifique | search_brain affiche le resume |
| Tags | 2 (type + domaine) | Navigation structurelle |
| Wikilinks | 2 | Graphe navigable |
| derniere-maj | Date ISO | Detecter les notes stales |

Enforcer via warning dans `create_note` : "WARNING: seulement N aliases (minimum 4)".

## Anti-patterns documentes

- [[erreur-mcp-stopwords-semantiques]] — ne pas filtrer les mots d intention
- [[erreur-mcp-yaml-dump-corruption]] — ne pas round-tripper le YAML
- [[erreur-hooks-bash-quoting-windows]] — hooks portables cross-OS
- Auto-boost generique (injecter "knowledge" a 30+ notes = ranking inutile)

## Liens

- [[mcp-obsidian-brain-v2]] — implementation deployee
- [[sqlite-fts5-vault]] — pattern technique FTS5
- [[pattern-fts5-aliases-vs-embeddings]] — decision embeddings
- [[erreur-mcp-stopwords-semantiques]] — audit devil's advocate
- [[MOC-Techniques]]
