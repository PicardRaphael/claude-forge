---
aliases:
- MOC Techniques
- index techniques
- techniques CC
- patterns Claude Code
- prompt engineering techniques
auteur: claude
derniere-maj: 2026-09-05
resume: 'Index des techniques : prompt engineering, context engineering, patterns,
  anti-patterns'
tags:
- '#type/index'
- '#type/technique'
titre: MOC — Techniques
type: index
---
# Techniques

## Prompt Engineering
- [[doctrine-par-modele-opus5-fable5]] — les règles de prompting diffèrent PAR MODÈLE et non par génération : Opus 5 s'auto-vérifie et sur-délègue, Fable 5.1 refuse les instructions show-your-reasoning (`reasoning_extraction`). À lire avant toute règle de prompting transversale
- [[prompting-fable5-cheatsheet]] — 12 prompts officiels Anthropic copier-coller pour Fable 5 (classe Mythos) : goal-setting > micromanagement, anti-refacto, verification loops, memory system
- [[recursive-language-models-rlm]] — RLMs (MIT, Khattab) : prompt = variable externe dans un REPL, auto-appel récursif, nouvel axe test-time compute / context folding

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
- [[audit-thematique-claims-vault]] — Audit claims factuelles d'un corpus : clusters de sub-agents, checkpoint A avant B, self-verify des FAUX, types 1/2/3
- [[refactor-masse-script-python-regex]] — >10 fichiers même pattern : script Python regex ponctuel au lieu d'Edit séquentiels (308L/18 fichiers/5s)
- [[verifier-audit-deja-fait-avant-relancer]] — Checklist 4 étapes AVANT tout audit thématique (derniere-maj, Knowledge/erreurs, context-actuel, CHANGELOG)
- [[verify-empirique-avant-affirmation-session]] — Vérifier matériellement avant d'affirmer en session (grep/read/run, jamais de mémoire)
- [[config-repo-equipe-vs-forge]] — Repo d'équipe ≠ machinerie forge : skills auto-portantes, hooks non-bloquants, pas de delegate-guard
- [[mcp-tool-prefix-serveur-wiring]] — Préfixe mcp__<serveur>__<tool> : wiring, collisions, renommage serveur
- [[pdf-chrome-headless]] — PDF fidèle à la charte via Chrome headless (--print-to-pdf), pas de lib intermédiaire
- [[llm-deep-research-version-numbers-hallucinated]] — Chiffres précis des deep research LLM tiers = vecteur principal d'hallucination, WebFetch source primaire avant action
- [[changer-mecanisme-lire-tests-qui-verrouillent]] — Avant de changer un mécanisme/contrat, grep ses tests (patch/grep-source/imports) — 9 tests cassés sinon
- [[raisonnement-da-probe-empirique-avant-verdict]] — DA sur prémisse falsifiable : mesurer AVANT de débattre des garde-fous ; la donnée tranche (c) tuer vs (b) garde-fous
- [[architecture-decision-memoire-portable-import]] — Raisonnement : mémoire portable cross-machine via @import CLAUDE.md (pivot depuis autoMemoryDirectory cassé en multi-repos). Mécanisme orthogonal > réglage global.

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

- [[memoire-agent-mem0]] — mem0 : couche mémoire long-terme universelle pour agents (extraction/consolidation LLM, cross-session). v3 avril 2026 a retiré le graphe externe de l'OSS
- [[memoire-agent-langmem]] — LangMem : SDK mémoire LangChain/LangGraph, différenciateur = mémoire procédurale (réécrit le prompt système). Lock-in LangGraph fort
- [[packmind-context-governance]] — Packmind (ex-Promyze) : gouvernance de contexte pour agents de codage (single-source → CLAUDE.md/.cursor/rules/AGENTS.md + versioning + drift). Industrialise la propagation cross-repo manuelle de la forge
- [[anti-reentrance-sub-agents-pattern-escalade]] — Escalade STOP + signal ESCALADE REQUISE markdown vers session principale qui orchestre = DÉFAUT recommandé (contexte propre, coût maîtrisé). Le nesting sous-agents est POSSIBLE depuis CC v2.1.172 (amende 16 juin) mais reste déconseillé par défaut ; verrouiller un agent leaf-node via `tools:` explicite sans `Agent` ou `disallowedTools: Agent`. Format standardise neo_ia 23 mai 2026.
- [[architecture-decision-niveaux-mesure-agents]] — Niveau 1 statique (frontmatter) = CARTE, Niveau 2 transcripts JSONL = verdict echantillon, Niveau 3 hook PostSubagentStop CSV = verdict statistique. Capacite vs usage = ne JAMAIS refactor mass agents sur Niveau 1 seul (architect-deep 5/5 seuils Niveau 1 mais 6 ops Niveau 2 = OK)

- [[Andrej Karpathy]] — Framework Karpathy : Software 3.0, vibe coding vs agentic engineering, jagged intelligence
- [[workflow-claude-code-optimal]] — Checklist deploiement agentic engineering sur projet Neoteem
- [[harness-engineering]] — Agent = Modèle + Harness : contraintes déterministes > prompts suggestifs
- [[mass-multi-agent-system-search]] — DeepMind ICLR 2026 : optimisation conjointe prompts + topologie
- [[prompt-armor]] — ICLR 2026 : LLM préprocesseur défense injection, taux attaque < 1%
- [[prompt-rewriter-pattern]] — Pattern prompt rewriter : transformer des prompts vagues en specs précises
- [[architecture-cerveau-obsidian-mcp]] — Architecture cerveau Obsidian + MCP pour mémoire persistante IA

