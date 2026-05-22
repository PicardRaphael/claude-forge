---
titre: "Recherche web — YouTube + talks vidéo Anthropic mai 2026"
resume: "Synthèse des talks Anthropic (Code with Claude SF/London, AI Ascent, Pragmatic Engineer, Lenny's, Frontend Masters) — workflow réel des équipes Claude Code en mai 2026 : routines, advisor strategy, multi-clotting, dreaming, HTML-over-markdown, vibe coding en prod."
aliases: ["recherche youtube anthropic", "talks code with claude", "code with claude london", "code with claude sf 2026", "talks anthropic mai 2026", "workflow anthropic claude code"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/synthese", "#domaine/claude-code"]
---
    
# Recherche web — YouTube + talks vidéo Anthropic mai 2026

## Scope et méthode

- **Période** : mars-mai 2026, focus Code with Claude SF (6-7 mai) + London (19 mai, il y a 3 jours)
- **Sources** : YouTube (livestream London transcrit via skill `watch`), blogs live (Simon Willison, Chris Ebert, Blake Crosley), interviews (Pragmatic Engineer, Every, Lenny's, ChatPRD), articles couverture (MIT Tech Review, Fortune, InfoQ, TechCrunch, Dotzlaw)
- **Méthode** : 8 WebSearch + 9 WebFetch + 1 transcription YouTube complète (London opening keynote, 6500 mots)
- **Limites** : pas trouvé d'upload individuel des talks London hors keynote (probable publication 7-10 jours post-event sur la playlist Code w/ Claude). Talk Thariq "multi-agent: when to split" Extended SF non encore uploadé séparément ; couvert via [How I AI Lenny's podcast](https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown) et [Vibe Code Camp distilled](https://davidguttman.github.io/every-vibe-code-camp-distilled/14_thariq_shihipar.html).

---

## 1. Code with Claude London — 19 mai 2026

### 1.1. Opening keynote — transcription complète

- **URL** : https://www.youtube.com/watch?v=6amLO7I9xdg (posté 2 jours après l'event)
- **Transcription** : faite via skill `watch`, ~6500 mots, auto-captions EN
- **Speakers** (ordre d'apparition) :
  1. **Boris Cherny** (Head of Claude Code) — intro nostalgique TI-83 + HTML/eBay enfance
  2. **Lisa Crofoot** (research PM) — capability curve, 17 versions Claude, task horizon
  3. **Angela Jiang** + **Katelyn Lesse** (Claude Platform) — advisor strategy + managed agents demo (Counter fictive)
  4. **Cat Wu** (Head of Product Claude Code) — Claude Code surfaces, antfooding
  5. **Boris Cherny** (clôture) — demo Acme Pay, routines, CI autofix

### 1.2. Takeaways HAUT SIGNAL

| # | Insight | Source |
|---|---------|--------|
| 1 | **"The default isn't 'I'm going to prompt Claude'—the default is now 'I'm going to have Claude prompt itself.'"** | Boris, clôture keynote |
| 2 | API volume **+17x YoY** sur Claude platform | Boris, intro |
| 3 | Développeur moyen passe **>20h/semaine** dans Claude Code | Boris, intro |
| 4 | **8 frontier models en 12 mois** (Sonnet 3 → Opus 4.7 + Mythos preview) | Lisa Crofoot |
| 5 | **Spotify** : agent background migre 1000+ PRs/mois en prod, -90% temps migration | Boris, intro |
| 6 | **Mercado Libre** : 23 000 ingénieurs sur Claude Code, 500k PRs reviewés, 9k apps modernisées, objectif **90% coding autonome Q3 2026** | Cat Wu |
| 7 | Anthropic interne : **+200% PRs/ingénieur** après adoption wall-to-wall Claude Code | Cat Wu |
| 8 | **Advisor strategy** : Haiku/Sonnet executor + Opus advisor → Eve Legal a obtenu "frontier model quality at 5x lower cost" | Angela Jiang |
| 9 | **Task horizon** : minutes (2025) → hours (2026) → continuous (futur). Mythos a trouvé une vulnérabilité OpenBSD vieille de 27 ans | Lisa Crofoot + Boris |
| 10 | Nouveau : **self-hosted sandboxes** (Daytona/Cloudflare/Vercel/Modal) + **MCP tunnels** (accès systèmes internes via firewall) | Angela/Katelyn |

### 1.3. Citations verbatim clés (London)

> "It's the calculator feeling except the calculator can write a distributed system." — **Boris**, ouverture

> "Designing for the next version of Cloud, not the current one. (...) Scaffolding is what we call the parts of the agent that aren't Claude. We're seeing that as models get smarter, the scaffolding that used to help can hold Claude back." — **Lisa Crofoot**

> "A lot of my code these days is written by routines. I'm not the one doing the prompting. I'm the one that creates a routine that does the prompting." — **Boris**, demo finale

> "Routines are a higher order prompt." — **Boris**

> "Who here has shipped a pull request in the last week that was completely written by Claude?" — **Jeremy Hadfield** (~50% des mains levées en salle) — voir [MIT Tech Review](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)

> "I think that right now Claude is probably as good as a midlevel engineer at writing code." — **Katelyn Lesse**

> "I think the absolute end state we're trying to get to is Claude basically being able to build itself." — **Angela Jiang**

### 1.4. Demos clés (London)

- **Counter (fictive e-commerce)** : agent "Growthbot" sur Slack qui détecte gagnant d'A/B test, ouvre PR, screenshot des variantes, propose next experiment, requête data warehouse via MCP tunnel (privé)
- **Acme Pay (fictive payments)** : Claude implémente refunds (idempotence, multicurrency, audit), trouve race condition optimistic update en testant lui-même via Chrome, CI autofix retry sur timeout réseau

### 1.5. Annonces majeures London (delta vs SF)

1. **Self-hosted sandboxes** (Daytona, Cloudflare, Vercel, Modal) — agents tournent sur l'infra cliente
2. **MCP tunnels** (`tunnel.anthropic.com`) — MCP servers internes derrière firewall, gateway dans réseau privé
3. Confirmation : multiagent orchestration, outcomes, dreaming maintenant en **public beta** (dreaming reste research preview)

### 1.6. Sources secondaires London

- [Code with Claude 2026 London — full livestream](https://www.youtube.com/watch?v=AgQ4cwL5eOM)
- [MIT Tech Review — coding's future](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- [Fortune — London as AI-coding goes mainstream](https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/)
- **Ravi Trivedi** (Anthropic) sur Dreaming : *"The key principle is getting out of Claude's way. We like to say: 'Let it cook.'"*

---

## 2. Code with Claude SF — 6-7 mai 2026

### 2.1. Speakers identifiés

| Speaker | Role | Talk |
|---------|------|------|
| Ami Vora | CPO | Keynote opening |
| Dianne Na Penn | Head Product Research | Models + capability |
| Cat Wu | Head Product Claude Code | Surfaces (CLI/IDE/Desktop) |
| Boris Cherny | Creator Claude Code | Routines + live coding avec Jarred Sumner |
| **Daisy Hollman** | MTS | **"Beyond the Basics with Claude Code"** |
| Brad Abrams | Product Lead Claude Platform | Advisor strategy + "Rubber Duck" critic |
| Noah Zweben | Anthropic | **"Build a Proactive Agent Workflow"** |
| Matt Bleifer | Anthropic | **"The Thinking Lever"** |
| Fiona Fung | Anthropic | Running AI-native engineering orgs |
| Alex Albert | Anthropic | Capability curve (SWE-bench 62% → 87%) |
| Dario + Daniela Amodei | CEO + President | Conversation main stage |
| Jess Yan + Lance Martin | Managed Agents PM + MTS | Managed agents demo |
| **Thariq Shihipar** | MTS | **"Designing multi-agent systems: When to split, when to sandbox, what to ship"** (Extended SF, 7 mai, Builder Stage 10:45-11:15) |
| Erik Schluntz | Anthropic | **"Vibe Coding in Prod (Responsibly)"** ([YouTube](https://www.youtube.com/watch?v=4Ls0Oa3tRNk) + [4Ls0Oa3tRNk](https://x.com/ErikSchluntz/status/1951010061871968470)) |

### 2.2. Annonces SF

- **SpaceX Colossus partnership** : 220 000+ NVIDIA GPUs, 300+ MW de capacité supplémentaire
- **Rate limits 5h doublés** (Pro/Max/Team/Enterprise), throttling peak-hours supprimé
- **Claude Managed Agents** : Multiagent orchestration (public beta), Outcomes (public beta, +8.4% docx / +10.1% pptx), Dreaming (research preview, header `dreaming-2026-04-21`, max 100 sessions/dream, Opus 4.7 + Sonnet 4.6 only)
- **Code Review** (utilisé par toutes les équipes Anthropic)
- **Remote Agents** (contrôle laptop depuis téléphone), **CI Auto-fix**, **Security Reviews**
- **Routines** = "higher-order prompts" (cron, GitHub webhooks, API endpoints)
- **Vercept acquisition** (25 février 2026) — roadmap computer use
- **Webhooks** for managed agents : at-least-once, no ordering, `X-Webhook-Signature` 5min replay protection
- API volume **+17x YoY**, Q1 2026 annualisé **+80x** vs plan (Dario)

### 2.3. Workflow patterns (SF — Chris Ebert + Blake Crosley + InfoQ)

| Pattern | Détail |
|---------|--------|
| **Hook-first context control** | Hooks fire on trigger only — zéro coût contexte sinon |
| **Prompt cache hit ≥80%** | Target avant toute autre optim ; top tools dans les 90s (Brad Abrams) |
| **Programmatic tool calling** | Agent écrit du code pour inspecter résultats outils, pull only needed |
| **JSON → Markdown tool output** | Sports company a coupé 66% des tokens via format change |
| **Overnight agent runs** | Opus 4.7 peut tourner autonomement plusieurs heures en auto mode |
| **Planner/Generator/Evaluator** | Architecture multi-agent harness pour tâches longues |
| **Prototyping over planning** | Anthropic remplace design docs upfront par prototypes concurrents |
| **Verification shifted left** | Doublé sur vérification précoce pour soutenir débit |
| **Advisor strategy** | Haiku exécute, Opus conseille en escalade — Eve Legal 5x cost reduction |
| **Rubber Duck critic** | Critic secondaire review plans, implémentations complexes, tests AVANT exécution |

### 2.4. Anti-patterns explicites (SF)

| Anti-pattern | Pourquoi ça nuit |
|--------------|-----------------|
| CLAUDE.md bloated | Chaque token chargé à chaque turn → dégrade perf, augmente coût |
| 20 MCP servers × 15 tools each | Prompt devient majoritairement tool definitions |
| Raw tool output dans contexte | Gaspille tokens, utiliser inspection programmatique |
| MCP wrapping de CLI existants | Si CLI marche, shell out plutôt que wrapper MCP |
| Upfront design docs | Remplacé chez Anthropic par prototypes rapides |
| No evals in production agents | Impossible de détecter améliorations ou régressions du modèle |

### 2.5. Citations verbatim SF

> "the bottleneck moved from coding to everything around coding." — **Fiona Fung**

> "Shifting verification left is the only way to maintain quality as throughput increases." — **Fiona Fung**

> "Claudify everything you can." — **Fiona Fung**

> "You should be running agents overnight." — **Daisy Hollman**

> "red squigglies for agents" — **Daisy Hollman** (en parlant des hooks comme linter d'agent)

> "context windows that feel infinite" — **Dianne Na Penn**

### 2.6. Métriques SF

| Métrique | Valeur | Source |
|----------|--------|--------|
| Demand growth 2026 YTD | **80×** | Dario Amodei |
| PRs hebdo lift 3 mois | ~500 → ~1 150 (**+300%**) | Noah Zweben |
| Token reduction via format | **66%** | Noah Zweben (sports company) |
| Target prompt cache hit | ≥80% (top : 90s) | Brad Abrams |
| Context window stable | ~1M tokens | Multiple sessions |
| SWE-bench Verified | 62% (Sonnet 3.7) → **87%** (Opus 4.7) | Alex Albert |

---

## 3. Boris Cherny — talks et workflow référence

### 3.1. Sources

- **Site canonique** : [howborisusesclaudecode.com](https://howborisusesclaudecode.com/)
- **AI Ascent 2026 (Sequoia)** : [YouTube SlGRN8jh2RI](https://www.youtube.com/watch?v=SlGRN8jh2RI) — *transcription non extractible via watch (page metadata uniquement, video probablement gatée pour transcript)*
- **Pragmatic Engineer interview (mars 2026)** : [Building Claude Code with Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)
- **Thread X janvier 2026** (8M views) : [bcherny status 2007179832300581177](https://x.com/bcherny/status/2007179832300581177)

### 3.2. Setup Boris (canonique 2026-05)

| Catégorie | Pratique |
|-----------|----------|
| **Parallèle** | 5 instances terminal numérotées 1-5, chacune dans son worktree git ; 5-10 sessions sur claude.ai/code en plus |
| **Model + effort** | Opus 4.7 + **xhigh** par défaut (max réservé hardest tasks, session-scoped) |
| **Plan mode** | `Shift+Tab Shift+Tab` quasi systématique → itère le plan → switch auto-accept |
| **CLAUDE.md** | Fichier partagé git, équipe contribue plusieurs fois/semaine, **tag `@.claude` sur PRs** déclenche GitHub Action qui commit la mise à jour. Pratique nommée **"Compounding Engineering"** |
| **Hooks** | PostToolUse (auto-format `bun run format \|\| true`), PostCompact (ré-inject contexte critique), Stop (deterministic completion), SessionStart (load context dynamique) |
| **Slash commands** | `/commit-push-pr`, `/techdebt`, `/btw` (side-query sans casser flow), `/simplify`, `/batch`, `/go` (test e2e → simplify → PR), `/loop` (jusqu'à 1 semaine), `/schedule` (cron cloud) |
| **Subagents** | `.claude/agents/` (frontmatter `isolation: worktree`), exemples `code-simplifier.md`, `verify-app.md`, `build-validator.md`. **Opus 4.7 ne spawn pas automatiquement** → demander explicitement |
| **Search** | **glob + grep, pas de RAG, pas de vector DB** ("Plain glob and grep, driven by the model, beat everything") |
| **Permissions** | `/permissions` → `.claude/settings.json` shared, wildcards `Bash(bun run *)`, **Auto mode** = safety classifier (évite manuel ET --dangerously-skip-permissions) |
| **MCP** | Slack HTTP, BigQuery via `bq` CLI, Sentry, Chrome extension (CRITIQUE pour verification frontend), iMessage plugin (`claude` comme contact Messages) |
| **Session mgmt** | `/rewind` (double Esc) drop attempt vs corriger in-place ; `/compact <hint>` ; `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` ; `/focus` cache intermediate output |
| **Verification** | Tip #1 : "Give Claude a way to verify its work" → **2-3x quality** |

### 3.3. Métriques Boris

- **20-30 PRs/jour** en solo (5 parallel + 5-10 cloud sessions)
- Avant l'IA : revue comments loggés dans spreadsheet, après **3-4 occurrences** → converti en lint rule
- Anthropic interne : **100% des tests + 100% des internal lint rules** écrits par Claude (cité dans Every podcast)
- "Now we're on the order of like double digit hours... the last model is like 30 hours" — Boris sur task horizon

### 3.4. Citations Boris

> "If my goal is to write a Pull Request, I will use Plan mode, and go back and forth with Claude until I like its plan. From there, I switch into auto-accept edits mode and Claude can usually 1-shot it."

> "Pretty soon we're going to be in this mode of Claudes monitoring Claudes."

> "It's not so much about deep work, it's about how good I am at context switching and jumping across multiple different contexts very quickly."

> "Start 10 agents and then just go... 10 at a time and just migrate all the stuff over." (sur subagents pour migrations)

---

## 4. Cat Wu — talks et insights

### 4.1. Sources

- **Every podcast (mai 2026)** : [How to Use Claude Code Like the People Who Built It](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it) + [transcript](https://every.to/podcast/transcript-how-to-use-claude-code-like-the-people-who-built-it)
- **TechCrunch (13 mai 2026)** : [Anthropic's Cat Wu says future AI will anticipate your needs](https://techcrunch.com/2026/05/13/anthropics-cat-wu-says-that-in-the-future-ai-will-anticipate-your-needs-before-you-know-what-they-are/)
- **Medium** : [Boris Cherny and Cat Wu: Anthropic's Batman and Robin](https://medium.com/design-bootcamp/boris-cherny-and-cat-wu-anthropics-batman-and-robin-2209d74927e6)

### 4.2. Takeaways Cat Wu

- **Antfooding** : >70-80% des "ants" (employés techniques Anthropic) utilisent Claude Code quotidiennement, feedback channel = 1 post/5 min
- **3 surfaces Claude Code** : CLI (power users) → IDE (UI changes) → Desktop (GUI plein écran, previews, images, rich outputs)
- **Multi-clotting** = nom interne pour juggler plusieurs sessions
- Execs et managers re-codent (n'avaient pas committé depuis des années)
- **Playwright subagent** (perso Cat) : "Really good at front end testing... uses Playwright to see... what are all the errors on this site"
- **Diary entry pattern** : "For every task they do, they tell Claude Code to write a diary entry in a specific format"

### 4.3. Citation Cat Wu (futur)

> "I think the next big thing is proactivity. Last year we were in this world of synchronous development. Right now, people are shifting to routines, so like automating, for example, responses to customer support tickets. And I think the next step is that Claude understands what you work on, and just sets up some of these automations for you."

---

## 5. Thariq Shihipar — multi-agent + HTML

### 5.1. Sources

- **Code with Claude SF Extended (7 mai 2026, Builder Stage)** : "Designing multi-agent systems: When to split, when to sandbox, what to ship" — *talk non encore uploadé séparément (au 22 mai). Suivre la playlist [Code w/ Claude Developer Conference](https://claude.com/code-with-claude)*
- **Workshop Agent SDK** : [YouTube TqC1qOfiVcQ](https://www.youtube.com/watch?v=TqC1qOfiVcQ)
- **How I AI (Lenny's)** : [HTML is the new Markdown](https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown) + [ChatPRD writeup](https://www.chatprd.ai/how-i-ai/claude-code-anthropic-thariq-shihipar-on-replacing-markdown-with-html)
- **Vibe Code Camp distilled** : [14_thariq_shihipar.html](https://davidguttman.github.io/every-vibe-code-camp-distilled/14_thariq_shihipar.html)

### 5.2. Concepts clés Thariq

1. **"HTML is the new Markdown"** : plans 1000 lignes en MD = désengagement. HTML = interactif, mockups, scrollable
2. **Compute allocator** : ~1% des tokens générés finissent en prod, les 99% restants = dashboards, micro-apps, planning artifacts
3. **Throwaway micro-apps** : "micro software on top of micro software" — UI custom pour chaque édition spécifique, jetable
4. **Living `design_system.html`** : source of truth portable (colors, typo, components) — meilleur que Figma pointer
5. **Unhobbling the model** : philosophie "delete scaffolding when new model lands". La plupart des équipes échouent à supprimer le code obsolète
6. **Tasks system** (nouveau, remplace Todos) : dependencies, persistence cross-session, context-passing entre Claudes
7. **Sandboxing** : SDK gère exécution + sandbox + error recovery. Hooks = 18 lifecycle events (PreToolUse, PostToolUse, Stop, SubagentStart, SubagentStop, Notification, PreCompact...)

### 5.3. Citations Thariq

> "we're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on"

> "I always needed to be like, 'Hey, Claude, like I trust you here.'"

> "Long autonomous runs require significant upfront spec work (~30 min interviewing with Opus) to constrain scope."

---

## 6. Erik Schluntz — Vibe Coding in Prod

### 6.1. Sources

- **YouTube canonique** : [Vibe Coding - Eric Schluntz, Anthropic Team](https://www.youtube.com/watch?v=4Ls0Oa3tRNk)
- **Annonce X** : [@ErikSchluntz status 1951010061871968470](https://x.com/ErikSchluntz/status/1951010061871968470)
- **Coverage** : [DeepInsightAI masterclass](https://deepinsightai.io/how-to-properly-do-vibe-coding/), [36Kr](https://eu.36kr.com/en/p/3774648797659657)

### 6.2. The 22 000-line merge case

Erik et son équipe RL ont **mergé 22 000 lignes** majoritairement écrites par Claude. 4 stratégies clés :

1. **Deep PM-style guidance** : plusieurs jours de planning manuel upfront
2. **Scope strict aux leaf nodes** : technical debt acceptable seulement sur feuilles (terminal functions, auxiliary components)
3. **Human intervention sur core** : trunk/architecture → revue manuelle stricte
4. **Verifiable checkpoints** : stress tests long-terme, IO standards faciles à vérifier

**Résultat** : 2 semaines d'effort humain → **compressées à 1 jour**.

### 6.3. Concepts Erik

- **Leaf nodes strategy** : laisse Claude dans les feuilles (terminaux, peu de dépendances), protège le trunk
- **Developer mindset shift** : se voir comme "product manager of Claude", **15-20 min context gathering** avant de laisser exécuter
- **Vibe coding ≠ abandon de responsabilité** = passage de "code writers" à "system designers and verifiers"
- **Métrique interne Anthropic** : "the length of tasks AI can complete is doubling every seven months"

### 6.4. Citation Erik

> "In a year or two, demanding to read every line of code will make you the bottleneck."

---

## 7. Lydia Hallie — workflows + DevEx

### 7.1. Sources

- **Frontend Masters workshop (21 avril 2026)** : [Claude Code Deep Dive](https://frontendmasters.com/workshops/advanced-claude-code/) — focus harness vs model, CLAUDE.md, plan mode, permissions, skills, MCP server from scratch
- **X annonces** : best practices docs (jan 2026, 245k+ views), session sharing, agent teams research preview, learning mode

### 7.2. Insights Lydia

- **Mental model clé** : distinction **harness vs model** (ce que fait le framework vs ce que fait le LLM)
- **Learning mode** (`/config → Output style → Learning`) : Lydia l'utilise pour ses side projects pour rester "sharper" — alternative à full automation
- **Agent teams** (research preview) : lead agent délègue à teammates parallèles qui coordonnent
- **Session sharing** : share full conversation via link (web, desktop, mobile)

---

## 8. Synthèse cross-talks — patterns émergents mai 2026

### 8.1. Le shift majeur

**Synchronous development → Proactive routines** (confirmé Boris, Cat, Lisa, Fiona)

- 2025 : "I prompt Claude"
- mai 2026 : "I create a routine that prompts Claude"
- futur (cat) : "Claude understands what I work on and sets up routines for me"

### 8.2. Verification = méta-priorité

Citée par **TOUS** : Boris ("give Claude a way to verify"), Fiona ("verification shifted left"), Erik ("verifiable checkpoints"), Daisy ("red squigglies for agents"). Le gating capability pour autonomy.

### 8.3. Anti-pattern unifié : scaffolding obsolète

- Lisa (London) : "scaffolding that used to help can hold Claude back"
- Thariq : "unhobble Claude... you have to like delete the code"
- Daisy : harnesses 2025 (compaction, retry, memory) ont une "half-life of just months"

### 8.4. Tooling minimal qui gagne

- **glob + grep > RAG** (Boris)
- **Shell CLI > MCP wrappers** (SF anti-patterns)
- **HTML > Markdown** pour planning (Thariq)
- **Plan mode** quasi systématique pour tâche substantielle (Boris, Cat)

### 8.5. Métriques de référence à mémoriser

| Métrique | Source | Note |
|----------|--------|------|
| **+200% PRs/eng** Anthropic interne | Cat Wu London | adoption wall-to-wall |
| **20-30 PRs/jour** Boris solo | Pragmatic Engineer | 5 parallel + 5-10 cloud |
| **>70-80%** ants utilisent CC daily | Cat Wu | "antfooding" |
| **+17x** API YoY | Boris London | platform |
| **+80x** Q1 2026 vs plan | Dario Amodei | infra contrainte |
| **5x cost reduction** advisor strategy | Eve Legal | Sonnet exec + Opus advisor |
| **Task horizon doublé tous les 7 mois** | Erik Schluntz | métrique interne |
| **62% → 87%** SWE-bench Verified | Alex Albert | Sonnet 3.7 → Opus 4.7 |

---

## 9. Sources clés à recapitaliser dans le vault

À créer en notes atomiques (suggéré) :

- `01-Claude/Code/features/routines.md` — higher-order prompts, cron + webhooks + API
- `01-Claude/Code/features/managed-agents.md` — multiagent orch, outcomes, dreaming, self-hosted sandboxes, MCP tunnels
- `01-Claude/Code/features/advisor-strategy.md` — Haiku/Sonnet executor + Opus advisor (Eve Legal case)
- `04-Techniques/patterns/compounding-engineering.md` — `@.claude` tag PR → CLAUDE.md auto-update (Boris)
- `04-Techniques/patterns/leaf-nodes-strategy.md` — Erik Schluntz, scope vibe coding sur feuilles
- `04-Techniques/patterns/html-is-the-new-markdown.md` — Thariq, planning + design system
- `04-Techniques/patterns/multi-clotting.md` — 5 worktrees + 5-10 cloud sessions (Boris)
- `05-Leaders/claude-code/lisa-crofoot.md` — research PM, 17 versions Claude (note manquante)
- `05-Leaders/claude-code/jeremy-hadfield.md` — engineer (note manquante)
- `05-Leaders/claude-code/daisy-hollman.md` — MTS, "let it cook", "red squigglies for agents" (note manquante)
- `05-Leaders/claude-code/erik-schluntz.md` — vibe coding in prod (note manquante)
- `05-Leaders/claude-code/thariq-shihipar.md` — multi-agent, HTML (à vérifier si existante, sinon créer)
- `06-Industrie/code-with-claude-london-2026-05-19.md` — event note
- `Knowledge/syntheses/synthese-cwc-may-2026.md` — cette note synthèse à raffiner pour 04-Techniques

---

## 10. Sources non explorées / next-pass

- **Code with Claude London full livestream** ([AgQ4cwL5eOM](https://www.youtube.com/watch?v=AgQ4cwL5eOM)) — transcription complète à faire (plusieurs heures, prioriser talks individuels quand uploadés)
- **Talks individuels London** : Daisy Hollman "Beyond the Basics", Noah Zweben "Proactive Agent Workflow", Matt Bleifer "The Thinking Lever" — à surveiller sur la playlist YouTube Anthropic dans 5-7 jours
- **Thariq SF Extended talk** : "Designing multi-agent: when to split, when to sandbox, what to ship" — non uploadé séparément encore (couvert partiellement via Lenny's podcast)
- **Boris Pragmatic Engineer podcast (mars 2026)** : audio complet, transcription approfondie possible
- **Webinar "Story of Claude Code"** : [resources.anthropic.com/webinar/claude-code-live](https://resources.anthropic.com/webinar/claude-code-live)
- **Live blog Simon Willison** : [simonwillison.net/2026/May/6/code-w-claude-2026/](https://simonwillison.net/2026/May/6/code-w-claude-2026/) — pourrait contenir des notes-talks détaillées non extraites

---

## Sources principales (URL canoniques)

- [Code w/ Claude London livestream](https://www.youtube.com/watch?v=AgQ4cwL5eOM)
- [London opening keynote (transcrit ici)](https://www.youtube.com/watch?v=6amLO7I9xdg)
- [How Boris uses Claude Code](https://howborisusesclaudecode.com/)
- [Boris AI Ascent 2026 (Sequoia)](https://www.youtube.com/watch?v=SlGRN8jh2RI)
- [Pragmatic Engineer × Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)
- [Every podcast Boris+Cat — How to Use Claude Code Like the People Who Built It](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it)
- [Erik Schluntz — Vibe Coding in Prod](https://www.youtube.com/watch?v=4Ls0Oa3tRNk)
- [Thariq SDK Full Workshop](https://www.youtube.com/watch?v=TqC1qOfiVcQ)
- [Thariq × Lenny — HTML is the new Markdown](https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown)
- [Lydia Hallie — Claude Code Deep Dive workshop](https://frontendmasters.com/workshops/advanced-claude-code/)
- [Simon Willison live blog CwC 2026](https://simonwillison.net/2026/May/6/code-w-claude-2026/)
- [Chris Ebert — Notes from CwC 2026](https://chrisebert.net/notes-from-code-with-claude-2026/)
- [Blake Crosley — CwC SF recap](https://blakecrosley.com/blog/code-with-claude-sf-2026-recap)
- [InfoQ — Managed Agents, Proactive, Capability Curve](https://www.infoq.com/news/2026/05/code-with-claude/)
- [Dotzlaw — doubled limits + infinite context](https://www.dotzlaw.com/insights/anthropic-2026-code-with-claude/)
- [MIT Tech Review — London coverage](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- [Fortune — London mainstream](https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/)
- [TechCrunch — Cat Wu sur proactivité](https://techcrunch.com/2026/05/13/anthropics-cat-wu-says-that-in-the-future-ai-will-anticipate-your-needs-before-you-know-what-they-are/)
