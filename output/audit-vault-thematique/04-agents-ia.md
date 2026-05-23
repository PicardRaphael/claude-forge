# Audit Vault — Thème : Agents IA (non Claude Code)

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md`
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème large, PAS bloqué sur Anthropic) :
>    - **Sources primaires agents IA** (les meilleurs du domaine, single source acceptable) : **Andrew Ng (4 agentic design patterns, Coursera)**, **Lilian Weng (VP Research OpenAI, blog canonical agents)**, **Harrison Chase (LangChain/LangGraph)**, **Jerry Liu (LlamaIndex)**, **Shunyu Yao (ReAct, Tree of Thoughts, Chief AI Scientist Tencent)**, **Joao Moura (CrewAI founder)**, **Yohei Nakajima (BabyAGI)**, **Chi Wang (AutoGen/AG2, Google DeepMind)**, **Jim Fan (NVIDIA, Foundation Agent, Voyager)**, **David Shapiro (ACE Framework)**, **Div Garg (MultiOn, browser agents)**
>    - **Papers académiques arXiv** = single source acceptable (ReAct, ToT, Voyager, Constitutional AI, etc.)
>    - **Docs officielles** frameworks (LangChain, CrewAI, AutoGen, LlamaIndex) sur LEUR produit = single source
>    - **Anthropic** = single source uniquement sur Agent SDK / Claude Code (cas spécifique), pas sur agents IA en général
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **⚠️ Risque spécifique ce thème** : confusion concepts cross-frameworks (LangGraph, CrewAI, AutoGen, BabyAGI, MultiOn, etc.) — vérifier chaque pattern attribué au bon framework, pas mélanger.
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `feedback_regle_scope_pas_universelle`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Navigation vault — où lire selon le cas

| Si tu cherches... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines |
|-------------------|------------------------------------------------------------------|
| Méthode d'audit thématique générale | `[[methode-analyser-repo]]` (section ORDRE CANONIQUE A→B→C→D→E) |
| Doctrine agents Claude Code | `[[comment-creer-agent]]` (2-agent Justin Young sans split, Sonnet/Opus split forge, Brad Abrams Advisor) |
| Doctrine agents IA généralistes vault | Notes `04-Techniques/agents/*` + `[[Agents IA]]` MOC |
| Harness engineering (Hashimoto popularise, Böckeler formalise) | `[[harness-engineering]]` + `[[comment-creer-hook]]` section Guides+Sensors |
| Sources primaires agents IA (Ng, Weng, Chase, Liu, Yao, Moura) | Voir hiérarchie sources ci-dessus + `05-Leaders/agents/*` |
| Pattern 2-agent / multi-agent / sub-agent | `[[comment-creer-agent]]` + `[[subagent-explore-then-edit]]` + `[[limites-subagents-claude-code]]` |
| Comment éviter erreurs d'audit (attribution croisée frameworks) | `[[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]]` |

**N'oublie pas de regarder aussi** :
- `05-Leaders/agents/*` pour fiches leaders agents IA (Andrew Ng, Lilian Weng, Harrison Chase, etc.)
- `Knowledge/erreurs/*` pour pièges d'audit passés
- `01-Claude/Cowork/*` si pattern agents proches Cowork/Dispatch
- `[[mcp-vs-skills-doctrine]]` pour la couche MCP qui sert les agents

## Scope

**Dossier** : `04-Techniques/agents/` + `04-Techniques/chatbot/`

**Notes à auditer (~22)** :

`04-Techniques/agents/` :
1. `Agents IA` (note principale)
2. `agents-architecture`
3. `agents-automation`
4. `agents-evaluation`
5. `agents-frameworks`
6. `agents-securite`
7. `decoupe-agents-anti-crash`
8. `harness-engineering`
9. `limites-subagents-claude-code`
10. `mass-multi-agent-system-search`
11. `prompt-armor`
12. `prompt-rewriter-pattern`
13. `subagent-explore-then-edit`
14. `technique-dreaming-cross-session`
15. `technique-shared-agent-memory`

`04-Techniques/chatbot/` (architectures multi-agents) :
16. `architecture-autogen`
17. `architecture-claude-api`
18. `architecture-crewai`
19. `architecture-gemini-api`
20. `architecture-langgraph`
21. `architecture-openai-api`
22. `index-architectures`
23. `pattern-orchestrateur`
24. `pattern-pipeline`
25. `pattern-single-agent-multi-tool`
26. `pattern-swarm`

## Hiérarchie experts (priorité ce thème)

### Liste actuelle forge

**Anthropic** (P1 pour agents Anthropic-specific) :
- Boris Cherny, Justin Young, Thariq Shihipar, Erik Schluntz (déjà dans liste Claude Code)

**Frameworks reconnus** (P1) :
- Harrison Chase (LangChain / LangGraph)
- Jerry Liu (LlamaIndex agents)
- Chi Wang (Microsoft AutoGen)
- Joao Moura (CrewAI)
- Yohei Nakajima (BabyAGI)
- Shunyu Yao (ReAct paper)
- David Shapiro (autonomous agents)

**Académique** (P2) :
- Lilian Weng (OpenAI, blog agents)
- Jim Fan (NVIDIA, Voyager Minecraft agent)
- Andrew Ng (DeepLearning.AI agent courses)
- Div Garg (MultiOn)

**Software architecture** (P3) :
- Martin Fowler + Birgitta Böckeler
- Hashimoto (Ghostty)
- Addy Osmani (Harness Engineering)

### Étape 0 — Valider/étendre

WebSearch : "AI agent framework expert 2026", "multi-agent system researcher", "LangGraph vs CrewAI vs AutoGen", "agentic engineering thought leader 2026", "harness engineering authors".

## Sources spécifiques

### Papers (arXiv)
- "ReAct: Synergizing Reasoning and Acting" (Yao 2022)
- "Toolformer" (Schick 2023)
- "Voyager: Open-Ended Embodied Agent" (Wang 2023)
- "AutoGPT papers" (multi-agent autonomy)
- "MASS Multi-Agent System Search" — vérifier paper original
- "Generative Agents: Interactive Simulacra" (Park 2023)
- "AutoGen" paper Microsoft

### Officiel frameworks
- python.langchain.com (LangChain)
- langchain-ai.github.io/langgraph
- docs.llamaindex.ai
- microsoft.github.io/autogen
- docs.crewai.com
- platform.openai.com/docs/assistants (OpenAI Assistants API)
- ai.google.dev (Gemini Function Calling)

### Blogs
- lilianweng.github.io (Lilian Weng — "LLM Powered Autonomous Agents" canonical post)
- harrisonchase posts (LangChain blog)
- jerry liu posts (LlamaIndex)
- jim fan tweets / posts NVIDIA

### Vidéos YouTube
- Harrison Chase keynotes (LangChain Interrupt)
- Andrew Ng "Agentic AI" courses DeepLearning.AI
- Jim Fan talks
- LangChain Interrupt conference 2024-2026

## Claims à vérifier

### Architectures
- Orchestrateur / Pipeline / Swarm / Single-agent multi-tool : convergence définitions ?
- AutoGen vs CrewAI vs LangGraph : verbatim comparaisons ?
- Quand utiliser quel framework — recommandations convergent ?

### Patterns spécifiques
- `prompt-armor` — source ? (vérifier convergence sécu agents)
- `harness-engineering` — Hashimoto + Osmani convergent ?
- `mass-multi-agent-system-search` — paper original existe ?
- `technique-dreaming-cross-session` — pattern reconnu ou forge ?
- `technique-shared-agent-memory` — pattern ou forge ?

### Sécurité agents
- "Lethal trifecta" (Thariq + Simon Willison) — convergence sources ?
- Prompt injection prevention — convergence techniques ?

### Stats
- LangChain Terminal Bench 52.8% → 66.5% (vérifié déjà avec Fowler/Böckeler — confirmer)
- Forge AI vs Claude Code 79.8% vs 58% (Addy Osmani — confirmer)
- Records production multi-agent (s'il y a des claims chiffrées)

## Étape F — Propagation Agents IA

Si modifs notes vault :

**Forge** :
- Notes Claude Code (overlap : 2-agent Justin Young, harness > model)
- Skills si patterns mentionnés
- CLAUDE.md (référence patterns)

**Repos applicatifs** :
- neo_ia : utilise patterns multi-agents (NeoChat, NeoMail, NeoDoc)
- Architectures `pattern-orchestrateur`, `pattern-pipeline` peuvent être appliquées
- Vérifier si neo_ia documents internes citent ces patterns

**Backlinks** :
- `get_backlinks` pour notes principales

## Output

`output/audit-vault-thematique/04-agents-ia/`

---

**Commence par étape 0. advisor() aux transitions.**
