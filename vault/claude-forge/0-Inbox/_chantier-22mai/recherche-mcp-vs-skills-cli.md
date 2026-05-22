---
titre: "MCP vs Skills+CLI — Doctrine Anthropic et leaders mai 2026"
resume: "Quand utiliser MCP server vs skill+CLI selon Anthropic/Thariq/Simon Willison/Karpathy/Trail of Bits + verdict argumenté pour forge-brain et neoteem-brain"
aliases:
  - "mcp vs skills"
  - "skills vs mcp"
  - "skill cli vs mcp"
  - "doctrine mcp skill 2026"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/claude-code"
  - "#domaine/mcp"
---

# MCP vs Skills+CLI — Doctrine Anthropic et leaders (mai 2026)

> **TL;DR** — La doctrine 2026 a basculé : **MCP = connectivité (data access), Skills = procédure (how-to)**. La position d'Anthropic ("MCP connects Claude to data; Skills teach Claude what to do with that data") rend la question "MCP OU Skills" mal posée. Le pattern dominant chez les leaders (Karpathy/Thariq/Trail of Bits) est : **CLI binaire + skill wrapper + MCP server optionnel pour exposition native**. Pour forge-brain et neoteem-brain : **garder MCP** (déjà optimal vu volume notes + outils structurés), mais **ajouter une skill descriptor** qui apprend au modèle quand/comment l'invoquer (progressive disclosure).

---

## Section 1 — Sources primaires verbatim

### 1.1 Simon Willison — "Claude Skills are awesome, maybe a bigger deal than MCP" (16 oct. 2025)

URL : https://simonwillison.net/2025/Oct/16/claude-skills/

> "GitHub's official MCP on its own famously consumes tens of thousands of tokens of context, and once you've added a few more to that there's precious little space left for the LLM to actually do useful work."

> "Almost everything I might achieve with an MCP can be handled by a CLI tool instead. LLMs know how to call `cli-tool --help`."

> "I don't even need to implement a new CLI tool. I can drop a Markdown file in describing how to do a task instead."

> "I expect we'll see a Cambrian explosion in Skills which will make this year's MCP rush look pedestrian by comparison."

Position de Willison : **prefer Skills** quand un environnement coding/execution est disponible. MCP reste pertinent en l'absence de filesystem/code execution. Skills "outsource the hard parts to the LLM harness — a very sensible strategy."

### 1.2 Anthropic — "Skills explained" (claude.com/blog/skills-explained)

Framing officiel verbatim :

> "MCP connects Claude to data; Skills teach Claude what to do with that data."

Décision rule officielle :
- Si tu expliques **comment** utiliser un outil ou suivre une procédure → **Skill**
- Si Claude doit **accéder** à un système externe → **MCP**
- Ils sont conçus pour être combinés

Autres distinctions officielles :
- **Projects** : "here's what you need to know" (static, always loaded)
- **Skills** : "here's how to do things" (dynamic, on-demand)
- **Subagents** : "complete, self-contained agents" with independent context — peuvent eux-mêmes consommer des Skills

### 1.3 Thariq Shihipar — Claude Agent SDK Workshop (jan 2026, ~20k mots transcrits)

Source : `recherche-youtube-watch-vibe-coding.md` section 3.

**Skills = filesystem-based progressive disclosure :**

> "Skills are basically a way of allowing our agent to take longer complex task and load in things via context. For example, we have a bunch of docx skills. And these docx skills tell it how to do code generation to generate these files. **Skills are an example of being very file system or bash tool built, because they're just really folders that your agent can CD into and read.**"

> "Skills are a form of progressive context disclosure. You ask it to make a docx file and then it CDs into the directory, reads how to do it, writes some scripts and keeps going."

**Bash > tools structurés (argument fondamental) :**

> "If you were designing an agent harness, maybe what you would do is you'd have a search tool and a lint tool and execute tool. Every time you thought of a new use case, you'd have another tool. Instead, now Claude just uses grep. It knows your package manager, so it runs npm run test.ts."

**Trade-offs verbatim (Tools vs Bash vs Code gen) :**

