---
titre: "Audit notes existantes vault vs sources fraîches chantier 22 mai"
resume: "Pour chaque sujet canonique : couverture actuelle, manques détectés vs rapports frais, obsolescence, verdict ABSORBER/RÉÉCRIRE/REMPLACER/CRÉER"
aliases:
  - "audit notes vs fraiches"
  - "couverture vault sujets canoniques"
  - "absorber reecrire remplacer creer"
  - "audit chantier 22 mai notes existantes"
  - "couverture sujets canoniques chantier"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#projet/forge"
---

# Audit notes existantes vault vs sources fraîches — chantier 22 mai 2026

> Méthode : pour chaque sujet canonique, lecture intégrale des notes existantes + croisement systématique avec les 8 rapports déposés dans `0-Inbox/_chantier-22mai/`. Verdict par note ET par sujet.

> Légende verdicts :
> - **ABSORBER** : contenu unique à préserver dans la nouvelle canonique
> - **RÉÉCRIRE** : base OK, enrichir 2-3× avec sources fraîches
> - **REMPLACER** : obsolète ou faux, à remplacer entièrement
> - **CRÉER** : note inexistante, à créer from scratch
> - **GARDER** : note encore valide, ne pas toucher

---

## Sujet 1 — Comment créer une skill Claude Code

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `skills-guide` | `01-Claude/Code/best-practices/skills-guide.md` | 2026-05-14 | Anatomie skill (dossier), frontmatter YAML complet, 9 catégories Thariq, progressive disclosure, /doctor, gotchas |
| `Agent — skill-creator` | `01-Claude/Code/agents/Agent — skill-creator.md` | 2026-05-08 | Fiche agent meta-créateur, 17 lignes, pointeur |
| `pattern-agentic-engineering` section skills | `04-Techniques/agents/pattern-agentic-engineering.md` | 2026-05-21 | Skills obligatoires (/recap, /go), règles (<500L, gotchas, progressive disclosure, Apprentissage) |
| `setup-project-complet` section skills | `01-Claude/Code/best-practices/setup-project-complet.md` | 2026-04-26 | Plugins skills officiels Anthropic, slash commands clés |

### Couverture actuelle (QUOI/POURQUOI/COMMENT/QUAND/OPTIM/ANTI-PATTERNS/EXEMPLES)

- **QUOI** : ✅ très bien — dossier complet, pas juste markdown, hub SKILL.md
- **POURQUOI** : ✅ progressive disclosure expliqué (~100 tokens metadata, body on-demand)
- **COMMENT** : ✅ frontmatter YAML exhaustif (15 champs documentés), substitutions $ARGUMENTS, 9 catégories Thariq
- **QUAND** : ⚠️ "description = trigger" mentionné mais pas formalisé comme principe central — gotcha activation 73% silencieusement cassées présent mais formule directive partielle
- **WORKFLOW** : ❌ workflow de création (capture intent → draft → test cases → eval `generate_review.py` → improve) ABSENT
- **OPTIM** : ✅ budget /doctor, post-compaction 5k/25k, < 500L
- **ANTI-PATTERNS** : ⚠️ partiel — gotchas listés mais pas les 5 anti-patterns officiels Anthropic (monolithique, charger upfront, contextes mutuellement exclusifs, deviner contexte, faire faire du déterministe au LLM)
- **EXEMPLES** : ❌ peu d'exemples concrets de skill réelle structurée

### Manques détectés vs rapports frais

1. **Workflow `skill-creator` Anthropic canonique** (rapport github-karpathy section 1.3) :
   - "capture intent → draft → run test cases (with-skill ET baseline en parallèle) → eval via `generate_review.py` → improve"
   - "Description field drives triggering — make it a little bit pushy" — citation Anthropic
   - Scripts `package_skill.py` → `.skill` file pour packaging
   - Baseline = no skill (nouveau) OU version précédente (amélioration)
   → MANQUE complètement

2. **Progressive disclosure 3 niveaux officiel** (blog-docs-anthropic §7) :
   - Level 1 : name + description pré-chargés (~100 tokens)
   - Level 2 : full SKILL.md body chargé quand applicable
   - Level 3+ : fichiers bundlés (`reference.md`, `forms.md`...) chargés on-demand
   - "context bundlé dans un skill est effectively unbounded"
   → Notion présente mais pas les 3 niveaux verbatim avec leur sémantique

3. **Citation Trail of Bits** (mcp-vs-skills §6) :
   - "Keep SKILL.md under 2000 words and move detailed content into references/"
   - "bundle analysis checklists, vulnerability patterns, example outputs, decision logic"
   → forge dit 500 lignes, TOB dit 2000 mots — préciser le double critère

4. **Skills clusterisent en 9 catégories** (recherche-x §2) :
   - "Les bonnes skills tombent dans une seule, les confuses en chevauchent plusieurs"
   - Citation manquante : "skills are the abstraction that all agents will build on" — Thariq 21 mars
   → Présent dans skills-guide MAIS pas le test "1 catégorie = skill propre, multiple = à splitter"

5. **Citation Willison "Cambrian explosion"** + "Skills awesome, maybe a bigger deal than MCP" — absent

6. **Skills file-system based / progressive context disclosure** (Thariq workshop verbatim) :
   - "Skills are an example of being very file system or bash tool built, because they're just really folders that your agent can CD into and read."
   → Pas capturé verbatim

7. **Citation Anthropic skills-explained "MCP connects to data; Skills teach what to do"** — absente de skills-guide (présente dans mcp-vs-cli-vs-skills)

8. **Section Gotchas = append-mostly** (recherche-x §2) :
   - "`/gotcha` → Claude trouve la skill concernée, ouvre le fichier, ajoute à la section Gotchas"
   - "the most highest-signal content in any skill is the Gotchas section"
   → Mentionné comme principe 2 mais pas le workflow `/gotcha` append-mostly

### Obsolescence détectée

- `skills-guide` est globalement à jour (mai 2026), pas d'obsolescence majeure
- `setup-project-complet` (avril 2026) : OK sur skills section, mais ne reflète pas les nouvelles features Routines/Outcomes/Dreaming citées dans rapport youtube
- `Agent — skill-creator` : trop léger (17 lignes), pointeur vide — ne reflète pas le workflow Anthropic canonique

### Verdict sujet 1

- `skills-guide` : **RÉÉCRIRE** (base solide, enrichir 2× avec workflow Anthropic + 3 niveaux progressive disclosure verbatim + citations Willison/TOB/Anthropic)
- `Agent — skill-creator` : **GARDER** (fiche agent, pas une note canonique)
- Sections skills de pattern-agentic-engineering / setup-project-complet : **GARDER** (rôle distinct = checklist projet)
- **CRÉER** note canonique séparée si non couverte par enrichissement skills-guide

---

