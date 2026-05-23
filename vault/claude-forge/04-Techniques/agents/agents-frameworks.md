---
titre: "Agents Frameworks — Comparatif 2026"
resume: "Comparatif complet frameworks agents IA 2026 : LangGraph, CrewAI, AutoGen, Claude SDK, OpenAI SDK, Google ADK, Pydantic AI, no-code"
aliases:
  - agent frameworks
  - frameworks agents
  - LangGraph vs CrewAI
  - AI agent tools
  - agent SDK
  - outils agents IA
domaine: ia
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026"
  - "https://gurusup.com/blog/best-multi-agent-frameworks-2026"
  - "https://langchain-ai.github.io/langgraph/"
  - "https://docs.crewai.com/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Tier 1 — Production enterprise

### LangGraph (LangChain)
Graphe dirige avec edges conditionnels, checkpointing integre, time-travel debugging, HITL (`interrupt`). ~25K+ GitHub stars (la suite LangChain cumule >1B downloads). Adoption enterprise forte (Klarna, LinkedIn, Uber documentes). LangSmith $39-500/mois.
- **Quand** : workflows complexes avec HITL, industries regulees (finance, sante)
- **Limites** : learning curve (concepts graphe, state schemas)

### Claude Agent SDK (Anthropic)
Le SDK **s'execute dans votre propre process** (verbatim docs : "runs inside your own process"), subagents natifs. Python-first, TypeScript dispo.
- **Managed Agents** (sandbox heberge, toolset integre — tarif horaire +tokens a confirmer pricing officiel)
- **Dreams** (auto-curation memoire entre sessions, Research Preview, beta header `dreaming-2026-04-21`)
- **Agent Teams** : agents independants, communication directe, task list partagee

## Tier 2 — Production capable

### CrewAI
Role-based crews, ~20 lignes pour demarrer. **~50K+ GitHub stars** (mai 2026), 2 milliards d'executions, $18M Series A. Flows pour event-driven.
- **Quand** : prototypage rapide, workflow business
- **Limites** : pas de checkpointing. Migration courante vers LangGraph en production
- ⚠️ Single source : "+18% token overhead vs LangGraph" cite par blog migration 3-agent (contexte limite, ne pas generaliser)

### Pydantic AI — Dark horse
Type-safe, FastAPI-style DX, OpenTelemetry. **17.2K+ stars, v1.102 (22 mai 2026)**. Capabilities et AgentSpec.
- **Quand** : equipes Python valorisant type contracts et testing
- Consensus communautaire : "LangGraph pour complexite, CrewAI pour vitesse, Pydantic AI pour stabilite"

## Tier 3 — Platform-specific

### OpenAI Agents SDK
Handoffs explicites, memory configurable, MCP support, TypeScript SDK. Successeur de Swarm.
- **Limites** : model-locked OpenAI — pas de BYOM

### Google ADK v1.0
Code-first, model-agnostic (optimise Gemini), multi-langage (Python, Go, Java, TS). A2A natif (v1.0 publiee 12 mars 2026).
- **Quand** : Google Cloud, interoperabilite cross-platform via A2A

### Microsoft Agent Framework 1.0
Unifie Semantic Kernel + AutoGen (annonce officielle Microsoft). .NET et Python LTS. AutoGen et SK sur trajectoire de maintenance suite au merge (statut precis a verifier docs Microsoft).

## Adoption production en baisse

### AutoGen / AG2
Adoption production en baisse apres le split Microsoft → Microsoft Agent Framework. Le pattern GroupChat (debat multi-agent partage) reste unique et utilise en recherche/prototypage. Zero mecanisme securite natif. Boucles de conversation = cout explosif si `max_round` mal configure (single source : un blog evoque ~3.5x overhead generique multi-agent ; ne pas citer "5-6x" sans source consolidee).

## Open-source builders

| Plateforme | Stars | Specialite |
|-----------|-------|-----------|
| **Dify** | 142K+ | Full LLM platform, multi-team |
| **n8n** | Large | 8000+ integrations, AI = un step workflow |
| **Flowise** | Large | Drag-and-drop LangChain, le plus leger |
| **LangFlow** | 100K+ | Code Python modifiable, DataStax |
| **Botpress** | — | Conversational, 10+ channels, SOC 2 |

Pattern populaire : **Dify + n8n** (Dify = LLM logic, n8n = triggers business).

## No-code / Low-code

| Plateforme | Prix | Specialite |
|-----------|------|-----------|
| Relevance AI | $0-234/mo | Sales/Marketing, multi-agent |
| Wordware | — | Natural language as code |
| Dust.tt | — | Enterprise, 50+ integrations, governance |
| Lindy AI | $0-199/mo | 5000+ integrations, Computer Use |
| Zapier AI | Task-based | 8000+ apps, ecosysteme imbattable |

## Couts comparatifs (qualitatifs)

Les chiffres precis par tache (ex "$0.08/tache leader cout") qui circulaient dans les versions anterieures de cette note **ont ete retires** (audit 23 mai : C5.9 = fabriquee + inversion qualitative ; Rasa CALM moins cher selon leur etude). Pour les ordres de grandeur fiables :

- LLM tokens dominent les couts framework (le framework ajoute peu vs le LLM)
- **Prompt caching** Anthropic : jusqu'a 90% reduction cache hit
- **Caching + batching combine** : Anthropic dit "jusqu'a 95% reduction" vs standard
- **Open-source** : economies framework, mais surcout setup et ops a mesurer
- 100K agent runs/mois avec sandbox manage : 4 chiffres (LLM + sandbox + ops) — calculer empiriquement, pas de chiffre canonique forge

> [!note] Audit 23 mai 2026
> Plusieurs metriques framework cites avant cette date etaient fabriques : "$0.08/tache" (C5.9), "LangGraph 34% citations enterprise" (confusion 34.5M PyPI downloads), "AutoGen 5-6x" (non sourcable). Voir [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]].

## Liens

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-architecture]] — Patterns d'architecture
- [[Harrison Chase]] — LangGraph, Deep Agents
- [[Joao Moura]] — CrewAI
- [[architecture-langgraph]] — Implementation LangGraph
- [[architecture-crewai]] — Implementation CrewAI
- [[architecture-autogen]] — AutoGen/AG2
