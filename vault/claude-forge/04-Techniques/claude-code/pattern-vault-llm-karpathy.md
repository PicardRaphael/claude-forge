---
titre: "Pattern vault LLM canonique Karpathy"
resume: "Pattern Karpathy LLM Wiki — 3-layers (raw/wiki/schema), 3 ops (Ingest/Query/Lint), 2 fichiers obligatoires (index.md + log.md). Métaphore Obsidian IDE / LLM programmer / wiki codebase. qmd = Tobi Lütke (PAS Karpathy). Karpathy chez Anthropic depuis 19 mai 2026."
aliases:
  - "pattern vault llm karpathy"
  - "karpathy llm wiki"
  - "vault canonique karpathy"
  - "3-layers raw wiki schema"
  - "ingest query lint"
  - "index.md log.md"
  - "obsidian IDE llm programmer"
  - "qmd tobi lutke"
  - "agentic engineering memory"
  - "compounding wiki"
derniere-maj: 2026-07-16
auteur: claude
type: pattern
sources:
  - "Karpathy Gist 4 avril 2026 — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
  - "Sequoia AI Ascent 29 avril 2026 — Karpathy"
  - "Thread X Karpathy 26 janvier 2026"
  - "github.com/forrestchang/andrej-karpathy-skills"
tags:
  - "#type/pattern"
  - "#domaine/vault"
  - "#domaine/karpathy"
  - "#domaine/llm-wiki"
---
# Pattern vault LLM canonique Karpathy

> ## ⚠️ STATUT 2026-06-27 — forge-brain s'est ÉMANCIPÉ de ce pattern
>
> **[[decision-vault-agent-first]]** : forge-brain est un **cerveau d'agent** piloté via MCP (Obsidian débranché de fait). Karpathy = échafaudage de départ, **pas la cible**. Ce que forge-brain n'applique plus :
> - **`raw/` supprimé** (8 notes `git rm`) — sources distillées directement en wiki/, pas de couche brute immuable. La règle « LLM modifie raw/ = bug fatal » est **caduque pour forge-brain**.
> - **`index.md` + `log.md`** : plus « obligatoires » — couche humaine **optionnelle**, non auto-maintenue.
> - **MOCs** : couche humaine optionnelle, non auto-maintenue (non supprimés : ~95 backlinks).
>
> **Cette note reste un document de référence** sur le pattern Karpathy générique, **valide pour d'autres vaults** (neo_ia, neoteem-brain). Les sections **DRIFT D'IMPLÉMENTATION** et **REQUALIFICATION POST-MESURE** plus bas sont la **trace historique** du raisonnement (8 juin) — leur conclusion à jour est désormais : **décision délibérée agent-first**, pas « écart à réparer ».
>
> **Condition de falsification (raw/)** : si un incident d'hallucination réel remontant à une source non archivée émerge → re-créer `raw/` pour ce besoin précis, **sans rouvrir le pivot agent-first global**.

> Note canonique forge — pattern Karpathy LLM Wiki (Gist 4 avril 2026), application à forge-brain.

---

## QUOI — Définition

**Pattern Karpathy LLM Wiki** = architecture de mémoire long-terme pour LLM, dans laquelle :
- Le **vault** sert de "codebase" du LLM
- **Obsidian** sert d'IDE
- Le LLM lui-même est le "programmer" qui ingère, écrit, lint le wiki

