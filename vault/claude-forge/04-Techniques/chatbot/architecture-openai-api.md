---
titre: "Architecture OpenAI API — Chatbot & multi-agent"
resume: "Guide implementation chatbot avec OpenAI : Responses API, Agents SDK, function calling, handoffs, Conversations API, couts"
aliases:
  - architecture openai api
  - openai chatbot
  - openai agents sdk
  - gpt chatbot
  - openai function calling
  - responses api
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://developers.openai.com/api/docs/guides/agents"
  - "https://openai.github.io/openai-agents-python/"
  - "https://developers.openai.com/api/docs/guides/function-calling"
  - "https://developers.openai.com/api/docs/guides/conversation-state"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/openai"
---

## Definition

Ecosysteme OpenAI pour chatbots et agents. Trois couches : Responses API (API primaire, remplace Chat Completions + Assistants), Agents SDK (orchestration multi-agent open-source), Conversations API (etat server-side). Philosophie : infrastructure hebergee, outils built-in, etat server-side.

## Architecture

```
┌──────────────────────────────────────────────┐
│               Responses API                   │
│  input → model + tools → output items         │
│  Outils heberges : web_search, file_search,   │
│  code_interpreter, image_generation, MCP       │
│  Etat : store:true + previous_response_id     │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│              Agents SDK                       │
│  Triage Agent                                 │
│    ├── handoff → Billing Agent (controle)     │
│    └── handoff → Tech Agent (controle)        │
│  Runner gere la boucle agentique              │
│  Guardrails en parallele (tripwire)           │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  Variante : Agents-as-Tools                   │
│  Manager Agent                                │
│    ├── tool_call → billing_expert             │
│    └── tool_call → tech_expert                │
│  Manager garde le controle et synthetise      │
└──────────────────────────────────────────────┘
```

## Code pattern

### Responses API (chatbot basique)

```python
from openai import OpenAI
client = OpenAI()

# Appel simple
response = client.responses.create(
    model="gpt-4.1",
    instructions="Tu es un assistant service client ACME.",
    input="Ou en est ma commande #12345 ?"
)

# Multi-turn avec etat server-side
res1 = client.responses.create(
    model="gpt-4.1", input="Bonjour", store=True
)
res2 = client.responses.create(
    model="gpt-4.1",
    input="Ou est ma commande ?",
    previous_response_id=res1.id, store=True,
)

# Avec Conversations API (persistance cross-session)
conv = client.conversations.create()
response = client.responses.create(
    model="gpt-4.1",
    input=[{"role": "user", "content": "Bonjour"}],
    conversation=conv.id,
)
```

### Agents SDK (multi-agent)

```python
from agents import Agent, Runner, function_tool

@function_tool
def lookup_order(order_id: str) -> str:
    """Recherche le statut d'une commande."""
    return db.get_order(order_id)

billing_agent = Agent(
    name="Facturation",
    instructions="Gere les questions de facturation.",
    tools=[lookup_order],
)
tech_agent = Agent(
    name="Support Tech",
    instructions="Resout les problemes techniques.",
    tools=[run_diagnostic],
)

# Pattern Handoff (transfert de controle)
triage = Agent(
    name="Triage",
    instructions="Dirige vers le bon specialiste.",
    handoffs=[billing_agent, tech_agent],
)
result = await Runner.run(triage, "J'ai un probleme de paiement")

# Pattern Agents-as-Tools (manager garde controle)
manager = Agent(
    name="Manager",
    instructions="Coordonne les reponses.",
    tools=[
        billing_agent.as_tool(
            tool_name="billing_expert",
            tool_description="Questions facturation",
        ),
        tech_agent.as_tool(
            tool_name="tech_expert",
            tool_description="Problemes techniques",
        ),
    ],
)
```

### Guardrails

