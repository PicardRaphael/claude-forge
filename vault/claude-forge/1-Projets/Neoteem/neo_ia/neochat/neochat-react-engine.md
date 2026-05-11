---
titre: "NeoChat Declarative ReAct Engine — 7 Phases"
resume: "Moteur ReAct générique piloté par AgentBlueprint : 7 phases (resume interrupts → pending action → cache-first → tool selection → auto-add → build conversation → ReAct loop), remplace ~1500L par agent"
aliases:
  - "neochat react engine"
  - "declarative react engine"
  - "react workflow node"
  - "neochat engine"
  - "AgentBlueprint"
  - "agent blueprint neochat"
  - "7 phases react"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#projet/neo-ia"
  - "#domaine/agents"
  - "#type/technique"
---

## Concept

Le Declarative ReAct Engine est le coeur de NeoChat. Un seul fichier `shared_utils/engine/react.py` (~780L) remplace les workflows individuels de chaque agent (chacun ~1500L avant refacto).

Chaque agent se définit via un `AgentBlueprint` (~50 lignes) qui déclare :
- `prompt_builder` : instance AdaptivePromptBuilderV2
- `tool_selector` : callable async pour la sélection de tools
- `interrupt_handlers` : liste ordonnée de handlers
- `hooks` : AgentHooks (extract_draft, inject_user_context, inject_draft)
- `config` : EngineConfig (max_iterations, cache_first, draft_context, pending_action)
- `conditional_rules` : règles L2 injectées si certains tools sont sélectionnés
- `fallback_tools` : tools par défaut si sélection retourne 0 résultat

## Les 7 Phases

