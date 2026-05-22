---
titre: "Karpathy — Vault LLM Wiki, architecture canonique pour forge-brain"
resume: "Spec verbatim Karpathy du LLM Wiki (Gist 4 avril 2026) + threads X + repos CLAUDE.md, base de réorganisation forge-brain"
aliases:
  - "karpathy vault canonique"
  - "llm wiki karpathy"
  - "agentic engineering karpathy"
  - "vault obsidian llm"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/agents"
  - "#type/leader"
---

# Karpathy — Vault LLM Wiki, architecture canonique pour forge-brain

> Recherche menée le 22 mai 2026 dans le cadre de la refonte forge-brain.
> Objectif : extraire la doctrine canonique Karpathy (vault LLM-maintained) et confronter à l'état actuel de forge-brain (309 notes, 7 dossiers numérotés, MOCs, Knowledge/).

## Index des sources

| # | Source | Date | Accès |
|---|--------|------|-------|
| 1 | Gist `llm-wiki.md` officiel ([gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) | 2026-04-04 | OK via WebFetch |
| 2 | Thread X "vibe coding → agentic engineering" | 2026-01-26 | Reconstitué via SD Times + Buttondown + Medium |
| 3 | Thread X annonce LLM Wiki | 2026-04-02 | Reconstitué via couverture presse (16M+ vues) |
| 4 | Thread X AutoResearch | 2026-03-09 | Reconstitué via blockchain.news + myoid.com |
| 5 | Thread X "joined Anthropic" ([x.com/karpathy/status/2056753169888334312](https://x.com/karpathy/status/2056753169888334312)) | 2026-05-19 | Confirmé CNBC + TechCrunch + VentureBeat |
| 6 | Sequoia AI Ascent 2026 "Software is changing again" — transcript [singjupost.com](https://singjupost.com/andrej-karpathy-software-is-changing-again/) | 2026 | Verbatim via WebFetch |
| 7 | Repo [karpathy/nanochat](https://github.com/karpathy/nanochat) — `.claude/skills/read-arxiv-paper/SKILL.md` | actif | OK |
| 8 | Repo [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — `program.md` | actif | OK |
| 9 | Repo [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — `CLAUDE.md` viral 70L | actif | OK |
| 10 | Repos `nanoGPT`, `llm.c` — fichiers `CLAUDE.md` / `AGENTS.md` | — | **Aucun** trouvé en root |

---

## Section 1 — Gist LLM Wiki (verbatim, 4 avril 2026)

### 1.1 Titre & framing

> "A pattern for building personal knowledge bases using LLMs."

Décrit comme un "idea file" à copier-coller dans un LLM agent (Codex, Claude Code, etc.). Explicitement **"intentionally abstract"** — tous les éléments sont "optional and modular — pick what's useful, ignore what isn't."

### 1.2 Thèse centrale (verbatim)

> "Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation."

Alternative :

> "the LLM **incrementally builds and maintains a persistent wiki**"

> **"the wiki is a persistent, compounding artifact."**

Rôles :
- **Humain** : sourcing, exploration, asking questions
- **LLM** : "the summarizing, cross-referencing, filing, and bookkeeping"

Métaphore phare :

> **"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."**

Workflow physique :

> "I have the LLM agent open on one side and Obsidian open on the other."

### 1.3 Architecture — 3 couches (verbatim)

**1. Raw sources**
- Articles, papers, images, data files
- > "immutable — the LLM reads from them but never modifies them"
- > "This is your source of truth."

**2. The wiki**
- > "a directory of LLM-generated markdown files"
- Contenus : summaries, entity pages, concept pages, comparisons, overview, synthesis
- > "The LLM owns this layer entirely."

**3. The schema**
- Fichiers config : `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex)
- > "what makes the LLM a disciplined wiki maintainer rather than a generic chatbot"
- > "You and the LLM co-evolve this over time"

### 1.4 Structure canonique (synthèse communauté à partir du gist)

```
your-wiki/
├── raw/          # Immutable source documents
│   ├── articles/
│   ├── papers/
│   └── meetings/
├── wiki/         # LLM-owned compiled markdown
│   ├── index.md
│   ├── people/
│   ├── projects/
│   └── decisions/
└── CLAUDE.md     # Schema file
```

> "so cleanly separated that even his linter can tell when you've broken the rule"

### 1.5 Les 3 opérations canoniques (verbatim)

#### Ingest
Flow : read source → discuss key takeaways → write summary page → update index → update entity/concept pages → append to log.

> "A single source might touch 10-15 wiki pages."

Style préféré Karpathy : **one source at a time**, batch produit "lower-quality cross-referencing."

#### Query
Flow : read `index.md` → read relevant pages → synthesize answer with citations.

Formats sortie : "markdown page, comparison table, Marp slide deck, matplotlib chart, canvas."

> **"good answers can be filed back into the wiki as new pages."**

#### Lint
Cibles (verbatim) :
- > "contradictions between pages"
- > "stale claims that newer sources have superseded"
- > "orphan pages with no inbound links"
- > "important concepts mentioned but lacking their own page"
- > "missing cross-references"
- > "data gaps that could be filled with a web search"

Métaphore : **"eslint for knowledge."** Schédulable (daily/weekly) ou ad hoc.

### 1.6 Fichiers obligatoires (verbatim)

#### `index.md`
- > "content-oriented" — catalogue de chaque page avec link + one-line summary + optional metadata
- LLM le lit en premier au query time
- > "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)"

#### `log.md`
- > "chronological" — "append-only record of what happened and when"
- Syntaxe préfixe recommandée :
  ```
  ## [2026-04-02] ingest | Article Title
  ```
- Astuce parsing Unix :
  ```
  grep "^## \[" log.md | tail -5
  ```

### 1.7 Tooling recommandé (verbatim)

| Outil | Usage |
|---|---|
| Obsidian Web Clipper | "converts web articles to markdown" |
| Obsidian attachment path | ex. `raw/assets/` |
| Hotkey "Download attachments for current file" | ex. `Ctrl+Shift+D` |
| Obsidian graph view | "see the shape of your wiki — what's connected" |
| Marp | "markdown-based slide deck format" |
| Dataview plugin | "runs queries over page frontmatter" |
| Git | "version history, branching, and collaboration for free" |
| qmd ([tobi/qmd](https://github.com/tobi/qmd)) | "local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking" — CLI + MCP server |

Limitation notée : > "LLMs can't natively read markdown with inline images in one pass."

### 1.8 Pourquoi ça marche (verbatim)

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."

> "Humans abandon wikis because the maintenance burden grows faster than the value."

Référence historique : Vannevar Bush's Memex (1945) — "a personal, curated knowledge store with associative trails between documents." > "The part he couldn't solve was who does the maintenance. The LLM handles that."

### 1.9 Échelle constatée

Wiki personnel Karpathy : ~100 articles, ~400,000 mots — toujours navigable efficacement via index + summaries.

### 1.10 Frontmatter / template note (communauté, pas verbatim Karpathy)

Le gist NE prescrit PAS de frontmatter strict. La communauté a convergé sur :

```yaml
**Tags**: #topic1 #topic2
**Created**: [date]
**Last Updated**: [date]
---
## Content
## Related Notes
- [[Note Title]]
```

> "every note has a summary line and tags — these give Claude quick signals about relevance without reading the full file"

**Conclusion frontmatter** : Karpathy lui-même est SILENCIEUX sur la spec exacte (tags ? aliases ? properties ?). C'est délibéré ("intentionally abstract"). La spec frontmatter forge-brain (4-6 aliases, derniere-maj, resume, tags) est **plus stricte** que ce que Karpathy prescrit.

---

## Section 2 — Tweets pivot 2026 (chronologie)

### 2.1 — 26 janvier 2026 : "Vibe coding → Agentic engineering"

Karpathy raconte le passage en quelques semaines de "80% code écrit manuellement avec autocomplete" à "80% code généré par agents, 20% édits ciblés et polish".

Définition :

> "agentic engineering is the discipline of coordinating stochastic, capable agents to go faster without sacrificing your quality bar"

> "'Agentic' because the new default is that you are not writing the code directly 99% of the time. You are orchestrating agents who do and acting as oversight."

Phrase clé :

> "You can outsource your thinking but you can't outsource your understanding."

### 2.2 — Les 4 failure patterns agentic engineering

Karpathy identifie 4 dommages structurels récurrents :

1. **Silent assumptions** never verified
2. **Hypertrophy** of code and abstractions
3. **Collateral changes** to portions of code that were never requested
4. Absence of **verifiable success criteria**

Forrest Chang a transformé ces 4 patterns en un `CLAUDE.md` 70 lignes → 110,000+ stars, 28 jours #1 GitHub Trending.

### 2.3 — 9 mars 2026 : AutoResearch (8.6M vues en 2 jours)

> 630 lignes de Python, 1 GPU, 1 markdown prompt → **700 expériences en 2 jours**, 20 optimisations découvertes, **+11% sur "Time to GPT-2"** (2.02h → 1.80h).

Architecture clé : trois fichiers seulement comptent :
- `prepare.py` — constantes fixes (read-only)
- `train.py` — le fichier que l'agent édite
- `program.md` — instructions baseline pour un agent

> "you're not touching any of the Python files like you normally would as a researcher. Instead, you are **programming the `program.md` Markdown files**"

Le `program.md` est la skill — itéré par l'humain, exécuté par l'agent.

### 2.4 — 2 avril 2026 : Annonce LLM Wiki (16M+ vues)

Tweet → 2 jours plus tard publication du gist `llm-wiki.md`. 5,000+ stars en 5 jours. 15+ implémentations open source apparues.

### 2.5 — 19 mai 2026 : Joined Anthropic ([x.com/karpathy/status/2056753169888334312](https://x.com/karpathy/status/2056753169888334312))

> "Personal update: I've joined Anthropic. I think the next few years at the frontier of LLMs will be especially formative. I am very excited to join the team here and get back to R&D. I remain deeply passionate about education and plan to resume my work on it in time."

**Rôle** : équipe **pretraining** Claude + lance une nouvelle équipe "using Claude itself to accelerate pretraining research" (AI-assisted research).

Implication forge-brain : Karpathy est désormais ALIGNÉ écosystème Claude Code → ses patterns vont influencer directement le produit qu'on utilise.

---

## Section 3 — Sequoia AI Ascent 2026 "Software is changing again"

Source : [theaiopportunities.com](https://www.theaiopportunities.com/p/sequoia-ai-ascent-2026-andrej-karpathy) + [singjupost.com transcript](https://singjupost.com/andrej-karpathy-software-is-changing-again/)

### 3.1 Thèse Software 3.0

> Software 1.0 = humans write explicit code
> Software 2.0 = humans train neural networks with data
> Software 3.0 = humans program models through **context**

> "the context window becomes the new programming surface"

### 3.2 Verbatim sur contexte / mémoire (transcript singjupost)

> "context windows are really kind of like working memory."

> "you have to sort of program the working memory quite directly because they don't just kind of like get smarter by default."

> "the LLMs basically do a ton of the context management."

### 3.3 Autonomy slider (verbatim)

> "you are in charge of the autonomy slider."

> "depending on the complexity of the task at hand, you can tune the amount of autonomy that you're willing to give up"

> "there should be an autonomy slider in your product."

### 3.4 Agent-ready software (verbatim)

> "you can have maybe lms.txt file, which is just a simple markdown that's telling LLMs what this domain is about."

> "Markdown is super easy for LLMs to understand."

> "any time your docs say click, this is bad."

### 3.5 Important pour forge-brain

**Le talk Sequoia NE MENTIONNE PAS** wikis, vaults, Obsidian ni knowledge bases (vérifié verbatim). Le LLM Wiki est un pattern **séparé** du discours Sequoia. Les deux convergent sur "markdown + agent-readable" mais le wiki est traité à part dans le gist d'avril.

---

## Section 4 — Repos Karpathy : que fait-il VRAIMENT chez lui ?

### 4.1 Inventaire

| Repo | `CLAUDE.md` racine | `AGENTS.md` racine | Autres |
|------|-------------------|--------------------|--------|
| nanochat | **NON** | **NON** | `.claude/skills/read-arxiv-paper/SKILL.md` |
| autoresearch | **NON** | **NON** | `program.md` (instructions agent) |
| nanoGPT | **NON** | **NON** | — |
| llm.c | **NON** | **NON** | — |

**Finding majeur** : Karpathy lui-même n'utilise PAS `CLAUDE.md` ou `AGENTS.md` à la racine de ses repos. Il utilise :
- `program.md` (fichier markdown unique d'instructions agent, façon autoresearch)
- `.claude/skills/<nom>/SKILL.md` (skills Claude Code natives, façon nanochat)

C'est cohérent avec sa philosophie : **abstract, modular, pick what's useful**. Pas de dogme sur le nom du fichier schema.

### 4.2 nanochat — `.claude/skills/read-arxiv-paper/SKILL.md`

Skill qui télécharge le .tar.gz source d'un arxiv, l'extrait sous `~/.cache/nanochat/knowledge/{arxiv_id}/`, lit le paper depuis `main.tex`, écrit un résumé markdown dans `./knowledge/summary_{tag}.md`. Note clé :

> "you're processing this paper within the context of the nanochat repository"

→ Le résumé doit explicitement connecter les findings du paper au code nanochat (lire le code pertinent au besoin).

**Pattern transposable forge-brain** : skills qui INGÈRENT depuis sources externes (arxiv, GitHub, blog) et écrivent dans un répertoire `knowledge/` local. C'est exactement le pattern "ingest" du LLM Wiki implémenté comme skill Claude Code.

### 4.3 autoresearch — `program.md`

Setup steps verbatim :
1. Agree on a run tag (date-based, e.g. `mar5`) and create a fresh git branch
2. Read `README.md`, `prepare.py` (read-only), and `train.py` (editable)
3. Verify cached data exists at `~/.cache/autoresearch/`
4. Initialize `results.tsv` with just the header row

Rules :
- **Only `train.py` may be modified**
- Fixed 5-minute wall-clock training budget per run
- Goal: lowest `val_bpb`
- > "a small improvement that adds ugly complexity is not worth it"

Tracking : TSV avec colonnes `commit, val_bpb, memory_gb, status, description`. Statuses : `keep`, `discard`, `crash`.

Core loop : modify → commit → run → log → keep/revert. > "Never stop"

**Pattern transposable** : un fichier markdown unique + rules strictes + tracking en TSV/markdown append-only. C'est la structure minimale de "schema file" Karpathy.

---

## Section 5 — `forrestchang/andrej-karpathy-skills` (CLAUDE.md viral)

### 5.1 Contenu intégral (verbatim, 70 lignes)

**4 sections** :

**1. Think Before Coding**
> "Surface assumptions and ambiguity first. If multiple interpretations exist, present them — don't pick silently."

**2. Simplicity First**
> "Write only what's needed. No features beyond what was asked. A useful self-check: would a senior engineer call this overcomplicated?"

**3. Surgical Changes**
> "Modify only what's necessary. Don't 'improve' adjacent code, comments, or formatting. Clean up only what your own edits orphaned."

**4. Goal-Driven Execution**
> "Convert tasks into verifiable outcomes. Example: 'Fix the bug' becomes 'Write a test that reproduces it, then make it pass.'"

Plan format multi-step :
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

### 5.2 Statut endorsement

- 110,000+ stars en ~3 mois
- 28 jours consécutifs #1 GitHub Trending hebdo
- **Karpathy a-t-il publiquement endorsé ce repo ?** → Non trouvé d'endorsement explicite dans les sources consultées le 22 mai 2026. Le repo est une **transcription** par Forrest Chang du thread X 26 janvier de Karpathy, pas une production Karpathy. À traiter comme "interprétation fidèle reconnue" (succès viral) mais **pas canonique au sens d'une publication Karpathy**.

### 5.3 Pertinence forge-brain

Ces 4 principes sont **doctrine code agent**, pas doctrine vault. Ils complètent le LLM Wiki (qui ne parle pas de coding agent discipline) — les deux sont orthogonaux.

Pour forge-brain (vault), ce n'est pas la source à imiter. Le gist `llm-wiki.md` reste la référence.

---

## Section 6 — Karpathy chez Anthropic : confirmé

**Date** : 19 mai 2026 (3 jours avant aujourd'hui).
**Sources confirmant** : CNBC, TechCrunch, VentureBeat, Axios, Yahoo Finance, TechRepublic, X (tweet officiel Karpathy).
**Rôle** : équipe pretraining Claude + lance équipe "Claude-accelerated pretraining research".
**Background** : OpenAI co-founder (jusqu'2017), Tesla AI (jusqu'2022), OpenAI return (1 an), Eureka Labs (éducation, 2024-2026), Anthropic (mai 2026).

**Implication stratégique forge-brain** :
- Karpathy va influencer directement Claude (et donc Claude Code) sur les prochaines années
- Son pattern LLM Wiki a une chance accrue d'être intégré comme "first-class" dans le produit
- Investir maintenant sur ce pattern = aligné avec la trajectoire Anthropic

---

## Section 7 — SYNTHÈSE : 8 questions stratégiques

### Q1 — Structure idéale d'un vault Obsidian pour LLM selon Karpathy ?

**3 couches strictes** :
1. `raw/` — sources immuables (papers, articles, transcripts, screenshots)
2. `wiki/` — markdown LLM-owned (humain ne touche pas)
3. Schema file racine (`CLAUDE.md` ou `AGENTS.md` ou `program.md`)

Sous `wiki/` : dossiers par domaine (people/, projects/, decisions/, etc.). Pas de prescription sur les noms exacts.

**Au-delà** : Karpathy refuse explicitement de prescrire la structure interne ("intentionally abstract", "pick what's useful").

### Q2 — Fichiers OBLIGATOIRES dans un vault ?

**2 seulement**, explicitement mentionnés :

1. **`index.md`** — content-oriented, catalogue de toutes les pages avec lien + one-line summary. LLM le lit EN PREMIER au query time. Tient bien jusqu'à ~100 sources / hundreds of pages.
2. **`log.md`** — chronological append-only, format `## [YYYY-MM-DD] action | titre`. Parseable Unix.

**Implicite obligatoire** : un schema file racine (CLAUDE.md / AGENTS.md / program.md).

### Q3 — Opérations canoniques (verbatim) ?

**3** : **ingest**, **query**, **lint**.

- **ingest** : one source at a time (préférable au batch), touche 10-15 pages par source
- **query** : index.md d'abord, citations, formats variés (md/table/Marp/chart/canvas), **good answers refiled into wiki**
- **lint** : eslint for knowledge — contradictions, stale, orphans, missing pages, missing cross-refs, data gaps

### Q4 — Format frontmatter recommandé ?

**Karpathy ne prescrit RIEN**. Le gist est silencieux sur le frontmatter. La communauté a convergé sur un format minimal :
```
**Tags**: #...
**Created**: ...
**Last Updated**: ...
```

→ Notre spec forge-brain (4-6 aliases, derniere-maj, resume, tags, 2+ wikilinks) est **plus stricte que Karpathy**. C'est défendable (qualité supérieure) mais ce n'est PAS la canon Karpathy. Choix à assumer.

### Q5 — Stratégie de navigation : flat vs nested, MOC, tags, aliases ?

**Karpathy verbatim** :
- Index.md = navigation primaire (catalogue)
- Obsidian graph view = "see the shape of your wiki — what's connected"
- Cross-references entre pages = critique (le lint vérifie qu'il n'y a pas d'orphans)

**Pas mentionné** : MOCs explicites, hiérarchie de tags, aliases.

**Implication** : Karpathy mise sur **index.md + cross-links + graph view**. Pas de MOC formel ni de système de tags élaboré. Notre `00-Hub/` à `07-Prompts/` numéroté et nos MOCs **sont des ajouts** au-delà de la canon Karpathy — défendables mais à justifier.

### Q6 — Différence vault Karpathy vs forge-brain actuel

| Dimension | Karpathy LLM Wiki | forge-brain actuel | Verdict |
|-----------|-------------------|--------------------|---------|
| Couches | 3 (raw/wiki/schema) | 1 (tout mélangé) | **ÉCART MAJEUR** — pas de `raw/` immuable |
| Index racine | `index.md` obligatoire | aucun fichier index single-source | **MANQUE** |
| Log | `log.md` append-only | aucun log chronologique | **MANQUE** |
| Schema | CLAUDE.md / AGENTS.md / program.md UNIQUE | éparpillé (CLAUDE.md + 8 rules + skills) | **DIFFÉRENT mais défendable** |
| Structure top-level | flat sous `wiki/` (people/, projects/) | 7 dossiers numérotés + `Knowledge/` + `1-Projets/` + `2-Casquettes/` | **PLUS COMPLEXE que Karpathy** |
| Frontmatter | non spécifié | strict (aliases, resume, tags, derniere-maj) | forge-brain plus rigoureux |
| MOCs | non mentionnés | présents (`00-Hub/`) | ajout forge-brain |
| Opérations | ingest/query/lint nommées | implicites (search_brain, create_note, etc.) | **MANQUE OPS NOMMÉES** |
| Tracking ingestion | log.md | aucun | **MANQUE** |
| Lint scheduled | recommandé | absent | **MANQUE** |

**Bilan** : forge-brain est PLUS RICHE que la canon Karpathy sur les conventions de qualité (frontmatter strict, aliases, MOCs), mais MANQUE les fondamentaux :
- Pas de séparation raw/wiki (pas de sources immuables archivées)
- Pas d'`index.md` single source of truth
- Pas de `log.md` chronologique
- Pas d'opération `lint` schedulée

### Q7 — Comment Karpathy résout "vault bruité avec doublons" ?

**Réponse Karpathy** : c'est exactement le rôle du **lint**. Cibles :
- "contradictions between pages"
- "stale claims that newer sources have superseded"
- "orphan pages with no inbound links"
- "important concepts mentioned but lacking their own page"
- "missing cross-references"

Lint = eslint for knowledge → schédulable (daily/weekly) ou ad hoc. C'est l'opération AGENT, pas humaine.

**Implication forge-brain** : créer une opération `lint` (skill ou agent automatique) qui scanne le vault à intervalle régulier. On a déjà `vault-audit` — à étendre pour cibler les 6 patterns Karpathy explicitement.

### Q8 — Architecture "agentic engineering" complète selon Karpathy

3 piliers convergents (jamais réunis explicitement par Karpathy, mais cohérents) :

1. **Agent coding discipline** (thread janv 2026 + forrestchang CLAUDE.md) : think before coding, simplicity, surgical changes, goal-driven verification.
2. **LLM Wiki** (gist avril 2026) : vault 3 couches + 3 ops + index/log + Obsidian.
3. **Software 3.0 / context engineering** (Sequoia) : context window = programming surface, autonomy slider, markdown-first docs, agent-readable everything.

Le glue : tout est **markdown-first, agent-readable, human-curatable, LLM-maintained**. Le vault Karpathy est l'incarnation de Software 3.0 appliqué à la connaissance personnelle.

---

## Recommandations de refonte forge-brain (Jarvis)

### Priorité 1 — Manques fondamentaux Karpathy

1. **Créer `index.md` racine** — catalogue auto-maintenu de toutes les notes avec one-liner. Skill `index-rebuilder` qui regénère depuis frontmatter + premier paragraphe.
2. **Créer `log.md` append-only** — chaque ingestion/création/modification majeure y est tracée, format `## [YYYY-MM-DD] <action> | <titre>`. Hook PostToolUse sur `create_note`/`update_property` pour append automatique.
3. **Séparer `raw/`** — créer un dossier dédié aux sources brutes (transcripts cc-news, articles defuddle, exports x-read). Règle : LLM lit, ne modifie jamais. Aujourd'hui c'est mélangé dans `0-Inbox/`.
4. **Skill `lint-vault`** — schedulable hebdomadaire via `/loop`, cible les 6 patterns Karpathy (contradictions, stale, orphans, missing pages, missing crossrefs, gaps).

### Priorité 2 — Aligner conventions

5. **Schema file unique** — décider : on garde CLAUDE.md éparpillé en rules/ OU on consolide à la Karpathy. Mon avis : garder l'éparpillé (composable, hooks) mais ajouter un `vault/CLAUDE.md` minimal qui pointe vers les ops canoniques.
6. **Renommer ops MCP forge-brain** — `search_brain` → garder, mais wrapper en `ingest`, `query`, `lint` au niveau skill pour matcher le vocabulaire Karpathy.

### Priorité 3 — Ne PAS toucher (forge-brain mieux que Karpathy ici)

7. Frontmatter strict (aliases/resume/tags/derniere-maj) — garder, c'est un PLUS qualité.
8. MOCs (`00-Hub/`) — garder, complémentaire à index.md.
9. Dossiers numérotés ontologie utilité — garder (inspiré Eliott Meunier Prisme One, validé).
10. Knowledge/ (erreurs, critiques, raisonnements) — garder, c'est notre cycle d'apprentissage Jarvis.

### Question ouverte

**Le pattern Karpathy "wiki = LLM-owned, humain ne touche pas"** est-il compatible avec notre usage où Raphael édite parfois directement les notes ? À trancher : soit on accepte le mode hybride (humain peut éditer mais marker `human-edited: true`), soit on bascule purement LLM-owned.

---

## Trous identifiés dans la recherche

- Tweet X Karpathy 2 avril 2026 (annonce LLM Wiki) : **pas accédé en verbatim direct** — reconstitué via couverture presse (16M+ vues). Si besoin du tweet original, utiliser skill `x-read` sur `x.com/karpathy/status/<id>` (id non récupéré ce jour).
- Talks Dwarkesh Patel récents Karpathy : non explorés ce tour (cap respecté : 1-2 talks max → Sequoia couvert).
- Statut endorsement public Karpathy sur `forrestchang/andrej-karpathy-skills` : non trouvé. À re-vérifier via x-read direct si critique.

## Liens vault

- [[reference_agentic_engineering]] — note existante Karpathy Sequoia, à enrichir avec ce qu'on vient de capturer
- [[reference_boris_thariq_bestpractices]] — converge sur la même philosophie agent coding (Boris) + vault (à créer)
- [[reference_eliott_meunier_prisme]] — autre inspiration vault (ontologie utilité), complémentaire à Karpathy
- [[Knowledge/raisonnements/raisonnement-22mai-doctrine-vs-enforcement]] — raisonnement frère sur l'application hooks/doctrine
