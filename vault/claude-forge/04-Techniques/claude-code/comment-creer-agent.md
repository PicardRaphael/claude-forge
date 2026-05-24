---
titre: "Comment créer un agent Claude Code parfait"
resume: "Note canonique pour créer un agent Claude Code — frontmatter complet, 2-agent architecture Justin Young (sans split modèles), Sonnet/Opus split doctrine forge cohérente avec Cat Wu + Brad Abrams, convention 8 couleurs forge, anti-patterns CTO orchestrator."
aliases:
  - "comment creer agent"
  - "creer un agent claude code"
  - "create claude code agent"
  - "agent parfait"
  - "agent best practices"
  - "2-agent architecture"
  - "harness agent"
  - "convention couleurs agents"
  - "frontmatter agent"
  - "sonnet opus split"
derniere-maj: 2026-05-24
auteur: claude
type: technique
sources:
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "Justin Young (MTS Anthropic) — Initializer + Coding agent (sans split modèles)"
  - "Cat Wu — Code with Claude London 19 mai 2026 (Opus 4.7 + xhigh)"
  - "Brad Abrams — Code with Claude SF 6 mai 2026 (Advisor Strategy)"
  - "docs.claude.com/agents"
  - "Böckeler — martinfowler.com/articles/harness-engineering.html (Guides+Sensors 2 avril 2026)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/agents"
  - "#doctrine/2026"
---
# Comment créer un agent Claude Code parfait

> Note canonique forge — création d'agents selon doctrine Anthropic + Justin Young + Cat Wu + Brad Abrams + Böckeler/Fowler mai 2026.

---

> ⚠️ **Ordre canonique pour TOUTE création/modification d'agent** : suivre A→B→C→D→E (analyser réel → lire canoniques EN ENTIER → croiser → plan d'écarts → exécuter). Cf [[methode-analyser-repo]] section **ORDRE CANONIQUE**. Pas de prescription avant analyse du réel.

## QUOI — Définition

**Agent Claude Code** = sous-instance Claude spécialisée par un fichier `.claude/agents/<nom>.md`, avec frontmatter contrôlant son modèle, ses outils, son contexte, ses permissions. Invoqué via le `Agent` tool depuis la session principale.

**Concept "Agent = Model + Harness"** :
- Popularisé par **Mitchell Hashimoto** (5 février 2026, [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey)) — terme "harness engineering"
- Formalisé par **LangChain**
- Repris par **Birgitta Böckeler** (Thoughtworks, 2 avril 2026, [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html))
- Verbatim Böckeler : "the harness is everything in an AI agent **except the model itself**" — guides steer before action, sensors catch problems after

Le **harness** = tout ce qui n'est pas le modèle : prompt système, outils disponibles, hooks, validation, état partagé.

