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
derniere-maj: 2026-06-17
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

Quand un système RAG échoue, la retrieval est généralement la principale source d'erreur (consensus communauté, statistique exacte non sourcée en source primaire). La transformation de query adresse le gap sémantique.

- **HyDE** : LLM génère une réponse hypothétique, embed ce texte pour la recherche. Efficace en zero-shot sur queries courtes.
- **Multi-Query** : 3+ reformulations parallèles, merge/dedup/rerank. Pour queries ambiguës.
- **Step-Back Prompting** : question plus abstraite, retrouve documentation explicative plutôt que symptômes.
- **Query Decomposition** : split questions complexes en sous-questions focalisées.

Systèmes matures : **adaptation dynamique** — HyDE pour queries courtes, Multi-Query pour ambiguïté, Decomposition pour complexité.

## Agentic RAG

Stack production 2026 : **LangGraph** (orchestration, graphes cycliques) + **LlamaIndex Workflows** (retrieval) + RAGAS/Phoenix/Langfuse (évaluation).

- **LangGraph** : graphe dirigé cyclique avec branching conditionnel, checkpoints, human-in-the-loop
- **LlamaIndex** : Composite Retrieval APIs, `auto_routed` mode, routing multi-index
- **Adaptive-RAG** ([Jeong et al. NAACL 2024](https://arxiv.org/abs/2403.14403)) : classifieur **T5-Large (770M)** prédit la difficulté de la query → no retrieval / single-step / multi-step. **Efficience vérifiée table 1 (full-text arXiv, FLAN-T5-XL, temps normalisé single-step=1.00)** : multi-step = 4,69 steps / **8,81× le temps** ; Adaptive-RAG = 2,17 steps / **3,60× le temps** → **~59% de réduction de temps vs multi-step** (calculé, jamais énoncé en % par les auteurs ; le « 30-50% » des blogs n'est PAS dans le paper). Compétitif en précision sauf retard sur HotpotQA / 2Wiki (pas un free lunch).

Coût : 3-10x plus de tokens, 2-5x latence. Justifié sur multi-hop, ambiguïté, high-stakes. Pas sur FAQ bots. Réponse au « quand un agent RAG bat un RAG simple » : quand la query exige décomposition/multi-hop ou auto-correction — le routage par complexité (Adaptive-RAG) *est* la réponse : ne pas faire d'agentic sur les queries simples.

## GraphRAG (Microsoft)

Extrait knowledge graphs du texte, construit hiérarchies de communautés, génère résumés.

> [!note] Chiffres vérifiés source primaire (full-text arXiv 2404.16130v2, 17 juin 2026)
> Le paper Edge et al. mesure des **win-rates de comprehensiveness/diversity** (LLM-as-judge) vs vector RAG, **PAS une accuracy multi-hop**. Le « 3.4× accuracy / 80% vs 50% multi-hop » (et le « 86% vs 32% ») des blogs **n'existe nulle part dans le paper** — fabrication tierce, à ne pas propager. Vrais chiffres : **comprehensiveness 72-83%** (podcasts) / 72-80% (news), p<.001 ; **diversity 75-82%** / 62-71%. Le niveau root C0 = 72% comprehensiveness à **~97% de tokens en moins** que la summarization full-source. Vector RAG garde l'avantage sur la « directness » (contrôle). Force documentée = **comprehensiveness/diversity sur summarization globale cross-document**, pas un % multi-hop.

**LazyGraphRAG** : *"data indexing costs are identical to vector RAG and **0.1% of the costs of full GraphRAG**"* — verbatim [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/), novembre 2024. Les deux disponibles via Microsoft Discovery sur Azure.

### Implémentations GraphRAG OSS (panorama 2026)

- **LightRAG** ([Guo et al. arXiv 2410.05779](https://arxiv.org/abs/2410.05779), [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)) : **dual-level retrieval** (entités low-level / concepts high-level) + **mise à jour incrémentale** (le vrai différenciateur vs MS GraphRAG qui réindexe mal l'incrémental), **pas de community detection**. ⚠️ **Conflit de coût à surfacer, pas à trancher** : LightRAG annonce ~60% de réduction du coût d'indexation (comparaison maison) MAIS le benchmark indépendant **GraphRAG-Bench 2025** mesure l'inverse en tokens bruts (LightRAG 83,9M vs GraphRAG 79,9M). Documenter les deux, jamais le « 60% » seul. Le « EMNLP 2025 » qui circule n'est PAS dans l'abstract arXiv.
- **nano-graphrag** : réimplémentation minimale (~1100 lignes), ~70-90% de la perf à ~1/100 du coût (rapporté, chiffre rond non primaire).
- **Neo4j GraphRAG** : pattern différent — pas de community detection LLM ; **Cypher (requêtes N-hops) + vector index natif**. Définition Emil Eifrem : *« GraphRAG is RAG where on the retrieval path you use a Knowledge Graph. »* Aussi Neo4j Graphiti (mémoire d'agent temporelle).

**Coût d'extraction d'entités = le vrai trade-off GraphRAG** (ordres de grandeur convergents, rapporté) : MS GraphRAG ≈ $50-200 pour un corpus moyen (10-40× l'indexation vector), nano/LightRAG-style ≈ $0,50 / 500 pages. MAJ MS jan. 2025 « Dynamic Community Selection » = -79% tokens. **Quand GraphRAG vaut le coût** : multi-hop / multi-entités, summarization globale cross-document. **Quand NON** : single-hop factuel (GraphRAG *sous-performe* vanilla RAG de ~13% sur Natural Questions, rapporté), queries time-sensitive, latence critique (2-3× latence). Pattern 2026 : *« vectors for semantic entry-point, graphs for relational depth »* — souvent hybride.

## RAPTOR (Stanford)

Recursive Abstractive Processing : embed → cluster → résume → recurse vers le haut. Retrieval multi-niveau. Paper [Sarthi et al. 2024](https://arxiv.org/abs/2401.18059) — affiliation **100% Stanford** (Sarthi, Abdullah, Tuli, Khanna, Goldie, Manning). Sarthi a rejoint Google DeepMind APRÈS publication.

Verbatim abstract : *"improves the best performance on the QuALITY benchmark by 20% in absolute accuracy"*. Scores F-1 (+1.8 pts vs DPR, +5.3 pts vs BM25) cités dans le corps du paper (tables).

Extensions 2026 : **adRAP** (ajustement incrémental), **postQFRAP** (post-retrieval black-box compatible).

## Self-RAG

LM unique qui décide adaptativement de retriever et évalue sa propre sortie via **reflection tokens** :
1. Token retrieval : faut-il retriever ?
2. Passages multiples traités en parallèle avec évaluation pertinence
3. Tokens critique : évaluent factualité et qualité

Paper [Asai et al. (arXiv oct. 2023, ICLR 2024)](https://arxiv.org/abs/2310.11511).

> [!note] Chiffres vérifiés source primaire (full-text arXiv table 2, 17 juin 2026)
> Le « ~81% PubHealth / ~80% FactScore » du vault confondait deux métriques. Vrais scores : **Self-RAG 7B** — PubHealth **72,4**, PopQA 54,9, ARC 67,3, Bio FactScore **81,2** ; **Self-RAG 13B** — PubHealth **74,5**, PopQA 55,8, ARC 73,1, Bio FactScore 80,2. (Le « ~81% » était le FactScore Bio, pas le PubHealth qui est à 72-74%.) Bat ChatGPT sur PubHealth/PopQA/Bio ; ChatGPT garde l'avantage sur ARC.

## CRAG (Corrective RAG)

Évaluateur léger assigne score de confiance aux documents retrievés :
- **Correct** (haute confiance) → refine via decompose-then-recompose
- **Incorrect** (basse confiance) → discard, fallback web search
- **Ambiguous** → combine retrieval refiné + web search

Paper [Yan et al. 2024](https://arxiv.org/abs/2401.15884).

> [!note] Chiffres vérifiés source primaire (full-text arXiv table 1, 17 juin 2026)
> Le « 78,1% / +26,7 pts » du vault **n'existe pas dans le paper**. Vrais gains CRAG vs RAG (backbone SelfRAG-LLaMA2-7b) : PopQA 52,8→59,8 (**+7,0**), Biography FactScore 59,2→74,1 (**+14,9**), **PubHealth 39,0→75,6 (+36,6, plus gros gain)**, Arc-Challenge 53,2→68,6 (**+15,4**). Sur backbone LLaMA2-7b nu : PubHealth 48,9→59,5, Arc 43,4→53,7.

## RAG vs Fine-tuning vs Long Context

**RAG résout un problème de connaissance. Fine-tuning résout un problème de comportement.** L'hybridation RAG+FT est la tendance dominante 2025-2026 (chiffre "60%" circulant entre blogs industry sans source primaire identifiable).

### Long context (1M+ tokens)
- **Gemini 1.5 Pro** : **>99.7% recall NIAH single ET multi-fact** jusqu'à 1M tokens, 99.2% à 10M tokens ([Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/the-needle-in-the-haystack-test-and-how-gemini-pro-solves-it))
- **GPT-4 Turbo** : ~50% recall en multi-fact à sa limite max 128K (même source)
- "Lost in the middle" ([Liu et al. 2023](https://arxiv.org/abs/2307.03172)) : dégradation significative (>30% observée dans certains contextes) pour info positionnée centralement
- Plafond pratique (circa 2024, Greg Kamradt NIAH) : 32-64K tokens pour la majorité des modèles avant dégradation notable. Les modèles 2025-2026 améliorent cette limite.
- Latence/coût : long-context est ordres de grandeur plus lent et plus cher que RAG (calculs varient selon tarifs API à date, ratio typique 100x-1000x+)

### Anthropic recommande
*"If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt"* — verbatim [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval). Avec prompt caching : "significantly faster and more cost-effective".

### Pattern hybride 2026
RAG retrieve les documents les plus pertinents d'un grand corpus → charge dans un long context pour cross-document reasoning. RAG = scale (millions docs), long context = depth (centaines de pages).

## Late interaction (ColBERT) vs dense — grille de décision

Complète [[jina-embeddings-v4|ColPali]] et FastPlaid (cf [[rag-embeddings]]) côté texte.

- **ColBERT (multi-vecteur, late interaction)** : 1 vecteur par token + scoring MaxSim. **Force** = généralisation out-of-domain (BEIR jamais vu en training), documents longs (le single-vecteur compresse de façon lossy), explicabilité (scoring token-level). PLAID/SPLATE = 7-45× latence en moins que le naïf.
- **Trade-off central = stockage** : 1 vecteur/token explose le footprint. Mitigations 2024-2025 : pooling post-hoc (÷2 sans perte), token pruning 50-75% (≤2% de perte), résiduel+centroïde (ColBERTv2/PLAID).
- **Grille** : **dense single-vector** si coût/stockage prioritaire + domaine bien couvert ; **ColBERT** si out-of-domain, docs longs, précision légale/financière critique, et budget stockage OK.

## Évaluation (RAGAS)

| Métrique | Mesure | Ground truth ? |
|----------|--------|----------------|
| Context Precision | Ranking pertinent en haut | Non (LLM judge) |
| Context Recall | Toute info nécessaire retrievée | Oui |
| Faithfulness | Claims supportés par contexte | Non (LLM judge) |
| Answer Relevancy | Réponse adresse la question | Non (LLM judge) |

Seuils production : **>0.8** faithfulness et context precision. Top-k optimal : 4-8 chunks. Au-delà de 8, faithfulness se dégrade.

## Multi-Index / Multi-Source
## Dédup multi-source : convergence amont vs dédup retrieval

Quand un RAG agrège plusieurs sources qui se recouvrent (ex : Confluence + tickets Jira + vault interne décrivant la même procédure), deux stratégies opposées pour éviter de retourner 3 fois la même réponse :

- **Dédup au retrieval** (aval) : N ingestors → N jeux de vecteurs (avec métadonnée `source`), puis collapse des near-duplicates au moment de la requête (similarité d'embedding post-rerank + priorité de source). Souple, mais on stocke et embedde le doublon, et on paie la dédup à chaque requête.
- **Convergence vers une source unique** (amont) : toutes les sources alimentent **une seule source canonique** (curée), qui est la **seule embeddée**. La dédup se fait à la **curation** (humaine ou semi-auto), pas au retrieval. → zéro doublon **par construction**, une seule chaîne d'embedding, pas de gaspillage.

La convergence amont est supérieure quand : (1) il existe une source canonique légitime (wiki/Confluence, base FAQ), (2) la qualité d'écriture compte plus que l'exhaustivité brute, (3) on veut une validation humaine avant que le contenu « compte » dans le RAG. Coût : il faut un pipeline de transformation source→canonique (ex : tickets Jira → notes curées → pages Confluence).

**Gotcha barrière** (cas réel neo_ia, juin 2026) : si la source canonique a un workflow de validation (dossier « à valider »), le sync incrémental doit **exclure explicitement** le contenu non validé (filtre statut/label sur TOUS les chemins CQL — full ET incrémental), sinon il embedde le brouillon et la validation devient décorative.

**Anti-gaspillage embedding** : avec convergence ou non, un pipeline d'ingestion doit stocker un `content_hash` (SHA256) par document et **skipper embedding + appels LLM auxiliaires si le hash est inchangé** — pré-filtre mtime/version, hash = vérité (un git pull ou un re-sync réécrit les dates sans changer le contenu). Pattern éprouvé : gate mtime+hash des watchers de vault.
## RAG souverain EU

Axe critique pour un chatbot support traitant des données clients européennes (RGPD). Le RGPD n'interdit pas le hors-UE mais l'encadre (art. 44-49) ; le vrai risque est le **Cloud Act** — c'est la nationalité juridique du prestataire qui prime, pas la localisation serveur. Échéance : **AI Act applicable 2 août 2026** (cf [[ai-act-eu-cheatsheet]], [[fine-tuning-privacy]]).

Spectre d'options, du moins au plus souverain :
1. Modèle US via cloud EU (Azure West Europe + clauses contractuelles types) — compromis PME.
2. **100% européen** (Mistral sur Scaleway/OVH) pour données sensibles. Labels : **SecNumCloud** (ANSSI), **HDS** (santé, décret renforcé mars 2026).

Briques souveraines 2026 :
- **Parsing** : [Mistral OCR 3](https://mistral.ai/news/mistral-ocr-3/) — SOTA extraction (markdown + tables HTML), ~$2/1000 pages ($1 batch), **self-hostable** pour données sensibles. Provider FR. Le pipeline [[Jonas Roman]] / ZParse l'utilise comme étape d'extraction. Paysage OCR complet → [[briques-produit-ia-build-vs-buy]].
- **Ingestion** : ZParse (FR, hébergé EU, ISO 27001 en cours) — cf [[Jonas Roman#ZParse — son outil d'ingestion RAG (souveraineté EU)]].
- **Vector DB EU** : Qdrant (HQ Allemagne, self-host Rust), Weaviate (HQ Pays-Bas, hybrid champion), ou **pgvector sur Postgres EU** (Supabase région EU, Neon) — confortable jusqu'à ~50M vecteurs, « use the Postgres you already have ».
- **Embeddings/génération** : Mistral (souveraineté EU, embed+gen même plateforme, soumis à l'AI Act). Sur la pure précision retrieval, Voyage/Jina restent devant — arbitrer souveraineté vs précision selon la sensibilité des données. Self-host (BGE-M3, Jina v5, Nomic) pour l'air-gap strict.

Stack support EU type : ZParse (ingestion EU) → Supabase/pgvector EU → embeddings Mistral + Mistral OCR 3 pour le parsing → reranker → éval Golden Dataset. Tout en souveraineté.

Pattern enterprise 2026 : hot/warm/cold indexes pour optimiser coûts d'embedding (chiffres exacts de pourcentage d'adoption non sourcés en source primaire).

- **Query routing** : classifieur/LLM détermine quel index interroger
- **Map-Reduce** : agents parallèles par sous-query/source, agrégation
- **Milvus 2.6** : dense + sparse dans la même collection, [hybrid_search() API unique](https://milvus.io/blog/introduce-milvus-2-6-built-for-scale-designed-to-reduce-costs.md)

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
