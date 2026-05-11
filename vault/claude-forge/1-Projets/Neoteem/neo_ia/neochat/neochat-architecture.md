---
titre: "NeoChat Architecture — Vue d'ensemble"
resume: "Architecture complète NeoChat : Declarative ReAct Engine, 26 tools avec Tool RAG pgvector, Adaptive Prompt Builder 4 layers, 6 interrupt handlers, 7 agents spécialisés"
aliases:
  - "neochat architecture"
  - "architecture neochat"
  - "neochat overview"
  - "neochat archi"
  - "lojii architecture"
  - "universal agent architecture"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#projet/neo-ia"
  - "#domaine/agents"
  - "#domaine/ia"
---

## Vue d'ensemble

NeoChat est l'app principale du monorepo [[neo_ia]]. C'est un système d'agents conversationnels B2B construit sur LangGraph + Gemini 2.5 Flash, avec une architecture **déclarative** où chaque agent = un `AgentBlueprint` de ~50 lignes au lieu de ~1500 lignes de workflow.

## Architecture en couches

```
┌─────────────────────────────────────────────────┐
│  API FastAPI (apps/neochat/api/)                │
│  SSE streaming, auth, rate limiting             │
├─────────────────────────────────────────────────┤
│  Agents (7 types)                               │
│  Lojii | Universal | Support | Web | Devis | …  │
│  Chaque agent = AgentBlueprint déclaratif       │
├─────────────────────────────────────────────────┤
│  Declarative ReAct Engine (shared_utils/engine/)│
│  7 phases, generic pour tous les agents         │
│  → voir [[neochat-react-engine]]                │
├─────────────────────────────────────────────────┤
│  Adaptive Prompt Builder V2 (4 layers)          │
│  Optimisé cache Gemini implicite                │
│  → voir [[neochat-adaptive-prompt]]             │
├─────────────────────────────────────────────────┤
│  HybridToolSelector (Tool RAG pgvector)         │
│  Full-text + semantic + RRF + LLM rerank        │
│  → voir [[neochat-tool-rag]]                    │
├─────────────────────────────────────────────────┤
│  26 Tools (packages/shared_tools/)              │
│  Chaque tool = config.yaml + prompts.py +       │
│  schemas.py + tool.py                           │
├─────────────────────────────────────────────────┤
│  Infrastructure (packages/shared_utils/)         │
│  LLM factory, DB, auth, billing, Langfuse       │
└─────────────────────────────────────────────────┘
```

## Les 7 agents NeoChat

| Agent | Domaine | Engine | Fichiers clés |
|-------|---------|--------|---------------|
| **Lojii** | NEOTEEM (acteurs, docs GED) | Declarative ReAct | `agents/lojii/blueprint.py` |
| **Universal** | Gmail + NEOTEEM + Support + Web | Declarative ReAct | `agents/universal/blueprint.py` |
| **Support** | Documentation Confluence (RAG) | LangGraph custom | `agents/support/graph.py` |
| **Web** | Sources officielles (Legifrance…) | LangGraph custom (classify→search→aggregate→synthesize→respond) | `agents/web/graph.py` |
| **Devis** | Analyse de devis fournisseurs | LangGraph custom | `agents/devis/graph.py` |
| **Annonce Immo** | Parsing annonces immobilières | LangGraph custom | `agents/annonce_immobiliere/graph.py` |
| **Reformulation** | Réécriture de texte (4 types) | LangGraph custom | `agents/reformulation/graph.py` |

**Lojii** et **Universal** utilisent le Declarative ReAct Engine partagé. Les autres ont des graphs LangGraph dédiés.

## Pattern ToolInTool (composition inter-tools)

NeoChat n'utilise PAS de pattern où un tool public appelle un autre tool public via `ainvoke()`. La composition se fait par :

1. **Shared resolution logic** : `recherche_document` importe `resolve_actor_context` de `recherche_acteur` (fonction Python directe, pas invocation via le framework tool)
2. **Internal tools** : `recherche_document` appelle `recherche_ged` (tool interne dans `_internal/`, non exposé au LLM) via `.ainvoke()`
3. **Dependency BFS** : `dependencies.py` auto-ajoute les tools prérequis (ex: `recherche_document` → ajoute `recherche_acteur`)
4. **Chaining signal** : les résultats contiennent `[ACTIONS DISPONIBLES: ...]` que le ReAct loop détecte pour continuer

## Structure d'un tool (26 tools)

Chaque tool vit dans `packages/shared_tools/shared_tools/tools/<name>/` :

```
<tool_name>/
├── config.yaml    # name, agents, description, examples, negative_examples, confusable_with, response_type
├── prompts.py     # INSTRUCTION (injecté dans le system prompt) + RESPONSE_FORMAT
├── schemas.py     # Pydantic InputModel (pour Gemini function calling)
└── tool.py        # @tool decorated async function (LangChain)
```

**Ajouter un tool à un agent = ajouter le nom de l'agent dans `config.yaml:agents`** — zéro import, zéro code agent à modifier.

## Interrupt Handlers (pattern confirmation)

Les handlers gèrent les interruptions utilisateur (sélection d'acteur, preview mail, confirmation suppression) :

| Handler | Rôle | Agents |
|---------|------|--------|
| `ActorSelectionHandler` | Disambiguation quand plusieurs acteurs trouvés | Lojii, Universal |
| `PendingRolesHandler` | Choix de rôle quand acteur a plusieurs rôles | Lojii, Universal |
| `ComposeInterruptHandler` | Formulaire compose quand mail sans sujet/body | Universal |
| `MailPreviewHandler` | Preview + optimisation LLM avant envoi | Universal |
| `DeleteConfirmHandler` | Confirmation avant suppression | Universal |
| `SupportNoDocsHandler` | Gestion cas zéro documents trouvés | Support |

## Services auxiliaires

- **Summarizer** : résumé incrémental de conversation (gemini-2.5-flash, seuil 4000 tokens / 10 messages)
- **History** : sliding window max 50 messages, smart loading (résumé + 10 derniers si > 10 messages)
- **ToolCache** : FIFO cross-turn (max 3 acteurs, 10 docs/acteur), persiste dans LangGraph state
- **Langfuse** : tracing uniquement (pas de prompt management runtime)

## Liens

- [[neo_ia]]
- [[neochat-react-engine]]
- [[neochat-adaptive-prompt]]
- [[neochat-tool-rag]]
- [[agents-architecture]]