### Phase 0 — Resume Interrupts
Itère sur `blueprint.interrupt_handlers`. Si un handler détecte un état en attente (`detect_in_state`), il le résout (ex: l'utilisateur a choisi un acteur parmi plusieurs). Deux issues :
- `continue_loop=True` : applique les state updates et continue vers Phase 3
- `continue_loop=False` : retourne immédiatement le state update (GraphInterrupt)

### Phase 1 — Pending Action Confirmation
Si `enable_pending_action=True` et qu'une action est en attente (ex: "oui, lis ce mail"), vérifie si la query est une confirmation (`is_confirmation` ou `is_implicit_confirmation` via LLM) et exécute l'action.

### Phase 2 — Cache-First Answer
Si `enable_cache_first=True` et pas en resume, tente de répondre directement depuis le `ToolCache` (acteurs, documents déjà en mémoire). Deux patterns :
- **Lojii** : réponse directe (`is_complete=True`), skip la synthèse
- **Universal** : passe au noeud `synthesize` pour formater

### Phase 3 — Tool Selection
Sélection dynamique via `blueprint.tool_selector` (= `HybridToolSelector` en production).

Stratégies selon le contexte :
| Contexte | `use_llm_expansion` | `context_hint` |
|----------|---------------------|----------------|
| Fresh query | `True` | Aucun |
| Follow-up (cache acteurs) | `False` | Noms acteurs + résumé |
| Resume avec state | Skip (reload) | — |
| Resume sans state | `False` | — |

**Tool coverage check** : si resume depuis interrupt, compare l'embedding de la nouvelle query vs les tools cachés. Si cosine < 0.40 → force re-sélection (changement de domaine fonctionnel).

### Phase 4 — Auto-Add Tools
- Si des documents sont en cache → ajoute `analyze_drive_document`
- Si `pending_action` existe → ajoute le tool correspondant

### Phase 5 — Build Conversation
Construction de la liste de messages pour le LLM :

```
1. SystemMessage(system_prompt)           ← AdaptivePromptBuilderV2.build()
2. SystemMessage([RESUME CONVERSATION])   ← conversation_summary (max 5000 chars)
3. SystemMessage([HISTORIQUE OUTILS])     ← turn_digests des tours précédents
4. SystemMessage([CONTEXTE ACTIF])        ← cache-aware instructions (acteurs/docs)
5. ToolMessage[]                          ← résultats repris depuis interrupt
6. History messages[]                     ← 8 derniers tours (extract_recent_history)
7. HumanMessage(context + question)       ← cache_context + draft_context + query
```

**Conditional rules** : si des tools sélectionnés matchent `blueprint.conditional_rules` (ex: `envoyer_mail` → `"redaction"`), les règles L2 correspondantes sont injectées dans le prompt.

### Phase 6 — ReAct Loop
Boucle max `config.max_iterations` (défaut 5) :

```
LLM.bind_tools(tools).ainvoke(conversation)
  ↓
Pour chaque tool_call :
  1. Delete confirmation check (DeleteConfirmHandler)
  2. Invariant validation (validate_tool_call)
     → peut BLOQUER, MODIFIER args, ou PERMETTRE
  3. Execute tool (execute_tool avec injection user_email/acteur_id)
  4. Post-execution interrupt detection (handlers.detect_in_result)
     → peut INTERROMPRE (GraphInterrupt) ou CONTINUER
  5. Cache update (cache_result → ToolCache)
  6. Format pour LLM (format_result_for_llm → ToolMessage)
  7. Détection chaining signal ([ACTIONS DISPONIBLES])
```

**Sortie de boucle** : pas de `tool_calls` OU pas de chaining signal OU max_iterations atteint OU tous les résultats OK sans final action en attente.

### Phase 7 — Return State
Construit le state update avec : tool_results, tool_cache, selected_actor, selected_tools, turn_digests, web_sources. Nettoie les états d'interrupt si nécessaire. Extrait le draft context (mail) si activé.

## AgentBlueprint — Dataclass complète

```python
@dataclass
class AgentBlueprint:
    name: str                           # "lojii", "universal"
    state_class: type                   # InterruptCapableState
    prompt_builder: AdaptivePromptBuilderV2
    tool_selector: Callable             # async (query, **kw) -> list[Tool]
    interrupt_handlers: list[InterruptHandler]
    hooks: AgentHooks                   # extract_draft, inject_user_context, inject_draft
    config: EngineConfig                # max_iterations, cache_first, draft_context, pending_action
    smart_mail_tools: set[str]
    delete_tools: set[str]
    tools_with_pending_actors: set[str]
    confirm_messages: dict[str, str]
    optimize_prompt: str
    fallback_tools: list[str]
    conditional_rules: dict[str, set[str]]  # rule_key -> set of trigger tools
```

## Exemple concret : UNIVERSAL_BLUEPRINT

```python
UNIVERSAL_BLUEPRINT = AgentBlueprint(
    name="universal",
    state_class=InterruptCapableState,
    prompt_builder=universal_adaptive_builder,
    tool_selector=select_tools_for_query,
    interrupt_handlers=[
        ActorSelectionHandler(tools_with_pending_actors=TOOLS_WITH_PENDING_ACTORS),
        PendingRolesHandler(),
        ComposeInterruptHandler(),
        MailPreviewHandler(optimize_prompt=..., confirm_messages=...),
        DeleteConfirmHandler(delete_tools=DELETE_TOOLS, confirm_messages=...),
    ],
    hooks=AgentHooks(extract_draft_context=True, inject_user_context=True, inject_draft_context=True),
    config=EngineConfig(max_iterations=5, enable_cache_first=True, enable_draft_context=True, enable_pending_action=True),
    conditional_rules={"redaction": REDACTION_TOOLS},
)
```

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `shared_utils/engine/react.py` | react_workflow_node (7 phases) |
| `shared_utils/engine/blueprint.py` | AgentBlueprint + EngineConfig |
| `shared_utils/engine/graph.py` | create_react_graph (StateGraph builder) |
| `shared_utils/engine/state.py` | BaseAgentState, InterruptCapableState |
| `shared_utils/engine/interrupts.py` | InterruptHandler base, WorkflowContext |
| `shared_utils/engine/invariants.py` | validate_tool_call (pre-execution checks) |
| `shared_utils/engine/utils.py` | execute_tool, safe_serialize |
| `shared_utils/engine/synthesis.py` | synthesize_response_node |
| `shared_utils/engine/hooks.py` | AgentHooks dataclass |
| `shared_utils/engine/handlers/` | 6 handlers concrets |

## Liens

- [[neochat-architecture]]
- [[neochat-adaptive-prompt]]
- [[neochat-tool-rag]]
- [[agents-architecture]]
