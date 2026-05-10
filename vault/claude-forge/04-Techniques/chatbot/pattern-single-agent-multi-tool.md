---
titre: "Pattern Single Agent Multi-Tool — Le defaut"
resume: "Pattern le plus simple et le plus courant : 1 seul agent avec N outils. Couvre 80% des cas chatbot. Code Claude, OpenAI, LangGraph. Quand PAS besoin de multi-agent"
aliases:
  - single agent multi tool
  - agent unique multi outils
  - pattern agent simple
  - chatbot basique
  - one agent many tools
  - pattern defaut chatbot
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/patterns"
---

## Definition

Un seul agent LLM equipe de N outils. Pas de multi-agent, pas de routing, pas de handoffs. Le LLM decide quand et quel outil appeler en boucle jusqu'a resolution.

C'est le **pattern par defaut** pour les chatbots. Anthropic recommande : "Optimize single LLM calls with retrieval and in-context examples AVANT d'ajouter de la complexite."

**Regle de decision** : si tu peux resoudre le probleme avec 1 agent + outils, ne pas aller en multi-agent. Multi-agent uniquement quand les domaines sont trop differents pour un seul system prompt.

## Architecture

```
┌─────────────────────────────────────────────┐
│         Single Agent + N Tools               │
│                                              │
│  User ──→ LLM (system prompt + tools)        │
│              │                               │
│              ├── tool_call: lookup_order      │
│              │   → result → LLM              │
│              ├── tool_call: search_faq        │
│              │   → result → LLM              │
│              ├── tool_call: create_ticket     │
│              │   → result → LLM              │
│              └── reponse finale → User        │
│                                              │
│  Boucle : tant que stop_reason == "tool_use" │
└─────────────────────────────────────────────┘
```

## Code pattern

### Claude API

```python
from anthropic import Anthropic
client = Anthropic()

tools = [
    {"name": "lookup_order", "description": "Cherche le statut d'une commande par ID",
     "input_schema": {"type": "object", "properties": {
         "order_id": {"type": "string"}}, "required": ["order_id"]}},
    {"name": "search_faq", "description": "Cherche dans la base de connaissances",
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string"}}, "required": ["query"]}},
    {"name": "create_ticket", "description": "Cree un ticket support",
     "input_schema": {"type": "object", "properties": {
         "subject": {"type": "string"},
         "description": {"type": "string"},
         "priority": {"type": "string", "enum": ["low", "medium", "high"]},
     }, "required": ["subject", "description"]}},
]

messages = [{"role": "user", "content": user_query}]
response = client.messages.create(
    model="claude-sonnet-4-6", system=SYSTEM_PROMPT,
    tools=tools, max_tokens=1024, messages=messages,
)

while response.stop_reason == "tool_use":
    results = [execute_tool(block) for block in response.content
               if block.type == "tool_use"]
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": results})
    response = client.messages.create(
        model="claude-sonnet-4-6", system=SYSTEM_PROMPT,
        tools=tools, max_tokens=1024, messages=messages,
    )
```

### OpenAI Responses API

```python
response = client.responses.create(
    model="gpt-4.1",
    instructions=SYSTEM_PROMPT,
    input=user_query,
    tools=tools,
    store=True,  # persistance server-side
)
# La boucle agentique est geree par l'API si outils heberges
# Pour les custom tools, boucler sur tool_calls comme Claude
```

### LangGraph (ReAct)

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[lookup_order, search_faq, create_ticket],
    prompt=SYSTEM_PROMPT,
)
config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = await agent.ainvoke({"messages": [("user", query)]}, config)
```

## System prompt chatbot

```xml
<role>
Tu es l'assistant virtuel de [Entreprise].
Tu aides les clients avec leurs commandes, questions, et problemes.
</role>

<outils_disponibles>
- lookup_order : TOUJOURS utiliser avant de repondre sur un statut de commande
- search_faq : chercher la reponse dans la base de connaissances AVANT de repondre
- create_ticket : creer un ticket si le probleme necessite un suivi humain
</outils_disponibles>

<regles>
- Ne devine JAMAIS une information verifiable par outil
- Appelle les outils en parallele quand possible (ex: lookup_order + search_faq)
- Si aucun outil ne peut aider, dis-le honnetement
- Reponses concises : 2-3 phrases max sauf explication technique
</regles>

<escalade>
- Demande de remboursement > 500€ → create_ticket(priority="high")
- 3+ echanges sans resolution → create_ticket + proposer contact humain
- Sujet hors scope → "Je ne suis pas en mesure de vous aider. Contactez..."
</escalade>
```

## Specificites chatbot

### Combien d'outils ?
- **Optimal** : 5-15 outils bien decrits
- **Au-dela de 20** : le LLM perd en precision de selection. Solutions :
  - Claude : `defer_loading: true` (Tool Search) → -85% tokens
  - OpenAI : tool namespaces + deferred loading
  - Tous : regrouper les outils par domaine, lazy-load

### Outils paralleles
Claude et GPT-4.1+ supportent les appels d'outils paralleles. Un seul tour pour lookup_order ET search_faq simultanement. Economie : -1 round-trip.

**Attention** : structured outputs (strict mode OpenAI) incompatible avec parallel tool calls.

### Quand passer au multi-agent ?
Signes qu'un seul agent ne suffit plus :
- System prompt > 2000 tokens (trop de domaines)
- Precision de routing outil < 90%
- Outils conflictuels (meme nom/description pour domaines differents)
- Besoin de personas/tons differents selon le domaine

### Optimisation des descriptions d'outils
Anthropic : "Write better tool descriptions, not more tools." Une description precise vaut 3 outils supplementaires.

Bonnes descriptions :
```
"Recherche le statut d'une commande par son ID. Retourne : statut, date estimee, 
 transporteur. Utiliser quand le client demande 'ou est ma commande'."
```

Mauvaises descriptions :
```
"Lookup order"  # trop vague, le LLM ne sait pas quand l'utiliser
```

## Couts et quand utiliser

| Aspect | Single Agent | vs Multi-Agent |
|--------|-------------|----------------|
| Tokens/requete | ~1,000-1,500 | -40-60% |
| Latence | 1-3s | -50% |
| Complexite code | Basse | -80% |
| Maintenabilite | Haute | Bien meilleure |
| Qualite routing | Outil-level | Agent-level |

### Quand utiliser (80% des cas)
- Chatbot FAQ avec base de connaissances
- Support client single-domain
- Assistant interne (lookup, creation, recherche)
- Tout cas avec < 3 domaines distincts

### Quand passer au multi-agent
- 4+ domaines tres distincts
- Besoin de personas/specialisations differentes
- Workflows avec HITL complexes
- Audit trail par domaine necessaire

## Liens

- [[agents-architecture]] — Tool Use (theorie)
- [[pattern-orchestrateur]] — Quand upgrader vers multi-agent
- [[architecture-claude-api]] — Implementation Claude
- [[architecture-openai-api]] — Implementation OpenAI
- [[architecture-langgraph]] — Implementation LangGraph
