---
titre: "RAG Metadata — Stratégies et data optimization"
resume: "Métadonnées RAG, preprocessing, parsing documents, indexation, coûts, monitoring production, A/B testing"
aliases:
  - RAG metadata
  - metadata filtering
  - data preparation RAG
  - preprocessing RAG
  - RAG data optimization
  - metadata strategies
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://unstructured.io/insights/how-to-use-metadata-in-rag-for-better-contextual-results"
  - "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Les métadonnées et la qualité des données sont les fondations d'un RAG performant. Un mauvais preprocessing condamne la retrieval avant même que le modèle ne soit choisi.

## Métadonnées essentielles par type

| Type document | Champs clés |
|---------------|-------------|
| PDFs | page_number, section_heading, table_id, figure_id, extraction_confidence |
| Code | language, file_path, function_name, class_name, repo, commit_hash |
| Emails | sender, recipients, date, thread_id, subject, has_attachments |
| Slack/Chat | channel, author, timestamp, thread_ts, reactions_count |
| Bases de données | table_name, column_name, row_id, schema_version, last_updated |

Qdrant supporte autant de payload indexes que nécessaire ([doc Qdrant payload](https://qdrant.tech/documentation/manage-data/payload/)) — chaque index consomme RAM. Règle empirique : 10-15 champs restent gérables sous 1M points.

## Pre-filtering vs Post-filtering

**Pre-filtering** (recommandé) : narrowe l'espace de recherche avant similarité. Réduit bruit et améliore vitesse.

**Post-filtering** : gaspille les slots retrieval. À 50 tenants, 10M docs : retourne < k résultats **30% du temps** sur queries restrictives.

## Auto-extraction metadata par LLM

Pattern dominant : function calling + Pydantic models. `SelfQueryRetriever` = +200-500ms (gpt-4o-mini). **Cacher les filtres extraits** via Redis pour queries répétées.

Architecture multi-niveau (paper financier) : résumés document-level, entités clés, clusters thématiques + enrichissements chunk-level.

## Pipeline preprocessing

```
Collect → Clean → Deduplicate → Normalize → Chunk → Enrich metadata → Embed → Index
```

**Convertir PDF → Markdown avant chunking** = meilleure pratique 2026.

## Outils de parsing 2026

| Outil | Spécialité | Tables complexes | Prix |
|-------|-----------|-----------------|------|
| Unstructured.io | 64-70+ formats, SOC 2/HIPAA Enterprise | 75% réduction erreurs préparation données | Managed |
| LlamaParse | LlamaIndex-native | Bon | 10K crédits free/mois |
| Docling (IBM) | Self-hosted, open-source | **97.9%** (benchmark Procycons 2025 sustainability reports) | Gratuit |
| Reducto | Enterprise compliance | Élevé | SOC 2 Type II |
| Amazon Textract | AWS, formulaires, manuscrit | Bon | Pay-per-page |
| Mistral OCR 3 (déc 2025) | Multilingue (chinois, EU-est/ouest, EN) | Bon | API |

**Tables** : toujours extraire structurellement, sérialiser en **Markdown** (20-40% moins de tokens vs HTML clean, jusqu'à 68-87% vs HTML "réel" avec balises/scripts ; meilleur raisonnement LLM). Jamais couper une table entre chunks.

## Indexation optimisée

### Multi-vector
Index multiple représentations : petits chunks pour retrieval précis, parents pour contexte. [[rag-architecture#RAPTOR]] construit des hiérarchies résumées.

### Time-aware
**TG-RAG** (Temporal GraphRAG) : graphes bi-niveau temporels. Retrieval local (faits dans une fenêtre) + global (tendances via résumés temporels). Update-friendly.

### Multi-tenancy

| Modèle | Isolation | Coût | Usage |
|--------|-----------|------|-------|
| Silo | Forte (index séparé/tenant) | Élevé | Enterprise/compliance |
| Pool | Faible (metadata filters) | Bas | SMB |
| Bridge | Hybride | Moyen | Bases mixtes |

## Optimisation des coûts

### Caching
- Cache sémantique : seuil cosine **~0.80** optimal selon [GPT Semantic Cache paper (arXiv 2411.05276)](https://arxiv.org/abs/2411.05276) — **-68.8% appels LLM** à ce seuil. Seuil >0.95 = trop strict (faible hit rate). Estimations communauté : -30-50% appels API selon traffic.
- Pré-chauffer contenu high-traffic en off-peak
- Hash documents : ne re-embedder que les changements

### Tiered retrieval
BM25 cheap d'abord, dense reranking ensuite. Matryoshka 256d pour shortlisting, full dims pour reranking. Routage intelligent : **-30-45% coûts, -25-40% latence**.

### Model routing
Queries simples → modèle cheap (Haiku, GPT-4o-mini). Complexes → modèle puissant (Opus, GPT-5.5). Batch embed en off-peak, **jamais dans le hot path**.

Pour 100K queries/jour : $10.5K/mois optimisé vs $19.5K/mois naif.

## Monitoring production

### Métriques cibles

Seuils pratiques recommandés (communauté RAG — **non canoniques [RAGAS docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)** qui ne prescrivent pas de thresholds). Métriques système (latence) à séparer des métriques RAGAS.

| Métrique | Cible (pratique) | Couche |
|----------|------------------|--------|
| Faithfulness | >= 0.9 | Génération (RAGAS) |
| Answer Relevancy | >= 0.85 | Génération (RAGAS) |
| Context Precision | >= 0.8 | Retrieval (RAGAS) |
| Context Recall | >= 0.8 | Retrieval (RAGAS) |
| Hit Rate | >= 0.9 | Retrieval |
| Hallucination Rate | < 5% | Génération |
| Latence p95 | < 2s (450ms cached) | Système (hors RAGAS) |

### Drift detection
3 types : Data Drift, Query Drift, Concept Drift. Golden probe set frozen, re-embed weekly, mesurer shift cosinus. **Arize Phoenix** : projection 2D/3D pour detection visuelle.

### Feedback loops
Thumbs up/down → NPS système. Hallucinations flaggées → test cases automatiques (CI/CD via DeepEval). **Crucible** (arXiv jan 2026) : système Nugget-Augmented Generation, évalué TREC NeuCLIR 2024 (recherche académique, pas framework production établi).

### Plateformes observabilité
1. Maxim AI — full-stack
2. LangSmith — deep LangChain
3. Arize Phoenix — open-source, embedding viz
4. RAGAS — évaluation spécialisée
5. DeepEval — CI/CD gates

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[rag-chunking]] — Metadata-aware chunking
- [[rag-embeddings]] — Modèles d'embedding
- [[rag-production]] — Pipelines production
- [[rag-evaluation]] — Métriques détaillées
