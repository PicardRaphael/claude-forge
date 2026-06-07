---
titre: "Référence technique — ingénierie LLM en production (niveau implémentation)"
resume: "Référence exhaustive sourcée VÉRIFIÉ/RAPPORTÉ : optimisation tokens, serving/inférence, RAG, orchestration d'agents, context engineering, eval/observabilité, fine-tuning, guardrails"
aliases:
  - référence technique stack IA
  - stack IA implémentation
  - ingénierie LLM production
  - reference technique LLM
  - serving RAG agents implementation
domaine: ia
type: reference
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/reference"
  - "#domaine/ia"
  - "#domaine/infrastructure"
---

> [!note] Note de référence exhaustive
> Document de référence niveau implémentation. Les **deltas décisionnels** sont capitalisés en notes atomiques : [[serving-inference-optimisation]] (§2), [[prompt-caching-kv-cache]] (§1), [[agents-evaluation]] (§6 — Langfuse→ClickHouse). Cette note reste la source longue, cherchable via `search_brain`.

# Référence technique d'ingénierie : comment les laboratoires d'IA et les équipes de production construisent et optimisent leurs systèmes (niveau implémentation)

> **Statut des sources** : VÉRIFIÉ-SOURCE = chiffre tiré d'une doc officielle, d'un papier ou d'un blog d'ingénierie primaire. RAPPORTÉ = chiffre fournisseur/marketing non vérifié indépendamment. Date de référence : 7 juin 2026. Plusieurs sources secondaires citaient des noms de modèles non vérifiables (« Opus 4.8 », « Mythos », « GPT-5.4 ») ; je m'appuie uniquement sur les mécanismes documentés, pas sur ces noms.

## TL;DR

- **Le levier coût/latence le plus rentable reste le caching de prompt + la réutilisation du KV-cache** : le prompt caching Anthropic facture les lectures à 0,1× le prix d'entrée (lecture après écriture à 1,25× pour le TTL 5 min, 2× pour 1 h) ; ProjectDiscovery rapporte 59–70 % d'économie réelle sur un agent multi-étapes. Côté serving, vLLM (PagedAttention) et SGLang (RadixAttention) réduisent le gaspillage mémoire KV de 60–80 % à <4 % ; le blog officiel vLLM (UC Berkeley, 20 juin 2023) mesure « 14x - 24x higher throughput than HF and 2.2x - 2.5x higher throughput than HuggingFace Text Generation Inference (TGI) » (LLaMA-7B sur A10G, LLaMA-13B sur A100-40GB).
- **Les gains de débit/latence viennent d'une pile bien choisie** : continuous batching + PagedAttention (vLLM) comme défaut ; RadixAttention (SGLang) quand les préfixes sont partagés (RAG, multi-tours, agents) ; speculative decoding EAGLE-3 (2–6,5× rapporté, dépendant du taux d'acceptation α) ; quantification FP8 (qualité quasi-intacte) ou AWQ/GPTQ INT4 (≈3× débit) ; et la désagrégation prefill/decode pour tenir des SLO TTFT/TPOT serrés à l'échelle.
- **Pour le RAG et les agents, l'architecture gagnante est explicite** : chunking ~256–512 tokens + Contextual Retrieval (Anthropic : -35 %/-49 %/-67 % d'échecs), recherche hybride dense+BM25 fusionnée par RRF (k=60), reranking cross-encoder top-150→top-20 ; orchestration via LangGraph (Python) / Vercel AI SDK (TS) / MCP au niveau protocole ; et context engineering (compaction, just-in-time retrieval, sous-agents) plutôt que tout charger en contexte.

---

## 1. OPTIMISATION DES TOKENS

### 1.1 Prompt caching (Anthropic, OpenAI, Gemini)

**Anthropic — mécanique exacte (VÉRIFIÉ-SOURCE, platform.claude.com/docs prompt-caching).**
- On marque les blocs avec `cache_control: {"type": "ephemeral"}`. Le cache couvre le préfixe **dans l'ordre tools → system → messages**, jusqu'au dernier bloc marqué inclus. Toute modification à un niveau invalide ce niveau et tous les suivants.
- **Multiplicateurs de prix** : écriture cache 5 min = **1,25× le prix d'entrée de base** ; écriture 1 h = **2,0×** ; lecture cache = **0,1×** (soit -90 %). Conséquence : le cache devient rentable après **une seule lecture** en TTL 5 min, ou **deux lectures** en TTL 1 h.
- **Minimum cachable** : 1 024 tokens pour la génération Sonnet/Haiku récente, 4 096 pour les plus gros modèles (selon le modèle). En dessous, la requête est traitée sans cache, sans erreur.
- Jusqu'à **4 breakpoints** `cache_control` par requête. Champs de monitoring dans `usage` : `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`. Le TTL se rafraîchit à chaque hit sans coût supplémentaire.
- **Caching automatique** : Anthropic gère désormais le placement des breakpoints sans marqueurs. Inconvénient documenté (blog ProjectDiscovery/Neo) : l'auto-caching ignore quels segments sont stables vs dynamiques, donc du contenu runtime au milieu du prompt provoque des cache misses. Le contrôle explicite + TTL 1 h reste nécessaire pour les agents.

**Pratique terrain (VÉRIFIÉ-SOURCE, blog ProjectDiscovery « How We Cut LLM Costs by 59% »).**
- « The relocation trick » : déplacer le contenu dynamique HORS du préfixe cachable a fait passer le taux de hit de 7 % à 74 % en un déploiement, puis jusqu'à 84 % avec breakpoints explicites + TTL délibérés. Économie réelle dérivée du spend : **59 % puis 66 %, et 70 % sur les 10 derniers jours**. Règle : « if your agents run more than 3–5 steps, you're leaving significant money on the table ».
- **Ordre de grandeur du gain à l'échelle (VÉRIFIÉ-SOURCE, DeepSeek-V3 Open-Infra, GitHub, 27–28 fév. 2025)** : sur 24 h, « Total input tokens: 608B, of which 342B tokens (56.3%) hit the on-disk KV cache », pour ~73,7k tokens/s en entrée et ~14,8k tokens/s en sortie par nœud H800. Le caching disque côté serveur absorbe ici plus de la moitié des tokens d'entrée.

**OpenAI (RAPPORTÉ via docs/secondaire).** Caching **automatique** par préfixe pour prompts ≥ 1 024 tokens, **sans pénalité d'écriture**, remise lecture de **50 %** (vs 90 % Anthropic). Paramètre optionnel `prompt_cache_key` pour mieux router les hits. Stratégie purement structurelle : garder le contenu identique en début de requête.

