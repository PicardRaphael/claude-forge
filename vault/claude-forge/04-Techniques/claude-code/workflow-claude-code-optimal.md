---
titre: "Workflow Claude Code optimal pour tout repo (mai 2026)"
resume: "Workflow canonique mai 2026 — Routines higher-order prompt (Boris), advisor 5× (Angela Jiang), leaf nodes/human core/verifiable checkpoints (Erik), multi-clauding /loop, planification 15-20min, parallélisation 5-10 sessions, Sonnet/Opus split, compounding."
aliases:
  - "workflow claude code optimal"
  - "workflow boris 2026"
  - "routines claude code"
  - "advisor strategy 5x"
  - "multi-clauding"
  - "leaf nodes erik schluntz"
  - "compounding error driven"
  - "verifiable checkpoints"
  - "parallelisation 5 sessions"
  - "compute allocator"
  - "comment automatiser claude code"
  - "automation workflow"
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "Code with Claude London 19 mai 2026 — Boris/Cat/Angela/Lisa/Daisy/Jeremy keynotes"
  - "Code with Claude SF 6-7 mai 2026 — Erik/Thariq/Boris"
  - "Sequoia AI Ascent 29 avril 2026 — Boris coding is solved"
  - "Pragmatic Engineer interview Boris Cherny"
  - "anthropic.com/engineering"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/workflow"
  - "#doctrine/2026"
---

# Workflow Claude Code optimal pour tout repo (mai 2026)

> Note canonique forge — workflow optimal pour utiliser Claude Code selon doctrine Anthropic mai 2026.

---

## QUOI — Définition

Le **workflow optimal Claude Code mai 2026** combine 7 pratiques canoniques de l'équipe Anthropic :

1. **Routines** — higher-order prompts (Boris)
2. **Advisor strategy** — pattern 5× cost reduction (Angela Jiang)
3. **Leaf nodes / human core / verifiable checkpoints** (Erik Schluntz)
4. **Multi-clauding** — 5-10 sessions parallèles
5. **`/loop`** — autonome long-running
6. **Sonnet/Opus split** — exécution vs jugement
7. **Compounding error-driven** — CLAUDE.md évolue avec les erreurs

**Verbatim Boris** (Sequoia avril 2026) :

> "coding is solved"

Le shift est de "comment faire coder Claude" vers "comment orchestrer Claude qui code".

> "I prompt Claude → I create a routine that prompts Claude"
> — Boris Cherny, Code with Claude London 19 mai 2026

---

## POURQUOI — Le problème résolu

Sans workflow optimisé :
- **1 session séquentielle** = bottleneck humain (1 thread)
- **Pas de spec** = code généré qui rate la cible
- **Pas de verification** = qualité aléatoire
- **Coût élevé** sur jugement (tout en Opus) ou qualité basse (tout en Sonnet)
- **Erreurs récurrentes** sans compounding

Avec workflow optimal :
- **5-10 sessions parallèles** = parallélisation horizontale
- **15-20 min planification** = 10× réduction d'itérations
- **Advisor strategy** = 5× cost reduction (Angela Jiang verbatim)
- **Compounding** = 0% récurrence d'erreurs capturées

---

## COMMENT — 7 pratiques canoniques

### 1. Routines (Boris)

**Higher-order prompt** : au lieu de prompter Claude à chaque fois, créer une **routine** (skill, slash command, agent) qui prompte Claude pour toi.

> "I prompt Claude → I create a routine that prompts Claude" — Boris, London keynote

Concrètement :
- Tâche faite > 2 fois → skill ou slash command
- Pattern reproduit > 3 fois → agent dédié
- Critère 100% → hook

Toute action manuelle répétée est une routine en attente.

### 2. Advisor strategy (Angela Jiang)

**5× cost reduction** sur agents long-running (Code with Claude London 19 mai 2026).

Pattern :
- Modèle puissant (Opus) **advise** le contexte initial
- Modèle moins cher (Sonnet) **execute** sur l'advise
- L'advisor revient à des checkpoints clés

Implémentation forge : tool `advisor()` natif (cf section parallélisation).

> "advisor strategy 5× cost reduction" — Angela Jiang, London

### 3. Stratégies Erik Schluntz (Vibe Coding in Production)

4 stratégies verbatim — Code with Claude SF 6-7 mai 2026 :

