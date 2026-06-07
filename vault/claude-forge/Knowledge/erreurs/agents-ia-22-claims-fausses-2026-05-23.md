---
titre: "Audit Agents IA — corrections 23 mai 2026"
resume: "Audit thematique vault 04-Techniques/agents et chatbot : 130 claims auditees, 20 NON CANONIQUES corrigees + 46 partielles requalifiees, 17 notes mises a jour. Mythes principaux : seuils 6-8 ops, scopes memory inventes, attribution Bockeler vs Fowler"
aliases:
  - audit agents IA 23 mai
  - corrections agents 130 claims
  - erreurs agents-ia 2026-05-23
  - mythes agents forge
type: knowledge
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://martinfowler.com/articles/harness-engineering.html"
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://code.claude.com/docs/en/memory"
  - "https://arxiv.org/abs/2305.16291"
  - "https://lilianweng.github.io/posts/2023-06-23-agent/"
  - "https://platform.claude.com/docs/en/managed-agents/dreams"
  - "https://www.anthropic.com/research/building-effective-agents"
tags:
  - "#type/knowledge"
  - "#domaine/erreurs"
  - "#domaine/agents"
  - "#domaine/audit"
---

## Contexte

Audit thematique du vault forge sur le theme **Agents IA (non Claude Code)** — dossiers `04-Techniques/agents/` (15 notes) et `04-Techniques/chatbot/` (11 notes), soit **26 notes** au total.

Audit conduit le 23 mai 2026 avec methode sub-agents par cluster + self-verify direct sur les fondations a fort impact. Inspire de la methode validee 22 mai sur l'audit Claude Code (cf [[feedback_audit_thematique_methode]]).

## Bilan chiffre

| | # | % |
|---|---|---|
| Claims totales auditees | 130 | 100% |
| ✅ Canonique | 58 | 45% |
| ⚠️ Partiel / drift / single source | 46 | 35% |
| ❌ Non canonique (mythe/fabrique) | 20 | 15% |
| Notes vault corrigees | 17 / 26 | 65% |

## Corrections structurelles (Type 3 — doctrines fausses au fond)

### 1. `decoupe-agents-anti-crash` — seuils "6-8 ops" et "5 fichiers" = MYTHES

**Avant** : note structuree autour de "Max 6-8 operations lourdes par agent" et "Max 5 fichiers par agent" comme regles absolues.

**Verification self-verify** : WebFetch direct https://code.claude.com/docs/en/sub-agents et https://code.claude.com/docs/en/best-practices = **aucun seuil numerique** documente. Description Anthropic est qualitative : "side task would flood your main conversation".

**Apres** : reecriture en principes qualitatifs (scoping precis, prompt format de sortie, parallelisation independante). L'incident cc-news 8 mai 2026 (24 web searches → crash, redecoupe en 4 agents) garde sa valeur d'illustration sans extrapoler le `6` comme regle.

Voir [[feedback_seuils_canoniques_agents_mythes]] qui confirme 4 mythes seuils (6-8 ops, <200L body, max 8 tools, max N skills) — seuls CLAUDE.md <200L et SKILL.md <500L sont canoniques.

### 2. `technique-shared-agent-memory` — "3 scopes memory + agent-memory-local" = MYTHE structurel

**Avant** : note citant "3 scopes : user / project / local" avec un chemin `.claude/agent-memory-local/<name>/` qui **n'existe pas** dans la doc Anthropic.

**Verification self-verify** : WebFetch direct https://code.claude.com/docs/en/memory = **4 scopes CLAUDE.md canoniques** :
1. Managed policy : `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux), `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows)
2. User : `~/.claude/CLAUDE.md`
3. Project : `./CLAUDE.md` ou `./.claude/CLAUDE.md`
4. Local : `./CLAUDE.local.md` (gitignore)

Mecanisme separe : **Auto memory** dans `~/.claude/projects/<project>/memory/` (machine-local). Verbatim docs : "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself".

**Apres** : reecriture complete de la note avec la vraie hierarchie + distinction CLAUDE.md vs auto memory.

### 3. `harness-engineering` — auteure reattribuee Fowler → Bockeler

**Avant** : "discipline emergente definie par Martin Fowler (ThoughtWorks), Addy Osmani, et Simon Willison".

**Verification self-verify** : WebFetch direct https://martinfowler.com/articles/harness-engineering.html = **auteure reelle = Birgitta Bockeler (Distinguished Engineer, Thoughtworks)**. Fowler heberge le site, n'est pas co-auteur. Addy Osmani et Simon Willison ne sont PAS co-auteurs.

