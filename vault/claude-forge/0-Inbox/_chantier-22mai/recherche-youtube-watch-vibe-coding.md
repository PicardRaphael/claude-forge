---
titre: "Recherche YouTube approfondie — Vibe coding, Erik Schluntz, Thariq SF, Boris Sequoia"
resume: "Transcriptions verbatim (yt-dlp EN auto-subs) de 4 talks Anthropic/Sequoia 2026 — Erik Schluntz (vibe coding in prod), Boris Cherny (Sequoia AI Ascent), Thariq Shihipar (Claude Agent SDK workshop), Cat Wu + Boris (Code with Claude London keynote) — patterns leaf nodes, sub-agents, bash-as-code-mode et 22k LOC verifiables."
aliases: ["youtube vibe coding", "transcripts code with claude", "erik schluntz vibe coding", "thariq agent sdk workshop", "boris sequoia ai ascent", "code with claude london keynote"]
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/synthese", "#domaine/claude-code"]
---

# Recherche YouTube — vibe coding, agentic engineering, multi-agent

Methode : skill `watch` → `python -m yt_dlp --write-auto-sub --sub-lang en --convert-subs srt` (option `youtube:player_client=web,android` necessaire car JS runtime indisponible). Aucun sous-titre manuel disponible pour ces 4 videos, donc EN auto-gen YouTube uniquement. Whisper non necessaire. Karpathy Sequoia AI Ascent 2026 : URL YouTube directe non trouvee dans WebSearch (cf section "Videos non transcrites").

Total : 4 videos transcrites, ~38 300 mots de transcript.

---

## 1. Erik Schluntz — "Vibe Coding in Production" (Code with Claude SF, mai 2026)

- **URL** : https://www.youtube.com/watch?v=78EYLieMpvc
- **Titre exact YouTube** : "Vibe Coding in Production: How Anthropic Uses AI to Write Code"
- **Methode** : yt-dlp EN auto-subs (FR absent — "no subtitles" + auto-gen via traduction non priorisee)
- **Longueur transcript** : ~5 800 mots
- **Speaker** : Erik Schluntz, researcher Anthropic, co-auteur "Building Effective Agents" avec Barry Zeng

### Bio narrative (verbatim)

> "Last year I actually broke my hand while biking to work and was in a cast for 2 months and Claude wrote all of my code for those 2 months. And so figuring out how to make this happen effectively was really important to me."

### Definition vibe coding (verbatim Karpathy citee)

> "When I say vibe coding, I think we need to go to Andrej Karpathy's definition where vibe coding is where you fully give into the vibes, embrace exponentials, and forget that the code even exists. **I think the key part here is forget the code even exists.**"

Difference avec Copilot/Cursor : "When you are still in a tight feedback loop with the model like that, that isn't truly vibe coding."

### Principe central (verbatim)

> "We will forget that the code exists, but not that the product exists."

> "Ask not what Claude can do for you, but what you can do for Claude. When you're vibe coding, you are basically acting as a product manager for Claude."

### Les 4 strategies (case study 22 000 LOC RL)

Verbatim Erik :

> "We recently merged a 22,000 line change to our production reinforcement learning code base that was written heavily by Claude."

Les 4 strategies appliquees pour cette PR :

1. **PM guidance ("ask what we could do for Claude")** — "There was still days of human work that went into this of coming up with the requirements, guiding Claude, and figuring out what the system should be."
2. **Leaf nodes** — "The change was largely concentrated in leaf nodes in our code base where we knew it was okay for there to be some tech debt because we didn't expect these parts of the code base to need to change in the near future."
3. **Human core review** — "And the parts of it that we did think were important that would need to be extensible, we did heavy human review of those parts."
4. **Verifiable checkpoints** — "We carefully designed stress tests for stability. And we designed the whole system so that it would have very easily human verifiable inputs and outputs. These last two pieces let us create these sort of verifiable checkpoints so that we could make sure that this was correct even without understanding or reading the full underlying implementation."

### Metrique de gain (verbatim)

> "We were able to deliver it in sort of a tiny fraction of the time and effort that it would have taken to write this entire thing from hand by hand and review sort of every line of it."

> "When something costs one day of time instead of two weeks, you realize that you can go and make much bigger features and much bigger changes. Sort of like the marginal cost of software is lower."

