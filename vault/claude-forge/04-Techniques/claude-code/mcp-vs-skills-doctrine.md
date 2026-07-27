---
titre: "MCP vs Skills+CLI : quand utiliser quoi (doctrine 2026)"
resume: "Doctrine canonique Anthropic mai 2026 — MCP connecte les données, Skills enseignent le how-to. Boris : MCP simple multi-clients. Thariq : 3-way trade-offs tools/bash/code-gen. Karpathy qmd = CLI+MCP les deux. Lethal trifecta = Simon Willison."
aliases:
  - "mcp vs skills"
  - "mcp ou skill"
  - "quand utiliser mcp"
  - "quand utiliser skill"
  - "doctrine mcp skills"
  - "mcp connects data skills teach how-to"
  - "mcp vs cli"
  - "tools bash code-gen tradeoffs"
  - "lethal trifecta willison"
  - "compute allocator"
derniere-maj: 2026-07-27
auteur: claude
type: technique
sources:
  - "https://www.claude.com/blog/skills-explained"
  - "Code with Claude SF 6-7 mai 2026 — Thariq Agent SDK Workshop"
  - "Code with Claude SF 6-7 mai 2026 — Thariq How I AI HTML markdown"
  - "Boris Cherny — Pragmatic Engineer interview"
  - "Karpathy LLM Wiki Gist 4 avril 2026"
  - "Simon Willison — simonwillison.net/2025/Jun/16/the-lethal-trifecta/"
  - "Simon Willison — simonwillison.net/2025/Oct/16/claude-skills/"
  - "Armin Ronacher — lucumr.pocoo.org/2025/12/13/skills-vs-mcp/"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/mcp"
  - "#domaine/skills"
  - "#doctrine/2026"
---

# MCP vs Skills+CLI : quand utiliser quoi (doctrine 2026)

> Note canonique forge — arbitrage MCP / Skills / CLI selon doctrine Anthropic mai 2026.

---

## QUOI — Définition

**MCP (Model Context Protocol)** = standard ouvert Anthropic pour **connecter Claude à des sources de données** externes (DB, APIs, vaults, services). Un serveur MCP expose des `tools` (atomic, non-réversibles) que Claude appelle directement.

