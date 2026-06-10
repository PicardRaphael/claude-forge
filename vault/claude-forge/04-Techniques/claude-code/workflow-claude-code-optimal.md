---
titre: "Workflow Claude Code optimal pour tout repo (mai 2026)"
resume: "Workflow canonique mai 2026 — Routines higher-order prompt (Boris), Advisor Strategy (Brad Abrams), leaf nodes/human core/verifiable checkpoints (Erik), multi-clauding /loop, planification 15-20min, parallélisation 5 terminal + 5-10 browser sessions, Sonnet/Opus split, compounding."
aliases:
  - "workflow claude code optimal"
  - "workflow boris 2026"
  - "routines claude code"
  - "advisor strategy brad abrams"
  - "multi-clauding"
  - "leaf nodes erik schluntz"
  - "compounding error driven"
  - "verifiable checkpoints"
  - "parallelisation 5 sessions"
  - "compute allocator"
  - "comment automatiser claude code"
  - "automation workflow"
derniere-maj: 2026-05-24
auteur: claude
type: technique
sources:
  - "Code with Claude London 19 mai 2026 — Boris/Cat/Brad Abrams/Lisa/Daisy/Jeremy/Noah/Fiona/Ami keynotes"
  - "Code with Claude SF 6-7 mai 2026 — Erik/Thariq/Boris/Brad Abrams"
  - "Sequoia AI Ascent 29 avril 2026 — Boris coding is solved"
  - "Pragmatic Engineer interview Boris Cherny"
  - "anthropic.com/engineering"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
<!-- TODO 2026-05-24: note >500L — extraction sections vers references/ -->

# Workflow Claude Code optimal pour tout repo (mai 2026)

> Note canonique forge — workflow optimal pour utiliser Claude Code selon doctrine Anthropic mai 2026.

---

## QUOI — Définition

Le **workflow optimal Claude Code mai 2026** combine 7 pratiques canoniques de l'équipe Anthropic :

1. **Routines** — higher-order prompts (Boris)
2. **Advisor Strategy** — pattern cost reduction (Brad Abrams)
3. **Leaf nodes / human core / verifiable checkpoints** (Erik Schluntz)
4. **Multi-clauding** — 5 terminal + 5-10 browser sessions parallèles
5. **`/loop`** — autonome long-running
6. **Sonnet/Opus split** — exécution vs jugement (doctrine forge cohérente avec Cat Wu + Brad Abrams)
7. **Compounding error-driven** — CLAUDE.md évolue avec les erreurs

**Verbatim Boris** (Sequoia avril 2026) :

> "coding is solved"

Le shift est de "comment faire coder Claude" vers "comment orchestrer Claude qui code".

**Concept canonique Boris** : routines = higher-order prompts (créer une routine qui prompte Claude pour toi, au lieu de prompter manuellement). Source : Code with Claude SF 6 mai 2026. La formule lapidaire "I prompt Claude → I create a routine that prompts Claude" parfois citée est une glose pédagogique, pas un verbatim Boris attesté.

---

## POURQUOI — Le problème résolu

Sans workflow optimisé :
- **1 session séquentielle** = bottleneck humain (1 thread)
- **Pas de spec** = code généré qui rate la cible
- **Pas de verification** = qualité aléatoire
- **Coût élevé** sur jugement (tout en Opus) ou qualité basse (tout en Sonnet)
- **Erreurs récurrentes** sans compounding

Avec workflow optimal :
- **5 terminal + 5-10 browser sessions parallèles** = parallélisation horizontale
- **15-20 min planification** = ROI massif sur itérations
- **Advisor Strategy** = "close to Opus-level intelligence at much lower prices" (Brad Abrams verbatim)
- **Compounding** = 0% récurrence d'erreurs capturées

---

## COMMENT — 7 pratiques canoniques

### 1. Routines (Boris)

**Higher-order prompt** : au lieu de prompter Claude à chaque fois, créer une **routine** (skill, slash command, agent) qui prompte Claude pour toi.

Concept Boris (CwC SF 6 mai 2026) : passer de prompter manuellement à créer des routines réutilisables.

Concrètement :
- Tâche faite > 2 fois → skill ou slash command
- Pattern reproduit > 3 fois → agent dédié
- Critère 100% → hook

Toute action manuelle répétée est une routine en attente.

### 2. Advisor Strategy (Brad Abrams, Anthropic Product Lead Claude)

Source : [Code with Claude SF — "Caching, harnesses, and advisors: Building on Claude at GitHub scale"](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale) (talk avec Mario Rodriguez, GitHub CPO).

Pattern :
- **Executor model** : smaller (Haiku), exécute la majorité des appels
- **Advisor model** : larger (Opus), consulté ponctuellement
- Cost efficiency sans sacrifier l'intelligence

