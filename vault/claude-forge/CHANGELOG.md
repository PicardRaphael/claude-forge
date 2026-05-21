---
titre: "Changelog vault forge-brain"
resume: "Historique des ajouts et modifications du vault forge-brain"
aliases:
  - changelog vault
  - historique vault
  - changelog forge-brain
  - historique notes vault
type: index
derniere-maj: 2026-05-20
auteur: claude
tags:
  - "#type/index"
  - "#domaine/claude-code"
---

## 2026-05-21 — Convention couleurs agents cross-repo

- **Ajoutée** : `01-Claude/Code/best-practices/agents-color-convention.md` — Standard palette couleurs par catégorie (8 couleurs, 8 rôles)
- **Source** : Test Desktop avec collègue — point coloré visible mais pas le nom d'agent, besoin de convention cohérente cross-repo

## 2026-05-20 — Fixes DA EVOLVE (frontière mémoire/vault + audit fantôme)

- **Créée** :
  - `1-Projets/Neoteem/agent-manager-neoteem.md` — Application concrète du rôle Agent Manager à Neoteem (scindée depuis agent-manager-role.md selon rule memory-discipline.md)
- **Modifiées** :
  - `01-Claude/Code/best-practices/agent-manager-role.md` — Section "Application à Neoteem" retirée (déportée vers 1-Projets/), tag #projet/neoteem retiré, wikilink ajouté vers [[agent-manager-neoteem]]
  - `04-Techniques/patterns/codebase-maps-pattern.md` — Table "Application aux repos Neoteem" retirée (audit fantôme non basé sur audit réel)
- **Source** : Verdict devil's advocate 2026-05-20 — fixes EVOLVE non-bloquants restants

## 2026-05-20 — Capitalisation blog Anthropic "Large codebases" + tweet Thariq

- **Créées** :
  - `04-Techniques/patterns/running-implementation-notes.md` — Pattern Thariq (758k vues 18 mai 2026) : fichier vivant maintenu pendant l'implémentation pour capturer design decisions, deviations, tradeoffs, open questions
  - `04-Techniques/agents/subagent-explore-then-edit.md` — Pattern Anthropic : subagent read-only mappe le subsystem dans un fichier, main agent édite avec la picture complète
  - `01-Claude/Code/best-practices/agent-manager-role.md` — Rôle org émergent (DRI / Agent Manager / équipe dédiée) pour Claude Code en enterprise
  - `04-Techniques/patterns/codebase-maps-pattern.md` — Markdown table of contents à la racine pour navigation Claude sur grosses codebases
- **Modifiées** :
  - `01-Claude/Code/best-practices/hooks-guide.md` — Ajout section "Self-improving hooks" : pattern Stop hook qui propose updates CLAUDE.md, SessionStart dynamique, 3 rôles des hooks
- **Source** : Blog Anthropic "How Claude Code works in large codebases" (14 mai 2026) + tweet @trq212 (18 mai 2026)

## 2026-05-18 — Feature classifier + audit skills cross-repo

- **Créée** :
  - `01-Claude/Code/features/auto-mode-classifier.md` — Filet de sécurité Anthropic en mode auto : scope, self-modification, destructif. Bypass via permissions.allow
- **Modifiée** :
  - `0-Inbox/context-actuel.md` — résolu conflit merge + mis à jour avec session 2026-05-18
- **Hors-vault** :
  - neo_ia : 13 skills passées `user-invokable: true` (référence/conventions accessibles spontanément)
  - ia_back : 7 skills passées `user-invokable: true`
- **Source** : Session audit neo_ia + question Raphael sur classifier

## 2026-05-18 — Capitalisation guide officiel Anthropic prompting Opus 4.7

- **Modifiées** :
  - `03-Modeles/anthropic/Opus 4.7.md` — enrichi : instruction-following littéral, response length adaptative, tool use, subagents, ton, design defaults, code review recall/precision, effort levels, prompts officiels
  - `04-Techniques/prompt-engineering/Effort Levels Guide.md` — strict respect low/medium, risque under-thinking, 64k tokens, steerability thinking
  - `04-Techniques/prompt-engineering/Adaptive Thinking.md` — steerability, interleaved thinking, migration extended→adaptive, bonnes pratiques Anthropic
