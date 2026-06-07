# L'État de l'Art du Stack IA en Production (2026) : Audit Ingénieur & Stratégie

## TL;DR
- **Le consensus des labs frontière et des meilleures équipes en production a convergé sur un principe central : commencez simple (un seul LLM + outils dans une boucle), ajoutez la complexité — workflows puis multi-agents — seulement quand les evals le prouvent.** Anthropic ("Building Effective Agents"), OpenAI ("A Practical Guide to Building Agents") et Cognition ("Don't Build Multi-Agents") disent la même chose sous des titres opposés : maximisez d'abord un agent unique ; le multi-agent n'est justifié que pour des tâches read-heavy/parallélisables (recherche), pas pour des tâches write-heavy (coding) où le contexte partagé est critique.
- **Le moat n'est ni le framework ni le modèle : c'est la discipline d'evals + context engineering.** "Evals are the new unit tests" est désormais une pratique établie ; les équipes qui construisent golden datasets, scorers déterministes + LLM-as-judge, et gates de régression CI ont un avantage structurel. Le "prompt engineering" a cédé la place au "context engineering" (curation du budget de tokens) comme compétence centrale.
- **L'économie agentique casse le modèle SaaS par siège.** Les systèmes multi-agents consomment ~15× plus de tokens qu'un chat (les agents simples ~4×) ; les prix par token ont chuté de ~98 % mais les factures IA entreprise ont triplé. Les abonnements flat-rate subventionnent massivement les power-users (Claude Code, Cursor), poussant l'industrie vers le métré, le routing de modèles, l'inférence maison (Cursor Composer) et le pricing à l'outcome.

---

## Key Findings (vérifié vs marketing)

1. **Workflows > agents par défaut.** Anthropic distingue *workflows* (LLM + outils orchestrés par du code prédéfini) et *agents* (le LLM dirige dynamiquement son propre processus). Citation vérifiée : « When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. » Les frameworks « add layers of abstraction » qui compliquent le debug — Anthropic recommande de commencer avec les APIs LLM directes.

2. **Le débat multi-agent est tranché par "read vs write".** Anthropic a publié que son système de recherche multi-agent (Claude Opus 4 lead + sous-agents Sonnet 4) a battu un agent unique Opus 4 de **90,2 %** sur son éval interne — au prix d'une consommation de tokens lourde : « agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats. » Cognition (Devin) a contre-argumenté dans "Don't Build Multi-Agents" que les sous-agents parallèles font des choix implicites conflictuels (l'exemple Flappy Bird : un sous-agent construit un fond Super Mario, un autre un oiseau hors-style, l'agent final doit réconcilier deux malentendus). En 2026, Cognition a nuancé : « we've begun to deploy multi-agent systems that actually work... setups where multiple agents contribute intelligence to a task while writes stay single-threaded. » **Verdict : parallélisez la lecture/recherche, gardez l'écriture mono-threadée.**

