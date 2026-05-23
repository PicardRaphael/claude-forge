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
derniere-maj: 2026-05-23
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

## Memory

Marche significatif en 2026 (croissance forte sur 2025-2030, sources tierces a confirmer ; eviter chiffres precis non sourcables).

| Type | Role | Persistance |
|------|------|------------|
| Short-term | Context window | Session |
| Long-term (semantique) | Facts, knowledge | Permanent (vector/graph) |
| Episodic | Interactions passees | Cross-session |
| Procedural | Workflows appris | Permanent |

Pattern dominant : **hybride vector + graph + episodic buffer**. Memory Router classifie et route les ecritures.

> Synthese forge — pas de verbatim externe identifie : "10M tokens de context ne remplacent pas la memoire — complements, pas substituts" et "Le modele n'est pas le produit — la memoire l'est". Slogans pedagogiques, pas des citations sourcees.

## Tool Use & Protocoles

### MCP (Anthropic) — agent → outils
Client-Host-Server, model-agnostic. Adoption massive 2026, **~10K servers publics**, 143+ orgs dans Agentic AI Foundation (Linux Foundation). OpenAI, Google, Microsoft supportent MCP.

### A2A (Google) — agent → agent
Agent Cards (JSON) pour discovery. HTTP/SSE/JSON-RPC. **v1.0 publiee 12 mars 2026**, adoption en croissance (binding gRPC ajoute via header `A2A-Version`). Task lifecycle : submitted → working → input-required → completed.

**MCP resout agent→tool. A2A resout agent→agent. Production utilise les deux.**

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
- [[Shunyu Yao]] — ReAct, ToT, LATS
- [[Lilian Weng]] — LLM = brain + Planning + Memory + Tool use (verbatim blog 2023)
- [[harness-engineering]] — 4e paradigme AI Engineering
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
