---
titre: "Agents IA — Index principal"
resume: "MOC agents IA 2026 : frameworks, architecture, automation, évaluation, sécurité, leaders, techniques inédites"
aliases:
  - Agents IA
  - AI agents
  - agents intelligents
  - agent IA
  - agentic AI
  - autonomous agents
domaine: ia
type: index
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://arxiv.org/abs/2210.03629"
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Vue d'ensemble

Le marché des agents IA : **$7.84B en 2025**, projeté $52.62B en 2030. Gartner : 40% des apps enterprise auront des agents task-specific fin 2026. Claude Code seul génère 4% des commits GitHub mondiaux et $2B+ de revenus annuels pour Anthropic.

**Formule canonique** ([[Lilian Weng]], 2023) : Agent = LLM + Memory + Planning + Tool Use

**Insight 2026** : le scaffolding (framework + orchestration) ajoute **5-15 points** à n'importe quel benchmark. L'infrastructure compte autant que le modèle.

## Notes techniques

### Frameworks et outils
- [[agents-frameworks]] — LangGraph, CrewAI, AutoGen, Claude SDK, OpenAI SDK, Google ADK, no-code
- [[agents-architecture]] — ReAct, multi-agent, orchestration, memory, tool use, planning, communication

### Production et automation
- [[agents-automation]] — Workflows, CI/CD, BPA, scheduling, Computer Use, browser agents
- [[agents-evaluation]] — Benchmarks (SWE-bench, GAIA), testing, deploy, observabilité
- [[agents-securite]] — OWASP top 10 agentic, sandboxing, prompt injection, audit

## Experts et leaders

### Créateurs de frameworks
- [[Harrison Chase]] — LangChain/LangGraph, Deep Agents, context engineering
- [[Joao Moura]] — CrewAI, role-based agents
- [[Shunyu Yao]] — ReAct, Tree of Thoughts, SWE-agent, Chief AI Scientist Tencent

### Anthropic (Claude Code)
- [[Boris Cherny]] — créateur Claude Code, "Coding is solved"
- [[Erik Schluntz]] — Building Effective Agents, 22K-line PR
- [[Thariq Shihipar]] — Skills system, 9 catégories

### Visionnaires
- [[Andrej Karpathy]] — Software 3.0, agentic engineering, vibe coding
- [[Andrew Ng]] — 4 design patterns agents (Reflection, Tool Use, Planning, Multi-agent)
- [[Lilian Weng]] — Agent = LLM + memory + planning + tool use
- [[Jim Fan]] — NVIDIA Voyager/GROOT, Foundation Agent
- [[Simon Willison]] — Agentic Engineering Patterns, LLM CLI
- [[Yohei Nakajima]] — BabyAGI, autonomous task loops
- [[Ethan Mollick]] — Equation of Agentic Work, One Useful Thing

## Décision rapide frameworks (2026)

| Besoin | Framework |
|--------|-----------|
| Production complexe, audit trail | LangGraph |
| Prototype rapide, rôles | CrewAI |
| Type-safe Python | Pydantic AI |
| Écosystème OpenAI | OpenAI Agents SDK |
| Écosystème Google, A2A | Google ADK |
| Enterprise .NET | Semantic Kernel / Microsoft Agent Framework |
| Anthropic natif | Claude Agent SDK |
| No-code, SMB | Lindy AI, Relevance AI |
| Open-source full platform | Dify + n8n |

## Protocoles de communication

- **MCP** (Anthropic) — agent → outils, 97M downloads/mois, Linux Foundation
- **A2A** (Google) — agent → agent, 150+ orgs prod, v1.2

Production utilise les deux. Joint MCP/A2A interoperability spec anticipée.

## Benchmarks headline (mai 2026)

| Benchmark | Leader | Score |
|-----------|--------|-------|
| SWE-bench Verified | GPT-5.5 | 88.7% |
| SWE-bench Pro | Claude Opus 4.7 | 64.3% |
| GAIA (scaffolded) | Claude Sonnet 4.5 + HAL | 74.6% |
| WebArena | Claude Mythos Preview | 68.7% |
| TAU-bench | Claude Mythos Preview | 89.2% |

## Papers fondamentaux

1. Yao et al. (2022) — [ReAct](https://arxiv.org/abs/2210.03629) — ICLR 2023 Oral
2. Yao et al. (2023) — [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
3. Weng (2023) — [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
4. Schluntz et al. (2024) — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) (Anthropic)
5. Park et al. (2023) — [Generative Agents](https://arxiv.org/abs/2304.03442)
6. Fan et al. (2023) — [Voyager](https://arxiv.org/abs/2305.16291)
7. Zhou et al. (2024) — [LATS](https://arxiv.org/abs/2310.04406) — ICML 2024

## Liens

- [[RAG]] — RAG pipeline (complémentaire aux agents)
- [[techniques-inedites]] — Combinaisons innovantes RAG + agents
- [[agentic-engineering-karpathy]] — Software 3.0
