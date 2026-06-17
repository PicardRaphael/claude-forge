---
titre: "Agents Architecture — Patterns et design"
resume: "Patterns architecture agents IA 2026 : ReAct, multi-agent, orchestration, memory, tool use, MCP, A2A, planning, context engineering"
aliases:
  - agent architecture
  - architecture agents
  - multi-agent patterns
  - ReAct pattern
  - agent orchestration
  - agent memory
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://arxiv.org/abs/2210.03629"
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://lilianweng.github.io/posts/2023-06-23-agent/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---
## Core patterns

### ReAct (Reasoning + Acting)
Backbone de tous les agents production 2026. Interleave Thought → Act → Observe. Failure modes : **long-horizon drift** (l'erreur s'accumule sur les sequences longues — calcul illustratif type ~95%/step compose mal sur 10+ steps), **error cascade**.

### Plan-and-Execute
Planner emet plan, executor (modele moins cher) execute. Moins cher mais fragile si adaptation mid-run necessaire.

### Reflexion
Etend ReAct avec auto-critique apres chaque iteration. Reduit les patterns d'echec repetes.

### LATS (Language Agent Tree Search)
MCTS + LLM (Zhou et al. 2024, ICML 2024). LLM = action generator + value function + reflection. **94.4% pass@1 HumanEval** (verbatim arXiv 2310.04406), bat ReAct/Reflexion/ToT. Le plus performant mais couteux.

## Multi-agent

| Pattern | Description | Usage |
|---------|------------|-------|
| **Supervisor** | Coordinateur central route vers specialistes | Workflows structures |
| **Swarm/Handoff** | Transfert sequentiel decentralise, 1 agent actif | Faible interdependance |
| **Pipeline** | Ordre fixe, chaque agent refine | Processus non-negociable |
| **Graph/Mesh** | Edges conditionnels, cycles, routage dynamique | Le plus flexible (LangGraph) |

Voir [[pattern-orchestrateur]], [[pattern-swarm]], [[pattern-pipeline]], [[pattern-single-agent-multi-tool]] pour details et code.

L'orchestration est souvent le maillon faible des deploiements agents enterprise (cf [[harness-engineering]] : 65% des echecs tracent au harness, TechTimes 13 mai 2026).

### Doctrine simple → workflows → multi-agent (consensus labs 2026)

