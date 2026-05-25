---
aliases:
  - technique-ia
  - lead-technique-ia
  - hub-technique
  - RAG-agents-MLOps-pour-Lead-IA
  - praticien-Lead-IA
  - carte-tech-Lead-IA
resume: Carte d'orientation Lead IA Neoteem pointant vers les 100+ notes techniques existantes du vault forge-brain (RAG, agents, MLOps, prompt engineering, fine-tuning).
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/technique-ia"
---

# Technique IA — carte d'orientation Lead IA Neoteem

> **Cette note ne contient PAS de savoir technique.** Elle pointe vers les 100+ notes techniques déjà capitalisées dans `vault/claude-forge/04-Techniques/`. Single source of truth — pas de duplication.

## Posture du Lead IA praticien

Risque #1 du Responsable IA : devenir "PowerPoint manager" en 18 mois.

Antidote : continuer à lire et expérimenter techniquement. Cette carte te dit OÙ chercher quand tu prépares :
- une décision technique (build vs buy, modèle, architecture)
- un brief technique pour ton équipe
- un cadrage stratégique CODIR sur un sujet technique
- un script de réunion client B2B avec questions techniques

## RAG — 13 notes existantes

Pour tout ce qui concerne **NeoChat / NeoDocs / recherche sur baux / fiches mandats** :