**Gemini (RAPPORTÉ via secondaire Helicone).** Modèle « multiplicateur + coût de stockage » : prix d'entrée de base + tarif de stockage par MTok/heure ; lecture autour de 0,25× le prix d'entrée. Vérifier la doc officielle Google avant de chiffrer.

**Structuration recommandée (du plus stable au moins stable)** : instructions système → définitions d'outils → documents de référence/contexte de session → message utilisateur (jamais caché). Les sources convergent : 60–90 % d'économie sur les charges à préfixe répété.

### 1.2 Optimisation du KV-cache (serving)

- **PagedAttention (vLLM, papier Kwon et al., SOSP 2023, VÉRIFIÉ-SOURCE)** : le KV-cache est partitionné en blocs de taille fixe (**16 tokens/bloc par défaut**), alloués à la demande comme la pagination mémoire d'un OS. Réduit la fragmentation de **60–80 % à <4 %**. Formule du coût KV par token et par couche : `2 × num_kv_heads × head_dim × dtype_bytes` (le facteur 2 = K et V).
- **RadixAttention (SGLang, LMSYS)** : KV-cache stocké dans un **arbre radix (trie compressé)** indexé au niveau token ; découverte automatique des préfixes partagés entre requêtes, éviction LRU des feuilles. Contraste avec le prefix caching par blocs de vLLM (hash de blocs). SGLang priorise les requêtes à plus long préfixe partagé (≈ parcours en profondeur de l'arbre).
- **Quantification du KV-cache** : vLLM supporte **FP8 (E4M3 et E5M2)** pour le KV-cache, **pas INT8**. Permet de cacher plus de tokens. Le 4-bit/2-bit KV dégrade nettement (baisse MMLU) — à éviter.

### 1.3 Code execution avec MCP / « Code Mode »

**Anthropic « Code execution with MCP » (4 nov. 2025, VÉRIFIÉ-SOURCE anthropic.com/engineering).** Au lieu d'exposer chaque outil MCP comme un tool-call, on présente les serveurs MCP comme une **API de code** (fichiers TypeScript dans `./servers/`). L'agent explore le filesystem (`list` du répertoire, `read` de `getDocument.ts`), ne charge que les définitions nécessaires, et écrit du code qui filtre les données AVANT qu'elles n'entrent dans le contexte. Cas Google Drive → Salesforce : **150 000 → 2 000 tokens, soit -98,7 %**. Bénéfice clé : les résultats intermédiaires restent dans l'environnement d'exécution.

**Cloudflare « Code Mode » (VÉRIFIÉ-SOURCE blog.cloudflare.com).** L'API Cloudflare complète (>2 500 endpoints) exposée via **deux outils seulement, `search()` et `execute()`**, pour ≈ **1 000 tokens** quelle que soit la taille de l'API. Une version flat-tool consommerait **1,17 million de tokens** (réduction ≈ 99,9 %). Le code s'exécute dans un **isolate V8** (Workers Loader), sans accès filesystem/réseau hors bindings explicites ; les clés API ne sont jamais vues par le LLM (injection au niveau transport). Insight cité : « LLMs are better at writing code to call MCP, than at calling MCP directly » (les formats tool-call JSON sont synthétiques, peu présents dans le corpus d'entraînement).
- Benchmark indépendant Bifrost (RAPPORTÉ) : à 508 outils/16 serveurs, tokens d'entrée 75,1M → 5,4M (**-92,8 %**), pass rate 100 % maintenu. Démo Cloudflare au « MCP Night » (RAPPORTÉ) : -32 % tokens sur tâche simple, -81 % sur batch complexe.

### 1.4 Compaction, context editing, semantic caching, sorties structurées
- **Compaction / structured note-taking / sous-agents** : voir §5 (Anthropic context engineering).
- **Context editing** : pruning par règles dans le scaffold (ex. purger les `tool_result` anciens du message history une fois consommés).
- **Semantic caching (GPTCache)** : cache de réponses indexé par similarité d'embedding de la requête (vs match exact).
- **Sorties structurées** réduisent les tokens de sortie et évitent les re-prompts (voir §8).

---

## 2. VITESSE D'INFÉRENCE & PERFORMANCE