**Verbatim Brad Abrams** :
> "We get close to Opus-level intelligence at much lower prices because we're being very conservative about the tokens that advisor actually sends"

Pattern utilisé chez **GitHub Copilot** à scale. Mario Rodriguez (GitHub CPO) : cache hit rate au-dessus de 94% comme métrique foundational, "1% efficiency means millions overall".

> ⚠️ Avant 23 mai 2026 : le vault forge attribuait à tort cette doctrine à "Angela Jiang 5× cost reduction" — coquille propagée depuis une mention Simon Willison "Angela Kiang". La source canonique est **Brad Abrams**, pas Angela Jiang, et il n'y a pas de "5×" verbatim.

Implémentation forge : tool `advisor()` natif (cf section parallélisation).

### 3. Stratégies Erik Schluntz (Vibe Coding in Production)

4 stratégies verbatim — Code with Claude SF 6-7 mai 2026 :

| Stratégie | Description |
|-----------|-------------|
| **PM guidance** | Agent agit comme PM, pas dev — guide la direction |
| **Leaf nodes** | Modifier les feuilles, pas les racines (limite blast radius) |
| **Human core** | L'humain garde le contrôle des décisions clés |
| **Verifiable checkpoints** | Chaque étape vérifiable mécaniquement |

**Case study Erik** : 22 000 LOC en 1 jour = **analogie cognitive verbatim** (pas métrique brute) — le framing exact est "2 semaines → 1 jour" à analogie cognitive près.

### 4. Multi-clauding (parallélisation 5 terminal + 5-10 browser)

