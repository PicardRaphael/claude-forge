---
titre: "Thariq Shihipar"
resume: "Skills author Claude Code, 9 catégories skills LinkedIn mars 2026, Agent SDK Workshop 3-way trade-offs, 'HTML is the new markdown' Code with Claude SF"
aliases:
  - "thariq"
  - "@trq212"
  - "thariq shihipar"
  - "thariq-shihipar"
  - "thariq skills"
  - "Thariq Anthropic"
  - "skills author claude code"
  - "9 categories skills"
  - "compute allocator"
  - "HTML is the new markdown"
role: "Skills Author, Claude Code team"
affiliation: "Anthropic"
derniere-maj: 2026-07-27
auteur: claude
sources:
  - "https://x.com/trq212"
  - "https://linkedin.com/in/thariq — post 17 mars 2026"
  - "Code with Claude SF, 6-7 mai 2026 — Agent SDK Workshop"
  - "Code with Claude SF, 6-7 mai 2026 — talk 'How I AI: HTML is the new markdown'"
type: leader
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#org/anthropic"
---
## QUI

Thariq Shihipar — auteur du système de **skills** Claude Code, équipe Anthropic Claude Code. Présent partout où la doctrine skills/SDK est formalisée : LinkedIn (post 9 catégories, 17 mars 2026), Code with Claude SF mai 2026 (Agent SDK Workshop + talk "HTML is the new markdown").

