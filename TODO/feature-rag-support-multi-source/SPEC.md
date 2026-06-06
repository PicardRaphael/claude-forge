# SPEC — Le meilleur chat support RAG Neoteem (architecture « tout converge vers Confluence »)

> **Repos : `neo_ia` + `neoteem-brain`** · Skills dans leurs repos respectifs.
> Ce dossier vit dans `claude-forge/TODO/` (BRIEF distant). À copier dans le repo cible avant `/go`.
> Taille : **XL** · Réécrit le 2026-06-05 (remplace la v1 « 3 ingestors pgvector », écartée) · PO : Raphael

## 0. Vision

Une **seule source embeddée = Confluence**. Tout le reste y converge. Zéro doublon **par construction** (dédup en amont, à la curation — pas au retrieval).

```
Jira tickets FERMÉS ──①──► neoteem-brain (notes curées) ──②──► Confluence espace NeoIA ──③──► pgvector ──► agent support RAG
   (API REST /search)     (07-Support, 06-Regles-Metier)    (dossier "À valider" → validé)   (collection confluence_docs)   (INCHANGÉ : hybrid RRF + rerank + LLM-judge + cache)
```

**Principe directeur** : la qualité de réponse finale est **plafonnée par la qualité de la doc source**. L'agent RAG est déjà mature — on n'y touche pas. Les leviers de qualité sont, par ordre d'impact :
1. **Qualité d'écriture des pages Confluence** (skill ②) — titre = la question, sections auto-suffisantes, structure problème/solution alignée sur le chunker 1200/180.
2. **Validation humaine étanche** — zéro page non validée embeddée.
3. **Exploitation des images** (description Gemini) — récupère l'information visuelle aujourd'hui perdue.
4. **Anti-ré-embedding** (hash) — « pas d'embedding inutile », fiabilise le pipeline.

## 1. Contexte technique confirmé (exploration)

- **Agent support RAG existant et mature** (`apps/neochat/.../support/`) : hybrid RRF + rerank `bge-reranker-v2-m3` + LLM-as-judge + cache. **NON refondu.**
- **Pipeline Confluence** (`scripts/confluence_sync.py` + `shared_utils/confluence/`) : chunking 1200/180, contextual retrieval Anthropic (1 LLM Gemini/page), UPSERT UUID5, embeddings `gemini-embedding-001` 768d Vertex, collection `confluence_docs`. Sync incrémental CQL `lastModified`. Credentials Atlassian en table `parametrage` type=`documentation_lojii`. **Espace actuellement syncé = `NEO`** (cible voulue = `NeoIA`).
- **Contrainte forte** : neo_ia est **Gemini/Vertex EXCLUSIF** (interdit Anthropic/OpenAI SDK, `CLAUDE.md:17`). JAMAIS de DDL en code.
- **MCP Jira Neoteem = admin-only** (move/orga/customer, pas de search JQL). `acli` non installé. → lecture des tickets via **API Jira REST** directe.
- **Vault brain** : `${NEOT_V2_ROOT}/neoteem-brain`, `07-Support/{faq,procedures,problemes-connus}` + `06-Regles-Metier` déjà curés (MOC-Support, templates, tags). Écriture via plugins `neoteem-brain-admin`.

## 2. ⚠️ Deux blockers critiques (la réussite du projet se joue ici)

### BLOCKER #1 — La barrière « À valider » fuit par défaut
Le sync incrémental (`get_modified_pages`, `client.py`) **ne pose AUCUN filtre statut** (contrairement à `get_all_pages` qui force `status:current`). Donc dès que skill ② crée une page « À valider », **le prochain sync l'embedderait** → la validation devient décorative.
**Fix (RISQUE ÉLEVÉ si oublié)** : skill ② pose le label **`a-valider`** à la création ; le pipeline ③ exclut ce label du CQL **sur les DEUX chemins** (full + incrémental). Validation humaine = sortir la page du dossier **ET** retirer le label. *(Options B = ancêtre/dossier, C = espace staging — voir §7. Recommandé : A label.)*

