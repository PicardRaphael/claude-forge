---
titre: "Prompt caching & KV-cache — mécanique exacte et relocation trick"
resume: "Mécanique du prompt caching Anthropic/OpenAI/Gemini (multiplicateurs de prix, ordre tools→system→messages, breakpoints) et du KV-cache côté serving ; le relocation trick pour maximiser le hit rate des agents"
aliases:
  - prompt caching
  - cache_control ephemeral
  - relocation trick
  - KV cache reuse
  - cache hit rate agents
  - prompt caching multiplicateurs
domaine: ia
type: technique
derniere-maj: 2026-06-07
auteur: claude
sources:
  - "https://platform.claude.com/docs/build-with-claude/prompt-caching"
  - "https://projectdiscovery.io/blog/how-we-cut-llm-costs"
  - "[[reference-technique-stack-ia]]"
tags:
  - "#type/technique"
  - "#domaine/ia"
---

## Description

Le caching de prompt + réutilisation du KV-cache est **le levier coût/latence le plus rentable** en production LLM. Distinct de la doctrine d'usage générale ([[Context Management]], [[architecture-claude-api]] : -90 % sur cache hit) : cette note porte la **mécanique exacte** et le pattern d'optimisation. Référence sourcée : [[reference-technique-stack-ia]] §1.

## Anthropic — mécanique exacte (VÉRIFIÉ-SOURCE platform.claude.com)

- On marque les blocs avec `cache_control: {"type": "ephemeral"}`. Le cache couvre le préfixe **dans l'ordre tools → system → messages**, jusqu'au dernier bloc marqué inclus. Toute modification à un niveau invalide ce niveau et tous les suivants.
- **Multiplicateurs de prix** : écriture cache 5 min = **1,25×** le prix d'entrée de base ; écriture 1 h = **2,0×** ; lecture = **0,1×** (-90 %). → rentable après **une seule lecture** (TTL 5 min) ou **deux lectures** (TTL 1 h).
- **Minimum cachable** : 1 024 tokens (Sonnet/Haiku récents), 4 096 (gros modèles). En dessous, traité sans cache, sans erreur.
- Jusqu'à **4 breakpoints** `cache_control` par requête. Monitoring `usage` : `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`. Le TTL se rafraîchit à chaque hit sans coût supplémentaire.
- **Auto-caching** : Anthropic place les breakpoints sans marqueurs, mais ignore quels segments sont stables vs dynamiques → du contenu runtime au milieu du prompt provoque des misses. **Le contrôle explicite + TTL 1 h reste nécessaire pour les agents.**

## Le « relocation trick » (VÉRIFIÉ-SOURCE ProjectDiscovery)

Déplacer le contenu dynamique **hors du préfixe cachable** : hit rate 7 % → 74 %, puis 84 % avec breakpoints explicites + TTL délibérés. **Économie réelle dérivée du spend : 59 % → 66 % → 70 %** (sur 10 derniers jours).

> Règle : « if your agents run more than 3-5 steps, you're leaving significant money on the table ».

Ordre de structuration (du plus stable au moins stable) : instructions système → définitions d'outils → documents de référence/contexte de session → message utilisateur (jamais caché).

## OpenAI / Gemini

- **OpenAI** (RAPPORTÉ docs) : caching automatique par préfixe (prompts ≥ 1 024 tokens), **sans pénalité d'écriture**, remise lecture **50 %** (vs 90 % Anthropic). Param `prompt_cache_key` pour mieux router les hits. Stratégie purement structurelle : garder le contenu identique en début de requête.
- **Gemini** (RAPPORTÉ Helicone) : modèle multiplicateur + coût de stockage (par MTok/heure), lecture ≈0,25× le prix d'entrée. Vérifier la doc Google avant de chiffrer.

## KV-cache côté serving

Réutilisation côté serveur (distinct du caching API) — détail dans [[serving-inference-optimisation]] :
- Coût KV par token et par couche : `2 × num_kv_heads × head_dim × dtype_bytes` (facteur 2 = K et V).
- À l'échelle : DeepSeek-V3 (Open-Infra, fév. 2025) — sur 24 h, 342B/608B tokens d'entrée (56,3 %) ont touché le KV-cache disque côté serveur.

## Code execution avec MCP / « Code Mode »

Pattern token connexe (VÉRIFIÉ-SOURCE Anthropic « Code execution with MCP », Cloudflare « Code Mode ») — voir aussi [[programmatic-tool-calling]] :
- Exposer les serveurs MCP comme une API de code (l'agent lit/filtre les données AVANT qu'elles entrent dans le contexte) : Google Drive → Salesforce **150 000 → 2 000 tokens (-98,7 %)**.
- Cloudflare : 2 500+ endpoints via `search()` + `execute()` ≈ 1 000 tokens (vs 1,17M en flat-tool, -99,9 %), code exécuté en isolate V8, secrets injectés au transport.
- **Seuil** : activer dès que les définitions d'outils dépassent ~10-20 % de la fenêtre.

## Semantic caching

GPTCache : cache de réponses indexé par **similarité d'embedding** de la requête (vs match exact). Cf [[rag-production]] (cache sémantique, seuil cosine ~0,80, -68,8 % appels LLM).

## Liens

- [[reference-technique-stack-ia]] — référence exhaustive §1
- [[serving-inference-optimisation]] — KV-cache serveur, PagedAttention/RadixAttention
- [[Context Management]] — doctrine d'usage du caching (compaction, context editing)
- [[architecture-claude-api]] — caching + batching combinés
- [[programmatic-tool-calling]] — orchestrer les outils via code
- [[MOC-Techniques]]
