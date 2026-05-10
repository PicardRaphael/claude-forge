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
derniere-maj: 2026-05-10
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

Framework open-source (MIT) pour orchestrer des agents via des graphes diriges avec etat type. Seul framework avec checkpointing natif, time-travel debugging, et HITL integre. Leader enterprise (34% des citations, Uber, LinkedIn, JP Morgan). Philosophie : model-agnostic, controle fin via graphe, persistence first-class.

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
│  Routing accuracy : 94%                       │
│  Extra LLM call par routing step              │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           Swarm (multi-agent)                 │
│  Alice ──handoff──→ Bob ──handoff──→ Alice    │
│  Pas de superviseur central                   │
│  -30% tokens, +latence reduite               │
│  Risque ping-pong (limiter a 3 hops)          │
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

# Invocation avec thread (memoire multi-turn)
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

### Hierarchique (equipes imbriquees)

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

# Cote appelant : reprendre apres approbation
app.invoke(Command(resume="approve"), config)
```

**Attention** : au resume, le noeud re-execute depuis le debut. Idempotence obligatoire.

## System prompt chatbot

```
Tu es un superviseur de support client. Tu routes les demandes :
- Questions facturation → agent "billing"
- Problemes techniques → agent "tech"  
- Questions generales → agent "faq"

Regles :
- Toujours router, ne jamais repondre directement
- Si la demande est ambigue, demander une clarification
- Si 2+ domaines concernes, commencer par le plus urgent
```

Pour les agents specialistes, chaque agent a son propre system prompt avec les regles de son domaine.

## Specificites chatbot

### Memoire multi-turn
**Checkpointing natif** — chaque step sauvegarde un snapshot de l'etat. Thread ID = 1 conversation.

| Backend | Usage |
|---------|-------|
| InMemorySaver | Dev uniquement |
| AsyncPostgresSaver | **Production standard** |
| Redis | Haut debit |
| MongoDB Store | Memoire cross-session (long-terme) |

### Memoire cross-session (long-terme)
```python
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()
app = graph.compile(checkpointer=checkpointer, store=store)
```
Le `Store` persiste des donnees entre threads (preferences utilisateur, historique).

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
| LangSmith Deployment (dev) | $0.0007/min |
| LangSmith Deployment (prod) | $0.0036/min |
| Node executions | $0.001/node (au-dela du free tier) |

**Overhead framework** : ~14ms/operation (negligeable vs latence LLM). OpenAI Agents SDK : ~2-5ms.

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
- Le trend "LangChain exit" : equipes prod migrent vers raw SDK pour -40-60% code, -8-22% latence

### Metriques production

| Metrique | Supervisor | Swarm |
|----------|-----------|-------|
| Latence single-domain | ~4.2s | ~2.8s |
| Latence multi-domain | ~9.1s | ~5.4s |
| Routing accuracy | **94%** | 91% |
| Tokens moyens/requete | ~2,800 | ~1,900 |

## Liens

- [[agents-architecture]] — Patterns abstraits
- [[agents-frameworks]] — Comparatif frameworks (LangGraph = Tier 1)
- [[architecture-claude-api]] — Equivalent Claude
- [[architecture-openai-api]] — Equivalent OpenAI
- [[pattern-orchestrateur]] — Supervisor detaille
- [[pattern-swarm]] — Swarm/handoffs detaille
- [[Harrison Chase]] — Createur LangGraph, Deep Agents
