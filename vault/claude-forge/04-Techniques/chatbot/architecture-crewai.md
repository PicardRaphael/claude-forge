---
titre: "Architecture CrewAI — Chatbot & multi-agent"
resume: "Guide implementation chatbot avec CrewAI : Crews, Flows, memory unifiee, delegation, prototypage rapide. Quand utiliser vs LangGraph/raw SDK"
aliases:
  - architecture crewai
  - crewai chatbot
  - crewai multi-agent
  - crews architecture
  - crewai flows
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://docs.crewai.com/en/concepts/agents"
  - "https://docs.crewai.com/en/concepts/flows"
  - "https://docs.crewai.com/en/concepts/memory"
  - "https://crewai.com/open-source"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/crewai"
---

## Definition

Framework role-based pour multi-agent. 4 primitives : Agent (role+goal+backstory), Task, Crew, Process. Le plus rapide a prototyper (~20 lignes). Flows pour l'orchestration production. ~2 milliards d'executions, 30K+ GitHub stars, $18M Series A.

Migration courante : prototyper en CrewAI, migrer vers LangGraph quand la complexite augmente.

## Architecture

```
┌─────────── Crew (sequential) ──────────────┐
│                                             │
│  Task 1 → Agent "Researcher"                │
│     output ↓                                │
│  Task 2 → Agent "Analyst"                   │
│     output ↓                                │
│  Task 3 → Agent "Writer"                    │
│     output → resultat final                 │
└─────────────────────────────────────────────┘

┌─────────── Crew (hierarchical) ─────────────┐
│                                              │
│  Manager Agent (auto-genere ou custom)       │
│     ├── delegue → Researcher                 │
│     ├── delegue → Analyst                    │
│     └── review + re-delegue si qualite < OK  │
└──────────────────────────────────────────────┘

┌─────────── Flow (production) ────────────────┐
│                                               │
│  @start() research()                          │
│     ↓ @listen                                 │
│  write(research_output)                       │
│     ↓ @router                                 │
│  quality_check() → "publish" | "revise"       │
│     ↓ @listen("publish")                      │
│  publish()                                    │
│                                               │
│  @persist pour reprise, @human_feedback       │
└───────────────────────────────────────────────┘
```

## Code pattern

### Crew basique (20 lignes)

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Chercheur Support",
    goal="Trouver la reponse dans la base de connaissances",
    backstory="Expert en recherche documentaire",
    tools=[search_kb, lookup_order],
    allow_delegation=False,
)

support = Agent(
    role="Agent Support",
    goal="Repondre au client de facon claire et empathique",
    backstory="Specialiste relation client",
    allow_delegation=True,  # peut deleguer au chercheur
)

research_task = Task(
    description="Recherche la reponse a : {query}",
    expected_output="Informations pertinentes avec sources",
    agent=researcher,
)

response_task = Task(
    description="Redige une reponse client basee sur la recherche",
    expected_output="Reponse concise et empathique",
    agent=support,
    context=[research_task],  # recoit le resultat de la recherche
)

crew = Crew(
    agents=[researcher, support],
    tasks=[research_task, response_task],
    process=Process.sequential,
    memory=True,  # active la memoire unifiee
)

result = crew.kickoff(inputs={"query": user_message})
```

### Flow production (avec HITL)

```python
from crewai.flow.flow import Flow, listen, start, router

class SupportFlow(Flow):
    @start()
    def classify(self):
        return classify_crew.kickoff(inputs={"query": self.state["query"]})

    @router(classify)
    def route(self, classification):
        return classification.category  # "billing", "tech", "escalation"

    @listen("escalation")
    @human_feedback
    def escalate(self, data):
        return create_ticket(data)

    @listen("billing")
    def handle_billing(self, data):
        return billing_crew.kickoff(inputs=data)
```

## Specificites chatbot

### Memoire unifiee (Memory class)
Classe unique remplacant l'ancien systeme (short/long/entity). LLM analyse le contenu au save, infere scope et importance. Scoring : similarite (0.5) + recence (0.3, demi-vie 30j) + importance (0.2). Stockage LanceDB local.

```python
from crewai import Memory
memory = Memory(llm="gpt-4o-mini", embedder={"provider": "openai"})
crew = Crew(agents=[...], tasks=[...], memory=memory)
```

### Limites chatbot
- **Pas de streaming natif** — probleme pour l'UX conversationnelle temps-reel
- **Pas de checkpointing** (contrairement a LangGraph) — reprise apres crash limitee
- **Delegation impredictible** — avec `allow_delegation=True`, l'agent peut deleguer de facon inattendue
- **> 7 agents** — role definitions deviennent confuses, qualite degrade

### Ce qui marche bien
- Content generation multi-etapes (recherche → analyse → redaction)
- Prototypage rapide de workflows support
- Equipes qui pensent en "roles et responsabilites"

### Ce qui marche mal
- Chatbot temps-reel (pas de streaming)
- Logique conditionnelle complexe (mieux avec LangGraph)
- Petits modeles open-source (7B) — function calling instable

## Couts et quand utiliser

| Aspect | CrewAI | vs LangGraph |
|--------|--------|--------------|
| Time to prototype | **1 heure** | 1 journee |
| Learning curve | Basse | Haute |
| Token overhead | +18% | Reference |
| Checkpointing | Non | Oui |
| Streaming | Non | Oui |
| Production ceiling | Moyen | Haut |

### Quand utiliser
- Prototype rapide d'un workflow multi-agent
- Equipe non-technique ou junior
- Content generation, recherche, marketing
- Validation de concept avant invest LangGraph

### Quand eviter
- Chatbot production avec streaming
- Workflows avec HITL complexe (LangGraph meilleur)
- > 7 agents
- Besoin de checkpointing/durabilite

## Liens

- [[MOC-Techniques]]
- [[agents-frameworks]] — CrewAI = Tier 2, production-capable
- [[architecture-langgraph]] — Alternative production avec checkpointing
- [[pattern-orchestrateur]] — Pattern supervisor en CrewAI (hierarchical process)
- [[pattern-pipeline]] — Pattern sequentiel en CrewAI (sequential process)
- [[Joao Moura]] — Createur CrewAI
