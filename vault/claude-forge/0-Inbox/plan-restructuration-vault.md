---
titre: "Plan Restructuration Vault — Session Suivante"
resume: "Plan complet pour restructurer le vault forge-brain : concurrents, modèles, tags, aliases, MOCs, notes atomiques"
aliases:
  - "plan restructuration"
  - "vault restructure plan"
  - "plan vault"
type: context
status: active
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Objectif

Restructurer le vault forge-brain pour : notes atomiques (1 sujet = 1 note), aliases riches (domaine + nom), tags normalisés, MOCs à jour, zéro lien orphelin.

## Validations obtenues

- **Advisor** : atomicité > taille. 1 concept = 1 note. Si >5 sections H2 → splitter.
- **Devil's advocate** : LIVRER AVEC CORRECTIONS. 4 bloquants identifiés (voir ci-dessous).
- **Raphael** : 1 dossier/entreprise, modèles séparés dans 03-Modeles/, notes courtes.

## Bloquants devil's advocate à résoudre

1. **Audit wikilinks AVANT migration** — scanner `[[GPT-5.3 Codex]]`, `[[OpenAI Codex]]`, `[[Gemini CLI]]` dans tout le vault. Chaque lien doit avoir un plan de redirection.
2. **MOC-Modeles déjà cassé** — 7+ liens orphelins (`[[GPT-5.4]]`, `[[Opus 4.6]]`, `[[Gemini 3.1 Pro]]`, `[[Grok 4.3 Beta]]`...). Réparer AVANT d'ajouter.
3. **Consolider `anthropic/` + `claude/` dans 03-Modeles/** — 2 dossiers pour le même provider. Unifier en `anthropic/` d'abord.
4. **Fusionner `GPT-5.3 Codex.md` + `OpenAI Codex.md`** — 2 snapshots contradictoires (5.3 vs 5.4). Réconcilier, pas juste supprimer un.

## Phase 1 — Pré-migration (5 min)

1. Scanner tous les wikilinks orphelins : `search_brain("[[GPT")` + `search_brain("[[Gemini")` + `search_brain("[[Grok")`
2. Lister les liens cassés dans MOC-Modeles et MOC-Concurrents
3. Backup mental : noter les aliases à préserver

## Phase 2 — 02-Concurrents/ restructuration

### Structure cible
```
02-Concurrents/
  openai/
    ChatGPT.md            ← le produit app (features, plans, pricing)
    OpenAI Codex.md       ← le CLI/coding tool (fusionné des 2 notes actuelles)
  google/
    Gemini.md             ← le produit app (AI Studio, features, plans)
    Gemini CLI.md         ← le CLI tool (déplacé depuis gemini-cli/)
  cursor/
    Cursor.md             ← existant, vérifier qualité
  copilot/
    GitHub Copilot.md     ← existant, vérifier qualité
  xai/
    xAI Grok.md           ← existant, vérifier qualité
```

### Actions
- Créer `openai/ChatGPT.md` (nouveau — le produit global)
- Fusionner `GPT-5.3 Codex.md` + `OpenAI Codex.md` → `openai/OpenAI Codex.md` (réconcilier 5.3 vs 5.4 vs 5.5)
- Supprimer le dossier `codex/`
- Créer `google/Gemini.md` (nouveau — le produit global)
- Déplacer `gemini-cli/Gemini CLI.md` → `google/Gemini CLI.md`
- Supprimer le dossier `gemini-cli/`
- PAS de `OpenAI API.md` séparé (devil's advocate a flag le risque de stub vide)

## Phase 3 — 03-Modeles/ extension

### Structure cible
```
03-Modeles/
  anthropic/              ← fusionner anthropic/ + claude/
    Opus 4.7.md
    Sonnet 4.6.md
    Haiku 4.5.md
    Claude Mythos Preview.md
  openai/
    GPT-5.5.md            ← NOUVEAU (recherche web nécessaire)
  google/
    Gemini 3.md           ← NOUVEAU
  meta/
    Llama 4.md            ← NOUVEAU
  deepseek/
    DeepSeek R1.md        ← NOUVEAU (info déjà dans fine-tuning-models)
  qwen/
    Qwen 3.md             ← NOUVEAU (info déjà dans fine-tuning-models)
```

### Actions
- Déplacer `claude/*.md` → `anthropic/`
- Supprimer le dossier `claude/`
- Créer les 5 notes modèles avec recherche web cc-news
- NE PAS créer Mistral Large 3 ni Grok sauf si info fraîche dispo

## Phase 4 — Tags normalisés

### Tags à fusionner
- `#domaine/technique` (11) → fusionner dans `#type/technique` (48)
- `#domaine/prompting` (1) + `#domaine/prompts` (1) → fusionner dans `#domaine/prompt-engineering` (5)
- `#domaine/leaders` (1) → supprimer (redondant avec `#type/leader`)
- Arrays YAML cassés → convertir en liste propre

### Tags canon à utiliser
- Type : `#type/leader`, `#type/technique`, `#type/concurrent`, `#type/modele`, `#type/index`, `#type/knowledge`, `#type/erreur`, `#type/context`
- Domaine : `#domaine/ia`, `#domaine/claude-code`, `#domaine/fine-tuning`, `#domaine/rag`, `#domaine/agents`, `#domaine/prompt-engineering`, `#domaine/industrie`
- Erreur : `#erreur/skill`, `#erreur/agent`, `#erreur/hook`, `#erreur/comportement`, `#erreur/infra`

## Phase 5 — Aliases leaders enrichis

### Problème actuel
Les aliases leaders sont nom-based seulement. Exemples :
- Daniel Han : `daniel han, danielhanchen, Unsloth creator, Unsloth AI` — manque "expert fine-tuning", "fine-tuning speed"
- Chip Huyen : `Chip Huyen, AI Engineering book, huyenchip` — manque "ML systems", "production ML"

### Pattern d'aliases à appliquer (pour chaque leader)
1. Nom complet (FR/EN)
2. Handle X/GitHub
3. Outil/contribution principale
4. Domaine d'expertise en mots-clés
5. Livre/cours si applicable

Exemple Daniel Han amélioré :
```yaml
aliases:
  - "daniel han"
  - "danielhanchen"
  - "Unsloth creator"
  - "Unsloth AI"
  - "fine-tuning speed expert"
  - "fast fine-tuning"
```

## Phase 6 — MOCs réparation

- MOC-Modeles : réparer les 7+ liens orphelins, ajouter les nouveaux modèles
- MOC-Concurrents : mettre à jour avec la nouvelle structure
- CHANGELOG.md : documenter toute la migration

## Phase 7 — Audit qualité notes existantes

Pour chaque note dans 02-Concurrents/, 03-Modeles/, 05-Leaders/ :
- Vérifier atomicité (1 sujet = 1 note, max 5 sections H2)
- Vérifier aliases (min 4-6, incluant domaine)
- Vérifier `derniere-maj` (>7 jours = stale)
- Vérifier wikilinks (min 2)
- Vérifier resume (spécifique, pas générique)

## Ordre d'exécution recommandé

1. Phase 1 (pré-migration) — 5 min
2. Phase 3 (03-Modeles/ consolider anthropic) — 5 min
3. Phase 2 (02-Concurrents/) — 15 min
4. Phase 3 suite (nouveaux modèles avec cc-news) — 10 min
5. Phase 6 (MOCs) — 5 min
6. Phase 5 (aliases) — 10 min, peut être parallélisé
7. Phase 4 (tags) — via vault-audit, parallélisable
8. Phase 7 (audit qualité) — via vault-audit

## Liens

- [[MOC-Modeles]]
- [[MOC-Concurrents]]
- [[erreur-skill-monolithique-sans-references]]
- [[context-actuel]]


---

## DIAGNOSTIC GLOBAL — Toutes les sections

### 01-Claude-Code/ (35 notes)

**Problèmes :**
- **16 changelogs individuels** (CC v2.1.110 à v2.1.136) — trop granulaire ? Consolider en notes mensuelles ?
- **Features + deprecations mélangées** dans `features/` — séparer en `features/` et `deprecations/` ?
- `claude-desktop-preferences` et `mcp-obsidian-brain-v2` sont des techniques, pas des features CC

**Actions proposées :**
- Évaluer si les changelogs individuels apportent de la valeur ou si des notes mensuelles suffisent
- Déplacer les deprecations dans un sous-dossier `deprecations/` ou les taguer distinctement
- Déplacer les faux features vers `04-Techniques/`

### 04-Techniques/ (50 notes — plus grosse section)

**Structure actuelle :** bien organisée avec `rag/`, `agents/`, `prompt-engineering/`, `patterns/`, `fine-tuning/`, `context-engineering/`

**Problèmes :**
- Notes orphelines à la racine : `agentic-engineering-karpathy`, `best-practices-claude-code-leaders`, `config-guardian-pattern`, `forge-prompt-machine`, `mcp-obsidian-brain-v2`, etc.
- Certaines de ces notes sont peut-être dans `patterns/` ou devraient l'être

**Actions proposées :**
- Déplacer chaque note orpheline dans le bon sous-dossier
- Vérifier que chaque sous-dossier a un scope clair

### 05-Leaders/ (38 notes)

**Problème principal : aliases pauvres**
- La plupart n'ont que nom + handle + outil créé
- Manquent : domaine d'expertise, mots-clés de recherche, termes que l'utilisateur utiliserait

**Actions proposées :**
- Enrichir les aliases de CHAQUE leader avec 1-2 termes domaine
- Pattern : nom, handle, outil, "expert X", "spécialiste Y"
- Parallélisable : 1 agent peut traiter les 38 notes

### 06-Industrie/ (8 notes)

**Problèmes :**
- `Cowork GA` et `Managed Agents` sont des **features Anthropic**, pas de l'industrie → déplacer vers `01-Claude-Code/features/`
- `anthropic-avril-2026` et `industrie-mai-2026` sont des **snapshots temporels** qui pourrissent. Pas atomiques (mélangent 6+ sujets)
- `Agent Skills Spec` est une spec technique → `04-Techniques/` ou `06-Industrie/` ?

**Actions proposées :**
- Déplacer `Cowork GA` + `Managed Agents` → `01-Claude-Code/features/`
- Splitter les snapshots temporels en notes atomiques par sujet (si encore pertinents)
- Garder `Agent Skills Spec` dans `06-Industrie/` (c'est un standard cross-industry)

### 07-Prompts/ (2 notes — quasi vide)

**Problème :** seulement 2 system prompts. Les techniques de prompting sont dans `04-Techniques/prompt-engineering/`.

**Actions proposées :**
- Soit enrichir avec les prompts réutilisables créés dans d'autres sessions
- Soit fusionner dans `04-Techniques/prompt-engineering/` et supprimer le dossier
- Décision à prendre avec Raphael

### Knowledge/ (18 notes)

**Problèmes :**
- 5 sous-dossiers quasi vides (juste `_index.md`) : `evolutions/`, `explorations/`, `questions/`, `raisonnements/`, `reviews/`
- Les `_index.md` sont des placeholders sans contenu utile

**Actions proposées :**
- Garder les dossiers (ils seront remplis par les skills : `skill-evolve` → `evolutions/`, `reasoning-cache` → `raisonnements/`, `forge-review` → `reviews/`)
- Supprimer les `_index.md` vides — Obsidian n'a pas besoin d'index pour afficher un dossier

### 00-Hub/ MOCs (8 notes)

**Problème critique : MOC-Modeles cassé**
- 7+ liens orphelins : `[[GPT-5.4]]`, `[[Opus 4.6]]`, `[[Gemini 3.1 Pro]]`, `[[Grok 4.3 Beta]]`, `[[GPT-5.3 Codex Spark]]`, `[[Gemini 3.0 Flash]]`, `[[Grok 5]]`
- Aucun de ces fichiers n'existe

**Actions proposées :**
- Supprimer les liens orphelins
- Ajouter les liens vers les nouvelles notes modèles créées
- Vérifier TOUS les MOCs pour liens orphelins

---

## Ordre d'exécution révisé (global)

1. **Audit wikilinks global** — scanner tous les liens orphelins dans tout le vault
2. **00-Hub/ MOCs** — réparer MOC-Modeles + MOC-Concurrents
3. **03-Modeles/** — consolider anthropic/claude, ajouter modèles concurrents
4. **02-Concurrents/** — restructurer par entreprise
5. **06-Industrie/** — déplacer features Anthropic, splitter snapshots
6. **01-Claude-Code/** — trier features vs deprecations, évaluer changelogs
7. **04-Techniques/** — ranger notes orphelines dans sous-dossiers
8. **05-Leaders/** — enrichir aliases (parallélisable)
9. **07-Prompts/** — décider : enrichir ou fusionner
10. **Knowledge/** — nettoyer _index vides
11. **Tags** — normaliser via vault-audit
12. **Audit final** — vault-audit qualité globale

---

## CONSIGNES IMPÉRATIVES — Prochaine session

### 1. Advisor + Devil's advocate OBLIGATOIRES

AVANT de toucher quoi que ce soit :
1. Lancer **advisor** avec la proposition d'architecture dossiers
2. Lancer **devil's advocate** avec la proposition
3. Appliquer les corrections
4. Raphael valide les questions ouvertes

Ne JAMAIS commencer l'exécution sans double validation.

### 2. Objectif d'optimisation

L'architecture du vault doit optimiser :
- **Moins de tokens** — notes courtes, atomiques, pas de blabla
- **Moins de contexte chargé** — quand on search_brain, les résultats doivent être pertinents et courts
- **Rapidité de recherche** — aliases riches pour que search_brain trouve en 1 query
- **Performance des agents** — quand un agent lit une note, il doit comprendre le sujet en <500 caractères de résumé

### 3. Architecture dossiers — OÙ ÉCRIRE QUOI

Règle : **chaque dossier = un thème clair**. Pas de dossiers vides. Pas de notes isolées à la racine d'un dossier parent.

| Je crée une note sur... | Dossier | Exemple |
|------------------------|---------|---------|
| Feature/update Claude Code | `01-Claude-Code/features/` | Computer Use CC.md |
| Deprecation Claude Code | `01-Claude-Code/deprecations/` | Deprecation Haiku 3.md |
| Changelog CC (par mois) | `01-Claude-Code/changelog/` | CC mai 2026.md |
| Best practice CC | `01-Claude-Code/best-practices/` | delegate-guard-pattern.md |
| Agent CC documenté | `01-Claude-Code/agents/` | Agent — skill-creator.md |
| Produit concurrent (app, CLI) | `02-Concurrents/<entreprise>/` | openai/ChatGPT.md |
| Modèle IA (specs, benchmarks) | `03-Modeles/<provider>/` | openai/GPT-5.5.md |
| Technique RAG | `04-Techniques/rag/` | rag-chunking.md |
| Technique agents | `04-Techniques/agents/` | agents-architecture.md |
| Technique prompt | `04-Techniques/prompt-engineering/` | Adaptive Thinking.md |
| Technique fine-tuning | `04-Techniques/fine-tuning/` | fine-tuning-techniques-peft.md |
| Pattern/workflow réutilisable | `04-Techniques/patterns/` | Workflow Boris.md |
| Context engineering | `04-Techniques/context-engineering/` | Context Engineering.md |
| Leader/expert (personne) | `05-Leaders/` | Daniel Han.md |
| News industrie (événement, funding) | `06-Industrie/` | Anthropic Revenue 30B.md |
| Feature Anthropic (produit, pas CC) | `06-Industrie/` | Cowork GA.md → à reclasser |
| Prompt réutilisable / system prompt | `07-Prompts/system-prompts/` | System Prompt Claude Code.md |
| Erreur commise | `Knowledge/erreurs/` | erreur-skill-monolithique.md |
| Critique devil's advocate | `Knowledge/critiques/` | critique-2026-05-09-skill-done.md |
| Synthèse d'analyse | `Knowledge/syntheses/` | neoteem-agentic-engineering-mapping.md |
| Raisonnement multi-étapes | `Knowledge/raisonnements/` | (via /reasoning-cache) |
| Évolution skill proposée | `Knowledge/evolutions/` | (via /skill-evolve) |
| Review stratégique forge | `Knowledge/reviews/` | (via /forge-review) |
| Projet en cours | `1-Projets/<nom>/` | Expertise-IA.md |
| Casquette de vie | `2-Casquettes/` | Raphael-Picard.md |
| Working memory / plan | `0-Inbox/` | context-actuel.md |

### 4. Règles de dossiers

- **Pas de dossier vide sans raison** — un dossier existe parce qu'une skill y écrit (`Knowledge/raisonnements/` existe car `/reasoning-cache` y écrit)
- **Pas de notes orphelines à la racine** — chaque note doit être dans un sous-dossier thématique
- **1 dossier = 1 thème clair** — si on ne peut pas décrire le dossier en 3 mots, il est mal nommé
- **Dossiers par entreprise pour concurrents et modèles** — `openai/`, `google/`, `anthropic/`, pas par produit

### 5. Règles de notes

- **1 concept = 1 note** — si >5 sections H2, splitter
- **Résumé spécifique** — pas "Note sur X", mais "X fait Y pour Z avec telle performance"
- **Aliases min 4-6** — nom FR, nom EN, handle, outil, domaine d'expertise
- **Tags normalisés** — utiliser UNIQUEMENT les tags canon (voir Phase 4 du plan)
- **Wikilinks min 2** — chaque note doit pointer vers au moins 2 autres notes
- **derniere-maj** — date ISO du jour de création/modification

### 6. Questions ouvertes pour Raphael

1. **Changelogs CC** : garder 1 note/version (16 notes) ou consolider en notes mensuelles (3-4 notes) ?
2. **07-Prompts/** : enrichir avec plus de prompts ou fusionner dans 04-Techniques/prompt-engineering/ ?
3. **Snapshots industrie** (`industrie-mai-2026`) : garder comme chronologie ou splitter en notes atomiques par sujet ?
4. **Features Anthropic** (`Cowork GA`, `Managed Agents`) : dans `01-Claude-Code/features/` ou `06-Industrie/` ?

---

## DÉCISIONS RAPHAEL (2026-05-10) — Tranchées, prêtes à exécuter

1. **05-Leaders/ → sous-dossiers par domaine** : `rag/`, `agents/`, `fine-tuning/`, `prompt/`, `industrie/`, `claude-code/`. Déplacer les 38 notes existantes dans le bon sous-dossier.
2. **01-Claude-Code/changelog/ → consolidé par mois** : fusionner les 16 notes individuelles (v2.1.110→v2.1.136) en ~3 notes mensuelles.
3. **Cowork GA + Managed Agents → `01-Claude-Code/features/`** : ce sont des features Anthropic, pas de l'industrie.
4. **07-Prompts/ → enrichir** : 1 note par technique de prompting dans `07-Prompts/techniques/` + 1 note index `index-prompting.md` qui dit quelle technique pour quel cas d'usage.

**Le mapping "où écrire quoi" vit dans `.claude/rules/forge-brain-proactive.md`** (déjà mis à jour). Pas dans ce plan. Ce plan est un one-shot pour la migration.

## Prompt prochaine session (FINAL)

> Lis `vault/claude-forge/0-Inbox/plan-restructuration-vault.md`. Les 4 décisions sont tranchées par Raphael. Exécute dans cet ordre :
> 1. Audit wikilinks global (Phase 1)
> 2. 03-Modeles/ : consolider anthropic/claude → anthropic/
> 3. 02-Concurrents/ : restructurer par entreprise (openai/, google/)
> 4. 05-Leaders/ : déplacer les 38 notes dans sous-dossiers domaine
> 5. 01-Claude-Code/ : fusionner changelogs par mois, déplacer Cowork GA + Managed Agents
> 6. 07-Prompts/ : créer techniques/ avec notes atomiques + index-prompting.md
> 7. MOCs : réparer tous les liens orphelins
> 8. Tags : normaliser via vault-audit
> 9. Aliases leaders : enrichir avec domaine d'expertise
> Lance cc-news concurrents pour les nouveaux modèles (GPT-5.5, Gemini 3, etc.).

---

## Phase 10 — RECHERCHE : Architectures Chatbot & Multi-Agent

### Objectif
Recherche approfondie (même profondeur que fine-tuning) sur comment construire des chatbots et systèmes multi-agent. Capitaliser dans le vault.

### Sujets à couvrir

1. **Frameworks** — LangGraph, Claude API (Anthropic SDK), OpenAI API, CrewAI, AutoGen/AG2, Semantic Kernel
2. **Architectures multi-agent** — agent orchestrateur qui délègue vs agents pairs, supervisor vs swarm vs hierarchical
3. **Multi-tool patterns** — comment un agent choisit et utilise des outils, tool routing, MCP
4. **Chatbot patterns** — conversation management, memory, context window, streaming, RAG-augmented chat
5. **Délégation** — quand un agent doit déléguer vs faire lui-même, coût/latence des sous-agents
6. **Best practices production** — error handling, fallbacks, observabilité, coûts, rate limits
7. **Leaders à identifier** — qui sont les experts de ce domaine (Harrison Chase, Andrew Ng, etc. — certains déjà dans le vault)

### Méthode
- Lancer 3-4 agents de recherche parallèles (comme pour fine-tuning)
- Consulter advisor sur l'architecture optimale
- Consulter devil's advocate sur la proposition
- Capitaliser dans `04-Techniques/agents/` ou créer `04-Techniques/chatbot/` si assez de contenu
- Ajouter les leaders manquants dans `05-Leaders/agents/`
- Mettre à jour MOC-Techniques

### Dossier cible vault
À décider avec advisor/devil :
- `04-Techniques/agents/` (enrichir l'existant) ?
- `04-Techniques/chatbot/` (nouveau sous-dossier) ?
- `04-Techniques/multi-agent/` (nouveau sous-dossier) ?

### Détail recherche — 1 note par framework/API, architectures comparées

Pour CHAQUE framework, documenter dans une note atomique :

#### `04-Techniques/chatbot/architecture-claude-api.md`
- Anthropic SDK (Python/TS) — tool_use, system prompt, streaming, thinking, caching
- Pattern avec orchestrateur (agent principal + sub-agents via tool calls)
- Pattern sans orchestrateur (single agent, multi-tool)
- Managed Agents (Anthropic natif)
- System prompt optimal pour chaque pattern
- Coûts, limites, context window

#### `04-Techniques/chatbot/architecture-openai-api.md`
- OpenAI SDK — function calling, Assistants API, Agents SDK
- Pattern orchestrateur (Agents SDK avec handoffs)
- Pattern swarm (agents pairs)
- Threads + runs (Assistants API)
- System prompt patterns GPT
- Coûts, limites

#### `04-Techniques/chatbot/architecture-langgraph.md`
- LangGraph — StateGraph, nodes, edges, conditional routing
- Pattern supervisor (1 orchestrateur → N workers)
- Pattern hierarchical (multi-level delegation)
- Pattern swarm (agents autonomes)
- Checkpointing, memory, human-in-the-loop
- Quand LangGraph vs API directe

#### `04-Techniques/chatbot/architecture-crewai.md`
- CrewAI — agents, tasks, crews, processes
- Pattern sequential (pipeline)
- Pattern hierarchical (manager agent)
- Pattern consensual
- Tools custom, delegation entre agents
- Comparaison avec LangGraph

#### `04-Techniques/chatbot/architecture-gemini-api.md`
- Gemini API — function calling, ADK (Agent Development Kit), A2A protocol
- Pattern avec ADK orchestrator
- Pattern multi-agent A2A
- Google AI Studio vs Vertex AI
- System instructions patterns Gemini

#### `04-Techniques/chatbot/architecture-autogen.md`
- AutoGen/AG2 — ConversableAgent, GroupChat, nested chats
- Pattern conversation-driven
- Pattern group chat avec speaker selection
- Code execution intégrée

#### `04-Techniques/chatbot/index-architectures.md` (NOTE INDEX)
Tableau comparatif : quel framework pour quel cas d'usage

| Cas d'usage | Framework recommandé | Pourquoi |
|-------------|---------------------|----------|
| Chatbot simple mono-agent | Claude API / OpenAI API directe | Pas besoin de framework |
| Multi-tool avec routing | Claude API tool_use / OpenAI function calling | Natif, pas de dépendance |
| Multi-agent avec orchestrateur | LangGraph supervisor / CrewAI hierarchical | Contrôle fin du flow |
| Agents autonomes collaboratifs | AutoGen GroupChat / LangGraph swarm | Émergence de comportements |
| Pipeline séquentiel | CrewAI sequential / LangGraph | Tâches ordonnées |
| Cross-platform multi-provider | A2A protocol / custom | Interopérabilité |

#### Patterns transversaux (dans chaque note)
- **Avec orchestrateur** : 1 agent central décide qui fait quoi → contrôle, coût prévisible, single point of failure
- **Sans orchestrateur** : agents pairs se coordonnent → flexible, résilient, imprévisible
- **Avec tools** : agent appelle des fonctions/APIs → structured output, vérifiable
- **Sans tools** : pure LLM chain → plus simple, moins fiable
- **System prompts** : comment adapter le prompt selon l'architecture (orchestrateur vs worker vs peer)

### Architectures par objectif — notes séparées

En plus des notes par framework, créer des notes par **pattern d'architecture** (indépendant du framework) :

#### `04-Techniques/chatbot/pattern-orchestrateur.md`
- Architecture hub-and-spoke : 1 agent central route vers N workers spécialisés
- Quand l'utiliser : tâches bien définies, contrôle strict, coûts prévisibles
- Exemples : LangGraph supervisor, CrewAI hierarchical, Claude tool_use avec sub-calls
- System prompt orchestrateur : routing decision, task decomposition
- System prompt worker : single-task, structured output
- Anti-patterns : orchestrateur qui fait tout, workers trop couplés

#### `04-Techniques/chatbot/pattern-swarm.md`
- Architecture peer-to-peer : agents autonomes se coordonnent sans chef
- Quand l'utiliser : exploration, créativité, problèmes mal définis
- Exemples : OpenAI Swarm, AutoGen GroupChat, LangGraph swarm
- Handoff patterns : comment un agent passe la main
- Risques : boucles infinies, coûts imprévisibles, incohérence

#### `04-Techniques/chatbot/pattern-pipeline.md`
- Architecture séquentielle : chaque agent traite puis passe au suivant
- Quand l'utiliser : workflows linéaires, ETL, content pipeline
- Exemples : CrewAI sequential, LangGraph linear chain
- Gates entre étapes : validation, human-in-the-loop

#### `04-Techniques/chatbot/pattern-hierarchique.md`
- Architecture multi-niveaux : managers → team leads → workers
- Quand l'utiliser : problèmes complexes décomposables, grandes équipes d'agents
- Exemples : LangGraph hierarchical, CrewAI nested crews
- Coûts : chaque niveau multiplie les tokens

#### `04-Techniques/chatbot/pattern-single-agent-multi-tool.md`
- PAS de multi-agent : 1 seul agent avec N outils
- Quand l'utiliser : 80% des cas. La plupart des problèmes ne NÉCESSITENT PAS multi-agent
- Claude tool_use, OpenAI function calling, Gemini function calling
- System prompt optimisé pour tool routing
- Quand basculer vers multi-agent (seuils de complexité)

#### `04-Techniques/chatbot/pattern-rag-agent.md`
- Agent augmenté par RAG : retrieval + reasoning + action
- Architecture : query → retrieve → reason → act → verify
- Intégration avec chaque framework (LangGraph, Claude, OpenAI)
- RAFT pattern (fine-tuning + RAG combinés)

### Leaders architectures multi-agent — à rechercher et ajouter

Rechercher et créer des fiches pour les leaders spécifiques aux architectures agent :

| Personne | Pourquoi | Déjà dans vault ? |
|----------|----------|-------------------|
| **Harrison Chase** | LangGraph, langgraph supervisor/swarm patterns | OUI — enrichir |
| **Andrew Ng** | 4 agentic design patterns (reflection, tool use, planning, multi-agent) | OUI — enrichir |
| **Joao Moura** | CrewAI, delegation patterns | OUI — enrichir |
| **Lilian Weng** | Blog canonical sur agents (LLM Powered Autonomous Agents) | OUI — enrichir |
| **Shunyu Yao** | ReAct, Tree of Thoughts | OUI — enrichir |
| **Dario Amodei** | CEO Anthropic, vision agents, Managed Agents | NON — créer |
| **Adam Cohen Hillel** | Browserbase, Stagehand, agent browser patterns | NON — rechercher |
| **Div Garg** | MultiOn, autonomous web agents | NON — rechercher |
| **Chi Wang** | AutoGen creator, Microsoft Research | NON — rechercher |
| **Yohei Nakajima** | BabyAGI creator, agent loops | NON — rechercher |
| **Jerry Liu** | LlamaIndex agents, agentic RAG | OUI — enrichir |
| **David Shapiro** | ACE Framework, agent architectures YouTube | NON — rechercher |

Objectif : 5-8 leaders agents vérifié mondialement reconnus à ajouter dans `05-Leaders/agents/`

### Requêtes de recherche pour la Phase 10

```
multi-agent architecture patterns comparison 2026
LangGraph supervisor vs swarm vs hierarchical
OpenAI Agents SDK handoff patterns architecture
Claude API tool_use multi-agent orchestrator pattern
CrewAI vs LangGraph vs AutoGen comparison 2026
Gemini ADK agent architecture A2A protocol
when to use multi-agent vs single agent with tools
best practices production multi-agent systems
Andrew Ng agentic design patterns 2026
Harrison Chase LangGraph architecture patterns 2026
Chi Wang AutoGen AG2 Microsoft 2026
Yohei Nakajima BabyAGI agent loops 2026
site:blog.langchain.com multi-agent architecture
site:docs.anthropic.com multi-agent tool-use
```

### Ajouter à cc-news domain-agents.md

Après la recherche, enrichir `references/domain-agents.md` avec :
- Les nouveaux leaders identifiés
- Queries spécifiques architectures multi-agent
- Sources directes (docs.anthropic.com, docs.together.ai, etc.)

---

## SÉQUENCE D'EXÉCUTION — Sessions découpées

### Session 1 : Restructuration vault (prérequis pour tout le reste)
1. Audit wikilinks global
2. 03-Modeles/ : consolider anthropic/claude → anthropic/
3. 02-Concurrents/ : restructurer par entreprise
4. 05-Leaders/ : déplacer dans sous-dossiers domaine
5. 01-Claude-Code/ : changelogs mensuels, déplacer features Anthropic
6. MOCs : réparer liens orphelins
7. Tags : normaliser

**Prompt :** "Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md, section 'Session 1'. Exécute les 7 étapes dans l'ordre. Consulte advisor + devil avant de commencer les migrations."

### Session 2 : cc-news test + modèles concurrents
1. Lancer /cc-news concurrents — tester la nouvelle architecture 11 agents
2. Créer les fiches modèles manquantes (GPT-5.5, Gemini 3, etc.) avec les résultats
3. Mettre à jour les fiches concurrents obsolètes
4. 07-Prompts/ : créer techniques/ + index-prompting.md
5. Aliases leaders : enrichir avec domaine

**Prompt :** "Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md, section 'Session 2'. Lance /cc-news concurrents pour tester le refactor. Capitalise les résultats. Puis enrichis 07-Prompts et les aliases leaders."

### Session 3 : Recherche architectures chatbot/multi-agent
1. Lancer 4 agents parallèles : Claude API / OpenAI API / LangGraph / CrewAI+AutoGen+Gemini
2. Consulter advisor + devil sur l'architecture des notes
3. Créer les 7 notes par framework (04-Techniques/chatbot/)
4. Créer les 6 notes par pattern (orchestrateur, swarm, pipeline, hierarchique, single-agent, RAG-agent)
5. Créer l'index comparatif (quel framework pour quoi)

**Prompt :** "Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md, section 'Session 3'. Lance la recherche architectures chatbot/multi-agent. 4 agents parallèles. Consulte advisor + devil sur la structure des notes AVANT de créer. Capitalise dans 04-Techniques/chatbot/."

### Session 4 : Leaders multi-agent + cc-news enrichi
1. Rechercher les leaders manquants (Chi Wang, Yohei Nakajima, Dario Amodei, David Shapiro, Div Garg)
2. Créer fiches dans 05-Leaders/agents/
3. Enrichir cc-news domain-agents.md avec nouveaux leaders + queries architectures
4. Mettre à jour MOC-Techniques avec les nouvelles notes chatbot
5. Audit final vault-audit qualité globale

**Prompt :** "Lis vault/claude-forge/0-Inbox/plan-restructuration-vault.md, section 'Session 4'. Recherche les leaders multi-agent manquants. Enrichis cc-news. Audit final."