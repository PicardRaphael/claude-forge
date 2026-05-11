---
titre: "Index Architectures Chatbot — Decision & evaluation"
resume: "Tableau de decision : quel pattern + framework pour quel chatbot. Evaluation croisee cout/latence/complexite/production-readiness. Le point d'entree du dossier chatbot/"
aliases:
  - index architectures chatbot
  - decision framework chatbot
  - quel framework chatbot
  - evaluation architectures
  - comparatif chatbot frameworks
  - chatbot decision tree
domaine: ia
type: index
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://openai.github.io/openai-agents-python/"
  - "https://langchain-ai.github.io/langgraph/"
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/chatbot"
---

## Regle d'or

> "Optimize single LLM calls with retrieval and in-context examples BEFORE adding complexity." — Anthropic, Building Effective Agents

**Commencer par [[pattern-single-agent-multi-tool]]**. Ne passer au multi-agent que quand un seul agent ne suffit plus (system prompt > 2000 tokens, precision routing < 90%, domaines conflictuels).

## Decision tree — Quel pattern ?

```
Combien de domaines distincts ?
│
├── 1-2 domaines
│   └── [[pattern-single-agent-multi-tool]]
│       Agent unique + N outils
│       80% des chatbots sont ici
│
├── 3-5 domaines
│   ├── Latence critique ?
│   │   ├── Oui → [[pattern-swarm]]
│   │   │         -30% tokens, -33% latence
│   │   └── Non → [[pattern-orchestrateur]]
│   │             94% routing accuracy, audit trail
│   │
│   └── Process fixe/deterministe ?
│       └── Oui → [[pattern-pipeline]]
│                 Classify → Enrich → Generate → Evaluate
│
├── 6+ domaines
│   └── [[pattern-orchestrateur]] variante hierarchique
│       Supervisor → sub-supervisors → workers
│
└── Process sequentiel strict ?
    └── [[pattern-pipeline]]
        Chaque step pre-determine
```

## Decision tree — Quel framework ?

```
Contrainte principale ?
│
├── Budget tokens
│   └── Gemini Flash-Lite ($0.10/MTok)
│       25x moins cher que GPT-4o
│       → [[architecture-gemini-api]]
│
├── Voice / Realtime
│   └── OpenAI Realtime API (seul a l'avoir)
│       → [[architecture-openai-api]]
│
├── Checkpointing / HITL / Durabilite
│   └── LangGraph + PostgresSaver
│       Time-travel debugging, interrupts natifs
│       → [[architecture-langgraph]]
│
├── Prototype rapide (< 1 jour)
│   └── CrewAI (20 lignes pour demarrer)
│       → [[architecture-crewai]]
│
├── Long-context documents (1M tokens)
│   └── Claude API (precision long-context superieure)
│       → [[architecture-claude-api]]
│
├── Interop cross-framework (A2A)
│   └── Google ADK + A2A protocol
│       → [[architecture-gemini-api]]
│
├── Infrastructure hebergee (zero ops)
│   └── Claude Managed Agents ($0.08/h)
│       → [[architecture-claude-api]]
│
├── Etat server-side (zero gestion historique)
│   └── OpenAI Conversations API ou Gemini Interactions API
│       → [[architecture-openai-api]] | [[architecture-gemini-api]]
│
└── Maximum controle + simplicite
    └── Raw SDK (Anthropic/OpenAI) sans framework
        -40-60% code, -8-22% latence vs framework
```

## Matrice d'evaluation croisee

### Par framework

| Critere | Claude API | OpenAI API | LangGraph | CrewAI | Gemini/ADK | AutoGen |
|---------|-----------|-----------|-----------|--------|-----------|---------|
| **Production-ready** | Haute | Haute | Haute | Moyenne | Moyenne | Basse |
| **Cout tokens** | Moyen | Variable | N/A (LLM) | N/A (+18%) | **Tres bas** | N/A (5-6x) |
| **Learning curve** | Basse | Basse | **Haute** | **Basse** | Moyenne | Moyenne |
| **Streaming** | Oui | Oui | Oui | **Non** | Oui | Non |
| **Checkpointing** | Non | Basique | **Natif** | Non | Basique | Non |
| **HITL** | Basique | Guardrails | **Interrupts** | Flows | Workflow | UserProxy |
| **Voice/Realtime** | Non | **Oui** | Non | Non | Non | Non |
| **Multi-agent** | Managed | Handoffs | Graph | Crews | ADK+A2A | GroupChat |
| **Model-agnostic** | Non | Non | **Oui** | **Oui** | Non* | **Oui** |
| **Memoire cross-session** | Client | Server | Store | Memory | Session | Non |

*ADK supporte d'autres modeles mais optimise pour Gemini

### Par pattern

| Pattern | Complexite | Latence | Tokens | Routing accuracy | Audit trail | Cas d'usage |
|---------|-----------|---------|--------|-----------------|-------------|-------------|
| **Single Agent** | **Basse** | **1-3s** | **~1,200** | Outil-level | Basique | 80% des cas |
| **Orchestrateur** | Moyenne | ~4.2s | ~2,800 | **94%** | **Centralise** | Support multi-domaine |
| **Swarm** | Moyenne | **~2.8s** | **~1,900** | 91% | Distribue | Latence critique |
| **Pipeline** | Basse | N × step | Variable | N/A (fixe) | Par step | Process deterministe |
| **Hierarchique** | **Haute** | +50-100% | x1.5-2 | ~94%/niveau | Multi-niveau | 6+ domaines |

