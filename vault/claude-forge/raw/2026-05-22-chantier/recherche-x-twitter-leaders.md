---
titre: "Recherche web — X/Twitter leaders Claude Code mai 2026"
resume: "Synthèse des threads/tweets à fort signal des leaders Anthropic et de l'écosystème Claude Code (jan-mai 2026), structurée par auteur avec verbatim, dates et takeaways workflow."
aliases: ["recherche x twitter", "tweets boris thariq karpathy", "leaders claude code 2026", "veille x mai 2026"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/synthese", "#domaine/claude-code", "#source/x-twitter"]
---

# Recherche X/Twitter — Leaders Claude Code (mai 2026)

> Couverture : tweets et threads jan-mai 2026, focus workflow réel, anti-patterns, recaps Code with Claude SF (6 mai) + London (19-20 mai).
> Méthode : WebSearch (snippets Google/X), WebFetch sur Simon Willison live blog. Verbatim quand entre guillemets, sinon `[paraphrase]`. Aucun tweet inventé.

## Handles — état de confirmation

| Leader | Handle X | Statut |
|---|---|---|
| Boris Cherny | `@bcherny` | confirmé |
| Thariq Shihipar | `@trq212` | confirmé |
| Cat Wu | `@_catwu` | **confirmé** (Head of Product Claude Code + Cowork) |
| Lydia Hallie | `@lydiahallie` | confirmé |
| Erik Schluntz | `@ErikSchluntz` | **confirmé** (capital E et S, pas en lowercase) |
| Alex Albert | `@alexalbert__` | confirmé (double underscore) |
| Andrej Karpathy | `@karpathy` | confirmé |
| Simon Willison | `@simonw` | confirmé |
| Addy Osmani | `@addyosmani` | **confirmé** |

---

## 1. Boris Cherny (@bcherny) — créateur Claude Code

### Thread fondateur "How I use Claude Code" — 2 jan 2026
- **Tweet** : https://x.com/bcherny/status/2007179832300581177
- **Reach** : 8M vues
- **Stats Boris** : 259 PRs en 30 jours, 497 commits, 40 000 lignes — 100% générées par Claude Code + Opus 4.5

**Verbatim** : *"I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code; it's intentionally built so you can use it, customize it, and hack it however you like."*

**Workflow extrait du thread** :
1. **5 instances parallèles en terminal** — 5 git checkouts du même repo, tabs numérotés 1-5, system notifications quand input requis
2. **5-10 sessions web supplémentaires** sur claude.ai/code
3. **Opus 4.5 with thinking partout** : *"Even though it's bigger and slower, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."*
4. **CLAUDE.md = mémoire d'équipe** — 2.5k tokens, documente erreurs, style, design, templates PR
5. **Plan mode first** : *"If my goal is to write a Pull Request, I will use Plan mode, and go back and forth with Claude until I like its plan. From there, I switch into auto-accept edits mode and Claude can usually 1-shot it. A good plan is really important!"*
6. **Slash commands inner-loop** — ex `/commit-push-pr` utilisée des dizaines de fois/jour, checked into `.claude/commands/`
7. **Subagents** — `code-simplifier` (refactor post-dev), `verify-app` (E2E test). *"I think of subagents as automating the most common workflows done for most PRs."*
8. **PostToolUse hook** pour formattage — *"handles the last 10% to avoid formatting errors in CI later"*
9. **Pas de `--dangerously-skip-permissions`** — `/permissions` pour pre-allow, settings.json shared
10. **Tag `@.claude` sur PRs collègues** pour ajouter à CLAUDE.md — *"our version of @danshipper's Compounding Engineering"*

[Tweet thread post 5/](https://x.com/bcherny/status/2007179842928947333) — confirme la pratique compounding sur PRs.

### Keynote Code w/ Claude SF — 6 mai 2026

**Verbatim** :
- *"Everything we are seeing today still feels magical to me, and I work on Claude Code every day."*
- *"We think that going forward a lot of code is going to be written in an async way."*

**Shift annoncé** : `[paraphrase]` passage de *"I prompt Claude Code"* → *"Claude prompts Claude Code"* via **Routines** (higher-order prompts async).

**Chart productivity équipe Boris** : PRs hebdo merged sur main passées de ~500 (janvier) à ~1150 (mars) = **+300% en 3 mois**. Goulot : 1 seul engineer dédié docs → routines overnight pour maintenir docs.

**Demo Robobun (avec Jarred Sumner)** : agent autonome Claude Code sur codebase Bun, *"more commits to Bun than Jarred himself"*.

**Takeaway workflow** : plan-first + auto-accept reste la règle. L'innovation 2026 = async via Routines, pas du temps réel.

### Sources
- [Thread Reader scroll](https://threadreaderapp.com/scrolly/2007179832300581177)
- [InfoQ article](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)
- [Pragmatic Engineer interview](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)

---

## 2. Thariq Shihipar (@trq212) — skills author

### Thread "Lessons from Building Claude Code: How We Use Skills" — 17 mars 2026
- **Tweet** : https://x.com/trq212/status/2033949937936085378
- **Contexte** : Anthropic en interne a "des centaines de skills en usage actif"

**Verbatim/extraits clés** :
- `[paraphrase]` Misconception commune : skills = "juste des fichiers markdown". Vrai = dossiers avec scripts, assets, data, dynamic hooks
- *"skills are the abstraction that all agents will build on"* (tweet 21 mars https://x.com/trq212/status/2035372718372073503)
- Les skills clusterisent en **9 catégories récurrentes** — les bonnes skills tombent dans une seule, les confuses en chevauchent plusieurs

### Thread "Seeing like an Agent" — mars 2026
- **Tweet** : https://x.com/trq212/status/2027463795355095314
- **Verbatim** : *"You want to give it tools that are shaped to its own abilities... You pay attention, read its outputs, experiment. You learn to see like an agent."*

### Tweet "Prompt Caching Is Everything"
- **Tweet** : https://twitter.com/trq212/status/2024574133011673516
- `[paraphrase]` — leçon : optimiser cache hit est le levier #1 perf/coût en Claude Code

### Tweet "skills allow you to extend Claude Code"
- **Tweet** : https://x.com/trq212/status/1978937127644668351
- *"Skills allow you to extend Claude Code in new ways using pre-packaged instructions and code. For example, add the docx skill to let Claude Code create word documents. I think skills make Claude Code even better as a general purpose agent, I'm excited to see how you use them!"*

### Pattern "Gotchas section = highest-signal"
- `[paraphrase]` Anthropic interne : tape `/gotcha` → Claude trouve la skill concernée, ouvre le fichier, ajoute à la section Gotchas
- *"the most highest-signal content in any skill is the Gotchas section — these should be built up from common failure points that Claude runs into, and ideally updated over time"*
- Skills sont **append-mostly** — la section gotchas accumule le plus de valeur dans le temps

### Tweet Claude Code channels (MCP Telegram/Discord) — mars 2026
- **Tweet** : https://x.com/trq212/status/2034761016320696565
- *"We just released Claude Code channels, which allows you to control your Claude Code session through select MCPs, starting with Telegram and Discord. Use this to message Claude Code directly from your phone."*

### Takeaway transversal
Pattern Thariq = **observation > prescription**. Sa méthode pédagogique : "regarde ce que fait Claude, formalise après". Cohérent avec doctrine forge "gotchas obligatoires CLAUDE.md".

### Sources
- [Profil x.com/trq212](https://x.com/trq212)
- [Anthropic blog Seeing like an agent](https://claude.com/blog/seeing-like-an-agent)
- [HN discussion](https://news.ycombinator.com/item?id=47196269)

---

## 3. Cat Wu (@_catwu) — Head of Product Claude Code + Cowork

### Verbatim Code w/ Claude SF — 6 mai 2026
*"Thank you for trusting Claude Code on your production databases back when Sonnet 3.7 was our top model."* (via Simon Willison live blog)

### Tweet annonce GA — 4 mars 2025 (contexte)
*"`npm install -g @anthropic-ai/claude-code` — there's no more waitlist. have fun!"* (1M+ vues)

### Tweet 21 mars 2025 (contexte)
*"It's been a big week for Claude Code. We launched 8 exciting new features to help devs build faster and smarter."*

### Vision 2026 (TechCrunch + interviews)
- `[paraphrase]` "AI will anticipate your needs before you know what they are" — proactive AI / Claude understands what you work on
- **Surnommée** avec Boris : *"Anthropic's Batman and Robin"*
- Podcast AI&I avec Dan Shipper (29 oct 2025) : 1h10 sur leçons construction Claude Code

### Note
Cat Wu poste peu de threads techniques publics sur X — son canal principal est **podcasts + keynotes**. Pour workflow concret, voir [interview Lenny Newsletter](https://www.lennysnewsletter.com/p/how-anthropics-product-team-moves) ("How Anthropic's product team moves faster than anyone else").

### Sources
- [Profil x.com/_catwu](https://x.com/_catwu)
- [TechCrunch mai 2026](https://techcrunch.com/2026/05/13/anthropics-cat-wu-says-that-in-the-future-ai-will-anticipate-your-needs-before-you-know-what-they-are/)

---

## 4. Lydia Hallie (@lydiahallie) — Anthropic / Frontend Masters

### Tweet Learning Mode — 18 mai 2026
- **Tweet** : https://x.com/lydiahallie/status/2056420694087594283
- **Verbatim** : *"💯 this is why I really like Learning mode in Claude Code. I personally use this for all my side projects and it keeps me so much sharper, great if you want to use Claude Code but still stay hands-on! /config → Output style → Learning"*

**Takeaway** : pattern **stay-sharp** — utiliser Learning mode pour ne pas dégénérer en pure validation. Aligné Karpathy/Schluntz : éviter le "bottleneck humain qui rubber-stamp".

### Tweet Agent Teams — 5 février 2026
- `[paraphrase]` Annonce support agent teams (research preview) : un lead agent délègue à des teammates en parallèle, qui recherchent/debuggent/buildent en coordination
- Architecture : 1 session = team lead, spawn teammates (full CC instances), shared task list, inbox-based messaging, self-claim work

### Takeaway
Lydia est **voix pédagogique** Frontend Masters → ses tweets visent l'audience dev "j'utilise Claude tous les jours, voilà ce qui marche". Bon proxy pour features qui survivent l'usage réel.

### Sources
- [Profil x.com/lydiahallie](https://x.com/lydiahallie)

---

## 5. Erik Schluntz (@ErikSchluntz) — Head of Programming Agents Anthropic

### Talk "Vibe Coding in Prod (Responsibly)" — Code w/ Claude 2025
- **Tweet release** : https://x.com/ErikSchluntz/status/1951010061871968470 — *"My 'Vibe Coding in Prod (Responsibly)' talk is now live"*
- **YouTube** : https://www.youtube.com/watch?v=78EYLieMpvc
- **Origine** : 2 mois de coding 100% Claude après s'être cassé la main

**Verbatim & concepts** :
- *"Ask not what Claude can do for you, but what you can do for Claude."* → devenir le PM de Claude
- 15-20 min pre-prompt : collecter contexte, explorer codebase, bâtir plan
- **"Forget the code, not the product"** — comme on a oublié l'assembly, on oubliera le code généré
- **Focus "leaf nodes"** : vibe code sur features sans dépendances (bells & whistles). Core architecture = supervision humaine profonde
- *"In a year or two, demanding to read every line of code will make you the bottleneck."*
- **22 000 LOC PR case study** : équipe RL Anthropic, majoritairement Claude. 4 stratégies = (1) deep PM guidance, (2) scope strict leaf nodes, (3) human intervention core, (4) verifiable checkpoints + stress tests long-terme. Résultat : 2 semaines → 1 jour
- **Analogie compiler** : *"Just as with compilers, Claude will get more reliable, trust will develop, and eventually not many people will write code by hand."*

### Tweet Code w/ Claude SF swag — 6 mai 2026
- **Tweet** : https://x.com/ErikSchluntz/status/1925671756611592331
- *"Code with Claude conference has the best swag: Anthropic branded mechanical keyboard caps"* (41.9K vues)

### Tweet historique — 24 fév 2025 (contexte release)
- **Tweet** : https://x.com/ErikSchluntz/status/1894096639968600532
- *"Along with Sonnet 3.7, we released Claude Code..."*

### Takeaway workflow forge
- Le combo **plan upfront 15-20 min + scope leaf-only + checkpoints vérifiables** = inverse exact du "vibe coding" sloppy
- Boris l'a confirmé Anthropic interne : *"100% production code is now AI"*, *"hadn't written a line by hand since October 2025"*
- Le terme "vibe coding" est jugé **counterproductif** par Boris (implique sloppiness)

### Sources
- [Tweet Vibe Coding](https://x.com/ErikSchluntz/status/1951010061871968470)
- [DeepInsightAI résumé](https://deepinsightai.io/how-to-properly-do-vibe-coding/)
- [Eric Jinks notes](https://ericjinks.com/blog/2025/vibe-coding-in-prod/)

---

## 6. Alex Albert (@alexalbert__) — Head of Claude Relations

### Tweet Hooks rollout
- **Verbatim** : *"We've rolled out another update to Claude Code to help customize your workflows: Hooks."*
- Définition : *"Hooks are user-defined shell commands that execute at various points in Claude Code's agent loop, giving users deterministic control over Claude Code's behavior to ensure certain actions always happen at certain times."*

### Tweet "Claude for Excel" — fin 2025
- `[paraphrase]` *"I'm hearing from many folks across finance industry that Claude for Excel is blowing their minds. The agentic coding takeoff but for other fields is coming in 2026."*
- Daniel MacAteer reprise : *"2026: Anthropic personnel are signaling the Claude Code experience for all knowledge workers is coming. First Sholto Douglas and now Alex Albert."* https://x.com/daniel_mac8/status/2005698996749090867

### Conférence quote Code w/ Claude 2026
- `[paraphrase]` hooks = *"red squigglies for agents"* — corrections injectées au moment de l'erreur plutôt que rattrapées en review
- Hooks = seule abstraction qui **ne consomme pas de contexte tant qu'elle ne fire pas**

### Takeaway
Alex Albert = **canal officiel produit**. Aligné doctrine forge : hooks > rules advisory (rule = 80% compliance, hook = 100%).

### Sources
- [Profil x.com/alexalbert__](https://x.com/alexalbert__)
- [Thread Reader](https://threadreaderapp.com/user/alexalbert__)

---

## 7. Andrej Karpathy (@karpathy) — Software 3.0

### Tweet fondateur — 26 janvier 2026
- **Reach** : repo dérivé `forrestchang/andrej-karpathy-skills` → **220 000+ étoiles cumulées** (91k Forrest Chang + 132k mirror multica-ai), 28 jours consécutifs au top GitHub Trending, rang #94 mondial
- **Quote pivot** : *"They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."*
- **Shift personnel** : `[paraphrase]` 80% manual+autocomplete / 20% agents en novembre → 80% agents / 20% touchups en janvier

### Les 4 règles dérivées (CLAUDE.md viral)
1. **Think Before Coding** — ask instead of assuming
2. **Simplicity First** — no abstractions nobody asked for
3. **Surgical Changes** — touch only what you must
4. **Goal-Driven Execution** — define verifiable success criteria

**Verbatim community** : *"Before, I'd ask for a bug fix and get a 40-line diff with type hints, reformatted quotes, and renamed variables mixed in with the actual fix. Now the diff is clean."*

### Sequoia Ascent 2026 — Software 3.0
- **Bearblog** : https://karpathy.bearblog.dev/sequoia-ascent-2026/
- **Verbatim vibe vs agentic** : *"Vibe coding is about raising the floor for everyone in terms of what they can do in software. Everyone can vibe code anything, and that is amazing. Agentic engineering is about preserving the quality bar of professional software. You are not allowed to introduce vulnerabilities because of vibe coding. You are still responsible for your software, just as before."*
- **Verbatim 10x** : *"People used to talk about the 10x engineer. I think this is magnified a lot more. 10x is not the speedup people can gain. People who are very good at this can peak much higher than that."*
- **Insight** : *"traditional software automates what can be precisely specified, while language models automate what can be verified"* → explique pourquoi feedback loops + tests sont load-bearing

### 4 failure patterns (canon vault)
1. silent assumptions never verified
2. hypertrophy of code and abstractions
3. collateral changes never requested
4. absence of verifiable success criteria

### Takeaway forge
Karpathy = **source canonique** pour CLAUDE.md doctrine. Tout déjà capitalisé dans `04-Techniques/` mais à re-checker contre cette liste 4 patterns.

### Sources
- [Sequoia Ascent 2026 - karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)
- [TechTimes article 220k stars](http://www.techtimes.com/articles/316798/20260518/karpathy-inspired-claudemd-passes-220000-combined-github-stars-four-rules-that-stop-ai-breaking.htm)

---

## 8. Simon Willison (@simonw) — live-blogs canoniques

### Live blog Code w/ Claude SF — 6 mai 2026
- **URL** : https://simonwillison.net/2026/May/6/code-w-claude-2026/
- **Format** : capture verbatim des keynotes avec sources

**Annonces majeures captées** :
- Rate limits 5h **doublés** Pro/Max/Enterprise
- Partenariat **SpaceX Colossus** datacenter
- API volume **17x year-on-year**
- **3 nouvelles Claude Managed Agents** : multi-agent orchestration (public beta), Outcomes/iteration loops (public beta), **Dreaming** (overnight self-improvement via session review — research preview)
- **Routines** Claude Code (async higher-order prompts)
- **CI auto-fix** (PRs auto-fixed sans intervention dev)
- Code Review + Security Reviews
- **AUCUN nouveau modèle flagship** annoncé

**Speakers quotes captées** :
- Ami Vora (CPO) : *"Today is about how we are making our products work better for you."*
- Boris (déjà cité section 1)
- Cat Wu (déjà citée section 3)
- Dianne Na Penn : *"Design for the next model"* — build pour capacités proches du futur

**Workflow insights** :
- **Advisor strategy** : petits modèles appellent Opus on-demand → frontier quality à ~5x coût moins
- Équipes qui réussissent focus **automated evals + simple scaffolding + applications novel**

**Strategic takeaway** (Simon's framing) : *"the next year of competitive lift comes from orchestration, not from raw model capability"*

### Sources
- [Live blog Simon Willison](https://simonwillison.net/2026/May/6/code-w-claude-2026/)
- [Pravin Kumar analyse](https://www.pravinkumar.co/blog/code-with-claude-2026-no-new-model)

---

## 9. Addy Osmani (@addyosmani) — Harness Engineering

### Concept "Agent Harness Engineering"
- **Blog principal** : https://addyosmani.com/blog/agent-harness-engineering/
- **O'Reilly Radar** : https://www.oreilly.com/radar/agent-harness-engineering/

**Définition** : *"A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips."*

**Harness = prompts + tools + context policies + hooks + sandboxes + subagents + feedback loops + recovery paths**.

### Le "Ratchet Principle"
- *"the harness only tightens, never loosens"*
- Quand un agent fait une erreur, tu fixes le **harness**, pas l'output → l'erreur ne peut plus arriver
- Erreur = signal permanent qui tighten le harness

### Pattern d'anti-pattern identifié
*"the agent does something dumb, the engineer blames the model, and the blame gets filed under 'wait for the next version'. The harness-engineering mindset rejects that default. The failure is usually legible — the agent didn't know about a convention, so you add it to AGENTS.md; the agent ran a destructive command, so you add a hook that blocks it."*

### Tweet sur Boris — Engineer's value shifts
- **Tweet** : https://x.com/addyosmani/status/2022822356050399673
- *"Boris created Claude Code. His point here is important - when AI handles the code generation, the engineer's value shifts to the decisions above the code: 1. what do we build? 2. why? for whom? 3. and how it all fits together. The bottleneck was always judgment, taste, and systems thinking — AI just made that more obvious."*

### Stat chocs harness > model
- Claude Opus 4.6 dans Claude Code : **58.0% Terminal-Bench 2.0**
- Même modèle dans ForgeCode : **79.8%** = **+21.8 points** par architecture harness seule
- Une équipe : top 40 → top 5 en changeant **uniquement** le harness

### Convergence pattern
- Claude Code, Cursor, Codex, Aider, Cline convergent sur les mêmes patterns harness malgré modèles/équipes différents → signal de "load-bearing scaffolding principles"

### Primitives harness clés
- filesystem/Git pour durable state
- bash execution + sandboxes
- memory/search
- context compaction strategies
- hooks for enforcement
- planner/evaluator splits
- Harness-as-a-Service emergent

### Takeaway pour forge
**Hooks > Rules** doctrine forge = exactement le Ratchet Principle. Déjà aligné. Mais Addy formalise mieux la **discipline systémique** : chaque erreur = bug du harness, pas du model.

### Sources
- [Blog AddyOsmani harness](https://addyosmani.com/blog/agent-harness-engineering/)
- [O'Reilly Radar](https://www.oreilly.com/radar/agent-harness-engineering/)
- [Tweet sur Boris](https://x.com/addyosmani/status/2022822356050399673)
- [Agent Skills blog](https://addyosmani.com/blog/agent-skills/)
- [Claude Code Swarms](https://addyosmani.com/blog/claude-code-agent-teams/)

---

## Code with Claude London — 19-20 mai 2026

**Format** : 2 events séparés
- **Code with Claude London** (19 mai) — main event, livestream
- **Code with Claude Extended London** (20 mai) — founders/early-stage, pas livestream mais enregistré

**Opening keynote** : Angela Jiang, Boris Cherny, Cat Wu, Katelyn Lesse, Lisa Crofoot (9-10am BST)

**Demo Boris** : refunds ACME dashboard avec idempotency / multi-currency / audit logging. Demo de **multiple sessions** dans Claude desktop app + flicker-free mode expérimental teased comme futur défaut.

**Robobun (live coding avec Jarred Sumner)** : agent autonome sur Bun, plus de commits que Jarred lui-même.

Pas de live blog Simon Willison trouvé pour Londres (peut-être pas attendu — couverture SF était la principale).

### Sources
- [Page event Anthropic](https://claude.com/code-with-claude/london)
- [Extended London](https://claude.com/code-with-claude/london-extended)
- [Relve events listing](https://relvehq.com/events/code-with-claude-london)

---

## Patterns transversaux observés (signaux croisés)

### 1. Plan-first universel
Boris, Erik, Karpathy convergent : **15-20 min de planification > 0 min de typing**. Anti-pattern = "open Claude Code, start typing".

### 2. Async > Realtime (mai 2026 shift)
Boris keynote SF : *"a lot of code is going to be written in an async way"*. Routines + Managed Agents + Dreaming = bascule architecturale 2026.

### 3. Compounding par fichier
- Boris : CLAUDE.md équipe + tag `@.claude` sur PRs
- Thariq : `/gotcha` + Gotchas section append-mostly
- Karpathy : 4 rules CLAUDE.md → 220k stars
- Addy : Ratchet Principle (chaque erreur tighten harness)

**Pattern unifié** : tout learning va dans un fichier persistant lu à chaque session. Pas de mémoire = pas de compounding.

### 4. Hooks > Rules (deterministic > advisory)
- Boris : PostToolUse pour format
- Alex Albert : "red squigglies for agents"
- Addy : hook bloque destructif, pas rule advisory
- Doctrine forge déjà alignée (cf rules/devils-advocate, hooks delegate-guard)

### 5. Skills clusterisent en 9 catégories (Thariq)
À vérifier contre les 9 catégories Thariq déjà capitalisées dans le vault `04-Techniques/`.

### 6. Aucun nouveau modèle Code w/ Claude SF
Signal stratégique fort : **2026 = year of harness/orchestration**, pas year of model. Cohérent avec Addy (+21.8 points par harness seul).

### 7. Vibe coding terminologie contestée
- Karpathy : reste utile pour "raise the floor"
- Erik Schluntz : ok si responsibly, focus leaf nodes
- Boris : trouve le terme "actively counterproductive" (implique sloppiness)
→ pour forge : préférer **"agentic engineering"** dans la doctrine.

---

## Anti-patterns détectés à capitaliser

| Anti-pattern | Source | Note forge |
|---|---|---|
| Start typing without plan | Boris, Erik | Renforcer rule architect-first |
| Read every line of code = bottleneck | Erik | À méditer pour code-reviewer agent |
| Blame the model, wait next version | Addy | Tout signaler en harness fix |
| Skills = "just markdown" | Thariq | Skills = dossiers complets (déjà rule forge) |
| `--dangerously-skip-permissions` | Boris (anti) | Ne pas adopter, `/permissions` à la place |
| Vibe code dans le core | Erik | Leaf nodes only |
| Manual docs pour 1150 PRs/sem | Boris | Routines overnight obligatoires si scale |

---

## Cross-pollination possibles avec forge

1. **Routines Anthropic ↔ /schedule + /loop forge** : capitaliser pattern async overnight (déjà skill `dreaming` cible Anthropic — vérifier équiv vault)
2. **CI auto-fix Anthropic ↔ skills forge** : pas encore d'équivalent forge, opportunité
3. **Advisor strategy (small model → Opus on-demand)** : déjà dans forge via tool advisor, mais pattern "à la demande" depuis Sonnet pourrait s'industrialiser
4. **Robobun pattern** : agent autonome sur repo → forge a déjà la doctrine mais pas l'instance pour un repo perso
5. **Learning mode (Lydia)** : à proposer aux devs Neoteem qui rubber-stamp trop vite

---

## Notes méthodologiques

- **Aucun tweet inventé** — quand le verbatim n'était pas accessible, marqué `[paraphrase]`
- **x.com bloque WebFetch direct** (auth wall) → snippets Google + threadreaderapp.com utilisés
- **Skill `x-read` non invoquée** : les snippets étaient suffisants pour cette synthèse. À utiliser si on veut un thread Cat Wu / Lydia exhaustif futur
- **defuddle non utilisé** : Simon Willison répond bien à WebFetch direct
- **Threads non explorés en profondeur** : Sholto Douglas (mentionné par Daniel MacAteer), Jarred Sumner (Robobun), Dan Shipper (Compounding Engineering)

## Pistes pour notes atomiques séparées (suivantes)

1. `04-Techniques/agents/harness-engineering-addy-osmani.md` — formaliser Ratchet Principle
2. `04-Techniques/agents/async-routines-anthropic-mai2026.md` — Routines + CI auto-fix + Dreaming
3. `04-Techniques/prompt-engineering/learning-mode-lydia.md` — pattern stay-sharp
4. `04-Techniques/agents/leaf-nodes-vibe-coding-schluntz.md` — où vibe code OK
5. `05-Leaders/claude-code/cat-wu.md` — fiche manquante probable (à vérifier vault)
6. `05-Leaders/agents/addy-osmani.md` — fiche à créer/MAJ
7. `Knowledge/syntheses/code-with-claude-sf-mai2026.md` — synthèse événement
