---
titre: "Agents IA — Index principal"
resume: "MOC agents IA 2026 : frameworks, architecture, automation, evaluation, securite, leaders, techniques inedites"
aliases:
  - Agents IA
  - AI agents
  - agents intelligents
  - agent IA
  - agentic AI
  - autonomous agents
domaine: ia
type: index
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://arxiv.org/abs/2210.03629"
  - "https://lilianweng.github.io/posts/2023-06-23-agent/"
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Vue d'ensemble

Marche agents IA : **$7.84B en 2025, projete $52.62B en 2030** (MarketsandMarkets). Gartner : **40% des apps enterprise auront des agents task-specific fin 2026**. Claude Code seul genere **4% des commits publics** sur GitHub et **$2B+ revenus annuels** pour Anthropic.

**Formule canonique** : [[Lilian Weng]] (2023) decrit le LLM comme **"the agent's brain"**, complete par 3 composantes : **Planning**, **Memory**, **Tool use**. Verbatim blog : "LLM functions as the agent's brain, complemented by several key components: Planning, Memory, Tool use".

> [!note] Audit 23 mai 2026
> La formule condensee "Agent = LLM + Memory + Planning + Tool Use" longtemps citee dans forge **n'apparait PAS verbatim** dans le blog de Weng. C'est une synthese pedagogique. Le verbatim canonique ci-dessus est preserve. Voir [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]].

**Insight 2026** : le scaffolding (framework + orchestration) ajoute substantiellement aux benchmarks. L'infrastructure compte autant que le modele (cf [[harness-engineering]] et stats GAIA HAL ci-dessous).

## Notes techniques

### Frameworks et outils
- [[agents-frameworks]] — LangGraph, CrewAI, AutoGen, Claude SDK, OpenAI SDK, Google ADK, no-code
- [[agents-architecture]] — ReAct, multi-agent, orchestration, memory, tool use, planning, communication

### Production et automation
- [[agents-automation]] — Workflows, CI/CD, BPA, scheduling, Computer Use, browser agents
- [[agents-evaluation]] — Benchmarks (SWE-bench, GAIA), testing, deploy, observabilite
- [[agents-securite]] — OWASP top 10 agentic, sandboxing, prompt injection, audit

## Experts et leaders

### Createurs de frameworks
- [[Harrison Chase]] — LangChain/LangGraph, Deep Agents, context engineering
- [[Joao Moura]] — CrewAI, role-based agents
- [[Shunyu Yao]] — ReAct, Tree of Thoughts, SWE-agent, Chief AI Scientist Tencent

### Anthropic (Claude Code)
- [[Boris Cherny]] — createur Claude Code, "coding is largely solved" (verbatim, repris par Lenny comme titre editorial "Coding is solved")
- [[Erik Schluntz]] — "Building Effective Agents" (Anthropic, co-ecrit avec Zhang)
- [[Thariq Shihipar]] — Skills system, 9 categories

### Visionnaires
- [[Andrej Karpathy]] — Software 3.0, agentic engineering, vibe coding
- [[Andrew Ng]] — 4 design patterns agents (Reflection, Tool Use, Planning, Multi-agent)
- [[Lilian Weng]] — VP Research OpenAI, blog canonique sur les agents
- [[Jim Fan]] — NVIDIA, co-auteur Voyager (premier auteur Guanzhi Wang)
- [[Simon Willison]] — Agentic Engineering Patterns, LLM CLI, lethal trifecta
- [[Yohei Nakajima]] — BabyAGI, autonomous task loops
- [[Ethan Mollick]] — Equation of Agentic Work, One Useful Thing

## Decision rapide frameworks (2026)

| Besoin | Framework |
|--------|-----------|
| Production complexe, audit trail | LangGraph |
| Prototype rapide, roles | CrewAI |
| Type-safe Python | Pydantic AI |
| Ecosysteme OpenAI | OpenAI Agents SDK |
| Ecosysteme Google, A2A | Google ADK |
| Enterprise .NET | Semantic Kernel / Microsoft Agent Framework |
| Anthropic natif | Claude Agent SDK |
| No-code, SMB | Lindy AI, Relevance AI |
| Open-source full platform | Dify + n8n |

## Protocoles de communication

- **MCP** (Anthropic) — agent → outils. Adoption massive 2026, **~10K servers publics**, 143+ orgs dans Agentic AI Foundation (Linux Foundation). OpenAI, Google, Microsoft supportent MCP.
- **A2A** (Google) — agent → agent. **v1.0 publiee 12 mars 2026**, adoption en croissance.

Production utilise les deux. MCP resout agent→tool, A2A resout agent→agent.

## Benchmarks headline (mai 2026)

| Benchmark | Leader | Score |
|-----------|--------|-------|
| SWE-bench Verified | GPT-5.5 | 88.7% |
| SWE-bench Pro | Claude Opus 4.7 | 64.3% |
| GAIA (scaffolded HAL) | Claude Sonnet 4.5 | 74.6% (vs 44.8% bare = +30pts gap) |
| WebArena | Claude Mythos Preview | 68.7% ⚠️ |
| TAU-bench | Claude Mythos Preview | 89.2% ⚠️ |

> ⚠️ Claude Mythos Preview = annonce Anthropic Project Glasswing (7 avril 2026), acces restreint. Benchmarks Mythos = single source Anthropic, a confirmer quand modele en GA.

## Papers fondamentaux

1. Yao et al. (2022) — [ReAct](https://arxiv.org/abs/2210.03629) — ICLR 2023
2. Yao et al. (2023) — [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
3. Weng (2023) — [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
4. Schluntz & Zhang (2024) — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) (Anthropic)
5. Park et al. (2023) — [Generative Agents](https://arxiv.org/abs/2304.03442)
6. **Wang et al. (2023)** — [Voyager](https://arxiv.org/abs/2305.16291) — premier auteur Guanzhi Wang, co-auteur Linxi "Jim" Fan
7. Zhou et al. (2024) — [LATS](https://arxiv.org/abs/2310.04406) — ICML 2024

## Liens

- [[MOC-Techniques]]
- [[RAG]] — RAG pipeline (complementaire aux agents)
- [[techniques-inedites]] — Combinaisons innovantes RAG + agents
- [[Andrej Karpathy]] — Software 3.0

### Pionniers agents autonomes
- [[Chi Wang]] — AutoGen/AG2, multi-agent conversationnel, Google DeepMind
- [[Yohei Nakajima]] — BabyAGI, task loop autonome, premier agent open-source populaire
- [[Joao Moura]] — CrewAI, role-based multi-agent
- [[David Shapiro]] — ACE Framework, architecture cognitive
- [[Div Garg]] — MultiOn, agents web autonomes
- [[Dario Amodei]] — CEO Anthropic, cadre securite agents (RSP, ASL levels)