- **Créées** :
  - `04-Techniques/prompt-engineering/opus-47-design-defaults.md` — style cream/Georgia/terracotta persistant + 2 contre-mesures + prompt anti-slop allégé
  - `04-Techniques/prompt-engineering/prompting-opus47-cheatsheet.md` — 16 prompts officiels Anthropic copier-coller + 4 bonus
- **Source** : Guide officiel Anthropic "Prompting best practices" (platform.claude.com) + article Ruben Hassid (Substack)

## 2026-05-15 — Audit vault complet + normalisation wikilinks + desorphelinement

- **Corrigé** :
  - 37 wikilinks à chemin normalisés (`[[path/note]]` → `[[note]]`) dans 11 fichiers
  - 8 wikilinks vers cibles inexistantes corrigés (Best practices Boris Thariq → lien correct, etc.)
  - 9 notes frontmatter corrigés (auteur, resume, MOC links) via fix.py
  - 3 notes critiques DA enrichies (resume + aliases + tags)
  - 2 notes MOC `derniere-maj` format corrigé
- **Créés** :
  - `Knowledge/erreurs/_index.md` — index 12 erreurs documentées
  - `Knowledge/syntheses/_index.md` — index 5 synthèses d'analyses
  - `Knowledge/critiques/_index.md` — index 5 critiques DA
- **Modifiés** :
  - `MOC-Claude-Code` — ajout section Agents forge (7 fiches), cowork-architecture, mcp-vs-cli-vs-skills
  - `MOC-Techniques` — ajout prompt-rewriter-pattern, architecture-cerveau-obsidian-mcp
- **Résultat** : score 98.2→98.8, orphelines 31→4, grade A 224→232, grade C 1→0
- **Bug fix** : audit.py crash sur `resume` de type list (AttributeError)
- **Batch stubs** (17 notes créées pour combler les red links) :
  - `05-Leaders/` : Amanda Askell, Patrick Lewis, Rafael Rafailov, Alex Albert
  - `01-Claude/Code/features/` : Agent Teams, Session Sharing, Claude Desktop, Project Glasswing
  - `04-Techniques/` : rag-production, rag-evaluation, Silent Assumptions, Context Management, System Prompt Design, ColPali
  - `07-Prompts/` : Piebald-AI System Prompts
  - `06-Industrie/` : OpenAI Revenue 25B
  - `Knowledge/erreurs/` : erreur-skip-checklist-skill-modification
- **Wikilinks redirigés** : Skills Best Practices → skills-guide, obsidian-markdown/python-ref → texte (skills)
- **Aliases ajoutés** : cowork-architecture += Cowork, Dispatch
- **Résultat final** : 251 notes, 100% grade A, score 98.9, orphelines 4 (intentionnelles)
- **Source** : /vault-audit + /vault-audit fix

## 2026-05-14 — 5 points Raphael + hooks enforcement + /done

- **Créés** :
  - `Knowledge/erreurs/erreur-auto-mode-classifier-self-modification.md` — double block delegate-guard + auto-mode
  - `04-Techniques/agents/prompt-rewriter-pattern.md` — analyse pattern et alternatives
- **Hooks créés** :
  - `skill-activation.py` (UserPromptSubmit) — recommandations skills automatiques
  - `vault-write-tracker.py` (PostToolUse) — compte écritures vault → DA après 3+
  - `proactivity-reminder.py` (Stop) — rappel proposition Jarvis si session > 5 tours
  - `apply-edit.py` — utilitaire bypass delegate-guard + auto-mode
- **Skill créée** : `/expand` — transforme prompt brut en spec précise
- **Source** : 5 questions Raphael sur meta-design forge

## 2026-05-14 — Restructuration 01-Claude + 8 notes deep research