### 2.1 vLLM
- **Continuous batching** (niveau itération, hérité d'ORCA/OSDI 2022) : à chaque pas de décodage, le scheduler insère une nouvelle requête dès qu'une se termine, libérant ses blocs KV. Active par défaut.
- **Paramètres clés (VÉRIFIÉ-SOURCE docs/field guides)** :
  - `--gpu-memory-utilization` : 0,90–0,95 (ne pas dépasser 0,95 ; vLLM a besoin de marge pour activations + contexte CUDA). Sur bare-metal dédié, 0,95.
  - `--max-num-seqs` : nombre max de séquences concurrentes (ex. 256–512 pour API à fort trafic).
  - `--max-num-batched-tokens` : 8 192–16 384 sur GPU à grande VRAM ; augmenter `max_num_seqs` sans augmenter ce paramètre **affame le scheduler**.
  - `--tensor-parallel-size` : = nombre de GPU pour le multi-GPU. Piège documenté : mettre TP=4 quand le modèle tient sur 1 GPU **réduit** le débit (overhead NCCL AllReduce à chaque couche).
  - **Chunked prefill** : découpe les longs prefills pour éviter de bloquer le decode (compromis TTFT/TPOT).
- **Chiffres (VÉRIFIÉ-SOURCE, blog officiel vLLM 2023)** : « 14x - 24x higher throughput than HF and 2.2x - 2.5x higher throughput than TGI ». Mesures secondaires (RAPPORTÉ) : Llama-2-70B sur 4×A100 ≈ 2 200 tok/s à 256 utilisateurs. Le moteur **V1** supprime la distinction prefill/decode au scheduling, intègre FlashAttention 3, et utilise des transferts DMA zero-copy.

### 2.2 SGLang
- **RadixAttention** : prefix caching par arbre radix (cf. §1.2). Bénéfice maximal quand le prefill est une grosse fraction du coût (petits modèles, sorties courtes, préfixes partagés).
- **Quand SGLang bat vLLM (RAPPORTÉ, benchmarks tiers)** : ≈ **29 % de débit en plus sur H100** (16 200 vs 12 500 tok/s, Llama-3.1-8B, prompts ShareGPT) ; jusqu'à **6,4×** sur charges à fort partage de préfixe (RAG, multi-tours) ; TTFT p95 5–8 % plus bas. À l'échelle 70B, écart réduit (3–5 %). Support DeepSeek/Qwen, structured output (overlap masque grammaire/inférence). Utilisé en prod par xAI (Grok 3) et Azure (DeepSeek R1 sur AMD).
- **Nuance honnête (GitHub issue #21061)** : sous très haute concurrence, le routage Python de SGLang peut souffrir de la contention du GIL ; le routage C++/CUDA de vLLM peut alors scaler mieux. Choisir selon la charge réelle, pas selon le chiffre de tête.
- **Décision** : SGLang par défaut pour DeepSeek, conversationnel multi-tours, structured output ; vLLM pour batch de prompts uniques, environnements multi-hardware (TPU, Trainium, Gaudi) et compatibilité modèle la plus large.

### 2.3 TensorRT-LLM
- **In-flight batching** (équivalent NVIDIA du continuous batching), support **FP8/FP4**, backend par défaut **XGrammar** pour le structured output. Désagrégation prefill/decode supportée (cf. §2.6). Complexité de setup plus élevée que vLLM/SGLang (compilation des moteurs). À privilégier sur Hopper/Blackwell quand on veut exploiter à fond les cores FP8/FP4 et qu'on accepte le coût d'intégration.

### 2.4 Speculative decoding
**Principe** : un brouillon (draft) propose γ tokens, le modèle cible les vérifie en un seul forward. Sans perte si l'acceptation suit l'échantillonnage cible (EAGLE), avec relâchement possible (Medusa) qui ne garantit pas le lossless à température 1.
- **Métrique reine : taux d'acceptation α** et **longueur d'acceptation moyenne τ** (`τ = K × (#acceptés/#brouillonnés) + 1`). À **α = 0,6–0,8** (réaliste avec un draft EAGLE3 prêt-à-l'emploi), on observe **2–3×** ; **α < 0,5 peut nuire** (cycles gaspillés). α dépend de la tâche (0,75–0,85 sur code/écriture formelle).
- **EAGLE / EAGLE-2 / EAGLE-3 (VÉRIFIÉ-SOURCE, papier arXiv 2503.01840 + repo SafeAILab)** : EAGLE-3 = **3,0×–6,5×** vs autoregressif vanilla, +20–40 % vs EAGLE-2. EAGLE-3 entraîné en « training-time test » garde un α quasi constant selon la position du token (EAGLE-1 décroît). EAGLE-2 (4× vs vanilla 13B) ajuste dynamiquement l'arbre de brouillon via les scores de confiance.
- **Medusa** : têtes de décodage indépendantes (K=6, pas de partage de poids) ; self-distillation, setup simple, mono-GPU.
- **MTP (multi-token prediction)** : **DeepSeek-V3 embarque un module MTP natif** servant de tête de brouillon (fine-tunable).
- **n-gram / prompt lookup (PLD)** : brouillon par copie depuis le contexte ; utile quand la génération répète le prompt (code), inutile sinon.
- **Cursor « speculative edits » (VÉRIFIÉ-SOURCE, blog Cursor « Editing Files at 1000 Tokens per Second » + Fireworks AI)** : « We achieve speeds of ~1000 tokens (around 3500 char/s) on our 70b model using a speculative-decoding variant tailored for code-edits… a ~13x speedup over vanilla inference using Llama-3-70b and a ~9x speedup over our previous GPT-4 speculative edits deployment ». Tous les gains diminuent à très grand batch (le cible devient compute-bound, non memory-bound).

### 2.5 Quantification
- **FP8 (W8A8-FP)** : symétrique par canal de sortie pour les poids, dynamique par token pour les activations, **sans calibration**. **Perte de qualité minimale**, recommandé par défaut sur Hopper/Blackwell. La recherche (ZeroQuant-FP) montre FP8 nettement meilleur qu'INT8 pour les activations.
- **AWQ vs GPTQ (INT4, W4A16)** : qualité quasi identique sur benchmarks académiques (AWQ +0,2–0,35 pt) ; GPTQ légèrement meilleur sur tâches réelles (papier « Give Me BF16 or Give Me Death », arXiv 2411.02355). Les deux ≈ **3× le débit du BF16**. **Les kernels comptent plus que l'algo** : Marlin-AWQ atteint 741 tok/s (10,9× vs AWQ naïf), Marlin-GPTQ 712 tok/s (benchmark JarvisLabs, RAPPORTÉ).
- **INT8 SmoothQuant** : décale la complexité des activations vers les poids ; nécessaire pour W8A8-INT à 70B (sinon chute de précision).
- **GGUF** : universel (llama.cpp, Ollama), CPU+GPU hybride, mais **overhead important dans vLLM** (≈93 tok/s) — réserver à llama.cpp.
- **NVFP4 / MXFP8** : formats 4-bit float pour Blackwell ; **NVFP4 ne supporte pas encore les adaptateurs LoRA** → pour vLLM + multi-LoRA, utiliser **GPTQ-Int4**.
- **Règle** : éviter INT4 pour maths/code/raisonnement (perte la plus visible) ; FP8 pour qualité+vitesse si hardware le permet ; AWQ/GPTQ INT4 si VRAM contrainte.

### 2.6 Désagrégation prefill/decode & métriques
- **Prefill** = compute-bound (traitement parallèle du prompt, produit le KV-cache) ; **decode** = memory-bound (génération autorégressive token par token). Les co-localiser crée de l'interférence.
- **Désagrégation P/D (DistServe, OSDI 2024 ; Splitwise)** : prefill et decode sur des pools GPU dédiés ; transfert du KV-cache via NVLink (600 GB/s) / InfiniBand. **DeepSeek-V3 en prod (VÉRIFIÉ-SOURCE, Hao AI Lab @ UCSD)** : « the team uses 3 prefill nodes and 9 decode nodes (each with 8 H100 GPUs)… the decode phase employs a much wider EP (≈ 256)… they built the 3FS library » pour le transfert KV. Devenu standard (vLLM, SGLang, TensorRT-LLM, NVIDIA Dynamo, LMDeploy).
- **Compromis SLO (papier TaiChi)** : agrégation P/D optimale sous TTFT serré + TPOT relâché ; **désagrégation optimale sous TPOT serré + TTFT relâché**. DistServe : 1,6×–7,4× de débit à SLO tenu vs DeepSpeed-MII.
- **Métriques** : **TTFT** (time-to-first-token, latence prefill), **TPOT/ITL** (time-per-output-token / inter-token latency, latence decode). Optimiser le débit (tokens/s agrégé) se fait souvent au détriment du TTFT/TPOT individuel — arbitrer selon l'usage (chat = TPOT, batch = débit).

---

## 3. RAG — DÉTAIL D'IMPLÉMENTATION

### 3.1 Chunking
- **Tailles typiques** : ~256–512 tokens par chunk, overlap de quelques dizaines de tokens. Anthropic recommande d'expérimenter taille/frontière/overlap.
- **Stratégies** : fixed-size (simple), recursive (respecte la structure : paragraphes→phrases), semantic (coupe aux ruptures sémantiques), **late chunking (Jina)** (embed le document long d'abord, découpe ensuite pour préserver le contexte), document-structure-aware (titres, sections).

### 3.2 Embeddings
- **voyage-3-large (VÉRIFIÉ-SOURCE blog.voyageai.com, 7 janv. 2025)** : surpasse OpenAI text-embedding-3-large de **+9,74 %** et Cohere-v3-English de **+20,71 %** en moyenne sur 100 datasets / 8 domaines (chiffres fournisseur). **Matryoshka** : 2048/1024/512/256 dims dans un seul appel ; quantification float32/int8/uint8/binaire. Contexte 32K tokens (vs OpenAI 8K, Cohere 512). Point clé : **binaire 512-dim bat OpenAI 3072-dim float, à 200× moins de stockage** ; int8 1024-dim n'est que 0,31 % sous float 2048-dim.
- **OpenAI text-embedding-3-large** : 3072 dims, Matryoshka tronquable à 256/1024. Choix « safe » par défaut quand on est déjà sur OpenAI.
- **Cohere embed-v4** : multilingue entreprise, multimodal (images/screenshots) ; input-types (`search_document`/`search_query`).
- **Open-source** : **BGE-M3** (meilleur rapport qualité-coût self-hosted, multilingue, supporte dense+sparse+multivector), **Qwen3-Embedding**, **Nomic Embed v2** (137M, multilingue).
- **MTEB — caveat** : ne pas s'y fier aveuglément, tester sur SES données (BEIR sur les datasets proches du domaine donne un prior). Matryoshka est désormais le standard pour arbitrer dims/stockage.
- **Quantification d'embeddings** : binaire/int8 réduisent drastiquement le coût vectorDB avec perte minime (voir voyage-3-large).

### 3.3 Bases vectorielles
- **pgvector (VÉRIFIÉ-SOURCE github.com/pgvector + docs Azure/Neon/Google)** :
  - **HNSW** : `m` (connexions max/couche, défaut **16**), `ef_construction` (taille liste candidats à la construction, défaut **64**), `hnsw.ef_search` (au query, défaut **40**). Démarrer à `m=16, ef_construction=200`, augmenter si recall insuffisant. `m=64, ef_construction=500` = graphe de haute qualité mais gourmand. Meilleur compromis vitesse/recall, build plus lent, plus de mémoire ; pas d'étape d'entraînement (indexable sur table vide).
  - **IVFFlat** : partition en `lists`, `probes` au query (défaut **1** = recall catastrophique → mettre 10–50). Build plus rapide, moins de mémoire, mais query moins bon. Réserver aux gros datasets quasi-statiques.
  - Tuning de session sûr : `SET LOCAL hnsw.ef_search = 100;` dans une transaction. Limite 2000 dims pour un index (utiliser `halfvec` au-delà).
  - **DiskANN** (via pgvectorscale) : bon équilibre build/recall, footprint mémoire très réduit.
- **Autres** : Qdrant (sparse vectors natifs, hybrid Query API v1.10+), Pinecone (single-index hybrid), Weaviate (hybrid natif), Milvus, Vespa, Turbopuffer. Index : HNSW, IVF, DiskANN. Vérifier support du filtrage pré/post et de la recherche hybride.

### 3.4 Recherche hybride & RRF
- **Reciprocal Rank Fusion (VÉRIFIÉ-SOURCE, Cormack/Clarke/Büttcher, SIGIR 2009)** : `RRF(d) = Σ_r 1/(k + rank_r(d))`. **k=60** = optimum empirique TREC ; k∈[40,80] équivalents. Fusionne par **rang, pas par score** → immunise contre l'incompatibilité BM25/cosinus et les outliers. Défaut dans OpenSearch, Elasticsearch, Azure AI Search, MongoDB Atlas, Weaviate.
- **Conseils terrain (RAPPORTÉ, secondaires)** : pour petit corpus (100–300 pages), descendre k à 10–20 (les écarts de rang sont plus signifiants) ; pondérer dense vs sparse selon le jargon. À rank 1, contribution 1/61≈0,0164 ; à rank 100, 1/160≈0,0063 (×2,6).
- **Sparse** : BM25 (lexical) ou **SPLADE** (sparse appris, meilleur sur sémantique-lourd) ; pré-calculer les vecteurs SPLADE des documents à l'indexation (l'inférence SPLADE au query ajoute 100–300 ms). Latence hybride ≈ somme sparse+dense moins parallélisme (≈ +5–20 ms sur dense-only).

### 3.5 Rerankers
- **Pattern** : retrieval bi-encoder top-50/100/150 → reranker cross-encoder → top-10/20 → LLM. Le cross-encoder voit query+document ensemble (plus précis que le dot-product bi-encoder). Corrige le « lost in the middle ».
- **Modèles** : **Cohere Rerank 3.5** (managé, multilingue, faible friction ; API `co.rerank(model=..., query=..., documents=..., top_n=...)` renvoie `relevance_score`) ; **bge-reranker-v2-m3** (BAAI, 568M, 100+ langues, Apache 2.0, **50–100 ms sur GPU**, ≈350 ms sur CPU — exiger un GPU) ; **Voyage rerank-2.5** ; **Jina Reranker v2** (long contexte 8k+, CC-BY-NC) ; **ms-marco-MiniLM-L-6** (rapide, prototypage anglais).
- **ColBERT / late interaction (VÉRIFIÉ-SOURCE, littérature ColBERT/PLAID)** : encode query et doc séparément en embeddings par token, score par **MaxSim** au query-time → docs pré-calculables/cachables. Avec PLAID (pruning par centroïdes), latence en dizaines de ms à grande échelle.

### 3.6 Contextual Retrieval (Anthropic)
**VÉRIFIÉ-SOURCE, anthropic.com/news/contextual-retrieval (sept. 2024).** Avant l'embedding, on préfixe chaque chunk d'un court contexte généré par Claude (prompt : `<document>{{WHOLE_DOCUMENT}}</document>` + `<chunk>{{CHUNK_CONTENT}}</chunk>` → « give a short succinct context to situate this chunk … Answer only with the succinct context »). On indexe en dense ET en BM25 contextuel.
- **Chiffres (sur top-20, échec de récupération)** : Contextual Embeddings seuls **-35 %** (5,7 %→3,7 %) ; + Contextual BM25 **-49 %** (→2,9 %) ; + reranking **-67 %** (→1,9 %). Coût d'indexation ≈ **1,02 $/M tokens de document** grâce au prompt caching. Anthropic précise (VÉRIFIÉ-SOURCE) : « Voyage and Gemini have the best embeddings of the ones we tested; Passing the top-20 chunks to the model is more effective than just the top-10 or top-5 ». Sous 200K tokens (~500 pages), inutile : tout mettre en contexte avec prompt caching.

### 3.7 Évaluation (Ragas)
- Métriques : **faithfulness** (réponse soutenue par le contexte), **context precision/recall**, **answer relevancy**. Calculées par LLM-as-judge + similarité. À coupler aux gates de régression (§6).

---

## 4. LIBRAIRIES D'AGENTS / ORCHESTRATION

### 4.1 LangGraph (Python/JS)
**VÉRIFIÉ-SOURCE, docs.langchain.com + repo langchain-ai/langgraph.**
- **StateGraph(State)** : on définit un **State** (TypedDict ou Pydantic) avec **reducers** ; on `add_node`/`add_edge`/`add_conditional_edges` ; on **`.compile(checkpointer=..., store=..., interrupt_before=...)`**.
- **Reducers** : signature `(left, right) -> value`. `Annotated[list, operator.add]` ou `add_messages` (dédup par ID) pour accumuler ; type nu = overwrite (dernière écriture). Critique pour les branches parallèles (évite les race conditions) et les reprises depuis checkpoint.
- **Checkpointing** : `InMemorySaver`/`MemorySaver` (dev), `SqliteSaver` (prod mono-serveur), `PostgresSaver` (multi-instance). Latences rapportées : SQLite <15 ms avec state <10KB ; **un state de 3 MB fait monter l'écriture à 300–800 ms** → garder le state minimal (IDs, findings, pas de contenu brut).
- **Interrupts / human-in-the-loop** : `interrupt("question")` met en pause ; reprise via `Command(resume=valeur)`. **`interrupt_before` gate l'action AVANT exécution** (à préférer pour les approbations) ; `interrupt_after` pour revue post-hoc.
- **Command** : `Command(goto="node", update={...})` — routage dynamique + mise à jour d'état depuis un node ou un outil (ajoute une arête dynamique).
- **Store** (mémoire long-terme cross-thread), **subgraphs**, **Functional API** (`@entrypoint`, `@task`) en alternative au graphe déclaratif. **LangGraph Platform** pour le déploiement managé.

### 4.2 Vercel AI SDK (TypeScript)
**VÉRIFIÉ-SOURCE, ai-sdk.dev + vercel.com/blog.**
- **`generateText` / `streamText`** : un step par défaut. **`stopWhen`** transforme en boucle d'outils ; conditions intégrées : `stepCountIs(n)` (défaut **20**), `hasToolCall(name)`, `isLoopFinished()`.
- **`prepareStep`** : modifie entre steps le modèle, le system prompt, les messages (compression/filtrage de contexte), les outils, le `toolChoice`.
- **`tool({ description, inputSchema: z.object({...}), execute })`** (en v5, `inputSchema`/`outputSchema` remplacent `parameters`/`result`).
- **Sorties structurées** : `generateObject` / `streamObject` avec schéma Zod ; en v5+, l'objet `Output`/`output` permet de combiner tool-calling + sortie structurée finale.
- **Classe `Agent`** (encapsule generateText avec stopWhen/prepareStep ; v6 introduit `ToolLoopAgent`). v5 : protocole **SSE standard** (remplace l'ancien protocole custom), distinction **UIMessage** (rendu front) vs **ModelMessage** (envoyé au LLM), provider global (`'openai/...'`), Zod 4, MCP V2.

### 4.3 Mastra (TS)
Workflows avec **suspend/resume**, composition `.then` / `.branch` / `.parallel` ; agents, mémoire, evals intégrés. Intégration de tracing native (Braintrust, etc.).

### 4.4 OpenAI Agents SDK
Primitives : **Runner** (boucle d'exécution), **handoffs** (délégation entre agents), **guardrails** (validation entrée/sortie), **sessions** (mémoire de conversation). Adaptateurs de tracing natifs (Braintrust).

### 4.5 Pydantic AI, DSPy, CrewAI
- **Pydantic AI** : agents typés Python, sorties validées Pydantic, intégration Temporal (voir §4.7) avec consigne **désactiver les retries du client LLM** (`max_retries=0`) car Temporal retry déjà.
- **DSPy (VÉRIFIÉ-SOURCE dspy.ai + stanfordnlp/dspy + arXiv 2310.03714, 2507.19457)** :
  - **Signature** : spec déclarative I/O — inline (`"context, question -> answer"`) ou classe avec `dspy.InputField()`/`dspy.OutputField()` typés (docstring = instruction).
  - **Modules** : `dspy.Predict` (base : formate, appelle le LM, parse), `dspy.ChainOfThought` (raisonnement avant la sortie), `dspy.ReAct(sig, tools=[...])` (boucle d'outils). Interchangeables sans réécrire la tâche.
  - **Optimiseurs (« teleprompters »)**, API `optimizer.compile(program, trainset=...)` :
    - **BootstrapFewShot** : bootstrap de démonstrations few-shot depuis le trainset.
    - **MIPROv2** : optimise conjointement **instructions + démos** en 3 phases (Bootstrap → Propose via `GroundedProposer` LM → **Search par optimisation bayésienne, sampler TPE d'Optuna**). Presets `auto="light"/"medium"/"heavy"`. (Opsahl-Ong et al. 2024.)
    - **GEPA** (Genetic-Pareto, arXiv 2507.19457, **ICLR 2026 Oral**) : évolution réflexive de prompts — échantillonne des **trajectoires**, réfléchit en langage naturel pour diagnostiquer les échecs, combine les leçons via une **frontière de Pareto**. Claims du papier (BENCHMARK, à flaguer) : **+13 % agrégé vs MIPROv2 (+5,6 %)** ; bat **GRPO de ~6 % en moyenne (jusqu'à ~20 %)** avec **jusqu'à 35× moins de rollouts** ; très sample-efficient. Famille incluant aussi SIMBA, COPRO, BootstrapFinetune.
- **CrewAI** : orchestration multi-agents par rôles/tâches (plus haut niveau, moins de contrôle fin).

### 4.6 MCP au niveau protocole
**VÉRIFIÉ-SOURCE, modelcontextprotocol.io spec.** Base **JSON-RPC 2.0**, protocole **stateful** (négociation de capacités via `initialize`). Architecture : Host → Clients (1:1) → Servers.
- **Trois primitives serveur** : **Tools** (model-controlled, `tools/list` + `tools/call`), **Resources** (application-controlled, `resources/list`/`resources/read`, templates URI RFC 6570, subscribe + `notifications/resources/updated`), **Prompts** (user-controlled, `prompts/list`/`prompts/get`).
- **Primitives client** : **Sampling** (`sampling/createMessage` : le serveur demande une complétion LLM au client → serveur indépendant du modèle), **Elicitation** (`elicitation/create` : demande d'info/confirmation à l'utilisateur), **Logging**, **Roots** (bornes filesystem/URI que le client expose au serveur).
- **Transports** : **stdio** (sous-processus, JSON-RPC newline-delimited sur stdin/stdout, logs sur stderr ; local) ; **HTTP+SSE** (legacy, spec 2024-11-05, deux endpoints, **déprécié au 2025-03-26**) ; **Streamable HTTP** (actuel, introduit **2025-03-26**, endpoint unique `/mcp` POST+GET, réponse JSON unique ou upgrade SSE `text/event-stream`, header `Mcp-Session-Id`, 202 Accepted pour notifications). Support SDK TS dans `@modelcontextprotocol/sdk` v1.10.0 (17 avr. 2025), classes `StreamableHTTPServerTransport`/`ClientTransport`.
- **Révisions spec** : 2024-11-05 → 2025-03-26 → 2025-06-18 → 2025-11-25. Négociées au `initialize` (`protocolVersion`, `capabilities`, `clientInfo`/`serverInfo`).

### 4.7 Temporal (exécution durable d'agents)
**VÉRIFIÉ-SOURCE, docs.temporal.io + temporalio/sdk-python.**
- **Workflow** (`@workflow.defn` sur classe, une `@workflow.run`) = orchestration **déterministe** (pas d'I/O, random, threads, horloge directe). **Activity** (`@activity.defn`) = tout ce qui peut échouer/est non-déterministe (appels LLM, API, DB) ; doit être **idempotente**.
- **Replay déterministe** : Temporal persiste un **Event History** immuable ; au crash/redémarrage, le worker rejoue le code mais **saute les activities déjà complétées** (résultats rejoués depuis l'historique) → reprise exacte. Non-déterminisme = échec de workflow task.
- **Timers durables** : `sleep` de jours/mois enregistré comme événement, survit aux crashs.
- **Retries** : les Activities ont une **Retry Policy par défaut** avec backoff exponentiel (`RetryPolicy(initial_interval, backoff_coefficient=2.0, maximum_interval, maximum_attempts, non_retryable_error_types)`). **Une activity qui échoue ne fait jamais échouer directement le workflow** — elle retry. Heartbeats (`activity.heartbeat()`) pour les longues activities. API : `workflow.execute_activity(fn, args, start_to_close_timeout=..., retry_policy=...)` ; `Client.connect(...)`, `client.execute_workflow(...)`, `Worker(client, task_queue=..., workflows=[...], activities=[...])`. Payload limite 2 MB.
- **Pourquoi pour les agents** : rend l'exécution « crash-proof » sur de longs horizons d'appels faillibles ; centralise resilience/retries/timers au lieu de les disperser. Caveat : désactiver les retries du client LLM (sinon double-retry).

---

## 5. CONTEXT ENGINEERING

**VÉRIFIÉ-SOURCE, anthropic.com/engineering/effective-context-engineering-for-ai-agents (29 sept. 2025, sortie avec Sonnet 4.5).** Principe : « find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome ». Justification : « context rot » — la fenêtre grandit, l'attention se dilue (relations en n² entre tokens).
- **Compaction** : résumer la conversation proche de la limite et réinitialiser une fenêtre avec le résumé. Conseil Anthropic : maximiser d'abord le **recall** du prompt de compaction, puis affiner la **precision** ; low-hanging fruit = purger les résultats d'outils anciens (« once a tool has been called deep in the message history, why would the agent need to see the raw result again? »).
- **Just-in-time retrieval** : stocker des identifiants légers et charger les données seulement au besoin (vs tout pré-charger).
- **Structured note-taking** : persister des notes hors fenêtre, les réintroduire au besoin (continuité multi-étapes).
- **Sous-agents (context isolation)** : déléguer à des sous-agents à fenêtre fraîche, l'agent principal ne reçoit que des résumés condensés. Le système de recherche multi-agents d'Anthropic montre des gains substantiels vs single-agent.
- **Outils & memory tool** : Claude Code utilise un **cap de réponse d'outil ~25k tokens** (RAPPORTÉ — à confirmer) ; memory tool (création/lecture/écriture/suppression de fichiers de mémoire) en beta avec Sonnet 4.5 ; **context awareness** (feedback sur la capacité restante après chaque appel) et **programmatic tool calling** (orchestrer les outils via code, ne renvoyer que le résultat final).
- **Structure du system prompt** : assez spécifique pour guider, assez flexible pour des heuristiques larges. **Définitions d'outils** : minimiser le chevauchement fonctionnel, maximiser l'efficacité en tokens, namespacing. **Skills / progressive disclosure** (re:Invent 2025 : SWE-bench 80 % rapporté par Anthropic — RAPPORTÉ).

### Architectures mémoire
- **Court-terme** : conversation (messages en contexte).
- **Long-terme** : vectoriel (sémantique) ou graphe (relations).
- **MemGPT / Letta** : le LLM gère sa propre mémoire paginée (main context vs external context, comme un OS), avec fonctions self-edit de la mémoire.
- **mem0** : couche mémoire (working/episodic) qui extrait et persiste les faits saillants entre sessions.

---

## 6. ÉVALUATION & OBSERVABILITÉ

**VÉRIFIÉ-SOURCE, docs Braintrust/Langfuse + OTel.**
- **Braintrust** : eval-first ; `Eval()` avec des **scorers** (déterministes ou LLM-as-judge), comparaison vs baseline, **GitHub Actions natives pour gates CI** (bloquer le merge si la qualité baisse). Implémente les **OTel GenAI semantic conventions** (mapping auto), `BraintrustSpanProcessor`. Free tier 1M spans/mois (RAPPORTÉ).
- **Langfuse** : open-source (MIT), sur ClickHouse, décorateur **`@observe`** (capture args/retour), ingest OTel first-class, datasets, prompt management. **Racheté par ClickHouse le 16 janv. 2026 (VÉRIFIÉ-SOURCE, blog ClickHouse)** : « We are thrilled to announce that ClickHouse has acquired Langfuse », annoncé avec une Série D de 400 M$ menée par Dragoneer (valorisation 15 Md$) ; licence MIT et self-hosting maintenus.
- **LangSmith** : intégration étroite LangChain/LangGraph (LangGraph Studio), per-seat + per-trace.
- **Arize Phoenix** : OTel-native, conventions OpenInference, open-source.
- **W&B Weave** : pour les équipes déjà sur W&B, harness d'eval.
- **LLM-as-judge** : rubrics explicites ; **pointwise** (note un output) vs **pairwise** (compare deux) ; mitiger le **biais de position** (alterner l'ordre, moyenner). Compléter par des **scorers déterministes** (regex, exact-match, schéma) et des **golden datasets** ; **gates de régression** en CI.
- **OTel GenAI semantic conventions** : schéma vendor-neutral. Attributs `gen_ai.request.model`, token usage, finish reason ; span types LLM call / tool execution / memory / agent orchestration. **Caveat (VÉRIFIÉ-SOURCE)** : à ~v1.41 la spec est en statut *Development* — la plupart des attributs `gen_ai.*` peuvent changer sans bump majeur. Endpoint Braintrust : `https://api.braintrust.dev/otel/v1/traces` avec header `Authorization: Bearer` + `x-bt-parent`.
- **Pattern prod** : eval à 3 couches (unit/déterministe, LLM-as-judge, sampling production) ; **tail-based sampling** (garder tous les traces échoués/coûteux/anormaux, échantillonner le happy-path) ; attribution de coût multi-dimensionnelle (per-user/task/tenant) taguée à la racine du trace.

---

## 7. FINE-TUNING & ADAPTATION

**VÉRIFIÉ-SOURCE, docs Unsloth/HuggingFace TRL/PEFT.**
- **LoRA / QLoRA** : matrices basse-rang sur les couches gelées. Paramètres : **`r`** (rang, capacité ; typique 8–64), **`lora_alpha`** (échelle ; heuristique courante `r` ou `2r`), **`lora_dropout`** (Unsloth optimisé à 0), **`target_modules`** = `["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]` (attention + MLP, recommandé par le papier QLoRA). QLoRA = base en **4-bit (NF4)**, adaptateurs en BF16 → **-75 % VRAM** (70B LLaMA <48 GB). LR typique : **2e-4** pour SFT LoRA, **5e-6** pour RL (DPO/GRPO).
- **Unsloth** : `FastLanguageModel.from_pretrained(..., load_in_4bit=True)` + `get_peft_model(...)` ; **≈2× plus rapide** (kernels Triton, backprop réécrite), compatible HF/PEFT/TRL. Mémoire exemple (Qwen2.5-14B, r=64) : base ~28 GB BF16, adaptateurs ~130 MB, total ~30 GB.
- **TRL** : trainers **`SFTTrainer`**, **`DPOTrainer`**, **`GRPOTrainer`**, `RewardTrainer`, `PPOTrainer` — wrappers légers du Trainer HF, support DDP/DeepSpeed ZeRO/FSDP, intégration PEFT + Unsloth.
- **Axolotl** : config YAML pour SFT/LoRA/full FT.
- **DPO vs PPO vs GRPO vs RLAIF** : **DPO** = optimisation directe sur préférences (pas de reward model séparé), stable et simple ; **PPO** = RL classique avec reward model + critic, plus lourd ; **GRPO** (DeepSeek) = avantages relatifs par groupe sans critic, efficace pour le raisonnement ; **RLAIF** = préférences générées par IA au lieu d'humains.
- **Quand fine-tuner vs RAG vs prompt** : prompt d'abord (rapide, zéro coût d'entraînement) ; RAG pour la connaissance factuelle fraîche/volumineuse ; fine-tuning pour le **style/format/comportement** ou réduire la latence/coût d'un comportement stable. Distillation (logit-matching d'un teacher BF16) et génération de données synthétiques pour amorcer.
- **Serving d'adaptateurs LoRA** : **vLLM multi-LoRA** (hot-swap d'adaptateurs sans recharger la base) et **S-LoRA** (servir des milliers d'adaptateurs concurrents). Sur INT4, utiliser **GPTQ-Int4** (NVFP4 ne supporte pas LoRA). Alternative : **merger** l'adaptateur dans la base puis exporter (ex. GGUF pour llama.cpp/Ollama).

---

## 8. PATTERNS DE PRODUCTION & GUARDRAILS

### 8.1 Sorties structurées (décodage contraint)
**VÉRIFIÉ-SOURCE, papiers XGrammar arXiv 2411.15100, Outlines/Willard-Louf 2023.**
- **Mécanique** : le moteur maintient un état (FSM ou pushdown automaton) et **masque les logits des tokens invalides** à chaque step → seuls les tokens valides sont échantillonnés.
- **Outlines** : approche **FSM** sur la grammaire/regex ; pionnier mais **temps de compilation élevés sur schémas complexes** (40 s à 10+ min) et compliance plus faible sur JSONSchemaBench.
- **XGrammar** : **pushdown automaton byte-level + cache de masque de tokens adaptatif** (tokens context-independent précalculés). **Backend par défaut de vLLM, SGLang, TensorRT-LLM** ; **<40 µs/token**, overhead quasi nul ; meilleur sur structures imbriquées complexes (97,1 % vs 76,4 % pour Outlines sur GitHub issues, Qwen-2.5-32B — papier SLOT).
- **Instructor** : librairie multi-provider qui abstrait les sorties structurées (validation Pydantic, retries).
- **JSON mode / function calling** : niveau API, le plus simple ; **GBNF** (grammaires llama.cpp) pour le contrôle fin local.
- **Caveat (papier Tam et al.)** : forcer le format peut dégrader le raisonnement (charge cognitive) — mesurer sur sa tâche.

### 8.2 Guardrails & défense injection
- **Guardrails AI** (validators déclaratifs entrée/sortie, re-ask), **NeMo Guardrails** (NVIDIA, rails de dialogue en Colang), **Llama Guard** (classifieur de sécurité Meta). Défense injection au niveau code : séparer instructions/données, sandboxer l'exécution de code (isolates V8, cf. §1.3), ne jamais exposer les secrets au LLM (injection au transport), valider/échapper les sorties d'outils.

### 8.3 Streaming, retries, fallbacks, routing
- **litellm** : abstraction unifiée multi-provider (OpenAI/Anthropic/etc.), retries, fallbacks, budget tracking.
- **Router pattern** : router les requêtes vers le bon modèle selon complexité/coût (petit modèle pour le facile, gros pour le difficile), avec fallback en cas de rate-limit. Le provider registry de Vercel AI SDK v5 permet la sélection runtime ; Temporal (§4.7) durabilise retries/fallbacks longs.

---

## Recommandations (étapes concrètes, avec seuils de bascule)

1. **D'abord, instrumenter et cacher (semaine 1).** Activer le prompt caching (Anthropic explicite avec TTL 1 h sur les préfixes vraiment stables ; OpenAI automatique) et tracer en OTel GenAI vers Langfuse (OSS) ou Braintrust (eval-first). **Seuil** : si l'agent fait >3–5 steps et le hit rate cache <50 %, appliquer le « relocation trick » (sortir le dynamique du préfixe). Cible : >70 % de hit.
2. **Serving (semaines 2–3).** Démarrer vLLM (continuous batching par défaut, `gpu_memory_utilization=0.90`, `max_num_batched_tokens=8192–16384`). **Bascule vers SGLang** si préfixes partagés (RAG/multi-tours/agents) — gain attendu 29 % à 6,4×. **Quantifier en FP8** (Hopper/Blackwell) pour qualité quasi-intacte ; AWQ/GPTQ-Marlin INT4 si VRAM contrainte. **Ajouter speculative decoding (EAGLE-3 ou MTP natif)** seulement si α mesuré >0,6 sur le trafic réel ; sinon ne pas l'activer (α<0,5 nuit).
3. **RAG (semaines 2–4).** Chunks 256–512 tokens + Contextual Retrieval (le ROI -49 %/-67 % justifie le coût d'indexation ~1 $/M tokens via caching). Hybride dense+BM25 fusionné par RRF (k=60, ou 10–20 si <300 pages) → reranker (Cohere 3.5 managé ou bge-reranker-v2-m3 sur GPU) top-150→top-20. Embeddings : voyage-3-large ou text-embedding-3-large (Matryoshka pour arbitrer stockage), BGE-M3 si self-hosted. **pgvector HNSW** `m=16, ef_construction=200`, monter `ef_search` si recall insuffisant. **Bascule** vers Qdrant/Vespa si besoin de sparse natif/filtrage avancé à grande échelle.
4. **Orchestration & durabilité (semaine 3+).** LangGraph (Python, checkpointer Postgres en multi-instance, state minimal <10KB) ou Vercel AI SDK (TS). MCP en Streamable HTTP + Code Mode si >quelques serveurs/centaines d'outils (réduction tokens 90 %+). Temporal pour les agents long-running (retries/timers durables). **Seuil Code Mode** : dès que les définitions d'outils dépassent ~10–20 % de la fenêtre.
5. **Eval & gates (continu).** Golden dataset + scorers déterministes + LLM-as-judge (mitiger biais de position) ; gate CI bloquante (Braintrust GitHub Action). **Seuil de release** : pas de régression nette sur faithfulness/context-recall vs baseline.
6. **Fine-tuning (seulement si justifié).** Rester sur prompt+RAG tant que le comportement n'est pas stable et répété. Passer à LoRA/QLoRA (Unsloth + TRL `SFTTrainer`, `r=16–64`, `target_modules` attention+MLP, LR 2e-4) **uniquement** pour figer un style/format ou réduire coût/latence ; DPO/GRPO (LR 5e-6) pour l'alignement préférentiel. Servir en vLLM multi-LoRA.

## Caveats

- **Noms de modèles non vérifiés** : plusieurs sources secondaires (blogs 2026) citaient « Opus 4.8/Mythos », « Sonnet 4.6 », « GPT-5.4 », « Gemma 4 » — invérifiables et probablement extrapolés ; je n'ai utilisé que les **mécanismes** documentés, pas ces noms ni leurs prix.
- **Chiffres fournisseur vs indépendants** : les gains voyage-3-large (+9,74 %), SGLang (+29 %/6,4×), EAGLE-3 (3–6,5×), Code Mode (98,7 %/99,9 %) sont **rapportés par l'auteur/fournisseur** ou par des benchmarks tiers à conditions spécifiques — re-tester sur sa charge. Les économies de caching (59–70 %, ProjectDiscovery) sont dérivées du spend réel (plus fiables) ; le 14–24× de vLLM est mesuré dans le blog officiel vLLM (LLaMA-7B/13B, A10G/A100).
- **Dépendance à la charge** : le débit vLLM/SGLang, l'acceptation du speculative decoding (α) et le bénéfice de RadixAttention dépendent fortement du profil de trafic (longueur prompt/sortie, partage de préfixe, concurrence). Aucun chiffre de tête n'est transférable sans benchmark.
- **OTel GenAI en statut *Development*** : attributs `gen_ai.*` susceptibles de changer ; instrumenter via une couche neutre (OpenLLMetry/OpenInference) pour pouvoir changer de backend.
- **Cap ~25k tokens de Claude Code** : rapporté/secondaire, à confirmer sur la doc primaire. (Le ~1000 tok/s de Cursor est désormais confirmé via le blog Cursor/Fireworks AI, cf. §2.4.)
- **Sécurité Code Mode** : exécuter du code généré par LLM exige un sandbox strict (isolate V8/Starlark, pas d'I/O hors bindings, secrets injectés au transport) — nouvelle surface d'attaque à auditer.

## Liens

- [[serving-inference-optimisation]] — delta décisionnel §2 (serving, quantification, spec decoding, P/D)
- [[prompt-caching-kv-cache]] — delta décisionnel §1 (caching mécanique, relocation trick)
- [[agents-evaluation]] — delta §6 (eval/observabilité, Langfuse→ClickHouse)
- [[rag-embeddings]] — embeddings, Matryoshka, quantization (couvre §3.2)
- [[rag-reranking]] — reranking, hybrid search, RRF (couvre §3.4-3.5)
- [[stack-python-ia]] — stack Python de production
- [[stack-typescript-ia]] — stack TypeScript
- [[fine-tuning-infrastructure]] — GPUs, cloud, serving LoRA (couvre §7)
- [[MOC-Techniques]]
