---
titre: "RAG en production — Patterns et defis"
resume: "Patterns et défis du RAG en production — chunking adaptatif, reranking multi-stage, évaluation continue, monitoring drift, gestion qualité embeddings à l'échelle."
aliases:
  - "rag production"
  - "RAG en production"
  - "rag prod patterns"
  - "production RAG"
  - "rag deployment"
  - "RAG observability"
type: technique
domaine: rag
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.anthropic.com/news/contextual-retrieval"
  - "https://arxiv.org/abs/2411.05276"
tags:
  - "#type/technique"
  - "#domaine/rag"
---

## Description

Déployer un RAG en production = stack complète : pipeline d'ingestion automatisé, retrieval multi-stage, observabilité fine, drift detection, cache sémantique, A/B testing. Le prototype qui fonctionne sur 100 docs n'est pas un système production. Cette note couvre les patterns et défis spécifiques au passage à l'échelle.

## Patterns clés production

### Pipeline d'ingestion

```
Collect → Clean → Deduplicate → Normalize → Chunk → Enrich metadata → Embed → Index
```

Détails dans [[rag-metadata]]. Convertir PDF → Markdown avant chunking est la meilleure pratique 2026. Hash documents pour ne re-embedder que les changements.

### Retrieval multi-stage

```
Query → Hybrid Search (BM25 + Dense, top-50) → RRF fusion → Reranker (top-5) → LLM
```

Pipeline standard production 2026. Voir [[rag-reranking]] pour benchmarks rerankers + [[rag-embeddings]] pour modèles d'embedding.

### Caching agressif

- **Cache sémantique** : seuil cosine ~0.80 ([arXiv 2411.05276](https://arxiv.org/abs/2411.05276)) → -68.8% appels LLM
- **Prompt caching** Anthropic : réduction jusqu'à 90% sur ingestion contextuelle
- **Pré-chauffer** contenu high-traffic en off-peak
- **Tiered retrieval** : BM25 cheap d'abord, dense en second

### Évaluation continue

Voir [[rag-evaluation]]. Pipeline CI/CD : golden set → re-évaluation à chaque release → blocage merge si métriques sous seuil. Boucle feedback prod : thumbs up/down → test cases auto.

## Défis production

### Drift detection

3 types ([[rag-metadata#Drift detection]]) :
- **Data drift** : distribution des documents change (nouvelles thématiques)
- **Query drift** : utilisateurs posent de nouvelles questions
- **Concept drift** : sens des termes évolue dans le temps

Solution : golden probe set frozen, re-embed weekly, mesurer shift cosinus. Arize Phoenix pour projection 2D/3D visuelle.

### Multi-tenancy

| Modèle | Isolation | Coût | Usage |
|--------|-----------|------|-------|
| **Silo** (index/tenant) | Forte | Élevé | Enterprise/compliance |
| **Pool** (metadata filter) | Faible | Bas | SMB |
| **Bridge** (hybride) | Moyen | Moyen | Bases mixtes |

### Coût à l'échelle

Pour 100K queries/jour, l'optimisation cache + tiered retrieval + model routing fait passer d'environ $19K/mois (configuration naïve) à environ $10K/mois (optimisée) — chiffres indicatifs, dépendent des tarifs API à date.

### Sécurité

Tools/MCP catalogues exposés → vecteurs d'attaque par injection ([ToolHijacker NDSS 2026](https://www.ndss-symposium.org/wp-content/uploads/2026-s675-paper.pdf), 96.7% succès attaque). Valider provenance des MCP tiers.

## Observabilité

### Plateformes 2026

- **Maxim AI** — full-stack agents
- **LangSmith** — natif LangChain
- **Arize Phoenix** — open-source, embedding viz
- **RAGAS** — métriques spécialisées
- **DeepEval** — CI/CD gates
- **Langfuse** — alternative open-source LangSmith

### Métriques cibles (seuils pratiques communauté)

Détails dans [[rag-metadata#Métriques cibles]]. Rappel : RAGAS ne prescrit **pas** de seuils canoniques — les 0.8+/0.9+ sont des recommandations pratiques.

## Pitfalls production

- **Pas de A/B testing** entre configurations → optimisations subjectives
- **Pas de drift detection** → dégradation silencieuse non détectée
- **Cache mal calibré** (seuil >0.95) → hit rate faible
- **Hot path LLM** pour metadata extraction → latence inutile (cacher Redis)
- **Pas de fallback** quand retrieval échoue → mauvaise UX

## Liens

- [[MOC-Techniques]]
- [[RAG]]
- [[rag-evaluation]]
- [[rag-architecture]]
- [[rag-metadata]]
- [[rag-reranking]]
- [[rag-embeddings]]
