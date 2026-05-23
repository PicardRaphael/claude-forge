---
titre: "Agents Evaluation — Benchmarks et testing"
resume: "Benchmarks agents 2026 (SWE-bench, GAIA, WebArena, TAU-bench), frameworks eval, testing patterns, deploy production"
aliases:
  - agent evaluation
  - agent benchmarks
  - SWE-bench
  - GAIA benchmark
  - agent testing
  - evaluation agents
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.swebench.com/"
  - "https://gaia-benchmark.github.io/"
  - "https://docs.ragas.io/en/stable/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Benchmarks mai 2026

### SWE-bench (coding)

| Agent | Verified | Pro |
|-------|---------|-----|
| GPT-5.5 | **88.7%** | — |
| Claude Opus 4.7 | 87.6% | **64.3%** (leader) |
| GPT-5.3 Codex | 85.0% | 56.8% |
| Gemini 3.1 Pro | 75-80.6% | — |

> Devin (Cognition Labs) : chiffres officiels variables selon variante (Lite vs Verified), retire de ce tableau faute de chiffre Verified canonique consolide audit 23 mai.

**Scaffolding +5-15 pts** : Gemini 3.1 Pro passe de ~55% a 80.2% avec TongAgents. Donnee illustrative de l'importance du harness.

### GAIA (assistant general)
**30-point gap** entre scaffolded (HAL 74.6% avec Sonnet 4.5) et bare (44.8%) — verbatim Anthropic. **L'infrastructure compte autant que le modele** (cf [[harness-engineering]]).

### WebArena (navigation web)
**Claude Mythos Preview** 68.7% (single source Anthropic Project Glasswing, 7 avril 2026, acces restreint). Humain ~78%.

### TAU-bench (tool-agent-user)
**Claude Mythos Preview** 89.2% sur scenarios enterprise multi-turn (⚠️ meme single source).

> ⚠️ **Tous les scores Mythos** = single source Anthropic Project Glasswing, acces restreint. A re-verifier quand Mythos passera en GA.

### Integrite des benchmarks
Berkeley/RDI aurait casse plusieurs benchmarks majeurs via reward hacking (avril 2026). ⚠️ Single source a re-verifier. Pour scores tiers, preferer Epoch AI / BenchLM.

## Frameworks d'evaluation

| Plateforme | Force | Prix |
|-----------|-------|------|
| LangSmith | Deep LangChain, annotation queues | Free 5K traces, $39+/seat |
| Langfuse | Open-source MIT, 19K stars, self-hostable | Free |
| Arize Phoenix | OTel-natif, embedding drift | Open-source + commercial |
| AgentOps | Session lifecycle, loop detection | SDK-based |
| DeepEval | 50+ metriques, pytest, CI/CD gates | — |
| Braintrust | Eval gates CI/CD, prompt optimization | — |

### Trajectory vs Outcome
Evaluer un agent uniquement sur l'output final surestime la qualite par rapport a une evaluation par trajectoire (les echecs sont au niveau step : tool call args, state propagation, goal drift). **Toujours mesurer la trajectoire** quand c'est possible.

### LLM-as-Judge
Ajoute de la latence par check (~1s ordre de grandeur). Pour inline rapide : Galileo Luna-2 (3B/8B) = sub-200ms.

## Testing agents

### Pyramide de tests
1. **Unit** (base) : tool functions, prompt templates, output parsers, memory
2. **Integration** : agent+tools, agent+memory, multi-agent
3. **Behavioral** : scenarios, adversarial, regression, safety
4. **E2E** (top) : full conversations, prod simulations, load

**Eval-driven development** = TDD pour agents : definir evaluations AVANT de build.

### Mocking
Mock la couche LLM via dependency injection. AWS ToolSimulator : intercepte tool calls → LLM-based response generator (pas de fixtures manuelles).

### CI/CD
DeepEval + pytest : 90% pass-rate threshold bloque les merges. Golden datasets avec trajectoires completes (pas juste Q&A).

## Deploy production

### Managed platforms

| Plateforme | Force |
|-----------|-------|
| Claude Managed Agents | Zero-infra, sandbox integre, Dreams |
| AWS Bedrock AgentCore | Serverless, isolation session, 8h workloads |
| Azure AI Foundry | GPU VMs + AKS, M365/Teams |
| Vertex AI Agent Builder | ADK + eval framework integre |

### Scaling
Kubernetes pod autoscaling. Queue-based (SQS, Pub/Sub). Rate limiting per-tenant token bucket. Tail-based sampling : garder toutes traces avec erreurs, sampler le reste a 5-10%.

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-frameworks]] — Frameworks compares
- [[agents-securite]] — Securite et guardrails
- [[rag-evaluation]] — Evaluation RAG (RAGAS)
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