3. **MCP (Model Context Protocol) a gagné la guerre des interfaces.** Lancé par Anthropic en nov. 2024, adopté par OpenAI (mars 2025, Sam Altman : « People love MCP and we are excited to add support across our products »), Google DeepMind (Demis Hassabis : « MCP is a good protocol and it's rapidly becoming an open standard for the AI agentic era »), Microsoft. Donné à la Linux Foundation (Agentic AI Foundation, co-fondée avec Block et OpenAI) en déc. 2025. Plus de **10 000 serveurs MCP publics actifs**. OpenAI déprécie son Assistants API (sunset mi-2026) au profit de MCP. **Mais MCP a des failles de sécurité réelles** : tool poisoning (Invariant Labs, avril 2025) et CVE-2025-49596 (RCE critique CVSS 9.4 dans MCP Inspector, corrigé en v0.14.1 le 13 juin 2025).

4. **Code execution with MCP** (Anthropic, 4 nov. 2025) : exposer les serveurs MCP comme des APIs code (le modèle écrit du TypeScript qui appelle les outils) au lieu d'appels d'outils directs « reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7% ». Cloudflare a publié des résultats similaires sous le nom « Code Mode ». Les données lourdes restent dans l'environnement d'exécution ; on peut tokeniser les champs sensibles (le modèle ne voit que des placeholders).

5. **Contextual Retrieval** (Anthropic, sept. 2024) : préfixer chaque chunk d'un contexte généré par LLM avant embedding réduit les échecs de récupération de **35 %** (contextual embeddings seuls), **49 %** (+ contextual BM25 fusionnés par Reciprocal Rank), **67 %** (+ reranking). Rendu économique par le prompt caching (charger le doc une fois). Pour <200 000 tokens (~500 pages), Anthropic recommande de ne PAS faire de RAG du tout — mettez tout dans le contexte. Embeddings recommandés : Gemini et Voyage. Pipeline : top-150 récupérés → reranker → top-20 dans le prompt.

6. **Le marché des modèles s'est rééquilibré.** Selon Menlo Ventures (rapport du 9 déc. 2025, ~500 décideurs entreprise US) : dépense IA entreprise passée de **1,7 Md$ (2023) à 37 Md$ (2025)**, soit un bond de 11,5 Md$ en 2024 à 37 Md$ (×3,2 en un an, « the fastest enterprise category expansion in history ») ; **76 % des cas d'usage sont achetés** (vs 47 % construits en interne en 2024) ; Anthropic ~40 % de part d'usage LLM API entreprise (54 % en coding spécifiquement), OpenAI tombé à 27 %, Google à 21 %. Le coding est la première "killer use case" : 4,0 Md$ sur 7,3 Md$ de dépense départementale, déclenché par Sonnet 3.5 mi-2024. **Flag : estimations d'enquête, pas des comptes audités.**

7. **Klarna : l'échec emblématique walk-back.** Après avoir affirmé en fév. 2024 que son chatbot (partenariat OpenAI) faisait « the work of 700 agents » et gérait 2,3 M chats/mois (résolution de 11 min → <2 min), le CEO Siemiatkowski a admis à Bloomberg (mai 2025) que la sur-pondération du coût avait produit une qualité moindre : « As cost unfortunately seems to have been a too predominant evaluation factor when organizing this, what you end up having is lower quality » — et que le client doit toujours pouvoir joindre « a human if you want ». Klarna ré-embauche des humains (modèle « Uber-style ») pour les cas complexes. **Leçon : l'IA gère le 80 % simple ; les humains gardent le 20 % complexe/empathique ; soignez le handoff (intent classifié + contexte + tentative + score de confiance).**

8. **Ramp : le succès build-it-yourself.** L'agent de coding interne "Inspect" (sur Modal Sandboxes + OpenCode + Cloudflare Durable Objects, câblé à Sentry/Datadog/LaunchDarkly/Braintrust/GitHub/Slack/Buildkite) écrit ~30-50 % des PR mergées ; 80 %+ d'Inspect est écrit par Inspect. Chaque session tourne dans une VM sandboxée avec l'environnement complet (Postgres, Redis, Temporal). Philosophie (Zach Bruggeman) : « The only way you're going to ensure that it is the best... is to build it yourself. » Ramp prévient toutefois : viable seulement avec de fortes compétences infra ; « only by model intelligence itself » reste la limite.

---

## Details

### 1. Langages & Frameworks

**Python** domine le ML/training/data (vLLM, fine-tuning, pipelines). **TypeScript/JS** domine les applications agentiques full-stack et le streaming web. **Rust/Go** pour l'infra perf-critique. Le clivage Python/TS est réel : utiliser un framework agent Python dans un stack TS signifie « maintaining two runtimes, two dependency trees, two deployment pipelines, and a serialization layer between them ».

**Frameworks orchestration :**
- **LangGraph** (Python + JS) : standard de facto pour agents stateful en production. GA en mai 2025, utilisé en prod chez LinkedIn (recruteur IA, SQL Bot), Uber (migrations de code), Replit, Elastic. Architecture graphe (nodes/edges, cycles, conditionals, state persistence, checkpointing). LangChain dit explicitement : « Use LangGraph for agents, not LangChain. » Limites : LangSmith couplé à l'écosystème ; LangGraph Platform non compatible Vercel/Cloudflare Workers par design ; recursion limit ; supervisor parfois instable.
- **Vercel AI SDK** (AI SDK 5, sorti 31 juil. 2025) : « the TypeScript toolkit designed to help developers build AI-powered applications and agents » — API unifiée (generateText/streamText, tool calling, structured objects), classe Agent (« everything you can do with Agent can be done with generateText or streamText »), contrôle de boucle agentique (stopWhen, prepareStep). Idéal pour les UI streaming web (React/Svelte/Vue/Angular).
- **Mastra** (TS, fondateurs de Gatsby, seed 13 M$ oct. 2025, YC W25) : « open-source JavaScript SDK for building agents on top of Vercel's AI SDK » — workflows suspend/resume, RAG, evals, memory, multi-agent, playground local. Pour les équipes TS voulant un framework complet. (Adoption reportée : Marsh McLennan 75 000 employés, Elastic, Docker — *claims vendeur*.)
- **OpenAI Agents SDK** : modèle minimaliste (Model + Tools + Instructions), handoffs, guardrails.
- **CrewAI** : multi-agent role-based, adoption entreprise (levée 18 M$).
- **Microsoft Agent Framework** : fusion d'AutoGen + Semantic Kernel.
- **Temporal / LangGraph checkpointing** : exécution durable pour agents long-running.
- **Pydantic AI, DSPy, Google ADK, LlamaIndex** : niches (validation typée, optimisation de prompts, framework agent Google, data framework).

**Recommandation pour le stack TS/Bun/Hono + Python :** Vercel AI SDK ou Mastra pour les agents côté app TS ; LangGraph (Python) si vous avez besoin de checkpointing/durabilité avancée et de traçage LangSmith ; gardez Python pour le ML/inférence.

### 2. RAG en 2026

L'architecture moderne : chunking → embeddings → vector DB → hybrid search (BM25 + dense, fusion par Reciprocal Rank) → reranking (Cohere Rerank, cross-encoders) → top-K dans le contexte.

**Patterns avancés :**
- **Contextual Retrieval** (cf. Finding 5) : la technique la plus citée ; +reranking fait passer les erreurs de récupération de 5,7 % à 1,9 % dans les tests Anthropic.
- **GraphRAG** : meilleur pour raisonnement multi-hop et domaines relationnels (finance, santé, supply chain) ; coûteux en setup/maintenance (schéma, curation continue). Vector RAG meilleur pour le contenu sémantique. Consensus 2025 : ne pas reconstruire — layer le graphe sur le vector existant. ~73 % des échecs RAG sont au stade retrieval, pas génération ; un embedding 512-dim dégrade au-delà de ~500k documents.
- **RAG vs long-context vs fine-tuning** : <200k tokens → long-context (pas de RAG). Grand corpus dynamique → RAG. Style/format/comportement → fine-tuning. Connaissances factuelles → RAG, pas fine-tuning.
- **Vector DBs** : Pinecone, Weaviate, Qdrant, pgvector (Postgres), Turbopuffer, Vespa. Latences typiques 10-100 ms ; ~0,23 $/Go/mois en managé.
- **Évaluation RAG** : séparer retrieval (context precision/recall@k) et génération (faithfulness/grounding). Ragas est le standard de fait pour le RAG.

### 3. Agents & Orchestration

**Architectures de production :** single-agent (défaut), prompt chaining, routing, orchestrator-workers (Anthropic coding agents sur GitHub issues), evaluator-optimizer loops, supervisor, swarm. OpenAI : « maximize a single agent's capabilities first » ; diviser seulement quand la logique conditionnelle explose ou que les outils se chevauchent (« Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools »).

**Leçons d'Anthropic (système multi-agent recherche) :** l'orchestrateur sur-enthousiaste spawnait 50 sous-agents pour une question simple ; les agents bouclaient à l'infini. Solutions : instructions de délégation précises (objectif, format, outils, limites par sous-agent) ; les modèles Claude 4 agissent comme leurs propres prompt engineers (un tool-testing agent réécrivant les descriptions d'outils a réduit les temps de tâche de ~40 %) ; extended/interleaved thinking comme scratchpad ; requêtes larges d'abord, puis affinées.

