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