**Verbatim absents** dans l'article :
- "Linters qui bloquent > Prompts qui suggerent" : non present, principe juste mais formule synthese forge.

**Verbatim canoniques confirmes** :
- "Guides (feedforward controls)" / "Sensors (feedback controls)"
- "Computational — deterministic and fast, run by the CPU" / "Inferential — Semantic analysis, AI code review, 'LLM as judge'"
- "Ashby's Law of Requisite Variety… a regulator must have at least as much variety as the system it governs"
- "Agent = Model + Harness" est cite par Bockeler comme attribue a LangChain (lien externe).

**Apres** : reattribution Bockeler partout, retrait du verbatim faux "Linters bloquent", verbatims canoniques cites textuellement.

## Corrections Type 1 (attribution / verbatim paraphrases)

### Citations Anthropic et leaders

| Claim avant | Realite verifiee |
|-------------|------------------|
| Lilian Weng : "Agent = LLM + Memory + Planning + Tool Use" | Verbatim blog 2023-06-23 : **"LLM functions as the agent's brain, complemented by several key components: Planning, Memory, Tool use"**. Formule equation = synthese forge pedagogique. |
| Karpathy : "context window EST le programme, le LLM est l'interprete" | Verbatim Sequoia 2026 = "context window as **lever over** the interpreter, interpreter = LLM". Reformule. |
| Anthropic : "Optimize single LLM calls... BEFORE adding complexity" | Verbatim Building Effective Agents = **"is usually enough"**. "BEFORE adding complexity" est paraphrase. |
| Anthropic : "Write better tool descriptions, not more tools" + "une description precise vaut 3 outils" | **Verbatim absents**. Le ratio "3 outils" est fabrique. Principe qualitatif garde. |
| Cherny : "Coding is solved" | Verbatim = **"coding is largely solved"**. Le titre court vient de l'editorial Lenny. |
| URL Dreaming : `claude.com/blog/claude-managed-agents-memory` | Vraie URL = **`platform.claude.com/docs/en/managed-agents/dreams`**. Feature en Research Preview, beta header `dreaming-2026-04-21`. |
| Rakuten : "97% moins d'erreurs first-pass" | Verbatim Anthropic = **"97% reduction in initial critical errors"**. |

### Papers

| Claim avant | Realite verifiee |
|-------------|------------------|
| Voyager : "Fan et al. 2023" | Premier auteur arXiv 2305.16291 = **Guanzhi Wang**. Linxi "Jim" Fan est avant-dernier (position senior). Convention citation = **"Wang et al. 2023"**. Aucune conference officielle dans metadonnees arXiv (preprint uniquement). |
| Building Effective Agents : "Schluntz et al." | En realite **Schluntz & Zhang** (2 auteurs). |
| ReAct : "ICLR 2023 Oral" | ICLR 2023 confirme ; "Oral" non confirme dans metadonnees, retire par prudence. |

## Corrections Type 2 (chiffres fabriques)

| Claim avant | Verdict |
|-------------|---------|
| LangGraph "$0.08/tache leader cout" | ❌ Fabrique + qualification inversee. Etude Rasa montre Rasa CALM moins cher que LangGraph. **Retire**. |
| Supervisor/Swarm "94%/91% routing, 4.2s/2.8s latence, 2800/1900 tokens" | ❌ Pas de source primaire. **Retires** dans 3 notes (architecture-langgraph, pattern-orchestrateur, pattern-swarm). |
| LangGraph overhead "14ms/op vs OpenAI 2-5ms" | ❌ Fabrique. **Retire**. |
| LangGraph "34% citations enterprise" | ❌ Confusion avec 34.5M downloads PyPI. **Retire**. |
| Marche browser agents "$12B +200% YoY" | ❌ Chiffres divergents non sourcables. **Retire**. |
| "57% echecs orchestration" | ❌ Probable confusion 60% NVIDIA / 65% TechTimes. **Retire**. |
| ReAct "95%/step → 60% sur 10 steps" | ❌ Calcul theorique non source. **Retire**, garder principe "long-horizon drift" qualitatif. |
| AutoGen "5-6x cout" | ⚠️ Source primaire absente, qualitatif garde mais ratio retire. |
| CrewAI "30K+ stars" → realite **~50K+** | ⚠️ Drift, mis a jour. |
| Dify "100K+ stars" → realite **~142K** | ⚠️ Drift, mis a jour. |
| Pydantic AI "15.5K stars, v1.71" → realite **17.2K stars, v1.102 (22 mai 2026)** | ⚠️ Drift, mis a jour. |
| Computer Use "44% OSWorld" | ⚠️ Obsolete (Sonnet 3.5, oct 2024). Sonnet 4.5/Mythos progresse. Disclaimer ajoute. |
| MCP "20K+ servers" → realite **~10K** | ⚠️ Mis a jour. |
| A2A "v1.2" → realite **v1.0 publiee 12 mars 2026** | ⚠️ Mis a jour. |
| Caching+batching "-70-90%" | ⚠️ Sous-estime, verbatim Anthropic = **"jusqu'a 95%"**. |
| Google Search grounding "$14/1000" | ⚠️ Vrai pour Gemini 3.x ; Gemini 2.5 = 500-1500 RPD free + $35/1000. |
| LangGraph "$0.001/node executions" | ⚠️ Modele billing migre vers $0.005/deployment run. Renvoye vers pricing officiel. |