**Verbatim Karpathy** ([Gist 4 avril 2026](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) :

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

**Karpathy a rejoint Anthropic le 19 mai 2026** — équipe pretraining + Claude-accelerated research. Confirmé CNBC/TechCrunch/X officiel. Le pattern Karpathy devient ainsi un pattern Anthropic de facto.

---

## POURQUOI — Le problème résolu

Sans pattern structuré, un vault LLM accumule :
- **Notes inconsistantes** — chacune réinvente sa structure
- **Pas de lifecycle** — pas d'Ingest formel, pas de Lint
- **Pas d'index navigable** — le LLM cherche aveuglément
- **Pas de log** — pas de trace des décisions / actions

Avec pattern Karpathy :
- **3 layers stricts** — séparation raw / wiki / schema
- **3 ops formelles** — Ingest / Query / Lint
- **2 fichiers obligatoires** — `index.md` (orientation LLM) + `log.md` (trace append-only)
- **Compounding** — le wiki s'enrichit, le LLM s'améliore

### 4 failure patterns LLM coding (thread X Karpathy 26 janvier 2026)

Patterns que ce vault aide à éviter :
1. **Silent assumptions** — Claude assume sans le dire
2. **Hypertrophy** — Claude génère trop, hors scope
3. **Collateral changes** — Claude modifie ce qui ne devait pas l'être
4. **No verifiable success criteria** — output non-vérifiable

Le wiki LLM rend explicites les assumptions, scope, modifications attendues, et critères vérifiables.

---

## COMMENT — 3 layers

### Layer 1 — `raw/` (sources immuables)

**Rôle** : tout ce qui vient de l'extérieur, en l'état.
- Articles, papers, transcripts de talks
- Web clips (Obsidian Web Clipper)
- PDF, slides Marp
- Fichiers téléchargés

**Règle** : **JAMAIS modifié par le LLM**. Lecture seule. Source de vérité brute.

### Layer 2 — `wiki/` (LLM-owned markdown)

**Rôle** : le LLM y écrit, restructure, compound.
- Notes atomiques (1 concept = 1 note)
- Wikilinks `[[Note]]`
- Frontmatter (aliases, tags, derniere-maj)
- Compounding : chaque erreur observée → note dans `wiki/Knowledge/erreurs/`

**Règle** : **LLM owns this**. L'humain peut éditer, mais le LLM est le mainteneur principal.

### Layer 3 — `CLAUDE.md` ou `AGENTS.md` (schema)

**Rôle** : le contrat entre humain et LLM.
- Conventions du vault
- Règles d'écriture (frontmatter standard, naming)
- Boundaries (que faire, ne pas faire)

**Règle** : **schema partagé**. Mis à jour rarement, validé humain.

---

## QUAND — Critère d'application

### Appliquer le pattern quand :
- Vault de notes LLM > 50 notes
- Plusieurs sources externes consommées régulièrement (papers, transcripts, web)
- Besoin de compounding sur erreurs / apprentissages
- Multi-agents accèdent au même vault

### Pattern allégé quand :
- < 50 notes : juste un dossier flat suffit
- Vault personnel non-LLM : pas besoin de schema strict
- One-shot : pas de structure complexe

---

## WORKFLOW — 3 opérations

### 1. **Ingest** — capturer une source externe

```
Source externe (talk, article, paper)
    ↓
Layer 1 : raw/ (capture brute, immuable)
    ↓
LLM Ingest : extrait concepts atomiques
    ↓
Layer 2 : wiki/ (notes atomiques avec wikilinks)
    ↓
Mise à jour : index.md + log.md
```

**Tooling** : Obsidian Web Clipper pour web, Whisper pour vidéos, Marp pour slides.

### 2. **Query** — répondre à une question via le wiki

```
Question utilisateur
    ↓
LLM cherche dans wiki/ via :
  - search_brain (FTS5)
  - read_note (par nom/alias)
  - get_backlinks (graphe)
    ↓
Compose réponse à partir des notes trouvées
    ↓
Cite les notes (wikilinks vers sources)
```

**Tooling Karpathy** : **qmd** (créé par **Tobi Lütke, CEO Shopify**, recommandé par Karpathy). qmd = BM25 + vector + reranker, exposé **CLI ET MCP** les deux.

**Tooling forge** : MCP forge-brain (11 outils, FTS5 SQLite, alias expansion FR, BM25 pondéré 10/1/8).

### 3. **Lint** — maintenir la qualité du wiki

```
LLM scanne wiki/ régulièrement :
  - Notes orphelines (aucun wikilink entrant)
  - Frontmatter incomplet
  - Aliases manquants
  - derniere-maj > X jours
  - Liens cassés (wikilink vers note inexistante)
    ↓
Propose corrections → humain valide
    ↓
Met à jour log.md (action de lint)
```

**Tooling forge** : skills `/vault-audit`, `/forge-review` mensuel.

---

## 2 fichiers obligatoires (verbatim Karpathy)

### `index.md` — content-oriented (lu en premier par LLM)

**Pas un sommaire**. **Un index navigable orienté contenu**.

Structure type :
```markdown
# Index

## Concepts clés
- [[Note A]] — résumé 1 ligne
- [[Note B]] — résumé 1 ligne

## Domaines principaux
- Domaine X : [[Note 1]], [[Note 2]]
- Domaine Y : [[Note 3]], [[Note 4]]

## Erreurs documentées
- [[erreur-foo]] — résumé
```

Quand le LLM cherche un sujet, il commence par `index.md` pour s'orienter.

### `log.md` — append-only, format strict

**Verbatim Karpathy** — format `## [YYYY-MM-DD] action | titre` :

```markdown
## [2026-05-22] note-created | comment-ecrire-claudemd
- Source : Code with Claude London + docs Anthropic
- Liens : [[CLAUDE.md]] [[memory]]

## [2026-05-22] note-updated | erreur-hooks-workflow
- Doctrine 22 mai inversée
- Liens : [[raisonnement-22mai-doctrine-vs-enforcement]]

## [2026-05-21] vault-audit | refonte doctrine
- 8 notes supprimées
- 4 notes réécrites
```

**Append-only** : on ne réécrit jamais l'historique. Le log est une trace.

---

## APPELS — Composants mobilisés

- [[comment-ecrire-claudemd]] — `CLAUDE.md` = layer 3 schema
- [[comment-creer-skill]] — skills pour opérations Ingest/Query/Lint
- [[comment-creer-agent]] — agents pour orchestrer les ops
- [[mcp-vs-skills-doctrine]] — MCP forge-brain = tooling Query
- [[workflow-claude-code-optimal]] — compounding base
- [[methode-analyser-repo]] — analyser un repo pour proposer son vault LLM

---

## OPTIMISATION — 3 niveaux

### Niveau basique (Karpathy minimal)
- 3 layers respectés (raw/wiki/schema)
- 2 fichiers obligatoires (index.md + log.md)
- Frontmatter minimal (alias + date)

### Niveau avancé (Karpathy + tooling)
- + qmd (Tobi Lütke) pour Query : BM25 + vector + reranker
- + Obsidian Web Clipper pour Ingest web
- + Marp pour slides
- + Dataview pour requêtes vault
- + git pour versioning

### Niveau expert (pattern générique — applicable à tout vault LLM)

**Frontmatter strict** (au-delà du minimum Karpathy) :
- 4-6 aliases minimum par note pour findability (FR + EN + variantes)
- `resume` 1 phrase spécifique obligatoire (pas générique)
- `derniere-maj` ISO obligatoire (détection notes obsolètes)
- 2+ wikilinks minimum (graphe dense)
- Tags type + domaine obligatoires
- Templates (Templater) pour cohérence

**Tooling custom MCP** :
- MCP custom pour le vault (FTS5 + alias expansion + content-hash watcher)
- Agents dédiés maintenance (project-auditor) + skill `/vault-audit`
- Skills dédiées format (obsidian-markdown)
- Pipeline news → capitalisation atomique systématique
- Sous-dossiers Knowledge structurés (erreurs / critiques / raisonnements / reviews)

---

## EXEMPLE D'APPLICATION — vault forge-brain (référence personnelle)

> Cette section illustre l'application du pattern Karpathy sur un vault réel. Elle est **descriptive**, pas prescriptive.

### Stats vault forge-brain (au 22 mai 2026)
- **318 notes** réparties dans dossiers ontologiques
- **1774 aliases** (moyenne 5.6 par note)
- **1508 wikilinks** internes
- **118 tags** structurels

### Tooling custom forge
- MCP forge-brain (port 8091, FastMCP 2 + pyyaml + SQLite FTS5)
- 11 outils MCP (search_brain, read_note, get_backlinks, vault_stats, etc.)
- 4 forces uniques : fallback search 4-strat, alias expansion FR avec stem variants, content-hash short-circuit watcher, BM25 pondéré 10/1/8

### Agents forge mobilisés
- `/vault-audit` (lint, dédoublonnage — skill session principale, MCP effectif)
- `project-auditor` (audit cohérence)
- `devils-advocate` (critique avant livraison)

### Slash commands forge
- `/forge-review` (audit mensuel)
- `/dream` (cross-session memory review, equiv Anthropic Dreaming)
- `/recap` (snapshot contexte)
- `/done` (capitalisation fin de session)

**NB** : ces détails sont spécifiques au forge. Le pattern Karpathy générique reste applicable avec d'autres outils (qmd, Obsidian natif, Dataview, etc.).

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| 3 layers stricts | Pas de pollution sources → wiki. Lifecycle clair. |
| `index.md` content-oriented | LLM s'oriente en 1 lecture vs cherche aveuglément |
| `log.md` append-only | Trace complète des actions, debug post-mortem possible |
| Aliases 4-6 minimum (forge dépasse Karpathy) | Findability ×3 vs aliases bricolés ad-hoc |
| MCP custom forge-brain | 4 forces uniques (fallback 4-strat, alias FR, content-hash, BM25 pondéré) |
| qmd (Tobi Lütke) | BM25 + vector + rerank = retrieval bien meilleur que keyword seul |
| Compounding wiki | LLM s'améliore session après session sur le même vault |

---

## ANTI-PATTERNS

### Layers
- ❌ **LLM modifie raw/** — viole l'immutabilité, perte de source de vérité
- ❌ **Tout dans wiki/ sans raw/** — pas de séparation source vs production
- ❌ **Pas de schema (CLAUDE.md/AGENTS.md)** — LLM invente les conventions

### Fichiers obligatoires
- ❌ **Pas d'`index.md`** — LLM cherche aveuglément, perte temps + tokens
- ❌ **`index.md` = sommaire généré** — doit être content-oriented, pas table des matières
- ❌ **Pas de `log.md`** — pas de trace, debug impossible
- ❌ **`log.md` modifié rétroactivement** — viole append-only

### Tooling
- ❌ **Attribuer qmd à Karpathy** — créé par **Tobi Lütke, CEO Shopify**
- ❌ **Confondre `qmd` avec MCP forge-brain** — qmd = retrieval (BM25+vector+rerank), MCP forge-brain = accès vault avec 11 outils
- ❌ **Grep/Read brut sur vault MCP-indexé** — utiliser MCP (cf [[forge-brain-proactive]])

### Frontmatter
- ❌ **Aliases bricolés** sans variantes FR/EN/abrév — findability dégradée
- ❌ **`resume` générique** ("note sur X") — doit être spécifique
- ❌ **`derniere-maj` absente ou stale** — pas de détection notes obsolètes

### Architecture
- ❌ **Plusieurs vaults sans index croisé** — silos
- ❌ **Vault sans backup git** — perte catastrophique possible
- ❌ **Vault sans audit régulier** — accumulation de doublons et contradictions (cf chantier 22 mai forge)

---

## EXEMPLES CONCRETS — Repos externes

### Karpathy lui-même
- **[Gist LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** — pattern verbatim 4 avril 2026
- **`karpathy/nanochat/.claude/skills/read-arxiv-paper/SKILL.md`** — seul skill public Karpathy, ~40 lignes
- **0 vidéo dédiée au vault**, **0 repo public dédié au vault** — le Gist est la référence unique

### Tooling Karpathy recommandé
- **qmd** (Tobi Lütke) — BM25+vector+rerank, CLI+MCP, retrieval
- **Obsidian Web Clipper** — Ingest web
- **Marp** — Ingest slides
- **Dataview** (Obsidian plugin) — requêtes vault
- **git** — versioning

### Fan project viral (ex-forrestchang → multica-ai)
- **[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** — CLAUDE.md viral (URL active, l'original `forrestchang/andrej-karpathy-skills` redirige vers ce repo). **NB** : pas endorsé par Karpathy publiquement, c'est un fan project. Stars exactes à vérifier à date.
- 70 lignes, 4 principes
- Démonstration "court + opinionated > long + neutre"

### Forge (référence personnelle — application concrète du pattern, voir section dédiée plus haut)
- Section "EXEMPLE D'APPLICATION" ci-dessus pour les détails forge spécifiques
- Pattern Karpathy générique applicable à tout vault LLM avec n'importe quel tooling (qmd, MCP custom, Obsidian natif + Dataview)

---

## SOURCES — Verbatim avec URLs

### Karpathy
- [Gist LLM Wiki 4 avril 2026](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — pattern verbatim
- Thread X 26 janvier 2026 — 4 failure patterns LLM coding
- Sequoia AI Ascent 29 avril 2026 — "Vibe coding is over → Agentic engineering"
- 19 mai 2026 : Karpathy rejoint Anthropic (CNBC, TechCrunch, X officiel)
- Tweet original "vibe coding" : fév 2025

### Tobi Lütke (créateur qmd)
- CEO Shopify
- qmd open source : BM25 + vector + rerank, CLI + MCP

### Fan project viral (ex-forrestchang → multica-ai)
- [github.com/multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) — URL active, ex-forrestchang. Stars à vérifier.

### Anthropic (Karpathy chez eux)
- Équipe pretraining + Claude-accelerated research

---

## GOTCHAS — Pièges observés

### Pièges attribution
- **qmd ≠ Karpathy** — créé par **Tobi Lütke** (Karpathy le recommande, ne l'a pas créé)
- **`forrestchang/andrej-karpathy-skills` URL obsolète** : redirige vers `multica-ai/andrej-karpathy-skills` aujourd'hui. Citer la version active. Stars exactes à vérifier à date.
- **Fan project pas endorsé** publiquement par Karpathy

### Pièges layers
- **LLM qui modifie raw/** = bug fatal du pattern
- **Pas de séparation wiki vs raw** = source vs production mélangées
- **CLAUDE.md = schema, pas wiki** — ne pas confondre

### Pièges tooling
- **qmd CLI ET MCP** — Karpathy expose les deux, pas opposition (cf [[mcp-vs-skills-doctrine]])
- **MCP forge-brain auto-start SessionStart** port 8091
- **JAMAIS Grep/Read brut sur vault** — MCP uniquement (cf [[forge-brain-proactive]])
- **JAMAIS CLI Obsidian** (doctrine MCP forge-brain uniquement — feedback `use-obsidian-cli` archivé 27 mai car obsolète)

### Pièges Obsidian
- **Web Clipper** : peut altérer le HTML sur certains sites, vérifier le markdown produit
- **Whisper** transcripts : cap 5 vidéos pour ne pas exploser coût
- **Dataview** : requêtes dynamiques mais coûteuses sur gros vault

### Pièges forge
- **318 notes** = vault actuel, croissance compounding
- **Standard qualité forge dépasse Karpathy** : 4-6 aliases min, resume spécifique, 2+ wikilinks
- **Audit mensuel** via `/forge-review` obligatoire
- **CHANGELOG.md** vault à jour après modifications notes (cf [[changelog-vault]])

### Pièges Karpathy chez Anthropic
- **Depuis 19 mai 2026** : équipe pretraining + Claude-accelerated research
- Pas encore de publication conjointe Anthropic + Karpathy à date du chantier
- Le pattern reste celui du Gist 4 avril 2026

---

## ALIASES — Findability

Aliases déclarés en frontmatter (10) :
- pattern vault llm karpathy
- karpathy llm wiki
- vault canonique karpathy
- 3-layers raw wiki schema
- ingest query lint
- index.md log.md
- obsidian IDE llm programmer
- qmd tobi lutke
- agentic engineering memory
- compounding wiki

---

## WIKILINKS

### Notes canoniques sœurs
- [[comment-ecrire-claudemd]]
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[mcp-vs-skills-doctrine]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]

### Fiches leaders (à créer)
- [[Andrej Karpathy]]
- [[Tobi Lutke]]

### Forge custom
- [[forge-brain-proactive]] — rule vault check MCP obligatoire
- [[changelog-vault]] — rule CHANGELOG vault
- [[obsidian-markdown]] — skill format vault
- skill `vault-audit` — vault audit (lint/dédoublonnage, session principale)
- [[project-auditor]] — agent audit
- [[forge-review]] — slash command audit mensuel

### Knowledge / refs liées
- audit-mcp-forge-brain — 11 outils + 4 forces uniques (note à créer)
- `use-obsidian-cli` — archivé 27 mai (obsolète) : accès vault = MCP forge-brain uniquement
- [[feedback_vault_quality_standard]] — standard 4-6 aliases
- [[feedback_vault_query_before_create]] — hook bloque write sans vault check

---

**Fin note canonique `pattern-vault-llm-karpathy.md`** — 8/8 chantier 22 mai 2026.

**🎉 LES 8 CANONIQUES SONT TERMINÉES.**

---

## CORRECTIONS POST-AUDIT 23 MAI 2026

Audit thématique vault forge a révélé les nuances suivantes (ne touche pas le pattern principal, juste les attributions/verbatim) :

### C7.3 — qmd attribution Tobi Lütke (nuance)

**Avant** : "qmd créé par Tobi Lütke (CEO Shopify)"
**Précision** : Handle `tobi` GitHub historiquement Tobias Lütke (Shopify CEO), confirmé par npm `@tobilu/qmd` et sources tierces (Medium). **Attribution communément acceptée mais non signée dans README officiel**. Karpathy le recommande dans son Gist LLM Wiki — il ne l'a pas créé.

### C7.5 — "Vibe coding is over" → titre exact

**Avant** : "Vibe coding is over → Agentic engineering" (Sequoia 29 avril 2026)
**Correction** : titre exact = **"From Vibe Coding to Agentic Engineering"**. Karpathy positionne les deux en **complémentaires** :
- Vibe coding = "raise the floor" (rendre accessible)
- Agentic engineering = "preserve the quality bar" (maintenir la qualité)

Pas un remplacement, une transition / complémentarité.

### C7.4 — 4 failure patterns labels (nuance)

**Avant** : "silent assumptions / hypertrophy / collateral changes / no verifiable success criteria" présentés comme verbatim Karpathy
**Précision** : Les **labels courts** sont des **synthèses communautaires** du thread X Karpathy 26 janvier 2026, pas verbatim Karpathy. Les concepts sous-jacents sont attestés (6+ sources convergentes), mais les noms exacts viennent de l'écosystème (vault forge, articles tiers).

**URL thread X 26 janvier 2026** : à reconstruire via archive.org si lien original mort.

---

**Pattern principal Karpathy (3 layers + 2 fichiers obligatoires + 3 ops) reste 100% canonique.** Ces corrections ne touchent que les attributions / verbatim secondaires.

Source audit : `output/audit-vault-thematique/01-claude-code/B-verif-cluster7-karpathy.md`


---

## DRIFT D'IMPLÉMENTATION CONSTATÉ — 8 juin 2026 (vérif empirique vault réel)

> Le pattern (architecture) reste 100% canonique. Cette section documente l'**écart entre la doctrine et l'état RÉEL du vault**, mesuré le 8 juin 2026 (`vault_stats`, `usage_stats(30j)`, `list_notes("raw")`, lecture `index.md`/`log.md` racine). Constat déclencheur : comparaison forge-brain vs pattern Karpathy demandée par Raphael. Les écarts du 22 mai (cf `recherche-karpathy-vault-canonique`, note raw/ supprimée au pivot agent-first) ont été PARTIELLEMENT comblés puis ont **re-dérivé**.

### 3 organes obligatoires Karpathy — état réel

| Organe Karpathy | Doctrine | État réel 8 juin 2026 | Verdict |
|---|---|---|---|
| **`raw/` (sources immuables)** | Alimenté à CHAQUE ingest (10-15 pages/source) | **8 notes, TOUTES du chantier 22 mai**. cc-news/x-read/defuddle/watch transforment la source en note wiki sans archiver le brut. | **ABANDONNÉ depuis le 22 mai** — plus gros écart |
| **`index.md` (lu en premier au Query)** | Catalogue content-oriented à jour | Existe mais **figé au 22 mai** : annonce « 318+ notes » alors que `vault_stats` = **480** (stale +51%, 162 notes invisibles à l'index) | **STALE** — l'organe censé orienter ment |
| **Query = qmd (BM25 + vector + rerank)** | Retrieval hybride recommandé nommément | `search_brain` = FTS5 **BM25 lexical pur**, 0 vectoriel, 0 rerank. Et c'est l'outil **n°1 en usage : 1237 appels/30j** (vs read_note 593). | **MOITIÉ VECTORIELLE ABSENTE** — l'outil le plus utilisé est le moins aligné |

### Lecture honnête

- **Outillage serveur** : forge-brain **dépasse** le Gist Karpathy (read_section gain 30x, pagination autoguidée, `lint_vault` 35 appels/30j, usage_stats, lifecycle move/delete/bulk). Le Gist est volontairement minimaliste là-dessus → surinvestissement assumé et justifié (cf [[mcp-vault-llm-design]], [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] verdict A).
- **Fondamentaux du pattern** : on a construit un **meilleur moteur** mais on **n'alimente plus 2 des 3 organes** (raw mort + index stale) et on a **sauté la moitié vectorielle** du retrieval. Le savoir RAG existe pourtant déjà dans le vault ([[rag-reranking]], [[rag-production]] : pipeline BM25+Dense→RRF→reranker, +15-30% RAGAS) — le manque n'est pas le savoir, c'est l'application à notre propre MCP.

### Distinction « manque à combler » vs « écarté faute de consommateur » (corrigé 8 juin après objection Raphael)

Tout manque vs Karpathy n'est PAS un défaut. Deux catégories à ne jamais confondre :

- **Manque à combler** = Karpathy le valorise ET on en a/aurait l'usage prouvé → angle mort réel, à réparer. Les 3 organes ci-dessus sont dans cette catégorie (raw mort, index stale, retrieval lexical) : ils sont *consommés en permanence* (le Query tourne à chaque session) donc leur dégradation a un coût réel.
- **Manque THÉORIQUE écarté faute de consommateur** = faisable mais sans demande prouvée → c'est de la **discipline anti-gonflage, PAS un défaut**. Ne jamais le capitaliser comme une lacune. Test décisif : **valoriser ≠ consommer** — un outil que Karpathy valorise mais qu'on ne consommerait pas reste à ne pas implémenter (mêmes critères que les limites #3/#4 du Chantier 5 et que `read_note_resolved` retiré pour 0 appel, cf [[mcp-vault-llm-design]] v1.4).

### Cas d'application de cette distinction

- **Traversée graphe multi-hop = manque THÉORIQUE écarté, PAS un angle mort.** `get_backlinks` (1-saut) existe mais est **quasi mort : 10 appels/30j**. `traverse_graph`/`find_concept_chain` (N-sauts) absents. **Faisabilité acquise** (table `links` présente, aucun frontmatter cross-stack requis pour la navigation pure) → l'écartement au Chantier 5 était **faute de BESOIN**, pas faute de possibilité. Si on ne consomme déjà pas le 1-saut, un N-sauts n'a aucune demande → cohérent avec la discipline. À réévaluer SI un consommateur réel émerge (ex. agent cartographiant un cluster de notes). Nuance vs critère #6 de [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] : #6 visait le typage cross-stack (vraiment « inapplicable sans pivot frontmatter ») ; la navigation pure, elle, est *faisable mais non demandée* — deux raisons distinctes, même conclusion « ne pas implémenter maintenant ». **Ma formulation initiale « on a écarté un manque réel en le qualifiant d'inapplicable » était fausse** : ce n'était ni un manque réel (pas de consommateur), ni écarté pour inapplicabilité (c'était faisable).
- **Tension « LLM-owned » jamais tranchée** : Karpathy = wiki LLM-owned, humain ne maintient pas. Raphael édite parfois en direct (d'où gotchas SQLite désync). Question ouverte depuis le 22 mai (marker `human-edited:` vs full LLM-owned), non décidée. Catégorie : *question doctrinale ouverte*, ni défaut ni discipline assumée tant que non tranchée.

### Réparations possibles (par ROI) — uniquement les 3 vrais manques

1. **#3 index.md (mécanique, gain immédiat)** : régénérer le catalogue depuis frontmatter actuel. Tout futur Query fidèle au pattern en bénéficie.
2. **#1 raw/ (doctrinal)** : rebrancher l'archivage de la source brute dans cc-news/x-read/defuddle/watch. Restaure la « source of truth » Karpathy → anti-hallucination (cf [[feedback_llm_deep_research_version_numbers]]).
3. **#2 retrieval hybride (structurel)** : POC vectoriel + rerank sur le MCP. Le plus lourd, le plus impactant sur l'outil n°1.

### Méta-leçon

Le drift doctrine↔réel se reproduit (cf `doctrine-drift-silent-regression` / `feedback_doctrine_drift_pattern`). Ici il est **silencieux car le système marche quand même** : on tape `search_brain` direct, donc l'index stale et le raw mort ne bloquent rien — le pattern Karpathy est contourné dans la pratique sans que personne ne l'ait décidé. **Un système qui fonctionne malgré un organe mort cache son propre drift.** Un `lint_vault` étendu devrait vérifier la fraîcheur de `index.md` (Karpathy : le lint cible « index entries that are stale »).

**Corollaire (objection Raphael 8 juin)** : symétriquement, ne pas sur-diagnostiquer. Un outil absent n'est un défaut que s'il a un consommateur. Vérifier `usage_stats` AVANT de qualifier un manque d'« angle mort » — sinon on confond la discipline anti-gonflage avec une lacune.


---

## REQUALIFICATION POST-MESURE — 8 juin 2026 (mesures `usage.jsonl` 30j)

> ⚠️ Cette section **ne réécrit pas** l'analyse « DRIFT D'IMPLÉMENTATION » ci-dessus (sa trace de raisonnement a sa valeur). Elle la **corrige sur l'implication**. Déclencheur : Raphael a demandé un diagnostic de décision sur critère **tokens ET/OU perf réelle**, pas conformité au pattern. Mesures faites sur `mcp-forge-brain/logs/usage.jsonl` (1239 `search_brain`/30j, lecture seule).

**Le CONSTAT tient** (les 3 organes sont dégradés vs le pattern Karpathy). **L'IMPLICATION était fausse** : « organe dégradé vs pattern » ≠ « défaut à réparer ». À la mesure, ② et ① sont des **écarts assumés justifiés par l'usage réel**, pas des chantiers. Même logique que les limites #3/#4 du Chantier 5 (cf [[mcp-vault-llm-design]]) : écart connu + déclencheur de réouverture. La conformité au pattern n'est jamais le critère — le besoin l'est.

### ② Retrieval vectoriel — ni gain tokens, ni gain perf → ÉCART ASSUMÉ

Mesures (1239 `search_brain`/30j) :
- Résultats à **0 chars : 0,3%** ; résultats pauvres (<400 chars) : **0,9%**.
- **Vrai ratage vocabulaire** (résultat pauvre suivi <90s d'une reformulation différente) : **11/1239 = 0,89%**.
- Classification des transitions search→search : **59% batch parallèle** (<2s, sujets distincts, même message), **20% séquences de notes différentes** (BM25 avait trouvé, `prev_chars` 1700-3900, on passe au composant suivant), **0,89% vrais ratages**.
- Les 11 ratages, lus un par un : presque tous des **recherches par nom de fichier exact** (`feedback_tests_adverses_ratio_3_1`, `skill-creator créer modifier skills`) → c'était `read_note` qu'il fallait, **pas** un problème sémantique. Un vectoriel n'en aurait sauvé quasiment aucun.
- **Bilan tokens NET = négatif** : économie plancher ~20k chars/mois (11 ratages) CONTRE surcoût = embedding de 1239 requêtes/mois + rerank + re-embedding de ~680k tokens de vault sur ~220 writes/mois.
- **Coût d'implémentation** : gros chantier (embeddings local/API, stockage vecteurs, pipeline RRF+reranker, éval — le pipeline production complet de [[rag-production]]) pour combler 0,89% de ratage non-sémantique.

**Verdict : le « 80% vraie exploration » de l'audit 7 juin est confirmé et sous-estimé — le ratage réel est <1% et non-sémantique.** BM25 pondéré + alias expansion FR couvre 99,1% de l'usage. Karpathy recommande qmd (BM25+vector+rerank), mais **notre usage réel ne génère pas le problème que qmd résout**.
**Trigger de réouverture** : si une mesure future montre un ratage **sémantique** (résultat pauvre + reformulation à vocabulaire proche du concept cherché, pas un nom de fichier) **> 5% des search_brain**, rouvrir l'arbitrage vectoriel.

### ① raw/ archivage des sources — ni tokens ni perf (c'est de la fiabilité), besoin non matérialisé → ÉCART ASSUMÉ

- Ce manque **ne touche NI tokens NI perf** : c'est un enjeu de **fiabilité** (re-vérifier une source brute, anti-hallucination, cf [[feedback_llm_deep_research_version_numbers]]).
- Mesure du besoin réel : **accès explicites à `raw/` en 30j = 0** (zéro `read_note`/`read_note_by_path` ciblant `raw/`, zéro recherche remontant à une source brute).
- Le risque théorique est réel **en principe**, mais le pattern d'usage actuel ne le déclenche pas : on cite des notes wiki, on ne remonte pas aux sources brutes archivées.

**Verdict : besoin de fiabilité non matérialisé (0 accès/30j) → écart assumé.**
**Trigger de réouverture** : au **1er incident d'hallucination réel remontant à une source non archivée** (une note cite un chiffre/fait faux qu'on ne peut pas re-vérifier faute de source brute). Pas avant.

### #3 index.md stale — HORS de cette requalification

Non mesuré ici (hors périmètre du diagnostic tokens/perf demandé). Reste un **geste mécanique possible** (régénérer le catalogue, quasi-gratuit), à évaluer séparément. Ne PAS le requalifier en écart assumé sans mesure (ce serait le sous-diagnostic inverse).

### Méta-leçon de la requalification

J'avais raison sur le constat (organes dégradés vs pattern), **tort sur l'implication** (défaut à réparer). La règle qui manquait : **mesurer le PROBLÈME sur l'usage réel avant de prescrire la SOLUTION**. Un écart au pattern canonique n'est un défaut que si l'usage réel génère le problème que le pattern prévient — sinon c'est de la conformité pour la conformité. Symétrique exact du garde-fou « valoriser ≠ consommer » (section traversée graphe) : ici c'est **« dévier du pattern ≠ avoir un problème »**. Cf [[feedback_measure_before_optimize]] (mesurer avant d'optimiser) appliqué non au code mais à la doctrine elle-même.

---

## VAGUE VIRALE JUILLET 2026 + CONSENSUS COMMUNAUTAIRE — capitalisé 2026-07-16

> Déclencheur : article X @chesny 15 juil. (reprise ES du guide viral) → recherche 15+ sources croisées. Le pattern Karpathy n'a PAS évolué à la source ; l'écosystème autour, si.

### État de la source

- **Gist inchangé depuis le 4 avril 2026** (1 seule révision = création, 5k+ stars/forks). **Karpathy silencieux sur le wiki depuis son arrivée chez Anthropic (19 mai)** — aucun post/talk wiki-related mai-juillet.
- Vault Karpathy (thread avril) : ~100 articles, ~400k mots, jamais écrits à la main.

### Vague virale 8-15 juillet (généalogie)

- **Guide canonique : @kirillk_web3, 8 juil.** (149k vues, mirror youmind.com/landing/x-viral-articles/karpathy-second-brain-claude-obsidian) : CLAUDE.md-schema verbatim (INGEST 8 étapes / QUERY avec « file the answer back » / LINT report-only), structure raw + raw/processed + wiki + index.md + log.md, weekly review, VPS 10 $/mois 24/7, alternative Kimi K2.7.
- **Reprises 13-15 juil.** : @chewadot, @MyWestLord, @chesny (version ES + storytelling « chico en China 15 000 notas »). Fiabilité curateurs FAIBLE : @chesnyfcb (même sphère) corrigé publiquement par kepano fin mai (claim « galaxie 3D » fausse). Kepano au passage : « je n'aime pas le terme second brain — écrire est une forme de penser ».
- **Ce que la vague AJOUTE vs gist avril** : (1) implémentation Claude Code native (CLAUDE.md auto-lu + slash commands /ingest /lint /query /save) ; (2) **/save = boucle refile formalisée** ; (3) couche kepano/obsidian-skills ~41k stars mi-juil. (forge a déjà 4/5 — obsidian-cli exclu par doctrine MCP-only) ; (4) scheduling 24/7 ; (5) hot.md cache + index.md en couche de routage.

### Modes d'échec documentés (retours 3+ mois d'usage réel)

- **Fausse absence** (répondre « pas de note » de mémoire, sans chercher) = failure mode n°1 sous-estimé (theaioperator). → Garde ajoutée à `.claude/rules/forge-brain-proactive.md` (16 juil.).
- **Débordement d'index** vers 150-200 pages sans discipline une-ligne-par-page ; drift nommage/style ; contradictions accumulées (kunalganglani, 147 pages/3 mois : *« rewards consistent use, falls apart under neglect »*).
- **Hallucination auto-certifiée** : le linteur est le même modèle qui a introduit l'erreur — une fausse référence écrite lundi est certifiée « consistent » mercredi (Proudfrog) → audits aléatoires tracés aux sources.
- Coûts réels mesurés : lint complet ~300k tokens/passe sur un wiki 100 articles.

### Consensus « ce qui fait vivre vs stagner un vault LLM »

1. **Gouvernance > infrastructure** — vectoriel = overkill sous ~100k tokens ; confidence tags, réconciliation, pruning, agents planifiés paient. (= validation externe de [[decision-vault-agent-first]] et de la requalification vectoriel du 8 juin, cf sections DRIFT/REQUALIFICATION supra.)
2. **Maintenance PLANIFIÉE, pas espérée** — agents cron nightly/weekly + consolidation post-session (Auto Memory/Dream natif Claude Code, mars 2026).
3. **Faits datés, jamais relatifs** — tampon `as of`, bi-temporalité (OKM) ; supersession explicite > décroissance numérique (« les scores de confiance flottants = fausse précision »).
4. **Ce qui vit est ce qui est UTILISÉ en boucle** : query → réponse refilée au wiki. Un vault seulement écrit stagne.

### Implémentations de pointe à surveiller

- **rohitg00 LLM Wiki v2** (gist ~1,6k stars, actif juil.) : graphe typé (uses/contradicts/supersedes) + traversal d'impact, hybrid search RRF, hooks event-driven (« on query → refile si quality > seuil »), crystallization des sessions de debug en digests.
- **eugeniughelbur/obsidian-second-brain v0.12** (3,3k stars, MIT) : self-rewriting à l'ingest (réécrit 5-15 pages au lieu d'appender), OKM bi-temporel, notes AI-first (« For future Claude »), 44 commandes dont `/obsidian-challenge` (le vault argumente CONTRE les décisions passées), 4 agents planifiés, hybrid search local mesuré (recall paraphrasé 77 % à 2 350 notes — trigger forge inchangé : >5 % ratages sémantiques).

### Application forge (16 juil. 2026)

- Diagnostic stagnation mesuré : vault sain (lint quasi 0), **consultation −80 %** (search_brain ~1240 → 236/30j) car **65 % des sessions de juin hors forge** sans MCP → **extension user-scope machine décidée** (Raphael, 16 juil.), voir [[decision-vault-agent-first]] § Validation externe.
- Boucle Query→refile mesurée morte (Knowledge/questions : 2 notes depuis création) → ligne refile ajoutée à forge-brain-proactive.
- NB drift : la skill `/dream` citée en « EXEMPLE D'APPLICATION » plus haut n'existe plus (supprimée dans un sweep) — remplacée par Auto Memory CC natif + `/done`.

Sources : gist karpathy 442a6bf (1 rev) · youmind kirillk_web3 · github.com/kepano/obsidian-skills · kunalganglani.com/blog/llm-wiki-karpathy-local-knowledge-base · theaioperator.io/p/karpathys-llm-wiki-v2-what-to-keep · proudfrog.com/en/insights/llm-wiki-skeptics-guide · gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2 · github.com/eugeniughelbur/obsidian-second-brain