**Stat harness > modèle** :
- LangChain : **52.8% → 66.5%** Terminal Bench avec **harness changes seuls**. Source : **Vivek Trivedy, LangChain blog 17 février 2026** ([langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)). Modèle = **GPT-5.2-Codex** (pas Claude). Böckeler 2 avril 2026 cite ce résultat sans le revendiquer.
- ForgeCode Terminal-Bench 2.0 ≈ **79.8%** (Nicolas Bustamante — [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit)). Comparaison à Claude Code et spread "+21.8 pts" **non sourcés directement chez Addy Osmani** ([addyosmani.com/blog/agent-harness-engineering/](https://addyosmani.com/blog/agent-harness-engineering/) qualitatif uniquement).

Le harness compte autant que le modèle.

---

## POURQUOI — Le problème résolu

Sans agents spécialisés, la session principale fait tout :
- **Pollution contexte** — recherches massives consomment le contexte principal
- **Pas de boundaries** — pas de restriction d'outils par rôle
- **Pas de modèle adapté** — code review = Sonnet, mais jugement archi = Opus
- **Pas de parallélisation** — 1 thread principal séquentiel

Avec agents :
- **Délégation focalisée** — 1 rôle = 1 agent
- **Boundaries explicites** (`allowed-tools`, `disallowedTools`)
- **Modèles adaptés** (Sonnet exécution, Opus jugement — doctrine forge)
- **Parallélisation** (multi-agents simultanés)

---

## COMMENT — Frontmatter complet

### Frontmatter de référence

```yaml
---
name: <nom-exact-du-fichier-sans-md>
description: <trigger directive 3e personne, max ~500 chars>
tools: <outils autorisés, séparés par virgule>
model: sonnet | opus | haiku
effort: low | medium | high | xhigh | max
color: red | orange | yellow | green | blue | purple | cyan | pink
memory: project
permissionMode: acceptEdits | auto | plan | default | dontAsk | bypassPermissions
disallowedTools: <outils interdits, ex Write, Edit>
skills: <skills mobilisées, optionnel>
maxTurns: <nombre, optionnel>
---
```

### Règles frontmatter critiques

1. **`name`** = nom du fichier sans `.md`, kebab-case
2. **`description`** = trigger directive 3e personne (comme skills)
3. **`model`** :
   - `sonnet` = `claude-sonnet-4-6` (exécution)
   - `opus` = `claude-opus-4-7` (jugement)
   - `haiku` = `claude-haiku-4-5` (tâches courtes ultra-rapides)
4. **`effort`** (verbatim docs Anthropic 23 mai 2026) :
   - Options : `low`, `medium`, `high`, `xhigh`, `max`
   - "Available levels depend on the model"
   - `max` **TOUJOURS DISPONIBLE** (mai 2026). Ce qui est déprécié = `budget_tokens` manuel, remplacé par adaptive thinking
   - Doctrine forge : `high` partout par défaut, `xhigh` réservé architect/dev-lead/refactor-pg, `max` avec prudence (prone overthinking observé)
5. **`memory: project`** = OBLIGATOIRE sur TOUS les agents forge (gère mémoire automatique)
6. **`permissionMode`** = OBLIGATOIRE forge :
   - `acceptEdits` pour créateurs (skill-creator, agent-creator, hook-creator, claudemd-optimizer)
   - `auto` pour exécutants (dev, code-reviewer, test-writer)
   - `plan` pour agents qui doivent **toujours passer par un plan validé** avant action
7. **`disallowedTools: Write, Edit`** sur agents read-only (force délégation)

### Politique modèles forge (doctrine inférée cohérente avec Anthropic)

> **Important honnêteté** : la politique "Sonnet exécution / Opus jugement" est une **doctrine forge inférée** par pattern observé en sessions. **Cohérente avec** :
> - **Cat Wu** (Code with Claude London 19 mai 2026) : "Opus 4.7 tips — delegate, write full-context briefs, use the new `xhigh` effort level"
> - **Brad Abrams** (Code with Claude SF 6 mai 2026, Advisor Strategy talk) : executor model (Haiku) + advisor model (Opus implicite)
>
> Aucune doctrine Anthropic verbatim n'énonce explicitement "Sonnet = exécution, Opus = jugement". C'est une généralisation forge.

| Modèle | Rôle forge | Exemples |
|--------|-----------|----------|
| **Sonnet** | Exécution | dev, code-reviewer, test-writer, python-dev |
| **Opus** | Jugement | architect, devils-advocate, project-auditor, outcomes-grader |
| **Haiku** | Checks rapides | classifiers, anti-rationalization |

### Convention couleurs forge (cross-repo)

> **Note** : convention forge perso, pas Anthropic. Anthropic accepte `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` comme valeurs valides (verbatim docs frontmatter), mais ne prescrit pas leur usage.

| Couleur | Catégorie forge |
|---------|-----------|
| **red** | Sécurité / Critique (devils-advocate, audits sécu) |
| **orange** | Review / Validation (code review, optim SQL) |
| **yellow** | Test / Évaluation / Debug |
| **green** | Développement (implem features) |
| **blue** | Architecture / Design (architect, API design) |
| **purple** | Analyse / Stratégie (codebase analyzer, schema mapping) |
| **cyan** | Infra / Maintenance (refactoring, migration) |
| **pink** | Meta-créateurs (skill-creator, agent-creator — forge only) |

**Règle cross-repo forge** : même rôle = même couleur sur TOUS les repos. Un `architect` est toujours `blue`.

---

## QUAND — Critère d'application

### Créer un agent quand :
- Un **rôle dev récurrent** émerge (architect, dev-feature, code-reviewer, test-writer, debugger, sécu-auditor)
- Une **boundary** est nécessaire (lecture seule, outils restreints, modèle dédié)
- **Parallélisation** souhaitée (multi-agents en parallèle)
- **Délégation focalisée** pour éviter pollution contexte

### NE PAS créer un agent quand :
- Pour une procédure réutilisable → **Skill**
- Pour un accès données → **MCP**
- Pour une règle 100% → **Hook**
- Si la session principale suffit (S/M tasks simples)

### Anti-pattern majeur : agent CTO orchestrateur
- ❌ **JAMAIS d'agent orchestrateur** — la session principale orchestre via rules (cf [[feedback_no_cto_agent]])

---

## WORKFLOW — Création étape par étape

### Étape 1 — Identifier le rôle
Lister les rôles dev récurrents du repo. Chaque rôle distinct = candidat agent.

### Étape 2 — Définir boundaries
- Outils nécessaires (`tools`)
- Outils interdits (`disallowedTools`)
- Skills mobilisées (`skills`)
- Modèle adapté (sonnet/opus/haiku)
- Effort niveau (high défaut)

### Étape 3 — Déléguer à `agent-creator`
Côté forge : agent `agent-creator` génère le `.md` conforme. Hook `delegate-guard.py` bloque l'édit direct.

### Étape 4 — Référencer skills dans le body
**Si tu mets une skill dans `skills:` frontmatter, tu DOIS la référencer dans le body avec instructions d'usage.** Sinon orpheline = jamais activée (cf [[feedback_skills_referenced_in_body]]).

### Étape 5 — Tester en isolation
Invoquer l'agent depuis session vierge. Vérifier :
- Trigger marche (description directive efficace)
- Outils suffisants (rien ne manque)
- Outils restreints respectés (disallowedTools)

### Étape 6 — DA si livrable majeur (CONDITIONNEL)
Côté forge : `devils-advocate` UNIQUEMENT si livrable majeur (agent orchestrant, agent sécu, agent cross-repos). Doctrine 22 mai : pas de gates systématiques (cf [[raisonnement-22mai-doctrine-vs-enforcement]] + [[feedback_pipeline_quality_gates]]). DA reste **conditionnel ciblé**.

---

## APPELS — Composants mobilisés

- [[comment-creer-skill]] — skills injectées via `skills:` frontmatter
- [[comment-creer-hook]] — hooks qui encadrent les agents
- [[comment-ecrire-claudemd]] — où mentionner les agents du repo
- [[workflow-claude-code-optimal]] — comment agents s'inscrivent dans le workflow
- [[methode-analyser-repo]] — méthode pour identifier les rôles → agents

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- 1 agent par rôle critique (architect, dev, reviewer)
- Tous Sonnet effort high
- `memory: project` partout
- `permissionMode: acceptEdits`

### Niveau avancé
- Sonnet/Opus split appliqué (jugement vs exécution, doctrine forge)
- `disallowedTools` sur read-only (project-auditor, code-reviewer)
- Skills injectées + référencées dans body
- Convention couleurs cross-repo forge

### Niveau expert : 2-agent architecture Justin Young (Anthropic)

**Pattern Justin Young — verbatim source officielle** :
Source : [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

```
┌─────────────────┐         ┌──────────────────┐
│  Initializer    │────────►│  Coding Agent    │
│  Agent          │  spec   │  (implementation)│
└─────────────────┘         └──────────────────┘
```

- **Initializer agent** : reçoit un prompt initial différent, produit la spec/contexte structuré
- **Coding agent** : reçoit la spec, implémente
- **Footnote 1 verbatim** : *"The system prompt, set of tools, and overall agent harness was otherwise identical"*
- **Pas de split modèles** dans l'article — seul Opus 4.5 mentionné comme baseline failure sans harness
- Le seul **différentiateur** entre les 2 agents = leurs initial user prompts

> ⚠️ Erreur historique forge : avant audit 23 mai 2026, cette doctrine était présentée comme "Init = Opus, Coding = Sonnet". **Extrapolation forge non sourcée**. Le 2-agent architecture est canonique, le split modèles n'est pas chez Justin Young — cohérent avec doctrine forge Sonnet/Opus split via d'autres sources (Cat Wu, Brad Abrams) mais pas verbatim Justin Young.

Démontré sur tâches **long-running** où la séparation init / exécution améliore qualité.

### Pattern Advisor Strategy (Brad Abrams, Anthropic Product Lead Claude)

Source : [Code with Claude SF — "Caching, harnesses, and advisors: Building on Claude at GitHub scale"](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale) (talk avec Mario Rodriguez, GitHub CPO).

```
┌──────────────┐  query   ┌────────────────┐
│  Executor    │─────────►│  Advisor       │
│  (Haiku)     │◄─────────│  (Opus)        │
│              │  advice  │                │
└──────────────┘          └────────────────┘
```

- **Executor model** : smaller (ex: Haiku), exécute la majorité des appels
- **Advisor model** : larger (Opus), consulté ponctuellement quand l'executor demande conseil
- **Verbatim Brad Abrams** : *"We get close to Opus-level intelligence at much lower prices because we're being very conservative about the tokens that advisor actually sends"*
- Pattern utilisé chez **GitHub Copilot** à scale

→ Pas un chiffre "5×" comme parfois cité (coquille propagée depuis live blog Simon Willison "Angela Kiang" → "Angela Jiang"). Le verbatim Abrams ne donne pas de multiplicateur précis.

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Sonnet/Opus split | Coût ~5× réduit sur exécution (Sonnet), qualité préservée sur jugement (Opus) — observation forge |
| 2-agent architecture Justin Young | Long-running tasks : qualité préservée par séparation init/coding |
| Advisor Strategy (Brad Abrams) | "Close to Opus-level intelligence at much lower prices" (verbatim) — pattern GitHub Copilot |
| LangChain harness changes | 52.8% → 66.5% Terminal Bench avec même modèle, harness seul (Vivek Trivedy 17 fév 2026, GPT-5.2-Codex) |
| `disallowedTools` read-only | Empêche modifications accidentelles, force délégation |
| Skills injectées + référencées | Auto-activation contextualisée, ~0 token gaspillé |

---

## ANTI-PATTERNS

### Architecture
- ❌ **Agent CTO orchestrateur** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Agent doc** — pas d'agent dédié à la doc, l'agent qui code update aussi
- ❌ **Agent monolithique** — découper en plusieurs rôles distincts
- ❌ **Agent qui invoque un autre agent (ré-entrance)** : risque de boucle infinie ou tool_use partagés conflictuels. Si nécessaire, passer par la session principale qui orchestre. Mise en garde forge — pas doctrine Anthropic explicite.

### Frontmatter
- ❌ **Pas de `memory: project`** — mémoire pas gérée (règle forge)
- ❌ **Pas de `permissionMode`** — auto-mode bloque (règle forge)
- ❌ **`effort: max` par défaut** — coût massif, réserver à cas justifiés
- ❌ **`effort: xhigh` partout** — réservé architect/dev-lead/refactor-pg (règle forge)
- ❌ **Description en 1ère personne** — toujours 3e personne directive
- ❌ **Pas de `color`** — convention forge

### Skills / tools
- ❌ **Skills dans `skills:` mais pas dans body** = orphelines (cf [[feedback_skills_referenced_in_body]])
- ❌ **`Bash` sur agent orchestrateur** — retirer pour forcer délégation (cf [[feedback_agent_tools_restriction]])
- ❌ **Pas de `disallowedTools` sur read-only** — risque modifs accidentelles

### Comportement
- ❌ **Agent qui commit dans repo externe** sans demande explicite (cf [[feedback_never_commit_foreign_repos]])
- ❌ **Sous-agent qui commit** malgré instruction "pas de commit" en fin de prompt → mettre en TOP en gras (cf [[feedback_subagent_autocommit]])
- ❌ **Sub-agent permissions** : `permissions.allow` toujours non hérité (cf [[reference_subagent_permissions]])
- ❌ **Édit direct `.md` agent** — délégation obligatoire à `agent-creator` (hook bloque)

---

## EXEMPLES CONCRETS — Repos externes

### Référence Anthropic
- **`anthropics/claude-code-action`** — workflow d'agent GitHub Action
- **Justin Young 2-agent** : [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Initializer + Coding, harness identique)
- **Brad Abrams Advisor Strategy** : Code with Claude SF, talk avec GitHub
- **Anthropic team** internalement : +300% PRs équipe sur 3 mois (Noah Zweben, CwC London — verbatim Every : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March")

### Référence harness
- **LangChain** : 52.8% → 66.5% Terminal Bench (Vivek Trivedy 17 fév 2026, GPT-5.2-Codex)
- **ForgeCode** (Bustamante) : 79.8% Terminal-Bench 2.0
- **Cognition Labs Devin** — harness avancé multi-agents

### Référence Trail of Bits
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- Anti-rationalization Stop hook : agent Haiku check cop-outs sur la session principale
- 3-tier sandbox boundaries

### Référence Karpathy
- `karpathy/nanochat/.claude/skills/` — Karpathy publie peu d'agents publics, focus skills atomiques

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent architecture (initializer + coding, harness identique)
- [code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents) — frontmatter spec, effort levels
- [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) — créer custom subagents
- [Code with Claude SF — Caching/Harnesses/Advisors](https://claude.com/code-with-claude/session/sf-caching-harnesses-and-advisors-building-on-claude-at-github-scale) — Brad Abrams + Mario Rodriguez

### Code with Claude London 19 mai 2026
- **Cat Wu** (Head of Product Claude Code) : Opus 4.7 tips, xhigh effort level
- **Noah Zweben** : "weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March"
- **Lisa Crofoot** : "scaffolding holds Claude back" (single source à confirmer)
- **Daisy Hollman** : "You should be running agents overnight" / "red squigglies for agents"
- **Fiona Fung** (Head of Engineering Anthropic) : "Pick your noisiest workflow…and ask if it's still serving its purpose" + "In technical debates, code wins"
- **Jeremy Hadfield** : Dreaming feature

### Code with Claude SF 6-7 mai 2026
- **Erik Schluntz** : Vibe Coding in Prod (PM guidance, leaf nodes, human core, verifiable checkpoints) — "22 000 LOC en 1 jour" est une analogie cognitive, pas une métrique brute
- **Thariq Shihipar** : Agent SDK Workshop, compute allocators verbatim "All of us are becoming these compute allocators now" (ChatPRD How I AI)
- **Brad Abrams** : Advisor Strategy

### Hashimoto / Böckeler / Bustamante
- [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) — popularisation "harness engineering" (5 fév 2026)
- [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Böckeler Guides+Sensors 2 avril 2026
- [langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — Vivek Trivedy 17 fév 2026
- [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit) — ForgeCode 79.8%
- [addyosmani.com/blog/agent-harness-engineering/](https://addyosmani.com/blog/agent-harness-engineering/) — Addy Osmani qualitatif

---

## GOTCHAS — Pièges observés

### Pièges modèle / effort
- **`effort: max` toujours disponible** mai 2026 (verbatim docs) — utiliser avec prudence (prone overthinking)
- **`xhigh` partout = coût massif** — réservé architect/dev-lead/refactor-pg (forge)
- **Opus 4.7 plus littéral** — être explicite sur scope et parallélisme (observation forge)
- **Modèle IDs exacts** : sonnet→`claude-sonnet-4-6`, opus→`claude-opus-4-7`, haiku→`claude-haiku-4-5`

### Pièges permissions
- **`permissionMode` OBLIGATOIRE** côté forge — sans, auto-mode bloque (cf [[feedback_permissionmode_mandatory]])
- **`permissions.allow`** : non hérité par sub-agents (cf [[reference_subagent_permissions]])
- **Worktree access + MCP tools** : OK depuis v2.1.101

### Pièges memory
- **`memory: project`** OBLIGATOIRE forge — gère mémoire automatiquement, pas besoin scripts manuels (cf [[feedback_memory_mandatory]])

### Pièges skills
- **Skills dans `skills:` non référencées dans body** = orphelines, jamais activées (cf [[feedback_skills_referenced_in_body]])

### Pièges délégation
- **Édit direct bloqué** par hook `delegate-guard.py` — utiliser `agent-creator`
- **Sub-agent commit autonome** — mettre "PAS DE COMMIT" en TOP du prompt en gras (cf [[feedback_subagent_autocommit]])
- **Repo externe** : pas de git autonome (cf [[feedback_never_commit_foreign_repos]])

### Pièges Windows
- **Python path absolu** dans hooks référencés par agent (Windows alias MS Store sinon)
- **Heredoc Bash Windows** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])

### Pièges forge
- **Vault check obligatoire** avant création (cf [[forge-brain-proactive]])
- **DA après création majeure** (cf [[devils-advocate-pipeline]])
- **Convention couleurs cross-repo** stricte (forge)

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- comment creer agent
- creer un agent claude code
- create claude code agent
- agent parfait
- agent best practices
- 2-agent architecture
- harness agent
- convention couleurs agents
- frontmatter agent
- sonnet opus split

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]

### Fiches leaders (à créer)
- [[Justin Young]]
- [[Cat Wu]]
- [[Brad Abrams]]
- [[Noah Zweben]]
- [[Daisy Hollman]]
- Fiona Fung (Head of Engineering Anthropic) — fiche à créer
- [[Jeremy Hadfield]]
- [[Erik Schluntz]]
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]
- [[Addy Osmani]]

### Knowledge / erreurs / refs
- [[feedback_no_cto_agent]]
- [[feedback_memory_mandatory]]
- [[feedback_permissionmode_mandatory]]
- [[feedback_skills_referenced_in_body]]
- [[feedback_agent_tools_restriction]]
- [[feedback_subagent_autocommit]]
- [[feedback_never_commit_foreign_repos]]
- [[reference_subagent_permissions]]
- [[erreur-da-heredoc-bash-silencieux]]

### Forge custom
- [[agent-creator]] — agent forge dédié
- [[devils-advocate-pipeline]] — rule DA après création
- [[agents-color-convention]] — rule couleurs cross-repo
- [[forge-brain-proactive]] — rule vault check

---

**Fin note canonique `comment-creer-agent.md`** — révisée 23 mai 2026 post-audit thématique vault.

---

## AJOUT 23 MAI 2026 — Alternative orchestration via PTC

Pour les tâches **multi-tools déterministes** (orchestration sans jugement à chaque étape), **Programmatic Tool Calling (PTC)** est une alternative au pattern sub-agents qui évite le "token tax" du contexte qui gonfle.

### Pattern complémentaire (pas concurrent)

- **Sub-agent (Justin Young 2-agent)** : initializer + coding agent. Chaque sub-agent peut faire du jugement contextuel. Résultats re-entrent dans contexte orchestrateur.
- **PTC** : Claude écrit Python qui orchestre N tool calls dans sandbox. Seul output final entre dans contexte. 1 inference vs N inferences.

### Quand préférer PTC

- ✅ Orchestration déterministe (loops, conditionals, data transformations)
- ✅ Filtrage / agrégation de gros volumes avant decision
- ✅ Réduction token consumption critique (workloads scale)
- ❌ PAS quand jugement contextuel requis à chaque étape

### Quand préférer sub-agents

- ✅ Tâches nécessitant jugement à chaque étape
- ✅ Multi-step reasoning chained
- ✅ Long-running avec context différencié par sub-agent

### Détail technique complet

Voir [[programmatic-tool-calling]] — note canonique avec config API, métriques, gotchas, comparaison détaillée.

### Sources

- [Docs Anthropic PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [[programmatic-tool-calling]] — note canonique forge

`derniere-maj` à mettre à jour après ce ajout.


## Anti-patterns

- [[erreur-seuils-canoniques-agents-inventes-2026-05-22]] — 4/5 seuils "canoniques" agents Claude Code cités dans le vault étaient des mythes (extrapolations, confusion). Seuls CLAUDE.md<200L et SKILL.md<500L sont vraiment canoniques.
