---
titre: "Pattern Agentic Engineering — Checklist projet Neoteem"
resume: "Checklist pour deployer une architecture agentic engineering sur tout nouveau projet Neoteem. Base sur Karpathy + Boris + experience neo_ia/ia_back."
aliases:
  - "agentic engineering checklist"
  - "pattern agentic"
  - "nouveau projet claude code"
  - "setup agentic"
  - "checklist agentic engineering neoteem"
  - "deploiement agentic"
domaine: claude-code
type: technique
derniere-maj: 2026-05-21
auteur: claude
sources:
  - "[[agentic-engineering-karpathy]]"
  - "[[vibe-coding-setup-complet]]"
  - "[[Boris Cherny]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/neoteem"
---
# Pattern Agentic Engineering

Checklist pour deployer l'architecture agentic engineering sur tout projet Neoteem. Chaque item est valide par l'experience production (neo_ia, ia_back) et le framework Karpathy.

## Principe fondateur

> L'humain orchestre, les agents executent, la verification est systematique.

Pas de vibe coding. Pas d'agent CTO. L'humain garde le jugement system design, le taste, et le controle des permissions.

## Phase 1 — Fondations (jour 1)

### CLAUDE.md
- [ ] ~100 lignes max
- [ ] Section Gotchas obligatoire
- [ ] Chaque ligne passe le test : "si je l'enleve, Claude fait des erreurs ?"
- [ ] Pas de routing (routing = rules/)
- [ ] Pas de documentation du code (le code se documente)

### Rules (dans .claude/rules/)
- [ ] `architect-first.md` — plan avant toute implem, meme taille S
- [ ] `quality-gates.md` — pipeline architect → dev → test-writer → code-reviewer
- [ ] `agent-delegation.md` — session principale orchestre, agents executent
- [ ] `memory-compounding.md` — erreurs dans Auto Memory, relire avant agir
- [ ] `shared-learnings.md` — apprentissages importants → skills commitees
- [ ] `changelog.md` — changelog mis a jour a chaque implem

### Settings
- [ ] 100% opus (zero sonnet)
- [ ] Effort levels : high (analystes/securite), medium (devs/gates), xhigh (session)
- [ ] Permissions : `acceptEdits` sur agents write, `plan` sur agents read-only
- [ ] `disallowedTools: Write, Edit` sur agents read-only (double protection)
- [ ] `memory: project` sur TOUS les agents

## Phase 2 — Agents (jour 1-2)

### Agents obligatoires (minimum viable)

| Agent | Role | Effort | Permission |
|-------|------|--------|------------|
| architect | Plan, design, decomposition | high | plan |
| dev-* (1 par domaine) | Implementation | medium | acceptEdits |
| test-writer | Tests apres chaque implem | medium | acceptEdits |
| code-reviewer | Review avant merge | medium | plan |

### Agents recommandes (selon le projet)

| Agent | Quand l'ajouter |
|-------|-----------------|
| security-auditor | Endpoints publics, auth, donnees sensibles |
| debugger | Codebase > 50 fichiers |
| codebase-analyst | Projets existants a reprendre |
| perf-reviewer | APIs a forte charge |

### Regles agents
- Un agent = une responsabilite
- Pas d'agent orchestrateur (session principale orchestre)
- Skills pertinentes injectees dans frontmatter
- Description = trigger ("Use PROACTIVELY when...")

## Phase 3 — Skills (jour 2-3)

### Skills obligatoires

| Skill | Usage |
|-------|-------|
| `/recap` | Debut de session — git status + log + tests + lint |
| `/go` | Fin d'implem — test → review → changelog → commit+push |

### Skills recommandees

| Skill | Quand |
|-------|-------|
| `/evolve` | Planification — propositions produit/archi |
| `/audit-health` | Health check periodique |
| `/refactor-scan` | Code quality |

### Regles skills
- SKILL.md < 500 lignes, detail dans references/
- Section Gotchas = highest-signal content
- Section Apprentissage sur skills metier
- Progressive disclosure (1 niveau max)

## Phase 4 — Verification (jour 3+)

### Gates qualite (obligatoire)
```
architect → dev-* → test-writer → code-reviewer
```
Enforce par rules. Pas de merge sans passage par les gates.