| Mode | Pros | Cons |
|------|------|------|
| Tools structurés (MCP) | "extremely structured and very very reliable, minimal errors/retries" | "**high context usage**. With 50–100 tools, the model gets confused. No discoverability. Not composable." |
| Bash | "very composable, low context usage" | "discovery time, slightly lower call rates" |
| Code gen | "highly composable, dynamic scripts" | "longest to execute, needs linting/compilation" |

**Quand utiliser quoi (verbatim Thariq) :**

> "**Tools** — atomic actions your agent usually needs to execute in sequence, you need a lot of control over. We don't use bash to write a file — we have a write_file tool, because we want the user to be able to see the output and approve it. Sending an email is another example. **Any sort of non-reversible change — a tool is a good place for that.**"

> "**Bash** — composable actions like searching a folder, using GitHub, linting code and checking for errors or memory."

> "**Code generation** — highly dynamic, very flexible logic, composing APIs, doing data analysis or deep research."

**Custom bash tool discovery pattern :**

> "You just put it in the file system and you tell it like, hey, here is a script. **I would design all my CLI scripts to have like a --help, so that the model can call that and then it can progressively disclose every sub command inside of the script.**"

### 1.4 Karpathy LLM Wiki — qmd pattern (gist 442a6bf...)

URL : https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

> "qmd is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device."

Crucial : `qmd` offre **les deux interfaces** :

> "a CLI (so the LLM can shell out to it) **and** an MCP server (so the LLM can use it as a native tool)"

→ Ce n'est PAS l'un OU l'autre. CLI = subprocess pour agents bash-centric. MCP = first-class tool pour agents tool-centric. **Le pattern recommandé chez Karpathy est de servir les deux.**

### 1.5 Armin Ronacher — "Skills vs Dynamic MCP Loadouts" (13 déc. 2025)

URL : https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/

Verdict : préfère **skills + agent-written tools** sur MCP, y compris MCP dynamique d'Anthropic.

Token cost concret :
> "Sentry MCP alone consumes ~8,000 tokens upfront."

Critique du dynamic loading :
> "the description is both too long to eagerly load it, and too short to really tell the agent how to use it"

Critique stabilité MCP :
> "MCP servers prioritize brevity over stability — they trim descriptions and change query syntax without warning"

Insight clé sur contrôle :
> "the tool is largely under my control. Whenever it breaks or needs some other functionality, I ask the agent to adjust it"

### 1.6 Boris Cherny — Sequoia AI Ascent 2026

Position pragmatique d'Anthropic, MCP comme connecteur universel :

> "For us, it's always just the simplest answer. It's just MCP. So the same MCP connector that you have in Claude AI, you hook up Salesforce, Google Docs, Google Calendar. And then Cowork can use that. Claude CLI can use it. Claude Code everywhere can use it."

→ **MCP n'est PAS abandonné par Anthropic — il reste la couche connectivité.** Skills viennent en complément.

### 1.7 Trail of Bits — claude-code-config (production)

URL : https://github.com/trailofbits/claude-code-config

Stack en production : sandboxing + permissions + hooks + **skills** + **MCP servers** + workflows. Les deux coexistent.

Skills chain : `brainstorm → plan → execute → verify`. Auto-invoked par description matching.

MCP servers en production : Context7, Exa, "additional MCP servers worth adding for specific workflows".

Default important : `enableAllProjectMcpServers: false` "to prevent compromised repositories from injecting malicious MCP servers" → **MCP a un coût sécu**, skills n'ont pas ce problème.

---

## Section 2 — Tableau comparatif

| Critère | MCP Server | Skill + CLI |
|---|---|---|
| **Coût tokens baseline** | Élevé : ~8k (Sentry), ~tens of thousands (GitHub) — chaque tool def + result envoyés à chaque call | Bas : ~quelques dizaines de tokens (juste description), full content loaded on-demand |
| **Découvrabilité** | "Always visible" — tools listés au démarrage | Description-driven — le modèle doit décider de lire la skill |
| **Standardisation** | Cross-ecosystem (Cursor, Gemini CLI, Copilot, Codex) | Anthropic-only à l'origine, format ouvert depuis 18 déc. 2025 (agentskills.io) |
| **Composabilité** | Faible — tools = atomiques, pas pipeable | Forte — bash + grep + jq + tail = pipelines naturels |
| **Maintenance** | Process serveur à maintenir (port, transport, lifecycle) | Markdown + scripts versionnés dans le repo |
| **Versioning/sharing** | Registries + protocoles versionnés | Drag-and-drop folder, peu de versioning natif |
| **Stabilité contractuelle** | Faible (Ronacher) : descriptions changent sans warning | Forte si CLI versionné (--help stable) |
| **Sécurité** | Surface d'attaque (compromised servers) → `enableAllProjectMcpServers: false` par défaut TOB | Code in-repo, code review standard |
| **Latence** | Faible (in-process tool call) | Légèrement plus haute (subprocess spawn) |
| **Idéal pour** | Atomic, non-reversible, structured outputs (send email, write file, approve PR) | Composable, exploratory, multi-step (search, lint, analyze) |
| **Anti-pattern** | 50–100 tools = "le modèle se perd" (Thariq) | Skill avec aucun script + 500L de docs |