```python
from agents import InputGuardrail, GuardrailFunctionOutput

async def check_harmful(ctx, agent, input):
    result = await Runner.run(
        Agent(instructions="Detecte contenu nocif", output_type=HarmCheck),
        input, context=ctx,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_harmful,
    )

safe_agent = Agent(
    name="Support",
    input_guardrails=[InputGuardrail(guardrail_function=check_harmful)],
)
```

## System prompt chatbot

```
# Role et Objectif
Tu es l'assistant service client ACME. Aide les clients avec
commandes, facturation, et problemes techniques.

# Instructions
## Comportement
- Reponses concises (2-3 phrases sauf explication technique)
- Utilise lookup_order AVANT de repondre sur un statut
- Ne devine jamais une information verifiable

## Escalade
- Remboursement > 500€ → transfert humain
- 3+ echanges sans resolution → transfert humain

# Format de sortie
- Salutation breve
- Information/action
- Question de suivi ou cloture

# Raisonnement (optionnel, +20% SWE-bench)
Planifie avant chaque appel d'outil. Reflechis aux resultats precedents.
```

**GPT-4.1** : tres literal, suivre les instructions exactement. **GPT-5** : plus oriente outcome, prompts plus courts suffisent. Parametre `verbosity` pour controler la longueur.

## Specificites chatbot

### Memoire multi-turn
**Server-side** (unique a OpenAI) : `previous_response_id` ou `Conversations API`. Pas besoin de renvoyer l'historique complet. Attention : tous les tokens precedents sont factures comme input a chaque appel.

### Streaming
```python
stream = client.responses.create(model="gpt-4.1", input=query, stream=True)
for event in stream:
    if event.type == "response.output_text.delta":
        yield event.delta
```

### Voice / Realtime
**Realtime API** (GA 2025) : audio bidirectionnel, detection d'interruption, TTS integre. Unique a OpenAI — ni Claude ni Gemini n'ont d'equivalent natif en API.

### Persona constante
Utiliser le parametre `instructions` (Responses API) plutot que system message. Il a priorite et est cache automatiquement.

## Couts et quand utiliser

| Modele | Tier | Usage chatbot |
|--------|------|---------------|
| GPT-4.1 Nano | Ultra-budget | Classification, extraction, FAQ |
| GPT-4.1 Mini | Budget | Qualite moderee, resumes |
| GPT-4.1 | Standard | Production, coding, agentique |
| o4-mini | Raisonnement eco | Math, planning, taches complexes |
| GPT-5 | Flagship | Meilleure qualite, long-context |

### Optimisations
- **Batch API** : 50% de reduction, traitement < 24h
- **Prompt caching** : automatique pour prefixes stables (50-90% reduction)
- **Model routing** : classifier avec Nano, router vers le modele adapte
- **Conversations API** : etat server-side evite de renvoyer tout l'historique

### Quand utiliser OpenAI
- Voice/Realtime chatbot (seul a avoir l'API native)
- Outils heberges (web_search, code_interpreter, file_search)
- Gestion d'etat server-side souhaitee
- Ecosysteme Azure existant

### Quand eviter
- Compliance-heavy (Claude plus avance sur la safety native)
- Long-context document processing (Claude 1M natif, GPT-4.1 1M aussi mais Claude plus precis)
- Budget serre + besoin de reasoning (tokens reasoning factures en output, invisibles)

## Migration Assistants → Responses

Assistants API deprecated 26 aout 2025, shutdown 26 aout 2026. Mapping :
- Assistants → Prompts (dashboard, versiones)
- Threads → Conversations
- Runs → Responses
- Run-Steps → Items

Pas de migration automatique des Threads.

## Liens

- [[MOC-Techniques]]
- [[agents-architecture]] — Patterns abstraits
- [[agents-frameworks]] — Comparatif tous frameworks
- [[architecture-claude-api]] — Equivalent Claude
- [[architecture-langgraph]] — Equivalent LangGraph
- [[pattern-orchestrateur]] — Orchestrateur detaille
- [[pattern-swarm]] — Swarm/handoffs detaille
