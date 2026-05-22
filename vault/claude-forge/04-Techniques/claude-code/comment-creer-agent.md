---
titre: "Comment créer un agent Claude Code parfait"
resume: "Note canonique pour créer un agent Claude Code — frontmatter complet, 2-agent architecture Justin Young, modèles Sonnet/Opus split, convention 8 couleurs, max 6-8 ops/agent, anti-patterns CTO orchestrator."
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
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "Justin Young (MTS Anthropic)"
  - "Code with Claude SF 6-7 mai 2026"
  - "docs.claude.com/agents"
  - "Martin Fowler — Agent = Model + Harness"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/agents"
  - "#doctrine/2026"
---

# Comment créer un agent Claude Code parfait

> Note canonique forge — création d'agents selon doctrine Anthropic + Justin Young + Fowler mai 2026.

---

## QUOI — Définition

**Agent Claude Code** = sous-instance Claude spécialisée par un fichier `.claude/agents/<nom>.md`, avec frontmatter contrôlant son modèle, ses outils, son contexte, ses permissions. Invoqué via le `Agent` tool depuis la session principale.

**Verbatim Fowler** :

> "Agent = Model + Harness"
> — Martin Fowler + Birgitta Böckeler

Le **harness** = tout ce qui n'est pas le modèle : prompt système, outils disponibles, hooks, validation, état partagé.

**Stat harness > modèle** :
- LangChain : **52.8% → 66.5%** sur Terminal Bench avec **même modèle, harness changes seuls**
- Forge AI : **79.8% vs 58%** Claude Code = **+21.8 pts harness > model** (Addy Osmani)

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
- **Modèles adaptés** (Sonnet exécution, Opus jugement)
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
effort: low | medium | high | xhigh
color: red | orange | yellow | green | blue | purple | cyan | pink
memory: project
permissionMode: acceptEdits | auto | plan
disallowedTools: <outils interdits, ex Write, Edit>
skills: <skills mobilisées, optionnel>
max-turns: <nombre, optionnel>
---
```

### Règles frontmatter critiques

1. **`name`** = nom du fichier sans `.md`, kebab-case
2. **`description`** = trigger directive 3e personne (comme skills)
3. **`model`** :
   - `sonnet` = `claude-sonnet-4-6` (exécution)
   - `opus` = `claude-opus-4-7` (jugement)
   - `haiku` = `claude-haiku-4-5` (tâches courtes ultra-rapides)
4. **`effort`** :
   - `low`/`medium` = coût/latence
   - `high` = défaut sur la plupart des agents
   - `xhigh` = défaut Opus 4.7, **RÉSERVÉ** architect / dev-lead / refactor-pg
   - `max` **DÉPRÉCIÉ** depuis v2.1.91 (prone overthinking)
5. **`memory: project`** = OBLIGATOIRE sur TOUS les agents (gère mémoire automatique)
6. **`permissionMode`** = OBLIGATOIRE — `acceptEdits` pour créateurs sinon auto bloque
7. **`disallowedTools: Write, Edit`** sur agents read-only (force délégation)

### Politique modèles forge (validée 21 mai 2026)

- **Sonnet** = exécution (la plupart des agents : dev, test-writer, code-reviewer, etc.)
- **Opus** = jugement (architect, devils-advocate, project-auditor, outcomes-grader)
- **Haiku** = checks rapides (anti-rationalization, classifiers)

### Convention couleurs forge (cross-repo)

| Couleur | Catégorie |
|---------|-----------|
| **red** | Sécurité / Critique (devils-advocate, audits sécu) |
| **orange** | Review / Validation (code review, optim SQL) |
| **yellow** | Test / Évaluation / Debug |
| **green** | Développement (implem features) |
| **blue** | Architecture / Design (architect, API design) |
| **purple** | Analyse / Stratégie (codebase analyzer, schema mapping) |
| **cyan** | Infra / Maintenance (refactoring, migration) |
| **pink** | Meta-créateurs (skill-creator, agent-creator — forge only) |

**Règle cross-repo** : même rôle = même couleur sur TOUS les repos. Un `architect` est toujours `blue`.

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
- Sonnet/Opus split appliqué (jugement vs exécution)
- `disallowedTools` sur read-only (project-auditor, code-reviewer)
- Skills injectées + référencées dans body
- Convention couleurs cross-repo

### Niveau expert : 2-agent architecture Justin Young

**Pattern verbatim Justin Young (MTS Anthropic)** — [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

```
┌─────────────────┐         ┌──────────────────┐
│  Init Agent     │────────►│  Coding Agent    │
│  (planning,     │  spec   │  (implementation)│
│   sketching)    │         │                  │
└─────────────────┘         └──────────────────┘
       Opus                       Sonnet
