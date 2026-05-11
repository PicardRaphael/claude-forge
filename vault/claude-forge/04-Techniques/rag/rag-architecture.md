---
titre: "RAG Architecture — Patterns avancés"
resume: "Patterns RAG avancés 2026 : GraphRAG, RAPTOR, Self-RAG, CRAG, Agentic RAG, query transformation, RAG vs fine-tuning vs long context"
aliases:
  - RAG architecture
  - advanced RAG
  - RAG patterns
  - patterns RAG avancés
  - agentic RAG
  - GraphRAG
domaine: ia
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://www.microsoft.com/en-us/research/project/graphrag/"
  - "https://arxiv.org/abs/2401.18059"
  - "https://selfrag.github.io/"
  - "https://arxiv.org/abs/2401.15884"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Au-delà du RAG basique, des patterns avancés permettent d'adresser les cas complexes : multi-hop, auto-correction, graph reasoning, et routage adaptatif.

## Query Transformation

Quand le RAG échoue, la retrieval est fautive **73% du temps**. La transformation de query adresse le gap sémantique.

- **HyDE** : LLM génère une réponse hypothétique, embed ce texte pour la recherche. Efficace en zero-shot sur queries courtes.
- **Multi-Query** : 3+ reformulations parallèles, merge/dedup/rerank. Pour queries ambiguës.
- **Step-Back Prompting** : question plus abstraite, retrouve documentation explicative plutôt que symptômes.
- **Query Decomposition** : split questions complexes en sous-questions focalisées.

Systèmes matures : **adaptation dynamique** — HyDE pour queries courtes, Multi-Query pour ambiguïté, Decomposition pour complexité.

## Agentic RAG

Stack production 2026 : **LangGraph** (orchestration, graphes cycliques) + **LlamaIndex Workflows** (retrieval) + RAGAS/Phoenix/Langfuse (évaluation).

- **LangGraph** : graphe dirigé cyclique avec branching conditionnel, checkpoints, human-in-the-loop
- **LlamaIndex** : Composite Retrieval APIs, `auto_routed` mode, routing multi-index
- **Adaptive RAG** : classifieur T5-large (~5-15ms) prédit difficulté query → no retrieval / single-step / multi-step. Coupe coûts de **30-50%**.

Coût : 3-10x plus de tokens, 2-5x latence. Justifié sur multi-hop, ambiguïté, high-stakes. Pas sur FAQ bots.

## GraphRAG (Microsoft)

Extrait knowledge graphs du texte, construit hiérarchies de communautés, génère résumés. **3.4x meilleure accuracy** que RAG traditionnel sur multi-hop complexe (80% vs 50%).

**LazyGraphRAG** : réduit coût indexation à **0.1% du GraphRAG complet**. Les deux disponibles via Microsoft Discovery sur Azure.

## RAPTOR (Stanford/Google)

Recursive Abstractive Processing : embed → cluster → résume → recurse vers le haut. Retrieval multi-niveau.

Coupling RAPTOR + GPT-4 : **+20% accuracy absolue** sur QuALITY benchmark. F-1 : +1.8 pts vs DPR, +5.3 pts vs BM25.

Extensions 2026 : **adRAP** (ajustement incrémental), **postQFRAP** (post-retrieval black-box compatible).

## Self-RAG

LM unique qui décide adaptativement de retriever et évalue sa propre sortie via **reflection tokens** :
1. Token retrieval : faut-il retriever ?
2. Passages multiples traités en parallèle avec évaluation pertinence
3. Tokens critique : évaluent factualité et qualité

**81% accuracy** fact-checking (vs 71% competing), **80% factualité** bio (vs 71% ChatGPT). Critique >90% agreement avec GPT-4.

## CRAG (Corrective RAG)

Évaluateur léger assigne score de confiance aux documents retrievés :
- **Correct** (haute confiance) → refine via decompose-then-recompose
- **Incorrect** (basse confiance) → discard, fallback web search
- **Ambiguous** → combine retrieval refiné + web search

Correct action : **78.1% accuracy** (+26.7 pts vs vanilla RAG). Reproduction open-source 2026 : pipeline Wikipedia 5 stages, 99% coverage.

## RAG vs Fine-tuning vs Long Context

**RAG résout un problème de connaissance. Fine-tuning résout un problème de comportement.** 60% des déploiements 2026 utilisent les deux.

### Long context (1M+ tokens)
- Gemini 1.5 Pro : 99.7% NIAH single-fact mais ~60% multi-fact réaliste
- "Lost in the middle" : -30% accuracy pour info positionnée centralement
- Plafond pratique : 32-64K tokens, pas les maximums annoncés
- Latence : ~60s pour 890K vs ~1s pour RAG
- Coût : ~$2/appel long-context vs ~$0.00008/query RAG (1250x)

### Anthropic recommande
Corpus < 200K tokens → full-context + prompt caching, skip retrieval.

### Pattern hybride 2026
RAG retrieve les documents les plus pertinents d'un grand corpus → charge dans un long context pour cross-document reasoning. RAG = scale (millions docs), long context = depth (centaines de pages).

## Évaluation (RAGAS)

| Métrique | Mesure | Ground truth ? |
|----------|--------|----------------|
| Context Precision | Ranking pertinent en haut | Non (LLM judge) |
| Context Recall | Toute info nécessaire retrievée | Oui |
| Faithfulness | Claims supportés par contexte | Non (LLM judge) |
| Answer Relevancy | Réponse adresse la question | Non (LLM judge) |

Seuils production : **>0.8** faithfulness et context precision. Top-k optimal : 4-8 chunks. Au-delà de 8, faithfulness se dégrade.

## Multi-Index / Multi-Source

73% des équipes enterprise (avril 2026) déploient hot/warm/cold indexes, coupant coûts embedding de **28-35%**.

- **Query routing** : classifieur/LLM détermine quel index interroger
- **Map-Reduce** : agents parallèles par sous-query/source, agrégation
- **Milvus 2.6** : dense + sparse dans la même collection, fusion single API

## Liens

- [[MOC-Techniques]]
- [[RAG]] — Index principal
- [[rag-chunking]] — Stratégies de découpage
- [[rag-reranking]] — Reranking et hybrid search
- [[rag-evaluation]] — Métriques détaillées
- [[rag-production]] — Pipelines production
- [[Jerry Liu]] — LlamaIndex, agentic retrieval
- [[Harrison Chase]] — LangChain, LangGraph
- [[Douwe Kiela]] — RAG original, RAG 2.0
- [[Omar Khattab]] — ColBERT, DSPy