Twitter/X : [@trq212](https://x.com/trq212).

## POURQUOI EST PERTINENT

Thariq est **le référent doctrinal du système skills** — sa parole prime sur celle d'observateurs externes quand il s'agit de "qu'est-ce qu'une skill bien faite". Trois apports majeurs en 2026 :

1. **9 catégories skills** (LinkedIn, 17 mars 2026) — taxonomie complète, ordre verbatim.
2. **Agent SDK Workshop** (Code with Claude SF, mai 2026) — 3-way trade-offs Tools/Bash/Code gen, Swiss cheese defense, anti-pattern "50-100 tools".
3. **"HTML is the new markdown"** (Code with Claude SF) — doctrine "compute allocator" : 99% des tokens à la planification.

Il porte aussi la formulation "lethal trifecta" en pratique Anthropic — terme **forgé par Simon Willison juin 2025**, repris/diffusé par Thariq mais pas inventé par lui.

## CONTRIBUTIONS CLÉS

### Les 9 catégories de skills (LinkedIn, 17 mars 2026) — ORDRE VERBATIM

Verbatim exact, dans l'ordre publié :

1. **Library & API Reference**
2. **Product Verification**
3. **Data Fetching & Analysis**
4. **Business Process & Team Automation**
5. **Code Scaffolding & Templates**
6. **Code Quality & Review**
7. **CI/CD & Deployment**
8. **Runbooks**
9. **Infrastructure Operations**

L'ordre n'est pas arbitraire : il va de la couche **référence/savoir** (1-2) vers la couche **action/exécution** (8-9), avec dev/qualité au milieu (5-7). Une skill bien rangée trouve une de ces catégories sans tordre la définition.

### Agent SDK Workshop — 3-way trade-offs (Code with Claude SF, 6-7 mai 2026)

La décision **comment exposer une capacité à l'agent** :

| Voie | Caractère | Bon pour |
|------|-----------|----------|
| **Tools (MCP)** | atomic, non-reversible | actions discrètes à effet de bord clair (créer ticket, envoyer mail) |
| **Bash** | composable, exploratoire | exploration d'un système, chaînage ad hoc, débug |
| **Code gen** | dynamique | data analysis, transformation, calcul non-trivial |

Pas "MCP partout" — chaque voie a son créneau. Anti-pattern explicite : enfiler 50-100 tools MCP → **"le modèle se perd"**.

### Swiss cheese defense

Doctrine sécurité agents : **plusieurs couches de défense imparfaites** > une seule couche parfaite. Comme le fromage suisse, les trous d'une couche sont couverts par la couche suivante. Implication concrète : combiner permissions + hooks + classifier + sandbox, pas miser sur un seul mécanisme.

### Talk "How I AI: HTML is the new markdown" — Code with Claude SF

Verbatim :

> "99% of your AI-generated tokens should go to planning, interfaces, and communication — not production code."

> "We're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on."

Doctrine **compute allocator** : la valeur humaine n'est plus dans l'écriture du code, mais dans le **choix de l'allocation compute**. Quel projet mérite quoi, quand, à quel modèle, sur quel chemin. Le code n'est qu'un sous-produit de l'allocation.

### Lethal trifecta — attribution correcte

Thariq diffuse et applique le concept, mais le **terme "lethal trifecta" a été forgé par Simon Willison en juin 2025** (private data access + untrusted content + external communication = exfiltration). À citer comme "lethal trifecta (Simon Willison, repris par Thariq Shihipar dans la doctrine skills Anthropic)".

## VERBATIM NOTABLES

> "99% of your AI-generated tokens should go to planning, interfaces, and communication — not production code."

> "We're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on."

> "Le modèle se perd quand on lui donne 50-100 tools."
— Agent SDK Workshop, paraphrase fidèle.

> "Gotchas = highest-signal content in a skill."
— Doctrine skills antérieure, reprise depuis l'article LinkedIn "Lessons from Building Claude Code: How We Use Skills".

## WIKILINKS

- [[comment-ecrire-claudemd]]
- [[comment-creer-skill]]
- [[mcp-vs-skills-doctrine]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[comment-creer-skill|Skills Best Practices]]
- [[Boris Cherny]] — co-doctrine Claude Code
- [[Erik Schluntz]] — co-architecture agents
- [[MOC-Leaders]]

## SOURCES

- Twitter : https://x.com/trq212
- LinkedIn post "Lessons from Building Claude Code: How We Use Skills" + post 9 catégories (17 mars 2026)
- Code with Claude SF, 6-7 mai 2026 — Agent SDK Workshop (3-way trade-offs, Swiss cheese, anti-pattern 50-100 tools)
- Code with Claude SF, 6-7 mai 2026 — talk "How I AI: HTML is the new markdown"
- Simon Willison, juin 2025 — terme original "lethal trifecta"
- Recherche vault : `0-Inbox/_chantier-22mai/recherche-youtube-talks.md`
- Recherche vault : `0-Inbox/_chantier-22mai/recherche-x-twitter-leaders.md`


---

## AJOUT 27 juillet 2026 — fireside AIEWF + system prompt −80 %

- Fireside avec Simon Willison + Cat Wu (21 juil.) — capitalisé dans [[fireside-cat-wu-thariq-aiewf-2026]]. Ses apports propres : « **Workflows… it's Claude not just prompting a single subagent, but prompting the orchestration of many subagents** » / « It's just Claude prompting Claude all the way down » ; tools « more of a biology than a physics » ; grep/glob supprimés pour bash natif ; mémoire Claude Tag = « a markdown file per channel » ; pro-rewrite (« a codebase is a spec, and maybe it's the only copy of the spec that you have »).
- **24 juil.** (X @trq212, 3,9M vues) : « **We removed ~80% of the Claude Code system prompt for our newest models** » + leçons system prompts/skills/CLAUDE.md — la confirmation primaire du chiffre du fireside.
- Keynote séparée AIEWF sur le « loop engineering » (recap tiers ChatForest) — VOD à surveiller.

## AJOUT 27 juillet 2026 (bis) — fireside SPC × Evan Tana (transcript intégral local)

Vidéo « Anthropic Engineer on How to Get the Most Out of Claude Code » (South Park Commons, YouTube `O-1VXHRlH54`), enregistrée **le jour de la sortie d'Opus 4.8 + workflows (28 mai 2026)**, redevenue virale fin juillet via reposts X. Transcrite intégralement le 27 juil. (pipeline x-read → ffmpeg → faster-whisper). ⚠️ Le tweet viral @cnemalek (24 juil., ~52K vues, en arabe) lui fait dire « plus besoin d'écrire des prompts, le nouveau métier est le Graph Engineering » — **le transcript ne contient AUCUNE occurrence de "graph engineering"** : hijacking du buzz sur une vidéo antérieure (cf [[graph-engineering-buzz]]).

Apports propres (au-delà du fireside AIEWF) :

- **Capability overhang** (son concept structurant) : « models are smarter than the harness or the interaction with the user allows them to express » — un « forever problem » : si on gelait les modèles aujourd'hui, ~6-12 mois de découverte d'overhang restants. Les modèles progressent « in these spiky, non-intuitive ways ». Exemple : la thèse 2024 « 100M-token context windows » vs la réalisation Claude Code « what if the models can build their own context ».
- **Plan mode en voie d'obsolescence interne** : « a lot of us on the team have stopped using plan mode because the model just thinks correctly » (génération Opus 4.7/4.8) — l'overhang se referme feature par feature.
- **Workflows = custom harness on the fly** : deep research hier = harness codé à la main ; aujourd'hui « Claude makes that harness on the fly and then executes it ». Sa réponse canonique au capability overhang.
- **« RAG especially for context search is now maybe an anti-pattern — you should use grep instead »** : verbatim fort. Converge avec la position Cline/no-index (cf [[intelligence-de-code-build-vs-buy]]). Périmètre : la recherche de contexte code des agents — le RAG produit/documentaire ([[rag-architecture]]) n'est PAS visé.
- **« Deleting stuff is really important »** : le piège startup = un memory system V1 bespoke jamais remplacé (« founders build a V1 and are never able to hire someone to build the V2 ») ; Opus 4.7/4.8 « really good at writing and reading memory off your files » → supprimer le scaffolding quand le modèle sait faire.
- **Évals « not a zero-to-one thing »** : en 0→1, itérer vite + intuition ; les évals servent à maintenir/améliorer l'existant + donner de la légibilité quand l'équipe grandit. Concevoir des évals = « very high skill people doing very honestly boring work » (conseil carrière : « choose something low status — evals are easily it »). Impossible d'anticiper toutes les évals — ex. le « stop early eval » ne se découvre qu'après avoir observé le problème.
- **Méta-prompts** : grille *known knowns / unknown knowns / known unknowns / unknown unknowns* pour choisir comment prompter ; « **interview me about this problem** » (via AskUserQuestion, son outil) ; explorations design en HTML jetable — « what's the cheapest way to figure out if this is the thing that you want ».
- **Long-running tasks** : il préfère les tâches courtes, sauf ambition claire spéccée up front ; les users qui saturent le plan Max20X sur-transforment en long-running (« five verification agents… running for 12 hours, but maybe you didn't need the 12 hours »).
- Politesse avec Claude : recherche interne sur les émotions — la méchanceté « activates this "person is being mean" feature » et guide les résultats ; pas d'éval « thank you » pour autant.
- Parcours : gaming company VC-backed 5 ans → SPC (squad avec Tom, futur Goodfire) → ~3 mois chez Goodfire → teste Claude Code (ère Opus 4) sur texto d'un ami → « I need to work at Anthropic, it doesn't matter what they want me to do » → embauché demo designer, bascule très vite équipe Claude Code. Créateur d'AskUserQuestion.
