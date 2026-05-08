---
titre: "SQLite FTS5 pour vault Obsidian"
resume: "Utiliser SQLite FTS5 comme moteur de recherche pour un vault Obsidian, sans dependance Obsidian"
aliases:
  - "FTS5 vault"
  - "SQLite full-text search vault"
  - "recherche plein texte vault"
  - "FTS5 obsidian"
  - "sqlite search MCP"
domaine: technique
type: technique
derniere-maj: 2026-04-29
auteur: claude
sources:
  - "[[mcp-obsidian-brain-v2]]"
tags:
  - "#type/technique"
  - "#domaine/technique"
---

## Description

Pattern pour indexer un vault Obsidian (fichiers .md) dans SQLite FTS5 et exposer la recherche via un serveur MCP. Remplace la dependance a la CLI/app Obsidian par un index autonome.

## Schema

5 tables : `notes` (contenu), `aliases` (resolution wikilink), `links` (backlinks), `tags`, `notes_fts` (FTS5 virtual table).

## Points cles

- **BM25 pondere** : `bm25(notes_fts, 10.0, 1.0, 8.0)` — nom x10, contenu x1, aliases x8. Les notes canoniques battent les meta-notes qui mentionnent le terme en passant.
- **Alias resolution** : `read_note("charges CC")` trouve `charges-copropriete.md` via la table aliases. Comme les wikilinks Obsidian.
- **Snippets natifs** : `snippet(notes_fts, 1, '>>> ', ' <<<', '...', 32)` — plus rapide que du Python maison.
- **Stop words FR** : filtrer "le", "la", "comment", "probleme", "erreur" avant la requete FTS5.
- **WAL mode** : `PRAGMA journal_mode=WAL` obligatoire pour multi-lecteurs.
- **Pas de stemming** : Obsidian n'en fait pas, on veut la parite.
- **brain.db est jetable** : si corrompu, supprimer et redemarrer. Reconstruit en ~5s.

## Quand utiliser

Quand on veut exposer un vault Obsidian a des agents/services sans installer Obsidian. Le vault reste des fichiers .md dans git, l'index est un cache recalculable.

## Exemple

```python
db = BrainDB(Path("brain.db"), FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
db.create_schema()
watcher = VaultWatcher(vault_path, db, excluded_dirs)
watcher.scan()  # 836 notes en 3.35s
results = db.search("charges copropriete", limit=5)
```

## Liens

- [[MOC-Techniques]]
- [[mcp-obsidian-brain-v2]]