---

## Section 3 — Critères de décision verbatim

**Anthropic (officiel) :**
- Données / accès externe → MCP
- Procédure / how-to → Skill
- Combinable : "MCP for connectivity, Skills for procedural knowledge"

**Thariq (Anthropic interne) :**
- **Tool MCP** quand : atomic + non-reversible + besoin de UX d'approbation (write_file, send_email)
- **Bash + CLI** quand : composable + exploratoire (search, lint, github)
- **Code gen** quand : très dynamique, data analysis, deep research

**Simon Willison :**
- Si tu as un coding env → **Skill+CLI prefer**
- Si pas de coding env (Claude.ai web sans code interp) → MCP nécessaire

**Karpathy :**
- Knowledge base ≥ 100-150 notes → Need search → **les deux** : CLI (`qmd search "..."`) + MCP server (`qmd mcp`)

**Ronacher :**
- Stabilité contractuelle critique → CLI > MCP (descriptions MCP changent silencieusement)
- Si l'agent doit pouvoir modifier l'outil lui-même → Skill avec scripts

**Trail of Bits (production) :**
- Sécurité-sensitive → skills par défaut (in-repo, code-reviewable), MCP désactivé en projet par défaut
- Cross-ecosystem (clients externes) → MCP

---

## Section 4 — Verdict pour forge-brain

**État actuel** : MCP `forge-brain` (port 8091, SQLite FTS5, 11 outils : `search_brain`, `read_note`, `read_note_by_path`, `get_backlinks`, `get_tags`, `get_property`, `list_notes`, `vault_stats`, `create_note`, `append_note`, `update_property`).

**Volume** : vault assez large (Knowledge/ + Projets/ + Techniques/ + Leaders/ + Prompts/) — clairement > seuil Karpathy 100-150 notes.

**Verdict : GARDER MCP + AJOUTER skill descriptor.**

### Raisons garder MCP

1. **Outils structurés non-reversibles** (`create_note`, `update_property`) = exactement le cas d'usage Thariq pour "tools" (atomic, non-reversible, UX d'approbation Cowork).
2. **FTS5 SQLite indexé** = recherche perf, mal exposable proprement via CLI (subprocess overhead à chaque query, pas de cache index).
3. **Backlinks + graph navigation** (`get_backlinks`) = requêtes structurées, mal modélisées en bash composable.
4. **Cowork distribué** (Boris : "the same MCP connector... Cowork can use that, CLI can use it") = pattern Anthropic recommandé pour multi-surface.
5. **Cohérence cross-projet** : neoteem-brain v2 (5 plugins Cowork) suit ce pattern, casser forge-brain = incohérence.

### Risques actuels

- **Token cost** : 11 tools listés au démarrage de chaque session. Estimation : ~3-5k tokens (à mesurer). Pas critique mais non-zéro.
- **Discoverability** : règles `forge-brain-proactive.md` + `vault-consultation-protocol.md` palliatives — mais "advisory" donc ~80% compliance (CLAUDE.md gotcha).

### Améliorations recommandées

**A. Skill descriptor `forge-brain` (NOUVELLE)** — pattern Karpathy/Thariq progressive disclosure :

- Description ~50 tokens : "When to query the forge-brain vault and which MCP tool to use for each scenario"
- Body : decision tree quand utiliser search_brain vs list_notes vs get_backlinks
- Charge à la demande quand le modèle hésite