- [[RAG]] — MOC racine (point d'entrée)
- [[rag-architecture]] — pipeline canonique chunking → embedder → vector store → retriever → reranker → generator
- [[rag-chunking]] — stratégies de découpage (taille, overlap, sémantique)
- [[rag-embeddings]] — choix embedder (multilingue FR, dimensions, coût)
- [[jina-embeddings-v4]] — embedder récent state-of-art
- [[rag-vector-databases]] — pgvector vs Qdrant vs Milvus vs Pinecone
- [[rag-reranking]] — BGE, Cohere, cross-encoder
- [[rag-evaluation]] — RAGAS, DeepEval, LLM-as-judge, faithfulness, answer relevancy
- [[rag-metadata]] — filtres hybrides date + métadonnée + vector
- [[rag-production]] — patterns scale, monitoring drift, qualité embeddings à l'échelle
- [[ColPali]] — RAG sur PDF avec vision
- [[sqlite-fts5-vault]] — alternative FTS5 pour petits corpus
- [[tool-retrieval-query-expansion]] — patterns retrieval tools pour agents

**Pour Neoteem NeoChat** : commencer par [[rag-architecture]] + [[rag-evaluation]] + [[rag-production]].

## Agents — 15 notes existantes

Pour tout ce qui concerne **agents autonomes Loji, MCP, multi-tool** :

- [[Agents IA]] — MOC racine
- [[agents-architecture]] — patterns ReAct, multi-agent, orchestration, memory, tool use, **MCP**, A2A, planning
- [[agents-frameworks]] — comparatif LangGraph / CrewAI / AutoGen / Claude SDK / OpenAI SDK / Google ADK / Pydantic AI
- [[agents-evaluation]] — benchmarks SWE-bench, GAIA, WebArena, TAU-bench
- [[agents-securite]] — OWASP top 10 agentic, prompt injection, sandboxing, dual-LLM, guardrails
- [[agents-automation]] — workflows production, n8n, Zapier, CI/CD, scheduling, Computer Use, browser agents
- [[harness-engineering]] — discipline 2026 Birgitta Bockeler : tout ce qui entoure le modèle (state, tools, feedback loops)
- [[decoupe-agents-anti-crash]] — anti-pattern scope trop large
- [[prompt-armor]] — sécurité prompts
- [[prompt-rewriter-pattern]] — pattern réécriture
- [[subagent-explore-then-edit]] — pattern Anthropic
- [[technique-dreaming-cross-session]] — pattern avancé
- [[technique-shared-agent-memory]] — pattern partage état
- [[limites-subagents-claude-code]] — limites pratiques Claude Code
- [[mass-multi-agent-system-search]] — scale multi-agent

**Pour Neoteem agents Loji** : commencer par [[agents-architecture]] + [[agents-securite]] + [[agents-evaluation]].

## Architecture chatbot — 11 notes

Pour le **design global d'un produit conversationnel comme NeoChat** :

- [[index-architectures]] — MOC architectures chatbot
- [[architecture-claude-api]] — patterns avec API Anthropic
- [[architecture-openai-api]] — patterns OpenAI
- [[architecture-gemini-api]] — patterns Gemini (utilisé dans Loji GEMINI)
- [[architecture-langgraph]] — orchestration LangGraph
- [[architecture-crewai]] — multi-agent CrewAI
- [[architecture-autogen]] — multi-agent AutoGen
- [[pattern-orchestrateur]] — pattern central orchestrateur
- [[pattern-pipeline]] — pattern séquentiel
- [[pattern-single-agent-multi-tool]] — recommandé pour NeoChat début
- [[pattern-swarm]] — pattern OpenAI Swarm

## Prompt engineering — 11 notes

Pour le **prompt engineering avancé sur Claude/GPT/Gemini** :

- [[Adaptive Thinking]] — extended thinking
- [[Effort Levels Guide]] — high/xhigh/max effort
- [[opus-47-design-defaults]] — défaut Opus 4.7
- [[prompting-opus47-cheatsheet]] — cheatsheet Opus 4.7
- [[prompting-chat-cowork-code]] — différences contextes
- [[forge-prompt-machine]] — pattern interne forge
- [[amanda-askell-prompt-engineering]] — école Amanda Askell Anthropic
- [[outcome-first-prompting]] — outcome > process
- [[over-specification-paradox]] — anti-pattern sur-spec
- [[System Prompt Design]] — design system prompts
- [[deprecated-techniques-2026]] — ce qui ne marche plus

## Fine-tuning — 10 notes

Pour la **décision fine-tuning vs RAG** et l'exécution :

- [[MOC-Fine-Tuning]] — MOC racine
- [[rag-vs-fine-tuning]] — décision matrix (**à lire en priorité**)
- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, PEFT
- [[fine-tuning-models]] — quels modèles fine-tuner
- [[fine-tuning-datasets]] — préparer datasets
- [[fine-tuning-evaluation]] — eval avant/après
- [[fine-tuning-frameworks]] — Hugging Face, Mistral, Together
- [[fine-tuning-infrastructure]] — compute, GPU
- [[fine-tuning-alignment]] — RLHF, DPO
- [[fine-tuning-privacy]] — données sensibles

**Verdict Neoteem 2026** : RAG + bon prompt engineering suffit pour 95% des cas. Fine-tuning si volume >100k req/mois ET style/tone récurrent ET data labellisée.

## Context engineering — 2 notes

- [[Context Engineering]] — concept canonique
- [[Context Management]] — gestion contexte long

## Stacks tech IA — 2 notes

- [[stack-python-ia]] — stack Python IA Neoteem (ia_back, neo_ia)
- [[stack-typescript-ia]] — stack TS IA Neoteem (back2.0 Bun/Hono/Drizzle)

## Patterns transverses (20+ notes)

Pour les **patterns architecturaux et méthodologiques** :

- [[architecture-cerveau-obsidian-mcp]] — pattern brain vault + MCP (cf neoteem-brain)
- [[mcp-vault-llm-design]] — design MCP vault LLM-friendly
- [[mcp-paths-relatifs-portabilite]] — bonnes pratiques MCP
- [[pattern-vault-query-guard]] — guard sur queries vault
- [[pattern-fts5-aliases-vs-embeddings]] — FTS5 vs embeddings
- [[pattern-figma-mcp-claude-code]] — Figma + MCP + CC
- [[pattern-github-spec-kit]] — GitHub spec kit
- [[pattern-spec-driven-development]] — SDD
- [[pattern-sdd-triangle]] — triangle SDD
- [[pattern-spec-skill-deployment]] — déploiement spec/skill
- [[pattern-gsd-framework]] — Get Stuff Done
- [[pattern-behavioral-dispatch-test]] — test comportemental
- [[audit-claude-folder-pattern]] — audit `.claude/`
- [[audit-puis-vagues-paralleles]] — audit + 3 vagues parallèles
- [[quartet-analyse-multi-repo]] — quartet analyse repo
- [[codebase-maps-pattern]] — cartographier codebase
- [[config-guardian-pattern]] — config guardian
- [[running-implementation-notes]] — notes implémentation continues
- [[LLM Wiki]] — pattern Karpathy LLM Wiki
- [[Silent Assumptions]] — silent assumptions

## Quand chercher quoi (orientation rapide)

| Situation Lead IA Neoteem | Notes à lire d'abord |
|---|---|
| Design RAG pour NeoChat | [[rag-architecture]] + [[rag-production]] + [[rag-evaluation]] |
| Choix vector DB | [[rag-vector-databases]] |
| Design agent NeoChat avec tools | [[agents-architecture]] + [[pattern-single-agent-multi-tool]] |
| Sécuriser agent contre prompt injection | [[agents-securite]] + [[prompt-armor]] |
| Décider fine-tuning vs RAG | [[rag-vs-fine-tuning]] |
| Évaluer un système IA en prod | [[rag-evaluation]] OU [[agents-evaluation]] selon cas |
| Choisir framework agent | [[agents-frameworks]] |
| Prompt engineering avancé | [[Adaptive Thinking]] + [[Effort Levels Guide]] |
| Choisir modèle (Claude/GPT/Gemini/Mistral) | [[stack-typescript-ia]] + benchmarks dans MOCs |
| Stack technique back2.0 Loji | [[stack-typescript-ia]] |
| Stack technique ia_back/neo_ia | [[stack-python-ia]] |
| Configurer MCP | [[mcp-vault-llm-design]] + [[mcp-paths-relatifs-portabilite]] |

## Notes complémentaires (NON dans 04-Techniques)

Si tu veux des notes spécifiquement adaptées à ta posture **Lead IA Neoteem** (pas pur technicien) sur :

- **MLOps minimum viable scale-up 5 pers** — à créer ou demander à l'agent [[responsable-ia]] de générer
- **Observability LLM Langfuse + Arize** — à créer
- **Eval suite Promptfoo CI** — à créer
- **Pattern MCP pour Loji** (NeoChat tools exposés) — à créer

**Stratégie recommandée** : ne pas dupliquer 04-Techniques/. Si tu as besoin d'une note adaptée Neoteem, demande à l'agent `responsable-ia` de la générer en lisant `04-Techniques/` + ton contexte projet.

## Liens

- [[../index]] — index casquette
- `vault/claude-forge/04-Techniques/` — source canonique technique
