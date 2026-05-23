---
titre: "Pattern Spec-Driven Development — Interview → Spec → Execute"
resume: "Consensus 2026 des pionniers Claude Code : interview AskUserQuestion → SPEC.md persistant → nouvelle session pour exécuter. Thariq, Boris, Anthropic docs, feature-dev plugin"
aliases:
  - spec-driven development
  - SDD
  - spec driven
  - interview pattern
  - SPEC.md workflow
  - spec before code
  - planning first development
domaine: claude-code
type: technique
derniere-maj: 2026-05-23
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
auteur: claude
---
## Principe

**Planifier AVANT de coder, séparer planning et implémentation.** Consensus universel des pionniers 2026.

Si Claude fait le bon choix 80% du temps et une feature implique 20 décisions : 0.8^20 ≈ 1% de chances de tout réussir sans plan. Le planning collapse les ambiguïtés en choix validés.

## Workflow Thariq Shihipar (Eng Manager Claude Code)

Le pattern officiel recommandé par Anthropic :

1. Prompt minimal (même vague suffit)
2. "Interview me using the AskUserQuestion tool" → 30-40 questions, ~30 min
3. Claude écrit la spec résultante
4. **Nouvelle session** pour exécuter (contexte propre)

> "my favorite way to use Claude Code to build large features is spec based -- start with a minimal spec or prompt and ask Claude to interview you using the AskUserQuestionTool then make a new session to execute the spec"

**Insight clé :** plus le workflow IA est long, PLUS le travail humain amont est important (pas moins).

## Workflow Boris Cherny (Créateur Claude Code)

Pas de SPEC.md formel. Plan Mode + CLAUDE.md compounding :

1. Plan Mode (Shift+Tab x2) sur quasi toute session complexe
2. Itérer jusqu'à plan solide
3. Auto-accept mode → one-shot
4. Tip #1 : "Give Claude a way to verify its work" = 2-3x qualité

Variante teammate : 2ème session Claude review le plan comme staff engineer.

## Prompt officiel Anthropic (code.claude.com)

> "I want to build [brief description]. Interview me in detail using the AskUserQuestion tool. Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered. Keep interviewing until we've covered everything, then write a complete spec to SPEC.md."

## Frameworks communautaires

| Framework | Stars | Approche |
|-----------|-------|----------|
| **GitHub Spec Kit** | ~105K (2026-05-23) | Constitution → Specify → Plan → Tasks → Implement (6 core + 3 optionnelles) |
| **GSD** | ~59K | Discuss → Plan → Execute → Verify → Ship, contexte frais par agent |
| **BMAD** | ~46K (v6.6.0 avril 2026) | 21 agents spécialisés, document sharding en story files |

## Plugin feature-dev (Anthropic officiel, Sid Bidasaria)

