---
titre: "NeoChat Adaptive Prompt Builder V2 — Architecture 4 Layers"
resume: "System prompt dynamique optimisé cache Gemini : Layer 1 core (toujours caché), Layer 2 task rules (par intent), Layer 3a tool instructions (par tool sélectionné), Layer 3b response templates, conditional rules"
aliases:
  - "neochat adaptive prompt"
  - "adaptive prompt builder"
  - "4 layer prompt"
  - "prompt builder v2"
  - "AdaptivePromptBuilderV2"
  - "neochat prompt architecture"
  - "prompts adaptatifs neochat"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#type/technique"
  - "#projet/neo_ia"
  - "#domaine/prompt-engineering"
---

## Concept

Le system prompt de chaque agent NeoChat est assemblé dynamiquement en 4 couches (layers), optimisées pour le cache implicite de Gemini 2.5 Flash. Les couches stables (L1+L2) forment un prefix cacheable, les couches dynamiques (L3) varient par requête.

## Les 4 Layers

```
┌──────────────────────────────────────┐
│ Layer 1 — CORE IDENTITY              │  Toujours inclus, toujours caché
│ Identité agent, règles absolues      │  (~2048+ tokens pour cache hit)
│ Ex: "Tu es Lojii, assistant NEOTEEM" │
├──────────────────────────────────────┤
│ Layer 2 — TASK RULES                 │  Par intent (workflow/generation/classification)
│ Règles spécifiques à la tâche        │  Souvent caché (même intent = même prefix)
│ Ex: règles MEMOIRE-FIRST, chaînement │
├──────────────── ─── ─────────────────┤  ← séparateur \n\n---\n\n
│ Layer 3a — TOOL INSTRUCTIONS         │  Par tool sélectionné dynamiquement
│ INSTRUCTION de chaque tool actif     │  Parfois caché (patterns répétitifs)
│ Injecté sous "## TOOLS DISPONIBLES"  │
├──────────────────────────────────────┤
│ Layer 3b — RESPONSE TEMPLATES        │  Par response_type du tool exécuté
│ FORMAT de réponse structuré          │  Utilisé en phase synthèse
└──────────────────────────────────────┘
```

**Séparateurs** :
- L1 + L2 : joints avec `\n\n` (section_separator) → prefix continu pour cache
- Prefix → L3 : séparé par `\n\n---\n\n` (layer_separator)

## Comment ça fonctionne

### 1. Configuration (à l'import, une seule fois)

```python
# builder.py de chaque agent
TOOL_INSTRUCTIONS = ToolPromptLoader.get_instructions_for_tools(ALL_TOOL_NAMES)
RESPONSE_TEMPLATES = ToolPromptLoader.build_response_templates("lojii")

config = AdaptivePromptConfigV2(
    core_identity=LOJII_SYSTEM_PROMPT,      # L1
    task_rules=LOJII_TASK_RULES,             # L2 : workflow, generation, classification
    tool_instructions=TOOL_INSTRUCTIONS,     # L3a : {tool_name: INSTRUCTION}
    response_templates=RESPONSE_TEMPLATES,   # L3b : {response_type: RESPONSE_FORMAT}
)
builder = AdaptivePromptBuilderV2(config)
```

### 2. Build dynamique (à chaque requête)

```python
prompt = builder.build(
    intent="workflow",                     # → sélectionne L2
    tools=["recherche_acteur", "acteur_detail"],  # → sélectionne L3a
    extra_rules=["redaction"],             # → ajoute L2 conditionnel
    user_email="jean@example.com",         # → format {user_email}
    user_name="Jean",                      # → format {user_name}
)
```

### 3. Conditional Rules (innovation clé)

Le `AgentBlueprint` déclare des `conditional_rules` :
```python
conditional_rules={"redaction": {"envoyer_mail", "repondre_mail", "transferer_mail", "creer_brouillon"}}
```

Si un de ces tools est sélectionné par le Tool RAG, la règle `"redaction"` (style d'écriture email) est automatiquement injectée comme extra L2. Les règles de style email ne polluent PAS le prompt quand l'utilisateur ne fait pas de mail.

## ToolPromptLoader — Le registre central

`packages/shared_tools/shared_tools/tools/base.py` — classe statique avec caches :

| Méthode | Rôle |
|---------|------|
| `get_tools_for_agent("lojii")` | Scanne tous les `config.yaml`, retourne les tools dont `agents` contient "lojii" |
| `get_instructions_for_tools(names)` | Import dynamique `prompts.py` de chaque tool, retourne `{name: INSTRUCTION}` |
| `build_response_templates("lojii")` | Mappe `response_type → RESPONSE_FORMAT` pour tous les tools de l'agent |
| `get_all_configs()` | Retourne tous les `ToolConfig` (utilisé par sync_tool_embeddings.py) |

**Ajouter un tool à un agent = ajouter le nom de l'agent dans `config.yaml:agents`** — ToolPromptLoader le détecte automatiquement au prochain import.

## Prompt d'un tool — Structure type

```python
# prompts.py de chaque tool
INSTRUCTION = """### recherche_acteur
**QUAND:** Utilisateur mentionne un nom, email, telephone...
<rules>...</rules>
**RETOURNE:** acteur_id, nom, mail, tel, adresse, roles[]
**EXEMPLES:** ..."""

RESPONSE_FORMAT = """<response_format tool="recherche_acteur">
<case name="single_info">...</case>
<rules>...</rules>
</response_format>"""
```

## Optimisation cache Gemini

L'architecture 4 layers est conçue pour maximiser les cache hits implicites de Gemini :

- **L1+L2 stable** : même agent + même intent = prefix identique = cache hit (~2048+ tokens économisés)
- **L3 semi-stable** : mêmes tools sélectionnés = même dynamic = cache étendu
- `estimate_cache_tokens()` : méthode de monitoring pour vérifier que L1+L2 > 1024 tokens (seuil cache)

## Builders par agent

| Agent | Builder | Core Identity | Task Rules |
|-------|---------|--------------|------------|
| Lojii | `lojii_adaptive_builder` | LOJII_SYSTEM_PROMPT | workflow, generation, classification |
| Universal | `universal_adaptive_builder` | UNIVERSAL_CORE_IDENTITY | workflow, redaction, generation |
| Support | `support_adaptive_builder` (V2) + `support_prompt_builder` (V1) | SUPPORT_SYSTEM_PROMPT | par query type |
| NeoMail | `neomail_adaptive_builder` | NEOMAIL_SYSTEM_PROMPT | workflow, generation, classification |

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `shared_utils/prompts/adaptive.py` | AdaptivePromptBuilderV2 + AdaptivePromptConfigV2 |
| `shared_utils/prompts/builder.py` | V1 AdaptivePromptBuilder (legacy, Support) |
| `shared_utils/prompts/context.py` | PromptContext (user_name, user_email, org) |
| `shared_utils/prompts/registry.py` | ToolInstructionRegistry + ResponseTemplateRegistry |
| `shared_utils/prompts/tokens.py` | Estimation tokens |
| `shared_utils/prompts/gemini/cache_optimizer.py` | Helpers éligibilité cache |
| `shared_tools/tools/base.py` | ToolPromptLoader |
| `agents/lojii/builder.py` | Config Lojii |
| `agents/universal/builder.py` | Config Universal |

## Liens

- [[neochat-architecture]]
- [[neochat-react-engine]]
- [[neochat-tool-rag]]
- [[index-prompting]]
