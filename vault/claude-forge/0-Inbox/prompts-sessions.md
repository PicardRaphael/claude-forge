---
titre: "Prompts Sessions — Restructuration + Recherche"
resume: "4 prompts prêts à copier-coller pour les 4 prochaines sessions"
aliases:
  - "prompts sessions"
  - "session prompts"
type: context
status: active
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---
Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md.

Objectif : restructurer le vault pour des notes atomiques, dossiers thématiques, aliases riches. Consulte advisor + devil AVANT de commencer les migrations.

Étapes :
1. Audit wikilinks global — scanner les liens orphelins dans tout le vault
2. 03-Modeles/ — fusionner anthropic/ + claude/ en un seul dossier anthropic/
3. 02-Concurrents/ — restructurer : codex/ → openai/ (ChatGPT.md + OpenAI Codex.md fusionné), gemini-cli/ → google/ (Gemini.md + Gemini CLI.md)
4. 05-Leaders/ — créer sous-dossiers (rag/, agents/, fine-tuning/, prompt/, industrie/, claude-code/) et déplacer les 38 notes
5. 01-Claude-Code/ — fusionner les 16 changelogs en notes mensuelles, déplacer Cowork GA + Managed Agents vers features/
6. MOCs — réparer MOC-Modeles (7+ liens orphelins), MOC-Concurrents
7. Tags — normaliser les doublons (voir plan Phase 4)

Règles : le mapping "où écrire quoi" est dans .claude/rules/forge-brain-proactive.md. 1 concept = 1 note. Max 5 sections H2. Aliases min 4-6 avec domaine d'expertise. CHANGELOG.md obligatoire.
## Session 1 — Restructuration vault

```
Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md.

Objectif : restructurer le vault pour des notes atomiques, dossiers thématiques, aliases riches. Consulte advisor + devil AVANT de commencer les migrations.

Étapes :
1. Audit wikilinks global — scanner les liens orphelins dans tout le vault
2. 03-Modeles/ — fusionner anthropic/ + claude/ en un seul dossier anthropic/
3. 02-Concurrents/ — restructurer : codex/ → openai/ (ChatGPT.md + OpenAI Codex.md fusionné), gemini-cli/ → google/ (Gemini.md + Gemini CLI.md)
4. 05-Leaders/ — créer sous-dossiers (rag/, agents/, fine-tuning/, prompt/, industrie/, claude-code/) et déplacer les 38 notes
5. 01-Claude-Code/ — fusionner les 16 changelogs en notes mensuelles, déplacer Cowork GA + Managed Agents vers features/
6. MOCs — réparer MOC-Modeles (7+ liens orphelins), MOC-Concurrents
7. Tags — normaliser les doublons (voir plan Phase 4)

Règles : le mapping "où écrire quoi" est dans .claude/rules/forge-brain-proactive.md. 1 concept = 1 note. Max 5 sections H2. Aliases min 4-6 avec domaine d'expertise. CHANGELOG.md obligatoire.
```

## Session 2 — cc-news test + prompts + aliases

```
Objectif : tester le refactor cc-news + enrichir les prompts + aliases leaders.

Étapes :
1. Lancer /cc-news concurrents — vérifier que les 11 agents parallèles fonctionnent et captent GPT-5.5
2. Avec les résultats : créer les fiches modèles manquantes dans 03-Modeles/ (GPT-5.5, Gemini 3, Llama 4, DeepSeek R1, Qwen 3)
3. Mettre à jour les fiches concurrents obsolètes dans 02-Concurrents/
4. 07-Prompts/techniques/ — créer 1 note par technique de prompting + index-prompting.md (quelle technique pour quand)
5. 05-Leaders/ — enrichir les aliases de chaque leader avec domaine d'expertise (ex: "expert fine-tuning", "spécialiste RAG")
6. Mettre à jour MOC-Techniques et MOC-Modeles avec les nouvelles notes
```

## Session 3 — Recherche architectures chatbot/multi-agent

```
Objectif : recherche approfondie sur les architectures chatbot et multi-agent. Consulte advisor + devil sur la structure des notes AVANT de créer.

Lancer 4 agents de recherche parallèles :
- Agent 1 : Claude API / Anthropic SDK — tool_use, managed agents, orchestrator patterns, system prompts
- Agent 2 : OpenAI API — Agents SDK, function calling, Assistants API, swarm, handoffs
- Agent 3 : LangGraph — StateGraph, supervisor, hierarchical, swarm, checkpointing, memory
- Agent 4 : CrewAI + AutoGen + Gemini API — crews, GroupChat, ADK, A2A protocol

Avec les résultats, créer dans 04-Techniques/chatbot/ :
- 1 note par framework : architecture-claude-api.md, architecture-openai-api.md, architecture-langgraph.md, architecture-crewai.md, architecture-gemini-api.md, architecture-autogen.md
- 1 note par pattern : pattern-orchestrateur.md, pattern-swarm.md, pattern-pipeline.md, pattern-hierarchique.md, pattern-single-agent-multi-tool.md, pattern-rag-agent.md
- 1 index : index-architectures.md (tableau "quel framework pour quel cas d'usage")

Chaque note couvre : avec/sans orchestrateur, avec/sans tools, system prompts adaptés, coûts, quand l'utiliser.

Parallélisable avec Session 2.
```

## Session 4 — Leaders agents + cc-news + audit final

```
Objectif : compléter les leaders multi-agent, enrichir cc-news, audit final.

Étapes :
1. Rechercher les leaders multi-agent manquants : Chi Wang (AutoGen), Yohei Nakajima (BabyAGI), Dario Amodei (Anthropic), David Shapiro (ACE Framework), Div Garg (MultiOn)
2. Créer les fiches dans 05-Leaders/agents/
3. Enrichir cc-news references/domain-agents.md avec les nouveaux leaders + queries architectures
4. Mettre à jour MOC-Techniques avec toutes les notes chatbot
5. Lancer /vault-audit pour audit qualité global (aliases, tags, wikilinks, résumés)
6. Lancer devil's advocate sur l'ensemble du vault restructuré

Dépend de Sessions 2 + 3.
```

## Liens