Le consensus des labs frontière a convergé (Anthropic *Building Effective Agents*, OpenAI *A Practical Guide to Building Agents*, Cognition *Don't Build Multi-Agents*) : **maximisez d'abord un agent unique**, ajoutez la complexité — workflows puis multi-agents — **seulement quand les evals le prouvent**.

Distinction canonique : **workflows** (LLM + outils orchestrés par du code prédéfini) vs **agents** (le LLM dirige dynamiquement son processus). OpenAI : « maximize a single agent's capabilities first » ; diviser quand la logique conditionnelle explose ou que les outils se chevauchent (« Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools »).

### Read vs write — comment trancher le multi-agent

Anthropic : son multi-agent recherche (Opus 4 lead + sous-agents Sonnet 4) a battu un agent unique Opus 4 de **90,2%** sur son éval interne, au prix de ~15× les tokens d'un chat. Cognition a contre-argumenté (sous-agents parallèles = choix implicites conflictuels, ex. Flappy Bird : un sous-agent fait un fond Super Mario, un autre un oiseau hors-style). En 2026, Cognition a nuancé : « multiple agents contribute intelligence to a task **while writes stay single-threaded** ».

> [!tip] Verdict canonique read/write
> **Parallélisez la lecture/recherche (read-heavy). Gardez l'écriture mono-threadée (write-heavy, ex. coding)** — le contexte partagé est critique en write. Cf [[stack-ia-production-2026]] (thèse 2) + [[decoupe-agents-anti-crash]].

### Leçons Anthropic (système multi-agent recherche)

- **Orchestrateur sur-enthousiaste** : spawnait 50 sous-agents pour une question simple ; les agents bouclaient à l'infini. Fix : **instructions de délégation précises** (objectif, format, outils, limites par sous-agent).
- Les modèles Claude 4 **agissent comme leurs propres prompt engineers** : un tool-testing agent réécrivant les descriptions d'outils a réduit les temps de tâche de **~40%** (claim Anthropic, existence vérifiée). Cf [[prompt-rewriter-pattern]].
- **Extended/interleaved thinking** comme scratchpad ; requêtes larges d'abord, puis affinées.

## Memory

Marche significatif en 2026 (croissance forte sur 2025-2030, sources tierces a confirmer ; eviter chiffres precis non sourcables).

| Type | Role | Persistance |
|------|------|------------|
| Short-term | Context window | Session |
| Long-term (semantique) | Facts, knowledge | Permanent (vector/graph) |
| Episodic | Interactions passees | Cross-session |
| Procedural | Workflows appris | Permanent |

Pattern dominant : **hybride vector + graph + episodic buffer**. Memory Router classifie et route les ecritures.

**Frameworks de mémoire (notes dédiées)** : [[memoire-agent-mem0]] (couche universelle agnostique, extraction/consolidation LLM, cross-session multi-user) et [[memoire-agent-langmem]] (LangChain-native, différenciateur = mémoire procédurale qui réécrit le prompt système). Autres acteurs cités : Zep/Graphiti (graphe temporel), Letta/MemGPT (self-editing).

> Synthese forge — pas de verbatim externe identifie : "10M tokens de context ne remplacent pas la memoire — complements, pas substituts" et "Le modele n'est pas le produit — la memoire l'est". Slogans pedagogiques, pas des citations sourcees.

## Tool Use & Protocoles

### MCP (Anthropic) — agent → outils
Client-Host-Server, model-agnostic. Adoption massive 2026, **~10K servers publics**, 143+ orgs dans Agentic AI Foundation (Linux Foundation). OpenAI, Google, Microsoft supportent MCP.

### A2A (Google) — agent → agent
Agent Cards (JSON) pour discovery. HTTP/SSE/JSON-RPC. **v1.0 publiee 12 mars 2026**, adoption en croissance (binding gRPC ajoute via header `A2A-Version`). Task lifecycle : submitted → working → input-required → completed.

**MCP resout agent→tool. A2A resout agent→agent. Production utilise les deux.**

> [!note] Réconciliation des chiffres « serveurs MCP »
> Deux mesures distinctes circulent, ne pas les confondre : **~10 000+ serveurs MCP publics actifs** (écosystème ouvert, tout serveur déployé) vs **308 serveurs / 2 797 tools** dans le **registre officiel** Model-Context-Protocol (cf [[tool-retrieval-query-expansion]], MCP-Zero). L'écosystème public ≫ le registre curé. MCP donné à la **Linux Foundation** (Agentic AI Foundation, co-fondée avec Block et OpenAI, déc. 2025).

### Code execution with MCP — réduction tokens

Exposer les serveurs MCP comme des **APIs code** (le modèle écrit du TypeScript/Python qui appelle les outils) au lieu d'appels d'outils directs réduit massivement les tokens — Anthropic rapporte **150 000 → 2 000 tokens (-98,7%)** sur un cas type. Cloudflare a publié des résultats similaires sous « Code Mode ». Les données lourdes restent dans l'environnement d'exécution ; les champs sensibles peuvent être tokenisés (le modèle ne voit que des placeholders). Pattern jumeau côté Claude Code : [[programmatic-tool-calling]] (code orchestre, modèle juge).

### Sécurité MCP — failles réelles

MCP a gagné la guerre des interfaces MAIS sa sécurité est immature : **tool poisoning** (Invariant Labs, avril 2025 — instructions malveillantes cachées dans les descriptions d'outils, PoC exfiltrant `~/.ssh/id_rsa` via Cursor), **CVE-2025-49596** (RCE CVSS 9.4 dans MCP Inspector), **CVE-2025-6514** (mcp-remote, 437k+ environnements). Traiter tout serveur MCP tiers comme du **code non fiable** ; auditer avec `mcp-scan`. Cf [[agents-securite]] (lethal trifecta, least-privilege).

## Planning

| Technique | Description | Performance |
|-----------|------------|------------|
| Tree-of-Thought | Branches DFS/BFS guidees par heuristic LM | Bon pour raisonnement delibere |
| Graph-of-Thought | Relations complexes entre idees | Ajustement dynamique |
| **LATS** | MCTS + LLM triple role | 94.4% HumanEval, 0.61 EM HotPotQA (arXiv 2310.04406) |
| Adaptive | LLM charge dynamiquement des "skills" | Deep Agents (Harrison Chase) |

## Context Engineering

[[Andrej Karpathy]] (Sequoia 2026) positionne le **context window comme levier** sur le LLM interprete. Software 3.0.

[[Harrison Chase]] : **"context engineering = amener la bonne information dans le bon format au LLM au bon moment"** (verbatim canonique confirme audit 23 mai).

Claude Code implemente : pipeline compaction 5 couches + CLAUDE.md persistent + auto-memory.

## Securite

Voir [[agents-securite]] pour details. Points critiques :
- **OWASP Top 10 for Agentic Applications** (decembre 2025, premier framework peer-reviewed)
- **Prompt injection** = #1 menace, presente dans **73% des deploiements production** (source Cisco State of AI Security)
- Pattern **Dual-LLM** (Simon Willison) : LLM privilegie (tools) ≠ LLM quarantaine (contenu non-fiable)

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-frameworks]] — Comparatif frameworks
- [[agents-automation]] — Patterns automation
- [[memoire-agent-mem0]] — couche mémoire universelle agnostique
- [[memoire-agent-langmem]] — mémoire LangChain-native (procédurale)
- [[Shunyu Yao]] — ReAct, ToT, LATS
- [[Lilian Weng]] — LLM = brain + Planning + Memory + Tool use (verbatim blog 2023)
- [[harness-engineering]] — 4e paradigme AI Engineering
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