- **Restructuration** : `01-Claude-Code/` → `01-Claude/Code/` + `01-Claude/Cowork/` (nouveau)
- **Créées dans 01-Claude/Code/best-practices/** :
  - `skills-guide.md` — Format YAML, 9 catégories Thariq, activation, budget /doctor
  - `hooks-guide.md` — 25+ events, exit 2, marker+guard, hookSpecificOutput
  - `claudemd-guide.md` — < 200 lignes, loading order, @import, compounding
  - `context-management.md` — /clear, /compact, compaction, subagents isolation
  - `agents-orchestration.md` — Subagents YAML, Generator/Evaluator, Dreaming, Outcomes
  - `mcp-vs-cli-vs-skills.md` — Benchmarks, Willison skills>MCP, matrice décision
- **Créées dans 01-Claude/Cowork/** :
  - `cowork-architecture.md` — Vue d'ensemble, plugins, Dispatch, Routines, pricing
  - `cowork-skills-reliability.md` — 2 problèmes, 73% cassées, debugging 9 étapes, bugs connus
- **Modifiées** :
  - `04-Techniques/agents/harness-engineering.md` — 4e paradigme, feedforward/feedback, 65% stat
  - `01-Claude/Code/changelog/CC mai 2026 - Code with Claude.md` — v2.1.139-140
- **Skills modifiées** :
  - `cc-news` v2.1.138 → v2.1.140
  - `cc-cowork-ref` — section diagnostic harness engineering
  - `cc-news/references/domain-claude-code.md` — @ClaudeCodeLog et @ClaudeDevs
- **Source** : cc-news 11 agents + 6 agents deep research (Boris, Cat Wu, Lydia, Thariq, Willison, Anthropic docs)

## 2026-05-14 — cc-news scan complet (session précédente)

- Harness Engineering enrichi, CC changelog v2.1.139-140
- Source : scan cc-news complet 11 agents

## 2026-05-13 — Setup Claude Code lojii + Figma MCP + Techniques memoire agents

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`, `04-Techniques/patterns/pattern-figma-mcp-claude-code.md`, `04-Techniques/agents/technique-dreaming-cross-session.md`, `04-Techniques/agents/technique-shared-agent-memory.md`, `Knowledge/critiques/critique-2026-05-13-setup-lojii.md`
- **Modifiées** : `0-Inbox/context-actuel.md`
- **Source** : Analyse projet-analyzer + recherche web Figma MCP + Anthropic Dreaming + Netflix memory pattern + agent-memory scopes

## 2026-05-13 — Setup Claude Code lojii + Pattern Figma MCP

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`, `04-Techniques/patterns/pattern-figma-mcp-claude-code.md`, `Knowledge/critiques/critique-2026-05-13-setup-lojii.md`
- **Modifiées** : `0-Inbox/context-actuel.md`
- **Source** : Analyse projet-analyzer + recherche web Figma MCP + critique devil's advocate

## 2026-05-13 — Analyse projet Lojii (frontend Vue 3)

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`
- **Source** : Analyse complète projet-analyzer sur neofront/lojii (634 composants Vue 3 / Vuetify 3)

## 2026-05-12 — État de l'art Tool Retrieval & Query Expansion

- **Ajoutées** : `04-Techniques/rag/tool-retrieval-query-expansion.md`
- **Modifiées** : `04-Techniques/rag/RAG.md` (ajout lien MOC)
- **Source** : Recherche web état de l'art 2024-2026 (Re-Invoke, TOOLQP, OATS, ToolRerank, ToolShed, MCP Semantic Discovery) + analyse code neo_ia HybridToolSelector

## 2026-05-11 — Architecture profonde NeoDoc (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/neodoc/** :
  - `neodoc-architecture.md` — Vue d'ensemble : RAG Vertex AI Discovery Engine, workspaces, notes indexables, schéma BDD 9 tables
  - `neodoc-research-agent.md` — Agent Research LangGraph 5 nœuds, query decomposition (google-genai natif), grounding citations, dual path (retrieve vs full_doc)
  - `neodoc-ingestion-pipeline.md` — Pipeline 7 étapes Drive/upload → GCS → Discovery Engine, 4 modes (sync/async/batch/folder), retry intelligent
- **Modifiée** : `neo_ia.md` — wikilinks NeoDoc ajoutés
- **Source** : analyse profonde du code source apps/neodoc/

## 2026-05-11 — Architecture profonde NeoMail (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/neomail/** :
  - `neomail-architecture.md` — Vue d'ensemble : webhook Pub/Sub, classification LLM, 21 tools, BROUILLON ONLY, diff NeoChat vs NeoMail
  - `neomail-webhook-pipeline.md` — Pipeline 10 étapes : Pub/Sub → History API → classify → label sync → auto-reply draft, sécurité IAM, hiérarchie exceptions
- **Restructurée** : notes NeoChat déplacées dans `neochat/`, NeoMail dans `neomail/`
- **Modifiée** : `neo_ia.md` — wikilinks NeoMail ajoutés
- **Source** : analyse profonde du code source apps/neomail/

## 2026-05-11 — Architecture profonde NeoChat (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/** :
  - `neochat-architecture.md` — Vue d'ensemble : 6 agents, 26 tools, interrupt handlers, ToolInTool patterns
  - `neochat-react-engine.md` — Declarative ReAct Engine 7 phases, AgentBlueprint dataclass, interrupt handlers
  - `neochat-adaptive-prompt.md` — Adaptive Prompt Builder V2 4 layers (cache Gemini), ToolPromptLoader, conditional rules
  - `neochat-tool-rag.md` — HybridToolSelector pgvector : 10 étapes (expansion, hybrid search, LLM rerank, BFS deps)
- **Modifiée** : `neo_ia.md` — ajout section Architecture détaillée par app (NeoChat/NeoDoc/NeoMail)
- **Source** : analyse profonde du code source neo_ia (blueprint, react.py, adaptive.py, selector.py, builders)

## 2026-05-11 — Capitalisation vidéos Code with Claude + Boris AI Ascent

- **Créées dans 01-Claude-Code/features/** :
  - `Memory Managed Agents.md` — Architecture memory : filesystem, permission scopes, optimistic concurrency, version history
  - `Dreaming Managed Agents.md` — Process scheduled review cross-sessions, déduplication, vérification, enrichissement
  - `Code with Claude 2026.md` — Résumé conférence SF : SpaceX, Dreaming, Outcomes, Multi-agent, Routines
- **Créée dans 04-Techniques/patterns/** :
  - `boris-workflow-2026-may.md` — Setup Boris mai 2026 : mobile-first, /loop partout, 150 PRs/jour, coding is solved
- **Modifiées** : `MOC-Claude-Code.md` (4 notes ajoutées), `Boris Cherny.md` (section mai 2026)
- **Source** : transcription YouTube — Memory & Dreaming (Mahesh Murag), Boris AI Ascent Sequoia, Everything new from CwC 2026 (Matt Cuda)

## 2026-05-11 — 6 fiches leaders agents/industrie + audit + corrections devil's advocate

- **Créées dans 05-Leaders/agents/** :
  - `Chi Wang.md` — AutoGen/AG2 creator, Google DeepMind, ICLR 2026
  - `Yohei Nakajima.md` — BabyAGI creator, Untapped Capital GP, build-in-public
  - `David Shapiro.md` — ACE Framework, architecture cognitive 6 couches
  - `Div Garg.md` — MultiOn founder, browser agents 500+ steps
  - `Joao Moura.md` — CrewAI founder & CEO, $18M levés, 50.8K stars
- **Créée dans 05-Leaders/industrie/** :
  - `Dario Amodei.md` — CEO Anthropic, RSP, Mythos, clash DoD 2026 (déplacé d'agents/ suite critique devil's advocate)
- **Corrections devil's advocate** :
  - Dario Amodei : déplacé de agents/ → industrie/ (cohérence taxonomique, la note dit elle-même qu'il n'est pas un builder agents)
  - `type: leader` harmonisé sur les 13 fiches agents (8 anciennes avaient `type: ""`)
  - Aliases Dario enrichis : +4 termes de recherche sémantique (responsible scaling, AI safety leader, etc.)
  - Joao Moura créé (candidat le plus évident absent de la batch initiale)
- **Modifiés** : `MOC-Leaders.md` (section Agents + Industrie enrichies), `Agents IA.md` (section Pionniers)
- **Enrichi** : `cc-news/references/domain-agents.md` (5 leaders ajoutés au tableau)
- **Audit** : 199 notes, score moyen 95/100 (185A/13B/0C/1D), fix déterministe appliqué
- **Source** : recherche web 2026 + devil's advocate

## 2026-05-10 — Dossier stacks/ : 2 notes reference implementation IA (TS + Python)

- **Creees dans 04-Techniques/stacks/** :
  - `stack-typescript-ia.md` — SDKs (Vercel AI SDK, Mastra, LlamaIndex.TS), RAG, streaming SSE, Zod, deployment edge, audit checklist, diagnostic optimisation
  - `stack-python-ia.md` — SDKs (LangGraph, Pydantic AI, Instructor, DSPy, CrewAI), RAG, ML/DL, FastAPI SSE, deployment, audit checklist, diagnostic optimisation
- **Sections ajoutees (corrections devil's advocate)** : Observability, Memory, Guardrails, MCP, Provider routing, Agent sandboxing, Audit Checklist (12-15 anti-patterns), Diagnostic optimisation (flux conditionnel)
- **Modifie** : `MOC-Techniques.md` — section "Stacks Implementation IA" ajoutee
- **Source** : Agent recherche TS/Python + advisor + devil's advocate (3 bloquants corriges)

## 2026-05-10 — Dossier chatbot/ : 11 notes architectures chatbot & multi-agent

- **Creees dans 04-Techniques/chatbot/** :
  - `index-architectures.md` — Decision tree pattern + framework, matrice evaluation croisee
  - `architecture-claude-api.md` — Messages API, Agent SDK, Managed Agents, system prompts
  - `architecture-openai-api.md` — Responses API, Agents SDK, Conversations, Realtime
  - `architecture-langgraph.md` — StateGraph, supervisor, swarm, checkpointing, HITL
  - `architecture-crewai.md` — Crews, Flows, memory unifiee, prototypage rapide
  - `architecture-gemini-api.md` — Function calling, ADK, A2A, Interactions API
  - `architecture-autogen.md` — GroupChat, en declin, successeur MS Agent Framework
  - `pattern-orchestrateur.md` — Supervisor + hierarchique cross-framework
  - `pattern-swarm.md` — Handoffs decentralises cross-framework
  - `pattern-pipeline.md` — Prompt chaining, evaluator-optimizer, parallelisation
  - `pattern-single-agent-multi-tool.md` — Pattern defaut 80% des chatbots
- **Modifie** : `MOC-Techniques.md` — section "Architectures Chatbot & Multi-Agent" ajoutee
- **Source** : 4 agents de recherche paralleles (Claude API, OpenAI, LangGraph, CrewAI/AutoGen/Gemini) + advisor + devil's advocate

## 2026-05-10 — Reorganisation 04-Techniques : 12 notes deplacees dans sous-dossiers, 5 index Knowledge crees

- **Deplacees vers prompt-engineering/** :
  - `amanda-askell-prompt-engineering.md` — depuis racine 04-Techniques
  - `forge-prompt-machine.md` — depuis racine 04-Techniques
  - `prompting-chat-cowork-code.md` — depuis racine 04-Techniques
- **Deplacees vers patterns/** :
  - `config-guardian-pattern.md` — depuis racine 04-Techniques
  - `pattern-vault-query-guard.md` — depuis racine 04-Techniques
  - `vibe-coding-setup-complet.md` — depuis racine 04-Techniques
  - `best-practices-claude-code-leaders.md` — depuis racine 04-Techniques
- **Deplacees vers agents/** :
  - `agentic-engineering-karpathy.md` — depuis racine 04-Techniques
  - `pattern-agentic-engineering.md` — depuis racine 04-Techniques (notes distinctes, pas fusionnees)
- **Deplacees hors 04-Techniques** :
  - `claude-desktop-preferences.md` → `01-Claude-Code/features/` (type feature, pas technique)
  - `mcp-obsidian-brain-v2.md` → `01-Claude-Code/features/` (feature Claude Code Neoteem)
  - `neoteem-brain-plugins.md` → `1-Projets/Neoteem/neoteem-brain/` (contexte projet)
  - `sqlite-fts5-vault.md` → `04-Techniques/rag/` (technique RAG/search)
- **Ajoutees** : 5 index `_index.md` dans Knowledge/ : evolutions/, reviews/, raisonnements/, explorations/, questions/
- **Modifiees** :
  - `00-Hub/MOC-Techniques.md` — reorganisation sections, suppression entrees parties, ajout Prompt Engineering + RAG
  - `00-Hub/MOC-Claude-Code.md` — ajout claude-desktop-preferences + mcp-obsidian-brain-v2 dans Features
  - `1-Projets/Neoteem/neoteem-brain/neoteem-brain.md` — ajout liens neoteem-brain-plugins + mcp-obsidian-brain-v2
- **Source** : reorganisation organisationnelle 04-Techniques demandee par Raphael

## 2026-05-10 — Capitalisation cc-news : 6 techniques prompt engineering 2026 (outcome-first, over-specification, harness, MASS, PromptArmor, deprecated)

- **Ajoutées** :
  - `04-Techniques/prompt-engineering/outcome-first-prompting.md` — OpenAI GPT-5.5 : outcome + critères de succès, pas process step-by-step
  - `04-Techniques/prompt-engineering/over-specification-paradox.md` — UCL arXiv 2601.00880 : seuil S*=0.509, dégradation quadratique, 29.8% réduction tokens
  - `04-Techniques/prompt-engineering/deprecated-techniques-2026.md` — Inventaire complet techniques contre-productives sur frontier models
  - `04-Techniques/agents/harness-engineering.md` — Agent = Modèle + Harness, contraintes déterministes > prompts suggestifs
  - `04-Techniques/agents/mass-multi-agent-system-search.md` — DeepMind ICLR 2026 : optimisation conjointe prompts + topologie multi-agent
  - `04-Techniques/agents/prompt-armor.md` — ICLR 2026 arXiv 2507.15219 : LLM préprocesseur défense injection, < 1% attack rate
- **Modifiées** :
  - `00-Hub/MOC-Techniques.md` — 3 nouvelles sections + 6 wikilinks ajoutés
  - `00-Hub/MOC-Prompts.md` — 3 wikilinks ajoutés dans section Principes
- **Source** : cc-news scan 2026-05-10 (24 techniques prompt engineering)

## 2026-05-10 — Capitalisation cc-news : changelogs CC 2.1.132-136, Cursor 3.3, Grok 4.20, Jina v4, Context Engineering

- **Ajoutées** :
  - `01-Claude-Code/changelog/CC v2.1.132.md` — CLAUDE_CODE_SESSION_ID, memory leak 10GB+ MCP stdout (6 mai)
  - `01-Claude-Code/changelog/CC v2.1.133.md` — worktree.baseRef, CLAUDE_EFFORT hooks, sandbox paths (7 mai)
  - `01-Claude-Code/changelog/CC v2.1.136.md` — Release majeure 50+ changements, autoMode.hard_deny (8 mai)
  - `04-Techniques/rag/jina-embeddings-v4.md` — 3.8B, single+multi-vector ColBERT unifié, 72.19 JinaVDR
- **Modifiées** :
  - `02-Concurrents/cursor/Cursor.md` — section Cursor 3.3 : PR Review, Parallel Agents, Visual Canvases
  - `02-Concurrents/xai/xAI Grok.md` — Grok 4.3 (1M ctx, vidéo), Grok 4.20 Beta (4+16 agents)
  - `04-Techniques/context-engineering/Context Engineering.md` — 4 pilliers, sweet spot 150-300 mots, règles empiriques
  - `00-Hub/MOC-Claude-Code.md` — wikilinks CC v2.1.132/133/136
- **Source** : cc-news scan 2026-05-10

## 2026-05-09 — Migration CLI→MCP complète + Stop hook devil's advocate + autonomie

- **Migration CLI→MCP** : TOUS les agents (10/10), skills (forge-brain, done, recap, reasoning-cache, skill-evolve, forge-review, vault-audit), rules (memory-discipline, check-before-create, forge-brain-proactive), et references migrés. Zéro ref CLI dans le projet.
- **Stop hook** : `devil-advocate-stop.py` bloque la fin de session si devil's advocate pas lancé
- **Auto-start MCP** : hook SessionStart lance le MCP automatiquement
- **Skill obsidian-cli supprimée** : remplacée par MCP forge-brain
- **Règle d'autonomie** : advisor + devil's advocate valident → agir sans demander
- **MCP optimisé** : 11 outils (+ list_notes, vault_stats), descriptions forge-brain, exemples adaptés
- **Source** : feedback Raphael, recherche Boris best practices, advisor

## 2026-05-09 — MCP forge-brain + /watch + Context Note + devil's advocate

- **Ajoutées** :
  - `mcp-forge-brain/` — MCP server self-contained (SQLite FTS5, port 8091), copie autonome de mcp-obsidian-brain
  - `.mcp.json` — config MCP projet pour forge-brain
  - `0-Inbox/context-actuel.md` — Working memory dynamique (/done écrit, /recap lit)
  - Skill `/watch` — transcription YouTube via yt-dlp
- **Modifiées** :
  - Skill `/done` : fix cross-projet, routing 1-Projets/2-Casquettes, frontmatter nettoyé, garde anti-hallucination, Context Note en étape 6
  - Skills `forge-brain`, `recap` : structure vault + scan 1-Projets/2-Casquettes
  - Skill `vault-audit` + `audit.py` : nouveaux dossiers dans FOLDER_TO_MOC + TEMPLATE_SECTIONS
  - Rule `memory-discipline.md` : frontière memory↔vault canonique
  - CLAUDE.md : 2 lignes vault structure + standard qualité
  - Notes vault enrichies : ia_back, neo_ia, bdd, neoteem-brain (détails composants Claude Code)
  - Memory project_*.md : 4 fichiers slimmés (pointeurs vers vault 1-Projets/)
- **Devil's advocate** : critique `/done` sauvée dans `Knowledge/critiques/`, 3 bloquants corrigés
- **Source** : Analyse Eliott Meunier + recherche MCP servers + advisor

## 2026-05-09 — Structure holistique vault + skill /done + standard qualité

- **Ajoutées** :
  - `0-Inbox/` — dossier capture rapide
  - `1-Projets/Claude-Forge/Claude-Forge.md` — contexte projet forge
  - `1-Projets/Neoteem/Neoteem.md` — contexte projet Neoteem
  - `1-Projets/Neoteem/ia_back/ia_back.md` — contexte repo ia_back
  - `1-Projets/Neoteem/neo_ia/neo_ia.md` — contexte repo neo_ia
  - `1-Projets/Neoteem/neoteem-brain/neoteem-brain.md` — contexte repo neoteem-brain
  - `1-Projets/Neoteem/bdd/bdd.md` — contexte repo bdd
  - `1-Projets/Expertise-IA/Expertise-IA.md` — projet vision expert IA
  - `2-Casquettes/Raphael-Picard.md` — profil holistique complet
  - `2-Casquettes/Famille.md` — casquette famille
  - `2-Casquettes/Gaming.md` — casquette gaming
  - `Templates/context-projet.md` — template note de contexte projet
  - `Templates/context-casquette.md` — template note de contexte casquette
- **Modifiées** : Rule `forge-brain-proactive.md` — standard qualité (4-6 aliases, résumé, wikilinks) + routage dossiers 0/1/2
- **Skills** : `/done` créée — métacognition fin de session (extraction décisions/faits/préférences)
- **Source** : Analyse vidéo Eliott Meunier "Son système IA remplace une équipe entière" — ontologie par utilité, contexte holistique, /done auto-update

## 2026-05-08 — Erreur paths hardcodés multi-poste

- **Ajoutées** : `Knowledge/erreurs/erreur-settings-paths-hardcodes-multi-poste.md` — bug paths absolus user-spécifiques dans settings.json + hooks Python + marker files, cassent quand on pull sur un autre poste
- **Source** : premier usage de claude-forge sur poste perso (rapha) après pull depuis poste pro (raphael.picard_neote) — flot d'erreurs `Python was not found` + guard vault-query bloqué en permanence

## 2026-05-08 — Skill reasoning-cache + template raisonnement

- **Ajoutees** : `Templates/raisonnement.md` — template pour noter les chaines de raisonnement validees
- **Modifiees** : `00-Hub/MOC-Techniques.md` — section "Raisonnements caches" ajoutee avec lien vers Knowledge/raisonnements/
- **Source** : creation skill reasoning-cache (chain-of-thought caching au niveau tooling)

## 2026-05-08 — Base de connaissances Agents IA complète

- **Ajoutées** : `04-Techniques/agents/` — 6 notes (Agents IA MOC, frameworks, architecture, automation, évaluation, sécurité)
- **Leaders** : 6 fiches agents dans `05-Leaders/` (Shunyu Yao, Andrew Ng, Lilian Weng, Jim Fan, Simon Willison, Ethan Mollick)
- **Synthèse** : `techniques-inedites.md` — 8 combinaisons innovantes RAG × Agents jamais faites
- **cc-news** : section Agents IA & Automation leaders ajoutée (12 sources)
- **CLAUDE.md** : v1.9, mindset Jarvis/Innovateur ajouté
- **Source** : recherche via 5 agents parallèles (frameworks, architecture, leaders, automation, évaluation)

## 2026-05-08 — Base de connaissances RAG complète

- **Ajoutées** : `04-Techniques/rag/` — 7 notes (RAG MOC, chunking, embeddings, architecture, metadata, reranking, vector-databases)
- **Leaders** : 10 fiches RAG dans `05-Leaders/` (Jonas Roman, Omar Khattab, Douwe Kiela, Jerry Liu, Harrison Chase, Han Xiao, Chip Huyen, Greg Kamradt, Nils Reimers, James Briggs)
- **Synthèses** : `rag-obsidian-claude-video-analyse.md` (analyse critique vidéo YouTube), `outils-portabilite-forge.md` (defuddle, yt-dlp)
- **cc-news** : section RAG & Embeddings leaders ajoutée (9 sources)
- **Source** : recherche approfondie via 5 agents parallèles (chunking, embeddings, architecture, experts, metadata) + analyse vidéo YouTube RAG+Obsidian+Claude

## Liens


## 2026-05-21 — Capitalisation Code with Claude 2026 (keynote SF + London)

- **Créées** :
  - `01-Claude/Code/features/Self-Hosted Sandboxes.md` — Public beta London, 4 providers (Cloudflare/Modal/Vercel/Daytona), architecture queue
  - `01-Claude/Code/features/MCP Tunnels.md` — Research preview London, tunnel outbound sécurisé vers MCP privés
- **Enrichies** :
  - `Code with Claude 2026.md` — Stats transcription (20h/semaine, 17x API, task horizon), section London, framework 16 features, quotes Boris/Dianne
  - `Code with Claude Conference.md` — Speakers London confirmés, annonces spécifiques London, Extended 20 mai
  - `Dreaming Managed Agents.md` — Limites techniques (100 sessions, header API, modèles supportés), démo Lumara
  - `Managed Agents.md` — London features, webhooks 8 events, Outcomes params, Advisor Strategy, clients keynote
  - `CC mai 2026 - Code with Claude.md` — London drop (Self-Hosted Sandboxes + MCP Tunnels + enrichissements)
- **Source** : Transcription Whisper vidéo YouTube (427 segments, 47 min) + 142 captures d'écran + blogs tiers (Chris Ebert, Simon Willison, Dotzlaw, inaiwetrust, dev.to) + page officielle London