**Skills** = bundles markdown (`SKILL.md` + scripts/ + references/) qui **enseignent à Claude comment faire** une tâche réutilisable. Chargées progressivement (description en métadonnées, body à l'activation).

**CLI / Bash** = exécution de commandes shell que Claude compose dynamiquement. Plus exploratoire et composable que les tools structurés.

**Verbatim Anthropic** :

> "MCP connects Claude to data; Skills teach Claude what to do with that data."
> — [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained)

Les trois sont **complémentaires, pas concurrents**.

---

## POURQUOI — Le problème résolu

Sans cadre, on tombe dans 2 pièges symétriques :

### Piège 1 — Tout en MCP
Conséquence : 50-100 tools chargés, le modèle se perd dans le choix (anti-pattern documenté Thariq).
> "le modèle se perd" — Thariq Shihipar, Agent SDK Workshop

### Piège 2 — Tout en Skills
Conséquence : on réimplémente l'accès aux données (auth, parsing, pagination) à chaque skill au lieu de centraliser.

### Le bon arbitrage
- **Accès données** = MCP (cross-clients, simple, partagé Claude Code + Desktop + Cursor + autres clients)
- **How-to procédural** = Skill (chargement progressif, < 5k tokens budget, partageable agentskills.io)
- **Exploration / composition dynamique** = Bash

---

## COMMENT — Arbitrage par cas d'usage

### Tableau de décision

| Besoin | Solution | Raison |
|--------|----------|--------|
| Lire/écrire dans une DB | **MCP** | Auth + connexion centralisée |
| Lire/écrire dans un vault Obsidian | **MCP** | Index FTS5 partagé, alias expansion |
| Appeler API métier interne | **MCP** | Auth bearer/OAuth managée |
| Lire des fichiers du repo | **Bash** (`cat`, `Grep`, `Read`) | Pas besoin d'abstraction |
| Scaffolder un composant React | **Skill** | Procédure réutilisable, templates |
| Faire un code review | **Skill** | Checklist, patterns à appliquer |
| Lister les commits récents | **Bash** (`git log`) | Composable, exploratoire |
| Analyser des données CSV/JSON | **Bash + code-gen** (`pandas`) | Dynamique selon shape data |
| Approuver un PR / envoyer email | **MCP tool** | Atomique, non-réversible |
| Pipeline déploiement | **Skill** (orchestration) + **Bash** (exec) | Combo |

### Doctrine Thariq — 3-way trade-offs (Agent SDK Workshop)

| Mode | Caractéristique | Quand |
|------|-----------------|-------|
| **Tools (MCP)** | Atomic, non-reversible | `write_file`, `send_email`, `approve_pr` — actions qui DOIVENT être structurées |
| **Bash** | Composable, exploratoire | `ls`, `grep`, `find`, pipelines — exploration et composition |
| **Code gen** | Dynamique, data analysis | Pandas, scripts ad-hoc — quand shape data inconnue d'avance |

> Anti-pattern : 50-100 tools structurés → "le modèle se perd"
> — Thariq, Agent SDK Workshop

### Doctrine Boris — MCP simple multi-clients

Concept Boris (Pragmatic Engineer interview) : MCP est la réponse simple quand on veut le même accès données partagé entre Claude Code + Desktop + Cursor + Goose + Copilot. La formule "cross-surface" parfois attribuée à Boris n'apparaît pas verbatim dans les sources primaires — c'est le concept qui est canonique, pas le terme.

---

## QUAND — Critère d'application

### Utiliser un MCP quand :
- Accès données partagé entre **plusieurs clients** (CC, Desktop, Cursor, etc.)
- Auth/connexion **centralisée** nécessaire (token, OAuth, secrets)
- Action **atomique non-réversible** (write DB, send_email, approve PR)
- L'opération a **moins de 10-15 tools logiques** par serveur (au-delà → splitter)

### Utiliser une Skill quand :
- Procédure **réutilisable** cross-repos
- **Progressive disclosure** souhaitée (description légère, body chargé à l'activation)
- Le savoir-faire est **textuel + scripts**, pas accès données
- On veut partager publiquement (`agentskills.io` spec ouverte adoptée par ~40 produits)

### Utiliser Bash quand :
- Exploration d'un repo / d'un système
- Composition dynamique (pipes, find, grep)
- Tout ce qui est lecture seule rapide
- Quand un tool MCP serait du sur-engineering

### NE PAS utiliser MCP quand :
- Pour exposer **toutes** les opérations possibles d'un système (50+ tools)
- Quand `Bash` ferait l'affaire en 1 ligne
- Quand la donnée est dans le repo (Read suffit)

---

## WORKFLOW — Décider en 3 questions

```
1. Est-ce un ACCÈS DONNÉES externe (DB, vault, API) ?
   → OUI : MCP
   → NON : continuer

2. Est-ce une PROCÉDURE RÉUTILISABLE (how-to) ?
   → OUI : Skill
   → NON : continuer

3. C'est de l'EXPLORATION / COMPOSITION dynamique ?
   → OUI : Bash
   → NON : reconsidérer le besoin
```

### Pattern hybride courant

Une **Skill** orchestre, appelle **MCP tools** pour les données, et compose avec **Bash** pour l'exploration. Exemple : skill `/code-review` lit le diff via `Bash git diff`, cherche prior art via MCP forge-brain, applique checklist via instructions skill.

---

## APPELS — Composants mobilisés

- [[comment-creer-skill]] — création de skill (procédure + structure)
- [[comment-creer-hook]] — quand une règle MCP/Skill doit tenir 100%
- [[comment-ecrire-claudemd]] — où mentionner les MCP du repo
- [[workflow-claude-code-optimal]] — comment MCP/Skills s'inscrivent dans le workflow
- [[pattern-vault-llm-karpathy]] — pattern Karpathy applique les deux (CLI+MCP via qmd)

---

## OPTIMISATION — 3 niveaux

### Niveau basique
- 1-3 MCP servers (data only), 5-10 skills (how-to)
- Pas de tool > 15 par MCP

### Niveau avancé
- MCP custom pour le métier (vault, DB business)
- Skills extraites par domaine (front, back, sécu, sql)
- Frontmatter skills riche (description = trigger directive 3e personne, < 250 chars pour auto-trigger)

### Niveau expert (forge actuel)
- 2 MCP custom distincts : **forge-brain** (vault perso, port 8091) + **obsidian-brain** (vault Neoteem business)
- Stack légère : FastMCP 2 + pyyaml + SQLite FTS5
- Skills + slash commands forge custom (/spec, /recap, /done, /go)
- Skills publiques via agentskills.io quand pertinent

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| MCP centralisé vs tools dispersés | Auth/connexion 1 fois vs N fois, partage cross-clients |
| < 15 tools par MCP server | Évite "le modèle se perd" (anti-pattern Thariq) |
| Skills progressive disclosure | < 5k tokens budget par skill, budget combiné 25k post-compaction (limite Anthropic) |
| Bash pour exploration | Pas de tool inutile, composable, ~0 token de schema |
| agentskills.io spec ouverte | Skill écrite 1 fois utilisable Cursor + Codex + Gemini CLI + Goose + ~40 produits |

### Mesure Ronacher (Sentry MCP)

Source : [lucumr.pocoo.org/2025/12/13/skills-vs-mcp/](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/) (Armin Ronacher, 13 décembre 2025).

Le serveur MCP Sentry pèse **~8k tokens upfront** (schemas tools). À mettre en balance avec : qu'aurais coûté de réimplémenter l'accès Sentry dans 5 skills ?

---

## ANTI-PATTERNS

### Anti-patterns MCP
- ❌ **50-100 tools dans un seul serveur** — "le modèle se perd" (Thariq)
- ❌ **MCP pour ce qu'un `Bash` ferait** — sur-engineering
- ❌ **MCP qui duplique l'accès filesystem natif** — Read/Glob/Grep suffisent
- ❌ **Credentials en clair dans `.mcp.json` versionné** — cf [[erreur-password-postgres-clair-mcp-json]]
- ❌ **MCP sans schema documenté** — Claude ne peut pas l'utiliser correctement
- ❌ **MCP server custom sans `tools_list` testé** : si le handshake `tools_list` retourne un schema invalide (champ manquant, type incorrect), Claude **skip silencieusement** le serveur. Toujours tester en isolation avec `mcp-inspector` ou client minimal avant d'exposer en prod.

### Anti-patterns Skills
- ❌ **Description en 1ère personne** ("I help you...") — toujours 3e personne directive ("Use when...")
- ❌ **Description > 250 chars** = tronquée par system reminder `/skills` → invisible à Claude pour auto-trigger
- ❌ **SKILL.md > 500 lignes monolithique** — déporter dans `references/`
- ❌ **Skills orphelines** dans frontmatter agent sans être référencées dans le body (cf [[feedback_non_invokable_skills_orphan]])
- ❌ **Keyword stuffing dans description** — cf [[e-descriptions-keyword-stuffing]]

### Anti-patterns Bash
- ❌ **Bash où une Skill structurée serait meilleure** (procédure réutilisable)
- ❌ **`Grep`/`Read` brut sur vault MCP-indexé** — utiliser le MCP (cf forge-brain-proactive)
- ❌ **Heredoc pour write disguised** quand agent a `disallowedTools: Write,Edit` (cf [[feedback_da_bash_write]])

### Anti-pattern transversal : Lethal trifecta (Simon Willison)

**Terme forgé par Simon Willison** ([simonwillison.net/2025/Jun/16/the-lethal-trifecta/](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), 16 juin 2025). Repris par l'écosystème Claude Code (Claude for Chrome / browser agents) pour la sécurité prompt injection.

Combinaison toxique d'accès LLM (verbatim Willison) :
1. **Private data** (données privées)
2. **Untrusted content** (contenu non-trusted, user input, web)
3. **Exfiltration vector** (capacité d'exfiltration externe)

Les trois ensemble = vulnérabilité majeure (prompt injection exfiltration). Couper au moins 1 des 3 axes.

> ⚠️ Avant 23 mai 2026 : le vault forge attribuait à tort le lethal trifecta à Thariq Shihipar (Agent SDK Workshop Code with Claude SF). C'est **Simon Willison** qui a forgé le terme en juin 2025. Thariq le mentionne mais ne l'a pas créé.

**"Swiss cheese defense"** = concept général cybersécurité (multi-layer defense, plusieurs couches imparfaites qui ensemble couvrent les trous). Repris dans l'écosystème Claude Code mais pas verbatim Thariq Agent SDK Workshop spécifiquement.

---

## EXEMPLES CONCRETS

### MCP officiels Anthropic / écosystème
- **Anthropic MCP servers** ([github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)) — filesystem, git, sqlite, etc.
- **Sentry MCP** (Ronacher) — ~8k tokens upfront, accès Sentry partagé cross-clients ([lucumr.pocoo.org/2025/12/13/skills-vs-mcp/](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/))
- **forge-brain** (custom forge) — 11 tools sur vault perso, FastMCP 2, port 8091
- **GitHub MCP** — `gh` operations + repos search

### Skills publiques (agentskills.io)
- `anthropics/skills` — skills officielles (pdf, skill-creator, mcp-builder, frontend-design, etc. — compte exact à vérifier sur le repo)
- `karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md` — seul skill public Karpathy, ~40 lignes atomique
- Stripe, Vercel, Cloudflare, Sentry, OpenAI, HashiCorp, Figma, Netlify — skills publics
- Simon Willison `simonw/llm`

### Pattern hybride Karpathy (qmd)
**qmd** — handle `tobi` GitHub (historiquement Tobias Lütke, CEO Shopify), confirmé par npm `@tobilu/qmd` et sources tierces (attribution communément acceptée, non signée dans README officiel). Karpathy le recommande dans son Gist LLM Wiki.

- BM25 + vector + reranker
- **CLI ET MCP** — les deux modes exposés
- Démontre : pas d'opposition CLI vs MCP, complémentarité

### Trail of Bits (config sécu publique)
- `/sandbox` builtin + devcontainer + dropkit DO droplets = 3-tier sandbox
- MCP minimaux, hooks Stop pour anti-rationalization
- Doctrine ToB : **Skills préférées par défaut, MCP réservé aux intégrations externes / cross-ecosystem**

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained) — "MCP connects Claude to data; Skills teach Claude what to do"
- docs.claude.com — sections MCP + Skills + Tools
- features-overview — doctrine hook vs rule

### Thariq Shihipar (Anthropic)
- **Code with Claude SF 6-7 mai 2026** — Agent SDK Workshop (3-way trade-offs tools/bash/code-gen, "le modèle se perd" anti-pattern)
- **Talk "How I AI: HTML is the new markdown"** — verbatim "All of us are becoming these compute allocators now" (ChatPRD)
- **Post Anthropic mars 2026** "Lessons from Building Claude Code: How We Use Skills" — 9 catégories skills

### Boris Cherny (Anthropic, créateur CC)
- Pragmatic Engineer interview — MCP simple multi-clients (concept)
- Code with Claude London 19 mai 2026

### Karpathy
- [Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 4 avril 2026, tooling = qmd (CLI+MCP)
- Sequoia AI Ascent 29 avril 2026 — "From Vibe Coding to Agentic Engineering"

### Simon Willison
- [simonwillison.net/2025/Jun/16/the-lethal-trifecta/](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — création du terme **lethal trifecta** (juin 2025)
- [simonwillison.net/2025/Oct/16/claude-skills/](https://simonwillison.net/2025/Oct/16/claude-skills/) — "Skills maybe a bigger deal than MCP"
  - **Contexte critique** : facilité de partage (agentskills.io), PAS la mort de MCP. Complémentaires.

### Spec ouverte
- [agentskills.io](https://agentskills.io) — adopté par ~40 produits (Cursor, Codex, Gemini CLI, Goose, Copilot, Roo, Kiro, Letta, Spring AI, Snowflake Cortex, Tabnine, Mistral Vibe, etc.)

### Ronacher
- [lucumr.pocoo.org/2025/12/13/skills-vs-mcp/](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/) — Sentry MCP cost analysis (~8k tokens upfront pour schemas)

---

## GOTCHAS — Pièges observés

### Pièges MCP
- **`.mcp.json` versionné avec credentials** = secret exposé, JAMAIS (cf [[erreur-password-postgres-clair-mcp-json]])
- **Stop words / stems** dans MCP custom : Python NLTK FR a 153 stop words, fuck up recherche "erreur" (cf [[erreur-mcp-stopwords-semantiques]])
- **`yaml.dump` corruption** : `default_flow_style=None` peut corrompre frontmatter (cf [[erreur-mcp-yaml-dump-corruption]])
- **Auto-mode classifier** bloque self-modification de `.mcp.json` (sécu Anthropic)
- **Tool response max 25k tokens** : MCP tool qui retourne plus = erreur littérale `exceeds maximum allowed tokens (25000)`
- **Hot reload MCP** : pas systématique, redémarrer la session pour prise en compte

### Pièges Skills
- **Description = trigger** 3e personne directive, pas description 1re personne
- **`name` YAML = nom exact du dossier** kebab-case
- **Description spec 1024 chars MAIS ~250 chars pratique** (system reminder `/skills` tronque)
- **Skills orphelines** dans frontmatter agent : si pas référencée dans le body, jamais activée
- **STOP critique en gotchas fin** : critique en haut < ligne 25, pas en bas (cf [[erreur-stop-critique-position-gotcha-fin]])
- **MultiEdit matcher** : hook PreToolUse "Write|Edit" sans MultiEdit = trou architectural (cf [[feedback_multiedit_matcher_blind_spot]])

### Pièges Bash
- **`$ARGUMENTS` dans backticks** = substitution littérale qui casse quoting (Windows particulièrement)
- **Heredoc Windows** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])

### Piège transversal
- **Confondre "MCP" et "Skill"** chez les juniors : MCP = couche data, Skill = couche savoir-faire. Pas le même rôle.
- **Lethal trifecta attribué à tort** : c'est Simon Willison (juin 2025), pas Thariq.

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- mcp vs skills
- mcp ou skill
- quand utiliser mcp
- quand utiliser skill
- doctrine mcp skills
- mcp connects data skills teach how-to
- mcp vs cli
- tools bash code-gen tradeoffs
- lethal trifecta willison
- compute allocator

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-hook]]
- [[comment-ecrire-claudemd]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[pattern-vault-llm-karpathy]]

### Fiches leaders (à créer phase B bis)
- [[Thariq Shihipar]]
- [[Boris Cherny]]
- [[Tobi Lutke]]
- [[Andrej Karpathy]]
- [[Simon Willison]]
- Armin Ronacher — créateur Flask, blog lucumr.pocoo.org (fiche à créer)

### Knowledge / erreurs liées
- [[erreur-password-postgres-clair-mcp-json]]
- [[erreur-mcp-stopwords-semantiques]]
- [[erreur-mcp-yaml-dump-corruption]]
- [[erreur-auto-mode-classifier-self-modification]]
- [[erreur-stop-critique-position-gotcha-fin]]
- [[erreur-da-heredoc-bash-silencieux]]
- [[feedback_multiedit_matcher_blind_spot]]
- [[feedback_non_invokable_skills_orphan]]
- [[feedback_da_bash_write]]
- [[e-descriptions-keyword-stuffing]]

### Forge custom
- [[forge-brain-proactive]] — rule MCP forge-brain obligatoire
- audit-mcp-forge-brain — audit technique 11 outils (note à créer)
- [[obsidian-markdown]] — skill format wikilinks/frontmatter

---

**Fin note canonique `mcp-vs-skills-doctrine.md`** — révisée 23 mai 2026 post-audit thématique vault.


---

## AJOUT 24 mai 2026 — Pattern MCP brief-then-direct (orchestration)

La doctrine MCP/Skills/CLI capture **où vit l'info**. Le pattern [[pattern-mcp-brief-then-direct]] capture **qui consulte quand**.

### Combinaison

| Pattern | Question répondue |
|---------|------------------|
| **MCP vs Skills vs CLI** | Où ranger ce savoir ? (data vs how-to vs exploration) |
| **Brief-then-direct** | Qui consulte ce MCP et quand ? |

### Application

Avant de dispatcher un sub-agent qui doit consulter un MCP :
1. **Session principale** consulte le MCP en amont (extraction ciblée)
2. **Brief enrichi** au sub-agent avec synthèse
3. **Sub-agent** exécute avec contexte fourni, filet MCP direct en cas de doute non couvert

Évite l'anti-pattern : N sub-agents qui consultent le même MCP en parallèle redondant (coût × N).

Détail complet + transposition cross-MCP (forge-brain, obsidian-brain, postgres, langfuse, context7) : [[pattern-mcp-brief-then-direct]].

---

## AJOUT 9 juin 2026 — Statuts à jour & dossier MCP dédié

Cette note arbitre **quand** un MCP est le bon outil. Le **comment construire** un MCP de production vit désormais dans un dossier dédié : [[MOC-MCP]] (point d'entrée).

### Statuts vérifiés (juin 2026, sources primaires)

- **Spec** : courant = **2025-11-25** ; RC = **2026-07-28** (MCP devient *stateless* au niveau protocole, schemas → JSON Schema 2020-12).
- **Transports** : `stdio` local + **Streamable HTTP** remote. **SSE pur déprécié** (depuis spec 2025-03-26), rétrocompat seulement.
- **SDK Python** : **FastMCP 3.0 GA** (18 fév 2026, repo `PrefectHQ/fastmcp`) = défaut prod ; FastMCP 1.0 absorbé dans le SDK officiel `mcp` (2024) ; ~70 % des serveurs MCP tous langages tournent sur du FastMCP.
- **SDK TypeScript** : `@modelcontextprotocol/sdk` v1.x (prod) ; v2 pre-alpha (Q3 2026 visé).
- **Gouvernance** : MCP gouverné par la **Linux Foundation** (10 000+ serveurs publics actifs début 2026).

### Le « 50-100 tools, le modèle se perd » a maintenant des réponses nommées

Le piège 1 (tout en MCP) de cette note avait une parade vague (« reste sous 15 tools »). En 2026 il y a des **solutions de scaling** mesurées, détaillées dans [[mcp-tool-design-scaling]] :
- **Code Execution with MCP** (Anthropic) : serveurs présentés comme filesystem de code, **-98,7 % tokens** (150k→2k).
- **Tool Search Tool** (Claude Developer Platform) : `defer_loading`, **-85 % tokens**, Opus 4.5 79,5 %→88,1 % de précision MCP.
- **Dynamic Tool Discovery** (GitHub MCP) : toolsets + `X-MCP-Tools` + `--dynamic-toolsets` + read-only mode.
- **Codemode** (Cloudflare) : 2 500+ endpoints via 2 tools `search()`/`execute()`.

### Sécurité — au-delà du lethal trifecta

Cette note documente déjà le lethal trifecta (Willison). La doctrine OAuth complète pour MCP remote (Resource Server, confused deputy, **token passthrough interdit**, RFC 8707, token exchange) vit dans [[mcp-securite-oauth-remote]].

### Multi-client

Ce que supportent réellement Claude / ChatGPT / Gemini en juin 2026 (ChatGPT = remote only, pas de localhost ; Streamable HTTP commun aux 3) : [[mcp-multi-client-claude-chatgpt-gemini]].


---

## AJOUT 27 juillet 2026 — RC spec 2026-07-28 : détails confirmés (plus grosse révision depuis le lancement)

La RC mentionnée dans l'AJOUT 9 juin est désormais détaillée (blog officiel MCP, ~20-23 juil. 2026 ; convergence TechCrunch + The Register) :

- **Core stateless** : suppression du handshake `initialize` et de la session protocolaire — chaque requête self-contained, header `Mcp-Method` routable, load-balancing round-robin possible.
- **Tasks sort du core** vers une extension ; **MCP Apps** (UI HTML sandboxée iframe) entre dans la spec ; durcissement authz OAuth/OIDC ; **politique de dépréciation formelle 12 mois**.
- **SDK v2 en beta — ⚠️ renames breaking** : Python `FastMCP` → **`MCPServer`** ; TypeScript éclaté en packages ESM-only (`@modelcontextprotocol/server` / `client`) ; Go v1.7.0-pre.1 ; C# 2.0.0-preview.1. Les serveurs 2026-07-28 peuvent être incompatibles avec les anciens clients.
- Impact forge : la ligne « FastMCP 3.0 GA = défaut prod » (AJOUT 9 juin, et [[reference-technique-stack-ia]]) reste vraie AUJOURD'HUI mais le rename `MCPServer` est à anticiper pour forge-brain/obsidian-brain à la GA de la spec. Pas d'action immédiate — surveiller la GA.

Sources : blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ · techcrunch.com/2026/07/20/ais-most-important-protocol-is-getting-a-little-bit-easier-to-use/ · theregister.com (23 juil. 2026).
