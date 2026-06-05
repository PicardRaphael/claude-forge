---
titre: "RAG Chunking — Stratégies de découpage"
resume: "Comparatif complet des stratégies de chunking RAG 2026 : recursive, semantic, late, contextual, AST, hierarchical — avec benchmarks"
aliases:
  - RAG chunking
  - chunking strategies
  - text splitting
  - découpage de texte
  - chunk size
  - stratégies de chunking
domaine: ia
type: technique
derniere-maj: 2026-06-05
auteur: claude
sources:
  - "https://blog.premai.io/rag-chunking-strategies-the-2026-benchmark-guide/"
  - "https://www.anthropic.com/news/contextual-retrieval"
  - "https://jina.ai/news/late-chunking-in-long-context-embedding-models/"
  - "https://arxiv.org/html/2506.15655v1"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---
## Description

Le chunking est l'étape la plus impactante du pipeline RAG. Le paper [NAACL 2025 (Vectara + UW-Madison)](https://aclanthology.org/2025.findings-naacl.114.pdf) — "Is Semantic Chunking Worth the Computational Cost?" (Qu, Tu, Bao) — démontre que **la configuration de chunking a un impact comparable au choix du modèle d'embedding** ("better chunking and large embeddings provide complementary benefits").

## Stratégies

### Recursive Character Splitting — Le défaut 2026