## Sujet 2 — Comment créer un agent Claude Code

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `agents-orchestration` | `01-Claude/Code/best-practices/agents-orchestration.md` | 2026-05-14 | Frontmatter YAML 17 champs, Generator/Evaluator, Dreaming/Outcomes, Agent Teams, claude-progress.txt |
| `agents-color-convention` | `01-Claude/Code/best-practices/agents-color-convention.md` | 2026-05-21 | Palette 8 couleurs par catégorie, règle cross-repo |
| `agent-manager-role` | `01-Claude/Code/best-practices/agent-manager-role.md` | 2026-05-20 | Rôle DRI org, 3 niveaux d'investissement, gouvernance |
| Section agents `pattern-agentic-engineering` | `04-Techniques/agents/pattern-agentic-engineering.md` | 2026-05-21 | 4 agents obligatoires + recommandés, règles agents |
| `Agent — agent-creator` | `01-Claude/Code/agents/Agent — agent-creator.md` | 2026-05-08 | Fiche meta-créateur, 18 lignes |

### Couverture actuelle

- **QUOI** : ✅ excellent — frontmatter complet, distinction agent / built-in (Explore, Plan, general-purpose)
- **POURQUOI** : ✅ Boris cité "feature-specific > qa/backend general", protection contexte
- **COMMENT** : ✅ très bon — `permissionMode`, `memory: project`, `isolation: worktree`, `effort`, `disallowedTools`, `skills:` frontmatter
- **QUAND** : ⚠️ partiel — couvre "isolate side-task" mais ne couvre pas la doctrine officielle Anthropic verbatim ("They're useful for tasks that read many files or need specialized focus without cluttering your main conversation")
- **WORKFLOW** : ⚠️ Generator/Evaluator présent, Sprint Contracts présent, mais workflow Anthropic two-agent architecture (Initializer + Coding Agent) ABSENT
- **OPTIM** : ✅ Agent Teams vs subagents, effort levels
- **ANTI-PATTERNS** : ⚠️ couvre "agents skew positive when grading own work", mais ne liste pas l'anti-pattern Anthropic "split by problem type" (planner/impl/tester/reviewer → telephone game)
- **EXEMPLES** : ✅ exemples Boris (code-simplifier, verify-app), pipeline 3 agents (Planner/Generator/Evaluator $0.46/$113.85/$10.39)

### Manques détectés vs rapports frais

1. **Two-agent architecture Anthropic** (blog-docs §4) :
   - Initializer Agent (scaffold env, `init.sh`, `claude-progress.txt`, `feature_list.json`, git baseline)
   - Coding Agent (incrémental, clean state)
   - "Distinction uniquement par leur user prompt initial. System prompt et tools identiques."
   - Failure mode officiel : "later agent instance surveys partial progress and declares the job done"
   → ABSENT (article Justin Young, 26 nov 2025)

2. **Sub-agents = context protection (Thariq verbatim)** (youtube-watch §3) :
   - "Sub agents were made to protect the context of the core agent"
   - "Sub agents are great for when you need to do a lot of work and return an answer to the main agent"
   - Sub-agents pour verification : "feed it a bunch of stuff and then tell it to critique it"
   - "Ideally, the best form of verification is rule-based"
   → ABSENT verbatim

3. **Context-centric split vs split by problem type** (youtube-watch §"Patterns multi-agent") :
   - "Work should only be split when context can be truly isolated"
   - "an agent handling a feature should also handle its tests, because it already possesses the necessary context"
   - Anti-pattern : "subagents spent more tokens on coordination than on actual work" (telephone game)
   → ABSENT — manque doctrine fondamentale

4. **Agent SDK gère race conditions bash + parallel sub-agents** (Thariq) :
   - "When you're running parallel sub agents at the same time, bash becomes very complex and there are lots of race conditions. We've solved that"
   - Exemple spreadsheet sub-agents parallèles
   → ABSENT

5. **Lethal trifecta + Swiss cheese defense** (Thariq) :
   - "execute code in env + change FS + exfiltrate code" = lethal trifecta
   - "Swiss cheese defense : alignment + permissioning + AST parser bash + sandbox"
   → ABSENT — critique pour design d'agents avec accès tools sensibles

6. **Métriques Boris 2026 mai mises à jour** (rapport youtube §2 Sequoia) :
   - 150 PRs en un seul jour record (avant : 259 PRs / 30 jours dans `agents-orchestration` cite Boris janvier)
   - "centaines d'agents par session, milliers la nuit"
   - "loops are the future" — dizaines de loops permanents
   → agents-orchestration cite "5-10 root sessions, quelques centaines d'agents" et "150 PRs un seul jour" — DÉJÀ présent, à confirmer date

7. **Anti-pattern Boris "split by role" + Anthropic blog explicite** : non capturé

8. **`isolation: worktree` + bug Claude Code v2.1.69+** (pipeline-boris §"Mise à jour 21 mai soir") :
   - Bug session-reset-markers wipe à chaque sub-agent worktree
   - Fix : ne wipe QUE si `source=startup` ET pas d'`agent_type`
   → Détail spécifique forge mais important pour qui design des agents en worktree

### Obsolescence détectée

- `agents-orchestration` (mai 2026) — globalement à jour
- `pattern-agentic-engineering` (21 mai) — mise à jour récente, valide
- `Agent — agent-creator` : trop léger, doctrine officielle non reflétée
- Note importante : pattern `architect-first` markers + hooks (architecture-first-pipeline) est **OBSOLÈTE** depuis 22 mai (suppression hooks workflow) — déjà signalé en bas de cette note. À NE PAS référencer comme canonique dans la nouvelle note agents.

### Verdict sujet 2

- `agents-orchestration` : **RÉÉCRIRE** (excellente base, enrichir avec Thariq verbatim "context protection", anti-pattern split-by-role, two-agent Anthropic architecture, lethal trifecta/swiss cheese)
- `agents-color-convention` : **GARDER** (norme forge interne, complète)
- `agent-manager-role` : **GARDER** (sujet org, distinct du sujet création)
- `pattern-agentic-engineering` : **GARDER** (checklist projet, complémentaire)
- `Agent — agent-creator` : **GARDER** (pointeur)

---

## Sujet 3 — Comment créer un hook Claude Code

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `hooks-guide` | `01-Claude/Code/best-practices/hooks-guide.md` | 2026-05-14 | 25+ events, 5 handlers, exit 2, marker+guard, hookSpecificOutput, self-improving (mai 2026), anti-pattern workflow enforcement (22 mai) |
| `delegate-guard-pattern` | `01-Claude/Code/best-practices/delegate-guard-pattern.md` | 2026-04-26 | Pattern hook protection composants forge, checklist setup |
| Section hooks `audit-claude-folder-pattern` | `04-Techniques/patterns/audit-claude-folder-pattern.md` | 2026-05-22 | Audit hooks via project-auditor, gotchas (MultiEdit blind spot, stack drift) |
| `Agent — hook-creator` | `01-Claude/Code/agents/Agent — hook-creator.md` | 2026-05-08 | Fiche meta-créateur, 18 lignes |

### Couverture actuelle

- **QUOI** : ✅ exhaustif — 25+ events listés, 5 types handlers (command/http/mcp_tool/prompt/agent)
- **POURQUOI** : ✅ "hooks = déterministe 100%, CLAUDE.md = advisory" — citation Boris
- **COMMENT** : ✅ exit 2 par event, hookSpecificOutput JSON avancé, marker+guard pattern
- **QUAND** : ✅ tableau "Besoin → Solution" couvre les 6 cas principaux + anti-pattern workflow enforcement (22 mai)
- **WORKFLOW** : ⚠️ self-improving (Stop hook learning-reminder) présent — bien
- **OPTIM** : ✅ asyncRewake, timeout 60s, MultiEdit matcher gotcha
- **ANTI-PATTERNS** : ✅ FORT — anti-pattern workflow enforcement révisé 22 mai détaillé, exemples concrets supprimés (architect-guard, commit-guard, dispatch-guard)
- **EXEMPLES** : ✅ très bon — auto-format Boris, agent Stop hook, delegate-guard, vault-query-guard

