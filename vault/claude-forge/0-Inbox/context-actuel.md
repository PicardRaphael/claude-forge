---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-23 : 4 audits thématiques vault complétés en parallèle (02 prompt-eng, 03 RAG, 04 agents-IA, 06 patterns/context/stacks). Reste 05 fine-tuning + 07 leaders + 08 dogfooding."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Audits thématiques vault forge en cours (méthode A→B→C→D→E + propagation F) — **4/7 thèmes complétés** : 02 prompt-eng ✅, 03 RAG ✅, 04 agents-IA ✅ (clôturé cette session), 06 patterns/context/stacks ✅. Reste : 05 fine-tuning, 07 leaders-modèles-industrie, 08 forge dogfooding.

## Dernière session (2026-05-23 — audit thème 04 agents-IA)

### Décisions prises
- Méthode 8 sub-agents par cluster appliquée intégralement — scaling 6 → 8 clusters fonctionne (130 claims, 26 notes, ~25 min wall-time)
- Carte blanche Raphael honorée — exécution direct du plan jusqu'au commit/push sans re-valider note par note
- 7 self-verify WebFetch direct sur fondations à fort impact (Böckeler, sub-agents docs, memory docs, Voyager arXiv, BEA, Weng blog, Dreams URL) — toutes ont confirmé sub-agents
- Slogans forge sans verbatim externe préservés explicitement avec marquage "Synthèse forge — pas de verbatim externe identifié"

### Corrections appliquées (20 NON CANONIQUES + 46 partielles sur 130 claims, 18 notes)
- **Type 3 (3 réécritures structurelles)** :
  - `harness-engineering` : auteure réelle = **Birgitta Böckeler (Thoughtworks)** seule, pas Fowler + Osmani + Willison. Verbatim "Linters bloquent > Prompts suggèrent" retiré (absent article). Verbatims canoniques cités : "Guides (feedforward controls) / Sensors (feedback controls)", "Computational / Inferential", "Ashby's Law of Requisite Variety"
  - `technique-shared-agent-memory` : retrait mythe "3 scopes + agent-memory-local", remplacé par 4 scopes CLAUDE.md canoniques (managed/user/project/local) + auto memory dans `~/.claude/projects/<project>/memory/`. Correction "system prompt" → "user message after system prompt" (verbatim docs)
  - `decoupe-agents-anti-crash` : retrait seuils mythes "max 6-8 ops" et "max 5 fichiers" (aucune source Anthropic via WebFetch direct), garde principes qualitatifs scoping
- **Type 2 (chiffres fabriqués retirés)** : LangGraph $0.08/tâche leader coût (inversé Rasa CALM moins cher), Supervisor/Swarm 94%/91% 4.2s/2.8s 2800/1900 tokens, LangGraph 14ms overhead, "34% citations enterprise" (confusion 34.5M PyPI dl), ReAct 95%/step → 60% sur 10 steps, "57% échecs orchestration", marché browser agents "$12B +200%", AutoGen "5-6x coût"
- **Type 1 (attributions corrigées)** : **Voyager = Wang et al.** (pas Fan et al., premier auteur Guanzhi Wang, preprint arXiv only), Building Effective Agents = Schluntz & Zhang, Lilian Weng formule réelle "LLM functions as the agent's brain", Anthropic "is usually enough" (pas "BEFORE adding complexity"), Cherny "coding is largely solved", Dreams URL = `platform.claude.com/docs/managed-agents/dreams`, Rakuten "initial critical errors"
- **Drifts mineurs** : CrewAI 30K → ~50K stars, Dify 100K → 142K, Pydantic AI v1.71/15.5K → v1.102/17.2K, MCP "20K servers" → "~10K", A2A "v1.2" → "v1.0 (12 mars 2026)", caching+batching "70-90%" → "jusqu'à 95%" (verbatim Anthropic), Google Search grounding pricing différencié Gemini 2.5/3.x
- **Propagation F** :
  - `neo_ia/.claude/rules/agent-delegation.md:54` : retrait attribution "Cat Wu canonique = 6-8 ops" (mythe), mesures empiriques p50/p75/p90 conservées (commit `6e304a6` sur develop)
  - Note vault `Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23.md` créée
  - 2 skills forge (`craft-prompt`, `pivot-check`) vérifiées sans drift

### Fondations canoniques confirmées (WebFetch direct, 7 sources primaires)
- ✅ Böckeler harness article : auteure seule, verbatims Guides/Sensors + Computational/Inferential + Ashby
- ✅ code.claude.com/docs/sub-agents : aucun seuil numérique d'opérations (confirme mythe)
- ✅ code.claude.com/docs/memory : 4 scopes CLAUDE.md + auto memory machine-local
- ✅ arXiv 2305.16291 Voyager : Wang premier auteur, preprint only
- ✅ anthropic.com/research/building-effective-agents : "is usually enough" verbatim
- ✅ lilianweng.github.io/posts/2023-06-23-agent : "agent's brain" + Planning/Memory/Tool use
- ✅ platform.claude.com/docs/managed-agents/dreams : Research Preview, beta header `dreaming-2026-04-21`

### Commits poussés
- `dbee1cd` (forge main) : 19 fichiers, +703/-536 lignes
- `6e304a6` (neo_ia develop) : 1 fichier, +3/-1

### Prochaines étapes (par priorité)
1. **Audit thème 05 fine-tuning** — ~15 notes (Dettmers, Hu, Han, Dao, etc.)
2. **Audit thème 07 leaders/modèles/industrie** — ~80 notes (le plus gros, dernière étape)
3. **Audit thème 08 forge dogfooding** — méta-audit canoniques forge

## Fils ouverts

- **architecture-openai-api inaccessible Cloudflare** : C4.12-C4.15 (Responses API, Assistants deprecated, Conversations, Realtime) à re-vérifier manuellement quand WebFetch passe, ou via alternative source
- **C7.4 Boris "PAS sub-agents profonds" ambigu** : audit confirme 5 worktrees + Plan Mode 80% multi-source, mais Boris recommande subagents pour investigation (doc Anthropic) — la formule a été nuancée mais reste potentiellement clivante
- **Claude Mythos Preview benchmarks (TAU 89.2%, WebArena 68.7%, SWE-bench 93.9%)** : single source Anthropic Project Glasswing accès restreint — re-vérifier quand Mythos passe en GA
- **Propagation cross-vault Bockeler** : sa fiche `Birgitta Böckeler` dans `05-Leaders/` existe-t-elle ? À auditer quand thème 07 leaders tournera
- **`gh` CLI absent forge** : workarounds documentés dans `reference_workarounds_session_constraints`
- **HEREDOC long Git Bash Windows échoue silencieusement** : préférer `git commit -F` ou inline court

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[methode-analyser-repo]]
- [[feedback_audit_thematique_methode]]
- [[feedback_carte_blanche_commit_push]]
- [[reference_audit_06_findings]]
- [[reference_workarounds_session_constraints]]
- [[harness-engineering]]
- [[technique-shared-agent-memory]]
- [[decoupe-agents-anti-crash]]
- [[Agents IA]]
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]]
- [[Birgitta Böckeler]]
- [[Andrej Karpathy]]
- [[Drew Breunig]]
