---
titre: "LangMem — SDK mémoire long-terme LangChain/LangGraph"
resume: "LangMem (langchain-ai/langmem, MIT) ajoute la logique mémoire (extraction, consolidation, prompt optimization) par-dessus le BaseStore LangGraph ; différenciateur = mémoire procédurale ; figé en 0.0.30 depuis oct. 2025, lock-in LangGraph fort."
aliases:
  - "LangMem"
  - "langmem"
  - "LangMem SDK"
  - "mémoire LangGraph"
  - "LangChain memory SDK"
  - "prompt optimization LangMem"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://github.com/langchain-ai/langmem"
  - "https://langchain-ai.github.io/langmem/concepts/conceptual_guide/"
  - "https://langchain-ai.github.io/langmem/guides/optimize_memory_prompt/"
  - "https://pypi.org/project/langmem/"
  - "https://www.langchain.com/blog/langmem-sdk-launch"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Description

**LangMem** (`langchain-ai/langmem`, MIT) = SDK open-source de gestion de mémoire long-terme pour agents, par l'équipe LangChain. Il fournit la **logique** (extraction LLM, consolidation, optimisation de prompt) par-dessus la couche de stockage de LangGraph.

**Architecture en 3 couches** (vérifié doc) : LangGraph **Checkpointers** = mémoire court-terme/working ; LangGraph **`BaseStore`** = stockage long-terme cross-session (le « disque dur ») ; **LangMem SDK** = logique applicative posée dessus (le « gestionnaire de mémoire »).

> [!note] Statut (vérifié source primaire, juin 2026)
> PyPI **`0.0.30`, 27 oct. 2025**, MIT, Python ≥ 3.10. Numérotation **`0.0.x` = pré-stable**, jamais passé en 1.0, **« No releases published »** sur GitHub, README inachevé. ~1.5k ⭐ seulement. **Pas déprécié** — au contraire, depuis LangChain v1.0 (oct. 2025) il est (avec le checkpointer) le **remplaçant recommandé** des anciennes classes mémoire (`ConversationBufferMemory`…). Mais SDK de niche, figé depuis oct. 2025 → surveiller l'activité avant d'en dépendre en prod.

## Comment ça marche (technique)

**Trois types de mémoire** (calqués sur la cognition) :

| Type | Contenu | Stockage |
|---|---|---|
| **Semantic** | Faits / préférences | Profile (1 doc en place) ou Collection (N docs) |
| **Episodic** | Expériences passées (few-shot) | Collection (schémas custom) |
| **Procedural** | Comportement de l'agent | Prompt ou Collection |

**Hot path vs background** (distinction centrale) : *conscious/hot path* = l'agent appelle des tools mémoire dans sa boucle (ajoute de la latence, pour mises à jour critiques temps réel) ; *subconscious/background* = réflexion LLM post-conversation (aucune latence, meilleur recall — **mode recommandé par défaut**).

**Prompt optimization = mémoire procédurale** (le différenciateur unique, absent de mem0) : réécrit automatiquement les **instructions système** de l'agent depuis les logs + feedback. Entrée = trajectoires `(conversation, annotation)`. Trois algos : `prompt_memory` (1 appel LLM, le moins cher), `metaprompt` (réflexion), `gradient` (2–10 appels, sépare critique et application, le plus qualitatif/coûteux).

**API** :
- Core stateless : `create_memory_manager`, `create_prompt_optimizer` / `create_multi_prompt_optimizer`.
- Stateful (adossé LangGraph) : `create_memory_store_manager`, + tools `create_manage_memory_tool` / `create_search_memory_tool` exposés à l'agent.
- Store : `InMemoryStore(index={"dims":1536,"embed":"openai:text-embedding-3-small"})` en dev, `AsyncPostgresStore` en prod.
- **Namespaces hiérarchiques** : ex. `("acme_corp", "{user_id}", "code_assistant")`, `{user_id}` résolu au runtime.
- Modèles agnostiques (format `provider:model`, ex. `anthropic:claude-3-5-sonnet-latest`).

## Quand utiliser

**Choisir LangMem si** : déjà sur LangChain/LangGraph (dépendance nulle, la mémoire est dans la stack) ; besoin de **mémoire procédurale** (agent qui réécrit ses propres instructions) — fonctionnalité unique.

**Éviter / préférer une alternative si stack agnostique** :
- **Lock-in maximal** : adopter LangMem = adopter LangGraph, usage standalone impraticable.
- **[[memoire-agent-mem0|mem0]]** : API REST drop-in, multi-stack, hosting managé, compliance large. Couplage écosystème le plus faible.
- **Zep / Graphiti** : raisonnement temporel + graphe natif, P95 ~300 ms sans appel LLM au query-time.
- LangMem n'a **pas** : raisonnement temporel, graphe natif, hosting managé.

> [!caution] Claim rapporté NON vérifié
> Plusieurs sources secondaires citent une latence **p95 de 59,82 s sur LOCOMO** pour LangMem (le présentant comme inadapté au temps réel) — **non confirmé en source primaire**, et contredit par un autre comparatif. Le principe documenté reste vrai : l'extraction LLM est coûteuse → privilégier le mode background.

## Optimisation

- **Background par défaut** ; réserver le hot path (tools) aux mises à jour réellement critiques.
- Modèle d'extraction moins cher que l'agent principal ; `prompt_memory` (1 appel) sauf besoin de qualité (`gradient`).
- Toujours un `{user_id}` dans le namespace (anti cross-user bleed).
- Semantic : Profile (état courant) vs Collection (connaissance non bornée, plus coûteuse).
- Pièges : lock-in LangGraph, churn d'API LangChain historique (v0.1→v0.3, rapporté), pas de hosting managé (Postgres/pgvector recommandé en prod).

## Liens

- [[memoire-agent-mem0]] — alternative agnostique, comparatif direct
- [[agents-architecture]] — modèle mémoire short/long/episodic/procedural
- [[stack-python-ia]] — tableau Memory frameworks (LangGraph Store)
- [[stack-typescript-ia]]
- [[MOC-Techniques]]