### Manques détectés vs rapports frais

1. **Doctrine Anthropic officielle verbatim "guardrails in hooks"** (blog-docs §2) :
   - "An instruction like 'never edit `.env`' in CLAUDE.md or a skill is a request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement"
   - "If a rule must hold every time, make it a hook rather than a prompt instruction"
   → Boris cité mais formulation Anthropic officielle docs absente verbatim

2. **Alex Albert "red squigglies for agents"** (recherche-x §6 + recherche-youtube §1) :
   - Daisy Hollman dit aussi "red squigglies for agents" (CwC SF)
   - Métaphore canonique pour expliquer rôle hooks
   → ABSENT

3. **Fowler Guides+Sensors taxonomy** (github-karpathy §4) :
   - Guides (feedforward) vs Sensors (feedback)
   - Computational vs Inferential
   - "Hooks Python exit 2 = Sensors Computational"
   - Citation Fowler : "Computational sensors d'abord (catch structurel cheap+deterministe)"
   → ABSENT — taxonomie utile pour positionner les hooks dans le harness

4. **Addy Osmani "Ratchet Principle"** (recherche-x §9) :
   - "the harness only tightens, never loosens"
   - "When agent makes error, you fix the harness, not the output → error can't happen again"
   - "the agent ran a destructive command, so you add a hook that blocks it"
   → ABSENT — formalisation utile

5. **Hashimoto AGENTS.md compounding pattern** (github-karpathy §3) :
   - "Each line in that file is based on a bad agent behavior"
   - Ghostty AGENTS.md (prompt interdictions explicites)
   - Forge a dépassé ce stade (hooks exit 2), MAIS la philosophie compounding vaut d'être citée
   → ABSENT comme référence cross-leader

6. **Self-improving hooks rôle sous-exploité** (déjà présent depuis Anthropic blog "Claude Code at scale" 14 mai) — bien couvert, GARDER

7. **Hashimoto formule canonique "Anytime you find an agent makes a mistake, take the time to engineer a solution"** — ABSENT

8. **Anti-pattern Boris vs forge supprimé 22 mai** : couvert FORT, c'est l'apport principal récent

9. **Trail of Bits `enableAllProjectMcpServers: false`** (mcp-vs-skills §6 + recherche-github §6) :
   - "prevent compromised repositories from injecting malicious MCP servers"
   → Relié hooks/sécurité, à mentionner

### Obsolescence détectée

- `hooks-guide` (mai 2026) : globalement à jour, mise à jour 22 mai forte
- `delegate-guard-pattern` (avril 2026) : pattern toujours valide, exemple canonique forge

### Verdict sujet 3

- `hooks-guide` : **RÉÉCRIRE** (excellente base 22 mai, enrichir avec doctrine Anthropic verbatim "guardrails", taxonomie Fowler Guides+Sensors, Ratchet Principle Osmani, Hashimoto formule canonique, "red squigglies for agents")
- `delegate-guard-pattern` : **GARDER** (pattern forge spécifique, exemple)
- `Agent — hook-creator` : **GARDER** (pointeur)

---

## Sujet 4 — Comment écrire un CLAUDE.md

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `claudemd-guide` | `01-Claude/Code/best-practices/claudemd-guide.md` | 2026-05-14 | < 200 lignes officiel, test Boris "Would removing this cause mistakes?", loading order, @import, rules paths frontmatter, compaction, advisory nature |
| `claudemd-maintenance` | `04-Techniques/patterns/claudemd-maintenance.md` | 2026-05-10 | Tailles recommandées (Anthropic 200 / Boris 100 / commu 40-60), test, où mettre quoi, anti-patterns, mécanisme maintenance |
| `Agent — claudemd-optimizer` | `01-Claude/Code/agents/Agent — claudemd-optimizer.md` | 2026-05-08 | Fiche meta-créateur, 18 lignes |

### Couverture actuelle

- **QUOI** : ✅ très bon — < 200L officiel + ~100L Boris explicite
- **POURQUOI** : ✅ "chaque ligne coût récurrent en tokens", advisory nature, compaction
- **COMMENT** : ✅ INCLURE/NE PAS INCLURE, hiérarchie chargement, @import, rules paths, html comments 0 tokens
- **QUAND** : ✅ frontière CLAUDE.md / Rules / Skills / Hooks claire
- **WORKFLOW** : ✅ pattern compounding, audit mensuel, tag `@.claude` PR Boris cité
- **OPTIM** : ✅ "ruthlessly prune", over-specification S* = 0.509 quadratique
- **ANTI-PATTERNS** : ✅ 4 anti-patterns (Context Stuffing, Static Memory, Tools in prose, Over-specification)
- **EXEMPLES** : ⚠️ peu d'exemples de structure réelle de CLAUDE.md court

### Manques détectés vs rapports frais

1. **Tableau INCLURE/EXCLURE verbatim Anthropic** (blog-docs §1) :
   - ✅ Bash commands Claude can't guess / ❌ Anything Claude can figure out by reading code
   - ✅ Code style rules that differ from defaults / ❌ Standard language conventions Claude already knows
   - ✅ Testing instructions / ❌ Detailed API documentation
   - ✅ Repository etiquette / ❌ Information that changes frequently
   - ✅ Architectural decisions / ❌ Long explanations or tutorials
   - ✅ Developer environment quirks / ❌ File-by-file descriptions of the codebase
   - ✅ Common gotchas / ❌ Self-evident practices like "write clean code"
   → ABSENT en tableau verbatim (les principes y sont mais pas le tableau officiel)

2. **5 "Common failure patterns" officiels Anthropic** (blog-docs §1) :
   1. Kitchen sink session
   2. Correcting over and over
   3. Over-specified CLAUDE.md
   4. Trust-then-verify gap
   5. Infinite exploration
   → ABSENT comme liste canonique des 5 anti-patterns Anthropic

3. **Verbatim verif claudemd-taille** (verif-claudemd-taille-officielle.md) :
   - "target under 200 lines per CLAUDE.md file"
   - Section "My CLAUDE.md is too large" verbatim
   - Distinction critique : 200L recommandation CLAUDE.md vs 200L/25KB HARD limit auto-memory MEMORY.md
   → DISTINCTION CRITIQUE MEMORY.md vs CLAUDE.md ABSENTE — risque confusion

4. **Citation Anthropic Memory page** :
   - "CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence"
   - "Splitting into @path imports helps organization but does not reduce context, since imported files load at launch"
   → ABSENT

5. **Karpathy 4 rules CLAUDE.md viral 220k stars** (recherche-x §7 + github §5) :
   - Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution
   - Plan format `1. [Step] → verify: [check]`
   - Forrest Chang repo (110k+ stars)
   → Partiellement présent dans `Karpathy Dev Discipline` (autre note) mais pas dans claudemd-guide comme exemple canonique court