### Memory compounding (obligatoire)
- Auto Memory active
- Erreurs documentees (relire avant meme type de tache)
- shared-learnings rule (apprentissages → skills commitees)

### Evals (recommande — gap actuel)
- [ ] Eval set par agent : inputs connus → outputs attendus → scoring
- [ ] Metriques : taux correction post-review, temps cycle, regressions
- [ ] Dashboard Langfuse : suivi qualitatif/semaine
- [ ] Feedback loop : evals qui echouent → enrichissent prompt agent

## Phase 5 — Knowledge Base (optionnel mais puissant)

### Quand creer un Brain vault
- Projet avec domaine metier complexe (regles business, schemas BDD)
- Equipe > 2 devs utilisant Claude Code
- Codebase > 100 fichiers

### Structure brain
- Notes atomiques (1 concept = 1 note)
- MOCs par domaine
- Aliases = semantic search
- MCP server pour acces agent-native

## Anti-patterns (tous observes en production)

| Anti-pattern | Consequence | Solution |
|--------------|-------------|----------|
| Agent CTO orchestrateur | Perte de controle, decisions non-revues | Session principale orchestre |
| Sonnet au lieu d'opus | Qualite inferieure pour cout comparable | 100% opus, effort adapte |
| Pas de test-writer | Regressions silencieuses | Gate obligatoire |
| CLAUDE.md > 200 lignes | Compliance ~60% | Pruner a ~100L, deporter dans rules/ |
| Routing dans CLAUDE.md | Melange de concerns | Routing dans .claude/rules/ |
| Edit direct skills/agents | Non-conforme, pas de validation | Deleguer aux agents specialises |
| "Je sais deja" | Erreurs repetees | Relire memory + erreurs AVANT |
| Pas d'evals | Pas de mesure = pas d'amelioration | Evals set + dashboard |

## Checklist de validation

Apres deploiement, verifier :

- [ ] `claude` dans le repo → CLAUDE.md se charge, rules se chargent
- [ ] Pipeline gates fonctionne (architect → dev → test → review)
- [ ] Agents dispatchent correctement (pas de session principale qui code)
- [ ] Memory compounding actif (erreurs documentees, relues)
- [ ] Repo autonome (pas de dependance externe vers forge)
- [ ] Un collegue peut ouvrir le repo et travailler avec Claude Code sans aide

## Karpathy : le test ultime

> "Build it. Secure it. Then I'll send 10 agents to try to break it."

Le test final : est-ce que le systeme resiste a un audit agressif ? Si oui, l'architecture tient.

## Liens

- [[MOC-Techniques]]
- [[vibe-coding-setup-complet]] — pattern setup detaille (skills, journalier, RECAP)
- [[agentic-engineering-karpathy]] — framework source
- [[config-guardian-pattern]] — audit multi-repo


---

## Mise à jour mai 2026 — Apprentissages neo_ia + ia_back

### Corrections par rapport à la version initiale

- **Modèles** : PAS 100% opus. Politique CwC 2026 = Opus xhigh pour jugement (architect, code-reviewer, security), Sonnet high pour exécution (dev-*). Exception : dev-neochat = Opus (LangGraph complexe).
- **Pipeline** : TDD test-first = `architect (contrats testables) → test-writer RED → dev → test-writer REFACTOR → code-reviewer`. PAS l'ancien architect → dev → test-writer.
- **Sprint Contract** : test-writer valide les contrats architect AVANT d'écrire les tests (handshake bidirectionnel).
- **Rules manquantes** : `learn-from-mistakes.md` + `agents-color-convention.md` + `outcomes-after-architect.md` obligatoires (tous oubliés au déploiement initial ia_back).
- **Frontmatter rules** : TOUTE rule DOIT avoir `---\ndescription: ...\n---` sinon elle est morte silencieusement.

### Arbre de décision — Questions à poser avant setup

Quand Raphael dit "analyse/setup ce repo", poser ces questions via AskUserQuestion :