## Architectures recommandees par cas d'usage

### Chatbot FAQ / Support simple
- **Pattern** : [[pattern-single-agent-multi-tool]]
- **Framework** : Claude API (Sonnet) ou OpenAI (GPT-4.1)
- **Cout estimatif** : ~$0.004/conversation (3,700 tokens moyen)
- **Implementation** : boucle tool_use, 3-5 outils (search_kb, lookup_order, create_ticket)

### Support client multi-domaine (3-5 domaines)
- **Pattern** : [[pattern-orchestrateur]] (commencer) → [[pattern-swarm]] (optimiser)
- **Framework** : LangGraph (si HITL/audit) ou OpenAI Agents SDK (si simplicite)
- **Cout estimatif** : ~$0.01-0.03/conversation
- **Implementation** : supervisor classifie, specialistes repondent

### Chatbot haute qualite (reponses verifiees)
- **Pattern** : [[pattern-pipeline]] (evaluator-optimizer)
- **Framework** : Claude API (extended thinking) ou raw SDK
- **Cout estimatif** : ~$0.02-0.05/conversation (3-5 iterations)
- **Implementation** : generate → evaluate → re-generate si score < 8

### Agent conversationnel temps-reel / voice
- **Pattern** : [[pattern-swarm]] ou single-agent
- **Framework** : OpenAI Realtime API (voice) + Agents SDK
- **Cout estimatif** : Variable (audio tokens)
- **Implementation** : Realtime API + handoffs pour routing

### Agent autonome long-running (recherche, coding)
- **Pattern** : [[pattern-orchestrateur]] hierarchique
- **Framework** : Claude Managed Agents ($0.08/h) ou LangGraph Cloud
- **Cout estimatif** : $0.08-0.70/session (1h Opus)
- **Implementation** : coordinator + specialists dans threads isoles

### Chatbot budget extreme (volume eleve)
- **Pattern** : [[pattern-single-agent-multi-tool]]
- **Framework** : Gemini Flash-Lite ($0.10/MTok input)
- **Cout estimatif** : ~$0.0004/conversation (10x moins que Sonnet)
- **Implementation** : function calling Gemini, automatic execution

## Optimisations transversales

### Cout
1. **Prompt caching** : -90% sur cache hit (Claude), -50-90% (OpenAI)
2. **Batch API** : -50% (tous providers), si latence < 24h acceptable
3. **Triage modele** : Haiku/Nano pour classifier, Sonnet/4.1 pour repondre
4. **Tool Search / deferred loading** : -85% tokens sur definitions outils (> 10 outils)

### Latence
1. **Streaming** : latence percue reduite de 3-5x
2. **Appels paralleles** : outils independants en parallele (Claude, GPT-4.1+, Gemini)
3. **Swarm over supervisor** : -33% latence single-domain
4. **Raw SDK over framework** : -8-22% (pas d'overhead LangGraph ~14ms/op)

### Qualite
1. **Descriptions outils precises** : "une bonne description vaut 3 outils" (Anthropic)
2. **Evaluator-optimizer** : boucle generate-evaluate pour reponses verifiees
3. **Extended thinking** (Claude) / reasoning (o3/o4-mini) pour cas complexes
4. **Gates programmatiques** : validation code entre steps, pas juste LLM

## Evolution typique

```
Phase 1 : Single agent + 3-5 outils (MVP, 1 semaine)
    ↓ volumes augmentent, domaines se multiplient
Phase 2 : Orchestrateur + 3 specialistes (v1 prod, 1 mois)
    ↓ latence critique, domaines stabilises
Phase 3 : Swarm avec handoffs (optimisation, itératif)
    ↓ besoin de durabilite/audit
Phase 4 : LangGraph avec checkpointing (enterprise)
```

## Notes du dossier

### Frameworks
- [[architecture-claude-api]] — Messages API, Agent SDK, Managed Agents
- [[architecture-openai-api]] — Responses API, Agents SDK, Conversations
- [[architecture-langgraph]] — StateGraph, checkpointing, HITL
- [[architecture-crewai]] — Crews, Flows, prototypage rapide
- [[architecture-gemini-api]] — Function calling, ADK, A2A
- [[architecture-autogen]] — GroupChat, en declin

### Patterns
- [[pattern-single-agent-multi-tool]] — Le defaut (80% des cas)
- [[pattern-orchestrateur]] — Supervisor central + hierarchique
- [[pattern-swarm]] — Handoffs decentralises
- [[pattern-pipeline]] — Chaine sequentielle + evaluator-optimizer

### Contexte
- [[agents-architecture]] — Patterns abstraits (WHAT)
- [[agents-frameworks]] — Comparatif general frameworks
- [[Agents IA]] — MOC principal agents

## Liens

- [[MOC-Techniques]]
