---
titre: "Tool Retrieval — Query Expansion & Rewriting pour Tool Selection"
resume: "État de l'art 2024-2026 des techniques de query expansion/rewriting appliquées à la sélection d'outils (pas au RAG documentaire) — Re-Invoke, TOOLQP, OATS, ToolRerank, ToolShed"
aliases:
  - tool retrieval
  - query expansion tool selection
  - query rewriting tools
  - tool RAG
  - tool selection retrieval
  - Re-Invoke
  - OATS tool selection
  - TOOLQP
  - ToolRerank
  - ToolShed
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://arxiv.org/abs/2408.01875"
  - "https://arxiv.org/abs/2601.07782"
  - "https://arxiv.org/abs/2603.20313"
  - "https://arxiv.org/abs/2603.13426"
  - "https://arxiv.org/abs/2506.01056"
  - "https://arxiv.org/abs/2403.06551"
  - "https://arxiv.org/abs/2410.14594"
  - "https://www.ndss-symposium.org/wp-content/uploads/2026-s675-paper.pdf"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
  - "#domaine/agents"
  - "#domaine/tool-selection"
---

## Le problème

Quand un agent LLM a accès à un grand catalogue d'outils (50-1000+), mettre toutes les descriptions dans le contexte échoue :
- **Token cost** : 741 tools ≈ 120K tokens/requête ([vLLM Semantic Router blog](https://vllm-semantic-router.com/blog/semantic-tool-selection/), corroboré par MCP-Zero 248.1k tokens / 2797 tools)
- **Dégradation non-linéaire** : accuracy chute de 64% à 20% entre 207 et 417 tools — cliff, pas pente (via vLLM blog, source académique primaire à tracer)
- **Lost in the Middle (tools)** : tools au milieu du contexte = 22-52% accuracy vs début/fin (vLLM blog appliquant le concept général de [Liu et al. 2023](https://arxiv.org/abs/2307.03172) au tool selection — les chiffres précis sont du blog, pas du paper original)
- **Contre-intuitif** : fournir 3-5 tools pertinents > fournir tous les tools (paper MCP Semantic Discovery)

La solution = **retrieve-then-select** : réduire à 3-10 tools via retrieval, puis LLM choisit dans cette short-list.

## Techniques pré-retrieval (Query Expansion/Rewriting)

### Re-Invoke (Google, EMNLP 2024)

Le plus pertinent pour du tool selection unsupervised.

1. **Tool Indexing** : générer des queries synthétiques diversifiées par outil
2. **Query Rewriting** : LLM extrait les intents et le contexte clé de la query user
3. **Multi-View Similarity** : ranker par similarité intent-based multi-vue

Résultats : **+20% nDCG@5** single-tool, **+39% multi-tool** (ToolE datasets). Aucune donnée labellisée requise.

Insight clé : réécrire la query en "langage outil" (pas en langage user).

### TOOLQP — "Beyond Single-Shot" ([MIT, Janvier 2026](https://arxiv.org/abs/2601.07782))

Paper : *"Beyond Single-Shot: Multi-step Tool Retrieval via Query Planning"* (Wei Fang, James Glass — MIT, 12 janvier 2026). Verbatim abstract : *"we propose TOOLQP, a lightweight framework that models retrieval as iterative query planning"*.

Modélise la retrieval comme **planification itérative** :

1. Planner décompose en sous-tâches séquentielles
2. Par sous-tâche : génère query → retrieve → self-correct
3. "Peak-rank aggregation" : rang final = meilleur rang sur toutes les sous-queries

Découvre les **dépendances inter-outils implicites** (ex: auth token avant password tool). Optimisation via RLVR (Reinforcement Learning with Verifiable Rewards) confirmée. Taille modèle (1.7B) et gain (+3-6% vs Re-Invoke/cross-encoder) cités dans les tables du paper PDF.

### HyDE (Hypothetical Document Embeddings)

Générer une description d'outil hypothétique depuis la query, embedder ça au lieu de la query brute. Fonctionne car le doc hypothétique est plus proche en espace embedding de la vraie description.

## Techniques intra-retrieval

### Semantic Tool Discovery pour MCP (Mars 2026)

- Index tool descriptions comme dense embeddings
- Top 3-5 tools par query au lieu d'exposer 50-100+
- **99.6% réduction tokens**, **97.1% hit rate à K=3**, **MRR 0.91** sur 121 tools (140 queries)
- Sub-100ms latence

Source : [arXiv 2603.20313](https://arxiv.org/abs/2603.20313) — "Semantic Tool Discovery for Large Language Models" (Mudunuri, Wan, Qin, Manoharan, mars 2026).

### MCP-Zero — Routing hiérarchique

Paper : [arXiv 2506.01056](https://arxiv.org/abs/2506.01056) — "MCP-Zero: Active Tool Discovery for Autonomous LLM Agents" (Fei, Zheng, Feng, juin 2025).

Coarse-to-fine en 2 étapes : filtrer les serveurs MCP candidats → puis retriever les tools spécifiques. **308 MCP servers**, **2,797 tools** (officiel Model-Context-Protocol repository). **98% réduction tokens** sur APIBank. Sélection précise depuis ~3k candidats sur 248.1k tokens.

## Techniques post-retrieval (Reranking)

### ToolRerank ([arXiv 2403.06551, LREC-COLING 2024](https://arxiv.org/abs/2403.06551))

Zheng, Li, Liu, Liu, Luan, Wang — soumis 11 mars 2024. Deux innovations :
- **Adaptive Truncation** : positions différentes pour tools vus vs non-vus
- **Hierarchy-Aware** : concentre pour single-tool, diversifie pour multi-tool

Finding : reranker sur top-50 peut dégrader vs DPR — top-10 OK, ne pas over-retrieve (claim à sourcer précisément dans les tables du paper, l'abstract dit uniquement "ToolRerank can improve the quality").

### ToolShed (Octobre 2024) — Pipeline complet

3 phases RAG-Tool Fusion :
- Pré-retrieval : enrichir docs tools avec queries synthétiques + topics clés
- Intra : query planning + transformation
- Post : reranking + self-reflection (agent évalue si tools suffisants, peut re-query)

## Apprentissage offline

### OATS — Outcome-Aware Tool Selection ([arXiv 2603.13426](https://arxiv.org/abs/2603.13426))

"Outcome-Aware Tool Selection for Semantic Routers: Latency-Constrained Learning Without LLM Inference" (Chen, Liu, Jiang, He, Liu — mars 2026). Le plus pertinent pour la production high-throughput.

- Interpole embeddings des tools vers le centroïde des queries qui ont **réussi**
- **Zéro coût runtime** : single-digit millisecond CPU budgets, pas de LLM call
- NDCG@5 : **0.869 → 0.940 sur MetaTool** (199 tools, 4287 queries) — verbatim abstract
- Sur "similar choices" (cas les plus durs) : 83.4% vs 73.5% (Vicuna-7b) — chiffres dans tables paper

Limitation : borné par la capacité du modèle d'embedding de base. Si MiniLM-L6 ne distingue pas deux tools, le raffinement n'aidera pas.

Pré-requis : traces (query, tool, succès/échec) — ~10 traces/tool minimum.

## Comparatif par contexte

| Technique | Meilleur pour | Latence | Entraînement ? | Échelle |
|-----------|--------------|---------|----------------|---------|
| Re-Invoke | Général, unseen tools | Moyen (1 LLM call) | Non | 100s tools |
| TOOLQP | Multi-tool complexe | Haut (multi-step) | Oui (RLVR) | 1000s tools |
| Semantic vector | MCP / gros catalogues | Bas (<100ms) | Embeddings seuls | 100s-1000s |
| OATS | Prod high-throughput | Très bas (3-7ms) | Offline seul | 100s tools |
| ToolRerank | Affiner retrieval initiale | Moyen | Fine-tuned reranker | 100s tools |
| ToolShed | Accuracy maximale | Haut | Non (modulaire) | 100s tools |
| Few-shot examples | Quick win, toute échelle | Nul (prompt) | Non | Tout |

## Pipeline recommandé (production)

```
1. Semantic vector pre-filter (sub-100ms, top 10-20)
2. Query rewriting Re-Invoke style (améliore recall)
3. Reranking top-10 (améliore precision → top 3-5)
4. OATS offline (feedback loop hebdo)
```

## Sécurité — ToolHijacker ([NDSS 2026](https://www.ndss-symposium.org/wp-content/uploads/2026-s675-paper.pdf))

**96.7% de succès d'attaque** par injection de description d'outil malveillante dans le catalogue (shadow LLM Llama-3.3-70B, target GPT-4o, benchmark MetaTool, méthode gradient-free). À considérer si tools de sources externes (MCP tiers).

## Application NeoChat

NeoChat implémente déjà un pipeline 10 étapes ([[neochat-tool-rag]]) :
- Query expansion via Gemini Flash avec heuristique `_should_expand_query()`
- Hybrid search pgvector (tsvector + semantic + RRF)
- LLM reranking (skip si ≤5 candidats ou scores bien séparés)
- Domain pre-filter centroïde

Évolution envisagée :
1. **Lazy Expansion** — supprimer `_CLEAR_KEYWORDS` heuristique, remplacer par : search brut → score bas → LLM rewrite Re-Invoke → re-search
2. **OATS** — pipeline offline Langfuse → shift embeddings tools (nécessite traces)

## Benchmarks

| Benchmark | Mesure | Échelle |
|-----------|--------|---------|
| BFCL v4 (Berkeley) | Accuracy function calling, structure args | Standard |
| MetaTool | When + which tool | Focalisé |
| ToolBench | Multi-step, 16K+ APIs | Grande échelle |
| ToolE | Single-tool + multi-tool retrieval | Standard |
| LiveMCPBench | MCP tool/agent retrieval réaliste | MCP |

## Pitfalls connus

- **Embedding misalignment** : queries users et descriptions tools vivent dans des espaces sémantiques différents — similarité brute souvent mauvaise
- **Over-retrieve = dégrade** : top-50 reranking peut être inférieur à DPR (à confirmer dans tables paper ToolRerank)
- **Plafond du modèle de base** : si l'embedding model ne distingue pas 2 tools, aucun raffinement n'aidera
- **Dégradation par cliff** : les chutes d'accuracy ne sont pas graduelles

## Liens

- [[RAG]] — index principal RAG
- [[rag-architecture]] — patterns avancés (HyDE, Multi-Query, Step-Back)
- [[rag-reranking]] — reranking documentaire
- [[rag-embeddings]] — modèles d'embedding et fusion
- [[neochat-tool-rag]] — implémentation NeoChat
- [[techniques-inedites]] — Adaptive RAG + model routing (technique connexe)