| Question | Impact sur le setup |
|----------|-------------------|
| Stack ? (Python/TS/Go/Rust) | Hooks dans le même langage, permissions Bash, test runner |
| Mono-app ou multi-app ? | 1 agent dev vs dev-* par app |
| TDD strict ou bypass S ? | Contrats testables dans architect, test-writer phases RED/REFACTOR |
| Base de données ? laquelle ? | db-inspector, schema-context, guard-pg-readonly |
| Domaine métier complexe ? | Brain vault, neo-brain skill, MCP obsidian |
| Multi-dev ou solo ? | shared-learnings rule, settings.local.json gitignore |
| Workflow (PR / commit direct) ? | /go avec ou sans PR, commit-guard |
| Endpoints publics ? | security-auditor, security-reviewer |
| CI/CD existant ? | deploy-check skill, /autofix-pr |

### Audit post-setup — 8 checks (confirmé empiriquement)

1. **Agents → Skills** : chaque skill `skills:` a des instructions dans le body
2. **Agents → Tools** : cohérent avec le rôle (read-only = pas Write/Edit)
3. **Skills → References** : < 500L, references/ utilisées
4. **Rules → Frontmatter** : chaque rule a `description:` (sinon morte)
5. **Hooks → Settings** : chaque hook existe physiquement
6. **Delegation → Agents** : agents mentionnés dans les rules existent
7. **Memory** : `memory: project` sur tous les agents
8. **Credentials** : `.mcp.json` + `settings.local.json` dans `.gitignore`

Source : [[synthese-audit-coherence-neo-ia-ia-back]]

### Pattern skills orphelines (problème #1 trouvé)

11/16 agents ia_back et 6/12 agents neo_ia avaient des skills dans `skills:` frontmatter mais aucune instruction dans le body. La skill est chargée (consomme des tokens) mais l'agent ne sait pas quand l'utiliser. Fix : 1 ligne d'instruction par skill.

### Liens ajoutés

- [[synthese-audit-coherence-neo-ia-ia-back]] — audit 67 problèmes, 4 patterns
- [[critique-2026-05-21-tdd-optimizations-handshake]] — DA Sprint Contract


## Workflow analyse/setup repo (confirmé mai 2026)

### Étape 1 — Analyse automatique (PAS de questions)