**Context engineering** (Anthropic, sept. 2025, avec Sonnet 4.5) : « the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference ». Tactiques : compaction/summarization pour tâches long-horizon ; just-in-time retrieval ; context editing (pruning rule-based) ; tool responses bornés (Claude Code : 25 000 tokens max par défaut) ; fichiers de progression (claude-progress.txt + git history) pour bridger les context windows. Principe : « find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome. »

**Tool design** (Anthropic) : peu d'outils ciblés à fort impact ; consolider (schedule_event plutôt que list+create ; search_logs plutôt que read_logs) ; namespacing (asana_search vs jira_search) ; processus eval-driven (générer des tâches d'éval réelles, collaborer avec un agent pour analyser les résultats).

**Durable execution & HITL :** Temporal et le checkpointing LangGraph pour la reprise sur incident ; checkpoints humains avant toute action irréversible (refunds, suppressions, paiements) ; escalade sur dépassement de seuil d'échec ou action à haut risque.

### 4. Model Layer & Optimization

**Sélection :** baseline avec le modèle le plus capable, puis descendre vers des modèles plus petits là où les evals le permettent. Model routing/cascades : Factory a lancé un router qui choisit le modèle par tâche. Diversité de modèles = norme (>75 % des équipes utilisent plusieurs modèles).