| Stratégie | Description |
|-----------|-------------|
| **PM guidance** | Agent agit comme PM, pas dev — guide la direction |
| **Leaf nodes** | Modifier les feuilles, pas les racines (limite blast radius) |
| **Human core** | L'humain garde le contrôle des décisions clés |
| **Verifiable checkpoints** | Chaque étape vérifiable mécaniquement |

**Case study Erik** : 22 000 LOC en 1 jour = **analogie cognitive verbatim** (pas métrique brute) — le framing exact est "2 semaines → 1 jour" à analogie cognitive près.

### 4. Multi-clauding (parallélisation 5-10 sessions)

**Boris** lance 5-10 sessions web Claude Code en parallèle pour features indépendantes.

Records Anthropic :
- **Boris** : 259 PRs/30j en décembre 2025 (Opus 4.5, ~8.6/j moyenne)
- **Boris** : "few dozen + 150 record" en avril 2026 (Sequoia, Opus 4.6-4.7)
- **Noah Zweben** : +300% PRs équipe sur 3 mois
- **Cat Wu** : +200% PRs/eng org Anthropic

Conditions :
- Features **indépendantes** (worktrees)
- **`/clear`** entre tâches non liées (Boris tip)
- Délégation **subagents pour recherche** (garde contexte principal propre)

### 5. `/loop` autonome

Skill bundled Anthropic pour exécution long-running autonome.

Pattern verbatim Boris :
> "Give Claude a way to verify its work → 2-3x quality"

`/loop` + verifiable checkpoints = autonome avec qualité.

### 6. Sonnet / Opus split

**Politique forge validée 21 mai 2026** :

| Modèle | Rôle | Exemples |
|--------|------|----------|
| **Sonnet** | Exécution | dev, code-reviewer, test-writer, python-dev |
| **Opus** | Jugement | architect, devils-advocate, project-auditor |
| **Haiku** | Checks rapides | classifiers, anti-rationalization |

**Effort** : `high` partout sauf architect/dev-lead/refactor-pg = `xhigh`. `max` déprécié.

### 7. Compounding error-driven (Boris)

> "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"
> — Boris Cherny

Cycle :
```
Erreur observée → ajout ligne CLAUDE.md (ou hook si 100%) → session suivante évite l'erreur
```

**Audit mensuel** : élaguer ce qui n'est plus nécessaire (cf `/forge-review`).

### 8. Compute allocator mindset (Thariq)

> "we're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on"
> — Thariq, "How I AI: HTML is the new markdown"