**Verbatim Boris** (Lenny's Newsletter) : "Boris runs 5 instances of Claude Code simultaneously in his terminal using 5 separate git checkouts of the same repo." Boris pousse aussi 5-10 sessions web Claude Code en parallèle pour features indépendantes.

Records Anthropic :
- **Boris** : 259 PRs/30j en décembre 2025 (Opus 4.5, ~8.6/j moyenne) — verbatim X/Threads
- **Boris** : "few dozen baseline + 150 record" en avril 2026 (Sequoia, Opus 4.6-4.7)
- **Noah Zweben** (CwC London, verbatim Every) : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March"
- **Cat Wu** : +200% PRs/eng org Anthropic (CwC London — single source, à reconfirmer)

Conditions :
- Features **indépendantes** (worktrees)
- **`/clear`** entre tâches non liées (Boris tip)
- Délégation **subagents pour recherche** (garde contexte principal propre)

### 5. `/loop` autonome

Skill bundled Anthropic pour exécution long-running autonome.

Pattern Boris (tip #1) : **"Give Claude a way to verify its work → 2-3x quality"**

`/loop` + verifiable checkpoints = autonome avec qualité.

### 6. Sonnet / Opus split (doctrine forge cohérente avec Anthropic)

**Doctrine forge inférée**, cohérente avec :
- **Cat Wu** (CwC London 19 mai 2026) : "Opus 4.7 tips — delegate, write full-context briefs, use the new `xhigh` effort level"
- **Brad Abrams** (CwC SF) : Advisor Strategy = executor (Haiku) + advisor (Opus)

| Modèle | Rôle forge | Exemples |
|--------|-----------|----------|
| **Sonnet** | Exécution | dev, code-reviewer, test-writer, python-dev |
| **Opus** | Jugement | architect, devils-advocate, project-auditor |
| **Haiku** | Checks rapides | classifiers, anti-rationalization |

**Effort** : `high` partout sauf architect/dev-lead/refactor-pg = `xhigh`. `max` toujours disponible (vérifié docs 23 mai 2026), à utiliser avec prudence (prone overthinking).

### 7. Compounding error-driven (Boris)

> "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"
> — Boris Cherny

Cycle :
```
Erreur observée → ajout ligne CLAUDE.md (ou hook si 100%) → session suivante évite l'erreur
```

**Audit mensuel** : élaguer ce qui n'est plus nécessaire (cf `/forge-review`).

### 8. Compute allocator mindset (Thariq)

> "All of us are becoming these compute allocators now"
> — Thariq, ChatPRD "How I AI: HTML is the new markdown" verbatim

> "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code"
> — Thariq, idem (à reconfirmer URL exact)

**Implication** : passe 15-20 min à planifier avant de lancer Claude. Le ROI est massif.

---

## QUAND — Critère d'application

### Workflow plein régime quand :
- Repo avec usage CC > 2 sessions/semaine
- Features indépendantes nombreuses
- Refactor / migration importante

### Workflow allégé quand :
- Repo tout neuf (CLAUDE.md minimal, pas de routines, ajustement progressif)
- Tâche one-shot
- Exploration / spike

---

## WORKFLOW — Séquence par taille de tâche

### S (small, < 30 min)

```
1. Prompt direct
2. Vérifier output
3. Commit
```

Pas d'overhead. Pas d'agent.

### M (medium, 30 min - 4h)

```
1. /spec (forge) ou prompt structuré (description + contraintes)
2. Architect-first SI archi non triviale (sinon skip)
3. Implémentation
4. Code review (skill ou agent)
5. Commit
```

### L (large, > 4h ou cross-files)

```
1. /spec exhaustif
2. Architect-first obligatoire
3. Décomposition en tickets (sub-agents en parallèle si indépendants)
4. Implémentation parallèle (worktrees)
5. Code review systématique
6. Devils-advocate si livrable majeur
7. Commit groupé
```

### XL (multi-jours)

```
1. Planning humain 15-20 min minimum
2. /spec + decompose
3. Multi-clauding (5 terminal + 5-10 browser) sur tickets indépendants
4. Advisor Strategy : Opus advise, Sonnet/Haiku execute
5. Verifiable checkpoints à chaque ticket
6. /loop autonome sur tâches répétitives
7. Compounding CLAUDE.md au fil
8. Audit final + DA livraison
```

---

## APPELS — Composants mobilisés

- [[comment-ecrire-claudemd]] — compounding base
- [[comment-creer-skill]] — routines (higher-order prompts)
- [[comment-creer-agent]] — rôles dédiés
- [[comment-creer-hook]] — boundaries 100%
- [[methode-analyser-repo]] — comment construire ce workflow pour un repo donné
- [[mcp-vs-skills-doctrine]] — où placer chaque pièce
- [[pattern-vault-llm-karpathy]] — memory compounding niveau vault

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- CLAUDE.md + 1-3 routines (slash commands)
- Sessions séquentielles
- Sonnet partout
- Pas de hooks

### Niveau avancé
- 5-10 routines (skills + slash commands)
- 3-5 agents par rôle
- Multi-clauding 2-3 sessions parallèles
- Sonnet/Opus split appliqué
- Hooks lint/security

### Niveau expert (forge actuel)
- Routines exhaustives + agents dédiés + hooks lint/security/scope
- Multi-clauding 5 terminal + 5-10 browser
- Advisor Strategy systématique (Brad Abrams pattern)
- Compounding CLAUDE.md + vault (pattern Karpathy LLM Wiki)
- `/loop` pour tâches répétitives
- `/spec` + `decompose-ticket` workflow
- DA avant livraisons majeures
- Audit mensuel `/forge-review`

**PR scope** : optionnel, à customiser selon repo. Forge perso utilise `/spec` etc. plutôt que CI/labels élaborés.

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain verbatim |
|-------|---------------|
| Routines (higher-order) | Productivité ×N (Boris : 259 PRs/30j déc 2025) |
| Advisor Strategy | **"Close to Opus-level intelligence at much lower prices"** (Brad Abrams verbatim CwC SF) |
| Multi-clauding 5 terminal + 5-10 browser | **+300% équipe 3 mois** Noah Zweben verbatim Every : "500 in January to roughly 1,150 in March" |
| Sonnet/Opus split (doctrine forge) | Cohérent avec Cat Wu + Brad Abrams patterns |
| Verifiable checkpoints + /loop | **2-3× quality** (Boris tip #1) |
| Harness changes (Böckeler) | LangChain **52.8% → 66.5%** Terminal Bench, **harness seul**, modèle **GPT-5.2-Codex** (Vivek Trivedy LangChain blog 17 fév 2026) |
| ForgeCode Terminal-Bench 2.0 | **79.8%** (Bustamante). Comparaison à Claude Code et +21.8 pts non sourcés directement chez Addy Osmani (qualitatif uniquement) |
| 99% tokens planning vs code | ROI massif sur 15-20 min planning (Thariq) |
| Compounding error-driven | 0% récurrence erreurs capturées |

---

## ANTI-PATTERNS

### Workflow
- ❌ **Tout prompter manuellement** — automatiser les routines
- ❌ **0 advisor / 0 verification** — qualité aléatoire
- ❌ **Tout en Opus** — coût ×N inutile sur exécution
- ❌ **Tout en Sonnet** — qualité dégradée sur jugement
- ❌ **`max` effort partout** — coût massif, réserver
- ❌ **Pipeline workflow trop long** (> 30 min sur CRUD) — frustration, supersédé doctrine 22 mai
- ❌ **REFACTOR phase systématique** dans pipeline — supprimée doctrine 22 mai

### Boundaries
- ❌ **Tout dans CLAUDE.md** — sortir routines en skills, règles 100% en hooks
- ❌ **CTO orchestrateur agent** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Doc agent dédié** — pas d'agent doc (cf [[feedback_no_doc_agent]])

### Parallélisation
- ❌ **5+ sessions sur features dépendantes** — conflits worktrees
- ❌ **Pas de `/clear` entre tâches non liées** — pollution contexte (Boris piège #1)
- ❌ **Pas de délégation subagent** pour recherche — pollue contexte principal

### Memory
- ❌ **Pas de compounding CLAUDE.md** — erreurs récurrentes
- ❌ **Mise à jour CLAUDE.md 3 sessions trop tard** — détail perdu (cf memory-discipline)

### Specifications
- ❌ **0 spec sur tâches L/XL** — code généré rate la cible
- ❌ **Spec trop générale** — Claude invente les détails (cf [[feedback_spec_brief_diagnostic]])

---

## EXEMPLES CONCRETS — Repos externes

### Anthropic interne (verbatim métrique)
- **Boris Cherny** : 259 PRs/30j (déc 2025, Opus 4.5), "few dozen baseline + 150 record" (avril 2026 Sequoia)
- **Boris setup parallel** : 5 terminal instances + 5-10 browser sessions
- **Noah Zweben** (verbatim Every) : "500 in January to roughly 1,150 in March" = +300% PRs équipe 3 mois
- **Cat Wu** : +200% PRs/eng org Anthropic (single source CwC London)
- **Brad Abrams** : Advisor Strategy (CwC SF talk avec GitHub)
- **Daisy Hollman** (CwC London) : "You should be running agents overnight" / "red squigglies for agents"
- **Fiona Fung** (Head of Engineering Anthropic, CwC London) : "Pick your noisiest workflow…and ask if it's still serving its purpose" + "In technical debates, code wins"

### Repos publics référence
- **[anthropics/claude-code](https://github.com/anthropics/claude-code)** : config minimaliste 3 slash commands (démonstration "minimum qui marche")
- **[anthropics/claude-code-action/CLAUDE.md](https://github.com/anthropics/claude-code-action)** : seul CLAUDE.md Anthropic public
- **[anthropics/claude-for-legal/CLAUDE.md](https://github.com/anthropics/claude-for-legal)** : **174 lignes**, 5 sections (vérifié 23 mai 2026)
- **[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** : CLAUDE.md viral (ex-forrestchang), **67 lignes**, 4 principes — fan project pas endorsé par Karpathy
- **[trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)** : entreprise sécu complète

### Pattern Karpathy
- [Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 3-layers (raw/wiki/schema), Ingest/Query/Lint, qmd (Tobi Lütke, attribution via handle `tobi`+npm) tooling

### Erik Schluntz case study
- 22 000 LOC en 1 jour (analogie cognitive verbatim)
- Stratégies : PM guidance, leaf nodes, human core, verifiable checkpoints

---

## SOURCES — Verbatim avec URLs

### Code with Claude London 19 mai 2026 (équipe Anthropic)
- **Boris Cherny** keynote — Routines / higher-order prompts (concept canonique CwC SF + London)
- **Cat Wu** : Opus 4.7 tips, xhigh effort level
- **Lisa Crofoot** : "scaffolding holds Claude back" (single source à confirmer)
- **Noah Zweben** verbatim Every : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March"
- **Daisy Hollman** : workshop "Beyond the Basics with Claude Code", "agents overnight", "red squigglies"
- **Jeremy Hadfield** : Dreaming feature (notes-to-self cross-tasks)
- **Fiona Fung** (Head of Engineering Anthropic) : "Pick your noisiest workflow" + "In technical debates, code wins"
- **Ami Vora** (Chief Product Officer) : keynote
- **Katelyn Lesse** (Head of Platform Engineering)

### Code with Claude SF 6-7 mai 2026
- **Erik Schluntz** : Vibe Coding in Prod (PM guidance, leaf nodes, human core, verifiable checkpoints)
- **Thariq Shihipar** : Agent SDK Workshop, HTML markdown, compute allocators verbatim
- **Brad Abrams + Mario Rodriguez (GitHub CPO)** : Caching, harnesses, advisors talk — Advisor Strategy

### Sequoia AI Ascent 29 avril 2026
- **Boris** : "coding is solved"
- **Karpathy** : "From Vibe Coding to Agentic Engineering" — vibe et agentic positionnés en **complémentaires** (pas remplacement)

### Pragmatic Engineer / Latent Space
- **Boris** : "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md" (Pragmatic Engineer)
- **Boris** : "All the secret sauce — it's all in the model" (Latent Space verbatim)
- **Boris** : "Plain glob and grep, driven by the model, beat everything" (Pragmatic Engineer)
- **Boris** : "Complex scaffolding is often rendered obsolete by the next model generation"

### Anthropic engineering blog
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent (initializer + coding, harness identique, pas de split modèles)

### Hashimoto / Böckeler / LangChain / Bustamante
- [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) — Hashimoto popularise "harness engineering" (5 fév 2026)
- [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Böckeler Guides+Sensors 2 avril 2026
- [langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — Vivek Trivedy 17 fév 2026
- [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit) — ForgeCode 79.8%
- [addyosmani.com/blog/agent-harness-engineering/](https://addyosmani.com/blog/agent-harness-engineering/) — Addy Osmani qualitatif

---

## GOTCHAS — Pièges observés

### Pièges parallélisation
- **Multi-clauding sur features dépendantes** = conflits worktrees, perte temps
- **Pas de `/clear` entre tâches** = pollution contexte
- **Subagent qui commit malgré "pas de commit"** — TOP du prompt en gras (cf [[feedback_subagent_autocommit]])

### Pièges modèle
- **`effort: max` toujours disponible** mai 2026 (vérifié docs), à utiliser avec prudence
- **`xhigh` partout = coût massif** — réservé architect/dev-lead/refactor-pg (forge)
- **Opus 4.7 plus littéral** — être explicite scope et parallélisme (observation forge)

### Pièges spec
- **BRIEF distant** (ex BRIEF-NEOIA depuis ia_back) = CONTRAT + ce que JE fais, JAMAIS les fichiers/internes du repo distant (cf [[feedback_spec_brief_diagnostic]])
- **Workaround devient sédiment** sans dette technique loggée (cf [[feedback_workaround_sediment]])

### Pièges advisor / DA
- **TOUJOURS advisor+DA AVANT de proposer** un setup, pas après rappel (cf [[feedback_advisor_da_mandatory]])
- **Rechercher internet AVANT advisor/DA** quand fait technique incertain (cf [[feedback_advisor_da_web_search]])
- **Si DA échoue (529/timeout)** : relancer 1×, sinon advisor fallback, sinon STOP (cf [[feedback_da_failure_options]])

### Pièges compounding
- **3 sessions trop tard** = détail perdu — capturer immédiatement
- **Audit mensuel sauté** = CLAUDE.md devient kitchen sink

### Pièges tests
- **Mesurer AVANT optimiser** : --durations sur 1 fichier (cf [[feedback_measure_before_optimize]])
- **Tests heureux ≠ tests adverses** (cf [[feedback_tests_adverses_obligatoires]])

### Pièges Jarvis (forge)
- **Pas de questionnaire avant analyse** : analyser d'abord, proposer, questions seulement non-déductible (cf [[feedback_analyse_first_not_questionnaire]])
- **JAMAIS mode exécutant pur** (cf [[feedback_never_pure_executor]])
- **Verdict direct** si travail fait dans la session, pas relire 20 fichiers (cf [[feedback_stop_over_verifying]])

---

## ALIASES — Findability

Aliases déclarés en frontmatter (12) :
- workflow claude code optimal
- workflow boris 2026
- routines claude code
- advisor strategy brad abrams
- multi-clauding
- leaf nodes erik schluntz
- compounding error driven
- verifiable checkpoints
- parallelisation 5 sessions
- compute allocator
- comment automatiser claude code
- automation workflow

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-ecrire-claudemd]]
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]
- [[pattern-vault-llm-karpathy]]

### Fiches leaders (à créer)
- [[Boris Cherny]]
- [[Cat Wu]]
- [[Brad Abrams]]
- [[Lisa Crofoot]]
- [[Noah Zweben]]
- [[Daisy Hollman]]
- [[Jeremy Hadfield]]
- Fiona Fung (Head of Engineering Anthropic) — fiche à créer
- Ami Vora (Chief Product Officer Anthropic) — fiche à créer
- [[Erik Schluntz]]
- [[Justin Young]]
- [[Thariq Shihipar]]
- [[Andrej Karpathy]]
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]
- [[Addy Osmani]]

### Knowledge / refs liées
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[raisonnement-revirement-pipeline-mai-2026]]
- [[erreur-pipeline-trop-long-frustration]]
- [[feedback_no_cto_agent]]
- [[feedback_no_doc_agent]]
- [[feedback_subagent_autocommit]]
- [[feedback_spec_brief_diagnostic]]
- [[feedback_workaround_sediment]]
- [[feedback_advisor_da_mandatory]]
- [[feedback_advisor_da_web_search]]
- [[feedback_da_failure_options]]
- [[feedback_measure_before_optimize]]
- [[feedback_tests_adverses_obligatoires]]
- [[feedback_analyse_first_not_questionnaire]]
- [[feedback_never_pure_executor]]
- [[feedback_stop_over_verifying]]

### Forge custom
- [[forge-review]] — audit mensuel
- [[devils-advocate-pipeline]]
- [[forge-brain-proactive]]

---

**Fin note canonique `workflow-claude-code-optimal.md`** — révisée 23 mai 2026 post-audit thématique vault.

---

## AJOUT 23 MAI 2026 — Code-first orchestration via Programmatic Tool Calling (PTC)

Anthropic ships **Programmatic Tool Calling (PTC)** mai 2026 — pattern d'orchestration où **le code Python orchestre, le modèle juge à chaque étape**.

### Principe canonique

> "Use code for what code is good at, use models for what models are good at"
> — popularisé par tweet @_vmlops 23 mai 2026 (résumé du principe docs Anthropic)

**Note honnêteté** : le slug "/workflows" cité par le tweet @_vmlops n'est PAS un slug officiel Anthropic (404 docs). Le pattern existe et s'appelle **Programmatic Tool Calling (PTC)** côté docs officielles.

### Pattern

```
LLM orchestrator (sub-agents classiques) :
- 10 sub-agents → main session paie token tax, contexte gonfle
- Chaque résultat sub-agent re-entre dans contexte orchestrateur

PTC (code orchestrator) :
- Claude écrit Python qui orchestre N tool calls dans sandbox
- Seul l'output final entre dans contexte
- 20 tool calls = 1 inference (vs N inférences)
```

### Quand utiliser PTC vs sub-agents

| Pattern | Quand préférer |
|---------|----------------|
| **PTC** | Orchestration déterministe + filtrage data + boucles + conditionals |
| **Sub-agents** (Justin Young 2-agent) | Jugement contextuel à chaque étape, multi-step reasoning |

Complémentaires, pas concurrents.

### Détail technique complet

Voir [[programmatic-tool-calling]] — note canonique dédiée avec :
- Config API verbatim (`code_execution_20260120` + `allowed_callers`)
- Métriques Anthropic (25.6% → 28.5% knowledge retrieval, 46.5% → 51.2% GIA)
- Use case verbatim (budget compliance 20 employees)
- Comparaison détaillée vs sub-agents
- Gotchas (containers 4.5 min, sandbox strict, slug `/workflows` non canonique)

### Sources

- [Docs Anthropic PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [Anthropic engineering blog](https://www.anthropic.com/engineering/advanced-tool-use)
- [[programmatic-tool-calling]] — note canonique forge

`derniere-maj` à mettre à jour après ce ajout.


---

## AJOUT 24 mai 2026 — Pipeline complet feature majeure (spec-driven + ADR + escalade)

Stack de pratiques cohérent issu du chantier 24 mai (recherche web + audit vault + déploiement neo_ia/ia_back).

### Pipeline canonique pour feature M/L

```
1. /spec <idée floue>
     ↓ (interview AskUserQuestion → SPEC.md / BRIEF.md persistant)
     ↓ output : TODO/feature-<slug>/SPEC.md + BRIEFs
2. /plugin feature-dev (optionnel, Anthropic officiel)
     ↓ 7 phases : Discovery → Exploration → Clarifying → Architecture → Implementation → Quality Review → Summary
     ↓ 3 agents en // : code-explorer, code-architect, code-reviewer
3. Boucle TDD via session principale orchestrant sub-agents :
     test-writer → dev/dev-* → code-reviewer
     - sub-agents qui détectent AMBIGUÏTÉ → emit ESCALADE structuré → session principale appelle AskUserQuestion → re-dispatch
     - sub-agents qui détectent hors-scope → emit ESCALADE REQUISE → session principale spawn agent recommandé
4. /go (Boris pattern)
     ↓ typecheck + tests + code-reviewer dispatch + changelog + commit + push
```

### Pipeline canonique pour fix rapide (bypass /spec)

```
1. Description user directe
2. Session principale → dev (sans architect si trivial)
3. /go (typecheck + tests + reviewer + commit)
```

### Innovations 24 mai déployées

1. **Pattern AMBIGUÏTÉ DÉTECTÉE** dans 15 sub-agents (neo_ia + ia_back + forge devils-advocate). Verbatim limitation Anthropic : `AskUserQuestion` ne marche pas dans sub-agent → escalade structurée vers main agent.
2. **Hook SubagentStop `escalade-detector`** (neo_ia .py + ia_back .ts) : détecte markers d'escalade, imprime suggestion stderr, non-bloquant (doctrine 22 mai respectée).
3. **Formule directive descriptions skills** : `ALWAYS invoke when X. DO NOT Y without invoking first.` Appliquée sur 10 skills critiques pour reliability auto-invocation > 50%.
4. **Plugin feature-dev Anthropic officiel** : `/plugin install feature-dev@claude-plugins-official` sur les 2 repos pour pipeline 7 phases Anthropic.

### Couches d'enforcement (doctrine 22 mai préservée)

| Couche | Outil | Force |
|--------|-------|-------|
| Advisory | CLAUDE.md, rules, descriptions skills directives | ~80% compliance |
| Deterministic (lint/test/security) | hooks PreToolUse lint, /go pre-commit | 100% sur ce qu'il détecte |
| Observability | hooks SubagentStop (escalade-detector, agent-metrics-logger) | passive |
| **NEVER** | hooks workflow agentique (architect-guard, commit-guard) | INTERDIT doctrine 22 mai |

### Sources

- [[pattern-spec-driven-development]] — Pipeline Thariq
- [[feature-dev-plugin]] — Plugin Anthropic
- [[anti-reentrance-sub-agents-pattern-escalade]] — Pattern hors-scope
- [[raisonnement-22mai-doctrine-vs-enforcement]] — Doctrine 22 mai préservée
- [[cowork-skills-reliability]] — Formule directive
- [[comment-creer-agent]] (section AjOUT 24 mai) — AskUserQuestion limitation
- [[comment-creer-hook]] (section AJOUT 24 mai) — SubagentStop suggester pattern

---

## AJOUT 9 juin 2026 — Couches de test du code généré par IA + cadence mutation testing

Doctrine **positive** sur *comment tester quand c'est Claude Code qui écrit le code* (le pendant de [[raisonnement-kill-tdd-strict-hooks-mai-2026]], qui dit ce qu'on NE fait PAS : pas de hook TDD bloquant). À porter dans les skills/rules/agents de **tout repo dev** (réflexe transverse, pas projet-spécifique).

### Pourquoi (état de l'art 2026)
Le code assisté par IA a ~1,7× plus de bugs ; le test devient le **contrat exécutable** qu'un humain relit en 20 lignes (vert/rouge remplace la relecture ligne par ligne). Mais un test écrit par IA peut être **cosmétique** (toujours vert) — d'où le mutation testing comme garde-fou.

### Les 4 couches (complémentaires)
| Couche | Rôle | Cadence |
|---|---|---|
| **TDD / unitaires** | bugs fonctionnels, edge cases | chaque PR (test-first, 1 test à la fois, cap ~3/comportement) |
| **CI bloquante + coverage + lint + frontières** | régressions, sécu, archi | chaque PR (bloquant si rouge) |
| **Mutation testing** | vérifie que les tests *valent quelque chose* (l'IA peut écrire des tests bidons) | **deux étages — voir ci-dessous** |
| **Contract tests** | dérive des schémas/API entre packages | chaque PR sur les frontières |

### Cadence mutation testing — DEUX étages (pas « rare » seulement)
Erreur intuitive : « le mutation testing est lent, donc on le fait rarement ». L'état de l'art (StrykerJS docs + retours monorepo 2026) est **deux étages complémentaires** :

- **Par PR — incrémental scopé** : `--incremental` + scope aux fichiers/packages changés (`git diff` / packages affectés Turborepo/Nx). 1-5 min. Sert de **gate** : build rouge si le score descend sous seuil (~80 %) ou si des mutants survivent sur le code touché.
- **Planifié — full `--force`** : run complet sur le cœur métier, en CI **nightly ou hebdomadaire** (`cron`), pour réinitialiser la baseline incrémentale (sinon elle dérive) et rattraper ce que l'incrémental ne voit pas (changements de deps, env, snapshots).
- **Scope** : cœur métier / logique à fort impact uniquement (évite le « mutant explosion » — ne pas muter tout le repo).
- **Seuils** : >80 % excellent, 60-80 % correct, <60 % suite de tests faible.

> Le **quoi/quand** est doctrine (ici + CLAUDE.md/rules du repo) ; le **comment** (config StrykerJS exacte, `stryker-incremental.json`, cache CI) vit dans la skill `test`/`drizzle-query` du repo, pas dans la doctrine.

### Ce qui reste interdit (cohérence [[raisonnement-kill-tdd-strict-hooks-mai-2026]])
- ❌ Forcer le test-first par **hook bloquant** → tests cosmétiques. Le hook *lance* les tests, la CI *bloque* si rouge.
- ❌ Coverage élevé **sans** mutation testing → fausse confiance (couverture ≠ qualité des assertions).
- ❌ Muter tout le repo à chaque PR → CI ingérable. Incrémental scopé + full planifié.

### Sources
- [StrykerJS — Incremental mode](https://stryker-mutator.io/docs/stryker-js/incremental/)
- [Mutation testing with Stryker — config CI](https://oneuptime.com/blog/post/2026-01-25-mutation-testing-with-stryker/view)
- [[martin-fowler]] — mutation testing = « Sensors / feedback computational »
- [[raisonnement-kill-tdd-strict-hooks-mai-2026]] — le négatif (pas de hook TDD bloquant)

## AJOUT 29 mai 2026 — Dynamic Workflows (orchestration native Claude Code)

Le 28 mai 2026, Anthropic ship **Dynamic Workflows** (research preview) avec Opus 4.8. Claude écrit dynamiquement un **script JS d'orchestration** lançant jusqu'à 1000 sous-agents (16 concurrents), coordination **hors-contexte** (plan dans le code, résultats dans des variables, seul l'output final revient en contexte). Déclenché par « workflow » dans un prompt ou le réglage **`ultracode`** (effort `xhigh` + décision auto). Requiert v2.1.154+, plans Max/Team/Enterprise.

**Continuité doctrinale** : c'est PTC ([[programmatic-tool-calling]]) porté au niveau Claude Code natif. « Code orchestre, modèle juge » s'applique désormais sans écrire de code API. La doctrine forge « pas d'agent orchestrateur custom » ([[feedback_no_cto_agent]]) reste valide — on ne CONSTRUIT pas un orchestrateur, l'outil natif le fait. Pattern à privilégier sur orchestration déterministe massive (migrations, audits multi-fichiers, fan-out review) vs sub-agents pour jugement contextuel pas-à-pas.

Détail complet + caps + changelog associé : [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]].

## AJOUT 10 juin 2026 — Harness design pour apps long-running (2e article Anthropic)

Anthropic publie un **second article** de la famille harness long-running : [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (suite de l'article Justin Young, cf [[justin-young]]). Mécanismes nouveaux non couverts ailleurs dans le vault :

### Architecture Planner / Generator / Evaluator (inspirée GAN)
- **Planner** : prompt 1-4 phrases → spec produit haut niveau. Gotcha : s'il sur-spécifie le technique, les erreurs cascadent.
- **Generator** : implémente, s'auto-évalue, décide raffiner ou pivoter.
- **Evaluator** : agent SÉPARÉ, **fresh-context** (n'a jamais vu le build), sans Write/Edit, mode ACTIF (Playwright MCP naviguant l'app — supérieur au scoring de screenshot). Séparer celui qui produit de celui qui juge bat l'auto-critique.

### Default-FAIL contract
Chaque critère de done **commence à FAIL** ; l'agent ne peut le passer à PASS qu'avec une **preuve ouverte** (sortie de test, fichier lu). Antidote au biais observé : sans ça, l'evaluator « talks itself into deciding [the bugs] weren't a big deal ». Convergent Trail of Bits anti-rationalization ([[trail-of-bits-config]]).

### Sprint contracts
Avant chaque sprint, generator et evaluator **négocient ce que « done » signifie** (proposition → validation → accord), communication par fichiers (état auditable). Comble l'écart entre user stories et comportements testables.

### Context anxiety + context resets vs compaction
- **Context anxiety** : le modèle clôt prématurément en sentant approcher sa limite de contexte (observé Sonnet 4.5, disparu Opus 4.6).
- **Context reset** = nouveau contexte vide + **structured handoff artifact** (fichier d'état + next steps) ≠ compaction (résumé en place, l'anxiété persiste).

### Principe de simplification itérative du harness (règle maîtresse)
> « Every component in a harness encodes an assumption about what the model can't do on its own » — hypothèses à **re-tester à chaque nouveau modèle**, en retirant UN composant à la fois et en mesurant. Cas concret v1→v2 : sprints + context resets nécessaires sur Sonnet 4.5, supprimés sur Opus 4.6 (compaction SDK suffit). Corollaire multi-modèles (ex. fable + opus en alternance) : calibrer le harness sur le **moins capable** — les gardes ne coûtent rien au modèle fort.

### Evaluator tuning loop
Lire les logs de l'evaluator → repérer les divergences avec le jugement humain → corriger le prompt QA → répéter. Même tuné, l'evaluator rate les bugs profondément imbriqués — coverage jamais exhaustif.

### Application neoteem-back-ts (10 juin 2026)
Audit harness du repo vs état de l'art (Fowler/Böckeler, Osmani, Anthropic ×2, Trail of Bits) : conforme ~85 %. Les 4 manques identifiés pour le dev nocturne : (1) protocole de nuit = loop invoquant `/feature` **explicitement** (déclenchement skills déterministe par construction, pas probabiliste), (2) branch restrictions Bitbucket = garde-fou serveur prérequis, (3) Default-FAIL contract dans reviewer + `/go`, (4) anti-rationalisation encodée dans la skill `/feature` (pas en hook Stop — cohérence doctrine 22 mai).

### Sources
- [Harness design for long-running application development — Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Effective harnesses for long-running agents — Justin Young](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (fresh-context evaluator, Default-FAIL)
- [[justin-young]] — article fondateur (two-agent, clean state)
- [[martin-fowler]] · [[addy-osmani]] · [[trail-of-bits-config]] — corpus harness engineering
