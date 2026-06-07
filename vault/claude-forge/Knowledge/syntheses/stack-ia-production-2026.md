---
titre: "Stack IA en production 2026 — synthèse transverse & carte des canoniques"
resume: "Synthèse de l'audit Stack IA 2026 : le consensus des labs frontière (Anthropic, OpenAI, Cognition) a convergé sur 'commencez simple, ajoutez la complexité quand les evals le prouvent'. Le moat = evals + context engineering, pas le framework ni le modèle. Multi-agent justifié pour la lecture parallélisable, pas l'écriture. Carte vers les notes canoniques enrichies."
aliases:
  - stack IA production 2026
  - état de l'art stack IA
  - audit stack IA 2026
  - simple workflows multi-agent
  - evals new unit tests
  - read vs write multi-agent
  - context engineering moat
domaine: ia
type: synthese
derniere-maj: 2026-06-07
auteur: claude
sources:
  - "Synthèse forge interne — audit ingénieur Stack IA 2026 (capitalisée intégralement dans le vault, doc source archivé)"
  - "https://www.anthropic.com/research/building-effective-agents (Building Effective Agents)"
  - "OpenAI A Practical Guide to Building Agents"
  - "Cognition — Don't Build Multi-Agents"
tags:
  - "#type/synthese"
  - "#domaine/ia"
  - "#domaine/agents"
  - "#domaine/rag"
---

# Stack IA en production 2026 — synthèse transverse & carte des canoniques

> [!info] Rôle de cette note
> Note-carte de synthèse. Elle porte les **3 thèses transverses** de l'audit Stack IA 2026 et **relie** les notes canoniques qui détaillent chaque volet. Le détail vit dans les canoniques — ici, la vue d'ensemble + les pointeurs. Capitalise une synthèse forge interne (audit ingénieur Stack IA 2026), désormais intégralement dans le vault — le doc source a été archivé après dispatch.

> [!warning] Statut épistémique
> Le rapport source distingue explicitement « vérifié » (la déclaration publique existe) de la véracité empirique. Beaucoup de chiffres sont des **estimations d'enquête** (Menlo ~500 répondants, LangChain 1340) ou des **claims vendeurs non reproduits** (« 4x faster », gains internes Ramp/Cursor). Les notes filles préservent ces marqueurs. Cf [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — historique de contamination par chiffres non vérifiés.

## Thèse 1 — Commencez simple, complexifiez sur preuve d'evals

Le consensus des labs frontière a convergé, **sous des titres opposés** :
- Anthropic — *Building Effective Agents*
- OpenAI — *A Practical Guide to Building Agents*
- Cognition — *Don't Build Multi-Agents*

…disent la même chose : **maximisez d'abord un agent unique** (un LLM + outils dans une boucle), ajoutez la complexité — workflows puis multi-agents — **seulement quand les evals le prouvent**.

Verbatim Anthropic (existence vérifiée) :
> « When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. »

**Distinction canonique** : *workflows* (LLM + outils orchestrés par du code prédéfini) vs *agents* (le LLM dirige dynamiquement son propre processus). Les frameworks « add layers of abstraction » qui compliquent le debug.

→ Détail : [[agents-architecture]] (patterns), [[agents-frameworks]] (comparatif), [[programmatic-tool-calling]] (code orchestre / modèle juge).

## Thèse 2 — Le multi-agent se tranche par « read vs write »

Anthropic : son système de recherche multi-agent (Opus 4 lead + sous-agents Sonnet 4) a battu un agent unique Opus 4 de **90,2%** sur son éval interne — au prix de ~15× les tokens d'un chat.

Cognition (*Don't Build Multi-Agents*) a contre-argumenté : les sous-agents parallèles font des **choix implicites conflictuels** (exemple Flappy Bird : un sous-agent construit un fond Super Mario, un autre un oiseau hors-style, l'agent final doit réconcilier deux malentendus).

En 2026, Cognition a nuancé : « we've begun to deploy multi-agent systems that actually work… setups where multiple agents contribute intelligence to a task **while writes stay single-threaded**. »

> [!tip] Verdict canonique
> **Parallélisez la lecture/recherche (read-heavy), gardez l'écriture mono-threadée (write-heavy, ex. coding).** Le contexte partagé est critique en write.

→ Détail : [[agents-architecture]] section Multi-agent + [[decoupe-agents-anti-crash]] + [[limites-subagents-claude-code]].

