---
titre: "Programmatic Tool Calling (PTC) — code orchestre, modèle juge"
resume: "Feature Anthropic mai 2026 : Claude écrit du code Python qui orchestre les tools dans un sandbox d'exécution, élimine N round-trips inférence, réduit token consumption massivement. Principe : 'use code for what code is good at, use models for what models are good at'."
aliases:
  - "programmatic tool calling"
  - "PTC anthropic"
  - "code orchestration anthropic"
  - "code execution tool"
  - "code as action pattern"
  - "workflow.js claude code"
  - "anthropic workflows shipped"
  - "allowed_callers code execution"
  - "claude python orchestrator"
derniere-maj: 2026-05-23
auteur: claude
type: technique
sources:
  - "https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling (docs officielles Anthropic)"
  - "https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc (cookbook)"
  - "https://www.anthropic.com/engineering/advanced-tool-use (engineering blog Anthropic)"
  - "Tweet @_vmlops 23 mai 2026 https://x.com/_vmlops/status/2058009381422412240 (illustration externe, pas source primaire)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/orchestration"
  - "#doctrine/2026"
---

# Programmatic Tool Calling (PTC) — code orchestre, modèle juge

> Feature Anthropic mai 2026. Le principe canonique : **le code orchestre le contrôle de flux, le modèle gère uniquement le jugement à chaque étape**.

## QUOI — Définition

**Programmatic Tool Calling (PTC)** : au lieu que Claude appelle les tools un par un avec chaque résultat qui re-entre dans son contexte, **Claude écrit du code Python** dans un **sandbox d'exécution** (Code Execution Tool) qui orchestre plusieurs tool calls, traite leurs outputs, et contrôle ce qui rentre dans le context window.

```
Pattern traditionnel (tool calling classique) :
Claude → tool A → résultat dans contexte → Claude → tool B → résultat dans contexte → ...
(N round-trips inférence, contexte gonfle linéairement)

Pattern PTC :
Claude → écrit Python qui orchestre N tool calls → sandbox exécute → seul l'output final entre dans contexte
(1 round-trip, contexte ne reçoit que l'agrégat)
```

**Verbatim docs Anthropic** ([platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)) :

> "Programmatic tool calling allows Claude to write code that calls your tools programmatically within a code execution container, rather than requiring round trips through the model for each tool invocation. This reduces latency for multi-tool workflows and decreases token consumption by allowing Claude to filter or process data before it reaches the model's context window."

## POURQUOI — Le problème résolu

### Pattern ancien (orchestrateur LLM)
- 1 LLM orchestre tout — spawne sub-agents, garde tous les résultats, planifie l'étape suivante
- **Problème** : chaque résultat de sub-agent re-entre dans le contexte de l'orchestrateur
- 10 sub-agents → main session paie une "token tax", contexte se remplit, qualité dégrade

### Pattern PTC (orchestrateur code)
- Code Python orchestre — contrôle de flux dans du code, modèle ne gère que le **jugement à chaque étape**
- **Bénéfice** : contexte reste propre, latence réduite (N inférences → 1), token consumption massivement réduite

### Principe verbatim
> *"use code for what code is good at, use models for what models are good at"*
> — @_vmlops, tweet 23 mai 2026 (résume principle docs Anthropic)

Code = control flow, loops, conditionals, data transformations.
Modèle = jugement contextuel, génération, raisonnement.

## COMMENT — Structure technique

### Configuration API

```python
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Query sales data..."}],
    tools=[
        {"type": "code_execution_20260120", "name": "code_execution"},
        {
            "name": "query_database",
            "description": "...",
            "input_schema": {...},
            "allowed_callers": ["code_execution_20260120"],  # ← clé du pattern
        },
    ],
)
```

**Clé du pattern** : `allowed_callers: ["code_execution_<timestamp>"]` dans la définition du tool — opt-in pour permettre au code Python d'appeler ce tool depuis le sandbox.

### Flow d'exécution

```
1. Claude écrit Python (multi-step orchestration)
2. Code s'exécute dans sandbox managé Anthropic
3. Code pause quand il a besoin d'un tool result
4. Tool result retourne au SCRIPT (pas au modèle)
5. Script continue, agrège, transforme
6. Seul l'output final entre dans le contexte de Claude
```

### Métriques Anthropic (verbatim docs)

- **Internal knowledge retrieval** : 25.6% → **28.5%** (avec PTC)
- **GIA benchmarks** : 46.5% → **51.2%** (avec PTC)
- **Token consumption** : réduction massive (filtrage avant context)
- **Latence** : 20 tool calls = 1 inference vs 20 inferences

### Use case réel docs

> "Checking budget compliance across 20 employees: the traditional approach requires 20 separate model round-trips, pulling thousands of expense line items into the context along the way. With programmatic tool calling, a single script runs all 20 lookups, filters the results, and returns only the employees who exceeded their limits, shrinking what Claude needs to reason over from hundreds of kilobytes down to a handful of lines."

## QUAND — Critère d'application

### Utiliser PTC quand :
- ✅ **Orchestration multi-tools** (>3 tools dans la même tâche)
- ✅ **Boucles, conditionnels, data transformations** (logique de contrôle)
- ✅ **Filtrage / agrégation** de gros volumes avant decision
- ✅ **Réduction token consumption** critique (workloads à scale)
- ✅ **Latence multi-round-trips** problématique