6. **Exemple Anthropic claude-for-legal 130L** (recherche-github §1.2) :
   - 5 sections : Layout · Validation · Conventions · Cookbooks · Things to Leave Alone
   - Invariants nommés I1-I11
   - "Things to Leave Alone" rassurant ("not a bug, probably intentional")
   - Validation enforcement : `claude plugin validate` + `python3 scripts/lint-tool-scope.py`
   - "Orchestrator = local-only tools; MCP/write tools = subagent leaves only"
   → ABSENT — exemple canonique officiel Anthropic à citer

7. **Hashimoto Ghostty AGENTS.md** (recherche-github §3.2) :
   - "Each line based on a bad agent behavior"
   - Interdictions explicites : "Never create an issue", "Never create a PR"
   → ABSENT — référence cross-leader

8. **Test "Would removing this cause Claude to make mistakes?"** : présent ✅

9. **Routines / hooks-led updates** (recherche-youtube §1.4) :
   - "tag `@.claude` sur PRs déclenche GitHub Action qui commit la mise à jour"
   - "Compounding Engineering" (Dan Shipper)
   → Partiellement présent mais pas comme workflow canonique nommé

### Obsolescence détectée

- `claudemd-guide` (mai 2026) : à jour, mais ne distingue pas explicitement CLAUDE.md (200L recommandation) vs MEMORY.md auto-memory (200L/25KB HARD limit) — risque confusion documenté dans verif fraîche
- `claudemd-maintenance` : valide, tailles Anthropic/Boris/communauté bien documentées
- `Agent — claudemd-optimizer` : trop léger

### Verdict sujet 4

- `claudemd-guide` : **RÉÉCRIRE** (base solide, enrichir avec tableau INCLURE/EXCLURE verbatim, 5 failure patterns Anthropic, distinction CLAUDE.md/MEMORY.md, exemple claude-for-legal 130L, référence Karpathy 4 rules + Hashimoto compounding)
- `claudemd-maintenance` : **ABSORBER** dans nouvelle canonique OU GARDER comme note pattern complémentaire (les deux notes peuvent fusionner)
- `Agent — claudemd-optimizer` : **GARDER** (pointeur)

---

## Sujet 5 — Workflow optimal Claude Code (pipeline, parallélisation, modèles)

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `pipeline-boris-adapte-neoteem` | `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md` | 2026-05-22 | Recette neoteem mai 2026 — routing S/M/L, max 3 tests, REFACTOR supprimé, effort high default, conditionnel + MAJ 22 mai suppression hooks workflow |
| `Workflow Boris` | `04-Techniques/patterns/Workflow Boris.md` | 2026-04-21 | Fleet Commander 5 terminaux + 5-10 cloud, worktrees, Plan Mode, voice |
| `boris-workflow-2026-may` | `04-Techniques/patterns/boris-workflow-2026-may.md` | 2026-05-11 | Boris mai 2026 — 5-10 sessions web, centaines d'agents, /loop killer feature, 150 PRs record, MCP universel |
| `best-practices-claude-code-leaders` | `04-Techniques/patterns/best-practices-claude-code-leaders.md` | 2026-05-10 | Synthèse Boris+Erik+Thariq+Cat+Karpathy 9 sections |
| `pattern-agentic-engineering` | `04-Techniques/agents/pattern-agentic-engineering.md` | 2026-05-21 | Checklist projet 5 phases + MAJ mai (modèles, TDD test-first, sprint contract) |
| `vibe-coding-setup-complet` | `04-Techniques/patterns/vibe-coding-setup-complet.md` | 2026-05-10 | Architecture complète neo_ia/ia_back, /recap /go, journalier, RECAP |
| `pattern-architect-first-pipeline` | `04-Techniques/patterns/pattern-architect-first-pipeline.md` | 2026-05-08 | Pattern markers + 6 hooks + advisor (OBSOLÈTE depuis 22 mai) |
| `harness-engineering` | `04-Techniques/agents/harness-engineering.md` | 2026-05-14 | Fowler + Osmani + Willison, formule Agent=Model+Harness, computational vs inferential |

### Couverture actuelle

- **QUOI** : ✅ très bon — pipeline conditionnel, parallélisation, modèles
- **POURQUOI** : ✅ frictio 6× justifie refonte 22 mai, doctrine Anthropic explicite
- **COMMENT** : ✅ TRÈS complet — pipeline 5 étapes, routing S/M/L, max 3 tests, effort allocation
- **QUAND** : ✅ critères par gate (security si auth/PII, perf si SQL 3+ joins, etc.)
- **WORKFLOW** : ✅ EXCELLENT — pipeline-boris-adapte est le plus à jour
- **OPTIM** : ✅ gain mesuré (50-75% par feature)
- **ANTI-PATTERNS** : ✅ 6 anti-patterns documentés + symptômes alarme
- **EXEMPLES** : ✅ chiffres concrets (12-18 min, 1h30, 3-5 min)

### Manques détectés vs rapports frais

1. **Métriques Anthropic interne mises à jour** (recherche-youtube §1.2) :
   - 17× API YoY (London keynote)
   - 20h/sem dev moyen sur Claude Code
   - +200% PRs/eng Anthropic adoption wall-to-wall
   - 87% SWE-bench Verified Opus 4.7 (vs 62% Sonnet 3.7)
   - Eve Legal 5x cost reduction advisor strategy
   → Métriques industrie pas reflétées dans pipeline note (normales pour note pattern), MAIS pertinent pour synthèse leaders

2. **Multi-clauding / multi-session pattern Boris mai 2026** (youtube §3.2 + §4.2) :
   - "Most of my work I do from my phone"
   - "5-10 sessions web, probably few hundred agents going, few thousand overnight"
   - 150 PRs/jour record
   → boris-workflow-2026-may présent mais pas intégré dans pipeline canonique

3. **Routines = higher-order prompts** (youtube §1.4 + §4.2) :
   - "I'm not the one prompting. I'm the one that creates a routine that does the prompting"
   - "Routines are a higher order prompt"
   - cron + GitHub webhooks + API endpoints
   - dozens de loops permanents (babysit PRs, fix CI flaky, cluster feedback)
   → ABSENT comme pattern explicite

4. **Advisor strategy Eve Legal verbatim** (blog-docs + youtube §1.2) :
   - "Sonnet performed even more cheaply than on its own because Opus advised it to get its work done better"
   - "frontier model quality at 5x lower cost"
   - Map directement sur tool `advisor()` dispo
   → Présent dans agents-orchestration mais pas comme stratégie de pipeline

5. **Erik Schluntz 4 stratégies 22k LOC** (youtube §1 + recherche-youtube-talks §6) :
   - 1. Deep PM-style guidance / 2. Strict leaf-nodes scope / 3. Human core review / 4. Verifiable checkpoints
   - "tech debt OK on leaf nodes only"
   - "2 weeks compressed to 1 day"
   → Présent partiellement dans best-practices-claude-code-leaders §2 mais sans détail 4 stratégies