7 phases : Discovery → Codebase Exploration (2-3 agents //) → Clarifying Questions → Architecture Design (2-3 architectes //) → Implementation → Quality Review (3 reviewers //) → Summary.

**Différence avec spec persistant** : feature-dev fait tout en session. Le pattern spec crée des artefacts collaboratifs pour exécution séparée.

## Anti-patterns documentés

- **Vibe coding** (pas de spec) → chaque itération perd du contexte
- **Monolithic spec** (>150 instructions) → compliance drop par règle ajoutée
- **Corriger > 2 fois** → /clear et réécrire le prompt
- **Pas de verification** → sans tests/screenshots, aucun feedback loop
- **Kitchen sink session** → tâches non liées polluent le contexte

## Le SDD Triangle (Drew Breunig)

SPEC ↔ TESTS ↔ CODE en feedback loop. La spec n'est pas figée — implémenter le code améliore la spec. Outil Plumb : sur git commit, extrait les décisions du diff, met à jour la spec automatiquement.

## Trois niveaux de maturité (Birgitta Böckeler, Thoughtworks)

⚠️ Attribution corrigée : les 3 niveaux viennent de **Birgitta Böckeler** ([martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)), pas de Heeki Park ni Drew Breunig. Park (AWS) utilise ces niveaux en référençant Böckeler explicitement.

1. **Spec-first** — spec écrite avant le dev, peut drifter après
2. **Spec-anchored** — spec maintenue comme living document tout au long du cycle de vie
3. **Spec-as-source** — spec = seul artefact humain, code = output généré, jamais touché à la main

## Liens

- [[MOC-Techniques]]
- [[workflow-claude-code-optimal]] — Pipeline d'implémentation EN AVAL de la spec
- [[over-specification-paradox]] — Risque de sur-spécification (concept, pas de chiffre canonique attesté)
- [[Context Engineering]] — La spec est un artefact de context engineering
- [[methode-analyser-repo]] — Plugin feature-dev dans le setup
- [[Agents IA]] — Agents spécialisés dans les frameworks SDD

## Architectures concrètes — structures de dossiers

### Architecture Neoteem /spec (implémentée mai 2026)

Skill `/spec` déployée dans ia_back + neo_ia. Pipeline : interview → exploration → architecture → génération adaptative.

**Taille M (feature mono-repo)** :
```
TODO/feature-<nom>/
  SPEC.md        ← vision + architecture + critères d'acceptation
  BRIEF.md       ← ce que le dev doit savoir (QUOI, pas COMMENT)
```

**Taille L (feature multi-repo)** :
```
TODO/feature-<nom>/
  SPEC.md
  BRIEF-IA-BACK.md     ← brief dev ia_back
  BRIEF-NEOIA.md       ← brief dev neo_ia
  BRIEF-FRONT.md       ← si front touché
  CONTRADICTIONS.md    ← si incohérences entre BRIEFs
```

**Taille XL (grosse feature cross-team)** :
```
TODO/feature-<nom>/
  00-vision.md         ← le QUOI et le POURQUOI
  01-architecture.md   ← le COMMENT (2-3 approches, choix marqué)
  02-endpoints.md      ← contrats API si ia_back touché
  03-tools.md          ← tools LLM si neo_ia touché
  04-priorites.md      ← vagues d'implémentation + estimations
  BRIEF-IA-BACK.md
  BRIEF-NEOIA.md
  BRIEF-FRONT.md
  CONTRADICTIONS.md
```

**Innovation clé** : Cross-BRIEF contradiction detection — prompt inline vérifie automatiquement les incohérences entre BRIEFs (format réponse API, pagination, auth, responsabilité de création). Personne d'autre ne fait ça.

**Calibration gate** : taille déterminée APRÈS exploration (pas avant). M par défaut, re-calibré en phase 2. Pas de taille S (trop trivial pour /spec).

### Architecture GitHub Spec Kit (~105K stars mai 2026)

```
specs/001-feature-name/
  spec.md
  plan.md
  tasks.md
  research.md
  data-model.md
  contracts/api-spec.json
  checklists/manual-testing.md
```

Concept de **Constitution** (`.specify/memory/constitution.md`) = règles architecturales non-négociables vérifiées en continu.

6 commandes : `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`

### Architecture GSD (~59K stars mai 2026)

```
PROJECT.md       ← vision et scope
REQUIREMENTS.md  ← requirements dérivés
ROADMAP.md       ← phases et dépendances
STATE.md         ← état courant (quelle phase, quoi fait/restant)
CONTEXT.md       ← contexte technique consolidé
```

Chaque subagent reçoit un **contexte frais** (200K tokens). Plans scopés à ~50% d'un contexte frais. 6 commandes : `/gsd-new-project` → `/gsd-discuss-phase` → `/gsd-plan-phase` → `/gsd-execute-phase` → `/gsd-verify-work` → `/gsd-ship`

Insight clé : "Plans are prompts — the PLAN.md file IS the executable instruction."

### Architecture BMAD (~46K stars v6.6.0 avril 2026)

Document Sharding : PRD + architecture docs → Story Files (`{epicNum}.{storyNum}.story.md`). Chaque story embarque le contexte archi + acceptance criteria. **21 agents spécialisés** (BA, PM, Architect, PO, Scrum Master, Dev, QA, etc.) + 50+ guided workflows + Scale-Adaptive Intelligence (Quick Flow / BMad Method / Enterprise Method).

Best pour gros projets greenfield. Overkill pour itération rapide.

### Architecture Kiro (AWS)

Design-first (pas requirements-first). Agent Hooks pré/post task. Parallel task execution via DAG de dépendances. "Steering files" pour contexte persistant.

### Architecture Jeremie (blog)

```
docs/
  specs/
    00-overview.md
    01-requirements.md
    02-architecture.md
    03-data-models.md
    04-ui-ux.md
    05-features/
      auth.md
      dashboard.md
  decisions/
    ADR-001-framework-choice.md
  prompts/
    system-prompt.md
    tasks/
      task-001.md
```

### Addy Osmani — 6 zones obligatoires (GitHub 2500+ configs analysés)

1. **Commands** — commandes exécutables complètes avec flags
2. **Testing** — framework, locations, coverage
3. **Project structure** — layout explicite
4. **Code style** — un snippet réel > 3 paragraphes
5. **Git workflow** — branch naming, commit format, PR
6. **Boundaries** — always do / ask first / never do

## Pipeline complet Neoteem

```
/spec (idée floue → dossier spec)
  ↓
/decompose-ticket (spec → tâches CC par vagues parallèles) [optionnel, pour XL]
  ↓
/go (exécution : lint → tests → review → commit → push)
```

## Comment déployer /spec sur un nouveau repo

1. Copier `.claude/skills/spec/` (SKILL.md + references/)
2. Adapter la phase 2 aux agents locaux du repo (codebase-analyst, architect, etc.)
3. Adapter les output-templates.md au stack du repo (hexa, MVC, monorepo, etc.)
4. Ajouter `skills: neo-brain-dev-ia` si le repo a accès au vault neoteem-brain
5. Vérifier que `AskUserQuestion` est dans `allowed-tools`

## Outils complémentaires à surveiller

- **Plumb** (Drew Breunig) — pre-commit hook qui extrait les décisions du diff, les compare à la spec, met à jour automatiquement. `.plumb/` directory avec decisions.jsonl + requirements.json + coverage.json
- **Quellit AI** — transforme acceptance criteria en test suites complètes
- **VSDD** (Verified SDD) — Builder et Adversary utilisent des modèles DIFFÉRENTS pour blind-spot diversity
- **Spine Pattern** — meta-repo au-dessus des repos de code, ne contient que markdown + task files. Coordination multi-repo sans duplication