### NE PAS utiliser PTC quand :
- ❌ Single tool call simple
- ❌ Tâche conversationnelle (chat)
- ❌ Jugement à chaque étape qui DOIT passer par le modèle (raisonnement chaîné contextuel)
- ❌ Sandbox 4.5 min insuffisant (containers expirent après inactivité)

## APPELS — Composants mobilisés

- [[comment-creer-agent]] — pattern sub-agent (alternative à PTC, voir comparaison ci-dessous)
- [[workflow-claude-code-optimal]] — où PTC s'inscrit dans le workflow global
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / PTC = code orchestration
- [[comment-creer-hook]] — hooks complémentaires (lint/security du code généré par Claude)

## Comparaison PTC vs Sub-agents (Justin Young 2-agent)

| Dimension | Sub-agents (Justin Young) | PTC |
|-----------|--------------------------|-----|
| Orchestration | LLM (initializer agent) | Code Python |
| Contrôle de flux | Prompts + tool calls | Code (loops, if, try/except) |
| Token contexte | Résultats sub-agents re-entrent contexte | Seul output final entre contexte |
| Latence | N round-trips inférence | 1 round-trip + sandbox exec |
| Quand préférer | Tâches nécessitant jugement à chaque étape | Orchestration déterministe + filtrage data |

**Complémentaires, pas concurrents** : sub-agents pour le jugement, PTC pour l'orchestration déterministe.

## ⚠️ Honnêteté intellectuelle — slug `/workflows`

Le tweet @_vmlops (23 mai 2026) annonce "Anthropic quietly shipped /workflows in Claude Code". **Vérification 23 mai 2026** :
- ❌ `code.claude.com/docs/en/workflows` retourne **404**
- ❌ WebSearch "claude code /workflows command" : 0 résultat sur slug officiel
- ✅ Le **principe** décrit dans le tweet (code orchestrator > LLM orchestrator) **est canonique** mais s'appelle **Programmatic Tool Calling (PTC)** côté docs Anthropic, pas `/workflows`

Le tweet @_vmlops est **single source externe** (DevOps Engineer, ~20k followers, pas équipe Anthropic). Selon la doctrine forge `[[feedback_anthropic_single_source]]` scopée, externes hors scope = 4+ sources requises. Le slug `/workflows` n'a pas 4 sources convergentes — c'est probablement une **paraphrase / interprétation libre** du concept PTC.

→ **Source canonique** = docs Anthropic PTC, pas le tweet. Le tweet est cité comme illustration externe du principe.

## ANTI-PATTERNS

### Doctrine
- ❌ **Citer "/workflows" comme verbatim Anthropic** — slug non vérifié, paraphrase tweet
- ❌ **Présenter PTC comme remplacement total des sub-agents** — complémentaires (jugement vs orchestration déterministe)
- ❌ **PTC pour single tool call** — overhead sandbox inutile

### Technique
- ❌ **`allowed_callers` manquant** sur tool definition → tool inaccessible depuis sandbox
- ❌ **Container >4.5 min inactif** → expire silencieusement
- ❌ **Code généré non testé en sandbox** AVANT production — strict sandboxing requis

## EXEMPLES CONCRETS

### Référence Anthropic
- [Docs officielles PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [Cookbook PTC](https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc)
- [Engineering blog Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

### Articles tiers (illustrations, pas sources primaires)
- [ikangai.com — Code as Action pattern](https://www.ikangai.com/code-as-action-the-pattern-behind-programmatic-tool-calling/)
- [ikangai.com — PTC Developer's Guide](https://www.ikangai.com/programmatic-tool-calling-with-claude-code-the-developers-guide-to-agent-scale-automation/)
- [techforproduct.com — What is PTC](https://blog.techforproduct.com/p/what-is-programmatic-tool-calling)

### Disponibilité
- Claude API ✅
- Claude Platform on AWS ✅
- Microsoft Foundry ✅
- LiteLLM support : [docs.litellm.ai PTC](https://docs.litellm.ai/docs/providers/anthropic_programmatic_tool_calling)

## SOURCES

### Primary (Anthropic, single source acceptable cf [[feedback_anthropic_single_source]])
- [platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use)

### Illustrations externes (citées avec disclaimer)
- Tweet @_vmlops 23 mai 2026 — popularisation du principe sous slug non-canonique "/workflows"

## GOTCHAS

- **Slug "/workflows" ≠ feature officielle** — c'est PTC. Slug @_vmlops non vérifié docs.
- **Container 4.5 min inactivité** — expire silencieusement
- **`allowed_callers` opt-in obligatoire** par tool
- **Strict sandboxing requis** (code généré exécuté)
- **`code_execution_20260120` tool type** — vérifier date version exacte selon date du projet

## ALIASES (9)

- programmatic tool calling
- PTC anthropic
- code orchestration anthropic
- code execution tool
- code as action pattern
- workflow.js claude code (paraphrase tweet)
- anthropic workflows shipped (paraphrase tweet)
- allowed_callers code execution
- claude python orchestrator

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-agent]] — sub-agents pattern (complémentaire à PTC)
- [[workflow-claude-code-optimal]] — workflow global
- [[mcp-vs-skills-doctrine]] — couches MCP/Skills/Bash + PTC
- [[methode-analyser-repo]] — quand recommander PTC dans une analyse

### Knowledge / refs liées
- [[feedback_anthropic_single_source]] — hiérarchie sources scopée
- [[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — pattern paraphrase non vérifiée

### Forge custom
- [[forge-brain-proactive]]

---

**Fin note canonique `programmatic-tool-calling.md`** — créée 23 mai 2026 suite tweet @_vmlops + audit doctrinal.
