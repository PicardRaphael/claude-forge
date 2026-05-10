---
titre: "Critique MCP forge-brain — optimisation token et recherche"
resume: "Devil's advocate : 2 bugs (stop words intention, yaml.dump corruption), pas besoin d'embeddings a 187 notes, 4 ameliorations appliquees"
aliases:
  - "critique mcp forge-brain"
  - "critique MCP optimisation"
  - "devil advocate MCP mai 2026"
  - "forge-brain audit technique"
type: critique
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---

## Contexte

Audit technique du MCP forge-brain (SQLite FTS5, 187 notes) demande par Raphael. Question : "a-t-il besoin d'optimisation token/recherche ?"

## Verdict

**LIVRER AVEC CORRECTIONS** — architecture saine, 2 bugs actifs, pas besoin d'embeddings.

## 2 Bugs trouves (corriges)

### Bug 1 — Stop words semantiques
`STOP_WORDS_FR` contenait "probleme", "erreur", "bug", "souci". Ces mots d'intention etaient filtres silencieusement. `search_brain("erreur edit direct")` ignorait "erreur". Contradiction directe avec le workflow documente qui encourage les recherches `"erreur <topic>"`.

**Fix :** retire les 4 mots de la liste.

### Bug 2 — update_property corrompt le YAML
`yaml.dump()` round-trippait tout le frontmatter : reordonnait les cles, re-quotait les dates, wrappait les resumes, detruisait les commentaires. Chaque appel degradait silencieusement la note.

**Fix :** remplace par regex ciblee (insertion/remplacement de la propriete uniquement).

## 4 Ameliorations appliquees

1. `read_note(max_lines)` — truncation optionnelle pour economiser des tokens
2. `get_property` sur listes — retourne format lisible au lieu de `str(list)`
3. `create_note` — warning si < 4 aliases (enforce standard qualite)
4. Auto-boost retire — aliases generiques "knowledge"/"synthese" polluaient le ranking

## Decision embeddings

**NON a 187 notes.** FTS5 BM25 tourne en microsecondes. Les aliases (FR+EN+variantes) resolvent le fosse semantique. Seuil estime : embeddings pertinents a 1000-5000+ notes. La bonne optimisation : enforcer le standard aliases (4-6 min) a l'ecriture.

## Liens

- [[erreur-hooks-bash-quoting-windows]]
- [[sqlite-fts5-vault]]
- [[MOC-Techniques]]
