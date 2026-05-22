---
titre: "MCP vs Skills+CLI : quand utiliser quoi (doctrine 2026)"
resume: "Doctrine canonique Anthropic mai 2026 — MCP connecte les données, Skills enseignent le how-to. Boris : MCP cross-surface simple. Thariq : 3-way trade-offs tools/bash/code-gen. Karpathy qmd = CLI+MCP les deux."
aliases:
  - "mcp vs skills"
  - "mcp ou skill"
  - "quand utiliser mcp"
  - "quand utiliser skill"
  - "doctrine mcp skills"
  - "mcp connects data skills teach how-to"
  - "mcp vs cli"
  - "tools bash code-gen tradeoffs"
  - "lethal trifecta mcp"
  - "compute allocator"
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "https://www.claude.com/blog/skills-explained"
  - "Code with Claude SF 6-7 mai 2026 — Thariq Agent SDK Workshop"
  - "Code with Claude SF 6-7 mai 2026 — Thariq How I AI HTML markdown"
  - "Boris Cherny — Pragmatic Engineer interview"
  - "Karpathy LLM Wiki Gist 4 avril 2026"
  - "Simon Willison — simonwillison.net/2025/Oct/16/claude-skills/"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/mcp"
  - "#sujet/skills"
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
- **Accès données** = MCP (cross-surface, simple, partagé Claude Code + Desktop + Cursor + autres clients)
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

### Doctrine Boris — MCP simple cross-surface

> "MCP la réponse la plus simple" quand on veut le même accès données depuis Claude Code + Desktop + Cursor + Goose + Copilot
> — Boris Cherny

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
- Frontmatter skills riche (description = trigger directive 3e personne)

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
- ❌ **SKILL.md > 500 lignes monolithique** — déporter dans `references/`
- ❌ **Skills orphelines** dans frontmatter agent sans être référencées dans le body (cf [[feedback_non_invokable_skills_orphan]])
- ❌ **Keyword stuffing dans description** — cf [[e-descriptions-keyword-stuffing]]

### Anti-patterns Bash
- ❌ **Bash où une Skill structurée serait meilleure** (procédure réutilisable)
- ❌ **`Grep`/`Read` brut sur vault MCP-indexé** — utiliser le MCP (cf forge-brain-proactive)
- ❌ **Heredoc pour write disguised** quand agent a `disallowedTools: Write,Edit` (cf [[feedback_da_bash_write]])

### Anti-pattern transversal : Lethal trifecta (Simon Willison)
**Terme forgé par Simon Willison** ([simonwillison.net](https://simonwillison.net), juin 2025), repris par Thariq dans Agent SDK Workshop mai 2026.

Combinaison toxique d'accès LLM :
1. Accès à des **données privées**
2. Capacité d'**exposition externe** (envoyer email, post API)
3. Exposition à du **contenu non-trusted** (user input, web content)

Les trois ensemble = vulnérabilité majeure (prompt injection exfiltration). Couper au moins 1 des 3 axes.

> "Swiss cheese defense" — multi-layer defense, plusieurs hooks/skills imparfaits qui ensemble couvrent les trous
> — Thariq Shihipar, Agent SDK Workshop Code with Claude SF mai 2026

---

## EXEMPLES CONCRETS

### MCP officiels Anthropic / écosystème
- **Anthropic MCP servers** ([github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)) — filesystem, git, sqlite, etc.
- **Sentry MCP** (Ronacher) — ~8k tokens upfront, accès Sentry partagé cross-clients
- **forge-brain** (custom forge) — 11 tools sur vault perso, FastMCP 2, port 8091
- **GitHub MCP** — `gh` operations + repos search

### Skills publiques (agentskills.io)
- `anthropics/skills` — 17 skills officielles (pdf, skill-creator, mcp-builder, etc.)
- `karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md` — seul skill public Karpathy, ~40 lignes atomique
- Stripe, Vercel, Cloudflare, Sentry, OpenAI, HashiCorp, Figma, Netlify — skills publics
- Simon Willison `simonw/llm`

### Pattern hybride Karpathy (qmd)
**qmd** (créé par **Tobi Lütke, CEO Shopify**, recommandé par Karpathy) :
- BM25 + vector + reranker
- **CLI ET MCP** — les deux modes exposés
- Démontre : pas d'opposition CLI vs MCP, complémentarité

### Trail of Bits (config sécu publique)
- `/sandbox` builtin + devcontainer + dropkit DO droplets = 3-tier sandbox
- MCP minimaux, hooks Stop pour anti-rationalization
- Modèle de doctrine "MCP minimaliste + hooks sécu"

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel
- [claude.com/blog/skills-explained](https://www.claude.com/blog/skills-explained) — "MCP connects Claude to data; Skills teach Claude what to do"
- docs.claude.com — sections MCP + Skills + Tools
- features-overview — doctrine hook vs rule

### Thariq Shihipar (Anthropic)
- **Code with Claude SF 6-7 mai 2026** — Agent SDK Workshop (lethal trifecta, swiss cheese, bash > tools, 3-way trade-offs)
- **Talk "How I AI: HTML is the new markdown"** — "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code" + "we're all becoming 'compute allocators'"
- LinkedIn 17 mars 2026 — 9 catégories skills

### Boris Cherny (Anthropic, créateur CC)
- Pragmatic Engineer interview — "MCP la réponse la plus simple" cross-surface
- Code with Claude London 19 mai 2026

### Karpathy
- [Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 4 avril 2026, tooling = qmd (CLI+MCP)

### Simon Willison
- [simonwillison.net/2025/Oct/16/claude-skills/](https://simonwillison.net/2025/Oct/16/claude-skills/) — "Skills maybe a bigger deal than MCP"
  - **Contexte critique** : facilité de partage (agentskills.io), PAS la mort de MCP. Complémentaires.

### Spec ouverte
- [agentskills.io](https://agentskills.io) — adopté par ~40 produits (Cursor, Codex, Gemini CLI, Goose, Copilot, Roo, Kiro, Letta, Spring AI, Snowflake Cortex, Tabnine, Mistral Vibe, etc.)

### Ronacher
- Sentry MCP cost analysis — ~8k tokens upfront pour schemas

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
- **Skills orphelines** dans frontmatter agent : si pas référencée dans le body, jamais activée
- **STOP critique en gotchas fin** : critique en haut < ligne 25, pas en bas (cf [[erreur-stop-critique-position-gotcha-fin]])
- **MultiEdit matcher** : hook PreToolUse "Write|Edit" sans MultiEdit = trou architectural (cf [[feedback_multiedit_matcher_blind_spot]])

### Pièges Bash
- **`$ARGUMENTS` dans backticks** = substitution littérale qui casse quoting (Windows particulièrement)
- **Heredoc Windows** : boucle quoting Git Bash (cf [[erreur-da-heredoc-bash-silencieux]])

### Piège transversal
- **Confondre "MCP" et "Skill"** chez les juniors : MCP = couche data, Skill = couche savoir-faire. Pas le même rôle.

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
- lethal trifecta mcp
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
- [[audit-mcp-forge-brain]] — audit technique 11 outils
- [[obsidian-markdown]] — skill format wikilinks/frontmatter

---

**Fin note canonique `mcp-vs-skills-doctrine.md`** — 2e pilote chantier 22 mai 2026.
