---
titre: "Méthode pour analyser un repo et proposer config Claude Code optimale"
resume: "Grille canonique 6 étapes pour analyser tout repo et proposer skills/agents/hooks/CLAUDE.md/workflow optimaux. Pipeline standard architect → dev → reviewer → test, pas systématique. Source de vérité actionnable pour 'analyse ce repo, propose-moi la config CC'."
aliases:
  - "methode analyser repo"
  - "analyse repo claude code"
  - "config claude code optimale"
  - "grille analyse repo"
  - "audit setup repo"
  - "proposer config claude code"
  - "6 etapes analyse repo"
  - "kit rules standard"
  - "scan architecture"
  - "mapper roles agents"
  - "comment automatiser un repo claude code"
  - "automate repo setup"
  - "automatiser projet claude code"
  - "pipeline architect dev test"
derniere-maj: 2026-05-25
auteur: claude
type: technique
sources:
  - "Code with Claude London 19 mai 2026"
  - "Code with Claude SF 6-7 mai 2026"
  - "github.com/anthropics/claude-code"
  - "github.com/anthropics/claude-for-legal"
  - "github.com/trailofbits/claude-code-config"
  - "github.com/multica-ai/andrej-karpathy-skills"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/methode"
  - "#meta"
---
<!-- TODO 2026-05-24: note >500L — extraction sections vers references/ -->

# Méthode pour analyser un repo et proposer config Claude Code optimale

> **Note méta canonique forge** — quand on dit "analyse ce repo, propose-moi la config CC", cette grille s'applique.

---

## QUOI — Définition

**Grille d'analyse en 6 étapes** pour transformer un repo brut en config Claude Code complète :
- **Skills** justifiées
- **Agents** par rôle avec modèle/effort/couleur
- **Hooks** lint/security/scope (PAS workflow)
- **CLAUDE.md** squelette
- **Workflow** adapté à la taille du repo

Cette méthode est la **synthèse opérationnelle** des notes canoniques sœurs ([[comment-creer-skill]], [[comment-creer-agent]], [[comment-creer-hook]], [[comment-ecrire-claudemd]], [[workflow-claude-code-optimal]], [[mcp-vs-skills-doctrine]]).

### Étape 7 (post-audit) — Proposer hooks transversaux applicables

Après les 6 étapes d'analyse, consulter le catalogue `[[comment-creer-hook]]` section "HOOKS TRANSVERSAUX" et proposer au repo audité ceux applicables. Format : un hook par écart empirique identifié (pas un batch). Voir le catalogue pour les cas d'usage de chaque hook (`meta-commentary-detector`, `delegate-guard`, `repo-scope-guard`, `vault-query-guard`, etc.).

---

## POURQUOI — Le problème résolu

Sans grille, l'analyse est :
- **Ad-hoc** — chaque analyse réinvente la méthode
- **Incomplète** — on oublie une dimension (sécu, scope, modèle)
- **Copiée d'un autre repo** — sans tenir compte du contexte spécifique
- **Pas justifiée** — l'utilisateur reçoit une config sans le "parce que"

Avec grille :
- **Reproductible** — même méthode = même qualité
- **Exhaustive** — 6 étapes couvrent tous les besoins
- **Justifiée** — chaque proposition liée à un observable du repo
- **Adaptée** — sortie spécifique à l'archi observée

---

## ORDRE CANONIQUE — A → B → C → D → E (Anthropic Explore-Plan-Code-Commit)

**Validé par recherche web 22-23 mai 2026** : convergence Anthropic docs + Boris Cherny + Thariq Shihipar + ATAM/SAAM. Option B (analyse du réel d'abord) est canonique, pas Option A (canoniques d'abord = biais perception).

### Ordre obligatoire

```
A. ANALYSER le RÉEL (faits bruts, sans biais)
        ↓
B. LIRE canoniques EN ENTIER (read_note, pas search_brain seul)
        ↓
C. CROISER analyse ⨯ canoniques → écarts mesurables
        ↓
D. PLAN basé sur écarts (pas idéologie)
        ↓
E. EXÉCUTER après validation utilisateur
```

### A. ANALYSER le RÉEL d'abord

- Scan archi (étape 1 ci-dessous) + scan code récurrent (étape 5)
- Auditer skills/agents/hooks/rules existants (compter, lister, mesurer)
- FAITS bruts uniquement, AUCUNE prescription à ce stade

