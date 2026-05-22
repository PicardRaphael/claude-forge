---
titre: "FTS5 + Aliases vs Embeddings — quand choisir quoi"
resume: "A moins de 1000 notes, BM25 + aliases riches bat les embeddings en cout, latence et simplicite. Les aliases SONT les embeddings pauvres-mais-efficaces."
aliases:
  - "aliases vs embeddings"
  - "FTS5 vs embeddings"
  - "BM25 vs vector search"
  - "quand embeddings vault"
  - "search strategy vault"
  - "pattern aliases recherche"
type: technique
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/rag"
---

## Decision

A 187 notes (vault forge-brain), FTS5 BM25 avec aliases riches est le bon choix. Pas d embeddings.

## Pourquoi BM25 + aliases gagne a petite echelle

| Critere | BM25 + Aliases | Embeddings |
|---------|---------------|------------|
| Latence | Microsecondes | 50-200ms (API call) |
| Cout | Zero (SQLite local) | $0.001-0.01/query (API) |
| Dependances | Zero | API provider ou modele local |
| Fosse semantique FR/EN | Resolu par aliases multilingues | Resolu par le modele |
| Precision | Excellent avec BM25 pondere | Excellent mais overkill |
| Maintenance | Aliases = effort humain | Modele = drift silencieux |

## Quand passer aux embeddings

- **1000+ notes** ET les aliases ne suffisent plus a couvrir le vocabulaire
- **Recherche semantique pure** ("notes similaires a celle-ci") sans mots-cles
- **Cross-lingue massif** (vault en 5+ langues)

A ce stade, hybrid search (BM25 0.4 + dense 0.6 + reranker) est le pattern.

## Les aliases SONT les embeddings manuels

Chaque alias ajoute est un vecteur semantique gratuit :
- "expert fine-tuning" → la note remonte pour "fine-tuning"
- "LoRA inventor" → la note remonte pour "LoRA"
- "fast fine-tuning" → la note remonte pour "rapide" via prefix match

Standard qualite : **4-6 aliases minimum** par note (FR + EN + variantes + domaine). C est l optimisation la plus rentable.

## Configuration BM25 optimale

```python
FTSWeights(file_stem=10.0, content=1.0, aliases=8.0)
```

- `file_stem x10` : le nom du fichier est le signal le plus fort
- `aliases x8` : quasi aussi fort — les aliases sont des synonymes curates
- `content x1` : baseline — le contenu peut matcher par accident

## Liens

- [[sqlite-fts5-vault]]
- [[RAG]]
- [[erreur-mcp-stopwords-semantiques]]
- [[MOC-Techniques]]