**B. Hook enforcement DÉJÀ EN PLACE** (`vault-query-guard`) — bloque Write si vault pas consulté. C'est le complément discipline qui rend MCP+skill robuste.

**C. PAS de migration vers `forge` CLI binaire** — coût migration > bénéfice. Le SQLite FTS5 + MCP est déjà optimal pour ce volume.

### Pattern hybride futur (si croissance)

Si le vault dépasse plusieurs milliers de notes ou si la rerank LLM devient nécessaire, copier le pattern Karpathy `qmd` :
- Garder MCP forge-brain pour writes + structured reads
- Ajouter un binaire `forge search` avec BM25+vector+rerank pour les queries exploratoires
- Les deux exposés, le modèle choisit selon le contexte

---

## Section 5 — Verdict pour neoteem-brain

**État actuel** : MCP obsidian-brain v2 (SQLite FTS5, repo séparé, 5 plugins Cowork support/dev/dev-ia/dev-admin/support-admin, VM serveur, benchmark 24/24).

**Verdict : GARDER MCP. Pas de migration vers skill+CLI.**

### Raisons (plus fortes encore que forge-brain)

1. **Multi-tenant Cowork** : 5 profils utilisateurs (Caroline, Boss support, Romane, Sylvain, etc.) ont besoin du même outil exposé. MCP = single source of truth déployable. Skill+CLI = duplication par profil.
2. **Knowledge-first routing pattern** (`reference_obsidian_query_brain.md`) déjà capitalisé — le wrapper CLI EXISTE déjà côté serveur, le MCP l'expose proprement.
3. **Sécurité multi-utilisateur** : MCP centralise les access controls. CLI distribué = chaque profil maintient sa version.
4. **682+ notes** : largement au-dessus du seuil Karpathy → recherche perf indispensable, déjà résolue par SQLite FTS5.
5. **Cross-profile cohérence** : neo-brain, neo-brain-dev, neo-brain-dev-ia, neo-brain-support partagent le même MCP. Migrer un seul profil casse l'architecture.

### Améliorations recommandées

**A. Auditer le nombre de tools exposés** par profil. Si > 15 tools → risque "modèle se perd" (Thariq). Si vrai, splitter en MCP scopés par profil.

**B. Skill descriptors par profil** (déjà partiellement fait — `neo-brain`, `neo-brain-dev`, `neo-brain-support`, `neo-brain-dev-ia`). Vérifier qu'ils sont assez courts (description ~50 tokens) et qu'ils chargent la doc complète on-demand.

**C. Mesurer le token cost réel** au démarrage d'une session Cowork. Si > 10k tokens juste pour le MCP brain → refactor priorité.

---

## Section 6 — Anti-patterns documentés

### Anti-pattern 1 — "Tout en MCP"
- **Symptôme** : 5+ MCP servers chargés en parallèle, 50+ tools dans le contexte au démarrage
- **Source** : Thariq workshop
- **Citation** : "If anyone's built an agent with 50 or 100 tools, they take up a lot of context and the model gets a little bit confused"
- **Fix** : MCP réservé à atomic+non-reversible. Le reste → bash + CLI + skills.

### Anti-pattern 2 — "Tout en Skills"
- **Symptôme** : créer skill pour chaque API access (Slack, GitHub, DB) au lieu d'utiliser leur MCP existant
- **Source** : Anthropic blog skills-explained
- **Pourquoi mauvais** : duplique l'authentification, perd la mise à jour automatique du protocole, perd l'observabilité MCP
- **Fix** : MCP pour les data sources externes, skills pour leur composition

### Anti-pattern 3 — "Container bash isolé"
- **Symptôme** : isoler bash tool dans VM séparée du file system de l'agent
- **Source** : Thariq workshop
- **Citation** : "If you got a tool result that's saving a file, then your bash tool can't read it"
- **Fix** : bash + tool MCP + filesystem doivent partager le même contexte

### Anti-pattern 4 — "MCP description trop courte/trop longue"
- **Symptôme** (Ronacher) : "the description is both too long to eagerly load it, and too short to really tell the agent how to use it"
- **Fix** : description MCP courte + skill compagnon qui détaille les patterns d'usage

