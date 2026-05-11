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
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://arxiv.org/abs/2210.03629"
  - "https://www.anthropic.com/research/building-effective-agents"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Core patterns

### ReAct (Reasoning + Acting)
Backbone de tous les agents production 2026. Interleave Thought → Act → Observe. Failure modes : **long-horizon drift** (95%/step → ~60% sur 10 steps), **error cascade**.

### Plan-and-Execute
Planner émet plan, executor (modèle moins cher) exécute. Moins cher mais fragile si adaptation mid-run nécessaire.

### Reflexion
Étend ReAct avec auto-critique après chaque itération. Réduit les patterns d'échec répétés.

### LATS (Language Agent Tree Search)
MCTS + LLM (ICML 2024). LLM = action generator + value function + reflection. **94.4% pass@1 HumanEval**, bat ReAct/Reflexion/ToT. Le plus performant mais coûteux.

## Multi-agent

| Pattern | Description | Usage |
|---------|------------|-------|
| **Supervisor** | Coordinateur central route vers spécialistes | Workflows structurés |
| **Swarm/Handoff** | Transfert séquentiel décentralisé, 1 agent actif | Faible interdépendance |
| **Pipeline** | Ordre fixe, chaque agent refine | Processus non-négociable |
| **Graph/Mesh** | Edges conditionnels, cycles, routage dynamique | Le plus flexible (LangGraph) |

**57% des échecs** d'agents enterprise viennent de l'orchestration, pas des modèles.

## Memory

Marché : $6.27B en 2026, projeté $28.45B en 2030. "Le modèle n'est pas le produit — la mémoire l'est."

| Type | Rôle | Persistance |
|------|------|------------|
| Short-term | Context window | Session |
| Long-term (sémantique) | Facts, knowledge | Permanent (vector/graph) |
| Episodic | Interactions passées | Cross-session |
| Procedural | Workflows appris | Permanent |

Pattern dominant : **hybride vector + graph + episodic buffer**. Memory Router classifie et route les écritures.

10M tokens de context NE REMPLACENT PAS la mémoire — compléments, pas substituts.

## Tool Use & Protocoles

### MCP (Anthropic) — agent → outils
Client-Host-Server, model-agnostic. **97M downloads SDK/mois**, 20K+ servers, 143+ orgs dans Agentic AI Foundation (Linux Foundation). OpenAI, Google, Microsoft supportent MCP.

### A2A (Google) — agent → agent
Agent Cards (JSON) pour discovery. HTTP/SSE/JSON-RPC. v1.2, **150+ orgs prod**. Task lifecycle : submitted → working → input-required → completed.

**MCP résout agent→tool. A2A résout agent→agent. Production utilise les deux.**

## Planning

| Technique | Description | Performance |
|-----------|------------|------------|
| Tree-of-Thought | Branches DFS/BFS guidées par heuristic LM | Bon pour raisonnement délibéré |
| Graph-of-Thought | Relations complexes entre idées | Ajustement dynamique |
| **LATS** | MCTS + LLM triple rôle | 94.4% HumanEval, 0.61 EM HotPotQA |
| Adaptive | LLM charge dynamiquement des "skills" | Deep Agents (Harrison Chase) |

## Context Engineering

[[Andrej Karpathy]] (Sequoia 2026) : Software 3.0 — le context window EST le programme, le LLM est l'interprète.

[[Harrison Chase]] : "Context engineering = amener la bonne information dans le bon format au LLM au bon moment."

Claude Code implémente : pipeline compaction 5 couches + CLAUDE.md persistent + auto-memory.

## Sécurité

Voir [[agents-securite]] pour détails. Points critiques :
- OWASP Top 10 for Agentic Applications (déc 2025)
- Prompt injection = #1 menace, présent dans **73% des déploiements production**
- Pattern **Dual-LLM** : LLM privilégié (tools) ≠ LLM quarantainé (contenu non-fiable)

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-frameworks]] — Comparatif frameworks
- [[agents-automation]] — Patterns automation
- [[Shunyu Yao]] — ReAct, ToT, LATS
- [[Lilian Weng]] — Agent = LLM + memory + planning + tools
