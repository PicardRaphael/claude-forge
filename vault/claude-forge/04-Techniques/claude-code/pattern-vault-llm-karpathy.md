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
derniere-maj: 2026-05-22
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
  - "#sujet/karpathy"
  - "#sujet/llm-wiki"
---

# Pattern vault LLM canonique Karpathy

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

**Tooling forge** : skills `/vault-audit`, `vault-maintainer` agent, `/forge-review` mensuel.

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
- Liens : [[raisonnement-22mai]]

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
- Agents dédiés maintenance (vault-maintainer, project-auditor)
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
- `vault-maintainer` (lint, dédoublonnage)
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
- **JAMAIS CLI Obsidian** (cf [[feedback_use_obsidian_cli]] — révisé)

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
- [[vault-maintainer]] — agent vault audit
- [[project-auditor]] — agent audit
- [[forge-review]] — slash command audit mensuel

### Knowledge / refs liées
- [[audit-mcp-forge-brain]] — 11 outils + 4 forces uniques
- [[feedback_use_obsidian_cli]] — révisé : MCP uniquement
- [[feedback_vault_quality_standard]] — standard 4-6 aliases
- [[feedback_vault_query_before_create]] — hook bloque write sans vault check

---

**Fin note canonique `pattern-vault-llm-karpathy.md`** — 8/8 chantier 22 mai 2026.

**🎉 LES 8 CANONIQUES SONT TERMINÉES.**