## Slogans forge legitimes (preservation explicite)

Quelques slogans n'avaient pas de verbatim externe identifiable mais sont des syntheses forge utiles. Marques explicitement comme tels :

- "10M tokens de context NE REMPLACENT PAS la memoire — complements, pas substituts" → marque "Synthese forge — pas de verbatim externe identifie"
- "Le modele n'est pas le produit — la memoire l'est" → idem
- "Linters qui bloquent > Prompts qui suggerent" → idem (principe deterministe > suggestif garde, formule retiree)

## Propagation cross-repo identifiee

### neo_ia
- `C:/Users/raphael.picard_neote/Documents/neot-v2/neo_ia/.claude/rules/agent-delegation.md:54` cite "Cat Wu canonique = 6-8 ops/agent max" → **mythe propage**.
- Action : retirer l'attribution "Cat Wu canonique" mais conserver les mesures empiriques neo_ia (p50=27, p75=52, p90=116, max=198) qui restent valides.

### Forge `.claude/`
- `.claude/skills/craft-prompt/references/techniques-claude.md`
- `.claude/skills/pivot-check/SKILL.md`
A re-auditer pour drift sur claims modifies.

## Methode (capitalisee pour audits futurs)

1. **Lecture parallele session principale** des 26 notes en 1 message → inventaire 130 claims dedupliquees en 8 clusters thematiques
2. **Checkpoint write A-inventaire-claims.md** avant phase B (resilience crash sub-agents)
3. **8 sub-agents paralleles par cluster** (verbatim citations / benchmarks / stats marche / frameworks / pricing / bugs GitHub / doctrines forge / papers) avec brief structure : claim verbatim + URLs candidates + format de sortie impose
4. **Self-verify FAUX fort impact** : WebFetch direct sur 7 fondations (Bockeler, sub-agents docs, memory docs, Voyager arXiv, Building Effective Agents, Weng blog, Dreaming URL)
5. **Plan correction par 3 vagues** distinguant Type 1 (attribution) / Type 2 (chiffres) / Type 3 (doctrine)
6. **advisor() AVANT execution structurelle** — 3 corrections de plan integrees (slogan invente a eviter, math 2.8% a reformuler, Devin a retirer)
7. **update_note via MCP forge-brain** uniquement (pas Edit/Write brut sur vault)

## Liens

- [[feedback_audit_thematique_methode]] — methode validee 22 mai
- [[feedback_seuils_canoniques_agents_mythes]] — 4 mythes seuils confirmes
- [[feedback_tweet_hype_paraphrase_pattern]] — pattern paraphrase vs verbatim
- [[feedback_anthropic_single_source]] — hierarchie sources scopee
- [[harness-engineering]] — note reecrite avec attribution Bockeler
- [[decoupe-agents-anti-crash]] — note reecrite sans seuils numeriques
- [[technique-shared-agent-memory]] — note reecrite avec 4 scopes CLAUDE.md
- [[Agents IA]] — MOC reattribue
- [[agents-architecture]], [[agents-frameworks]], [[agents-evaluation]], [[agents-automation]] — 4 notes Type 1+2
- [[architecture-claude-api]], [[architecture-langgraph]], [[architecture-gemini-api]], [[architecture-autogen]] — 4 architectures corrigees
- [[pattern-orchestrateur]], [[pattern-swarm]], [[pattern-single-agent-multi-tool]] — 3 patterns sans metriques fabriquees
- [[limites-subagents-claude-code]] — bugs GitHub avec disclaimers
- [[technique-dreaming-cross-session]] — URL et verbatim Rakuten corriges
- [[prompt-rewriter-pattern]] — 189 tokens / 2.8% reformule precisement
