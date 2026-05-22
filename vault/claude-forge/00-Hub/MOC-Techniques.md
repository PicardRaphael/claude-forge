---
aliases:
- MOC Techniques
- index techniques
- techniques CC
- patterns Claude Code
- prompt engineering techniques
auteur: claude
derniere-maj: 2026-05-20
resume: 'Index des techniques : prompt engineering, context engineering, patterns,
  anti-patterns'
tags:
- '#type/index'
- '#type/techniques'
titre: MOC — Techniques
type: index
---
# Techniques

## Prompt Engineering

- [[Context Engineering]] — Paradigme dominant 2026
- [[Adaptive Thinking]] — Opus 4.7, off par défaut
- [[Effort Levels Guide]] — low/medium/high/xhigh/max
- [[amanda-askell-prompt-engineering]] — 15 techniques Askell : TDD prompts, anti-filler, disposition vs regles
- [[forge-prompt-machine]] — 12 principes FORGE BellumAI x Askell, checklist, anti-patterns
- [[prompting-chat-cowork-code]] — Differences de prompting Chat vs Cowork vs Code, Opus 4.7
- [[outcome-first-prompting]] — OpenAI GPT-5.5 : définir l'outcome, pas le process (avril 2026)
- [[over-specification-paradox]] — UCL : au-delà de S*=0.509, spécifier nuit quadratiquement
- [[deprecated-techniques-2026]] — Techniques désormais contre-productives sur modèles frontier
- [[prompting-opus47-cheatsheet]] — 16 prompts officiels Anthropic copier-coller pour Opus 4.7
- [[opus-47-design-defaults]] — Style visuel persistant Opus 4.7 + 2 contre-mesures

## Patterns

- Knowledge-First Routing — Brain avant code
- Fleet Commander — Boris, parallélisme worktrees
- Document and Clear — Plan → .md → /clear → nouvelle session
- Skills as Composability — Thariq, skills = couche composable
- [[LLM Wiki]] — Karpathy, knowledge management plain text
- [[Andrej Karpathy]] — 4 principes coding (Simplicity, Surgical, Assumptions, Verifiable Steps)
- [[config-guardian-pattern]] — Audit multi-repo 5 checks, corrections par stack, mémoire compounding Boris+Karpathy
- [[workflow-claude-code-optimal]] — Synthese Boris, Erik, Thariq, Cat Wu, Karpathy : planification, contexte, skills, effort
- [[workflow-claude-code-optimal]] — Architecture complete vibe coding Claude Code : agents, skills, pipeline, /go, /recap
- [[pattern-vault-query-guard]] — Hook deterministe : agents DOIVENT consulter vault avant d'ecrire
- [[decoupe-agents-anti-crash]] — Max 6-8 ops/agent, decoupage par theme/repo/phase, parallelisation
- [[limites-subagents-claude-code]] — 200K ctx, 32K output, maxTurns casse, jamais parallele, bugs GitHub
- [[running-implementation-notes]] — Thariq : fichier vivant pendant implémentation, capture décisions/déviations/tradeoffs/questions
- [[subagent-explore-then-edit]] — Anthropic : subagent read-only mappe le subsystem dans un fichier, main agent édite avec picture complète
- [[codebase-maps-pattern]] — Markdown table of contents racine pour grosses codebases / structure non-conventionnelle

## Agents & Harness Engineering

- [[Andrej Karpathy]] — Framework Karpathy : Software 3.0, vibe coding vs agentic engineering, jagged intelligence
- [[workflow-claude-code-optimal]] — Checklist deploiement agentic engineering sur projet Neoteem
- [[harness-engineering]] — Agent = Modèle + Harness : contraintes déterministes > prompts suggestifs
- [[mass-multi-agent-system-search]] — DeepMind ICLR 2026 : optimisation conjointe prompts + topologie
- [[prompt-armor]] — ICLR 2026 : LLM préprocesseur défense injection, taux attaque < 1%
- [[prompt-rewriter-pattern]] — Pattern prompt rewriter : transformer des prompts vagues en specs précises
- [[architecture-cerveau-obsidian-mcp]] — Architecture cerveau Obsidian + MCP pour mémoire persistante IA

## Architecture Hooks