**Verbatim Anthropic** ([Best practices Claude Code](https://code.claude.com/docs/en/best-practices)) :
> "Explore: Read the codebase and understand existing implementation patterns and related files... This phase is critical because it **prevents Claude from making assumptions about your architecture**."

**Boris Cherny** (Pragmatic Engineer interview) : "Plain glob and grep, driven by the model, beat everything" — Plan Mode pour la plupart des sessions complexes (chiffre "80%" parfois cité non sourcé verbatim).

**Thariq Shihipar** : "Seeing like an Agent" + "interview me" = élicitation contexte AVANT spec.

### B. LIRE canoniques EN ENTIER (après analyse)

`mcp__forge-brain__read_note` SANS `max_lines` ou `max_lines: 500+`. `search_brain` retourne ~10 lignes — INSUFFISANT pour audit.

| Tâche | Notes canoniques à lire EN ENTIER |
|-------|----------------------------------|
| Créer/modifier agent | [[comment-creer-agent]] + [[workflow-claude-code-optimal]] |
| Créer/modifier skill | [[comment-creer-skill]] + [[mcp-vs-skills-doctrine]] |
| Créer/modifier hook | [[comment-creer-hook]] + [[raisonnement-22mai-doctrine-vs-enforcement]] |
| Optimiser CLAUDE.md | [[comment-ecrire-claudemd]] + [[pattern-vault-llm-karpathy]] |
| Auditer / analyser repo | **TOUTES** ci-dessus + cette note |

### C. CROISER analyse ⨯ canoniques → écarts mesurables

Mettre côte-à-côte FAITS observés (A) et RÈGLES canoniques (B). Lister les ÉCARTS :
- Agent X = Opus mais canonique dit Sonnet → écart sonnet/opus split
- Skill Y = 800L mais canonique dit < 500L → écart taille
- Hook Z = workflow gate mais doctrine 22 mai interdit → écart doctrinal

Pas d'opinion, pas d'idéologie. Que des **écarts mesurables**.

**Verbatim Anthropic 3-agent harness** : *Default-FAIL contract* — "every criterion starts false, agent can't mark it passing without **opening evidence first**". Évidence empirique avant verdict.

### D. PLAN basé sur les ÉCARTS

Plan = liste des écarts à fixer, priorisés. Si pas d'écart sur un point → pas de fix. Pas d'application aveugle de canonique.

**Verbatim ATAM/SAAM** ([CoStrategix](https://www.costrategix.com/insight/guide-to-evaluating-software-architecture-characteristics/)) :
> "evaluating the overall architecture's maintainability... identifying opportunities for architectural improvements, **and then ensuring that the architecture aligns with best practices** — rather than the reverse."

### E. EXÉCUTER après validation

Plan validé par utilisateur → exécution (via agents spécialisés ou Edit direct selon contexte). Capitaliser apprentissages dans vault après chantier.

### Pièges documentés (recherche web)

- **Skipper Explore** = "code that solves the wrong problem" (Anthropic docs)
- **Best practices avant analyse** = biais d'idéologie (ATAM/SAAM existent pour ça)
- **Partially-migrated codebases** (Cherny/Meta) : confondent humains ET modèles — toujours observer l'état réel avant prescrire
- **Reviewer qui a vu le build** = biais de confirmation → fresh-context evaluator obligatoire
- **Sauter Plan Mode** pour gagner du temps : "phases 1 et 2 sont les moins chères en tokens et les plus précieuses en outcome" (Anthropic)

### Sources verbatim

- [Anthropic Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Anthropic Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Pragmatic Engineer Building Claude Code with Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)
- [How Boris Uses Claude Code](https://howborisusesclaudecode.com/)
- [Thariq Vibe Code Camp Distilled](https://davidguttman.github.io/every-vibe-code-camp-distilled/14_thariq_shihipar.html)
- [CoStrategix Software Architecture Characteristics (ATAM/SAAM)](https://www.costrategix.com/insight/guide-to-evaluating-software-architecture-characteristics/)
- [InfoQ Anthropic Three-Agent Harness](https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/)

### Erreur passée à éviter

[[feedback_lire_canoniques_avant_audit]] — audit ia_back 22 mai 2026, double erreur : `search_brain` seul (extraits insuffisants), puis sur-correction "lire canoniques d'abord" = biais perception. Corrigé par Raphael : ordre A→B→C→D→E.

---

## PIPELINE STANDARD — architect → dev → code-reviewer → test (CONDITIONNEL)

> ⚠️ **Doctrine 22 mai 2026** : ce pipeline est un **template recommandé**, PAS systématique. Doctrine "Claude decides when to invoke" — la session principale décide quels rôles appeler selon la tâche.

Le pipeline canonique recommandé pour les tâches M/L/XL :

```
┌──────────┐    ┌────────┐    ┌──────────────┐    ┌────────┐
│ architect│───►│  dev   │───►│code-reviewer │───►│  test  │
│  (Opus)  │    │(Sonnet)│    │  (Sonnet)    │    │(Sonnet)│
└──────────┘    └────────┘    └──────────────┘    └────────┘
   plan          implem        review code         tests
```

| Rôle | Modèle | Effort | Quand skip ? |
|------|--------|--------|--------------|
| **architect** | Opus | xhigh | Tâche S (< 30 min), bug fix one-liner, typo |
| **dev** | Sonnet | high | Jamais skip (cœur de l'exécution) |
| **code-reviewer** | Sonnet | high | Tâche S, ou refactor pur dans repo perso |
| **test** | Sonnet | high | Skip si pas de framework test ou doc-only |

### Quand utiliser le pipeline complet

- **Tâche L/XL** (> 4h, cross-files) — pipeline complet obligatoire
- **Feature nouvelle** avec impact architecture — architect obligatoire
- **Refactor multi-files** — architect + code-reviewer obligatoires
- **Bug critique** en production — pipeline complet (verification multi-layers)

### Quand skip / alléger (cf [[raisonnement-22mai-doctrine-vs-enforcement]])

- **Tâche S** (< 30 min) — prompt direct, vérifier, commit
- **Typo / formatting** — pas d'architect
- **Hot fix sécu** — dev + code-reviewer suffit, architect si systémique
- **Doc-only** — dev seul

### Anti-patterns pipeline

- ❌ **Pipeline forcé via hook** (architect-guard, commit-guard, etc.) — doctrine 22 mai a supprimé ces hooks workflow
- ❌ **architect + dev + reviewer + test sur typo** — frustration 6× observée pré-pivot 22 mai
- ❌ **Skip architect sur archi non triviale** — code généré rate la cible
- ❌ **Skip code-reviewer sur prod-critical** — pas de verification

---

## COMMENT — Grille 6 étapes

### Étape 1 — Scanner l'architecture ET lire du code RÉEL

> **Pas que les metadata.** Le piège classique : se contenter de package.json + README + git log. C'est insuffisant pour ne pas inventer. **3-5 fichiers exemples par couche** sont obligatoires (échantillon, pas exhaustivité).

#### 1a — Observer la topologie (metadata)

- **Stack** : langages + versions (Python, TypeScript, Vue, Rust, etc.)
- **Structure** : mono-repo / microservices / monorepo workspaces
- **Database** : type (PostgreSQL, SQLite, etc.), nombre de DB, migrations
- **Tests** : framework, coverage, intégration / e2e
- **CI** : GitHub Actions, GitLab CI, Jenkins
- **Build** : npm/pnpm/yarn, pip/poetry/uv, cargo, etc.
- **Taille codebase** : LOC, nombre de fichiers, profondeur
- **MCP existants** : `.mcp.json` ou équivalent
- **`.claude/` existant** : audit ce qui est déjà là
- **Architecture documentée** : `ARCHITECTURE.md`, `docs/`, `CONTRIBUTING.md` si présents

**Outils** :
- `Glob` pour structure
- `Read package.json / pyproject.toml / Cargo.toml`
- `Read README.md` + `ARCHITECTURE.md` + `docs/` pour intent
- `git log --oneline -50` pour activité + style commits
- `tree -L 3` ou `Glob '**/*'` pour topologie

#### 1b — Lire du code RÉEL (échantillonnage représentatif)

**OBLIGATOIRE** : pas que les metadata. Lire **3-5 fichiers exemples par couche** :
- 1 route / endpoint
- 1 service / business logic
- 1 modèle / schema
- 1 test (pour comprendre style + assertions)
- 1 utilitaire transverse

**Comment choisir l'échantillon** :
- Représentatif (le plus typique, pas l'exception)
- Récent (dernières features, pas du legacy)
- Cross-couches (pas tout dans `routes/`)

**Outils** : `Read` les 3-5 fichiers identifiés. **Lecture intégrale** (pas extraits).

#### 1c — Grep patterns récurrents (conventions implicites)

Avant de proposer des conventions dans CLAUDE.md, observer ce qui EST déjà fait :
- **Naming** : `camelCase` vs `snake_case` vs `kebab-case` selon couche
- **Error handling** : try/except patterns, custom exceptions, error wrappers
- **Logging** : console.log vs logger structuré, niveaux utilisés
- **Mocking** : MagicMock vs vraie DB en test
- **Async** : async/await vs callbacks vs Promises

**Outils** :
- `Grep` pour patterns récurrents (ex: `grep -r "raise.*Error" --type=py`)
- `Grep` imports communs (ex: stack OLD vs NEW — cf `feedback_drizzle_postgresjs_drift`)

#### 1d — Comprendre les frontières

- **Mono-repo workspace** : où sont les libs partagées ? Les apps ?
- **Microservices** : points de couplage (RPC, queue, DB partagée) ?
- **Modules** : qui dépend de qui ? Circular deps ?

#### Sortie étape 1

Note technique 1-2 pages max :
- Stack + topologie + signaux forts (1a)
- 3-5 fichiers lus avec ce qu'on a compris (1b)
- Patterns récurrents observés (1c)
- Frontières + dépendances (1d)

**Anti-pattern** : se contenter de 1a. Si tu ne peux pas citer 1 ligne de code réel observée, étape 1 incomplète.

### Étape 2 — Identifier les rôles dev récurrents (pipeline standard)

**Pipeline canonique recommandé** (cf section dédiée plus haut) :
- **architect** (Opus, blue) — toujours sauf tâches S
- **dev** (Sonnet, green) — toujours
- **code-reviewer** (Sonnet, orange) — toujours sauf S
- **test-writer** (Sonnet, yellow) — si framework test présent

**Rôles complémentaires selon contexte** :

| Rôle | Présent quand |
|------|---------------|
| **refactor** | Codebase legacy ou patterns à harmoniser |
| **debugger** | Tests qui échouent, prod issues à reproduire |
| **sécu-auditor** | Repo avec credentials, IDOR, scope critique |
| **db-migrator** | DB avec migrations |
| **api-designer** | API publique ou interne |
| **doc-writer** | OBSOLÈTE — pas d'agent doc (cf [[feedback_no_doc_agent]]) |

**Sortie** : liste 4-8 rôles dev pertinents au repo (pipeline standard + complémentaires si justifié).

### Étape 3 — Mapper rôles → agents

**Pour chaque rôle identifié**, créer un agent avec :
- **`name`** : kebab-case (`architect`, `dev-feature`, `code-reviewer`)
- **`model`** (doctrine forge cohérente avec Cat Wu + Brad Abrams) :
  - Sonnet pour exécution (dev, test-writer, code-reviewer)
  - Opus pour jugement (architect, devils-advocate)
  - Haiku pour checks rapides
- **`effort`** :
  - `high` partout
  - `xhigh` UNIQUEMENT pour architect / dev-lead / refactor-pg
  - `max` toujours disponible (vérifié docs 23 mai 2026), à utiliser avec prudence
- **`color`** : convention 8 couleurs cross-repo forge
- **`memory: project`** OBLIGATOIRE forge
- **`permissionMode`** OBLIGATOIRE forge
- **`disallowedTools: Write, Edit`** sur read-only (code-reviewer, project-auditor)
- **`skills`** : injecter les skills pertinentes (et les référencer dans body)

**Sortie** : liste 4-8 agents proposés avec justification ("parce que ton repo a X feature critique → architect blue Opus xhigh").

### Étape 4 — Identifier les boundaries critiques → Hooks

**Repérer les invariants 100%** :

| Boundary | Hook type |
|----------|-----------|
| **Lint / format** | PostToolUse Write/Edit/MultiEdit (prettier, black, eslint) |
| **Credentials secrets** | PreToolUse (grep secrets dans Write) |
| **Scope cross-repo** | PreToolUse Bash (empêcher `cd ../autre-repo`) |
| **DB migrations immutables** | PreToolUse (empêcher Edit sur migrations passées) |
| **Frontmatter YAML valide** | PostToolUse (vérifier YAML) |
| **Secrets en clair `.mcp.json`** | PostToolUse (grep + block) |

**Anti-pattern doctrine 22 mai forge** :
- ❌ JAMAIS hooks workflow (architect-first, TDD strict, commit gates)
- ❌ JAMAIS pipeline markers + guards
- ❌ JAMAIS TTL sur markers
- ✅ Lint / security / scope UNIQUEMENT

**Sortie** : liste 2-5 hooks proposés (lint/security/scope uniquement).

### Étape 5 — Identifier les patterns récurrents → Skills

**Pour chaque pattern qui apparaît > 2 fois dans le repo** :
- Pattern de test → skill `test-X-pattern`
- Pattern de scaffolding composant → skill `scaffold-component`
- Pattern de runbook ops → skill `runbook-X`

**Filtrer par 9 catégories Thariq** (post Anthropic mars 2026 "Lessons from Building Claude Code") :
1. Library & API Reference
2. Product Verification
3. Data Fetching & Analysis
4. Business Process & Team Automation
5. Code Scaffolding & Templates
6. Code Quality & Review
7. CI/CD & Deployment
8. Runbooks
9. Infrastructure Operations

Si le pattern entre dans 1 des 9 → skill légitime. Sinon, CLAUDE.md ou rule suffit.

**Important — description < 250 chars** pour auto-trigger fiable (limite system reminder `/skills`).

**Sortie** : liste 3-10 skills proposées, justifiées par pattern observé.

### Étape 6 — Définir CLAUDE.md

**Squelette 5 sections** (référence [anthropics/claude-for-legal/CLAUDE.md](https://github.com/anthropics/claude-for-legal) 174 lignes vérifié 23 mai 2026) :

```markdown
# <Nom projet>

**Une phrase qui dit ce que fait le projet.**

## Stack
- <Stack identifiée étape 1>

## Commandes fréquentes
- Build / Test / Lint / Run dev

## Gotchas (compounding)
- <Pièges observés en session, ajoutés au fil>

## Conventions
- <Naming, structure>

## Things to leave alone
- <Migrations, vendored code, générés>
```

**Cible < 200 lignes** (verbatim Anthropic).

**Sortie** : CLAUDE.md skeleton + premières gotchas observées au scan.

---

## QUAND — Critère d'application

### Méthode complète quand :
- Nouveau repo à équiper
- Audit complet repo existant
- Refonte majeure setup `.claude/`

### Méthode légère (étape 1 + 6) quand :
- Repo très simple ou very small
- POC / spike
- One-shot exploration

---

## WORKFLOW — Pipeline analyse complète

```
1. Scan archi (étape 1)
        ↓
2. Identifier rôles (étape 2 — pipeline standard architect/dev/reviewer/test + complémentaires)
        ↓
3. Mapper agents (étape 3) ── parallèle ── 4. Identifier boundaries → hooks (étape 4)
        ↓                                          ↓
5. Identifier patterns → skills (étape 5)
        ↓
6. CLAUDE.md squelette (étape 6)
        ↓
[Output complet : skills + agents + hooks + CLAUDE.md + workflow recommandé]
        ↓
Validation utilisateur (qu'est-ce qu'il veut garder/modifier)
        ↓
Déploiement (via skill-creator, agent-creator, hook-creator, claudemd-optimizer)
```

---

## APPELS — Composants mobilisés
## QUARTET D'AGENTS FORGE — Pattern d'invocation validé 25 mai 2026

Pour appliquer cette méthode sur un repo, dispatcher en PARALLÈLE le quartet forge :

| Agent | Scope |
|-------|-------|
| `project-analyzer` | Vue projet haut niveau + recommandations |
| `project-auditor` × N (1 par cluster `.claude/`) | Audit `.claude/` agents/skills/hooks/rules+CLAUDE.md |
| `codebase-scanner` | Étapes 1b/1c/1d/5 (code applicatif réel) |
| `devils-advocate` | Critique livrables majeurs (conditionnel) |

Soit typiquement **5 sub-agents en parallèle** (4 project-auditor par cluster + 1 codebase-scanner). Cf [[quartet-analyse-multi-repo]] + [[audit-puis-vagues-paralleles]] pour le détail orchestration + vagues d'application.


- [[comment-creer-skill]] — pour chaque skill proposée étape 5
- [[comment-creer-agent]] — pour chaque agent proposé étape 3
- [[comment-creer-hook]] — pour chaque hook proposé étape 4
- [[comment-ecrire-claudemd]] — pour CLAUDE.md étape 6
- [[workflow-claude-code-optimal]] — workflow recommandé selon taille repo
- [[mcp-vs-skills-doctrine]] — décider quand MCP custom nécessaire

---

## OPTIMISATION — Output recommandé
## KIT DE BASE — composants systématiques vs selon-repo (24 juin 2026)

### Socle minimum rules — projet-analyzer recommande TOUJOURS ces 3 rules

Quel que soit le repo cible, `project-analyzer` propose systématiquement ces 3 rules comme socle minimum (même niveau que les composants systématiques ci-dessous) :
1. `check-before-create.md` — **adapté aux agents DU PROJET** (pas les agents forge qui n'existent pas localement)
2. `quality-gates.md` — workflows concrets avec les agents du projet
3. `learn-from-mistakes.md` — sans globs restrictifs

**Règle delegate-guard = forge ONLY** : le hook `delegate-guard` n'a de sens que dans forge (seul repo avec les agents créateurs spécialisés). Le déployer dans un repo d'équipe bloque les édits sans alternative disponible. Dans tout repo non-forge, le workflow check-before-create s'appuie sur les agents LOCAUX : `architect` (fast pass cohérence) + `code-reviewer` (conformité standards). Cf [[config-repo-equipe-vs-forge]].

> Issu du chantier migration_script (24 juin 2026) — repo d'équipe PostgreSQL/PLpgSQL. Distingue ce qu'on déploie TOUJOURS de ce qui dépend du repo.

Tout setup `.claude/` complet (étape 5-6 de la grille) comprend un **kit de base systématique** puis des composants **calibrés au repo**.

### Systématique (tout repo équipé, quel que soit le type)
- **`memory/`** (pattern neo_ia) : `MEMORY.md` index + fichiers `reference_*`/`feedback_*`/`project_*`. Compounding versionné, contenu portable (zéro wikilink/MCP si repo d'équipe — cf [[config-repo-equipe-vs-forge]]).
- **`learning-reminder`** (hook Stop, **non-bloquant** exit 0) : rappelle de capitaliser dans `memory/`. Sur repo d'équipe, JAMAIS la version bloquante de forge (cf [[decision-garder-learning-reminder-hook]]). C'est ce qui rend la mémoire vivante sans discipline manuelle.
- **`.skill-triggers.json` + hook `skill-activation`** (UserPromptSubmit) : garantit l'auto-suggestion des skills (sinon ~50%). Gotcha vérifié : un trigger finissant par `_` (`vp_`, `chk_`) est MORT (`\b` après `_` ne matche jamais une lettre suivante) → triggers en prose uniquement. Ajouter `memory-watcher` qui reset `.skill-recommendations-session` au SessionStart (sinon chaque skill se tait après 1 fois — bug latent de neo_ia).
- **`README.md` + `workflow.md`** (doc onboarding) : inventaire + parcours « je dois faire X ». Critique pour une équipe de débutants.
- **`astuces.md`** : bonnes pratiques Claude Code builtin (Shift+Tab normal/auto/plan, `/model`, `/advisor` si l'équipe l'a, `/clear`, vérifier, capitaliser).

### Selon le repo (calibrer, ne pas copier)
- **Pipeline d'agents** : dérivé des rôles RÉELS. Un repo SQL sans test runner → PAS d'agent test-writer ni de pipeline architect→dev→test app. Sa couche « give Claude a way to verify » est SQL-native (vues `chk_`, contrôles, reviewer).
- **TDD / mutation testing / `/go` typecheck-lint** : INAPPLICABLE sans substrat (test runner, CI). Ne PAS docker la note d'un repo SQL pour leur absence — erreur de catégorie.
- **Hooks** : lint/format adaptés à la STACK (encoding SQL ≠ ruff ≠ eslint). Sur repo d'équipe, tous non-bloquants.
- **Skills** : workflows récurrents détectés dans la doc du repo, pas un set générique.

### Anti-pattern (cas migration_script)
Transplanter le workflow dev **app** (vault [[workflow-claude-code-optimal]] calibré neo_ia/ia_back) sur un repo SQL = même erreur de catégorie que transplanter la machinerie forge. Filtrer chaque brique : « assume-t-elle un test runner / typecheck / CI app ? » → si oui, inapplicable.

### Niveau basique
- 2-3 agents (architect, dev, reviewer)
- 1 hook (lint)
- CLAUDE.md 50-100 lignes
- Workflow S/M

### Niveau avancé
- 4-6 agents par rôle (Sonnet/Opus split — doctrine forge)
- 2-3 hooks (lint + security)
- 5-10 skills
- CLAUDE.md ~150 lignes
- Workflow L

### Niveau expert (Trail of Bits style)
- 6-10 agents avec couleur + skills injectées
- 3-5 hooks (lint + security + scope + anti-rationalization Stop)
- 10-20 skills par catégorie Thariq
- MCP custom si métier
- CLAUDE.md ~180 lignes
- Workflow XL avec Advisor Strategy (Brad Abrams pattern), multi-clauding, /loop

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| Méthode reproductible | Time-to-config divisé par ~3 (vs ad-hoc) |
| Sonnet/Opus split (doctrine forge) | Coût réduit sur agents exécution, qualité préservée sur jugement |
| Boundaries → hooks (pas rules) | 100% compliance vs compliance partielle advisory |
| Patterns → skills (9 catégories Thariq) | Réutilisation cross-sessions |
| CLAUDE.md < 200L | Moins de tokens contexte (verbatim Anthropic : "consume more context and reduce adherence") |
| Sortie justifiée | Utilisateur peut challenger et itérer rationnellement |

---

## ANTI-PATTERNS

### Méthode
- ❌ **Copier config d'un autre repo sans analyse** — chaque repo a son contexte
- ❌ **Sauter étape 1** — proposer agents sans scan archi
- ❌ **Pas de justification** — "voici la config" sans "parce que ton repo a X"
- ❌ **Trop d'agents** (> 10) — surcharge cognitive, conflits
- ❌ **Trop de skills** (> 30) — budget contexte explosé

### Doctrine
- ❌ **Hooks workflow** — anti-pattern 22 mai 2026
- ❌ **Agent CTO orchestrateur** — session principale orchestre (cf [[feedback_no_cto_agent]])
- ❌ **Agent doc** — pas d'agent doc (cf [[feedback_no_doc_agent]])
- ❌ **Pipeline markers + guards** — anti-pattern
- ❌ **Pipeline architect→dev→reviewer→test FORCÉ via hook** — doctrine "Claude decides when to invoke"

### Output
- ❌ **CLAUDE.md > 200L** — kitchen sink (verbatim Anthropic anti-pattern)
- ❌ **Pas de section Gotchas** dans CLAUDE.md — pas de compounding
- ❌ **PR-workflow imposé** comme standard — optionnel customisable par repo
- ❌ **Skills sans description trigger 3e personne** — pas d'activation
- ❌ **Skills description > 250 chars** — tronquée system reminder

### Process
- ❌ **Pas advisor+DA AVANT proposer** (cf [[feedback_advisor_da_mandatory]])
- ❌ **Questionnaire avant analyse** — analyser d'abord (cf [[feedback_analyse_first_not_questionnaire]])
- ❌ **Pas de vérification empirique** des claims sub-agents (cf [[feedback_audit_claims_after_brief]])

---

## EXEMPLES CONCRETS — Repos de référence

### Anthropic minimaliste
- **[anthropics/claude-code](https://github.com/anthropics/claude-code)** — config 3 slash commands. Démonstration "minimum qui marche". Pour repo très simple.

### Anthropic structuré
- **[anthropics/claude-for-legal/CLAUDE.md](https://github.com/anthropics/claude-for-legal)** — **174 lignes**, 5 sections (vérifié 23 mai 2026). Référence canonique CLAUDE.md.

### Entreprise sécu complète
- **[trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)** — stack complet :
  - Anti-rationalization Stop hook (inédit)
  - 3-tier sandbox (`/sandbox` + devcontainer + dropkit DO)
  - Hooks sécu uniquement
  - Référence pour repos sensibles

### Viral minimaliste
- **[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** — CLAUDE.md **67 lignes**, 4 principes (URL active, ex-forrestchang). Fan project pas endorsé par Karpathy. Démonstration "court + opinionated > long + neutre".

### Pattern vault Karpathy
- **[Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** — 3-layers raw/wiki/schema, Ingest/Query/Lint, qmd (Tobi Lütke, attribution via handle `tobi`+npm). Référence pour repos avec memory compounding profond.

### Tech écosystème
- **Stripe, Vercel, Cloudflare, Sentry, OpenAI, HashiCorp, Figma, Netlify** — skills publics
- **Simon Willison** `simonw/llm` — référence skill atomique

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) — CLAUDE.md target 200L
- [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — spec 29 events, timeouts par type
- [code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents) — effort levels (max inclus)
- [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 2-agent Justin Young (initializer + coding, harness identique)
- features-overview — "If a rule must hold every time, make it a hook"
- [code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview) — "Claude decides when to call a tool", "Skills are model-invoked"

### Code with Claude SF + London
- Boris : Routines (higher-order prompts)
- Cat Wu / Lisa Crofoot / Noah Zweben / Daisy Hollman / Jeremy Hadfield / Fiona Fung / Ami Vora (London 19 mai 2026)
- Erik Schluntz : Vibe Coding stratégies (SF mai 2026)
- Thariq : 9 catégories (post Anthropic mars 2026), lethal trifecta (référé, créé par Willison), compute allocator
- Brad Abrams + Mario Rodriguez (CwC SF) : Advisor Strategy avec GitHub

### Référence Boris doctrine
- Pragmatic Engineer — compounding error-driven
- Sequoia AI Ascent — "coding is solved"
- Latent Space — "All the secret sauce — it's all in the model"

### Référence harness
- Hashimoto [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) — popularisation "harness engineering" (5 fév 2026)
- Böckeler [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) — Guides+Sensors 2 avril 2026
- Vivek Trivedy [langchain.com/blog/improving-deep-agents-with-harness-engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — 17 fév 2026 (GPT-5.2-Codex)
- Bustamante [nicolasbustamante.com/blog/model-harness-fit](https://nicolasbustamante.com/blog/model-harness-fit) — ForgeCode 79.8%

### Trail of Bits
- [github.com/trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)

---

## GOTCHAS — Pièges observés

### Pièges analyse
- **Sauter étape 1** = config ad-hoc, pas adaptée
- **Pas de scan `.claude/` existant** = double composants
- **Pas de `git log`** = manque le contexte récent
- **Trop d'hypothèses sans vérification empirique** (cf [[feedback_audit_claims_after_brief]])

### Pièges proposition
- **Trop ambitieux** : 20 agents pour repo qui en mérite 4
- **Trop conservateur** : 0 hook sur repo sécu critique
- **Copier config d'un autre repo** sans contexte
- **Pas justifier** : "voici la config" sans "parce que"

### Pièges déploiement
- **Édit direct** au lieu de déléguer aux agents spécialisés (skill-creator, agent-creator, etc.)
- **Pas de DA** avant livraison majeure
- **Pas de test comportemental** post-setup (cf [[feedback_behavioral_test_pattern]])

### Pièges cross-repo
- **Décisions naming faites sur un repo** doivent être propagées (cf [[feedback_propagate_decisions_cross_repo]])
- **Drift de stack** (ex Drizzle → postgres.js) à détecter par grep stack OLD vs NEW (cf [[feedback_drizzle_postgresjs_drift]])

### Pièges Jarvis (forge)
- **Pas mode exécutant pur** (cf [[feedback_never_pure_executor]])
- **JAMAIS un seul agent pour multi-repo** — 1 agent par repo en parallèle (cf [[feedback_audit_repo_method]])
- **`Explore` ≠ `project-auditor`** — Explore = recherche rapide, audit = project-auditor
- **Remettre en cause TOUT y compris ce qui vient d'être écrit** si incohérence détectée (posture Jarvis active)

---

## ALIASES — Findability

Aliases déclarés en frontmatter (14) :
- methode analyser repo
- analyse repo claude code
- config claude code optimale
- grille analyse repo
- audit setup repo
- proposer config claude code
- 6 etapes analyse repo
- kit rules standard
- scan architecture
- mapper roles agents
- comment automatiser un repo claude code
- automate repo setup
- automatiser projet claude code
- pipeline architect dev test

---

## WIKILINKS

### Notes canoniques sœurs (sources de vérité)
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[mcp-vs-skills-doctrine]]
- [[pattern-vault-llm-karpathy]]
- [[methode-pivoter-doctrine]]

### Fiches leaders (à créer)
- [[Boris Cherny]]
- [[Cat Wu]]
- [[Thariq Shihipar]]
- [[Erik Schluntz]]
- [[Brad Abrams]]
- [[Birgitta Böckeler]]
- [[Mitchell Hashimoto]]

### Knowledge / refs liées
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[synthese-audit-coherence-neo-ia-ia-back]]
- [[feedback_audit_repo_method]]
- [[feedback_no_cto_agent]]
- [[feedback_no_doc_agent]]
- [[feedback_analyse_first_not_questionnaire]]
- [[feedback_advisor_da_mandatory]]
- [[feedback_audit_claims_after_brief]]
- [[feedback_behavioral_test_pattern]]
- [[feedback_propagate_decisions_cross_repo]]
- [[feedback_drizzle_postgresjs_drift]]
- [[feedback_never_pure_executor]]

### Forge custom
- [[project-auditor]] — agent forge dédié audit
- [[project-analyzer]] — agent forge analyse projet
- [[devils-advocate-pipeline]]
- [[forge-brain-proactive]]

---

**Fin note canonique `methode-analyser-repo.md`** — révisée 23 mai 2026 post-audit thématique vault (ajout pipeline standard architect/dev/reviewer/test conditionnel).
