---
titre: "Architecture Claude API — Chatbot & multi-agent"
resume: "Guide implementation chatbot avec Claude API : Messages API, tool_use, Agent SDK, Managed Agents, system prompts, prompt caching, couts"
aliases:
  - architecture claude api
  - claude api chatbot
  - anthropic sdk chatbot
  - claude tool use
  - managed agents architecture
  - claude agent sdk
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview"
  - "https://platform.claude.com/docs/en/managed-agents/overview"
  - "https://code.claude.com/docs/en/agent-sdk/overview"
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/anthropic"
---

## Definition

API Anthropic pour construire des chatbots et agents conversationnels. Trois niveaux d'abstraction : Messages API (controle total), Agent SDK (loop geree, **"runs inside your own process"** verbatim docs), Managed Agents (infrastructure hebergee, Research Preview). Philosophie : MCP-first pour les outils, gestion d'etat cote client, extended thinking integre.

## Architecture

```
┌─────────────────────────────────────────────┐
│              Messages API                    │
│  User → System Prompt + Tools → Claude       │
│       ↓                                      │
│  stop_reason == "tool_use" ?                 │
│       ├─ Oui → Executer tool → tool_result   │
│       │        → Reboucler                   │
│       └─ Non → Reponse finale               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│           Managed Agents (production)        │
│  Coordinator ──┬── Specialist A (thread)     │
│                ├── Specialist B (thread)     │
│                └── Specialist C (thread)     │
│  Filesystem partage, contexte isole          │
└─────────────────────────────────────────────┘
```

## Code pattern

### Boucle agentique de base (Messages API)

```python
from anthropic import Anthropic

client = Anthropic()
tools = [{"name": "lookup_order", "description": "...", "input_schema": {...}}]

messages = [{"role": "user", "content": query}]
response = client.messages.create(
    model="claude-sonnet-4-6",
    system="Tu es un assistant service client ACME...",
    tools=tools, max_tokens=1024, messages=messages,
)

while response.stop_reason == "tool_use":
    tool_results = execute_tools(response.content)
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
    response = client.messages.create(
        model="claude-sonnet-4-6", system=system,
        tools=tools, max_tokens=1024, messages=messages,
    )
```

### Agent SDK

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Aide le client avec sa commande",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Agent"],
        agents={"support": AgentDefinition(
            description="Specialiste support client",
            tools=["Read", "Bash"],
        )},
    ),
):
    print(message)
```

### Managed Agents (multi-agent heberge)

```python
coordinator = client.beta.agents.create(
    name="Lead Support", model="claude-opus-4-7",
    system="Coordonne le support. Delegue facturation et technique.",
    tools=[{"type": "agent_toolset_20260401"}],
    multiagent={"type": "coordinator", "agents": [
        {"type": "agent", "id": billing_agent.id},
        {"type": "agent", "id": tech_agent.id},
    ]},
)
session = client.beta.sessions.create(
    agent=coordinator.id, environment_id=env.id,
)
```

## System prompt chatbot

```xml
<role>
Tu es l'assistant virtuel de [Entreprise]. Ton nom est [Nom].
Ton role : aider les clients avec leurs commandes, questions produit,
et problemes techniques.
</role>

<persona>
- Ton professionnel mais chaleureux
- Reponses concises (2-3 phrases max sauf explication technique)
- Toujours proposer une action concrete
</persona>

<outils>
Utilise lookup_order AVANT de repondre sur un statut de commande.
Utilise create_ticket pour tout probleme necessitant un suivi.
Ne devine JAMAIS une information verifiable par outil.
</outils>

<regles_conversation>
- Si le client est frustre, reconnaitre le probleme avant de proposer
- Ne jamais promettre de delais specifiques
- Escalader vers un humain si : demande de remboursement > 500€,
  menace legale, 3+ echanges sans resolution
</regles_conversation>

<default_to_action>
Implemente les changements plutot que les suggerer. Si l'intention
est ambigue, infere l'action la plus utile et procede.
</default_to_action>
```

## Specificites chatbot

### Memoire multi-turn
Gestion cote client : le developpeur maintient `messages[]` et les renvoie a chaque appel. Pas de persistence server-side (contrairement a OpenAI Conversations API). Pattern recommande : stocker les messages en DB, charger les N derniers + un resume des precedents.

### Streaming
```python
with client.messages.stream(model=model, messages=msgs, system=sys) as stream:
    for text in stream.text_stream:
        yield text  # SSE vers le frontend
```

### Persona constante
Le system prompt est cache automatiquement (jusqu'a 90% de reduction sur cache hit). Placer la persona et les regles dans le system prompt, pas dans les messages user.

### Clarification et fallback
Instruire Claude a poser des questions de clarification plutot que deviner. Pattern : `tool_choice: "auto"` + tool `ask_clarification` dans la liste d'outils.

## Couts et quand utiliser

| Modele | Input $/MTok | Output $/MTok | Usage chatbot |
|--------|-------------|--------------|---------------|
| Haiku 4.5 | $1 | $5 | Triage, classification, FAQ simple |
| Sonnet 4.6 | $3 | $15 | Production standard, support client |
| Opus 4.7 | $5 | $25 | Cas complexes, orchestration multi-agent |

### Optimisations
- **Prompt caching** : jusqu'a 90% de reduction sur cache hit (system prompt + tools statiques)
- **Batch API** : 50% de reduction, traitement asynchrone
- **Caching + batching combine** : Anthropic verbatim "jusqu'a 95% reduction" vs standard
- **Triage Haiku→Sonnet→Opus** : classifier la complexite, router vers le modele adapte
- **Managed Agents** : tarif horaire + tokens (a confirmer pricing officiel ; rentable pour taches longues > 5 min)

### Quand utiliser Claude API
- Support client avec outils internes (CRM, ticketing)
- Chatbot document-heavy (1M tokens de contexte natif)
- Agent coding / technique (Claude Code domine)
- Compliance-sensitive (Constitutional AI, safety integree)

### Quand eviter
- Besoin de voice/realtime natif (pas d'API voix Claude)
- Ecosysteme existant full OpenAI/Azure

## Fonctionnalites avancees (mai 2026)

- **Tool Search** : Claude decouvre les outils a la demande (`defer_loading: true`). Reduction substantielle des tokens sur definitions d'outils (chiffre exact varie selon nombre d'outils).
- **Programmatic Tool Calling (PTC)** : Claude orchestre plusieurs tools via code Python sandbox. Reduction tokens moyenne documentee Anthropic.
- **Dreams** ([[technique-dreaming-cross-session]], Managed Agents Research Preview, beta header `dreaming-2026-04-21`) : l'agent reflechit sur les sessions passees pour curer sa memoire.

## Liens

- [[MOC-Techniques]]
- [[agents-architecture]] — Patterns abstraits (ReAct, Supervisor, Swarm)
- [[agents-frameworks]] — Comparatif tous frameworks
- [[architecture-openai-api]] — Equivalent OpenAI
- [[architecture-langgraph]] — Equivalent LangGraph
- [[pattern-orchestrateur]] — Pattern orchestrateur detaille
- [[pattern-single-agent-multi-tool]] — Pattern agent unique + outils
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