6. **Thariq compute allocator + HTML > Markdown** (recherche-youtube-talks §5) :
   - "~1% des tokens en prod, 99% en dashboards/micro-apps/planning artifacts"
   - "HTML is the new Markdown" — plans 1000 lignes en MD = désengagement
   - "throwaway micro-apps"
   - "delete scaffolding when new model lands"
   → ABSENT — pertinent pour planning et docs

7. **3 piliers Karpathy** (recherche-karpathy §7 + agentic-engineering-karpathy) :
   - Agent coding discipline + LLM Wiki + Software 3.0
   - 4 failure patterns (silent assumptions / hypertrophy / collateral changes / no verifiable criteria)
   → Présent partiellement, pas systémique dans pipeline

8. **Fowler Agent=Model+Harness** + Guides/Sensors :
   - "No fine-tuning, no model swap, just harness changes" → +21.8 points (Claude Opus 4.6 58→79.8% Terminal-Bench 2.0 via harness)
   - Convergence harness > model
   → harness-engineering note présente, à RELIER au pipeline canonique

9. **"Scaffolding hold Claude back" Lisa Crofoot London keynote** (youtube §1.3) :
   - "Designing for the next version of Claude, not the current one"
   - "More intelligent models can often get further with generalized primitives like a file system and sandbox computing environment"
   → ABSENT — fondamental pour décider quoi conserver dans harness

10. **Mercado Libre 23k engineers, 90% autonomous coding Q3 2026** (youtube §1.2)
    Spotify 1000+ PRs/mois -90% migration time
    Binti 20 jours sauvés foster licensing
    → Cas industrie ABSENT — utile pour contextualiser

### Obsolescence détectée

- `pattern-architect-first-pipeline` : **OBSOLÈTE** depuis 22 mai (suppression hooks workflow) — note à marquer obsolète ou réécrire en "historique des erreurs"
- `Workflow Boris` (avril 2026) : superseded par boris-workflow-2026-may (peut absorber)
- `vibe-coding-setup-complet` (10 mai) : utilise "TOUS opus" (zero sonnet), obsolète depuis politique mai (Sonnet exécution + Opus jugement — voir feedback_all_opus révisé)
- `best-practices-claude-code-leaders` (10 mai) : section 7 dit "Opus 4.7 par défaut" + "100% opus jamais sonnet medium" — partiellement obsolète depuis politique CwC 2026

### Verdict sujet 5

