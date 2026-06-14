---
titre: "Schema vault forge-brain — conventions self-describing"
resume: "Schema layer Karpathy : conventions d'ecriture du vault (frontmatter, aliases, wikilinks, dossiers). Self-describing pour qu'un LLM puisse comprendre le vault sans contexte externe."
aliases:
  - "schema vault"
  - "vault schema"
  - "conventions vault"
  - "AGENTS.md vault"
  - "self-describing vault"
  - "schema forge-brain"
derniere-maj: 2026-06-14
auteur: claude
type: schema
tags:
  - "#type/schema"
  - "#karpathy/schema"
---

# Schema vault forge-brain

> Pattern Karpathy LLM Wiki layer 3 (schema). Conventions self-describing pour qu'un LLM novice (ou n'importe quel outil cross-LLM type Hashimoto AGENTS.md) puisse ecrire dans le vault correctement.

---

## 1. Architecture 3-layers (Karpathy)

| Layer | Dossiers | Regle |
|-------|----------|-------|
| **raw/** (sources immuables) | `raw/<YYYY-MM-DD-contexte>/` | JAMAIS modifie par LLM. Web research, transcripts Whisper, papers, clips Defuddle. Lecture seule. |
| **wiki/** (LLM-owned) | `00-Hub/`, `01-Claude/` a `07-Prompts/`, `1-Projets/`, `2-Casquettes/`, `Knowledge/`, `0-Inbox/` | LLM ecrit, restructure, compound. Notes atomiques, frontmatter strict, wikilinks. |
| **schema/** (conventions) | `SCHEMA.md` (ce fichier), `index.md`, `log.md`, `CHANGELOG.md` | Schema partage humain/LLM. Mis a jour rarement. |

---

## 2. Frontmatter obligatoire

```yaml
---
titre: "Titre lisible humain"
resume: "1 phrase specifique decrivant ce que contient la note (pas generique)"
aliases:
  - "minimum 4 aliases (FR + EN + variantes + abreviation)"
  - "synonymes techniques"
  - "termes que utilisateur taperait en conversation"
derniere-maj: YYYY-MM-DD  # ISO format
auteur: claude | raphael
type: feature | changelog | best-practice | technique | leader | modele | concurrent | knowledge | erreur | critique | raisonnement | synthese | pattern | schema | index | log
sources:
  - "URL ou [[wikilink]] vers source"
tags:
  - "#type/<type>"
  - "#domaine/<domaine>"
---
```

### Aliases — minimum 4-6 par note

Choisir parmi :
- Nom complet FR
- Nom complet EN
- Abreviation / acronyme
- Variante avec/sans tirets/espaces
- Terme conversation utilisateur
- Synonyme technique

**Exemple bon** : `["claude-forge", "forge", "le forge", "framework forge", "forge personnel"]`
**Exemple mauvais** : `["claude-forge"]` (1 alias = findability dégradée)

### resume — specifique pas generique

- ❌ "Note sur Claude Code"
- ✅ "Backend IA Neoteem — FastAPI Python, agents autonomes, RAG sur 318 notes vault"

---

## 3. Wikilinks — minimum 2 par note

- Format : `[[Nom de note]]` ou `[[Note|Alias custom]]`
- JAMAIS de markdown link `[text](path.md)` pour notes internes
- Au moins 2 wikilinks par note pour graphe dense
- Wikilinks brisés (vers note inexistante) acceptés temporairement (= note a creer)

---

## 4. Ontologie dossiers — par utilite

| Je cree une note sur... | Dossier |
|------------------------|---------|
| Projet en cours | `1-Projets/<nom-projet>/` |
| Aire de responsabilite de vie | `2-Casquettes/` |
| Capture rapide a trier | `0-Inbox/` |
| Feature Claude Code | `01-Claude/Code/features/` |
| Best practice CC | `01-Claude/Code/best-practices/` |
| Note canonique CC (chantier 22 mai) | `04-Techniques/claude-code/` |
| Modele d'un fournisseur IA | `<NN>-<Fournisseur>/models/` (ex `01-Claude/models/`, `02-OpenAI/models/`) |
| Produit / outil d'un fournisseur IA | `<NN>-<Fournisseur>/products/` (ex `02-OpenAI/products/`, `09-Anysphere/products/`) |
| Technique RAG | `04-Techniques/rag/` |
| Technique agents | `04-Techniques/agents/` |
| Pattern/workflow reutilisable | `04-Techniques/patterns/` |
| Leader CC/Anthropic | `05-Leaders/claude-code/` |
| Leader agents | `05-Leaders/agents/` |
| Leader industrie | `05-Leaders/industrie/` |
| News industrie | `06-Industrie/` |
| System prompt reutilisable | `07-Prompts/system-prompts/` |
| Erreur commise | `Knowledge/erreurs/` |
| Critique devil's advocate | `Knowledge/critiques/` |
| Synthese d'analyse | `Knowledge/syntheses/` |
| Question technique resolue | `Knowledge/questions/` |
| Raisonnement multi-etapes | `Knowledge/raisonnements/` |
| Source externe brute | `raw/<YYYY-MM-DD-contexte>/` |

**Convention fournisseur (14 juin 2026)** : 1 dossier par acteur IA — Anthropic = `01-Claude`, puis `02-OpenAI`, `03-Google`, `08-xAI`, `09-Anysphere`, `10-Microsoft`… — contenant `models/` (modèles fondation : specs, benchmarks, pricing) et `products/` (apps, CLI, IDE, API), **créés à la demande** (pas de dossier vide). **Pas de dossier « Concurrents »** : les fournisseurs sont des acteurs suivis, pas des concurrents. Les comparatifs cross-fournisseurs (modèle-vs-modèle) vont en thématique (`04-Techniques/` ou une MOC `00-Hub/`), jamais dans un dossier acteur.

---

## 5. 3 operations Karpathy

### Ingest (capturer source → wiki)
1. Source externe (talk, article, paper, transcript)
2. Depose dans `raw/<YYYY-MM-DD-contexte>/` (Layer 1, immuable)
3. LLM extrait concepts atomiques → cree notes dans dossiers wiki (`01-` a `07-`, `Knowledge/`)
4. Mise a jour : `index.md` (nouveaux concepts) + `log.md` (action ingest)

### Query (chercher dans le wiki)
1. Question utilisateur
2. LLM cherche via MCP forge-brain : `search_brain`, `read_note`, `get_backlinks`
3. Compose reponse a partir des notes trouvees
4. Cite les notes (wikilinks vers sources)

### Lint (maintenir qualite)
1. Scan periodique (mensuel via `/forge-review`)
2. Detecte : notes orphelines, frontmatter incomplet, aliases manquants, derniere-maj > 30j, liens casses
3. Propose corrections → humain valide
4. Update `log.md` (action lint)

---

## 6. Outils MCP forge-brain (acces vault OBLIGATOIRE)

JAMAIS Grep/Read/Glob/CLI Obsidian brut sur le vault. **MCP uniquement** (port 8091, FTS5).

| Outil | Usage |
|-------|-------|
| `search_brain(query, limit)` | Recherche full-text FTS5 |
| `read_note(file)` | Lire par nom ou alias |
| `read_note_by_path(path)` | Lire par chemin exact |
| `get_backlinks(file)` | Naviguer le graphe |
| `get_tags()` | Vue structurelle |
| `get_property(file, name)` | Lire propriete frontmatter |
| `list_notes(folder, limit)` | Lister notes d'un dossier |
| `vault_stats()` | Stats vault |
| `create_note(path, content)` | Creer une note |
| `append_note(file, content)` | Ajouter a une note |
| `update_property(file, name, value)` | Modifier propriete |

---

## 7. Conventions edition

### Templates obligatoires
Lire le template AVANT de creer une note :
- Features CC → `Templates/feature.md`
- Best practices → `Templates/best-practice.md`
- Leaders → `Templates/leader.md`
- Modeles → `Templates/modele.md`
- Concurrents → `Templates/concurrent.md`
- Techniques → `Templates/technique.md`
- Knowledge → `Templates/knowledge.md`
- Erreurs → `Templates/erreur.md`
- Projets → `Templates/context-projet.md`
- Casquettes → `Templates/context-casquette.md`

### Format Obsidian Flavored Markdown
Utiliser la skill `obsidian-markdown` pour : wikilinks, callouts, frontmatter YAML, properties.

### Append vs Edit
- Ajouter du contenu → `append_note` MCP
- Modifier une propriete frontmatter → `update_property` MCP
- Refonte complete → `create_note` (ecrase) — uniquement si justifie

---

## 8. Anti-patterns vault

- ❌ Editer dans `raw/` (viole immutabilite Karpathy)
- ❌ Grep/Read brut sur le vault (utiliser MCP)
- ❌ Aliases bricoles ad-hoc (4-6 minimum, semantiques)
- ❌ `resume` generique ("note sur X")
- ❌ Wikilinks via markdown link `[text](path.md)` (utiliser `[[wikilink]]`)
- ❌ Note sans tags (au moins 2 : type + domaine)
- ❌ Note isolee (au moins 2 wikilinks)
- ❌ Note > 500L sans references/ extraite (cf [[comment-creer-skill]])
- ❌ Editer `log.md` retroactivement (append-only strict)
- ❌ Mettre du Knowledge/projet dans MCP-only-readable formats (toujours markdown)

---

## 9. Cross-LLM compatibility (alternative AGENTS.md)

Ce schema est compatible avec le pattern AGENTS.md propose par [[hashimoto]] (Ghostty) pour repos multi-LLM. Si le vault doit etre lu par Cursor / Codex / Gemini CLI / Goose en plus de Claude Code, ce SCHEMA.md sert de contrat commun.

---

## 10. Maintenance schema

Ce SCHEMA.md est modifie **rarement** (changements doctrinaux majeurs uniquement). Pour changements frequents → `CHANGELOG.md` ou `log.md`.

Derniere modification doctrinale : **22 mai 2026** — adoption pattern Karpathy strict + creation `raw/` + `index.md` + `log.md` + `SCHEMA.md`. **14 juin 2026** — réorg fournisseurs IA en dossiers premier niveau (dissout `02-Concurrents` + `03-Modeles`, squelette `models/`+`products/` par acteur).

---

## Voir aussi

- [[index]] — index content-oriented (orientation LLM)
- [[log]] — log append-only operations
- [[CHANGELOG]] — narration prosaique
- [[pattern-vault-llm-karpathy]] — pattern complet 3-layers + 3 ops
- [[forge-brain-proactive]] — rule MCP forge-brain proactif
- [[obsidian-markdown]] — skill format Obsidian