Analyser le repo comme `claude-code-setup:claude-automation-recommender` :
- Détecter stack (package.json, pyproject.toml, Cargo.toml, go.mod)
- Détecter framework (imports, dépendances)
- Détecter DB (Drizzle, Prisma, SQLAlchemy, raw SQL)
- Détecter tests existants (jest, pytest, bun:test, go test)
- Détecter .claude/ existant (agents, skills, hooks, rules, settings)
- Détecter mono-app vs multi-app (src/ vs apps/*/)

### Étape 2 — Proposer (1-2 par catégorie, pas submerger)

Mapper les signaux codebase aux composants via le Decision Framework :

| Signal | Composant |
|--------|-----------|
| Code source modifiable | dispatch-guard (main session ne code pas) |
| Tests existants ou testable | tdd-guard + test-writer + architect contrats testables |
| Plusieurs apps/modules | dev-* par app, architect obligatoire |
| DB | db-inspector, guard-readonly si DB externe |
| Framework avec linter | PostToolUse auto-format (ruff, prettier, eslint) |
| .env ou secrets | PreToolUse guard .env |
| Endpoints publics | security-auditor agent |
| Domaine métier complexe | Brain vault + MCP obsidian |

### Étape 3 — Questions SEULEMENT pour ce qui ne se déduit pas

- TDD strict ou bypass taille S ?
- Commit direct ou PRs ?
- Solo ou multi-dev ?

### Étape 4 — Déployer via agents spécialisés

agent-creator, skill-creator, hook-creator, claudemd-optimizer. JAMAIS éditer directement.

### Étape 5 — Audit 8 checks post-setup

Voir section "Audit post-setup" ci-dessus.

### Étape 6 — DA avant livraison

Devil's advocate sur le setup complet avant d'annoncer "terminé".

### Composants indispensables (confirmés par neo_ia + ia_back)

| Composant | Type | Pourquoi indispensable |
|-----------|------|----------------------|
| dispatch-guard | hook | Force délégation aux agents (advisory = 80%, hook = 100%) |
| architect-guard | hook | Force plan avant code |
| tdd-guard | hook | Force tests avant code (si TDD) |
| commit-guard | hook | Force code-reviewer avant commit |
| guard-test-scope | hook | Empêche test suite complète |
| session-reset-markers | hook | Reset markers à chaque session |
| learn-from-mistakes | rule | Boris compounding |
| shared-learnings | rule | Apprentissages commités, pas juste mémoire |
| quality-gates | rule | Pipeline documenté |
| agent-delegation | rule | Routing clair |
| agents-color-convention | rule | Cohérence visuelle cross-repo |
| /go | skill | test → review → changelog → commit |
| /recap | skill | Contexte au retour |
| /spec | skill | Spec avant implem (taille M/L) |

Source : [[synthese-audit-coherence-neo-ia-ia-back]], plugin `claude-code-setup:claude-automation-recommender`

## Cas d'usage — Au-delà du setup repo

### Quand Raphael dit "analyse ce skill" / "améliore ce skill"

1. Lire le SKILL.md complet + references/
2. Consulter vault : `04-Techniques/`, `Knowledge/erreurs/`, critiques similaires
3. Charger `cc-skills-ref` (référence canonique structure skills)
4. Vérifier : < 500L, gotchas présents, section Apprentissage, progressive disclosure
5. Proposer : diviser si trop long, ajouter gotchas manquants, extraire en references/
6. Exécuter via `skill-creator` (JAMAIS éditer directement)
7. Si modification majeure → DA avant livraison

### Quand Raphael dit "analyse ce CLAUDE.md" / "améliore-le"

1. Lire le CLAUDE.md complet
2. Consulter vault : `best-practices-claude-code-leaders` (Boris ~100L, test "si je l'enlève, ça casse ?")
3. Charger `cc-prompt-ref` (best practices prompts)
4. Vérifier : < 150L, gotchas présents, pas de routing (routing = rules/), pas de doc code
5. Proposer les coupes + ajouts
6. Exécuter via `claudemd-optimizer` (JAMAIS éditer directement)

### Quand Raphael dit "analyse ces agents" / "audite le setup"

1. Lancer `project-auditor` avec les 8 checks (voir Audit post-setup)
2. Consulter vault : `synthese-audit-coherence-neo-ia-ia-back` pour les patterns connus
3. Vérifier cross-références : skills→body, rules→frontmatter, hooks→settings
4. Proposer corrections par batch (sécurité → critiques → warnings → cosmétique)
5. Exécuter via `agent-creator` pour les agents, `skill-creator` pour les skills
6. Revalider avec un 2ème audit après corrections

### Quand Raphael dit "crée un agent/skill/hook"

1. Consulter vault : `Knowledge/erreurs/` pour erreurs passées similaires
2. Charger la skill forge référence (`cc-agents-ref`, `cc-skills-ref`, `cc-hooks-ref`)
3. Vérifier si un composant similaire existe déjà
4. Proposer AVANT de créer (jamais créer sans validation Raphael)
5. Exécuter via l'agent spécialisé
6. DA si composant majeur (agent, skill métier, hook bloquant)
7. Audit cohérence post-création (le nouveau composant est-il bien référencé partout ?)

### Règle transversale

**Toujours consulter le vault EN PREMIER** — avant de répondre, avant de proposer, avant de créer. Le vault contient les erreurs passées, les patterns validés, et les critiques DA précédentes. Ne jamais travailler "de mémoire" quand le vault a l'info.

**Toujours utiliser les agents spécialisés** — delegate-guard bloque de toute façon, mais le réflexe doit être naturel, pas forcé par un hook.


## Phase 7 — Test comportemental post-modification (mai 2026)

Après setup, audit ou modification massive → produire une **suite de tests comportementaux PASS/FAIL** que Raphael lance en session fraîche.

Détail complet : [[pattern-behavioral-dispatch-test]]

### Checklist rapide

- [ ] Chaque agent apparaît dans au moins 1 scénario
- [ ] Chaque hook bloquant (exit 2) a un test négatif
- [ ] Chaque skill user-invokable est testée
- [ ] Le pipeline TDD complet est testé bout en bout
- [ ] Les prompts utilisent le vocabulaire métier du projet
- [ ] Score quantitatif (/N) pour suivi d'évolution

### Position dans le workflow

```
setup/audit → corrections → devil's advocate → TEST COMPORTEMENTAL → livraison
```
