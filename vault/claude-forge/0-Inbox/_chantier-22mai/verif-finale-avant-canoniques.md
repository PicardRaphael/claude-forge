---
titre: "Vérification finale — 16 claims arbitrés avant rédaction notes canoniques"
resume: "Arbitrage 16 claims clés avec source primaire équipe Claude Code > Karpathy > autres. Verbatim, URLs, dates"
aliases:
  - "verif finale canoniques"
  - "arbitrage claims chantier"
  - "verbatim canoniques anthropic"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/verification"
  - "#domaine/claude-code"
---

# Vérification finale — 16 claims arbitrés

Sources primaires utilisées :
- **docs Anthropic officielles** : `code.claude.com/docs/en/{sub-agents,skills,slash-commands,commands}` (redirect depuis `docs.claude.com`)
- **transcripts YouTube** stockés dans `recherche-youtube-watch-vibe-coding.md` (4 talks, ~38 300 mots)
- **Anthropic Engineering blog** : `anthropic.com/engineering/effective-harnesses-for-long-running-agents` (Justin Young)
- **agentskills.io** (spec ouverte) + **github.com/agentskills/agentskills**
- **github.com/trailofbits/claude-code-config** (README inline)
- **WebSearch** sur tweets/threads Boris Cherny pour chronologie PRs
- **chrisebert.net/notes-from-code-with-claude-2026/** pour Noah Zweben +300%

Règle d'arbitrage : Anthropic > Karpathy > Boris/Cat/Thariq officiel > tiers (Simon Willison, Trail of Bits, blogs).

---

## Claim 1 — Chronologie PRs Boris (150/jour record vs 259/30j vs 20-30/jour régulier)

**Claim original** : "150 PRs/jour record" vs "259 PRs en 30 jours" vs "20-30 PRs/jour régulier" — chronologie verbatim demandée.

**Sources primaires** :
- Boris Cherny — Sequoia AI Ascent 2026 (avril 2026), `youtube.com/watch?v=SlGRN8jh2RI` — transcript local
- Boris Cherny — Threads.com `@boris_cherny/post/DSxC69PCCz_` (~déc 2025 / Opus 4.5 era)
- Tweet Rohan Paul `x.com/rohanpaul_ai/status/2005962896929661047` relayant le même chiffre 259

**Verdict** : CONFIRMÉ avec chronologie distincte — ce sont DEUX métriques différentes à deux périodes différentes, pas un conflit.

**Verbatim Sequoia (avril 2026)** :
> "I write somewhere usually a few dozen PRs every day. There was a day last week I did like 150 PRs in a day. That was a record."

→ **150/jour = pic exceptionnel**, **"a few dozen" = quelques douzaines = 20-30 = régulier**, période Sequoia (Opus 4.6/4.7).

**Verbatim Threads (Opus 4.5 era)** :
> "In the last thirty days, I landed 259 PRs — 497 commits, 40k lines added, 38k lines removed. Every single line was written by Claude Code + Opus 4.5. Claude consistently runs for minutes, hours, and days at a time (using Stop hooks)."

→ **259/30j ≈ 8.6 PRs/jour moyenne**, période ANTÉRIEURE (Opus 4.5), aligne avec "few dozen" en upper bound.

**Implication note canonique** : ne pas additionner ni opposer. Présenter comme **évolution Opus 4.5 (déc 2025, 259/30j ≈ 8.6/j) → Opus 4.6-4.7 (avril 2026, dozens/j + pic 150)**. Le "Ralph Wiggum plugin" pour itération continue + Stop hooks est mentionné dans les replies threads.

---

## Claim 2 — +300% PRs hebdo équipe Anthropic (Boris ou Noah Zweben ?)

**Claim original** : "+300% PRs hebdo équipe Anthropic" attribué à Boris keynote London.

**Source primaire trouvée** : `chrisebert.net/notes-from-code-with-claude-2026/` — Code with Claude SF/London 2026.

**Verdict** : NUANCÉ — DEUX chiffres distincts, attribués à DEUX speakers différents.

1. **+300% = Noah Zweben** (pas Boris, pas Cat) :
   > "Noah Zweben's session put numbers on it. He showed a chart of his own team's weekly PRs merged to main. In three months, weekly PR throughput went up 300%, from around 500 in January to roughly 1,150 in March."
   → c'est l'équipe de **Noah Zweben** chez Anthropic, pas l'org entière, 3 mois (jan→mars 2026).

2. **+200% PRs/engineer Anthropic = Cat Wu** (London keynote, verbatim transcript local) :
   > "Anthropic, we've seen that this has driven a 200% increase in the number of PRs per engineer even as our engineering org has scaled substantially."
   → c'est la métrique **org-wide Anthropic**, ratio par ingénieur, et c'est **200%** pas 300%.

**Implication note canonique** : NE PAS dire "+300% Anthropic". Dire **"+200% PRs/eng Anthropic (Cat Wu, London keynote)"** et **"+300% PRs hebdo équipe Noah Zweben en 3 mois (CwC 2026)"** séparément.

---

## Claim 3 — Sub-agents context window (mai 2026)

**Source primaire** : `code.claude.com/docs/en/sub-agents` (récupéré).

**Verdict** : CONFIRMÉ — context window séparé, pas hérité du parent.

**Verbatim doc officielle** :
> "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results."

> "Subagents help you: **Preserve context** by keeping exploration and implementation out of your main conversation"

**Implication note canonique** : sub-agent = nouvelle fenêtre de contexte propre, indépendante. Pas de héritage. Le parent reçoit uniquement le résumé final. → fondement architectural des patterns "Document & Clear" et "search sub-agent".

---

## Claim 4 — Skills budget tokens (5k chacun / 25k combiné)

**Source primaire** : `code.claude.com/docs/en/skills` section "Skill content lifecycle".

**Verdict** : CONFIRMÉ verbatim, mais avec précisions importantes.

**Verbatim doc officielle** :
> "Auto-compaction carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, **keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens.** Claude Code fills this budget starting from the most recently invoked skill, so older skills can be dropped entirely after compaction if you have invoked many in one session."

**Précision critique** : ces 5k/25k ne s'appliquent **qu'après auto-compaction**. AVANT compaction, le skill complet entre en contexte et y reste pour toute la session. Le claim "skills = 5k tokens chacun" est donc INEXACT en régime normal — c'est 5k uniquement post-compaction.

**Autres limites verbatim** :
- description+when_to_use : "truncated at 1,536 characters in the skill listing"
- skill listing budget : "scales at 1% of the model's context window" (réglable via `skillListingBudgetFraction`)
- SKILL.md size : "Keep `SKILL.md` under 500 lines" (Tip, pas hard limit)

**Implication note canonique skill** : reformuler — "5k/25k = budget de SURVIE post-compaction, pas budget d'entrée. 1,536 chars hard cap sur description+when_to_use. 1% du context window total pour le listing des skills."

---

## Claim 5 — Tool response max 25k tokens

**Verdict** : NON-ARBITRÉ-ANTHROPIC. Ne figure pas dans les docs publiques sub-agents/skills/commands consultées. Le chiffre 25k apparaît UNIQUEMENT dans le contexte skills budget combiné post-compaction (claim 4), pas comme limite tool response générique.

**Source secondaire** : la limite 25k est mentionnée dans la doc Claude API "Tool use" mais variable selon la version SDK. Aucune source officielle confirmant "tool response max 25k tokens" comme limite Claude Code n'a été retrouvée en 2 recherches.

**Implication note canonique** : NE PAS affirmer ce chiffre. Reformuler en "les outputs longs doivent être sauvegardés sur le file system" (verbatim Thariq, claim non chiffré) et ne pas inventer de plafond.

---

## Claim 6 — Architecture 2-agents Justin Young (init + coding)

**Source primaire** : `anthropic.com/engineering/effective-harnesses-for-long-running-agents` — Justin Young (Member of Technical Staff Anthropic).

**Verdict** : CONFIRMÉ.

**Verbatim (résumé fidèle de l'article)** :
- **Initializer Agent** : "The very first agent session uses a specialized prompt that asks the model to set up the initial environment — an `init.sh` script, a `claude-progress.txt` file that keeps a log of what agents have done, and an initial git commit that shows what files were added."
- **Coding Agent** : "Every subsequent session asks the model to make incremental progress, then leave structured updates."
- Principe central : "leave the environment in a clean state at the end of a session — meaning code that would be appropriate for merging to a main branch."

**Question ouverte (verbatim article)** :
> "It's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture."

**Implication note canonique** : pattern officiel Anthropic. Convergence avec doctrine forge "agent loop = gather context + act + verify" (Thariq). À citer dans note "long-running agents" + "harness engineering".

---

## Claim 7 — Slash commands : /simplify, /batch, /btw, /goal, /go, /loop, /schedule

**Source primaire** : `code.claude.com/docs/en/commands` (récupéré, table complète).

**Verdict** : NUANCÉ — distinction builtin vs bundled skill vs custom.

| Command | Statut officiel mai 2026 |
|---|---|
| `/simplify` | **Alias** historique pour `/code-review` (bundled Skill). Verbatim doc : "Formerly `/simplify`, which still works as an alias" |
| `/batch <instruction>` | **Bundled Skill**. "Orchestrate large-scale changes across a codebase in parallel. Decomposes into 5 to 30 independent units, spawns one background subagent per unit in isolated git worktree" |
| `/btw <question>` | **Builtin command**. "Ask a quick side question without adding to the conversation" |
| `/goal [condition\|clear]` | **Builtin command**. "Set a goal: Claude keeps working across turns until the condition is met" |
| `/go` | **PAS dans la doc officielle**. C'est un slash command CUSTOM forge (`.claude/commands/go.md` ou skill). Pattern Boris workflow, pas builtin. |
| `/loop [interval] [prompt]` | **Bundled Skill**. "Run a prompt repeatedly while the session stays open. Alias: `/proactive`" |
| `/schedule [description]` | **Builtin command**. "Create, update, list, or run routines, which execute on Anthropic-managed cloud infrastructure. Alias: `/routines`" |

**Implication note canonique** : `/go` est SPÉCIFIQUE forge/Neoteem (custom). Tous les autres sont officiels CC v2.1.x. Important pour la note "Claude Code slash commands" — ne pas confondre custom forge avec builtin.

---

## Claim 8 — Anti-rationalization Stop hook (Trail of Bits)

**Source primaire** : `github.com/trailofbits/claude-code-config` README.

**Verdict** : CONFIRMÉ — c'est un hook Stop inline dans le README (pas un fichier séparé).

**Verbatim/structure** :
- Type : `Stop` hook, `"type": "prompt"`, modèle Haiku (fast model)
- Mécanique : évaluateur LLM intercepte la réponse finale de Claude avant validation
- Pattern bloqué (verbatim cité par le README) :
  > "claiming issues are 'pre-existing' or 'out of scope', saying 'too many issues' to fix, deferring to unrequested 'follow-ups'"
- Réponse de rejet : `{"ok": false, "reason": "You are rationalizing incomplete work. [specific issue]. Go back and finish."}`
- Le `reason` est injecté comme prochaine instruction → force la continuation
- Réponse d'approbation : `{"ok": true}`
- **Gotcha critique** : "The prompt must demand 'raw JSON only' — without that instruction, Haiku wraps results in markdown fences, silently breaking the hook's JSON parsing."
- Timeout défaut : 30s

**Implication note canonique** : pattern généralisable. Note "Anti-rationalization Stop hook" dans `04-Techniques/agents/` ou `01-Claude/Code/best-practices/`. Convergence avec doctrine forge "hooks > rules" (`feedback_enforce_not_advise`). Le gotcha "raw JSON or markdown breaks" est highest-signal.

---

## Claim 9 — "Lethal trifecta" (Thariq citant Simon Willison)

**Source primaire** : Thariq Shihipar — Claude Agent SDK Workshop, `youtube.com/watch?v=TqC1qOfiVcQ` — transcript local section 3.

**Verdict** : CONFIRMÉ verbatim, avec contexte important.

**Verbatim Thariq** :
> "Ultimately that's what they call the lethal trifecta. Is like the ability to execute code in environment, change the file system, exfiltrate the code. I think I'm getting the lethal trifecta a little bit wrong there, but the idea is basically like if they can exfiltrate your information back out. That's like they still need to be able to extract information. So if you sandbox the network, that's a good way of doing it."

**Note critique** : Thariq lui-même dit "I think I'm getting the lethal trifecta a little bit wrong there." La formulation **canonique Simon Willison** est : (1) accès à des données privées, (2) exposition à du contenu non-fiable, (3) capacité d'exfiltration externe. Thariq la reformule en (1) exécution de code, (2) modification FS, (3) exfiltration. C'est une approximation.

**Implication note canonique** : citer la formulation Simon Willison comme canonique, mentionner que Thariq la cite avec une variation. **"Sandbox the network" = mitigation principale recommandée par Thariq.**

---

## Claim 10 — "Swiss cheese defense" (Thariq)

**Source primaire** : Thariq Shihipar — Agent SDK Workshop, transcript local.

**Verdict** : CONFIRMÉ verbatim.

**Verbatim** :
> "Swiss cheese defense. On every layer some defenses and together we hope that it blocks everything. On the model layer we do a lot of alignment. Then there is the harness itself, we have a lot of permissioning and prompting, and we do AST parser on the bash tool. Finally, the last layer is sandboxing."

**Layers identifiés** : (1) model alignment, (2) harness permissioning + prompting, (3) AST parser sur bash tool, (4) sandboxing.

**Implication note canonique** : pattern défense en profondeur. À documenter dans `04-Techniques/agents/` ou `Knowledge/syntheses/`. Convergence directe avec auto-mode-classifier Anthropic (cf `reference_auto_mode_classifier`) + hooks bloquants forge.

---

## Claim 11 — "Compute allocator 1% tokens en prod" (Thariq)

**Verdict** : NON CONFIRMÉ dans le transcript Thariq disponible. Le terme "compute allocator" et le chiffre "1% tokens" ne figurent PAS dans le transcript du workshop Agent SDK consulté.

**Recherche** : grep sur "allocator", "1%", "compute" dans le transcript transcrit dans `recherche-youtube-watch-vibe-coding.md` ne ramène rien de pertinent.

**Hypothèse** : la claim provient peut-être d'une AUTRE intervention Thariq (Code with Claude SF Extended "Multi-agent systems: when to split, when to sandbox" — non transcrit, URL non trouvée), ou d'une mauvaise mémoire du chantier vague 1.

**Implication note canonique** : **NE PAS UTILISER** ce chiffre tant qu'une source primaire n'est pas retrouvée. Marquer "non-arbitré-Anthropic". Si crucial, retrancher après identification de la vraie source.

---

## Claim 12 — "Bash > tools" (Thariq, quand bash vs MCP vs code gen)

**Source primaire** : Thariq Shihipar — Agent SDK Workshop, transcript local.

**Verdict** : CONFIRMÉ verbatim avec trade-offs explicites.

**Verbatim "Bash is what makes Claude Code so good"** :
> "Bash is what makes Claude Code so good. The bash tool was like the first code mode, right? So the bash tool allows you to store the results of your tool calls to files, store memory, dynamically generate scripts and call them, compose functionality like tail, grep. It lets you use existing software like FFmpeg or LibreOffice."

**Trade-offs verbatim** :
- **Tools** : "extremely structured and very very reliable. If you want to have as fast an output as possible with minimal errors, minimal retries, tools are great. Cons: they're high context usage. If anyone's built an agent with 50 or 100 tools, they take up a lot of context and the model gets a little bit confused. No discoverability of the tools, and they're not composable."
- **Bash** : "very composable, low context usage. Can take a little bit more discovery time. Might be slightly lower call rates."
- **Code gen** : "Highly composable, dynamic scripts. They take the longest to execute, need linting, possibly compilation. API design becomes very interesting."

**Quand utiliser quoi (verbatim)** :
> "**Tools** — think about them as atomic actions your agent usually needs to execute in sequence, and you need a lot of control over. For example, in Claude Code, we don't use bash to write a file. We have a write_file tool, because we want the user to be able to see the output and approve it, and we're not really composing write_file with other things. **Sending an email is another example. Any sort of non-reversible change — a tool is a good place for that.**"

> "**Bash** — composable actions like searching a folder, using GitHub, linting code and checking for errors or memory. You can write files to memory, and bash can be your memory system."

> "**Code generation** — if you're trying to do this highly dynamic, very flexible logic, composing APIs, doing data analysis or deep research or reusing patterns."

**Implication note canonique** : note technique "bash vs tools vs code gen" — décision tree clair. **Tools = non-reversible + atomic.** **Bash = composable + memory.** **Code gen = highly dynamic.** Aligne avec doctrine forge (hooks bash) et auto-mode-classifier (bash sous surveillance).

---

## Claim 13 — Advisor strategy 5× cost reduction (Angela Jiang, London keynote)

**Source primaire** : Cat Wu + Boris — Code with Claude London Opening Keynote, `youtube.com/watch?v=6amLO7I9xdg`, transcript local section 4 — speaker **Angela Jiang** (Head of Claude Platform Product), pas Cat Wu ni Boris.

**Verdict** : CONFIRMÉ verbatim, attribution à corriger (Angela, pas Cat).

**Verbatim Angela** :
> "One of the ways that we're solving [frontier intelligence at lower cost] is with the advisor strategy. All you have to do is update your tools in your tools array on the messages API. What we're doing behind the scenes is that we're splitting execution from advising. In execution, you can use a smaller model. But when that small model needs help, it can reach out to a larger model for advice. **In practice, this means you can have a haiku or sonnet class model do your executing and use Opus as an adviser.** Sonnet performed even more cheaply than on its own because Opus advised it to get its work done better."

> "Eve Legal used the advisor strategy and they told us they got frontier model quality at five times lower cost."

**Implication note canonique** : la feature `advisor()` tool dispo dans le harness Claude Code = implémentation directe de cette stratégie. Note à créer dans `04-Techniques/agents/advisor-strategy.md` avec attribution **Angela Jiang, Head of Claude Platform Product, CwC London mai 2026**. Cas d'usage Eve Legal = preuve de marché.

---

## Claim 14 — "Routines = higher order prompt" (Boris)

**Source primaire** : Cat Wu + Boris — CwC London keynote, transcript local section 4.

**Verdict** : CONFIRMÉ verbatim.

**Verbatim Boris** :
> "A lot of my code these days is written by routines. I'm not the one doing the prompting. I'm the one that creates a routine that does the prompting. **For the engineers in the room, think of it like a higher order function. Routines are a higher order prompt.**"

> "**The default isn't 'I'm going to prompt Claude Code.' The default is now 'I'm going to have Claude prompt Claude Code.'**"

**Implication note canonique** : citation parfaite pour note `01-Claude/Code/features/routines.md` + `04-Techniques/patterns/higher-order-prompting.md`. Convergence directe avec `/schedule` (builtin) et `/loop` (bundled skill). Boris "dozens of loops running" (Sequoia) = preuve d'usage personnel.

---

## Claim 15 — "Scaffolding holds Claude back" (Lisa Crofoot, London keynote)

**Source primaire** : Cat Wu + Boris — CwC London keynote, transcript local section 4 — speaker **Lisa Crofoot** (PM research), pas Cat Wu.

**Verdict** : CONFIRMÉ verbatim.

**Verbatim Lisa** :
> "You need to build for emerging capabilities, not just what works today. That means designing for the next version of Claude, not the current one. **Scaffolding is what we call the parts of the agent that aren't Claude. So the loops, the instructions, the tools. We're seeing that as models get smarter, the scaffolding that used to help can hold Claude back.** Claude is intelligent and resourceful and more intelligent models can often get further with generalized primitives like a file system and sandbox computing environment."

**Métaphore task horizon (verbatim Lisa)** :
> "One metric I look to is task horizon. So how long can a model work before losing the thread? Last year at this time, models could reliably work for minutes. And today, most users have agents that run for hours. **We expect future generations of Claude to run continuously.**"

**Implication note canonique** : argument central pour la doctrine forge "hooks = lint/security/scope, JAMAIS workflow" (révision 22 mai). Citation **Lisa Crofoot, PM research, CwC London**. **Convergence directe avec `feedback_enforce_not_advise` révisé** : workflow scaffolding lourd = handicap pour Opus 4.7+. Citer dans `Knowledge/raisonnements/raisonnement-22mai-doctrine-vs-enforcement.md` comme source externe Anthropic.

---

## Claim 16 — agentskills.io / agentskills.io (spec ouverte)

**Source primaire** : `agentskills.io` + référencé officiellement par `code.claude.com/docs/en/skills`.

**Verdict** : CONFIRMÉ. La spec existe, ouverte, originellement développée par Anthropic, adoptée par 40+ produits.

**Verbatim agentskills.io** :
> "Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. At its core, a skill is a folder containing a `SKILL.md` file."

> "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem. Come join the discussion on GitHub or Discord!"

**Confirmation côté Claude Code (doc officielle)** :
> "Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like invocation control, subagent execution, and dynamic context injection."

**Progressive disclosure 3 étapes (verbatim agentskills.io)** :
1. **Discovery** : "agents load only the name and description of each available skill, just enough to know when it might be relevant"
2. **Activation** : "When a task matches a skill's description, the agent reads the full `SKILL.md` instructions into context"
3. **Execution** : "The agent follows the instructions, optionally executing bundled code or loading referenced files as needed"

**Adoptions notables visibles dans la liste** : Cursor, GitHub Copilot, VS Code, OpenAI Codex, Gemini CLI, Goose (Block), Roo Code, Kiro, Letta, Spring AI, Laravel Boost, Databricks Genie, Snowflake Cortex, Tabnine, Mistral Vibe, OpenCode, OpenHands, Factory, Amp, ByteDance Trae, Junie (JetBrains) — soit la quasi-totalité des coding agents 2026.

**GitHub** : `github.com/agentskills/agentskills`. Quickstart : `agentskills.io/skill-creation/quickstart`. Spec complète : `agentskills.io/specification`.

**Implication note canonique** : créer note **`01-Claude/Code/features/agent-skills-open-standard.md`** — affirmer "skills CC = spec ouverte cross-tool, pas lock-in Anthropic." Argument fort pour Raphael : skills écrites pour Claude Code marchent dans Cursor, Codex, Gemini CLI, etc. Lien direct avec note `reference_anthropic_skills_plugin.md` à mettre à jour.

---

## Synthèse arbitrage

### CONFIRMÉS verbatim avec source primaire (12)

Claims 1, 3, 4, 6, 8, 9, 10, 12, 13, 14, 15, 16.

### NUANCÉS / chronologie distincte (2)

- Claim 2 : +300% Noah Zweben (équipe) vs +200% Cat Wu (org Anthropic) — chiffres différents, speakers différents.
- Claim 7 : `/simplify` alias `/code-review`, `/go` est CUSTOM forge pas builtin.

### NON-ARBITRÉS-ANTHROPIC (2) — à NE PAS utiliser dans notes canoniques

- **Claim 5** : "tool response max 25k tokens" — aucune source primaire confirmant ce chiffre exact comme limite Claude Code générique. Le 25k existe uniquement comme budget skills post-compaction (claim 4).
- **Claim 11** : "compute allocator 1% tokens en prod" — absent du transcript Thariq Agent SDK Workshop disponible. Hypothèse : provient d'un autre talk non transcrit. À retrancher ou retrouver une source.

### Corrections d'attribution à faire dans les notes canoniques

| Claim | Attribution erronée | Attribution correcte |
|---|---|---|
| Advisor strategy 5× | "Cat Wu" ou générique | **Angela Jiang, Head of Claude Platform Product** |
| Scaffolding holds back | "Cat Wu" ou "Anthropic" | **Lisa Crofoot, PM research** |
| +300% PRs | "Anthropic" ou "Boris" | **Noah Zweben (son équipe, 3 mois)** |
| +200% PRs/eng | "Boris" | **Cat Wu (org Anthropic)** |
| 2-agent init+coding | générique Anthropic | **Justin Young, MTS Anthropic** |
| 259 PRs/30j | Sequoia | **Threads Boris ~déc 2025, Opus 4.5** |
| 150 PRs/jour record | "régulier" | **Sequoia avril 2026, "record" exceptionnel, "few dozen" régulier** |

### Sources prêtes à citer (URLs durables)

- `code.claude.com/docs/en/sub-agents` — sub-agent context window
- `code.claude.com/docs/en/skills` — skills budget 5k/25k post-compaction
- `code.claude.com/docs/en/commands` — table commands officielle
- `code.claude.com/docs/en/slash-commands` — alias `code.claude.com/docs/en/commands`
- `anthropic.com/engineering/effective-harnesses-for-long-running-agents` — Justin Young
- `agentskills.io` + `agentskills.io/specification` — spec ouverte
- `github.com/agentskills/agentskills` — repo officiel spec
- `github.com/trailofbits/claude-code-config` — anti-rationalization Stop hook
- `youtube.com/watch?v=TqC1qOfiVcQ` — Thariq Agent SDK Workshop
- `youtube.com/watch?v=6amLO7I9xdg` — CwC London Opening Keynote (Cat/Lisa/Angela/Katelyn/Boris)
- `youtube.com/watch?v=SlGRN8jh2RI` — Boris Sequoia AI Ascent 2026
- `youtube.com/watch?v=78EYLieMpvc` — Erik Schluntz "Vibe Coding in Production" CwC SF
- `threads.com/@boris_cherny/post/DSxC69PCCz_` — 259 PRs/30j Opus 4.5 (déc 2025)
- `chrisebert.net/notes-from-code-with-claude-2026/` — Noah Zweben +300%

---

## Pas d'invention. Pas de paraphrase si verbatim accessible.

Tous les claims avec verdict CONFIRMÉ ci-dessus ont été vérifiés contre la source primaire correspondante. Les claims 5 et 11 sont explicitement marqués non-arbitrés et NE DOIVENT PAS apparaître dans les notes canoniques avec ces chiffres précis. Les claims 2 et 7 nécessitent une reformulation pour distinguer correctement les sources/attributions.

Lien : voir aussi [[recherche-youtube-watch-vibe-coding]] pour les transcripts complets et [[raisonnement-22mai-doctrine-vs-enforcement]] pour la convergence avec la révision doctrine forge.