### BLOCKER #2 — Pas de capacité d'écriture Confluence
`shared_utils/confluence/client.py` est **lecture seule** (que des GET). La publication est du **net-new code** → créer `shared_utils/confluence/publisher.py` (`ConfluencePublisher` : `POST/PUT pages`, `POST label`, recherche d'existence create-vs-update), séparé de `client.py` pour ne pas risquer le pipeline ③.

## 3. Skill ① « Jira → brain » (repo **neoteem-brain**)
`neoteem-brain/.claude/skills/jira-to-brain/SKILL.md` (net-new). Gabarit : skill existante `ticket-analyzer`.
- **Déclenchement** : tâche planifiée Claude Code desktop, fin de semaine, batch tickets fermés.
- **Lecture** : API REST Jira `POST /rest/api/3/search`, credentials `parametrage` `documentation_lojii` (même domaine). PAS le MCP (admin-only).
- **JQL incrémental** : `project IN (<à confirmer>) AND statusCategory = Done AND resolutiondate >= "<dernier_traité>" ORDER BY resolutiondate ASC`.
- **Mémoire du déjà-traité** : sidecar `neoteem-brain/.claude/skills/jira-to-brain/state/processed.json` (`last_resolutiondate` + `processed_keys`). PAS la table `parametrage` (DB neo_ia inaccessible depuis le repo brain).
- **Classification par domaine** (par Claude lui-même, pas que support) : bug→`07-Support/problemes-connus/`, question→`faq/`, procédure→`procedures/`, règle métier→`06-Regles-Metier/`, autres branches selon contenu.
- **Format** : templates brain existants (frontmatter v2, aliases ≥3, tags `#domaine/X`, `#statut/draft` à la création, source = réf ticket).
- **Dédup** : `search_brain` AVANT création → enrichir (`append_note`/`insert_section`) si la note existe ; skill `deduplicate-brain`. Écriture via plugin admin. Gate humaine obligatoire.

## 4. Skill ② « brain → Confluence » (repo **neo_ia**)
`neo_ia/.claude/skills/brain-to-confluence/SKILL.md` (net-new) + `shared_utils/confluence/publisher.py` (BLOCKER #2).
- **Sélection** : notes `07-Support/**` + `06-Regles-Metier/**` taguées `#statut/valide`.
- **Transformation « parfaite RAG »** (cœur qualité, aligné chunker 1200/180 séparateurs `\n\n`) :
  - **Titre de page = la question/le problème** reformulé (le titre est injecté dans CHAQUE chunk).
  - Sections `H2`/`H3` **auto-suffisantes** (un chunk = une réponse), structure problème → cause → solution.
  - Labels Confluence = domaine + type (repris du frontmatter brain).
  - Traduire les wikilinks `[[...]]` (pas de syntaxe Obsidian dans Confluence).
  - **Images** : description Gemini insérée en texte (§5.2) pour que le sens visuel soit embeddé.
- **Workflow** : pages créées sous la page parente **« À valider »** de l'espace **NeoIA** + label `a-valider`. Validation humaine = relecture/correction → sortie du dossier **+ retrait du label** → ③ l'embedde au sync suivant.
- **Publication** : via `ConfluencePublisher` (create/update idempotent par titre).

## 5. Amélioration pipeline ③ (repo **neo_ia**)

### 5.1 content_hash anti-ré-embedding (« pas d'embedding inutile »)
Aujourd'hui `_process_page` re-chunke + re-appelle le LLM-context (1 Gemini/page) + ré-embedde TOUT, sans hash. **Fix (modèle = MCP brain `watcher.py:57-69` + `database.py:93-95`)** : `content_hash = sha256(content)` avant chunking ; comparer au hash stocké en `cmetadata` ; **inchangé → skip total** (pas de chunk, pas de LLM-context, pas d'embedding). Gate mtime/version en pré-filtre, hash = vérité.

### 5.2 Description d'images via Gemini multimodal (contrainte Gemini respectée)
Le processor insère des marqueurs d'images mais ne les décrit pas → info visuelle perdue. **Fix** : à l'ingestion, télécharger l'image (`client.download_attachment` existe) → décrire via `get_genai_client()` (`gemini-2.5-flash` multimodal, déjà dispo, PAS Mistral OCR) → injecter la description en texte dans le chunk (alt enrichi). Coût maîtrisé : décrire seulement si la page a changé (combiné §5.1) + cache description en `cmetadata`.

### 5.3 Bascule space NEO → NeoIA
Le sync vise `NEO` aujourd'hui ; cible = `NeoIA`. Ajuster le `space_key`. **À confirmer (PO)** : cutover de la collection `confluence_docs` (purge + full sync NeoIA) vs cohabitation.

### 5.4 Conserver tel quel
Chunking 1200/180, contextual retrieval, UPSERT UUID5, keywords, breadcrumb. Déjà aligné best-practices.

## 6. Vagues

| Vague | Repo | Contenu | Dépend | Risque |
|---|---|---|---|---|
| **V0 — Barrière** | neo_ia | filtre `status`+`label!=a-valider` CQL (2 chemins) ; bascule space→NeoIA | — | ÉLEVÉ |
| **V1 — Anti-ré-embed** | neo_ia | content_hash skip embed+LLM-context | V0 | MOYEN |
| **V2 — Images Gemini** | neo_ia | description multimodale + cache hash | V1 | MOYEN |
| **V3 — Publisher** | neo_ia | `publisher.py` (create/update/label) | V0 | MOYEN |
| **V4 — Skill ② brain→Confluence** | neo_ia | SKILL.md transformation RAG + workflow dossier | V3, V2 | MOYEN |
| **V5 — Skill ① Jira→brain** | neoteem-brain | SKILL.md REST Jira + state + classif + dédup | indépendante ‖ | MOYEN |
| **V6 — Orchestration** | les 2 | tâches planifiées (① hebdo, ②, ③) | V1-V5 | FAIBLE |

V5 démarrable en parallèle. V0 = prérequis dur de la qualité.

## 7. À confirmer avant `/go` (inputs PO)
1. **Cutover space NEO → NeoIA** : purge `confluence_docs` + full sync, ou cohabitation ?
2. **Mécanisme barrière** : label `a-valider` (A, recommandé) vs ancêtre (B) vs espace staging (C) ?
3. **Périmètre projets Jira** pour le JQL (`project IN (...)`).
4. **Validation manuelle** acceptée en V1 (qui retire le label / sort du dossier) ? automatisation plus tard ?
5. **Coût Gemini images** OK (atténué par cache hash) ?
6. **Stockage état skill ①** : sidecar JSON validé ?

## 8. Hors scope
- Refonte de l'agent support (retrieval déjà mature).
- Migration modèle embedding / vector store / Mistral OCR (contrainte Gemini).
- Ingestor pgvector direct Jira/brain (approche v1 écartée : tout passe par Confluence).
