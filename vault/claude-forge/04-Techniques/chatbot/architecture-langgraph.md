---
titre: "Architecture LangGraph — Chatbot & multi-agent"
resume: "Guide implementation chatbot avec LangGraph : StateGraph, supervisor, swarm, checkpointing, HITL, memory multi-session, couts"
aliases:
  - architecture langgraph
  - langgraph chatbot
  - langgraph multi-agent
  - stategraph chatbot
  - langgraph supervisor
  - langgraph swarm
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://langchain-ai.github.io/langgraph/"
  - "https://github.com/langchain-ai/langgraph-supervisor-py"
  - "https://github.com/langchain-ai/langgraph-swarm-py"
  - "https://www.langchain.com/pricing-langgraph-platform"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/langgraph"
---

## Definition

Framework open-source (MIT) pour orchestrer des agents via des graphes diriges avec etat type. Seul framework grand-public avec **checkpointing natif, time-travel debugging et HITL integre (`interrupt`)**. Adoption enterprise forte (Klarna, LinkedIn, Uber, JP Morgan documentes). Philosophie : model-agnostic, controle fin via graphe, persistence first-class.

## Architecture

```
┌──────────────────────────────────────────────┐
│               StateGraph                      │
│                                               │
│  State (TypedDict/Pydantic)                   │
│    ├── messages: list[Message]                │
│    ├── context: str                           │
│    └── retry_count: int                       │
│                                               │
│  Nodes (fonctions Python)                     │
│    ├── agent (appel LLM)                      │
│    └── tools (execution outils)               │
│                                               │
│  Edges                                        │
│    ├── Fixes : A → B                          │
│    └── Conditionnels : f(state) → node        │
│                                               │
│  Reducers (merge state concurrent)            │
│    └── add_messages (append, pas overwrite)    │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           Supervisor (multi-agent)            │
│  User → Supervisor → [Math | Research | FAQ]  │
│       ← Supervisor ← resultat                │
│  Routage LLM-based + audit trail centralise   │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           Swarm (multi-agent)                 │
│  Alice ──handoff──→ Bob ──handoff──→ Alice    │
│  Pas de superviseur central                   │
│  Risque ping-pong (limiter recursion_limit)   │
└──────────────────────────────────────────────┘
```

## Code pattern

### Chatbot basique (ReAct)

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import AsyncPostgresSaver

agent = create_react_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[lookup_order, create_ticket, search_faq],
    prompt="Tu es un assistant service client ACME.",
)
app = agent  # deja compile

config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = await app.ainvoke({"messages": [("user", query)]}, config)
```

### Supervisor (multi-specialistes)

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

billing = create_react_agent(model, tools=[lookup_invoice], name="billing")
tech = create_react_agent(model, tools=[run_diagnostic], name="tech")
faq = create_react_agent(model, tools=[search_kb], name="faq")

workflow = create_supervisor(
    [billing, tech, faq],
    model=model,
    prompt="Route vers le specialiste adapte.",
    output_mode="last_message",
)
app = workflow.compile(checkpointer=AsyncPostgresSaver(conn))
```

### Swarm (handoffs decentralises)

```python
from langgraph_swarm import create_swarm, create_handoff_tool

billing = create_react_agent(model, name="Billing", tools=[
    lookup_invoice,
    create_handoff_tool(agent_name="Tech", description="Probleme technique"),
])
tech = create_react_agent(model, name="Tech", tools=[
    run_diagnostic,
    create_handoff_tool(agent_name="Billing", description="Question facturation"),
])

app = create_swarm([billing, tech], default_active_agent="Billing")
    .compile(checkpointer=AsyncPostgresSaver(conn))
```

### Hierarchique

```python
research_team = create_supervisor(
    [search_agent, analysis_agent], model=model,
).compile(name="research_team")

writing_team = create_supervisor(
    [draft_agent, editor_agent], model=model,
).compile(name="writing_team")

top = create_supervisor(
    [research_team, writing_team], model=model,
).compile()
```

### HITL (Human-in-the-Loop)

```python
from langgraph.types import interrupt, Command

def sensitive_action(state):
    approval = interrupt("Approuver le remboursement de 450€ ?")
    if approval == "approve":
        execute_refund(state)
    else:
        return {"messages": ["Remboursement refuse par l'operateur."]}

app.invoke(Command(resume="approve"), config)
```

**Attention** : au resume, le noeud re-execute depuis le debut. Idempotence obligatoire.

## Specificites chatbot

### Memoire multi-turn
**Checkpointing natif** — chaque step sauvegarde un snapshot de l'etat. Thread ID = 1 conversation.

| Backend | Usage |
|---------|-------|
| InMemorySaver | Dev uniquement |
| AsyncPostgresSaver | **Production standard** |
| Redis | Haut debit |
| MongoDB Store | Memoire cross-session (long-terme) |

### Streaming
Streaming natif via `.astream()` ou `.astream_events()`. Chaque noeud du graphe peut streamer independamment.

### Time-travel debugging
Revenir a n'importe quel checkpoint et re-executer. Invaluable pour debugger des conversations multi-turn complexes.

## Couts et quand utiliser

| Composant | Cout |
|-----------|------|
| LangGraph (framework) | **Gratuit** (MIT) |
| LLM provider | Par token (Anthropic, OpenAI, etc.) |
| LangSmith Plus | $39/seat/mois |
| LangSmith Deployment | Voir [pricing officiel](https://www.langchain.com/pricing-langgraph-platform) — modele migre vers per-deployment-run (mai 2026) |

### Quand utiliser LangGraph
- Workflows complexes avec branching, cycles, retries
- HITL obligatoire (finance, sante, legal)
- Multi-agent avec audit trail (checkpointing)
- Besoin de time-travel debugging
- Equipe deja sur l'ecosysteme LangChain

### Quand eviter
- Chatbot simple single-agent (raw SDK plus simple et maintenable)
- Equipe qui valorise la simplicite (learning curve graphe)
- Budget serre (LangSmith ajoute des couts)
- Tendance "LangChain exit" : equipes prod migrent parfois vers raw SDK pour reduire code et latence (chiffres precis a mesurer cas par cas)

### Metriques production

> ⚠️ Les chiffres precis Supervisor vs Swarm ("94%/91% routing accuracy, 4.2s/2.8s latence, 2800/1900 tokens, overhead 14ms/op") qui figuraient dans les versions anterieures de cette note **n'ont pas de source primaire identifiable** (audit 23 mai 2026). Garder l'idee qualitative : Supervisor offre meilleur audit trail + meilleure tolerance aux domaines ambigus, Swarm reduit la latence et les tokens via moins de hops centraux. Pour chiffrer ton cas : mesurer empiriquement.

## Liens

- [[MOC-Techniques]]
- [[agents-architecture]] — Patterns abstraits
- [[agents-frameworks]] — Comparatif frameworks (LangGraph = Tier 1)
- [[architecture-claude-api]] — Equivalent Claude
- [[architecture-openai-api]] — Equivalent OpenAI
- [[pattern-orchestrateur]] — Supervisor detaille
- [[pattern-swarm]] — Swarm/handoffs detaille
- [[Harrison Chase]] — Createur LangGraph, Deep Agents
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source des retraits