> "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code"
> — Thariq, idem

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
3. Multi-clauding (5-10 sessions) sur tickets indépendants
4. Advisor strategy : Opus advise, Sonnet execute
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
- Multi-clauding 5-10 sessions
- Advisor strategy systématique
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
| Routines (higher-order) | Productivité ×N (Boris : 259 PRs/30j) |
| Advisor strategy | **5× cost reduction** (Angela Jiang, London) |
| Multi-clauding 5-10 sessions | **+200% PRs/eng** (Cat Wu, org Anthropic) — **+300% équipe 3 mois** (Noah Zweben) |
| Sonnet/Opus split | ~5× moins de coût sur exécution, qualité préservée jugement |
| Verifiable checkpoints + /loop | **2-3× quality** (Boris tip #1) |
| Harness changes (Fowler) | LangChain **52.8% → 66.5%** Terminal Bench, même modèle |
| Harness > model | Forge AI **79.8% vs CC 58%** = **+21.8 pts** (Addy Osmani) |
| 99% tokens planning vs code | ROI massif sur 15-20 min planning (Thariq) |
| Compounding error-driven | 0% récurrence erreurs capturées |

---

## ANTI-PATTERNS

### Workflow
- ❌ **Tout prompter manuellement** — automatiser les routines
- ❌ **0 advisor / 0 verification** — qualité aléatoire
- ❌ **Tout en Opus** — coût ×5 inutile sur exécution
- ❌ **Tout en Sonnet** — qualité dégradée sur jugement
- ❌ **`max` effort** — déprécié v2.1.91, prone overthinking
- ❌ **Pipeline workflow trop long** (> 30 min sur CRUD) — frustration, supersédé doctrine 22 mai
- ❌ **REFACTOR phase systématique** dans pipeline — supprimée doctrine 22 mai

### Boundaries
- ❌ **Tout dans CLAUDE.md** — sortir routines en skills, règles 100% en hooks
- ❌ **CTO orchestrateur agent** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Doc agent dédié** — pas d'agent doc (cf [[feedback_no_doc_agent]])

### Parallélisation
- ❌ **5 sessions sur features dépendantes** — conflits worktrees
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
- **Boris Cherny** : 259 PRs/30j (déc 2025, Opus 4.5), "few dozen + 150 record" (avril 2026)
- **Noah Zweben** : +300% PRs équipe sur 3 mois
- **Cat Wu** : +200% PRs/eng org Anthropic
- **Angela Jiang** : advisor strategy 5× cost reduction

### Repos publics référence
- **[anthropics/claude-code](https://github.com/anthropics/claude-code)** : config minimaliste 3 slash commands, démonstration "minimum qui marche"
- **[anthropics/claude-code-action/CLAUDE.md](https://github.com/anthropics/claude-code-action)** : seul CLAUDE.md Anthropic public
- **[anthropics/claude-for-legal/CLAUDE.md](https://github.com/anthropics/claude-for-legal)** : 130 lignes, 5 sections
- **[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** : CLAUDE.md viral (ex-forrestchang), 70 lignes, 4 principes — fan project pas endorsé par Karpathy
- **[trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)** : entreprise sécu complète

### Pattern Karpathy
- [Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 3-layers (raw/wiki/schema), Ingest/Query/Lint, qmd (Tobi Lütke) tooling

### Erik Schluntz case study
- 22 000 LOC en 1 jour (analogie cognitive verbatim)
- Stratégies : PM guidance, leaf nodes, human core, verifiable checkpoints

---

## SOURCES — Verbatim avec URLs

### Code with Claude London 19 mai 2026 (équipe Anthropic)
- **Boris Cherny** keynote — "I prompt Claude → I create a routine that prompts Claude"
- **Cat Wu** : +200% PRs/eng
- **Lisa Crofoot** : "scaffolding holds Claude back"
- **Angela Jiang** : advisor strategy 5× cost reduction
- **Noah Zweben** : +300% PRs équipe 3 mois
- **Daisy Hollman** : ...
- **Jeremy Hadfield** : Dreaming feature

### Code with Claude SF 6-7 mai 2026
- **Erik Schluntz** : Vibe Coding in Prod (PM guidance, leaf nodes, human core, verifiable checkpoints)
- **Thariq Shihipar** : Agent SDK Workshop + HTML markdown (lethal trifecta, swiss cheese, 99% tokens planning, compute allocator)

### Sequoia AI Ascent 29 avril 2026
- **Boris** : "coding is solved"
- **Karpathy** : "Vibe coding is over → Agentic engineering"

### Pragmatic Engineer
- **Boris** : "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"

### Anthropic engineering blog
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent

### Martin Fowler / Birgitta Böckeler
- 2 avril 2026 — Guides+Sensors, "Agent = Model + Harness"

### Addy Osmani
- Harness Engineering — Forge 79.8% vs CC 58%, Ratchet Principle

---

## GOTCHAS — Pièges observés

### Pièges parallélisation
- **Multi-clauding sur features dépendantes** = conflits worktrees, perte temps
- **Pas de `/clear` entre tâches** = pollution contexte
- **Subagent qui commit malgré "pas de commit"** — TOP du prompt en gras (cf [[feedback_subagent_autocommit]])

### Pièges modèle
- **`effort: max` déprécié** v2.1.91 — utiliser `xhigh`
- **`xhigh` partout = coût massif** — réservé architect/dev-lead/refactor-pg
- **Opus 4.7 plus littéral** — être explicite scope et parallélisme

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

Aliases déclarés en frontmatter (10) :
- workflow claude code optimal
- workflow boris 2026
- routines claude code
- advisor strategy 5x
- multi-clauding
- leaf nodes erik schluntz
- compounding error driven
- verifiable checkpoints
- parallelisation 5 sessions
- compute allocator

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
- [[Angela Jiang]]
- [[Lisa Crofoot]]
- [[Noah Zweben]]
- [[Daisy Hollman]]
- [[Jeremy Hadfield]]
- [[Erik Schluntz]]
- [[Justin Young]]
- [[Thariq Shihipar]]
- [[Andrej Karpathy]]
- [[Martin Fowler]]
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

**Fin note canonique `workflow-claude-code-optimal.md`** — 6/8 chantier 22 mai 2026.
