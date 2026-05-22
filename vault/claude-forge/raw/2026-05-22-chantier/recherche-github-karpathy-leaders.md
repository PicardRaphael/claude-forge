---
titre: "Recherche web — GitHub Anthropic + Karpathy + leaders tech reconnus"
resume: "Cartographie des configs Claude Code publiques (Anthropic, Karpathy, Hashimoto, Fowler, Willison) et des patterns récurrents — harness engineering, LLM Wiki, AGENTS.md par compounding"
aliases: ["recherche github anthropic", "karpathy software 3.0", "claude code leaders tech", "harness engineering sources", "anthropic claude pour legal"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/synthese", "#domaine/claude-code", "#domaine/agents", "#domaine/harness-engineering"]
---

# Recherche — Claude Code en pratique chez Anthropic + leaders reconnus

Mission : capturer **sources primaires** (GitHub publics, blogs auteurs reconnus) qui montrent COMMENT Claude Code est utilisé. Pas de blogs aggrégateurs. Focus : `.claude/` exposé, `CLAUDE.md`/`AGENTS.md` publiés, patterns récurrents.

---

## 1. Anthropic — `.claude/` exposés publiquement

### 1.1 `anthropics/claude-code` (repo principal)

- **URL** : https://github.com/anthropics/claude-code
- **`.claude/` exposé** : OUI — contient `.claude/commands/` avec **3 slash commands** seulement
  - `commit-push-pr.md`
  - `dedupe.md`
  - `triage-issue.md`
- **`CLAUDE.md` racine** : NON
- **`settings.json`** : non visible
- **Pattern** : Anthropic eux-mêmes utilisent une config **minimaliste** sur le repo Claude Code — 3 commandes opérationnelles, pas de CLAUDE.md, pas d'agents/skills exposés
- **Source** : https://github.com/anthropics/claude-code/tree/main/.claude/commands

**Lecture clé** : Anthropic ne fait PAS de "config porn". 3 commandes ciblées, pas de méta-framework. Contraste fort avec forge (60+ skills/agents/hooks).

### 1.2 `anthropics/claude-for-legal` — CLAUDE.md COMPLET publié

- **URL** : https://github.com/anthropics/claude-for-legal/blob/main/CLAUDE.md
- **Taille** : 130 lignes, ~5.89 KB (sweet spot 100-300L confirmé)
- **5 sections** : Layout · Validation · Conventions · Cookbooks · Things to Leave Alone

**Structure observée** :
- H2 sections, H3 subsections — pas de nesting plus profond
- Layout = pseudo-tree en fenced code block avec commentaires inline `#`
- Validation = mix shell block + bullet list invariants (I1-I11 nommés)
- Conventions = 6 sous-sections, **2-5 phrases chacune**, ton prescriptif ("Don't fix it")
- Cookbooks = numbered list, règles lint-enforced
- **"Things to Leave Alone"** = bullets de non-bugs intentionnels, ton **rassurant** ("not a bug", "probably intentional")

**Patterns techniques notables** :
- Validation enforcement : `claude plugin validate` + `python3 scripts/lint-tool-scope.py`
- Invariants nommés I1-I11 avec descriptions courtes
- Regex naming : `^[a-z0-9][a-z0-9-]{1,63}$`
- Frontmatter obligatoire : `name`+`description` pour agents, `description` pour skills/commands
- **Cookbook tool rule** : *"Orchestrator = local-only tools; MCP/write tools = subagent leaves only"* — règle de séparation des privilèges
- *"Skill references in prose must be exact directory names — short forms are dead commands"*

**Style** : em-dashes (—) extensifs, `_italics_` pour asides, pas de TODO — les imperfections sont normalisées explicitement.

### 1.3 `anthropics/claude-plugins-official` — 36 plugins officiels

- **URL** : https://github.com/anthropics/claude-plugins-official
- **Structure double** : `/plugins` (Anthropic interne) + `/external_plugins` (communauté curé)
- **36 plugins internes**. Catégories clés :
  - **12 LSP** : clangd, csharp, gopls, jdtls, kotlin, lua, php, pyright, ruby, rust-analyzer, swift, typescript
  - **Dev tools** : `agent-sdk-dev`, `mcp-server-dev`, `plugin-dev`, `feature-dev`
  - **Quality** : `code-review`, `code-simplifier`, `code-modernization`, `pr-review-toolkit`
  - **Méta** : `skill-creator`, `claude-md-management`, `hookify`, `claude-code-setup`
  - **Style** : `explanatory-output-style`, `learning-output-style`
  - **Spéciaux** : `ralph-loop`, `math-olympiad`, `cwc-makers`, `playground`, `session-report`, `mcp-tunnels`

**Structure standard d'un plugin** (canonique Anthropic) :
```
plugin-name/
├── .claude-plugin/plugin.json   # REQUIS, seul artefact obligatoire
├── .mcp.json                    # optionnel
├── commands/                    # optionnel
├── agents/                      # optionnel
├── skills/                      # optionnel
└── README.md
```

**Skill `skill-creator` (référence canonique)** :
- Workflow : capture intent → draft → run test cases (with-skill ET baseline en parallèle) → eval via `generate_review.py` → improve
- *"Description field drives triggering — make it a little bit pushy"* → confirme la posture "trigger pushy" déjà adoptée dans forge
- SKILL.md < 500 lignes (cohérent forge)
- Scripts `package_skill.py` → `.skill` file
- Baseline = no skill (nouveau) OU version précédente (amélioration)

**Source** : https://github.com/anthropics/claude-plugins-official/tree/main/plugins

---

## 2. Karpathy — LLM Wiki + agentic engineering

### 2.1 LLM Wiki (gist canonique)

- **URL** : https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Publié** : 3-4 avril 2026 sur X, gist le lendemain
- **Reach** : 21M vues sur X
- **Karpathy a rejoint Anthropic** (annonce mai 2026) — alignement direct avec Claude Code

**Architecture 3-couches (canonique)** :

| Layer | Rôle | Owner |
|-------|------|-------|
| **Raw Sources** | Immutables : PDFs, articles, notes | Humain |
| **Wiki** | Markdown généré : summaries, entity pages, concept pages, overview, synthesis | LLM |
| **Schema** | Config : `CLAUDE.md` / `AGENTS.md` qui dicte conventions et workflows | Co-évolution humain+LLM |

**3 opérations core** :
- **Ingest** : LLM lit source → discute avec user → écrit summary → met à jour index → met à jour entity/concept pages (10-15 pages touchées) → append log
- **Query** : recherche pages → lecture → synthèse avec citations → réponse peut être markdown/table/slides (Marp)/chart (matplotlib)
- **Lint** : santé périodique : contradictions, orphan pages, claims stales, cross-refs manquantes

**Fichiers navigation** :
- `index.md` — catalogue contenu, mis à jour à chaque ingest, sert de **RAG-replacement à moyenne échelle**
- `log.md` — append-only chronologique, parseable Unix-tools via headings consistants

**Scale prouvée** : 100 articles, 400K mots — LLM navigue efficacement via index+summaries.

**Citation centrale** :
> "The LLM handles the bookkeeping — cross-referencing, consistency checks, updates — at near-zero cost, letting humans focus on sourcing, questioning, synthesis."

**Outillage cité par Karpathy** : Obsidian (IDE + graph view), Obsidian Web Clipper, Marp (slides), Dataview (YAML queries), qmd (BM25+vector local), Git.

**ALIGNEMENT FORGE** : forge-brain = implémentation LLM Wiki avant l'heure. Vault Obsidian, schema = CLAUDE.md + rules, ingest = capitalisation cc-news/recherche, query = MCP forge-brain, log = CHANGELOG.md vault.

### 2.2 nanochat + autoresearch (octobre 2025 + mars 2026)

- **nanochat** : ChatGPT clone 8K lignes, $73 sur 8×H100 / 3h, capstone LLM101n Eureka Labs
- **autoresearch** : agents IA qui font ML expérimentation overnight, 66K stars en 1 mois, "Karpathy Loop" (Fortune). 20 améliorations stackables trouvées sur nanochat → 11% speedup "Time to GPT-2"

---

## 3. Mitchell Hashimoto — origine "Harness Engineering"

### 3.1 Blog post fondateur

- **URL** : https://mitchellh.com/writing/my-ai-adoption-journey
- **Date** : 5 février 2026
- **Crédit** : a nommé "harness engineering", repris par Fowler, OpenAI, Mollick dans les 2 semaines

**Définition canonique** (quote verbatim) :
> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

**Composants harness cités** :
- `AGENTS.md` — plain-text implicit prompting, **chaque ligne = un bad behavior observé**
- Scripts pour screenshots
- Filtered test runners
- Outils pairés avec updates AGENTS.md pour que l'agent les connaisse

**3 quotes verbatim** :
> "Agents are much more efficient when they produce the right result the first time"

> "I'm making an earnest effort whenever I see an agent do a Bad Thing to prevent it from ever doing that bad thing again."

> "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all."

### 3.2 Ghostty `AGENTS.md` — référence vivante

- **URL** : https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md
- **Repo** : terminal Ghostty (créateur = Hashimoto)
- **Contenu type observé** :
  - Build commands ciblées : `zig build`, flag macOS speedup `-Demit-macos-app=false`
  - Tests : `zig build test`, **préférence `-Dtest-filter`** (suite full lente)
  - Structure : `src/` core Zig, `macos/` Swift, `src/apprt/gtk` GTK
  - libghostty-vt : *C enums must include `a _MAX_VALUE = GHOSTTY_ENUM_MAX_VALUE sentinel`*
  - Formatters : `zig fmt .`, SwiftLint `--strict --fix`, Prettier
  - **Règles interdictions** explicites : *"Never create an issue"* et *"Never create a PR"*

**Pattern clé** : interdictions explicites = enforcement par prompt (Hashimoto n'a pas de hooks bloquants à ce stade). Forge a déjà dépassé ce stade (hooks exit 2). 

**ALIGNEMENT FORGE** : règle Jarvis "workaround ≥ 2 fois = bug" + memory `recurring-meta-anti-pattern` = MÊME PHILOSOPHIE que Hashimoto (compounding errors → harness).

---

## 4. Martin Fowler / Birgitta Böckeler — taxonomie Guides+Sensors

### 4.1 Article

- **URL** : https://martinfowler.com/articles/harness-engineering.html
- **Auteur** : Birgitta Böckeler (Thoughtworks Distinguished Engineer)
- **Mémo initial** : 17 février 2026 · **Article complet** : 2 avril 2026

### 4.2 Définition harness

> *"Agent = Model + Harness"* (formule Hashimoto reprise)

Pour coding agents : **user-built outer harness** sit outside l'inner harness intégré (Claude Code, Codex). Double objectif :
1. Augmenter probabilité de bonne sortie au premier coup
2. Fournir feedback loops self-correcting avant review humain

### 4.3 Taxonomie Guides vs Sensors

| Dimension | Type | Exécution | Exemples |
|-----------|------|-----------|----------|
| **Guides** (feedforward) | Anticipatif | **Computational** | LSP, bootstrap scripts, OpenRewrite codemods |
| **Guides** (feedforward) | Anticipatif | **Inferential** | AGENTS.md, Skills, coding convention docs |
| **Sensors** (feedback) | Corrective | **Computational** | ESLint, ArchUnit, dep-cruiser, mutation testing |
| **Sensors** (feedback) | Corrective | **Inferential** | AI code review agents, architecture review Skills |

**Distinction clé** :
- Computational = déterministe, fast (ms-s)
- Inferential = probabiliste, slower, GPU, mais gère semantic judgment

### 4.4 Quotes verbatim

> "Guides increase the probability that the agent creates good results in the first attempt"

> "Correctness is outside any sensor's remit if the human didn't clearly specify what they wanted."

> "A good harness should not necessarily aim to fully eliminate human input, but to direct it to where our input is most important."

### 4.5 7 recommandations pratiques

1. Combiner feedforward + feedback (ni l'un ni l'autre seul ne suffit)
2. **Shift quality left** : computational sensors rapides (linters, unit tests) avant commit ; inferential sensors lourds (mutation, archi review) en post-integration
3. Prioriser computational sensors d'abord (catch structurel cheap+deterministe)
4. **Ne pas over-trust AI-generated tests** — behavior harness = maillon faible
5. Construire harness templates par topologie service (CRUD API, event processor)
6. Traiter **harnessability comme architectural concern** — strongly typed langs + clear module boundaries → meilleure couverture harness
7. Utiliser agents pour BUILD le harness lui-même (auto-scaffold linters, rules from patterns)

**ALIGNEMENT FORGE** :
- Rules forge = Guides Inferential (AGENTS.md équivalent)
- Hooks Python exit 2 = Sensors Computational (déterministe, fast)
- devils-advocate / code-reviewer agents = Sensors Inferential
- Doctrine "Hooks > Rules" forge = recommandation #3 de Fowler (computational > inferential)

### 4.6 Evidence harness > model

LangChain février 2026, Terminal Bench 2.0 :
- Même modèle, même API : 52.8% → 66.5% via harness changes seuls
- Rank Top 30 → Top 5
- *"No fine-tuning, no model swap, just harness changes"*

---

## 5. Simon Willison

### 5.1 Live blog Code w/ Claude 2026 (6 mai 2026)

- **URL** : https://simonwillison.net/2026/May/6/code-w-claude-2026/

**Patterns observés** :
- **Async multi-session** : Boris (CTO CC) roule N sessions desktop simultanées, switch entre elles
- **Routines** = *"higher-order prompts"* — async PR delivery overnight
- **PR auto-fix loop** : CI trigger → Claude self-prompt → file fixes → *"the person who owns the PR is never going to see a red X"*
- **Advisor pattern (Sonnet→Opus)** : smaller model call Opus pour judgment — un client a divisé coûts par 5
- *"Design for the next model"* (Boris) — construire ce qui marche presque, parier sur upgrade modèle proche
- *"Automated evals, simple scaffolding, imaginative model use"* (Dianne, Head of Product Research)

**Annonces majeures** :
| Annonce | Status |
|---------|--------|
| Multi-agent orchestration (Managed Agents) | Beta publique |
| Outcomes (success criteria loop) | Beta publique |
| Dreaming (session introspection + memory) | Research preview |
| Routines | Available |
| CI auto-fix | Available |
| Rate limit Claude Code 5h doublé | Live (Pro/Max/Enterprise) |
| API volume | 17× year-on-year |
| SpaceX Colossus capacity deal | Annoncé |
| Pas de nouveau modèle | Confirmé — event = tooling/platform |

**Quote Boris** :
> "Everything we are seeing today still feels magical to me, and I work on Claude Code every day."

**Mercado Libre** : target 90% autonomous coding by Q3 2026.

### 5.2 Agentic Engineering Patterns Guide

- **URL** : https://simonwillison.net/guides/agentic-engineering-patterns/
- **Format** : chapter-shaped patterns, inspiré Gang of Four (1994)
- **12 chapitres** à mi-mars 2026
- **2 principes fondateurs** :
  1. *"Code is now inexpensive"* — focus dev shift vers décisions architecturales
  2. *"Preserve domain expertise"* — devs gardent le knowledge work
- **Red/Green TDD** adapté agents
- Tag `ai-assisted-programming` : 345+ posts

**Quote Willison sur Skills** :
> "Claude Skills are awesome, and maybe a bigger deal than MCP"

Distinction : *"Skills aren't about hiding context like subagents do, nor prompts you explicitly invoke like slash commands — Skills are about discovery and determinism: Claude figures out when to use them."*

---

## 6. Écosystème tech leaders publiant des Skills officielles

### 6.1 `VoltAgent/awesome-agent-skills` (curation officielle)

- **URL** : https://github.com/VoltAgent/awesome-agent-skills
- **Description** : 1000+ skills, compatible Claude Code / Codex / Gemini CLI / Cursor / Antigravity

**Top 20 skills officielles par org** :

| Org | Skill | Rôle |
|-----|-------|------|
| Stripe | `stripe-best-practices` | Patterns intégration Stripe |
| Stripe | `upgrade-stripe` | Migration SDK + API versions |
| Vercel | `next-best-practices` | Patterns Next.js |
| Vercel | `react-best-practices` | Patterns React |
| Vercel | `next-upgrade` | Migration Next versions |
| Cloudflare | `workers-best-practices` | Review Workers code |
| Cloudflare | `durable-objects` | Stateful coordination RPC+SQLite+WS |
| Cloudflare | `agents-sdk` | Build stateful AI agents (scheduling + MCP) |
| Cloudflare | `wrangler` | Deploy Workers/KV/R2/D1/Queues |
| Sentry | `sentry-workflow` | End-to-end fix production issues |
| Sentry | `sentry-fix-issues` | Fix via stack traces (MCP) |
| Sentry | `sentry-nextjs-sdk` | SDK setup Next.js App+Pages |
| Sentry | `sentry-code-review` | Review avec context Sentry |
| OpenAI | `linear` | Gestion Linear issues/projects |
| OpenAI | `figma-implement-design` | Figma → code production |
| OpenAI | `security-threat-model` | Threat models repo-specific |
| HashiCorp | `terraform-style-guide` | Generate HCL canonique |
| HashiCorp | `terraform-test` | Tests `.tftest.hcl` |
| Figma | `figma-implement-design` | Designs → code |
| Netlify | `netlify-cli-and-deploy` | CLI + dev + deploy |

### 6.2 Vercel — `claude-managed-agents-starter`

- **URL** : https://github.com/vercel-labs/claude-managed-agents-starter
- **Install pattern** : `npx skills add anthropics/skills` + `npx skills add vercel/workflow`
- **Extension** : connecter Linear/Jira/internal tools via MCP URLs + OAuth flows
- **CLI `add-skill`** : install skills sur **16 agents en une commande**
- **deepsec** : *"open-source security harness from vercel-labs that audits your repo with Claude Opus"*
- Vercel Agent **lit nativement CLAUDE.md** et répond sur PR tagué

### 6.3 Cloudflare

- **URL** : https://developers.cloudflare.com/agent-setup/claude-code/
- Page docs dédiée Claude Code
- 3 axes : Cloudflare Skills, Code Mode API MCP, Domain Specific MCPs

---

## 7. Patterns récurrents (ce que tout le monde fait pareil)

1. **CLAUDE.md / AGENTS.md = source of truth d'instruction** — universel (Anthropic, Hashimoto, Karpathy, Vercel)
2. **Compounding errors** — chaque erreur observée → règle ajoutée. Identique chez Hashimoto (Ghostty AGENTS.md) et forge (memory + Knowledge/erreurs/)
3. **Computational sensors > inferential** — Fowler explicite, Anthropic implicite (hooks Python plugins), forge explicite ("Hooks > Rules")
4. **Skills > prompts hidden** — Anthropic + Willison convergent : Skills = discovery + déterminisme
5. **Multi-agent + delegation** — Anthropic Managed Agents, Vercel, OpenAI, forge agents spécialisés
6. **MCP comme intégration first-class** — universel (Anthropic, Vercel, Cloudflare, Sentry)
7. **Validation/lint pipelines** — `claude plugin validate`, scripts Python lint, ESLint, ArchUnit (Fowler)
8. **CLAUDE.md court, sweet spot 100-300 lignes** — claude-for-legal = 130L, recommandation forge confirmée par observation directe Anthropic
9. **TDD adapté agents** — Willison (Red/Green), forge (test-writer)
10. **Async / overnight / dreaming** — Karpathy (autoresearch), Anthropic (Dreaming, Routines), Hashimoto (engineer one time, agent runs forever)

---

## 8. Divergences (ce qui varie)

| Dimension | Anthropic interne | Hashimoto/Ghostty | Karpathy | Forge |
|-----------|-------------------|-------------------|----------|-------|
| Taille config | Minimaliste (3 commandes claude-code, 130L CLAUDE.md legal) | AGENTS.md unique ciblé | Schema CLAUDE.md léger | Riche (60+ composants, vault) |
| Enforcement | Lint scripts | Prompt interdictions | Aucun (collab humain) | Hooks Python exit 2 |
| Knowledge persistence | Skills + plugins | AGENTS.md compounding | LLM Wiki 3-layer | Vault forge-brain (= LLM Wiki implémenté) |
| Multi-repo | Plugin marketplace | Per-repo | Single wiki | Cross-repo rules + agents |
| Pipeline qualité | feature-dev workflow (architect→explore→review) | Manuel | Ingest/Query/Lint | architect → impl → test → DA → livre |

**Lecture stratégique** : forge est **PLUS structuré** que la moyenne. Pas un défaut — mais à confronter au minimalisme Anthropic. Question ouverte : combien de composants forge sont vraiment utilisés ?

---

## 9. Sources inaccessibles ou non trouvées

- **Steve Yegge** : pas trouvé de publication récente sur Claude Code workflow (peut-être obsolète sur ce vecteur)
- **Sebastian Raschka** : focus reste LLMs from scratch, pas de workflow CC publié spécifique
- **Pieter Levels** : indie hacker mais pas de config CC publique trouvée
- **Cognition Labs / Devin team** : pas de repos `.claude/` publics
- **Addy Osmani** : référencé sur "harness engineering" mais pas de blog primaire trouvé sur usage CC concret
- **Karpathy LLM Wiki interne (100 articles 400K mots)** : NON publié — seulement le gist spec
- **Anthropic interne sur claude-code** : pas de CLAUDE.md exposé, donc partie immergée invisible

---

## 10. Sources canoniques à archiver (par priorité)

### Tier 1 — Anthropic primary

- `anthropics/claude-code` repo : https://github.com/anthropics/claude-code
- `anthropics/claude-for-legal` CLAUDE.md : https://github.com/anthropics/claude-for-legal/blob/main/CLAUDE.md
- `anthropics/claude-plugins-official` : https://github.com/anthropics/claude-plugins-official

### Tier 2 — Leaders fondateurs

- Karpathy LLM Wiki gist : https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Karpathy autoresearch : https://github.com/karpathy/autoresearch
- Hashimoto My AI Adoption Journey : https://mitchellh.com/writing/my-ai-adoption-journey
- Ghostty AGENTS.md : https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md
- Fowler/Böckeler Harness Engineering : https://martinfowler.com/articles/harness-engineering.html

### Tier 3 — Communauté + entreprises

- Willison Live blog Code w/ Claude 2026 : https://simonwillison.net/2026/May/6/code-w-claude-2026/
- Willison Agentic Engineering Patterns : https://simonwillison.net/guides/agentic-engineering-patterns/
- Vercel claude-managed-agents-starter : https://github.com/vercel-labs/claude-managed-agents-starter
- Cloudflare CC docs : https://developers.cloudflare.com/agent-setup/claude-code/
- VoltAgent awesome-agent-skills : https://github.com/VoltAgent/awesome-agent-skills

---

## 11. Implications immédiates pour forge

1. **CLAUDE.md forge actuel ~150L** = aligné avec claude-for-legal Anthropic (130L). Pas de bloat.
2. **Vault forge-brain** = implémentation LLM Wiki Karpathy avant l'heure. **À documenter comme tel** dans une note canonique : forge a anticipé Karpathy.
3. **Hooks > Rules forge** = Fowler "computational > inferential sensors" — alignement théorique confirmé. **Citer Fowler** dans `enforce-not-advise` rule.
4. **Pattern compounding (memory + Knowledge/erreurs/)** = identique Hashimoto Ghostty. **Confirmer** par citation explicite.
5. **Skill-creator workflow (with-skill + baseline parallèle)** = à comparer à `outcomes-test` forge actuel. Potentiel évolution forge.
6. **Minimalisme Anthropic interne** = signal d'alerte : auditer ce qui est VRAIMENT utilisé dans forge vs ornement. Question pour `/forge-review` mensuel.
7. **Skills officielles Stripe/Vercel/Cloudflare/Sentry** = inspiration pour skills neo-* Neoteem. Pattern : `<org>/<domain>-best-practices` + `<org>/<domain>-upgrade`.
8. **Routines + Managed Agents** = next frontier — forge utilise déjà /schedule + Cowork, mais pas Managed Agents.
