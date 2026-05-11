---
titre: "Agents Évaluation — Benchmarks et testing"
resume: "Benchmarks agents 2026 (SWE-bench, GAIA, WebArena, TAU-bench), frameworks eval, testing patterns, deploy production"
aliases:
  - agent evaluation
  - agent benchmarks
  - SWE-bench
  - GAIA benchmark
  - agent testing
  - évaluation agents
domaine: ia
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://rapidclaw.dev/blog/ai-agent-benchmarks-2026"
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
| Devin | ~51.5% | — |

**Scaffolding +5-15 pts** : Gemini 3.1 Pro passe de ~55% à 80.2% avec TongAgents.

### GAIA (assistant général)
30-point gap entre scaffolded (74.6%) et bare (44.8%) = **l'infrastructure compte autant que le modèle**.

### WebArena (navigation web)
Claude Mythos Preview 68.7%, humain ~78%. Progress de 14.41% baseline à 68.7%.

### TAU-bench (tool-agent-user)
Claude Mythos Preview **89.2%** sur scenarios enterprise multi-turn.

### Intégrité des benchmarks
Berkeley/RDI a cassé les 8 benchmarks majeurs via reward hacking (avril 2026). Préférer Epoch AI / BenchLM scores tiers.

## Frameworks d'évaluation

| Plateforme | Force | Prix |
|-----------|-------|------|
| LangSmith | Deep LangChain, annotation queues | Free 5K traces, $39+/seat |
| Langfuse | Open-source MIT, 19K stars, self-hostable | Free |
| Arize Phoenix | OTel-natif, embedding drift | Open-source + commercial |
| AgentOps | Session lifecycle, loop detection | SDK-based |
| DeepEval | 50+ métriques, pytest, CI/CD gates | — |
| Braintrust | Eval gates CI/CD, prompt optimization | — |

### Trajectory vs Outcome
Agents évalués uniquement sur output final passent **20-40% plus de tests** que l'évaluation par trajectoire. Les échecs sont au niveau step : tool call args, state propagation, goal drift.

### LLM-as-Judge
Ajoute +1000ms/check. Pour inline : Galileo Luna-2 (3B/8B) = sub-200ms, 10-20 métriques simultanées.

## Testing agents

### Pyramide de tests
1. **Unit** (base) : tool functions, prompt templates, output parsers, memory
2. **Integration** : agent+tools, agent+memory, multi-agent
3. **Behavioral** : scenarios, adversarial, regression, safety
4. **E2E** (top) : full conversations, prod simulations, load

**Eval-driven development** = TDD pour agents : définir évaluations AVANT de build.

### Mocking
Mock la couche LLM via dependency injection. AWS ToolSimulator : intercepte tool calls → LLM-based response generator (pas de fixtures manuelles).

### CI/CD
DeepEval + pytest : 90% pass-rate threshold bloque les merges. Golden datasets avec trajectoires complètes (pas juste Q&A).

## Deploy production

### Managed platforms
| Plateforme | Force |
|-----------|-------|
| Claude Managed Agents | Zero-infra, sandbox intégré, Dreaming |
| AWS Bedrock AgentCore | Serverless, isolation session, 8h workloads |
| Azure AI Foundry | GPU VMs + AKS, M365/Teams |
| Vertex AI Agent Builder | ADK + eval framework intégré |

### Scaling
Kubernetes pod autoscaling. Queue-based (SQS, Pub/Sub). Rate limiting per-tenant token bucket. Tail-based sampling : garder toutes traces avec erreurs, sampler le reste à 5-10%.

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-frameworks]] — Frameworks comparés
- [[agents-securite]] — Sécurité et guardrails
- [[rag-evaluation]] — Évaluation RAG (RAGAS)