- `pipeline-boris-adapte-neoteem` : **GARDER + ABSORBER** (référence canonique pipeline neoteem la plus à jour — c'est elle qui doit être pointée par la nouvelle note canonique workflow)
- `Workflow Boris` : **REMPLACER** (superseded, fusionner dans boris-workflow-2026-may ou marquer historique)
- `boris-workflow-2026-may` : **RÉÉCRIRE** (à jour Sequoia mai, enrichir avec London keynote 19 mai + Routines + multi-clauding + advisor strategy verbatim)
- `best-practices-claude-code-leaders` : **RÉÉCRIRE** (sections 7 modèles obsolète, mettre à jour avec politique CwC 2026 Sonnet/Opus split, ajouter London keynote, routines, advisor)
- `pattern-agentic-engineering` : **GARDER** (mise à jour 21 mai valide)
- `vibe-coding-setup-complet` : **RÉÉCRIRE** (section "100% opus" obsolète, replacer par politique split + ajouter Routines + leaf-nodes Erik)
- `pattern-architect-first-pipeline` : **REMPLACER** (obsolète, marquer "historique pré-22mai")
- `harness-engineering` : **GARDER + ÉTENDRE** (fondamental, peut absorber Ratchet Principle Osmani + Lisa Crofoot "scaffolding holds back")

---

## Sujet 6 — Méthode analyse-repo (méta canonique)

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `audit-claude-folder-pattern` | `04-Techniques/patterns/audit-claude-folder-pattern.md` | 2026-05-22 | Méthode validée audit `.claude/` : 4 project-auditor parallèles + vérif empirique + DA + 3 vagues fix |
| `kit-rules-standard` | `01-Claude/Code/best-practices/kit-rules-standard.md` | 2026-04-26 | 3 rules obligatoires par projet : check-before-create, quality-gates, learn-from-mistakes |
| `setup-project-complet` | `01-Claude/Code/best-practices/setup-project-complet.md` | 2026-04-26 | Permissions par stack, ENV vars, flags CLI, slash commands, MCP, plugins LSP, hooks par framework |
| Section méthode `pattern-agentic-engineering` | `04-Techniques/agents/pattern-agentic-engineering.md` | 2026-05-21 | Workflow analyse/setup repo (6 étapes), 8 checks post-setup, composants indispensables |

### Couverture actuelle

- **QUOI** : ⚠️ ÉPARPILLÉ — pas de note canonique unique "comment auditer/setup un repo"
- **POURQUOI** : ✅ historique (audit fragmenté → 4 project-auditor parallèles), erreurs documentées
- **COMMENT** : ✅ très complet via `audit-claude-folder-pattern` (7 phases + gotchas) + `pattern-agentic-engineering` (6 étapes setup) + `kit-rules-standard` (rules min)
- **QUAND** : ✅ "user demande audite mon repo", maintenance trimestrielle
- **WORKFLOW** : ✅ excellent — phase 0 orientation → 4 auditeurs parallèles → vérif empirique → DA → 3 vagues fix → test comportemental
- **OPTIM** : ✅ parallélisation, scope par auditeur (pas general-purpose)
- **ANTI-PATTERNS** : ✅ JAMAIS Explore, JAMAIS general-purpose, JAMAIS 1 seul agent
- **EXEMPLES** : ✅ neo_ia 72 composants 26 fix, ia_back 74 composants 30+ fix le 22 mai

### Manques détectés vs rapports frais

1. **Pattern Anthropic minimaliste exposé** (recherche-github §1.1) :
   - anthropics/claude-code : 3 commandes seulement (`commit-push-pr`, `dedupe`, `triage-issue`), pas de CLAUDE.md
   - "Anthropic ne fait PAS de config porn"
   - Contraste fort avec forge 60+ composants → signal pour /forge-review
   → ABSENT comme référence "ce qu'Anthropic fait sur ses propres repos"

2. **Anthropic claude-for-legal 130L comme exemple** (déjà cité §4) — référence pour audit CLAUDE.md cible

3. **Patterns auditeurs faux positifs récurrents** : ✅ déjà couvert dans audit-claude-folder-pattern §"Phase 2 — Vérification empirique" — bien

4. **Karpathy 4 failure patterns à intégrer** : utile comme grille de lecture pour audit (silent assumptions, hypertrophy, collateral changes, no verifiable success) — pourrait enrichir checklist auditeurs

5. **Skills Stripe/Vercel/Cloudflare/Sentry comme baseline industrie** (github §6) :
   - Pattern `<org>/<domain>-best-practices` + `<org>/<domain>-upgrade`
   - Inspiration pour skills neo-* Neoteem
   → ABSENT — utile pour benchmark "ce qui se fait ailleurs"

6. **Trail of Bits claude-code-config production stack** (mcp-vs-skills §1.7) :
   - sandboxing + permissions + hooks + skills + MCP servers
   - skills chain `brainstorm → plan → execute → verify`
   - `enableAllProjectMcpServers: false` default sécurité
   → ABSENT — référence importante pour audit sécu

7. **Métriques empiriques harness > model** (github §4.6 + harness-engineering) :
   - 52.8% → 66.5% via harness changes seuls (Terminal Bench 2.0 LangChain)
   - 58% → 79.8% Claude Opus 4.6 (+21.8 points)
   → Présent dans harness-engineering, utile pour pédagogie audit

### Obsolescence détectée

- `audit-claude-folder-pattern` (22 mai) : ULTRA À JOUR, c'est la canonique de facto
- `kit-rules-standard` (avril 2026) : valide mais peut être enrichi avec rules révisées 22 mai
- `setup-project-complet` (avril 2026) : valide

### Verdict sujet 6

- `audit-claude-folder-pattern` : **GARDER** (canonique de facto, à pointer)
- `kit-rules-standard` : **RÉÉCRIRE** (mise à jour avec rules révisées 22 mai et politique Sonnet/Opus split)
- `setup-project-complet` : **RÉÉCRIRE** (mise à jour avec composants indispensables consolidés, exemple Anthropic minimaliste contre forge)
- **CRÉER** méta-note "méthode analyse/setup repo" qui orchestre les trois (audit + kit + setup) + pointe sur Workflow analyse-repo dans pattern-agentic-engineering

---

## Sujet 7 — Pattern Karpathy LLM Wiki / vault canonique

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `karpathy-llm-wiki-pattern` | `04-Techniques/patterns/karpathy-llm-wiki-pattern.md` | 2026-05-22 | 3 layers (raw/wiki/schema), 3 ops (Ingest/Query/Lint), fichiers obligatoires (index.md, log.md), tooling, application forge-brain |
| `agentic-engineering-karpathy` | `04-Techniques/agents/agentic-engineering-karpathy.md` | 2026-05-10 | Software 3.0, vibe vs agentic, jagged intelligence, shifted scarcity, workflow, agent-native infra |
| `Karpathy Dev Discipline` | `04-Techniques/patterns/Karpathy Dev Discipline.md` | 2026-04-26 | 4 principes (Think/Simplicity/Surgical/Goal-driven), implémentation Neoteem rules |
| `Andrej Karpathy` | `05-Leaders/agents/Andrej Karpathy.md` | 2026-05-08 | Fiche leader, LLM Wiki/AutoResearch/anti-patterns |

### Couverture actuelle

- **QUOI** : ✅ excellent (karpathy-llm-wiki-pattern créée 22 mai)
- **POURQUOI** : ✅ "Obsidian = IDE, LLM = programmer, wiki = codebase" verbatim
- **COMMENT** : ✅ très bon — 3 layers, 3 ops, fichiers obligatoires
- **QUAND** : ✅ tableau quand utiliser/pertinent par projet
- **WORKFLOW** : ✅ Ingest/Query/Lint détaillés
- **OPTIM** : ✅ tooling (qmd, Obsidian Web Clipper, Marp, Dataview)
- **ANTI-PATTERNS** : ✅ 6 anti-patterns vs doctrine Karpathy
- **EXEMPLES** : ✅ 4 implémentations communautaires listées + application forge-brain

### Manques détectés vs rapports frais

1. **Verbatim Karpathy plus complets** (recherche-karpathy §1) :
   - "Most people's experience with LLMs and documents looks like RAG... the LLM is rediscovering knowledge from scratch on every question. There's no accumulation."
   - "the wiki is a persistent, compounding artifact"
   - "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping"
   - "Humans abandon wikis because the maintenance burden grows faster than the value"
   - Référence Vannevar Bush Memex (1945) "the part he couldn't solve was who does the maintenance. The LLM handles that"
   → MANQUE plusieurs citations canoniques

2. **Lint cibles 6 verbatim** (recherche-karpathy §1.5) :
   - contradictions / stale claims / orphan pages / important concepts lacking page / missing cross-refs / data gaps fillable by web search
   - "eslint for knowledge"
   → Présent partiellement, 4 cibles génériques sans verbatim complet

3. **index.md "RAG-replacement à moyenne échelle" + scale 100 sources / hundreds of pages** :
   → Présent ✅

4. **log.md syntaxe exacte verbatim** :
   - Format `## [2026-04-02] ingest | Article Title`
   - `grep "^## \[" log.md | tail -5` (Unix tools)
   → Présent ✅

5. **Karpathy frontmatter EXPLICITEMENT silencieux** (recherche-karpathy §1.10 + Q4) :
   - "Karpathy NE PUBLIE PAS de spec frontmatter strict"
   - "intentionally abstract"
   - Communauté a convergé sur format minimal `**Tags**: ... **Created**: ... **Last Updated**: ...`
   - Notre forge-brain (4-6 aliases, resume, derniere-maj) PLUS STRICT que Karpathy
   → Présent ✅ dans Q4

6. **Karpathy a rejoint Anthropic 19 mai 2026** (recherche-karpathy §2.5 + §6) :
   - Équipe pretraining + lance équipe Claude-accelerated pretraining research
   - Implication stratégique : pattern LLM Wiki va influencer Claude
   → ABSENT de karpathy-llm-wiki-pattern (à ajouter)

7. **Repos Karpathy : il n'utilise PAS CLAUDE.md / AGENTS.md à la racine** (recherche-karpathy §4) :
   - nanochat : `.claude/skills/read-arxiv-paper/SKILL.md`
   - autoresearch : `program.md` unique
   - nanoGPT, llm.c : aucun schema racine
   - Cohérent avec philosophie "abstract, modular, pick what's useful"
   → Présent dans recherche mais pas dans karpathy-llm-wiki-pattern (à ajouter)

8. **autoresearch program.md détails** (recherche-karpathy §4.3) :
   - Only `train.py` may be modified
   - Fixed 5-min wall-clock budget
   - TSV tracking `commit, val_bpb, memory_gb, status, description`
   - Statuses: keep / discard / crash
   - Core loop: modify → commit → run → log → keep/revert. "Never stop"
   → Pattern transposable, ABSENT comme exemple

9. **forrestchang/andrej-karpathy-skills statut** (recherche-karpathy §5) :
   - 110k+ stars, 28 jours #1 GitHub Trending
   - Karpathy ne l'a PAS publiquement endorsé
   - Transcription par Forrest Chang, pas production Karpathy
   - "interprétation fidèle reconnue" mais pas canon
   → ABSENT — nuance importante

10. **Sequoia AI Ascent verbatim** (recherche-karpathy §3) :
    - "context windows are really kind of like working memory"
    - "you have to sort of program the working memory quite directly"
    - "you are in charge of the autonomy slider"
    - "any time your docs say click, this is bad"
    - "lms.txt" pour faire un site agent-readable
    - **Talk Sequoia NE MENTIONNE PAS** wikis/vaults/Obsidian (verbatim verified)
    → Présent dans agentic-engineering-karpathy mais formulation moins précise

11. **3 piliers Karpathy convergents** (recherche-karpathy §Q8) :
    - Agent coding discipline + LLM Wiki + Software 3.0
    - Glue : tout est markdown-first, agent-readable, human-curatable, LLM-maintained
    → ABSENT comme architecture globale

12. **Q7 "comment Karpathy résout vault bruité doublons" = lint** :
    → Présent ✅

### Obsolescence détectée

- `karpathy-llm-wiki-pattern` (22 mai) : note récente créée pendant chantier, v0.1 partielle (signalée par Raphael dans la mission)
- `agentic-engineering-karpathy` (10 mai) : valide, complémentaire
- `Karpathy Dev Discipline` (avril 2026) : valide, distinct (focus rules implémentation)
- `Andrej Karpathy` (8 mai) : à mettre à jour avec "joined Anthropic 19 mai" + métriques 220k stars

### Verdict sujet 7

- `karpathy-llm-wiki-pattern` : **RÉÉCRIRE** (note récente partielle, enrichir 2-3× avec verbatim canoniques + repos Karpathy réels + Anthropic move + autoresearch program.md pattern + forrestchang nuance + 3 piliers convergents)
- `agentic-engineering-karpathy` : **GARDER + ABSORBER** (sources Sequoia, à enrichir avec citations verbatim plus précises)
- `Karpathy Dev Discipline` : **GARDER** (note distincte rules)
- `Andrej Karpathy` : **RÉÉCRIRE** (fiche leader à mettre à jour Anthropic + 220k stars + statut LLM Wiki)

---

## Sujet 8 — MCP vs Skills+CLI doctrine

### Inventaire

| Note | Chemin | derniere-maj | Résumé |
|---|---|---|---|
| `mcp-vs-cli-vs-skills` | `01-Claude/Code/best-practices/mcp-vs-cli-vs-skills.md` | 2026-05-14 | Position Willison "skills > MCP", Boris "agentic search > RAG", benchmarks, matrice 5 critères, recommandation skill-first |
| Mention dans `skills-guide` | `01-Claude/Code/best-practices/skills-guide.md` | 2026-05-14 | Citation Willison + comparaison rapide |
| Section `architecture-cerveau-obsidian-mcp` | `04-Techniques/patterns/architecture-cerveau-obsidian-mcp.md` | — | MCP forge-brain architecture (pas le sujet doctrine) |

### Couverture actuelle

- **QUOI** : ✅ bon — comparaison skill / MCP / CLI sous 5 critères
- **POURQUOI** : ✅ token cost, fiabilité, état persistant
- **COMMENT** : ✅ matrice de décision, recommandation "commencer CLI, promouvoir MCP si frequency"
- **QUAND** : ✅ tableau Skills vs MCP par besoin
- **WORKFLOW** : ⚠️ pas de workflow décisionnel structuré "questions à poser"
- **OPTIM** : ✅ benchmarks tokens chiffrés
- **ANTI-PATTERNS** : ❌ ABSENT — pas de liste d'anti-patterns explicite
- **EXEMPLES** : ⚠️ peu d'exemples concrets de cas frontière

### Manques détectés vs rapports frais

1. **Citation Anthropic officielle "MCP connects to data; Skills teach what to do"** (mcp-vs-skills §1.2) :
   - "If you explain HOW to use → Skill. If Claude must ACCESS external system → MCP. Designed to be combined"
   - "Projects: 'here's what you need to know'. Skills: 'here's how to do things'"
   → ABSENT verbatim — citation canonique manquante

2. **Boris position Sequoia "MCP est toujours la simplest answer"** (mcp-vs-skills §1.6) :
   - "the same MCP connector you have in Claude AI... Cowork can use that. CLI can use it"
   - **MCP n'est PAS abandonné par Anthropic**, Skills viennent en complément
   → ABSENT — nuance critique car mcp-vs-cli-vs-skills penche fort "skills > MCP"

3. **Thariq 3-way trade-offs (Tools vs Bash vs Code gen)** (mcp-vs-skills §1.3 + youtube-watch §3) :
   - Tools : "structured/reliable, high context usage, no discoverability, not composable"
   - Bash : "composable, low context usage, discovery time"
   - Code gen : "highly composable, dynamic, longest to execute"
   - Quand chaque : Tools = atomic non-reversible (write_file, send_email), Bash = composable exploratoire, Code gen = dynamic data analysis
   → ABSENT — distinction Thariq 3-way critique pour décider

4. **Ronacher "Skills vs Dynamic MCP Loadouts"** (mcp-vs-skills §1.5) :
   - "Sentry MCP alone consumes ~8 000 tokens upfront"
   - "MCP descriptions trim brevity over stability — change query syntax without warning"
   - "the tool is largely under my control. When it breaks, ask agent to adjust it"
   → ABSENT — argument stabilité MCP critique

5. **Trail of Bits production stack + sécu** (mcp-vs-skills §1.7) :
   - `enableAllProjectMcpServers: false` default
   - "prevent compromised repositories from injecting malicious MCP servers"
   - skills + MCP coexistent en production
   → ABSENT — angle sécu critique

6. **Karpathy qmd pattern : LES DEUX interfaces** (mcp-vs-skills §1.4) :
   - "qmd has both a CLI (so LLM can shell out) AND an MCP server (so LLM can use it as native tool)"
   - "Ce n'est PAS l'un OU l'autre"
   → ABSENT — pattern hybride canonique non capturé

7. **Verdict pour forge-brain et neoteem-brain détaillé** (mcp-vs-skills §4 + §5) :
   - GARDER MCP + AJOUTER skill descriptor
   - Pour neoteem-brain encore plus fort (multi-tenant Cowork)
   - Pattern hybride futur si croissance
   → ABSENT — verdict opérationnel manquant

8. **6 anti-patterns documentés** (mcp-vs-skills §6) :
   - "Tout en MCP" / "Tout en Skills" / Container bash isolé / Description MCP courte+longue / Skill sans references / `enableAllProjectMcpServers: true`
   → ABSENT — liste manquante

9. **Citations verbatim consolidées** (mcp-vs-skills §7) : 7 leaders cités verbatim
   → ABSENT en bloc consolidé

10. **Distinction Skills vs Subagents** (blog-docs §2 Hook vs Skill + Skill vs Subagent) :
    - "Skills = reusable content you can load into any context. Subagents = isolated workers running separately"
    - "Combinable : subagent preload skills (`skills:` field). Skill in isolated context via `context: fork`"
    → Présent dans skills-guide mais pas dans mcp-vs-cli-vs-skills

### Obsolescence détectée

- `mcp-vs-cli-vs-skills` (14 mai 2026) : à jour mais SOUS-DOCUMENTÉ vs rapport frais (rapport fait 7 sections détaillées vs note 5 sections génériques)
- Penche skill-first Willison-pure alors qu'Anthropic + Boris + Trail of Bits + Karpathy ont position plus nuancée (MCP + Skills + CLI coexistent)

### Verdict sujet 8

- `mcp-vs-cli-vs-skills` : **RÉÉCRIRE** (note 2× plus dense, intégrer position officielle Anthropic + Boris MCP toujours valide + Thariq 3-way + Ronacher stabilité + Trail of Bits sécu + Karpathy qmd pattern hybride + verdict forge-brain/neoteem-brain + 6 anti-patterns + 7 citations verbatim consolidées)
- **CRÉER** note séparée si trop dense : `doctrine-mcp-vs-skills-2026.md` canonique + garder l'existante comme matrice rapide

---

## Synthèse — Plan de production

### Tableau récapitulatif verdicts

| Sujet | Notes existantes | Verdict global | Nouvelle note canonique ? |
|-------|-----------------|----------------|---------------------------|
| 1. Créer skill | skills-guide (solide) + Agent + pattern-agentic + setup | **RÉÉCRIRE** skills-guide + GARDER complémentaires | Enrichir skills-guide suffit |
| 2. Créer agent | agents-orchestration (solide) + color + manager + pattern + Agent | **RÉÉCRIRE** agents-orchestration + GARDER complémentaires | Enrichir suffit |
| 3. Créer hook | hooks-guide (solide 22 mai) + delegate-guard + audit + Agent | **RÉÉCRIRE** hooks-guide + GARDER complémentaires | Enrichir suffit |
| 4. Écrire CLAUDE.md | claudemd-guide + claudemd-maintenance + Agent | **RÉÉCRIRE** claudemd-guide + **ABSORBER** maintenance | Fusion possible |
| 5. Workflow optimal | pipeline-boris-adapte (canon 22 mai) + Workflow Boris + boris-mai + best-practices + pattern-agentic + vibe-coding + architect-first + harness | Complexe : 1 GARDER, 1 REMPLACER, 4 RÉÉCRIRE | **CRÉER** méta-note synthèse + nettoyer obsolètes |
| 6. Méthode analyse-repo | audit-claude-folder (canon 22 mai) + kit-rules + setup-project + pattern-agentic section | GARDER audit + RÉÉCRIRE kit-rules + setup | **CRÉER** méta-note orchestratrice |
| 7. Karpathy LLM Wiki | karpathy-llm-wiki (v0.1 22 mai) + agentic-engineering + Dev Discipline + Andrej | **RÉÉCRIRE** karpathy-llm-wiki + Andrej Karpathy | Enrichir suffit |
| 8. MCP vs Skills | mcp-vs-cli-vs-skills (sous-documenté) | **RÉÉCRIRE** 2× plus dense | Enrichir suffit OU créer canonique séparée |

### Notes à NETTOYER / MARQUER OBSOLÈTES

1. `pattern-architect-first-pipeline` — OBSOLÈTE depuis 22 mai (hooks workflow supprimés). Marquer "historique pré-22mai" ou supprimer.
2. `Workflow Boris` (avril 2026) — superseded par boris-workflow-2026-may. Fusionner.
3. Section "100% opus" dans `vibe-coding-setup-complet` et `best-practices-claude-code-leaders` — corriger avec politique CwC 2026 Sonnet/Opus split.

### Notes LIÉES à créer/enrichir (mentionnées dans la mission)

- **Karpathy** : enrichir karpathy-llm-wiki-pattern + Andrej Karpathy fiche
- **MCP** : enrichir mcp-vs-cli-vs-skills
- **Trail of Bits** : créer fiche `Trail of Bits` (référence sécu repeated dans 3 sujets)
- **Fowler / Böckeler** : enrichir harness-engineering avec taxonomie Guides+Sensors verbatim
- **Hashimoto Mitchell** : créer fiche leader + référence "AGENTS.md compounding"
- **Addy Osmani Ratchet Principle** : créer note pattern dans `04-Techniques/agents/` ou enrichir harness-engineering
- **Lisa Crofoot / Daisy Hollman / Jeremy Hadfield / Erik Schluntz / Thariq Shihipar / Cat Wu** : créer fiches manquantes dans `05-Leaders/claude-code/`

### Priorité de production recommandée

1. **P1 — Doctrine fraîche 22 mai (impact immédiat)** :
   - hooks-guide (RÉÉCRIRE — déjà à jour mais enrichir avec Fowler + Osmani + Hashimoto verbatim)
   - claudemd-guide (RÉÉCRIRE — distinction MEMORY.md critique + tableau Anthropic verbatim)
   - Méta-note workflow Sujet 5 (synthèse)

2. **P2 — Mises à jour cross-leaders** :
   - skills-guide (workflow Anthropic skill-creator)
   - agents-orchestration (Thariq verbatim + 2-agent Anthropic + lethal trifecta)
   - mcp-vs-cli-vs-skills (densification 2×)

3. **P3 — Karpathy + leaders fraîches** :
   - karpathy-llm-wiki-pattern (enrichissement complet)
   - Fiche Andrej Karpathy (joined Anthropic)
   - Fiches leaders manquantes (Lisa Crofoot, Daisy Hollman, Hashimoto, Osmani, Trail of Bits)

4. **P4 — Nettoyage** :
   - Marquer pattern-architect-first-pipeline OBSOLÈTE
   - Fusionner Workflow Boris dans boris-workflow-2026-may
   - Corriger sections "100% opus" obsolètes

### Risque de doublon à éviter

- Karpathy : 4 notes existantes (Andrej, agentic-engineering-karpathy, Karpathy Dev Discipline, karpathy-llm-wiki-pattern) — éviter d'en créer une 5ème, ENRICHIR existantes en se répartissant les angles (fiche leader / framework Sequoia / discipline coding rules / pattern vault)
- Workflow : risque accumulation (pipeline-boris-adapte + Workflow Boris + boris-mai + best-practices + pattern-agentic + vibe-coding + architect-first + harness = 8 notes). Une méta-note de synthèse aidera mais NE PAS dupliquer le contenu — pointer.

### Citations verbatim non capturées à PRIORISER

Top 10 verbatim haut signal absentes du vault et essentielles :

1. Boris London "The default isn't 'I'm going to prompt Claude'—the default is now 'I'm going to have Claude prompt itself.'"
2. Boris London "Routines are a higher order prompt"
3. Lisa Crofoot "Designing for the next version of Cloud, not the current one. Scaffolding that used to help can hold Claude back"
4. Erik Schluntz "In a year or two, demanding to read every line of code will make you the bottleneck"
5. Thariq "Sub agents were made to protect the context of the core agent"
6. Anthropic docs verbatim "Put guardrails in hooks. An instruction like 'never edit `.env`' in CLAUDE.md or a skill is a request, not a guarantee"
7. Anthropic docs "MCP connects Claude to data; Skills teach Claude what to do with that data"
8. Hashimoto "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again"
9. Karpathy "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase"
10. Karpathy "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping"

Ces verbatim sont la matière première à intégrer dans les notes RÉÉCRITES.

---

## Liens

- [[recherche-youtube-talks]] — sources YouTube/talks
- [[recherche-blog-docs-anthropic]] — sources blog/docs officielles
- [[recherche-x-twitter-leaders]] — sources X/Twitter
- [[recherche-github-karpathy-leaders]] — sources GitHub
- [[verif-claudemd-taille-officielle]] — vérification 200L
- [[recherche-youtube-watch-vibe-coding]] — transcripts profonds (38k mots)
- [[recherche-karpathy-vault-canonique]] — Karpathy verbatim
- [[recherche-mcp-vs-skills-cli]] — MCP vs Skills doctrine
- [[skills-guide]] · [[agents-orchestration]] · [[hooks-guide]] · [[claudemd-guide]] · [[pipeline-boris-adapte-neoteem]] · [[audit-claude-folder-pattern]] · [[karpathy-llm-wiki-pattern]] · [[mcp-vs-cli-vs-skills]] · [[harness-engineering]]
