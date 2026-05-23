---
titre: "ColPali — Vision-based document retrieval"
resume: "Modèle de retrieval multimodal vision-based — PaliGemma + ColBERT late interaction sur images de pages, élimine le pipeline OCR/parsing/chunking."
aliases:
  - "ColPali"
  - "colpali"
  - "col pali"
  - "vision retrieval"
  - "document retrieval vision"
  - "PaliGemma ColBERT"
type: technique
domaine: rag
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://arxiv.org/abs/2407.01449"
  - "https://huggingface.co/vidore/colpali"
tags:
  - "#type/technique"
  - "#domaine/rag"
  - "#domaine/multimodal"
---

## Description

**ColPali** ([arXiv 2407.01449](https://arxiv.org/abs/2407.01449), Faysse et al., ICLR 2025) est un modèle de retrieval multimodal qui traite les documents comme **des images** plutôt que comme du texte. Il combine **PaliGemma** (VLM) avec une architecture **ColBERT late interaction** appliquée aux patches d'image.

Élimine le pipeline OCR/parsing/chunking traditionnel en utilisant directement la représentation visuelle du document pour le retrieval.

## Architecture

1. Chaque page de document est encodée comme une image
2. PaliGemma extrait des embeddings par patch (multi-vector)
3. Late interaction ColBERT-style : score MaxSim entre query tokens et patches d'image
4. Retrieval direct sur le pool d'images de pages

## Avantages

- **Pas de pipeline OCR/parsing** — la couche visuelle preserve layout, tableaux, graphiques
- **Gère nativement** tableaux complexes, graphiques, layouts multi-colonnes, formulaires
- **Performance supérieure** sur documents structurés vs RAG textuel classique
- **Robuste aux scans** et documents mal parsés par OCR

## Benchmark — ViDoRe

Le benchmark **ViDoRe** (Visual Document Retrieval) est devenu le standard pour les modèles vision-RAG. ColPali a établi la baseline. Concurrents 2025-2026 :

| Modèle | JinaVDR | ViDoRe |
|--------|---------|--------|
| ColPali (v1.2) | 64.50 | baseline |
| [[jina-embeddings-v4|Jina v4]] (3.8B, single-vector) | **72.19** | **84.11** |
| Jina v4 (multi-vector) | — | **90.17** |

## Quand utiliser ColPali

- Corpus de **PDFs avec layouts complexes** (rapports financiers, papers scientifiques, slides)
- Documents avec **tableaux et graphiques** importants pour la sémantique
- Cas où **l'OCR fait perdre de l'information** (scans, manuscrits, formulaires)
- Pas de budget pour pipeline parsing complexe

## Quand ne pas utiliser

- Corpus 100% texte propre (markdown, web articles) → embeddings text classiques suffisent
- Latence critique sub-50ms — ColPali multi-vector est plus coûteux que dense
- Très grands corpus sans GPU (multi-vector pèse en stockage)

## Évolutions

- **ColQwen2** (suite de ColPali) — base Qwen2-VL
- **Jina v4 multi-vector** ([[jina-embeddings-v4]]) — surpasse ColPali sur les benchmarks
- **ColNomic** — variante open-source

## Liens

- [[MOC-Techniques]]
- [[RAG]]
- [[jina-embeddings-v4]] — alternative 3.8B unifiée
- [[rag-embeddings]] — comparatif modèles embedding
- [[Omar Khattab]] — ColBERT late interaction
