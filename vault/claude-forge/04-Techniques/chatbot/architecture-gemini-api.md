---
titre: "Architecture Gemini API & ADK — Chatbot & multi-agent"
resume: "Guide implementation chatbot avec Gemini API, Google ADK, A2A protocol, Interactions API. Le moins cher en tokens, unique pour l'interop cross-framework"
aliases:
  - architecture gemini api
  - gemini chatbot
  - google adk
  - agent development kit
  - gemini function calling
  - a2a protocol chatbot
  - interactions api
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://ai.google.dev/gemini-api/docs/function-calling"
  - "https://adk.dev/"
  - "https://a2a-protocol.org/"
  - "https://ai.google.dev/gemini-api/docs/interactions"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/google"
---

## Definition

Ecosysteme Google pour chatbots et agents. Trois couches : Gemini API (function calling + Interactions API), ADK v1.0 GA (orchestration multi-agent), A2A protocol (communication inter-agents cross-framework, **v1.0 publiee 12 mars 2026**). Avantages : tokens les moins chers du marche (Flash-Lite a $0.10/MTok input) et interoperabilite cross-framework via A2A.

## Architecture

```
┌──────────── Gemini API (single agent) ───────────┐
│  Function calling : declare → call → execute →    │
│  return result → response                         │
│  Modes : AUTO, ANY, VALIDATED, NONE               │
│  Parallel + Compositional calling                 │
│  Interactions API : server-side state (beta)      │
└───────────────────────────────────────────────────┘

┌──────────── ADK (multi-agent) ───────────────────┐
│  LlmAgent (Gemini + reasoning)                    │
│  Workflow Agents (pas de LLM) :                   │
│    ├── SequentialAgent (pipeline)                  │
│    ├── ParallelAgent (fan-out)                     │
│    └── LoopAgent (iteration)                      │
│  State sharing via output_key                     │
│  Event Compaction : -38% tokens, -18% latence     │
└───────────────────────────────────────────────────┘

┌──────────── A2A Protocol v1.0 ───────────────────┐
│  Agent Cards (JSON) → discovery                   │
│  Tasks : submitted → working → completed          │
│  HTTP/SSE + gRPC binding                          │
│  Cross-framework : ADK ↔ LangGraph ↔ CrewAI      │
└───────────────────────────────────────────────────┘
```

## Code pattern

### Gemini function calling (chatbot basique)

```python
from google import genai
from google.genai import types

def lookup_order(order_id: str) -> dict:
    """Cherche le statut d'une commande."""
    return db.get_order(order_id)

client = genai.Client(api_key="...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Ou est ma commande #12345 ?",
    config=types.GenerateContentConfig(
        tools=[lookup_order],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        ),
    ),
)
```

### ADK multi-agent (coordinator)

```python
from google.adk.agents import LlmAgent, SequentialAgent

billing = LlmAgent(
    name="billing", model="gemini-2.5-flash",
    description="Gere les questions de facturation",
    instruction="Reponds aux questions de facturation.",
    tools=[lookup_invoice],
)

tech = LlmAgent(
    name="tech", model="gemini-2.5-flash",
    description="Resout les problemes techniques",
    instruction="Diagnostique et resous les problemes techniques.",
    tools=[run_diagnostic],
)

coordinator = LlmAgent(
    name="coordinator", model="gemini-2.5-pro",
    description="Route vers le bon specialiste",
    instruction="Analyse la demande et delegue au bon agent.",
    sub_agents=[billing, tech],
)
```

### Interactions API (beta — server-side state)

```python
interaction = client.interactions.create(
    model="gemini-2.5-flash",
    input="Bonjour", store=True,
)
interaction2 = client.interactions.create(
    model="gemini-2.5-flash",
    input="Ou est ma commande ?",
    previous_interaction_id=interaction.id,
)
```

## Specificites chatbot

### Avantage cout
Flash-Lite a $0.10/$0.40 par MTok = ordre de grandeur **~25x moins cher** qu'un agent GPT-4o ou Sonnet. Un systeme 4 agents en Flash-Lite peut couter moins qu'un single agent Sonnet.

### A2A pour interop
Unique a Google. Permet a un agent ADK de communiquer avec un agent LangGraph ou CrewAI via Agent Cards et Tasks. **v1.0 publiee 12 mars 2026**, adoption en croissance.

### Limites chatbot
- Gemini API pas d'equivalent direct a Claude Managed Agents (infrastructure hebergee)
- Interactions API en beta
- Multi-langue (Python, Go, Java, TS) = avantage mais ecosysteme communautaire plus petit que LangGraph

### Event Compaction (ADK 1.0)
Fenetre glissante d'evenements recents + resume des anciens. **-38% tokens, -18% latence** (docs ADK). Crucial pour chatbots longues conversations.

## Couts et quand utiliser

| Modele | Input $/MTok | Output $/MTok | Usage chatbot |
|--------|-------------|--------------|---------------|
| Flash-Lite 2.5 | **$0.10** | $0.40 | Budget extreme, classification, FAQ |
| Flash 2.5 | $0.30 | $2.50 | Production standard, meilleur value |
| Pro 3.1 (preview) | $2.00-4.00 | $12.00-18.00 | Reasoning complexe, frontier |

- **Batch API** : 50% reduction
- **Context caching** : $0.01-0.40/MTok + $1/MTok/h stockage
- **Google Search grounding** : pricing depend de la version Gemini. **Gemini 3.x** : 5000 free/mois, $14/1000 ensuite. **Gemini 2.5** : 500-1500 RPD free, $35/1000 ensuite. Verifier [ai.google.dev/pricing](https://ai.google.dev/pricing) selon ta version.

### Quand utiliser Gemini/ADK
- Budget tokens critique (Flash-Lite imbattable)
- Equipe Google Cloud native (Vertex AI Agent Engine)
- Besoin d'interop cross-framework (A2A unique)
- Equipe multi-langage (Go, Java, TS en plus de Python)

### Quand eviter
- Ecosysteme existant AWS/Azure
- Besoin de checkpointing avance (LangGraph meilleur)
- Besoin de voice/realtime (OpenAI meilleur)
- Features agents matures (Claude Managed Agents plus complet)

## Liens

- [[MOC-Techniques]]
- [[agents-frameworks]] — Google ADK = Tier 3, platform-specific
- [[architecture-claude-api]] — Concurrent Anthropic
- [[architecture-openai-api]] — Concurrent OpenAI
- [[pattern-orchestrateur]] — ADK coordinator = pattern orchestrateur
- [[pattern-pipeline]] — ADK SequentialAgent = pattern pipeline
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
