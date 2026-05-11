---
titre: "Architecture AutoGen/AG2 — Multi-agent conversationnel"
resume: "AutoGen (Microsoft) en declin : GroupChat, AssistantAgent, nested chats. Successeur = Microsoft Agent Framework. Usage = recherche/prototypage uniquement"
aliases:
  - architecture autogen
  - autogen chatbot
  - ag2 chatbot
  - autogen groupchat
  - microsoft autogen
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://github.com/ag2ai/ag2"
  - "https://microsoft.github.io/autogen/stable/"
  - "https://docs.ag2.ai/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/microsoft"
---

## Definition

Framework multi-agent conversationnel de Microsoft Research, maintenant scinde en deux : **AG2** (fork communautaire open-source) et **Microsoft AutoGen** (steering vers Microsoft Agent Framework). Pattern unique : GroupChat ou les agents debattent dans un thread partage avec selection de speaker par LLM.

**Statut 2026 : en declin pour la production.** Le vault `agents-frameworks.md` le confirme : "Adoption production en declin apres le split Microsoft. Zero mecanismes securite. Boucles de conversation = cout explosif si non-bornees."

Usage recommande : recherche academique, prototypage de patterns conversationnels.

## Architecture

```
┌──────────── GroupChat ───────────────────────┐
│                                              │
│  GroupChatManager (selectionne le speaker)    │
│    ├── Tour 1 : Planner parle                │
│    ├── Tour 2 : Researcher repond            │
│    ├── Tour 3 : Analyst critique             │
│    ├── Tour 4 : Planner ajuste              │
│    └── ... (max_round pour limiter)          │
│                                              │
│  Speaker selection : auto (LLM), round_robin,│
│  random, manual, callable                    │
│  TOUT l'historique est partage entre agents   │
└──────────────────────────────────────────────┘
```

## Code pattern

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

llm_config = {"model": "gpt-4", "api_key": "..."}

planner = AssistantAgent("planner", llm_config=llm_config,
    system_message="Tu planifies les taches.")
researcher = AssistantAgent("researcher", llm_config=llm_config,
    system_message="Tu recherches les informations.")
analyst = AssistantAgent("analyst", llm_config=llm_config,
    system_message="Tu analyses et critiques.")

user_proxy = UserProxyAgent("user", human_input_mode="NEVER",
    code_execution_config={"work_dir": "output"})

group_chat = GroupChat(
    agents=[user_proxy, planner, researcher, analyst],
    messages=[], max_round=10,
    speaker_selection_method="auto",
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="Analyse les tendances IA Q3")
```

## Pourquoi en declin

| Probleme | Impact |
|----------|--------|
| Split Microsoft/AG2 | Fragmentation, confusion documentation |
| Zero securite native | Pas de sandboxing, pas de guardrails |
| Boucles non-bornees | Cout 5-6x vs LangGraph si `max_round` mal configure |
| Pas de checkpointing | Pas de reprise apres crash |
| Python only | Pas de support multi-langage |

### Successeur : Microsoft Agent Framework 1.0
Unifie Semantic Kernel + AutoGen. .NET et Python LTS. Pour les equipes Microsoft, c'est la voie recommandee.

## Quand utiliser malgre tout

- Recherche academique sur les patterns de debat multi-agent
- Prototypage rapide de GroupChat (le pattern est unique)
- Budget zero (Apache 2.0, pas de cout framework)
- AutoGen Studio pour explorer visuellement les patterns

## Liens

- [[MOC-Techniques]]
- [[agents-frameworks]] — AutoGen = en declin
- [[architecture-langgraph]] — Alternative production recommandee
- [[pattern-orchestrateur]] — GroupChatManager ≈ pattern orchestrateur conversationnel
