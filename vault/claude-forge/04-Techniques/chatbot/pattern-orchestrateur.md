---
titre: "Pattern Orchestrateur — Supervisor & hierarchique"
resume: "Pattern multi-agent avec coordinateur central : 1 supervisor route vers N specialistes. Variante hierarchique avec sub-supervisors. Code LangGraph, OpenAI, Claude API"
aliases:
  - pattern orchestrateur
  - supervisor pattern
  - orchestrator pattern
  - pattern superviseur
  - pattern hierarchique
  - hierarchical agents
  - multi-agent supervisor
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://github.com/langchain-ai/langgraph-supervisor-py"
  - "https://openai.github.io/openai-agents-python/multi_agent/"
  - "https://platform.claude.com/docs/en/managed-agents/multi-agent"
  - "https://www.anthropic.com/research/building-effective-agents"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/patterns"
---

## Definition

**Orchestrateur** (1 niveau) : un supervisor central recoit chaque message, classifie l'intention, et route vers le specialiste adapte. Apres reponse du specialiste, le controle revient au supervisor.

**Hierarchique** (≥2 niveaux) : le supervisor delegue a des sub-supervisors qui gerent leurs propres equipes. Equipes de equipes.

Difference cle avec le [[pattern-swarm]] : le supervisor est un point de passage OBLIGATOIRE. Aucun specialiste ne communique directement avec un autre.

## Architecture

```
┌─────────────── Orchestrateur (1 niveau) ───────────────┐
│                                                         │
│  User ──→ Supervisor ──┬──→ Billing Agent ──→ Supervisor│
│                        ├──→ Tech Agent    ──→ Supervisor│
│                        └──→ FAQ Agent     ──→ Supervisor│
│                                              ──→ User   │
└─────────────────────────────────────────────────────────┘

┌─────────────── Hierarchique (2+ niveaux) ──────────────┐
│                                                         │
│  User ──→ Top Supervisor                                │
│              ├──→ Support Team (sub-supervisor)          │
│              │      ├──→ Billing Agent                  │
│              │      └──→ Refund Agent                   │
│              └──→ Tech Team (sub-supervisor)             │
│                     ├──→ Diagnostic Agent               │
│                     └──→ Escalation Agent               │
└─────────────────────────────────────────────────────────┘
```

## Code pattern

### LangGraph — Supervisor

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

billing = create_react_agent(model, tools=[lookup_invoice], name="billing")
tech = create_react_agent(model, tools=[run_diagnostic], name="tech")

supervisor = create_supervisor(
    [billing, tech],
    model=model,
    prompt="Route vers le specialiste adapte. Ne reponds jamais directement.",
    output_mode="last_message",  # ou "full_history"
)
app = supervisor.compile(checkpointer=checkpointer)
```

### LangGraph — Hierarchique

```python
support_team = create_supervisor(
    [billing_agent, refund_agent], model=model,
).compile(name="support_team")

tech_team = create_supervisor(
    [diagnostic_agent, escalation_agent], model=model,
).compile(name="tech_team")

top = create_supervisor(
    [support_team, tech_team], model=model,
    prompt="Coordonne les equipes support et technique.",
).compile()
```

### OpenAI — Agents-as-Tools (manager garde controle)

```python
from agents import Agent

manager = Agent(
    name="Manager",
    instructions="Coordonne les reponses. Synthetise avant de repondre.",
    tools=[
        billing_agent.as_tool(tool_name="billing", tool_description="Facturation"),
        tech_agent.as_tool(tool_name="tech", tool_description="Support technique"),
    ],
)
```

### Claude — Managed Agents Coordinator

```python
coordinator = client.beta.agents.create(
    name="Coordinator", model="claude-opus-4-7",
    system="Delegue au bon specialiste.",
    multiagent={"type": "coordinator", "agents": [
        {"type": "agent", "id": billing.id},
        {"type": "agent", "id": tech.id},
    ]},
)
```

## System prompt chatbot — Supervisor

```
Tu es le superviseur du support client [Entreprise].

# Routing
- "commande", "facture", "paiement" → billing
- "bug", "erreur", "ne marche pas" → tech
- Questions generales → faq

# Regles
- TOUJOURS router, ne JAMAIS repondre directement
- Si ambigu, demander une clarification (1 question max)
- Si 2+ domaines, commencer par le plus urgent
- Apres reponse du specialiste, verifier la satisfaction client
```

## Specificites chatbot

### Quand l'orchestrateur est meilleur que le swarm
- Domaines **ambigus** (le routing LLM corrige les erreurs de classification)
- **Audit trail** necessaire (tout passe par le supervisor = point de log centralise)
- **Qualite de routing** prioritaire sur la latence (94% vs 91% pour swarm)
- Phase de **deploiement initial** (commencer par orchestrateur, migrer vers swarm si les domaines se stabilisent)

### Couts multi-agent
Chaque routing = 1 appel LLM supplementaire. Le supervisor consomme ~2,800 tokens/requete vs ~1,900 pour swarm.

**Optimisation** : utiliser un modele leger pour le supervisor (Haiku/GPT-4.1-mini) et des modeles plus puissants pour les specialistes.

### Hierarchique : quand justifie ?
- 6+ agents specialistes (trop pour un seul supervisor)
- Domaines avec sous-domaines naturels (support → billing + refund)
- Equipes qui developpent et testent les sub-graphes independamment

**Attention** : chaque niveau ajoute de la latence (hop supplementaire). 2 niveaux = acceptable. 3+ = rarement justifie.

## Couts et quand utiliser

| Facteur | Orchestrateur | Hierarchique |
|---------|---------------|--------------|
| Latence | ~4.2s (single) | +50-100% par niveau |
| Tokens | ~2,800/req | x1.5-2 |
| Routing accuracy | 94% | ~94% par niveau |
| Complexite debug | Moyenne | Haute |
| Scalabilite agents | 2-5 | 6-20+ |

### Quand utiliser
- Support client multi-domaine (le cas d'usage canonique)
- Workflows avec validation centralisee (compliance, moderation)
- Chatbot enterprise avec audit trail

### Quand eviter
- 1-2 domaines seulement → [[pattern-single-agent-multi-tool]]
- Latence critique → [[pattern-swarm]]
- Pipeline deterministe → [[pattern-pipeline]]

## Liens

- [[MOC-Techniques]]
- [[agents-architecture]] — Pattern Supervisor (theorie)
- [[pattern-swarm]] — Alternative decentralisee
- [[pattern-pipeline]] — Alternative sequentielle
- [[architecture-langgraph]] — Implementation LangGraph
- [[architecture-openai-api]] — Implementation OpenAI
- [[architecture-claude-api]] — Implementation Claude