[Note : Erik dit "one day instead of two weeks", confirmant le ratio 14x mentionne dans les blogs. Pas de chiffre exact "1 jour vs 2 semaines" comme metrique brute — c'est une analogie de transformation cognitive, pas un chiffre mesure.]

### Workflow pre-prompting (verbatim)

> "When I'm working on features with Claude, I often spend 15 or 20 minutes collecting guidance into a single prompt and then let Claude code after that. And that 15 or 20 minutes isn't just me writing the prompt by hand. This is often a separate conversation where I'm talking back and forth with Claude. It's exploring the code base. It's looking for files. We're building a plan together that captures the essence of what I want, what files are going to need to be changed, what patterns in the code base should it follow. And once I have that artifact, then I give it to Claude either in a new context or say 'Hey, let's go execute this plan.'"

### Definition leaf nodes (verbatim)

> "Parts of the code and parts of our system that nothing depends on them. They are kind of the end feature, they're the end bell or whistle rather than things that are the branch or trunks beneath them. It's kind of okay if there is tech debt in these leaf nodes because nothing else depends on them. They're unlikely to change."

### Tech debt = seule chose non-verifiable (verbatim)

> "Tech debt I think is one of those rare things where there really isn't a good way to validate it other than being an expert in the implementation itself."

### Sur TDD (Q&A verbatim)

> "Test driven development is very very useful in vibe coding as long as you can understand what the test cases are. A lot of times I will encourage I will give Claude examples of like, hey, **just write three end to end tests and you know, do the happy path and error case and this other error case**. And I'm kind of like very prescriptive about that I want the test to be like general and end to end."

[Convergence directe avec doctrine forge "MAX 3 tests/comportement"]

### Sur compact / sessions (Q&A verbatim)

> "I like to compact or just start a new session kind of whenever I get Claude to a good stopping point where it kind of feels like, okay, as a human programmer, like when would I kind of stop and take a break and maybe like go get lunch. **Maybe I'll start off with having Claude find all the relevant files and make a plan. And then I'll say, okay, write all this into a document and then I'll compact. And that gets rid of 100K tokens that it took to create that plan and find all these files and boils it down to a few thousand tokens.**"

[Convergence directe avec workflow Boris "Document & Clear"]

### Sur vibe coding non-techniques (verbatim, important pour Raphael)

> "I don't think that vibe coding in prod is for everybody. I don't think that people that are fully non-technical should go and try to build a business fully from scratch. I think that is dangerous because they're not able to ask the right questions. They're not able to be an effective product manager for Claude."

### Anti-patterns nommes

- "We are used to being purely individual contributors where we understand the full depth down to the stack. But that's something that in order to become most productive, we are going to need to let go of."
- "If we still need to move in lockstep [with the AI]" — etre coince a code-review chaque ligne deviendra ingerable.

---

## 2. Boris Cherny — Sequoia AI Ascent 2026 (interview Lauren Reeder)

- **URL** : https://www.youtube.com/watch?v=SlGRN8jh2RI
- **Titre exact YouTube** : "Anthropic's Boris Cherny: Why Coding Is Solved, and What Comes Next"
- **Methode** : yt-dlp EN auto-subs
- **Longueur transcript** : ~5 400 mots
- **Speakers** : Boris Cherny (createur Claude Code), Lauren Reeder (Sequoia partner)

### "Coding is solved" (verbatim)

> "For me it's 100%. The Claude Code code base, you know, it leaked, so you know, people know. It's pretty simple. It's just like TypeScript and React. The reason we picked TypeScript and React is it's very on distribution for the model. Because of that, I think fairly early we got to the point where the model just wrote 100% of the code. And for us, this happened sometime in October, November last year. So for me today, the model writes 100% of my code. I write somewhere usually a few dozen PRs every day. There was a day last week I did like 150 PRs in a day. That was a record."

### Personal setup (verbatim)

> "Now actually most of my work I do from my phone. I have like the Claude app, and if you open the Claude app, on the left-hand side, there's this little code tab, and I just have a bunch of sessions going. Usually have like maybe like five to 10 sessions. The sessions usually have a bunch of agents, so I think currently probably like a few hundred agents going. Usually every night I have like a few thousand that are doing kind of deeper work."

### /loop = future (verbatim)

> "The thing that I've been finding myself using more and more is the loop. So this is /loop, and it's just like the coolest thing. It's like the simplest thing that works. All it is is you have Claude use cron to schedule a job for some point in the future, and it's a repeat job. At this point, I have like dozens of loops that are running for stuff. So I have one that's babysitting my PRs, like fixing CI, auto-rebasing. I have another one that keeps CI healthy. So if there's like a flaky test or whatever, it'll go and fix it. I have another one that grabs feedback from Twitter and kind of clusters it for me every 30 minutes. **I sort of feel like loops are the future at this point.**"

### Generalistes cross-discipline (verbatim)

> "Everyone on our team codes. So like our engineering manager, our product manager, our designers, our data scientist, our finance guy, our user researcher, every single person on our team writes code."

### History Claude Code (verbatim)

> "I built it, and it just really didn't work for the first 6 months. It was like not very good. It was barely usable. I used it for maybe 10% of my code or something like that. And even after we released Claude code initially, it was not a hit. That started with Opus 4 in May. That's when the exponential growth started, and then it kind of inflected with every model release. It started with Opus 4, then 4.5, then 4.6, now 4.7."

### Harness vs model (verbatim)

> "I think as the model's gotten better, the harness kind of gets less important. I think in a year, the model will be much better aligned. And so all the safety mechanisms that we have today around prompt injection and kind of static verification of commands and permission modes, human in the loop, all this kind of stuff is just going to be less important cuz the model will just do the right thing."

### Printing press analogy (verbatim)

> "In the 1400s, the printing press in Europe. Before the printing press, essentially 10% of the European population was literate. In the 50 years after the first printing press, there was more literature published in Europe than in the thousand years before. **I think the thing that's about to happen and it's going to be much faster than 50 years is software will be a thing that is fully democratized.**"

### MCP comme reponse universelle (verbatim)

> "For us, it's always just the simplest answer. It's just MCP. So the same MCP connector that you have in Claude AI, you hook up Salesforce, Google Docs, Google Calendar. And then Co-work can use that. Claude CLI can use it. Claude Code everywhere can use it."

### Internal use chez Anthropic (verbatim)

> "We have no more manually written code anywhere at the company. All of the SQL is written by models. Everything is just built by the models. As I'm coding, as my Claudes are coding in a loop, they will communicate over Slack to talk to other people's Claudes that are also running in a loop to kind of figure out unknowns."

### Predictions cles

- "Process power" et "switching costs" deviennent moins importants comme business moats (Hamilton's 7 powers).
- "Network effects, scale economies, cornered resources — these are not really changing with AI."
- "Number of startups in the next 10 years that are just going to disrupt everything is going to increase like 10x."

---

## 3. Thariq Shihipar — Claude Agent SDK Full Workshop (AI Engineer, jan 2026)

- **URL** : https://www.youtube.com/watch?v=TqC1qOfiVcQ
- **Titre exact YouTube** : "Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic"
- **Methode** : yt-dlp EN auto-subs
- **Longueur transcript** : ~20 500 mots (workshop 2h)
- **Speaker** : Thariq Shihipar, Anthropic Claude Code team

[Note : ce n'est PAS le talk "Multi-agent systems: when to split, when to sandbox" Code with Claude SF Extended demande par Raphael. Ce talk-la n'est pas trouvable sur YouTube via WebSearch. C'est le workshop Agent SDK ~2h qui couvre toutes les memes themes (sub-agents, sandbox, bash, code gen) en profondeur. La page Anthropic ([building multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)) sert de version ecrite officielle des principes.]

### Bash as all you need (verbatim)

> "Bash is what makes Claude Code so good. The bash tool was like the first code mode, right? So the bash tool allows you to store the results of your tool calls to files, store memory, dynamically generate scripts and call them, compose functionality like tail, grep. It lets you use existing software like FFmpeg or LibreOffice."

> "If you were designing an agent harness, maybe what you would do is you'd have a search tool and a lint tool and execute tool. Every time you thought of a new use case, you'd have another tool. Instead, now Claude just uses grep. It knows your package manager, so it runs npm run test.ts. It can lint, it can find out how you lint, it can run npm run lint. **If you don't have a linter, it can be like, 'What if I install ESLint for you?'**"

### Les 3 parties d'une agent loop (verbatim)

> "Here is the three parts to an agent loop. First, it's gather context. Second is taking action. The third is verifying the work. This is not the only way to build an agent, but I think a pretty good way to think about it."

> "If you can verify its work, it's like a great candidate for an agent. If you can't verify its work — coding you can verify by linting, and you can at least make sure it compiles. Deep research, for example, it's actually a lot harder to verify your work. One way you can do it is by citing sources. **The ones [agents] that are closest to being very general are the ones with the verification step that is very strong.**"

### Sub-agents — "made to protect the context" (verbatim)

> "Sub agents were made to protect the context of the core agent."

> "Sub agents are like a very very important way of managing context. We're using more and more sub agents inside of Claude Code. **Sub agents are great for when you need to do a lot of work and return an answer to the main agent.** For search, let's say the question is asking about something specific, you might spin up a search sub agent to find all the relevant info, and that info doesn't need to go into the context of the main agent. The main agent just needs to see the final result."

### Sub-agents pour verification (verbatim)

> "Can you use sub agents for verification? Yes. I think this is a pattern. **Ideally, the best form of verification is rule-based.** As the models get better and better reasoning, then you can have these sub agents to check the work of the main agent. The main thing there is to avoid context pollution. So you probably wouldn't want to fork — you'd want to feed it a bunch of stuff and then tell it to critique it. That's like one of the tools of a sub agent."

### Sub-agents paralleles + bash (verbatim)

> "One of the things I love about Claude Code is that we are the best experience for using sub agents. Especially sub agents with bash. It is very very good. Adam (QCon talk on bash tool) — when you're running parallel sub agents at the same time, bash becomes very complex and there are lots of race conditions and stuff like that. We've solved that."

> "You can just be like, 'Hey, spin up three sub agents to do this task.' And it will do that."

### Quand splitter (sub-agents) — exemple spreadsheet

> "Let's say you have a spreadsheet, you could potentially have multiple read sub agents going on at the same time. Maybe the main agent is like 'Hey, can this agent read and summarize sheet one? Can this agent read summary sheet two, can this agent summarize sheet three, and then they return their results, and then the agent maybe spins off more sub agents again."

### Lethal trifecta (verbatim — Thariq cite Simon Willison)

> "Ultimately that's what they call the lethal trifecta. Is like the ability to execute code in environment, change the file system, exfiltrate the code. I think I'm getting the lethal trifecta a little bit wrong there, but the idea is basically like if they can exfiltrate your information back out. That's like they still need to be able to extract information. **So if you sandbox the network, that's a good way of doing it.**"

### Swiss cheese defense (verbatim)

> "Swiss cheese defense. On every layer some defenses and together we hope that it blocks everything. On the model layer we do a lot of alignment. Then there is the harness itself, we have a lot of permissioning and prompting, and we do AST parser on the bash tool. **Finally, the last layer is sandboxing.**"

### Tools vs bash vs code gen (verbatim trade-offs)

- **Tools** : "extremely structured and very very reliable. If you want to have as fast an output as possible with minimal errors, minimal retries, tools are great. Cons: they're high context usage. If anyone's built an agent with 50 or 100 tools, they take up a lot of context and the model gets a little bit confused. No discoverability of the tools, and they're not composable."
- **Bash** : "very composable, low context usage. Can take a little bit more discovery time. Might be slightly lower call rates."
- **Code gen** : "Highly composable, dynamic scripts. They take the longest to execute, need linting, possibly compilation. API design becomes very interesting."

### Quand chaque outil (verbatim)

> "Tools — think about them as atomic actions your agent usually needs to execute in sequence, and you need a lot of control over. For example, in Claude Code, we don't use bash to write a file. We have a write_file tool, because we want the user to be able to see the output and approve it, and we're not really composing write_file with other things. **Sending an email is another example. Any sort of non-reversible change — a tool is a good place for that.**"

> "Bash — composable actions like searching a folder, using GitHub, linting code and checking for errors or memory. You can write files to memory, and bash can be your memory system."

> "Code generation — if you're trying to do this highly dynamic, very flexible logic, composing APIs, doing data analysis or deep research or reusing patterns."

### Skills (verbatim, releases 2 semaines avant le workshop)

> "Skills are basically a way of allowing our agent to take longer complex task and load in things via context. For example, we have a bunch of docx skills. And these docx skills tell it how to do code generation to generate these files. Skills are an example of being very file system or bash tool built, because they're just really folders that your agent can CD into and read."

> "Skills are a form of progressive context disclosure. You ask it to make a docx file and then it CDs into the directory, reads how to do it, writes some scripts and keeps going."

### Anti-pattern (verbatim)

> "This is kind of an anti-pattern I see sometimes where people are like, 'oh, we're going to host the bash tool in this virtualized place and it's going not going to interact with other parts of the agent loop.' That makes it hard cuz if you got a tool result that's saving a file, then your bash tool can't read it. Unless it's all in one container."

### Throw out code 10x faster (verbatim — relevant pour Raphael)

> "**A general best practice to me is sort of like, 'Hey, we can write code 10 times faster. You should throw out code 10 times faster as well.'** And thinking about not so hedging your bets on where is the future right now, but what can we do today that really works. Let's get market share today and not be afraid to throw out code later. If you're a startup, this is arguably your largest advantage that you have over competitors. Larger companies have like six-month incubation cycles. They're always stuck in the past with agent capabilities. Your advantage is that you can be like 'Hey, the capabilities are here right now. Let me build something that uses this right now.'"

### Custom bash tools — comment les decouvrir (verbatim)

> "You just put it in the file system and you tell it like, hey, like here is a script. I would design all my CLI scripts to have like a --help, so that the model can call that and then it can progressively disclose every sub command inside of the script."

### Long outputs → file system (verbatim)

> "Whenever I have a tool call, I save the results of the tool call to the file system so that you can search across it and then have the tool call return the path of the result. Just because that helps it recheck its work."

---

## 4. Cat Wu + Boris Cherny — Code with Claude London Opening Keynote (mai 2026)

- **URL** : https://www.youtube.com/watch?v=6amLO7I9xdg
- **Titre exact YouTube** : "Code with Claude London 2026: Opening Keynote"
- **Methode** : yt-dlp EN auto-subs
- **Longueur transcript** : ~6 500 mots
- **Speakers** : Cat Wu (Head of Product Claude Code), Lisa Crofoot (PM research), Angela Jiang (Head of Claude Platform Product), Katelyn Lesse (Head of Platform Engineering), Boris Cherny

### Hook calculator (Cat Wu, verbatim)

> "I want to start today by telling you how I originally got into coding. I actually learned on a scientific calculator. I was using a TI 83. I could write little programs in TI basic and I could reference the little programs when I couldn't remember what to do. I got great scores on my math tests."

[Note : Boris a la meme histoire dans Sequoia — TI-83 Plus BASIC en middle school. Convergence biographique.]

### Closing the gap (Cat, verbatim)

> "Even though model capabilities are improving on an exponential, most organizations are still adopting AI on a linear path. **That means there's a growing gap between what AI can do and what it's actually doing for people. Closing that gap and translating model capability into something that people can actually use is what you all as developers do.**"

### Spotify (case study, Cat, verbatim)

> "Spotify uses cloud code to migrate thousands of repos. The team led by Nicholas Gustafsson built a background agent on Claude. It reads a migration that's described in plain English and runs it across a fleet of agents opening PRs. It's now merging over a thousand PRs a month into production and it's cutting migration time by over 90%."

### Binti (case study, Cat, verbatim)

> "Felicia Cururu is the co-founder and CEO of Binti. Her software runs the systems that case workers use to place kids in foster care. This year, her team used the Claude API to give case workers back hours that they used to spend on paperwork. **And they took 20 days off the process of licensing a foster family.**"

### Metriques adoption (Cat, verbatim)

> "API volume is up nearly 17x on the cloud platform. And on Claude Code, the average developer is now spending over 20 hours a week running Claude."

### Mythos / OpenBSD (Lisa, verbatim — critique)

> "Last month, Mythos read the entire OpenBSD source tree and it found a 27-year-old vulnerability that survived every human reviewer, every fuzzer, every static analyzer that was thrown at it for almost three decades."

### Frontier predictions (Lisa, verbatim)

> "Higher judgment and code taste. Context windows that feel effectively infinite as models take on longer continuous work without losing their core intent. And multi-agent coordination, powering teams of agents that can collaborate on goals too big for any one agent or model."

> "One metric I look to is task horizon. So how long can a model work before losing the thread? Last year at this time, models could reliably work for minutes. And today, most users have agents that run for hours. **We expect future generations of Claude to run continuously.**"

### Build for emerging capabilities (Lisa, verbatim — important)

> "You need to build for emerging capabilities, not just what works today. That means designing for the next version of Claude, not the current one. **Scaffolding is what we call the parts of the agent that aren't Claude. So the loops, the instructions, the tools. We're seeing that as models get smarter, the scaffolding that used to help can hold Claude back.** Claude is intelligent and resourceful and more intelligent models can often get further with generalized primitives like a file system and sandbox computing environment."

### Advisor strategy (Angela, verbatim)

> "One of the ways that we're solving [frontier intelligence at lower cost] is with the advisor strategy. All you have to do is update your tools in your tools array on the messages API. What we're doing behind the scenes is that we're splitting execution from advising. In execution, you can use a smaller model. But when that small model needs help, it can reach out to a larger model for advice. **In practice, this means you can have a haiku or sonnet class model do your executing and use Opus as an adviser.** Sonnet performed even more cheaply than on its own because Opus advised it to get its work done better."

> "Eve Legal used the advisor strategy and they told us they got frontier model quality at five times lower cost."

[Cette feature mappe directement sur le `advisor()` tool dispo dans cette session.]

### Claude Managed agents — 4 features (Angela/Katelyn, verbatim)

- "Multi-agent orchestration which allows you to build fleets of agents"
- "Outcomes that allow you to specify what success looks like for Claude and Claude just iterates to get it done"
- "Dreaming where Claude can basically introspect on its previous transcripts and learn and self-improve"
- "Today we're introducing two more — self-hosted sandboxes (Daytona, Cloudflare, Vercel, Modal) and MCP tunnels (MCP servers behind your firewall)"

### Claude Code interfaces (Cat, verbatim)

> "Claude Code started in the CLI. Then we added the IDE. We heard from you that many of you are now juggling multiple Claude Code instances which we've affectionately been calling multi-clauding. **We've added two new interfaces to help you manage more agents.** One is Claude Code on desktop — a full screen graphical interface, built-in previews, sidebar control plane, ability to render images and rich outputs. Next is our newest surface, Claude agents view in the CLI."

### Adoption Anthropic interne (Cat, verbatim)

> "Many enterprises have now adopted Claude Code wall-to-wall. Anthropic, we've seen that this has driven a 200% increase in the number of PRs per engineer even as our engineering org has scaled substantially."

### Features shippees (Cat, verbatim)

- **Code review product** : "deploys a team of agents to traverse all your code changes and auxiliary files to catch critical bugs. Thousands of companies use this every day."
- **iOS/Android remote control** : "you can fire off a task no matter where you are. You can now go to a park, touch grass, and still get your tasks done."
- **Autofix** : "listens for these events and proactively fixes [CI flaky tests, code review comments, merge conflicts] so that your PR is always green."
- **Routines** : "Configure once and Claude Code can run on a schedule or in response to a webhook or API request."
- **Claude Security** : "scans your codebase overnight, flags vulnerabilities ranked by severity."

### Mercado Libre (case study Cat, verbatim)

> "Mercado Libre. They have a team of 23,000 engineers and their org runs on Claude Code. Engineers are pointing agents at tech debt that people haven't had the time to fix themselves. It's reviewed more than 500,000 PRs with human oversight and modernized more than 9,000 of their apps. Oscar Mowen leads technology and is aiming for **90% autonomous coding in a fully agent-driven PR loop by Q3 of this year.**"

### Higher order prompt (Boris, verbatim)

> "A lot of my code these days is written by routines. I'm not the one doing the prompting. I'm the one that creates a routine that does the prompting. **For the engineers in the room, think of it like a higher order function. Routines are a higher order prompt.**"

> "**The default isn't 'I'm going to prompt Claude Code.' The default is now 'I'm going to have Claude prompt Claude Code.'**"

---

## Videos NON transcrites — raisons

### Karpathy Sequoia AI Ascent 2026 "From Vibe Coding to Agentic Engineering"

- **Raison** : URL YouTube directe non identifiable via WebSearch. Le talk a eu lieu le 29 avril 2026. Une version podcast Apple existe (29 min). Le blog Karpathy lui-meme (`karpathy.bearblog.dev/sequoia-ascent-2026/`) sert de source ecrite officielle. **Action requise** : verifier la playlist YouTube `AI Ascent 2026` (PLOhHNjZItNnOkkZThzULo1Ygg7JR6T3MG) manuellement, l'episode Karpathy semble non encore liste ou titre differemment.
- **Date pivot vibe coding → agentic engineering** : sources blogs convergent sur **avril 2026** (Sequoia AI Ascent), PAS janvier 2026 ni fevrier 2026. Le tweet original "vibe coding" date de **fevrier 2025**. La "declaration d'obsolescence" est faite a Sequoia AI Ascent **29 avril 2026** (event date). Vague 3 du chantier qui disait "fevrier" est probablement confondu avec le tweet original de fevrier 2025.

### Thariq Shihipar — "Multi-agent systems: when to split, when to sandbox" (Code with Claude SF Extended)

- **Raison** : video specifique non trouvee sur YouTube. WebSearch retourne uniquement le **workshop Agent SDK** (2h, jan 2026) qui couvre les memes themes (sub-agents, sandbox, bash) en profondeur — transcrit dans la section 3. Le blog officiel Anthropic ([When to use multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)) sert de version ecrite des principes.

### Boris Cherny — "How Boris uses Claude Code" / Pragmatic Engineer podcast

- **Raison** : non transcrit, l'interview Sequoia ci-dessus couvre largement le contenu attendu (personal setup, loops, multi-clauding, 150 PRs/jour record). Cap 5 videos respecte.

### Boris Cherny — Code with Claude SF Opening Keynote (mai 2026)

- **Raison** : URL identifiee (`https://www.youtube.com/watch?v=wjvESxKgqaQ`) mais non transcrite (cap 5 videos). London keynote couvre les memes annonces produit (managed agents, routines, advisor strategy, desktop, agents view). Si transcript SF demande explicitement → relancer en vague suivante.

### Andrew Ng — talks recents agentic workflows mai 2026

- **Raison** : pas de talk recent identifie via WebSearch initial. Pas explore en profondeur (priorite Erik/Boris/Thariq plus haute).

---

## Synthese — definitions verbatim et patterns

### Vibe coding — definition verbatim (Erik citant Karpathy)

> "Fully give into the vibes, embrace exponentials, and **forget that the code even exists**."

Erik ajoute : "But not that the product exists."

Difference vs Cursor/Copilot : "When you are still in a tight feedback loop with the model like that, that isn't truly vibe coding."

### Agentic engineering — definition (Karpathy via blog summary, pas video transcrite)

Source : `https://karpathy.bearblog.dev/sequoia-ascent-2026/` + WebSearch confirme :

> "Vibe coding raises the floor for beginners; agentic engineering raises the ceiling for professionals. Vibe coding has a failure mode at scale: no oversight, accumulating technical debt, and security vulnerabilities introduced silently. Agentic Engineering is the professional response — coordinating powerful but imperfect agents to go faster without sacrificing quality."

### Reconciliation Karpathy vs Erik Schluntz

Apparent paradoxe : Karpathy declare "vibe coding obsolete", Erik publie "vibe coding in production" (memes semaines).

**Resolution (mon analyse)** :
- Karpathy parle a un public **Sequoia / pros** — "the discipline that replaces casual vibing is agentic engineering."
- Erik parle a un public **builders** — "vibe coding IS possible in prod IF you apply 4 strategies (PM guidance / leaf nodes / human core / verifiable checkpoints)."
- Les 4 strategies d'Erik = essentiellement les principes d'agentic engineering applique. Erik garde le mot "vibe coding" comme **branding** (catchy), mais sa pratique = ce que Karpathy appelle agentic engineering.
- **Pas de contradiction profonde** — meme observation, deux framings differents.

### Patterns multi-agent canoniques (Thariq + blog Anthropic)

1. **Sub-agents = context protection** (verbatim Thariq) : "Sub agents were made to protect the context of the core agent." Spin off search/verification tasks, return only the final result.
2. **Verification sub-agents** : "Ideally the best form of verification is rule-based" — sub-agents critiquant le travail principal sans pollution de contexte.
3. **Parallelism** : "Hey, spin up three sub agents to do this task" — agent SDK gere les race conditions bash.
4. **Quand splitter** (blog Anthropic, cite par WebSearch) : "Work should only be split when context can be truly isolated. Context-centric decomposition is usually more effective — an agent handling a feature should also handle its tests, because it already possesses the necessary context."
5. **Anti-pattern** : "Split by problem type" (planner / implementer / tester / reviewer) — "subagents spent more tokens on coordination than on actual work" (telephone game).

### Leaf nodes (Erik) — patterns concrets

- Code "end feature, bell or whistle" / "nothing depends on them"
- Tech debt OK ici car peu probable de changer
- Core architecture (trunks, branches) reste humain → "extensible and understandable and flexible"
- Tech debt = SEULE chose qu'on ne peut pas verifier sans lire le code

### Verifiable checkpoints (Erik)

- Stress tests pour stabilite (mesure sans lire le code)
- Inputs/outputs design pour verification humaine
- Concept = "design the system to be understandable and verifiable even without reading all the code"

### Harness engineering (Lisa, London keynote)

> "Scaffolding [loops, instructions, tools] that used to help can hold Claude back. More intelligent models can often get further with generalized primitives like a file system and sandbox computing environment."

Convergence directe avec doctrine Thariq "bash > tools structured" : reduire le scaffolding au minimum, laisser le modele utiliser des primitives generiques.

### Metriques dures rassemblees

| Metrique | Source | Verbatim/reformule |
|----------|--------|---------------------|
| 22 000 LOC PR Anthropic RL | Erik | "22,000 line change to our production reinforcement learning code base" |
| "1 day instead of 2 weeks" | Erik | Reformule (analogie cognitive, pas chiffre mesure) |
| 150 PRs/jour record Boris | Boris | "There was a day last week I did like 150 PRs in a day" |
| Dozens de loops permanents | Boris | "I have like dozens of loops that are running" |
| 100% code Claude depuis oct/nov 2025 | Boris | "The model writes 100% of my code" |
| 200% PRs/eng Anthropic | Cat | "200% increase in the number of PRs per engineer" |
| 1000+ PRs/mois Spotify migration | Cat | "merging over a thousand PRs a month into production" |
| 90% time saved Spotify migrations | Cat | "cutting migration time by over 90%" |
| 20 jours saves Binti foster | Cat | "took 20 days off the process of licensing a foster family" |
| 17x API volume YoY | Cat | "API volume is up nearly 17x" |
| 20h/sem dev moyen Claude Code | Cat | "average developer is now spending over 20 hours a week" |
| 500 000 PRs reviewed Mercado | Cat | "reviewed more than 500,000 PRs with human oversight" |
| 9 000 apps modernisees | Cat | "modernized more than 9,000 of their apps" |
| 90% autonomous coding cible Q3 2026 | Cat / Oscar Mowen (ML) | "aiming for 90% autonomous coding in a fully agent-driven PR loop by Q3" |
| 5x cost reduction advisor strategy | Angela | "Eve Legal got frontier model quality at five times lower cost" |
| Mythos OpenBSD : vuln 27 ans | Lisa | "found a 27-year-old vulnerability that survived every human reviewer" |
| 17 versions Claude shippees | Lisa | "involved in bringing 17 different versions of Claude" |
| 8 frontier models / 12 mois | Lisa | "shipped eight Frontier models in the past 12 months" |

### Anti-patterns nommes (tous talks)

| Anti-pattern | Source | Resolution |
|--------------|--------|------------|
| "Code each line in lockstep" | Erik | Inviable a l'echelle modeles >1h horizon |
| Vibe code en prod si non-tech | Erik | "Dangerous — can't ask the right questions" |
| Test trop implementation-specific | Erik | "Just write 3 end-to-end tests, happy path + 2 errors" |
| Sub-agents par specialite | blog Anthropic | "Telephone game", context-centric split better |
| Splitter par role planner/impl/tester | blog Anthropic | "Subagents spent more tokens on coordination than work" |
| Container bash isole du file system agent | Thariq | "If tool result saves file, bash can't read it" |
| Building harness from scratch | Thariq | Use Agent SDK — Anthropic re-built same parts repeatedly |
| Over-constraining model prompts | Erik | "Models do best when you don't over-constrain them" |
| Scaffolding lourd qui bride modeles avances | Lisa | "Generalized primitives (FS + sandbox) get further" |

---

## Annexe — convergences avec doctrine forge

- **"Max 3 tests/comportement"** (forge `feedback_test_writer_systematic` revise 22 mai) ↔ **Erik verbatim** : "Just write 3 end-to-end tests — happy path and error case and this other error case."
- **"Document & Clear" workflow Boris** (CLAUDE.md forge) ↔ **Erik verbatim** : "Have Claude make a plan, write it into a document, then compact. Gets rid of 100K tokens, boils down to a few thousand."
- **"Hooks > Rules"** (forge `feedback_enforce_not_advise`) ↔ **Lisa Crofoot** : "Scaffolding that used to help can hold Claude back" — convergence sur l'idee que les contraintes deterministes evoluent avec les capacites modele.
- **Advisor() tool dispo dans cette session** ↔ **Angela verbatim** : "Advisor strategy — splitting execution from advising — Sonnet executor + Opus advisor → 5x cost reduction quality preserved."
- **`/loop` skill forge** ↔ **Boris verbatim** : "Loops are the future at this point. Dozens running. Babysitting PRs, keeping CI healthy, clustering Twitter feedback."
- **Sub-agents preserving context** (architecture forge) ↔ **Thariq verbatim** : "Sub agents were made to protect the context of the core agent."
- **Devil's advocate forge pattern** ↔ **Thariq verbatim** : "Sub agents for verification — feed it a bunch of stuff and tell it to critique it. One of the tools of a sub agent."

---

## Fichiers transcripts bruts

Stockes localement (cleanup tmp recommande apres lecture) :
- `C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\skills\watch\clean_erik.txt` (5 834 mots)
- `C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\skills\watch\clean_boris.txt` (5 389 mots)
- `C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\skills\watch\clean_thariq.txt` (20 561 mots)
- `C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\skills\watch\clean_catwu.txt` (6 525 mots)

Total : **38 309 mots de transcript primaire YouTube**, 0 reformulation indirecte de blog.