**Fine-tuning vs RAG vs prompting :** Cursor (Composer) a entraîné son propre modèle MoE par RL dans des environnements sandbox (Firecracker VMs sur Anyrun, 500+ pods/s, inférence RL via Fireworks) — Composer 2 atteint 73,7 sur SWE-bench Multilingual et 61,7 sur Terminal-Bench, « 4x faster than similarly intelligent models ». Techniques : self-summarization (chaîner les générations avec reward final propagé), MTP layers pour speculative decoding (2-3× plus rapide), MXFP8/NVFP4 quantization. (La base de Composer serait Kimi K2.5 de Moonshot — *non confirmé officiellement par Cursor*.)

**Optimisation coût :** prompt caching, batch APIs, model cascades, quantization (FP8, 4-bit), speculative decoding, KV-cache (PagedAttention, RadixAttention), semantic caching. Cursor : speculative edits utilisant le code source existant comme "draft tokens" → ~1000 tokens/s (≈13× speedup), avec un modèle Tab ré-entraîné toutes les ~90 min sur les accept/reject.

**Inférence infra :** **vLLM** (défaut, large support modèles/hardware, PagedAttention — « most teams should start with vLLM ») ; **SGLang** (RadixAttention = prefix caching arborescent, idéal RAG/agents/multi-turn, fort sur modèles chinois DeepSeek/Qwen) ; **TensorRT-LLM** (NVIDIA-only, 15-30 % throughput de plus que vLLM sur H100, speculative decoding jusqu'à 3,6×, mais 1-2 semaines de setup ; utilisé par Perplexity) ; **TGI** désormais en mode maintenance (HuggingFace recommande vLLM/SGLang). Serverless GPU : Modal, Replicate, Baseten. Orchestration : Kubernetes, Ray.

### 5. Evaluation & Observability

**"Evals are the new unit tests"** est la thèse centrale. La TDD naïve échoue car les LLMs n'ont pas une sortie déterministe unique. Workflow pragmatique (NurtureBoss, 40+ entreprises) : error analysis → open coding → axial coding → identifier les 3 modes d'échec dominants → construire des evaluators (assertions code pour l'objectif type extraction de date, LLM-judge pour le nuancé type décision de handoff).

**Offline vs online :** offline = unit tests sur golden datasets avant déploiement ; online = scoring asynchrone sur échantillon de trafic prod (drift, requêtes nouvelles). Mix recommandé : ~60 % déterministe (exact match, regex, JSON-schema, latence), ~30 % LLM-as-judge, ~10 % humain. Ne jamais se fier au LLM-judge seul (stochasticité sur stochasticité). Le golden dataset, annoté à la main et versionné en git, est l'artefact le plus précieux. **Coding agents** : graders déterministes (SWE-bench Verified : run les tests ; Terminal-Bench : tâches end-to-end).

**Données LangChain State of Agent Engineering 2025** (1340 réponses, nov-déc 2025) : **57,3 %** ont des agents en prod (vs 51 % en 2024) ; 52,4 % font des evals offline, 37,3 % online ; human review 59,8 %, LLM-as-judge 53,3 %. Customer service = #1 cas d'usage (26,5 %), recherche/data analysis (24,4 %). Les grandes orgs (>10k) avancent plus vite (67 % en prod).

**Outils :** LangSmith (couplé LangChain/LangGraph, tracing zéro-config) ; Braintrust (eval-first, scorers Python sandboxés, gates CI/CD ; Notion est passé de 3 à 30 fixes/jour ; Stripe/Vercel/Zapier/Airtable/Instacart en prod ; Series B à ~800 M$ fév. 2026) ; Langfuse (open-source, racheté par ClickHouse jan. 2026) ; Arize Phoenix (OTel-native) ; W&B Weave ; Promptfoo (red-teaming, racheté par OpenAI mars 2026). **Leçon-clé** : construisez votre propre harness sur vos golden data avant de citer le moindre leaderboard public (l'effet harness sur SWE-bench est énorme).

### 6. Infra & Production Engineering

**Build-vs-buy inférence :** la majorité utilise des APIs ; les acteurs à très haut volume internalisent (Cursor Composer nov. 2025, pour casser le coût retail par token et atteindre la profitabilité brute sur les grands comptes en avril 2026). **Deployment :** serverless GPU (Modal) pour bursty/sandboxes ; Kubernetes/Ray pour le steady-state.

**Sécurité (OWASP Top 10 for LLM Applications 2025) :** LLM01 **Prompt Injection** (#1 deux éditions de suite), LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data/Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector/Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption. « You can't patch your way out of prompt injection » — défense en profondeur requise. **Lethal trifecta** (Simon Willison, juin 2025) : accès aux données privées + exposition au contenu non fiable + capacité de communication externe = vulnérabilité grave ; « MCP makes it very easy for people to glue lots of tools together... so you can accidentally do the trifecta ». Willison insiste : pas de mitigation statistique (« You can't have security mitigations that work on statistics »). Défenses : least-privilege tooling, input/output filtering, human-in-the-loop pour actions irréversibles, tokenisation des données sensibles. Outils/patterns : Llama Guard 3, Azure Prompt Shields, Google DeepMind CaMeL, le paper "Design Patterns for Securing LLM Agents against Prompt Injections" (IBM/Invariant/ETH/Google/Microsoft). **MCP** : tool poisoning (instructions malveillantes cachées dans les descriptions d'outils — PoC exfiltrant ~/.ssh/id_rsa via Cursor), rug pulls, CVE-2025-49596 (RCE), CVE-2025-6514 (mcp-remote, 437k+ environnements). Auditez avec mcp-scan ; traitez tout serveur MCP tiers comme du code non fiable.

### 7. Stratégie & Org

**Build vs buy :** bascule décisive vers le buy (76 % en 2025). Mais les acteurs AI-native build leur tooling propre (Ramp Inspect, Cursor Composer, Block Goose). **Wrapper-vs-moat** : le moat n'est pas le wrapper du modèle mais (a) les evals/golden data propriétaires, (b) le context engineering domaine-spécifique, (c) l'intégration profonde au workflow. Harvey (legal, valorisé 11 Md$) : 25 000+ agents custom exécutant M&A/due diligence/contract review, avec des « embedded legal engineering teams » — moat = données métier + expertise embarquée, pas le modèle.

**Structure des équipes :** montée du "AI engineer" (vs ML engineer) ; forward-deployed/embedded engineers (Palantir, OpenAI, Harvey "legal engineers"). Ramp : non-ingénieurs (PMs, designers) shippent du code via l'agent (clients Slack, web VS Code, extension Chrome, multiplayer). Product-led growth domine (Cursor a atteint 200 M$ ARR avant d'embaucher un seul commercial entreprise ; PLG = 27 % de la dépense IA, ~40 % avec le shadow AI).

**Le shift 2025-2026 :** des chatbots vers les agents ; du prompt engineering vers le context engineering ; l'économie agentique casse le pricing par siège. Les prix par token ont chuté ~98 % depuis 2022 mais les budgets IA entreprise ont triplé (volume agentique). Données de consommation Claude Code : 90 % des users restent sous 30 $/jour actif, moyenne ~150-250 $/dev/mois, mais un user Max 20x à 200 $ peut consommer l'équivalent de 600-1500 $/mois en tokens API ; Cursor estime qu'un abonnement à 200 $ peut correspondre à ~5000 $ de compute sous-jacent (**flag : estimation Cursor, non auditée**). Anthropic a divulgué (juillet 2025) un user consommant « tens of thousands » de dollars d'usage sur un plan à 200 $. Réponses : tiered metering, model routing, inférence maison, pricing à l'outcome (Intercom Fin 0,99 $/résolution, HubSpot 0,50 $/conversation résolue), kill switches/spend ceilings (un cas reporté de facture Claude de ~500 M$ faute de limites).

---

## Recommendations

**Étape 1 — Commencez minimal (semaine 1).** Un seul LLM + tool calling dans une boucle, APIs directes (pas de framework multi-agent). Établissez une baseline avec le modèle le plus capable. *Seuil de passage à l'étape suivante :* la logique conditionnelle du prompt explose, ou >10-15 outils se chevauchent malgré des descriptions claires.

**Étape 2 — Instrumentez avant d'optimiser (semaines 2-3).** Tracing (LangSmith si LangGraph ; sinon Langfuse/Braintrust/Phoenix). Construisez un golden dataset de 50-200 cas annotés à la main, versionnés en git. Mix de scorers 60/30/10 (déterministe/LLM-judge/humain). Gate de régression en CI. *Seuil :* ne déployez aucun changement de prompt/modèle sans score sur le golden set.

**Étape 3 — RAG seulement si nécessaire (semaine 4+).** Corpus <200k tokens → long-context + prompt caching, pas de RAG. Sinon : hybrid search (BM25 + dense) + Contextual Retrieval + reranking (top-150 → top-20). Mesurez recall@k/precision@k par type de requête. GraphRAG seulement si requêtes multi-hop relationnelles le justifient (layer sur le vector existant, ne reconstruisez pas).

**Étape 4 — Context engineering avant multi-agent.** Compaction, just-in-time retrieval, bornage des tool responses, code execution with MCP pour les workflows à gros payloads (gain potentiel ~98 % de tokens). Multi-agent SEULEMENT pour la recherche/lecture parallélisable ; gardez l'écriture mono-threadée.

**Étape 5 — Coût & sécurité (continu).** Prompt caching discipliné, model routing/cascades, batch APIs. Kill switches et spend ceilings par agent/workflow/BU. Défense prompt-injection : least privilege, human-in-the-loop pour actions irréversibles, audit des serveurs MCP (mcp-scan), filtrage I/O. FinOps de tokens : benchmark par tâche/outcome, suivez le coût comme un KPI d'allocation de capital.

**Benchmarks qui changent la décision :** si le LLM-judge diverge >10 % du human review → recalibrez le judge. Si la marge brute tombe sous ~50 % à cause de l'inférence → routez vers des modèles moins chers ou internalisez (les marges AI-native projetées ~52 % en 2026 vs 75-85 % SaaS mûr — ICONIQ). Si >5 % des conversations agent hallucinent des faits/politiques → corrigez les content gaps, pas le prompt (leçon Klarna). Si vous dépassez 62-140 M tokens/dev/mois sur un plan flat → passez au métré ou à l'API.

---

## Caveats

- **Chiffres d'adoption = estimations d'enquête, non audités.** Menlo Ventures (~500 répondants), LangChain (1340 répondants) reflètent des biais d'auto-sélection. Les chiffres de revenu/marge (Cursor ~5000 $ compute, Anthropic ~40 % marge brute, parts de marché LLM) sont des estimations directionnelles, pas des comptes audités.
- **Lab guidance ≠ pratique réelle.** Les labs RECOMMANDENT la simplicité mais déploient eux-mêmes des systèmes multi-agent complexes (Anthropic Research) et des modèles maison (Cursor). Le hype multi-agent dépasse souvent ce que des workflows simples suffisent à accomplir — c'est la divergence la plus importante à garder en tête.
- **Le champ bouge vite.** Versions de modèles, frameworks et prix changent au trimestre (ex. AI SDK 5 → suite, Composer 1 → 2, specs MCP). Vérifiez les specs courantes avant toute décision d'architecture.
- **Sources secondaires polluées par des hallucinations** (noms de modèles futurs inventés, métriques non sourcées). Ce rapport privilégie les sources primaires : blogs d'ingénierie des labs (Anthropic, OpenAI, Cursor, Ramp), docs officielles, OWASP GenAI, Menlo Ventures, LangChain State of Agent Engineering, Cognition, Invariant Labs/Oligo Security, Simon Willison.
- **MCP : adoption massive mais sécurité immature.** Les failles (tool poisoning, RCE) sont réelles et publiquement documentées ; traitez tout serveur MCP tiers comme du code non fiable et appliquez least-privilege + human approval sur les actions à effet de bord.
- **Le statut "vérifié" porte sur l'existence de la déclaration publique, pas sur sa véracité empirique.** Les claims de performance vendeurs (ex. « 4x faster », gains de productivité internes) sont rapportés comme tels et n'ont pas été reproduits indépendamment ici.