### Anti-pattern 5 — "Skill sans bundled resources"
- **Symptôme** (Trail of Bits) : SKILL.md de 2000 mots sans `references/` ni scripts
- **Citation TOB** : "don't just describe the workflow — bundle the reference material. Keep SKILL.md under 2000 words and move detailed content into references/"
- **Fix** : pattern progressive disclosure : SKILL.md léger + references/ chargées à la demande

### Anti-pattern 6 — "MCP server enabled par défaut sur tous les projets"
- **Symptôme** : `enableAllProjectMcpServers: true`
- **Source** : Trail of Bits config
- **Risque** : repo compromis injecte un MCP malveillant
- **Fix** : default false, allowlist explicite

---

## Section 7 — Citations verbatim consolidées

### Karpathy (qmd / LLM Wiki gist)
> "qmd is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool)."

### Thariq (Agent SDK Workshop)
> "Bash is what makes Claude Code so good. The bash tool was like the first code mode."

> "Skills are basically a way of allowing our agent to take longer complex task and load in things via context. Skills are an example of being very file system or bash tool built, because they're just really folders that your agent can CD into and read."

> "Tools — think about them as atomic actions your agent usually needs to execute in sequence, and you need a lot of control over. Any sort of non-reversible change — a tool is a good place for that."

### Simon Willison
> "GitHub's official MCP on its own famously consumes tens of thousands of tokens of context."

> "Almost everything I might achieve with an MCP can be handled by a CLI tool instead. LLMs know how to call cli-tool --help."

> "I expect we'll see a Cambrian explosion in Skills which will make this year's MCP rush look pedestrian by comparison."

### Anthropic officiel
> "MCP connects Claude to data; Skills teach Claude what to do with that data."

> "Projects say 'here's what you need to know.' Skills say 'here's how to do things.'"

### Boris Cherny (Sequoia)
> "For us, it's always just the simplest answer. It's just MCP. The same MCP connector you have in Claude AI, you hook up Salesforce, Google Docs, Google Calendar. And then Cowork can use that. Claude CLI can use it. Claude Code everywhere can use it."

### Ronacher (Skills vs Dynamic MCP)
> "Sentry MCP alone consumes ~8,000 tokens upfront."

> "the description is both too long to eagerly load it, and too short to really tell the agent how to use it"

> "the tool is largely under my control. Whenever it breaks or needs some other functionality, I ask the agent to adjust it"

### Trail of Bits
> "don't just describe the workflow — bundle the reference material that makes it expert-level: analysis checklists, vulnerability patterns, example outputs, and the decision logic. Keep the SKILL.md lean (under 2,000 words) and move detailed content into references/ files."

### Eric J. Ma
> "If your goal is a shareable, versioned interface for many users, MCP is still the safer default. If you need quick, local customization inside Claude with a lean prompt footprint, skills are compelling."

---

## Annexe — sources non explorées / gaps

- **Boris howborisusesclaudecode.com section MCP vs skills** : pas vérifiée verbatim cette session, le talk Sequoia couvre la position MCP générale.
- **Thread X récents 2026 "skills replacing MCP"** : sentiment communautaire diversifié, pas de prise de position officielle Anthropic au-delà du blog "skills-explained" et du framing "MCP for data, Skills for how-to".
- **Anthropic blog "How we built Claude Code"** : article référencé non lu cette session — pas indispensable, la doctrine officielle est dans skills-explained.
- **Mesure token cost réelle** forge-brain + neoteem-brain : à faire avec Langfuse trace sur une session Cowork.
- **Talk Karpathy Sequoia "From Vibe Coding to Agentic Engineering"** : non transcrit (URL YouTube non trouvée), couvert par son blog `karpathy.bearblog.dev/sequoia-ascent-2026/`.

---

## Wikilinks vers notes vault liées

- [[reference_obsidian_query_brain]] — pattern neo-brain wrapper CLI + skill
- [[reference_boris_thariq_bestpractices]] — best practices auditées
- [[reference_agentic_engineering]] — Karpathy Sequoia
- [[project_mcp_v2]] — MCP obsidian-brain v2 architecture
- [[project_neoteem_brain_plugin]] — 3 plugins Cowork
- [[reference_forge_brain_vault]] — vault forge-brain architecture
- [[recherche-youtube-watch-vibe-coding]] — transcripts Thariq/Boris/Erik/Cat
- [[reference_techniques_cheatsheet]] — quelle technique quand
