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
derniere-maj: 2026-05-10
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
