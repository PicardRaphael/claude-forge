---
titre: "5 outils IA juin 2026 — mémoire, vector DB, RAG entreprise, gouvernance contexte"
resume: "Index d'orientation pour 5 outils de catégories différentes (mem0, LangMem, Pinecone, Onyx, Packmind) : à quoi sert chacun, quand le choisir, lien vers la note détaillée. PAS un comparatif tête-à-tête (catégories non comparables)."
aliases:
  - "outils mémoire RAG gouvernance 2026"
  - "mem0 vs LangMem vs Pinecone"
  - "index outils IA juin 2026"
  - "mem0 LangMem Onyx Pinecone Packmind"
  - "comparatif outils agents 2026"
domaine: ia
type: index
derniere-maj: 2026-06-17
auteur: claude
tags:
  - "#type/index"
  - "#domaine/ia"
  - "#domaine/agents"
  - "#domaine/rag"
---

# 5 outils — orientation par catégorie

> Vue marché plus large (5 catégories : voix, briques produit, productivité, infra, plateformes) → [[MOC-paysage-outils-ia-marche-2026]].

> [!info] Pourquoi pas un tableau comparatif
> Ces 5 outils recouvrent **3 catégories non comparables** : mémoire d'agent (mem0, LangMem) ≠ vector DB / RAG (Pinecone, Onyx) ≠ gouvernance de contexte pour agents de code (Packmind). Un versus tête-à-tête serait apples-to-oranges. Cet index oriente : **à quoi sert chacun + quand le choisir + note détaillée**. Recherche de juin 2026, sources primaires distinguées du rapporté dans chaque note.

## A. Mémoire d'agent (cross-session)

| Outil | À quoi ça sert | Choisir si… |
|---|---|---|
| [[memoire-agent-mem0]] | Couche mémoire **universelle agnostique** : extrait/consolide/récupère les faits saillants des conversations, cross-session, multi-user | Stack **agnostique**, hosting managé voulu, isolation multi-tenant (`user_id`). ⚠️ v3 (avril 2026) : OSS n'a plus de graphe traversable (entity-linking spaCy) ; la Platform garde le graphe |
| [[memoire-agent-langmem]] | SDK mémoire **LangChain-native** ; unique : **mémoire procédurale** (réécrit le prompt système de l'agent) | Déjà sur **LangChain/LangGraph**, ou besoin d'un agent qui s'auto-améliore via prompt optimization. Lock-in LangGraph fort, SDK figé en 0.0.30 |

Autres acteurs cités (pas de note dédiée) : **Zep/Graphiti** (graphe temporel, P95 ~300 ms sans LLM au query-time), **Letta/MemGPT** (self-editing memory).

## B. Vector DB & RAG entreprise

| Outil | À quoi ça sert | Choisir si… |
|---|---|---|
| [[pinecone-vector-database]] | **Vector DB managée serverless** (propriétaire, pas de self-host) : zéro-ops, pricing RU/WU, Inference + Assistant intégrés | Production scalable sans gérer d'infra, time-to-market. **Pas** si volume faible (pgvector/Qdrant) ou budget serré (factures imprévisibles). Comparatif inter-DB → [[rag-vector-databases]] |
| [[onyx-enterprise-search]] | **Plateforme RAG/recherche entreprise** open-source : assistant connecté à 50-60+ sources avec sync ACL natif | Recherche unifiée du knowledge interne + **self-host/souveraineté**. **Pas** si RAG mono-source sur-mesure (stack lourde : Postgres+OpenSearch+Redis+MinIO+Celery). ⚠️ v4.0 (mai 2026) : Vespa → OpenSearch |

## C. Gouvernance de contexte pour agents de code

| Outil | À quoi ça sert | Choisir si… |
|---|---|---|
| [[packmind-context-governance]] | Capture les **standards de code** d'une équipe et les rend en CLAUDE.md/.cursor/rules/AGENTS.md depuis une **source unique**, + versioning + détection de drift | Entreprise multi-équipes/multi-repos avec ≥ 2 agents de code et besoin d'audit. **Pas** si 1 dev + 1 repo (CLAUDE.md à la main suffit — Packmind l'admet) |

> [!tip] Croisement forge (Packmind)
> Packmind industrialise exactement la propagation single-source → multi-agent + versioning + drift que la forge fait à la main entre ia_back/neo_ia/neoteem-back-ts (cf rule `cross-repo-propagation.md`). À surveiller si la propagation manuelle devient un goulot.

## Liens

- [[memoire-agent-mem0]] · [[memoire-agent-langmem]] · [[pinecone-vector-database]] · [[onyx-enterprise-search]] · [[packmind-context-governance]]
- [[agents-architecture]] — modèle mémoire short/long/episodic/procedural
- [[rag-vector-databases]] — comparatif inter-vector-DB
- [[MOC-Techniques]]