```

- **Init agent** = Opus, jugement, planification, sketching, sélection outils
- **Coding agent** = Sonnet, exécution rapide, focused, implémente la spec
- Init produit un contexte structuré que Coding consomme

Démontré sur tâches **long-running** où la séparation phase pensée / phase exécution améliore qualité ET coût.

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Sonnet/Opus split | Coût ~5× réduit sur exécution (Sonnet), qualité préservée sur jugement (Opus) |
| 2-agent architecture | Long-running tasks : qualité préservée + coût optimisé (Justin Young) |
| Harness > model (Fowler) | +21.8 pts Terminal Bench avec même modèle (Addy Osmani Forge vs CC) |
| LangChain harness changes | 52.8% → 66.5% avec même modèle, harness seul |
| `disallowedTools` read-only | Empêche modifications accidentelles, force délégation |
| Skills injectées + référencées | Auto-activation contextualisée, ~0 token gaspillé |
| Advisor strategy 5× (Angela Jiang) | Cost reduction 5× sur agents long-running avec advisor pattern |

---

## ANTI-PATTERNS

### Architecture
- ❌ **Agent CTO orchestrateur** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Agent doc** — pas d'agent dédié à la doc, l'agent qui code update aussi
- ❌ **Agent monolithique** > 6-8 ops/agent — découper

### Frontmatter
- ❌ **Pas de `memory: project`** — mémoire pas gérée
- ❌ **Pas de `permissionMode`** — auto-mode bloque
- ❌ **`effort: max`** — déprécié v2.1.91, prone overthinking
- ❌ **`effort: xhigh` partout** — réservé architect/dev-lead/refactor-pg
- ❌ **Description en 1ère personne** — toujours 3e personne directive
- ❌ **Pas de `color`** — convention forge OBLIGATOIRE

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
- **Justin Young pattern** — anthropic.com/engineering/effective-harnesses-for-long-running-agents (Init+Coding)
- **Anthropic team** internalement utilisé : +200% PRs/eng (Cat Wu, London), +300% PRs équipe 3 mois (Noah Zweben)

### Référence harness
- **Forge AI** (Addy Osmani) — 79.8% Terminal Bench vs CC 58% = +21.8 pts harness seul
- **LangChain** — 52.8% → 66.5% avec même modèle, harness changes
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
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Justin Young 2-agent architecture
- docs.claude.com/agents — frontmatter spec
- features-overview — `memory: project`, `permissionMode`

### Code with Claude London 19 mai 2026
- **Cat Wu** : +200% PRs/eng org Anthropic
- **Noah Zweben** : +300% PRs équipe sur 3 mois
- **Angela Jiang** : advisor strategy 5× cost reduction
- **Lisa Crofoot** : "scaffolding holds Claude back"

### Code with Claude SF 6-7 mai 2026
- **Erik Schluntz** : Vibe Coding in Prod, leaf nodes, human core, verifiable checkpoints
- **Thariq Shihipar** : Agent SDK Workshop, lethal trifecta, swiss cheese, 3-way trade-offs

### Martin Fowler / Birgitta Böckeler
- [martinfowler.com](https://martinfowler.com) — "Agent = Model + Harness", Guides+Sensors taxonomy 2 avril 2026

### Addy Osmani
- Harness Engineering article — Forge 79.8% vs CC 58%, Ratchet Principle

### Hashimoto (Ghostty)
- Origine du terme "harness engineering"
- `AGENTS.md` compounding pattern

---

## GOTCHAS — Pièges observés

### Pièges modèle / effort
- **`effort: max` déprécié** v2.1.91 — utiliser `xhigh` ou `high`
- **`xhigh` partout = coût massif** — réservé architect/dev-lead/refactor-pg
- **Opus 4.7 plus littéral** — être explicite sur scope et parallélisme
- **Modèle IDs exacts** : sonnet→`claude-sonnet-4-6`, opus→`claude-opus-4-7`, haiku→`claude-haiku-4-5`

### Pièges permissions
- **`permissionMode` OBLIGATOIRE** — sans, auto-mode bloque (cf [[feedback_permissionmode_mandatory]])
- **`permissions.allow`** : non hérité par sub-agents (cf [[reference_subagent_permissions]])
- **Worktree access + MCP tools** : OK depuis v2.1.101

### Pièges memory
- **`memory: project`** OBLIGATOIRE — gère mémoire automatiquement, pas besoin scripts manuels (cf [[feedback_memory_mandatory]])

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
- **Convention couleurs cross-repo** stricte

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
- [[Noah Zweben]]
- [[Angela Jiang]]
- [[Lisa Crofoot]]
- [[Erik Schluntz]]
- [[Martin Fowler]]
- [[Addy Osmani]]
- [[Hashimoto]]

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

**Fin note canonique `comment-creer-agent.md`** — 4/8 chantier 22 mai 2026.
