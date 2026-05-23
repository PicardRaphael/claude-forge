---
titre: "Pattern Swarm — Handoffs decentralises"
resume: "Pattern multi-agent peer-to-peer : agents autonomes se transferent le controle directement via handoffs, sans superviseur central. Code LangGraph, OpenAI"
aliases:
  - pattern swarm
  - swarm pattern
  - handoff pattern
  - pattern handoffs
  - decentralized agents
  - agent transfer
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://github.com/langchain-ai/langgraph-swarm-py"
  - "https://github.com/openai/swarm"
  - "https://openai.github.io/openai-agents-python/multi_agent/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/patterns"
---

## Definition

Architecture peer-to-peer ou les agents se transferent le controle directement via des **handoffs** (fonctions/outils). Pas de superviseur central. Un seul agent est actif a la fois. Quand un agent detecte qu'une requete sort de son domaine, il appelle un outil `transfer_to_X` qui passe le controle.

Difference cle avec le [[pattern-orchestrateur]] : pas de point de passage central. Les agents communiquent directement entre eux.

## Architecture

```
┌─────────────────────────────────────────────┐
│              Swarm / Handoffs                │
│                                              │
│  User ──→ Agent A (actif)                    │
│              │                               │
│              ├── "pas mon domaine"            │
│              └── transfer_to_B()             │
│                    │                         │
│                    ▼                         │
│                Agent B (actif)               │
│                    │                         │
│                    ├── resolu → User          │
│                    └── transfer_to_C()       │
│                         │                    │
│                         ▼                    │
│                     Agent C (actif) → User   │
│                                              │
│  Historique complet passe a chaque handoff   │
└─────────────────────────────────────────────┘
```

## Code pattern

### LangGraph Swarm

```python
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.prebuilt import create_react_agent

billing = create_react_agent(
    model, name="Billing",
    tools=[
        lookup_invoice,
        create_handoff_tool(
            agent_name="Tech",
            description="Transferer pour probleme technique",
        ),
    ],
)

tech = create_react_agent(
    model, name="Tech",
    tools=[
        run_diagnostic,
        create_handoff_tool(
            agent_name="Billing",
            description="Transferer pour question facturation",
        ),
    ],
)

app = create_swarm(
    [billing, tech],
    default_active_agent="Billing",
).compile(checkpointer=AsyncPostgresSaver(conn))

config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = await app.ainvoke({"messages": [("user", query)]}, config)
```

### OpenAI Agents SDK — Handoffs

```python
from agents import Agent

def transfer_to_tech():
    """Transferer au support technique."""
    return tech_agent

def transfer_to_billing():
    """Transferer a la facturation."""
    return billing_agent

billing_agent = Agent(
    name="Billing",
    instructions="Gere la facturation. Transfere au tech si probleme technique.",
    tools=[lookup_invoice, transfer_to_tech],
)

tech_agent = Agent(
    name="Tech",
    instructions="Resout les problemes techniques. Transfere a billing si question facture.",
    tools=[run_diagnostic, transfer_to_billing],
)

result = await Runner.run(billing_agent, "Mon paiement a echoue et l'app crashe")
```

### OpenAI — Triage Agent

```python
triage = Agent(
    name="Triage",
    instructions="Dirige vers le bon specialiste.",
    handoffs=[billing_agent, tech_agent, faq_agent],
)
```

## System prompt — Agent swarm

```
Tu es l'agent [Domaine] du support client [Entreprise].

# Ton domaine
- [Liste des sujets que tu geres]

# Quand transferer
- Si la question concerne [autre domaine] → transfer_to_[autre]
- Si tu ne peux pas resoudre apres 2 tentatives → transfer_to_escalation

# Regles
- Ne reponds JAMAIS a une question hors de ton domaine
- Transfere IMMEDIATEMENT si tu detectes un autre domaine
- Inclus un resume de ce que tu as deja tente dans le message de transfert
```

## Failure modes et solutions

### 1. Ping-pong loops
Agent A transfere a B qui transfere a A. Solution : tracker le nombre de handoffs, hard limit. En LangGraph : `recursion_limit` dans la config.

### 2. Perte de contexte
Agent B ne sait pas ce que Agent A a deja fait. Solution : `create_handoff_tool` passe l'historique complet par defaut. Ajouter un resume explicite dans le `Command.update` si l'historique est long.

### 3. Mauvais routing
L'agent route mal sans superviseur pour corriger. Solution : system prompts tres precis sur les domaines. Ajouter un agent "fallback" qui re-route.

### 4. Conversation history bloat
Chaque handoff passe TOUT l'historique, tokens explosent. Solution : compacter l'historique avant handoff. Passer un resume + les 3 derniers messages.

## Specificites chatbot

### Memoire et continuity
Le systeme track quel agent etait actif en dernier. Sur un nouveau message du meme thread, l'agent precedent reprend automatiquement (pas de re-triage).

### Experience utilisateur
Le handoff est transparent pour l'utilisateur — il ne voit qu'un seul chatbot. Le changement d'agent est invisible sauf si on l'annonce.

### Latence vs Orchestrateur
Swarm reduit les hops centraux (pas d'appel intermediaire au supervisor) → moins de tokens et moins de latence. Compromis : routing moins fiable sur domaines ambigus.

> ⚠️ Les chiffres precis "-30% tokens, latence 2.8s/5.4s, accuracy 91%" qui figuraient avant **n'ont pas de source primaire** (audit 23 mai). Tendance qualitative confirmee multi-sources, chiffres a mesurer empiriquement.

## Quand utiliser
- **Latence critique** (chatbot temps-reel, voice)
- **Domaines bien definis** avec peu de chevauchement
- **Volume eleve** ou l'economie de tokens compte
- **Requetes multi-domaines frequentes** (le swarm les gere sans retour au centre)

## Quand eviter
- Domaines ambigus (le swarm route moins bien que le supervisor)
- Audit trail centralise necessaire
- Phase de deploiement initial (commencer par orchestrateur, migrer vers swarm une fois les domaines stabilises)

## Heritage Swarm → Agents SDK

OpenAI Swarm (oct 2024) etait un framework experimental/educatif, explicitement "pas pour production". L'Agents SDK (mars 2025) a repris les primitives (Agent + Handoff) en ajoutant : guardrails, tracing, structured outputs, MCP, sessions.

## Liens

- [[MOC-Techniques]]
- [[agents-architecture]] — Pattern Swarm (theorie)
- [[pattern-orchestrateur]] — Alternative centralisee
- [[pattern-pipeline]] — Alternative sequentielle
- [[architecture-langgraph]] — Implementation LangGraph
- [[architecture-openai-api]] — Implementation OpenAI (Agents SDK)
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source
