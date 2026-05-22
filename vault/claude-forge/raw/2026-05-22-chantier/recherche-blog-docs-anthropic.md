---
titre: "Recherche web — Blog Anthropic + docs officielles mai 2026"
resume: "Synthèse des sources officielles Anthropic (blog, engineering, docs.claude.com) sur le workflow Claude Code — doctrine hooks/skills/agents/CLAUDE.md, sweet spots, anti-patterns, patterns Boris/Cat Wu."
aliases: ["recherche blog anthropic", "docs claude code officielles", "doctrine anthropic workflow", "anthropic engineering claude code"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/synthese", "#domaine/claude-code", "#domaine/anthropic"]
---

# Recherche — Blog Anthropic + docs officielles (mai 2026)

> Mission : capturer le contenu écrit officiel Anthropic sur le workflow Claude Code pour alimenter 6 notes canoniques.
> Sources prioritaires : **docs.claude.com / code.claude.com / claude.com/blog / anthropic.com/engineering / anthropic.com/research**.

## Carte des sources

| # | Source | URL | Date | Auteurs |
|---|---|---|---|---|
| 1 | Best practices for Claude Code | https://code.claude.com/docs/en/best-practices | (page vivante, redir depuis anthropic.com/engineering) | équipe Claude Code |
| 2 | Extend Claude Code — Match features to your goal | https://code.claude.com/docs/en/features-overview | page vivante docs | équipe docs |
| 3 | Automate workflows with hooks | https://code.claude.com/docs/en/hooks-guide | page vivante docs | équipe docs |
| 4 | Effective harnesses for long-running agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | **2025-11-26** | Justin Young |
| 5 | Building Effective Agents (research) | https://www.anthropic.com/research/building-effective-agents | **2024-12-19** | Erik Schluntz, Barry Zhang |
| 6 | Introducing Agent Skills (blog) | https://claude.com/blog/skills | **2025-10-16**, MAJ 2025-12-18 | non listés |
| 7 | Equipping agents for the real world with Agent Skills (engineering) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | **2025-10-16** | Barry Zhang, Keith Lazuka, Mahesh Murag |
| 8 | How Anthropic teams use Claude Code | https://claude.com/blog/how-anthropic-teams-use-claude-code | **2025-07-24** | non listés |
| 9 | Writing effective tools for AI agents | https://www.anthropic.com/engineering/writing-effective-tools-for-agents | **2025-09-11** | Ken Aizawa et al. |

> ⚠️ Notes importantes :
> - `anthropic.com/engineering/claude-code-best-practices` redirige désormais vers `code.claude.com/docs/en/best-practices` (page vivante, sans signature ni date). Le contenu est la version canonique 2026.
> - `docs.claude.com/en/release-notes/claude-code` redirige vers le CHANGELOG GitHub `anthropics/claude-code` (non-fetchable directement, déjà capitalisé via `cc-news`).
> - Pas trouvé : article séparé "How we use Claude Code at Anthropic" co-signé Cat Wu/Boris Cherny. Les seules formes officielles sont le blog `how-anthropic-teams-use-claude-code` (juillet 2025) + le PDF interne `58284b19e702b49db9302d5b6f135ad8871e7658.pdf` (How Anthropic teams use Claude Code).

---

## 1. Best practices for Claude Code — `code.claude.com/docs/en/best-practices`

Page canonique 2026 (redirigée depuis anthropic.com/engineering). Structure : Context → Verify → Plan/Code/Commit → Configure env → Communicate → Manage session → Automate → Failure patterns.

### Doctrine fondatrice

> "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

### Sweet spots (verbatim)

- **CLAUDE.md** : "Keep it concise. For each line, ask: *Would removing this cause Claude to make mistakes?* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" + ailleurs : **"Keep CLAUDE.md under 200 lines."**
- **Plan mode** : "If you could describe the diff in one sentence, skip the plan."
- **Verification** : "Include tests, screenshots, or expected outputs so Claude can check itself. **This is the single highest-leverage thing you can do.**"

### CLAUDE.md — INCLURE vs EXCLURE (tableau verbatim)

| ✅ Include | ❌ Exclude |
|---|---|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

### Doctrine hooks vs CLAUDE.md (verbatim)

> "Use hooks for actions that must happen every time with zero exceptions. Hooks run scripts automatically at specific points in Claude's workflow. **Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens.**"

### Sub-agents — quand

> "Subagents run in their own context with their own set of allowed tools. They're useful for tasks that read many files or need specialized focus without cluttering your main conversation."
> "Since context is your fundamental constraint, **subagents are one of the most powerful tools available**."

### Anti-patterns OFFICIELS (les 5 "Common failure patterns")

1. **The kitchen sink session** — sessions fourre-tout. Fix : `/clear` entre tâches non liées.
2. **Correcting over and over** — après 2 corrections échouées : `/clear` + nouveau prompt.
3. **The over-specified CLAUDE.md** — > "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise." Fix : "Ruthlessly prune. If Claude already does something correctly without the instruction, **delete it or convert it to a hook**."
4. **The trust-then-verify gap** — code plausible mais ne gère pas les edge cases. Fix : "If you can't verify it, don't ship it."
5. **The infinite exploration** — "investigate" sans scope. Fix : scoper ou utiliser un subagent.

### Patterns d'automation

- **Non-interactive** : `claude -p "prompt"` pour CI/scripts.
- **Worktrees** + Desktop app + Web + Agent teams pour parallélisation.
- **Writer/Reviewer** explicite : un Claude écrit, un autre review (fresh context bias-free).
- **Fan out** : boucle bash `for file in $(cat files.txt); do claude -p "..."; done` avec `--allowedTools` scopé.
- **Auto mode** : `claude --permission-mode auto -p "fix all lint errors"`.

### Liens secondaires
- `/en/how-claude-code-works` · `/en/context-window` · `/en/permission-modes` · `/en/sandboxing` · `/en/hooks-guide` · `/en/skills` · `/en/sub-agents` · `/en/plugins` · `/en/agent-teams` · `/en/checkpointing` · `/en/headless`

---

## 2. Extend Claude Code — Match features to your goal — `code.claude.com/docs/en/features-overview`

**LA PAGE DE DOCTRINE.** Tableau central de décision + tableau "Build your setup over time".

### Onglet "CLAUDE.md vs Skill" — règle de pouce

> **"Rule of thumb: Keep CLAUDE.md under 200 lines. If it's growing, move reference content to skills or split into `.claude/rules/` files."**

| Aspect | CLAUDE.md | Skill |
|---|---|---|
| Loads | Every session, automatically | On demand |
| Can trigger workflows | No | Yes, with `/<name>` |
| Best for | "Always do X" rules | Reference material, invocable workflows |

### Onglet "CLAUDE.md vs Rules vs Skills"

| Aspect | CLAUDE.md | `.claude/rules/` | Skill |
|---|---|---|---|
| Loads | Every session | Every session, or when matching files opened | On demand |
| Scope | Whole project | Path-scoped via `paths` frontmatter | Task-specific |

> "Use rules to keep CLAUDE.md focused. Rules with `paths` frontmatter only load when Claude works with matching files, saving context."

### Onglet "Hook vs Skill" — frontière de doctrine

> **"Put guardrails in hooks. An instruction like 'never edit `.env`' in CLAUDE.md or a skill is a request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement. If a rule must hold every time, make it a hook rather than a prompt instruction."**

> "Hook output lands in context. A `PostToolUse` hook that runs your linter feeds results back as text Claude reads; a `/fix-lint` skill tells Claude how to resolve them."

### Onglet "Skill vs Subagent"

> "Skills are reusable content you can load into any context. Subagents are isolated workers that run separately from your main conversation."
> "They can combine. A subagent can preload specific skills (`skills:` field). A skill can run in isolated context using `context: fork`."

### Onglet "Subagent vs Agent team"

> "Transition point: If you're running parallel subagents but hitting context limits, or if your subagents need to communicate with each other, agent teams are the natural next step."

### Tableau "Build your setup over time" (verbatim)

| Trigger | Add |
|---|---|
| Claude gets a convention or command wrong twice | Add it to CLAUDE.md |
| You keep typing the same prompt to start a task | Save it as a user-invocable skill |
| You paste the same playbook for the third time | Capture it as a skill |
| You keep copying data from a browser tab Claude can't see | Connect that system as an MCP server |
| Claude reads many files to find where a symbol is defined | Install a code intelligence plugin |
| A side task floods your conversation with output | Route it through a subagent |
| You want something to happen every time without asking | Write a hook |
| A second repository needs the same setup | Package it as a plugin |

### Context costs (tableau verbatim)

| Feature | When loads | Context cost |
|---|---|---|
| CLAUDE.md | Session start | Every request |
| Skills | Session start (description) + when used (full) | Low (descriptions) |
| MCP | Session start (names) + on demand (schemas) | Low |
| Subagents | When spawned | Isolated |
| Hooks | On trigger | Zero (unless returns output) |

### Layering / priorité

- **CLAUDE.md** : additif (tous les niveaux contribuent).
- **Skills/subagents** : override par nom (managed > user > project ; subagents : managed > CLI flag > project > user > plugin).
- **MCP** : local > project > user.
- **Hooks** : merge (tous fire).

---

## 3. Hooks guide — `code.claude.com/docs/en/hooks-guide`

### Doctrine deterministe (verbatim)

> "Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. They provide **deterministic control** over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them."

### 5 types de handlers

- `"type": "command"` — shell command (le plus courant)
- `"type": "http"` — POST event data to URL
- `"type": "mcp_tool"` — call tool on connected MCP server
- `"type": "prompt"` — single-turn LLM evaluation
- `"type": "agent"` — multi-turn verification, spawn subagent (60s timeout, 50 tool-use turns)

### Quand un hook vs un skill

> "For decisions that require judgment rather than deterministic rules, you can also use prompt-based hooks or agent-based hooks that use a Claude model to evaluate conditions."

### Frontière (rappel features-overview)

> "If a rule must hold every time, make it a hook rather than a prompt instruction."

---

## 4. Effective harnesses for long-running agents — Justin Young, 26 nov 2025

Pour les agents long-running (multi-session). Pose la doctrine **two-agent architecture** + **clean state**.

### Failure modes officiels

1. Agent attempts to one-shot, exhausts context mid-implementation.
2. Later agent instance surveys partial progress and **"declares the job done"** prématurément.

### Architecture deux agents

- **Initializer Agent** (1ère session) : scaffold env (`init.sh`, `claude-progress.txt`, `feature_list.json`, git baseline).
- **Coding Agent** (sessions suivantes) : incrémental, clean state à la fin.

Distinction : **uniquement par leur user prompt initial.** System prompt et tools identiques.

### Artefacts d'environnement

| Artefact | Rôle |
|---|---|
| `init.sh` | Démarrer dev server fiablement |
| `claude-progress.txt` | Log des features done |
| `feature_list.json` | JSON breakdown, `"passes": false` au départ |
| Commit git initial | Baseline recoverable |

> JSON > Markdown : "the model is less likely to inappropriately overwrite it."
> Tests : "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

### Doctrine clean state

> "the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages"

### Question multi-agent ouverte

> "it's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture"

### Liens
- `github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding`
- Claude Agent SDK : `platform.claude.com/docs/en/agent-sdk/overview`

---

## 5. Building Effective Agents — Erik Schluntz & Barry Zhang, 19 déc 2024

Paper fondateur — toujours référencé en 2026. **Le seul vrai paper** ; pas de version "v2".

### Distinction workflows vs agents (verbatim)

- **Workflows** : "systems where LLMs and tools are orchestrated through predefined code paths"
- **Agents** : "systems where LLMs dynamically direct their own processes and tool usage"

### 5 patterns (canonique)

1. **Prompt Chaining** — séquentiel avec gates.
2. **Routing** — classifier puis dispatch spécialisé.
3. **Parallelization** — Sectioning (subtasks indépendantes) ou Voting (même tâche N fois).
4. **Orchestrator-Workers** — central LLM décompose dynamiquement (≠ parallelization car subtasks NON pré-définies).
5. **Evaluator-Optimizer** — generator + critic en boucle.

### Doctrine framework

> "many patterns can be implemented in a few lines of code"
> "incorrect assumptions about what's under the hood are a common source of customer error"

Frameworks cités : Claude Agent SDK, Strands Agents SDK (AWS), Rivet, Vellum.

### 3 principes core

1. **Simplicity**
2. **Transparency** — show planning steps explicitly
3. **ACI as careful as HCI** — documentation + tests des tools

### Anti-patterns explicites

- "add multi-step agentic systems only when simpler solutions fall short"
- Skipping evaluation
- Tools poorly documented
- Relative filepaths (cited SWE-bench fix : absolute paths éliminé les erreurs)

---

## 6. Skills (blog) — `claude.com/blog/skills` — 16 oct 2025 (MAJ 18 déc 2025)

Annonce produit. 4 propriétés clés des Skills :

- **Composable** — stack auto-coordonné
- **Portable** — "Build once, use across Claude apps, Claude Code, and API."
- **Efficient** — only loads what's needed
- **Powerful** — peut inclure "executable code for tasks where traditional programming is more reliable than token generation"

### Liens canoniques
- Engineering deep-dive : voir #7
- Open standard : `agentskills.io`
- Exemples : `github.com/anthropics/skills`

---

## 7. Equipping agents for the real world with Agent Skills — Barry Zhang / Keith Lazuka / Mahesh Murag, 16 oct 2025

LE post engineering canonique sur **progressive disclosure**.

### 3 niveaux de progressive disclosure (verbatim)

> "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix"

- **Level 1** : Skill `name` + `description` pré-chargés dans system prompt (juste assez pour déclencher la pertinence)
- **Level 2** : Full `SKILL.md` body chargé quand Claude juge applicable
- **Level 3+** : Fichiers bundlés additionnels (`reference.md`, `forms.md`...) chargés seulement quand le sous-scénario survient

> Context bundlé dans un skill est "effectively unbounded" parce que l'agent lit les fichiers sélectivement.

### Structure SKILL.md

- YAML frontmatter OBLIGATOIRE : `name`, `description`
- Body : instructions, refs à d'autres fichiers, scripts
- Fichiers additionnels dans le même dossier

### Anti-patterns implicites

| Anti-pattern | Alternative |
|---|---|
| Un agent monolithique par use case | Compose skills réutilisables |
| Tout charger upfront | Progressive disclosure / split |
| Faire faire à LLM du déterministe (sorting) | Bundler des scripts exécutables |
| Deviner le contexte | Itérer avec Claude, ask self-reflect on failures |
| Contextes mutuellement exclusifs dans un fichier | Séparer en fichiers |

### Skills vs MCP

> Skills "complement Model Context Protocol (MCP) servers by teaching agents more complex workflows that involve external tools."

---

## 8. How Anthropic teams use Claude Code — 24 juillet 2025

**Article daté juillet 2025** — pré-Skills (oct 2025), pré-features 2026. Source historique pour les usages par équipe.

### Équipes et usages

- **Security Engineering** : workflow "design doc → janky code → refactor → give up on tests" remplacé par TDD guidé. Stack traces + docs pour trace control flow lors d'incidents — résolution **~3x plus rapide**. Runbooks markdown générés depuis docs multiples.
- **Data Infrastructure** : screenshots dashboard pendant outage Kubernetes → Claude guide "menu-by-menu through Google Cloud's UI". Identifie pod IP exhaustion. **Nouveaux : feed l'entier codebase dans CLAUDE.md** pour mapper upstream pipelines.
- **Inference Team** : non-ML members → research time **cut ~80%**. Traduit tests vers langages inconnus (Rust).
- **Product Engineering** : Claude = "first stop" pour toute tâche prog.
- **Product Design** : Figma → autonomous loops (code + tests + iter). A construit **"Vim key bindings for itself with minimal human review"**.
- **Growth Marketing** : workflow agentique avec **"two specialized sub-agents"** pour CSVs → ad copy variations dans limites de caractères. Figma plugin générant **"up to 100 ad variations"**.
- **Legal Team** : "phone tree" pour router vers le bon lawyer interne — sans dev resources.

### Pas mentionnés dans cet article (gap)

- Hooks, Skills nommés, parallel sessions, worktrees — **rien** dans l'article (antérieur à ces features).

---

## 9. Writing effective tools for AI agents — Ken Aizawa et al., 11 sept 2025

### Doctrine

> Tools représentent "a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."
> "More tools don't always lead to better outcomes" · "Too many tools or overlapping tools can also distract agents"

### 5 principes

1. **Choose tools deliberately** — consolider workflows multi-étapes en un tool (`schedule_event` > `list_users` + `create_event`).
2. **Namespace clearly** — `asana_projects_search`.
3. **Return meaningful context** — pas d'UUIDs cryptiques. Enum `response_format` (`concise`/`detailed`).
4. **Token efficiency** — pagination, filter, truncate. **Claude Code limite à 25 000 tokens par réponse de tool**.
5. **Prompt-engineer descriptions** — décrire "as you would to a new hire".

### Anti-patterns

| Anti-pattern | Mieux |
|---|---|
| `list_contacts` brute-force | `search_contacts` targeted |
| Generic `read_logs` | `search_logs` returning relevant lines |
| Returning UUIDs | Resolve to semantic names |
| Opaque error codes | Actionable, example-driven |

---

## Synthèse — Doctrine 2026 consolidée

### Frontière hook / skill / agent / CLAUDE.md / rules (consensus officiel)

| Besoin | Outil canonique | Pourquoi |
|---|---|---|
| Règle qui doit tenir 100% du temps | **Hook** (PreToolUse blocking) | Advisory ≠ guarantee. "Make it a hook rather than a prompt instruction." |
| Convention à toujours rappeler | **CLAUDE.md** (< 200 lignes) | Loaded every session, additive |
| Convention scopée à un path | **`.claude/rules/`** avec `paths:` frontmatter | Loaded only when matching files |
| Reference material / playbook | **Skill** | On-demand, progressive disclosure |
| Workflow `/<name>` invocable | **Skill** (avec optional `disable-model-invocation: true`) | Trigger explicite |
| Isoler un side-task lourd | **Subagent** | Context isolé, summary only |
| 2+ workers qui doivent communiquer | **Agent team** | P2P messaging |
| Connexion à service externe | **MCP** | Protocol standard |
| Bundle réutilisable cross-repo | **Plugin** | Package skills + hooks + agents + MCP |

### Sweet spots officiels (citations)

- **CLAUDE.md** : **< 200 lignes** (règle de pouce explicite docs)
- **Tool response** : **25 000 tokens max** dans Claude Code (par défaut)
- **Skills re-attached après compaction** : 5 000 tokens chacun, budget combiné **25 000 tokens**
- **Agent hook** : timeout 60s, jusqu'à **50 tool-use turns**

### Anti-patterns officiels (consensus)

1. CLAUDE.md trop long → règles ignorées (doc + Boris IRL)
2. Kitchen sink session → `/clear` between tâches
3. Trust-then-verify gap → "If you can't verify it, don't ship it"
4. Frameworks avant patterns simples → "few lines of code first"
5. Tools poorly documented → "as much prompt engineering as your overall prompts"
6. Skills monolithiques upfront → progressive disclosure

### Évolutions clés mai 2026 vs avant

- **Skills GA** (oct 2025) — devient l'extension la plus flexible, supplante les "custom agents per use case".
- **Hooks** : 5 types de handlers (command/http/mcp_tool/prompt/agent) — agent hooks sont nouveaux (multi-turn).
- **Agent teams** : nouveau, encore expérimental, default disabled.
- **Auto mode** (`--permission-mode auto`) : classifier model qui bloque scope escalation / unknown infra / hostile-content. Remplace `--dangerously-skip-permissions` comme posture par défaut.
- **Plugins + marketplaces** : packaging officiel, namespacing skills (`/plugin:command`).
- **`.claude/rules/` avec `paths:` frontmatter** : reconnu officiellement comme alternative légitime à CLAUDE.md (réf : "split into `.claude/rules/` files").

### Confirmations des choix forge

- `.claude/rules/` existe officiellement dans la doc ✅
- Hooks > Rules pour enforcement absolu ✅
- Sweet spot CLAUDE.md ~100-200L ✅ (forge dit 100, docs disent 200)
- Subagents pour context isolation ✅
- Skills avec progressive disclosure (references/) ✅
- Worktrees pour parallel sessions ✅

### Sources clés sur Boris/Cat Wu (hors blog officiel)

L'article co-signé spécifique n'existe pas. Les sources les plus officielles :
- PDF interne Anthropic : `www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf` (How Anthropic teams use Claude Code)
- Webinar : `anthropic.com/webinars/claude-code-advanced-patterns`
- Webinar Boris : `anthropic.com/webinars/claude-code-for-financial-services-a-session-with-the-creator-boris-cherny`

Sources tierces de qualité (interviews directes) : Lenny's Newsletter (Boris), Pragmatic Engineer (Gergely Orosz), Every.to podcast, howborisusesclaudecode.com (fan site qui cite Boris).

---

## Sources manquantes / gaps

- ❌ Page CLAUDE.md officielle séparée : pas trouvée. Le contenu canonique vit dans `code.claude.com/docs/en/memory` (référencée 6× mais pas fetchée ici — exhaustive ailleurs).
- ❌ Changelog Claude Code v2.1.x avril-mai 2026 : redirige vers GitHub (déjà capitalisé via `cc-news`).
- ❌ Pas d'article officiel co-signé Cat Wu + Boris Cherny sur "comment ils utilisent CC".
- ❌ "Erik Schluntz, Amanda Askell" en co-auteurs : seul Erik Schluntz est co-auteur, avec Barry Zhang (pas Amanda Askell).

## Liens hyperlinks (récap)

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Extend Claude Code — features overview](https://code.claude.com/docs/en/features-overview)
- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Introducing Agent Skills (blog)](https://claude.com/blog/skills)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code)
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-effective-tools-for-agents)
- [Anthropic Cookbook — agents patterns](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
- [GitHub anthropics/skills](https://github.com/anthropics/skills)
- [agentskills.io](https://agentskills.io)

Voir aussi : [[reference_boris_thariq_bestpractices]], [[doctrine-vs-enforcement-22mai]], [[pipeline-boris-adapte-neoteem]].