## Thèse 3 — Le moat = evals + context engineering

« **Evals are the new unit tests** » : la TDD naïve échoue (pas de sortie déterministe unique). Le **golden dataset** annoté à la main et versionné en git est l'artefact le plus précieux.

Le « prompt engineering » a cédé la place au « **context engineering** » (curation du budget de tokens) comme compétence centrale.

Le moat n'est **ni le framework ni le modèle** : c'est la **discipline d'evals + le context engineering**.

→ Détail : [[agents-evaluation]] (benchmarks, scorers 60/30/10), [[rag-evaluation]] (RAGAS), [[agents-architecture]] section Context Engineering, [[economie-agentique-pricing-2026]] (le moat côté business : data + evals propriétaires).

## Carte des volets → canoniques

| Volet du rapport | Note canonique | Statut |
|---|---|---|
| Langages & frameworks orchestration | [[agents-frameworks]], [[stack-typescript-ia]], [[stack-python-ia]] | Enrichi (datations 2026) |
| RAG (Contextual Retrieval, GraphRAG, vector DBs) | [[rag-chunking]], [[rag-architecture]], [[rag-reranking]], [[RAG]] | Déjà complet (Contextual Retrieval mot pour mot) |
| Agents & orchestration | [[agents-architecture]] | Enrichi (read/write, leçons Anthropic) |
| Model layer — entraînement maison & optim | [[stack-typescript-ia]], [[agents-frameworks]] | Enrichi (Cursor Composer 2/2.5) |
| Inférence serving (vLLM, SGLang, TensorRT-LLM, TGI maintenance) | [[stack-python-ia]], [[fine-tuning-infrastructure]] | Déjà couvert (TGI archivé 21 mars 2026 capitalisé) |
| Évaluation & observabilité | [[agents-evaluation]] | Enrichi (LangChain State 2025, scorers) |
| Infra & sécurité (OWASP, lethal trifecta, MCP CVE) | [[agents-securite]], [[tool-retrieval-query-expansion]] | Enrichi (réconciliation MCP servers) |
| Stratégie & org (build/buy, pricing, Klarna/Ramp/Harvey) | [[economie-agentique-pricing-2026]] | **Créé** |
| Économie agentique (tokens, marges) | [[economie-agentique-pricing-2026]] | **Créé** |

## Recommandations — les 5 étapes (verbatim rapport)

1. **Commencez minimal** : un LLM + tool calling dans une boucle, APIs directes. Baseline avec le modèle le plus capable. *Seuil :* logique conditionnelle explose, ou > 10-15 outils se chevauchent.
2. **Instrumentez avant d'optimiser** : tracing + golden dataset 50-200 cas en git + scorers 60/30/10 (déterministe/LLM-judge/humain) + gate de régression CI.
3. **RAG seulement si nécessaire** : corpus < 200k tokens → long-context + prompt caching, pas de RAG. Sinon hybrid search + Contextual Retrieval + reranking (top-150 → top-20).
4. **Context engineering avant multi-agent** : compaction, just-in-time retrieval, bornage tool responses, code execution with MCP (gain ~98% tokens). Multi-agent **seulement** pour la lecture parallélisable.
5. **Coût & sécurité (continu)** : prompt caching, model routing, batch APIs, kill switches/spend ceilings, défense prompt-injection (least privilege, HITL, audit MCP via mcp-scan).

## Caveats structurants (à garder en tête)

- **Lab guidance ≠ pratique réelle** : les labs RECOMMANDENT la simplicité mais déploient eux-mêmes du multi-agent complexe (Anthropic Research) et des modèles maison (Cursor). C'est **la divergence la plus importante**.
- **Chiffres d'adoption = estimations d'enquête**, non audités (biais d'auto-sélection).
- **Le champ bouge au trimestre** : versions modèles/frameworks/prix. Vérifier les specs courantes avant toute décision d'archi.
- **MCP : adoption massive mais sécurité immature** — traiter tout serveur MCP tiers comme du code non fiable.

## Liens

- Synthèse forge interne « audit ingénieur Stack IA 2026 » — rapport source, dispatché intégralement dans le vault puis archivé (7 juin 2026)
- [[MOC-Techniques]]
- [[techniques-inedites]] — croisements de techniques
- [[economie-agentique-pricing-2026]] — volet économique/stratégique
- [[harness-engineering]] — l'infra compte autant que le modèle
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — discipline anti-contamination