Utilise une hiérarchie de séparateurs (`"\n\n"`, `"\n"`, `". "`, `" "`). À 512 tokens + **10-20% overlap** (consensus benchmarks 2026) : **69% accuracy** ([FloTorch 2026](https://www.flotorch.ai/blogs/rag-benchmarking-of-amazon-nova-and-gpt-4o-models), 50 papers académiques) et ~88-89% recall (Chroma Research benchmarks).

**C'est le benchmark à battre pour 80% des cas.**

### Semantic Chunking

Encode chaque phrase, détecte les baisses de similarité cosinus comme frontières de topic. Chroma mesure **91.9% recall** mais FloTorch seulement **54% accuracy** car fragments trop petits (43 tokens moyen). Plancher pratique : **200 tokens minimum**.

Variante NMF ([Journal of Supercomputing 2026](https://link.springer.com/article/10.1007/s11227-026-08370-3)) : décomposition en topics latents, **19.6×–32.6× speedup GPU**.

### Late Chunking (Jina AI)

Inverse le pipeline "chunk-then-embed" en "embed-then-chunk" :
1. Document complet → modèle long-context (jina-embeddings-v3, 8192 tokens)
2. Chaque token reçoit un embedding contextuel
3. Segmentation en chunks via span annotations
4. Mean pooling par chunk

**+6.5 points nDCG@10** sur NFCorpus (Late Chunking 29.98 vs naive 23.46). Sur Table 4 du paper : Late Chunking 0.8516 vs Contextual Embedding Anthropic 0.8590 — Late Chunking avantage : sans LLM supplémentaire à l'ingestion. Idéal pour documents avec pronoms, cross-références, dépendances contextuelles.

### Contextual Chunking (Anthropic)

Claude lit chaque chunk + document complet, génère un préfixe de 50-100 tokens pour situer le chunk. Résultats (cumulatifs) :
- Contextual Embeddings seuls : **-35% échecs retrieval**
- + Contextual BM25 : **-49%**
- + Reranking : **-67%** (5.7% → 1.9%)

Coût : **$1.02 / million tokens** avec prompt caching. Skip si corpus < 200K tokens.

### Hierarchical (Parent-Child)

- Parents (500-2000 tokens) : contexte cohérent pour génération
- Enfants (100-500 tokens) : retrieval précis
- H-RAG ([SemEval-2026, arXiv 2605.00631](https://arxiv.org/abs/2605.00631)) : fenêtres 3 phrases, stride 2 → **nDCG@5 0.4271** sur Task A

Résout la tension fondamentale : **recall demande petits chunks, génération demande grands chunks**.

### Agentic Chunking
### Scoring de pertinence à l'ingestion (write-time)

Pattern observé chez [[Jonas Roman]] (pipeline ZParse, vidéo 20 mai 2026), complémentaire au reranking : plutôt que de filtrer le bruit au *retrieval-time*, on note chaque chunk **dès l'ingestion**.

- Pendant la phase d'enrichissement, un LLM-as-judge attribue à chaque chunk un **`relevant_score` 1-10** selon le cas d'usage métier (ex : « pertinence pour le diagnostic de panne »), via function calling structuré.
- Filtre seuil à l'ingestion (ex : `>= 5`) → les chunks sous le seuil ne sont jamais vectorisés. Curseur de granularité ajustable selon la qualité observée en sortie.
- Gain : la base vectorielle ne contient que du signal → moins de distracteurs, meilleure précision au scale, coût de stockage/embedding réduit. Exemple vidéo : 428 chunks → 227 après filtre `>=5`.
- Champs métadonnée enrichis en parallèle (symptôme, cause, solution, page, équipement…) ; valeur par défaut `null`/`-1` si absent pour ne pas bloquer le pipeline.

**Write-time scoring vs retrieval-time reranking** : le scoring write-time est un filtre *statique* one-shot (payé une fois à l'ingestion, dépend du cas d'usage figé) ; le reranking ([[rag-reranking]]) est *dynamique* par requête (s'adapte à chaque query). Les deux sont composables : filtrer le bruit à l'ingestion PUIS reranker au retrieval. Limite du write-time : un chunk jugé non pertinent pour le cas d'usage prévu est définitivement perdu pour tout autre usage de la même base.

LLM lit chaque proposition, décide si elle appartient à un chunk existant ou en démarre un nouveau. Greg Kamradt "Level 5". Coût : $0.01-0.10 par document de 10K mots.

Évolution 2026 : **meta-agentic chunking** — l'agent analyse les caractéristiques du document et sélectionne la stratégie par type.

### Code Chunking (AST-based)

**cAST** ([CMU, EMNLP 2025 Findings, arXiv 2506.15655](https://aclanthology.org/2025.findings-emnlp.430/)) : fusionne les noeuds AST jusqu'à un budget de taille. StarCoder2-7B gagne **+5.5 pts RepoEval**, **+4.3 CrossCodeEval**, **+2.7 SWE-bench**.

**tree-sitter** = backend dominant. Implémentations : `code-chunk` (Supermemory AI), `code-splitter` (Rust).

### Multimodal Chunking

- **Vision-Guided** (2025-2026) : LMM traite pages PDF par lots, préserve cohérence multi-pages
- **MultiDocFusion** ([arXiv 2604.12352](https://arxiv.org/abs/2604.12352), 2026) : pipeline hiérarchique, **+8-15% precision retrieval**
- Tables : toujours chunker comme unités complètes, jamais couper une table

## Tailles optimales

| Cas d'usage | Taille optimale | Source |
|-------------|----------------|--------|
| Défaut général | 400-512 tokens | FloTorch 2026, Chroma |
| Queries factuelles | 256-512 tokens | [NVIDIA](https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/) |
| Queries analytiques | 1024 tokens | NVIDIA |
| Documents financiers | 512-1024 tokens | NVIDIA |
| Plancher minimum | 200 tokens | Vectara NAACL 2025 |

**Context cliff à ~2500 tokens** : qualité chute fortement au-delà ([arXiv 2601.14123](https://arxiv.org/abs/2601.14123), SPLADE + Mistral-8B, janvier 2026).

## Overlap

Consensus 2026 : **10-20% overlap** (50-100 tokens pour chunks de 512). Microsoft Azure recommande jusqu'à 25%.

Étude janvier 2026 ([arXiv 2601.14123](https://arxiv.org/abs/2601.14123), SPLADE + Mistral-8B) : *"overlap provides no measurable benefit and increases indexing cost"* en sparse retrieval. Tester avant de payer le surcoût.

## Quand utiliser quoi

1. **Défaut** → recursive 400-512 tokens, 10-20% overlap
2. **PDFs paginés** → page-level chunking
3. **Précision domaine** → semantic chunking (min 200 tokens)
4. **Documents longs cross-référentiels** → late chunking (Jina)
5. **High-stakes** → contextual retrieval Anthropic ($1.02/M tokens)
6. **Code** → AST via tree-sitter
7. **Multimodal** → vision-guided + hierarchical assembly
8. **Retrieval précis + génération cohérente** → parent-child

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[rag-embeddings]] — Impact du chunking sur les embeddings
- [[rag-metadata]] — Metadata-aware chunking
- [[Greg Kamradt]] — 5 Levels of Text Splitting
- [[Han Xiao]] — Late chunking (Jina AI)
