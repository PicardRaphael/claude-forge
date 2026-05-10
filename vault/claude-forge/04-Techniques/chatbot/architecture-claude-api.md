---
titre: "Architecture Claude API — Chatbot & multi-agent"
resume: "Guide implémentation chatbot avec Claude API : Messages API, tool_use, Agent SDK, Managed Agents, system prompts, prompt caching, coûts"
aliases:
  - architecture claude api
  - claude api chatbot
  - anthropic sdk chatbot
  - claude tool use
  - managed agents architecture
  - claude agent sdk
domaine: ia
type: technique
derniere-maj: 2026-05-10
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

API Anthropic pour construire des chatbots et agents conversationnels. Trois niveaux d'abstraction : Messages API (controle total), Agent SDK (loop geree), Managed Agents (infrastructure hebergee). Philosophie : MCP-first pour les outils, gestion d'etat cote client, extended thinking integre.

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
│  Max 20 agents, 25 threads concurrents       │
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

### Agent SDK (loop geree)

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
Le system prompt est cache automatiquement (10% du cout apres le 1er appel). Placer la persona et les regles dans le system prompt, pas dans les messages user.

### Clarification et fallback
Instruire Claude a poser des questions de clarification plutot que deviner. Pattern : `tool_choice: "auto"` + tool `ask_clarification` dans la liste d'outils.

## Couts et quand utiliser

| Modele | Input $/MTok | Output $/MTok | Usage chatbot |
|--------|-------------|--------------|---------------|
| Haiku 4.5 | $1 | $5 | Triage, classification, FAQ simple |
| Sonnet 4.6 | $3 | $15 | Production standard, support client |
| Opus 4.7 | $5 | $25 | Cas complexes, orchestration multi-agent |

### Optimisations
- **Prompt caching** : 90% de reduction sur cache hit (system prompt + tools statiques)
- **Batch API** : 50% de reduction, traitement asynchrone (< 1h en general)
- **Triage Haiku→Sonnet→Opus** : classifier la complexite, router vers le modele adapte
- **Managed Agents** : $0.08/h session + tokens. Rentable pour taches longues (> 5 min)

### Quand utiliser Claude API
- Support client avec outils internes (CRM, ticketing)
- Chatbot document-heavy (1M tokens de contexte natif)
- Agent coding / technique (Claude Code domine)
- Compliance-sensitive (Constitutional AI, safety integree)

### Quand eviter
- Besoin de voice/realtime natif (pas d'API voix Claude)
- Ecosysteme existant full OpenAI/Azure
- Budget ultra-serre sur du volume (Haiku reste plus cher que GPT-4.1 Nano)

## Fonctionnalites avancees (beta mai 2026)

- **Tool Search** : Claude decouvre les outils a la demande (`defer_loading: true`). -85% tokens sur les definitions d'outils.
- **Programmatic Tool Calling** : Claude orchestre plusieurs tools via code Python sandbox. -37% tokens moyen.
- **Dreaming** (Managed Agents) : l'agent review ses sessions passees et s'auto-ameliore.

## Liens

- [[agents-architecture]] — Patterns abstraits (ReAct, Supervisor, Swarm)
- [[agents-frameworks]] — Comparatif tous frameworks
- [[architecture-openai-api]] — Equivalent OpenAI
- [[architecture-langgraph]] — Equivalent LangGraph
- [[pattern-orchestrateur]] — Pattern orchestrateur detaille
- [[pattern-single-agent-multi-tool]] — Pattern agent unique + outils
