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
derniere-maj: 2026-05-08
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

Le chunking est l'étape la plus impactante du pipeline RAG. Un paper NAACL 2025 (Vectara) démontre que la **configuration de chunking a autant d'impact que le choix du modèle d'embedding**.

## Stratégies

### Recursive Character Splitting — Le défaut 2026

Utilise une hiérarchie de séparateurs (`"\n\n"`, `"\n"`, `". "`, `" "`). À 512 tokens + 50-100 tokens overlap : **69% accuracy** (FloTorch, 50 papers, 905K tokens) et **88-89% recall** (Chroma Research).

**C'est le benchmark à battre pour 80% des cas.**

### Semantic Chunking

Encode chaque phrase, détecte les baisses de similarité cosinus comme frontières de topic. Chroma mesure **91.9% recall** mais FloTorch seulement **54% accuracy** car fragments trop petits (43 tokens moyen). Plancher pratique : **200 tokens minimum**.

Variante NMF (2026, Journal of Supercomputing) : décomposition en topics latents, 19-32x speedup GPU.

### Late Chunking (Jina AI)

Inverse le pipeline "chunk-then-embed" en "embed-then-chunk" :
1. Document complet → modèle long-context (jina-embeddings-v3, 8192 tokens)
2. Chaque token reçoit un embedding contextuel
3. Segmentation en chunks via span annotations
4. Mean pooling par chunk

**+6.5 points nDCG@10** sur NFCorpus. Approche qualité LLM-augmented (0.8516 vs 0.8590). Idéal pour documents avec pronoms, cross-références, dépendances contextuelles.

### Contextual Chunking (Anthropic)

Claude lit chaque chunk + document complet, génère un préfixe de 50-100 tokens pour situer le chunk. Résultats (cumulatifs) :
- Contextual Embeddings seuls : **-35% échecs retrieval**
- + Contextual BM25 : **-49%**
- + Reranking : **-67%** (5.7% → 1.9%)

Coût : **$1.02 / million tokens** avec prompt caching. Skip si corpus < 200K tokens.

### Hierarchical (Parent-Child)

- Parents (500-2000 tokens) : contexte cohérent pour génération
- Enfants (100-500 tokens) : retrieval précis
- H-RAG (SemEval-2026) : fenêtres 3 phrases, stride 2 → nDCG@5 de 0.4728

Résout la tension fondamentale : **recall demande petits chunks, génération demande grands chunks**.

### Agentic Chunking

LLM lit chaque proposition, décide si elle appartient à un chunk existant ou en démarre un nouveau. Greg Kamradt "Level 5". Coût : $0.01-0.10 par document de 10K mots.

Évolution 2026 : **meta-agentic chunking** — l'agent analyse les caractéristiques du document et sélectionne la stratégie par type.

### Code Chunking (AST-based)

**cAST** (CMU/Augment Code, 2025) : fusionne les noeuds AST jusqu'à un budget de taille. StarCoder2-7B gagne **+5.5 pts RepoEval**, **+4.3 CrossCodeEval**, **+2.7 SWE-bench**.

**tree-sitter** = backend dominant. Implémentations : `code-chunk` (Supermemory AI), `code-splitter` (Rust).

### Multimodal Chunking

- **Vision-Guided** (2025-2026) : LMM traite pages PDF par lots, préserve cohérence multi-pages
- **MultiDocFusion** (2026) : pipeline hiérarchique, **+8-15% precision retrieval**
- Tables : toujours chunker comme unités complètes, jamais couper une table

## Tailles optimales

| Cas d'usage | Taille optimale | Source |
|-------------|----------------|--------|
| Défaut général | 400-512 tokens | FloTorch 2026, Chroma |
| Queries factuelles | 256-512 tokens | NVIDIA |
| Queries analytiques | 512-1024 tokens | NVIDIA |
| Documents financiers | 1024 tokens | NVIDIA |
| Plancher minimum | 200 tokens | Vectara NAACL 2025 |

**Context cliff à ~2500 tokens** : qualité chute fortement au-delà.

## Overlap

Consensus 2026 : **10-20% overlap** (50-100 tokens pour chunks de 512). Microsoft Azure recommande jusqu'à 25%.

Étude janvier 2026 (SPLADE + Mistral-8B) : overlap **sans bénéfice mesurable** en sparse retrieval. Tester avant de payer le surcoût.

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
