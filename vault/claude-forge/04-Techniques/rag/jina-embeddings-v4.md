---
titre: "Jina Embeddings v4"
resume: "3.8B params, seul modèle combinant single-vector ET multi-vector ColBERT en un seul modèle, multimodal texte+image, 89 langues, 32K context"
aliases:
  - "jina embeddings v4"
  - "jina v4"
  - "jina-embeddings-v4"
  - "jinaai embeddings v4"
  - "single-vector multi-vector ColBERT unified"
  - "jina 3.8B"
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://jina.ai/news/jina-embeddings-v4"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Jina Embeddings v4 est le premier modèle d'embedding qui combine **single-vector** (dense) ET **multi-vector ColBERT** dans un seul modèle unifié. 3.8B paramètres, multimodal (texte + image), 89 langues, 32K tokens de contexte.

> [!tip] Différenciateur clé
> Single-vector + ColBERT-style late interaction dans UN SEUL modèle — là où les autres imposent de choisir entre les deux approches.

## Spécifications

| Paramètre | Valeur |
|-----------|--------|
| Taille | 3.8B paramètres |
| Modalités | Texte + Image (multimodal) |
| Langues | 89 |
| Context window | 32K tokens |
| Architecture | Single-vector + Multi-vector (ColBERT) |
| LoRA adapters | 3 adapters spécialisés |

## Benchmarks

| Benchmark | Jina v4 | Référence concurrente |
|-----------|---------|----------------------|
| JinaVDR | **72.19** | ColPali : 64.50 |
| ViDoRe | **84.11** | — |

Surpasse [[ColPali]] (PaliGemma + ColBERT) sur la recherche visuelle documentaire.

## LoRA adapters

3 adapters LoRA intégrés permettant de spécialiser le modèle sans re-training complet :
1. **Retrieval** — optimisé pour la recherche documentaire
2. **Code** — spécialisé pour le code et les identifiants techniques
3. **Text-matching** — similarité sémantique précise

## Cas d'usage

- **RAG multimodal** — ingestion de PDFs, slides, images + texte dans le même index
- **Recherche multilingue** — 89 langues sans modèle séparé par langue
- **Hybrid search** — single-vector pour le recall rapide + multi-vector ColBERT pour la précision

## Comparaison avec Jina v3

| Feature | Jina v3 | Jina v4 |
|---------|---------|---------|
| Taille | Non précisé | 3.8B |
| Multimodal | Non | Oui (text+image) |
| Multi-vector | Non | Oui (ColBERT-style) |
| Langues | 89 | 89 |
| Context | 8K | 32K |
| MTEB | 65.5 | >65.5 |

## Liens

- [[rag-embeddings]] — Comparatif complet des modèles d'embedding
- [[RAG]] — Architecture RAG parent
- [[rag-reranking]] — Combiner Jina v4 multi-vector + reranking
- [[MOC-Techniques]]
