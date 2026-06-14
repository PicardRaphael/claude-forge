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
derniere-maj: 2026-06-14
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

## Trajectoire & déclencheur de ré-audit

> Ajout 2026-06-14 — suite au croisement avec la vidéo « Obsidian + Claude » (IA Talkshow), qui prône embeddings + reranker. Verdict : à notre échelle, inutile ; le fossé sémantique est **latent, pas actif**. Capitalisation du déclencheur pour ne pas rater la bascule.

**Trajectoire du vault forge-brain** : note écrite à **187 notes** → **487 notes** (juin 2026) → seuil de bascule documenté = **1000 notes**. On est encore confortablement sous le seuil.

**Pourquoi pas d'action maintenant (mesure avant optim)** : le moteur empile déjà 4 garde-fous au niveau requête (prefix match `"terme"*`, expansion OR, alias-expansion, variantes pluriel/féminin via `_like_variants`) + 2 couches actives — aliases (~5,8/note en moyenne, au-dessus du minimum 4-6) et **l'agent qui relance avec un autre mot** quand une recherche rate. **Aucun raté de synonyme récurrent mesuré** → construire une couche synonymes maintenant = feature spéculative (cf [[feedback_measure_before_optimize]] + [[feedback_drift_implementation_karpathy_organes_morts]] : « un manque n'est un défaut que s'il a un consommateur »).

**Déclencheur de ré-audit** — ré-évaluer BM25-vs-embeddings dès que l'UN survient :
- le vault atteint **~1000 notes**, OU
- on observe **2-3 vrais ratés de synonyme** récurrents (consommateur réel, pas théorique — ex : recherche « automobile » qui rate une note ne parlant que de « voiture », répété).

**Drop-in pré-conçu (le jour où le déclencheur tombe)** : la réponse n'est PAS d'abord les embeddings, mais une **couche synonymes query-time** — un `synonyms.yaml` curaté, appliqué dans `database.py` (~ligne 198, après tokenization, avant les stratégies FTS), expansion **additive** (OR) en conservant les termes originaux pour l'alias-expansion. Coût : ~40 lignes, **zéro réindexation** (l'expansion agit à la requête, l'index FTS5 reste intact). Embeddings vectoriels seulement si le dict sature (cross-lingue massif ou recherche sémantique pure sans mot-clé).