- [[raisonnement-22mai-doctrine-vs-enforcement]] — TTL sur markers = blocage, existence seule + SessionStart reset
- [[workflow-claude-code-optimal]] — SessionStart reset → architect → dev → code-reviewer → /go → pipeline-reset

## Anti-patterns

- Silent Assumptions — Karpathy anti-pattern #1
- Over-Engineering — Abstraction prématurée
- Drive-By Refactoring — Refacto non demandé
- [[erreur-advisory-rules-insuffisantes]] — Rules advisory ignorées, hooks déterministes obligatoires

## Architectures Chatbot & Multi-Agent

- [[index-architectures]] — **Decision tree : quel pattern + framework pour quel chatbot**
- [[pattern-single-agent-multi-tool]] — Le defaut (80% des cas) : 1 agent + N outils
- [[pattern-orchestrateur]] — Supervisor central + variante hierarchique
- [[pattern-swarm]] — Handoffs decentralises, latence optimale
- [[pattern-pipeline]] — Chaine sequentielle, evaluator-optimizer
- [[architecture-claude-api]] — Messages API, Agent SDK, Managed Agents
- [[architecture-openai-api]] — Responses API, Agents SDK, Conversations
- [[architecture-langgraph]] — StateGraph, checkpointing, HITL
- [[architecture-crewai]] — Crews, Flows, prototypage rapide
- [[architecture-gemini-api]] — ADK, A2A protocol, budget tokens
- [[architecture-autogen]] — GroupChat, en declin

## Stacks Implementation IA (TypeScript / Python)

- [[stack-typescript-ia]] — **Stack TS complet** : Vercel AI SDK, Mastra, Zod, SSE, Cloudflare, audit checklist
- [[stack-python-ia]] — **Stack Python complet** : LangGraph, Pydantic AI, Instructor, DSPy, FastAPI, audit checklist

## RAG & Search

- [[sqlite-fts5-vault]] — Pattern : indexer un vault Obsidian dans SQLite FTS5 sans dependance Obsidian

## Raisonnements caches

- `Knowledge/raisonnements/` — Chaines de raisonnement validees, indexees par type de probleme (skill `/reasoning-cache`)
- [[architecture-decision-hook-maison-vs-plugin-tiers]] — Hook maison Python l'emporte sur plugin tiers populaire (tdd-guard) car validation LLM = antipattern dans un guard déterministe

## Fine-Tuning LLM

- [[MOC-Fine-Tuning]] — **Index complet fine-tuning** (techniques, outils, modèles, infra, privacy)
- [[fine-tuning-techniques-peft]] — LoRA, QLoRA, DoRA, Spectrum, IA3, configs recommandées 2026
- [[fine-tuning-alignment]] — DPO, GRPO, ORPO, SimPO, DAPO, RLHF, pipeline 3 stages
- [[fine-tuning-frameworks]] — Unsloth, Axolotl, LLaMA-Factory, TRL, Ludwig, MLX
- [[fine-tuning-models]] — Meilleurs modèles open-source par taille et cas d'usage
- [[fine-tuning-datasets]] — Préparation données, qualité, synthétique, Argilla, Distilabel
- [[fine-tuning-evaluation]] — Benchmarks, LLM-as-judge, métriques post-FT
- [[fine-tuning-infrastructure]] — GPUs, cloud providers, serving (vLLM, SGLang, Ollama)
- [[fine-tuning-privacy]] — On-premise, RGPD, VaultGemma, federated learning, TEE
- [[rag-vs-fine-tuning]] — Quand RAG, quand fine-tuning, quand hybride, RAFT

## Liens



## Spec-Driven Development

- [[pattern-spec-driven-development]] — Consensus pionniers 2026 : interview → SPEC.md → execute. Thariq, Boris, Anthropic
- [[pattern-spec-skill-deployment]] — Guide déploiement skill /spec sur un nouveau repo
- [[pattern-sdd-triangle]] — Drew Breunig : SPEC ↔ TESTS ↔ CODE, outil Plumb, spec diffing
- [[pattern-github-spec-kit]] — Framework 93K stars, 6 commandes, Constitution.md
- [[pattern-gsd-framework]] — GSD 59K stars, contexte frais par agent, plans = prompts
- [[feature-dev-plugin]] — Plugin officiel Anthropic 7 phases, 3 types d'agents en //