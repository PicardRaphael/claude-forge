# Corpus RAG — 11 notes vault forge-brain

La profondeur (schémas JSON complets, papers, métriques chiffrées, comparatifs) vit dans le vault, pas ici. Lire via `mcp__forge-brain__read_note("<stem>")` SANS `max_lines`. Le stem est le nom nu (pas le chemin).

## Index

| Note (stem) | Quand la lire |
|---|---|
| `RAG` | point d'entrée, taxonomie, papers fondamentaux, experts/leaders, décision rapide |
| `rag-data-audit-discovery` | AVANT tout code : audit des questions (golden dataset), grille d'inventaire des sources, modélisation entités flat vs graph, audit qualité pré-ingestion, audit→décisions d'archi, cadres CODIR (Azure CAF) |
| `rag-data-models-par-cas-usage` | structurer le schéma de chunk : règle des 3 couches, 6 patterns, **8 schémas JSON concrets** (maintenance, proptech/Loji, support, juridique, e-commerce, médical, code, financier) |
| `rag-metadata` | principes métadonnées transverses, preprocessing, parsing documents, indexation, coûts, monitoring prod, A/B testing, limites Pinecone 40 KB / Qdrant index |
| `rag-chunking` | stratégies de découpage détaillées (recursive, semantic, late, contextual, AST), ChunkViz, 5 levels Greg Kamradt |
| `rag-embeddings` | modèles d'embedding 2026, fine-tuning, Matryoshka, quantization, dense vs sparse |
| `rag-reranking` | modèles de reranking, hybrid search, fusion RRF, comparatif scores |
| `rag-vector-databases` | comparatif vector DBs 2026 (pgvector, Qdrant, Pinecone, Weaviate…), support hybrid natif |
| `rag-architecture` | patterns avancés : GraphRAG, RAPTOR, Self-RAG, CRAG, Agentic, Contextual Retrieval |
| `rag-evaluation` | métriques retrieval + génération, RAGAS, DeepEval, golden set frozen, drift detection, pitfalls |
| `rag-production` | pipelines prod, monitoring, coûts, caching, semantic caching |

## Notes connexes (hors corpus RAG strict)

| Note | Lien |
|---|---|
| `briques-produit-ia-build-vs-buy` | OCR, embeddings, reranking, RAG-aaS au niveau build-vs-buy (→ skill `choix-outils-ia`) |
| `tool-retrieval-query-expansion` | query expansion/rewriting pour tool selection (Re-Invoke, OATS, TOOLQP) |
| `ai-act-eu-cheatsheet` + `rgpd-ia-cnil-article-22` | conformité PII/souveraineté d'un RAG sur données personnelles (→ skill `responsable-ia`) |

## Leaders RAG (fiches vault)

Douwe Kiela (paper RAG original, CEO Contextual AI) · Omar Khattab (ColBERT, DSPy) · Nils Reimers (Sentence-BERT, BEIR) · Jerry Liu (LlamaIndex) · Harrison Chase (LangChain/LangGraph) · Han Xiao (Jina, late chunking) · Greg Kamradt (ChunkViz) · Chip Huyen (AI Engineering) · James Briggs · Jonas Roman (RAG prod FR).