## Limites connues MCP forge-brain

- [[limite-mcp-lock-inter-ecritures]] — pas de lock inter-écritures (race théorique). Non codé : usage solo séquentiel. Déclencheur : multi-agent parallèle écrivant le vault.
- [[limite-mcp-lag-reindexation-agregats]] — lag des agrégats (poll watcher 30s, fluctuation compteur non liée aux edits). Non codé : sans impact, vérifier par git diff pas par compteur. Déclencheur : usage dépendant d'un compteur temps-réel.

## Architecture Hooks
- [[hooks-conformite-audit-passif-continu]] — Hook de conformité = audit passif permanent. Un blocage sur action légitime révèle souvent une dette préexistante. Ne jamais contourner, nettoyer dans la même passe.

- [[raisonnement-22mai-doctrine-vs-enforcement]] — TTL sur markers = blocage, existence seule + SessionStart reset
- [[workflow-claude-code-optimal]] — SessionStart reset → architect → dev → code-reviewer → /go → pipeline-reset

## Anti-patterns
- [[audit-lifecycle-classification-categories]] — Raisonnement validé 28 mai 2026 : auditer N composants `.claude/` → classifier par catégorie (référence/outil-pur/exécution/audit-jugement) AVANT verdict, sinon mass-AMEND aveugle (overreach) ou audit à l'œil (skip canoniques)

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

## Paysage outils IA marché (build-vs-buy)

- [[intelligence-de-code-build-vs-buy]] — context engines (SocratiCode, CodeGraph, Serena, Augment) + revue de code IA (CodeRabbit, SonarQube, Semgrep). Faire coder mieux les agents.

- [[MOC-paysage-outils-ia-marche-2026]] — **Cartographie marché 5 catégories** : voix, briques produit, productivité interne, infra/LLMOps, plateformes générales. Angle build-vs-buy + adoption.
- [[outils-voix-ia-build-vs-buy]] — TTS / STT / agents vocaux (ElevenLabs, Gladia, Whisper, Retell, LiveKit). Build-vs-buy par brique.
- [[briques-produit-ia-build-vs-buy]] — OCR, embeddings, reranking, modération, RAG-aaS, extraction structurée (Mistral OCR, Ragie, BAML).
- [[outils-memoire-rag-gouvernance-juin-2026]] — mem0, LangMem, Pinecone, Onyx, Packmind.

## Stacks Implementation IA (TypeScript / Python)

- [[stack-typescript-ia]] — **Stack TS complet** : Vercel AI SDK, Mastra, Zod, SSE, Cloudflare, audit checklist
- [[stack-python-ia]] — **Stack Python complet** : LangGraph, Pydantic AI, Instructor, DSPy, FastAPI, audit checklist

## RAG & Search

- [[pinecone-vector-database]] — Pinecone en profondeur : vector DB managée serverless, pricing RU/WU, Inference + Assistant
- [[onyx-enterprise-search]] — Onyx (ex-Danswer) : plateforme RAG/recherche entreprise open-source, 50-60+ connectors, sync ACL, index OpenSearch (ex-Vespa v4.0)

- [[sqlite-fts5-vault]] — Pattern : indexer un vault Obsidian dans SQLite FTS5 sans dependance Obsidian

## Raisonnements caches
- [[decision-byte-for-byte-splice-test-live]] — Écriture fichier byte-for-byte : disqualifier le re-dump a priori (splice ciblé), et ne jamais conclure « validé » sans test live byte-exact (un diff mémoire ment sur l'IO ; splitlines() est aveugle aux conversions EOL)

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



## OpenAI Codex

Corpus doctrinal Codex (miroir de la doctrine Claude Code) — index complet dans [[MOC-Codex]].

- [[MOC-Codex]] — **index Codex** : workflow, AGENTS.md, config/profils, skills, hooks, subagents, loops, mémoire, arbitrage ChatGPT
- [[workflow-codex-optimal]] — note maître : Surface Map des 8 leviers, multitasking Sottiaux, séquence par taille de tâche
- [[comment-creer-hook-codex]] — hooks Codex stables (v0.124.0), **12 events au 5 sept. 2026** (dont `Interrupt`, seul event sans équivalent Claude Code), trust model par hash, piège `Stop` inversé vs Claude Code
- [[comment-creer-skill-codex]] — Skills Codex : noyau standard partagé + divergences (`.agents/skills`, `openai.yaml`), portabilité non byte-identique
- [[codex-vs-chatgpt-seul]] — arbitrage Codex (agent de code) vs ChatGPT (app conversationnelle)

## Spec-Driven Development

- [[pattern-spec-driven-development]] — Consensus pionniers 2026 : interview → SPEC.md → execute. Thariq, Boris, Anthropic
- [[pattern-spec-skill-deployment]] — Guide déploiement skill /spec sur un nouveau repo
- [[pattern-sdd-triangle]] — Drew Breunig : SPEC ↔ TESTS ↔ CODE, outil Plumb, spec diffing
- [[pattern-github-spec-kit]] — Framework 6 commandes, Constitution.md
- [[pattern-gsd-framework]] — GSD : contexte frais par agent, plans = prompts
- [[feature-dev-plugin]] — Plugin officiel Anthropic 7 phases, 3 types d'agents en //

## Synthèses

- [[techniques-inedites]] — Combinaisons innovantes que personne ne fait encore, issues du croisement de 10 rapports de recherche RAG + Agents IA 2026.
