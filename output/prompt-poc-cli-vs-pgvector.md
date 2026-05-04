# Prompt — POC comparatif CLI Obsidian vs pgvector

## Techniques appliquees
- **Role Prompting** : ingenieur RAG + benchmark
- **Chain-of-Thought guide** : 6 phases numerotees
- **Outcome Delegation** : criteres de succes mesurables
- **Contraintes negatives** : ce qu'il ne faut PAS faire
- **Self-Verification** : criteres de validation integres

---

## Le prompt

```xml
<system>
Tu es un ingenieur senior qui implemente un POC de comparaison entre deux systemes d'acces a une base de connaissances Obsidian. Tu vas construire le pipeline pgvector, executer 20 requetes test sur les deux systemes, et produire un rapport objectif avec des scores.

Tu travailles dans le repo neoteem-brain. Tu ne prends pas parti — tu mesures.

Tu fais tout toi-meme dans cette session Claude Code : tu codes, tu executes, tu lis les resultats, tu evalues les reponses, tu generes le rapport. Pas d'API externe pour l'evaluation — c'est toi le juge.
</system>

<context>
## Le projet

On compare deux facons d'acceder au vault neoteem-brain (682 notes Obsidian, domaine immobilier : syndic, gerance, comptabilite) via Claude :

**Systeme A — CLI Obsidian (existant)**
- Appel CLI Obsidian directement (search:context, read, backlinks)
- Claude recoit les fichiers .md complets avec wikilinks, frontmatter, structure

**Systeme B — pgvector (a construire dans ce POC)**
- Les notes sont chunkees par section ##, embeddees, stockees dans PostgreSQL + pgvector
- Appel d'un script Python qui fait search/read/expand sur la BDD
- Claude recoit des chunks avec metadata

## Le vault neoteem-brain

Chemin : `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/`

Structure :
```
00-Hub/           — Home + MOCs (index thematiques)
01-Domaines/      — Concepts metier, jargon, acteurs
02-Regles/        — Regles de calcul, workflow, cas particuliers
03-Apps/          — Documentation par application (neofront/, neot-v2/)
04-BDD/           — Fonctions PG, tables, schemas
05-Projets/       — Projets en cours
06-Decisions/     — ADRs, choix techniques
07-Support/       — FAQ, procedures, problemes connus
Knowledge/        — Explorations, syntheses
```

Dossiers a NE PAS indexer : Templates/, Daily/, .claude/, doc/, neo-brain/, neo-brain-support/, fichiers a la racine.

Format d'une note :
```yaml
---
titre: "Titre lisible"
resume: "1 ligne"
aliases:
  - "synonyme 1"
  - "synonyme 2"
domaine: syndic | gerance | compta | technique
type: regle | concept | app | bdd | faq | procedure | decision
derniere-maj: YYYY-MM-DD
tags:
  - "#type/xxx"
  - "#domaine/xxx"
---

## Section 1
Contenu avec [[wikilinks]] vers d'autres notes.

## Section 2
...
```

## Infrastructure disponible

- PostgreSQL sur Cloud SQL (connexion via `psql` ou `psycopg2`)
- Python 3.11+
- pip install : psycopg2-binary, pyyaml, openai (pour text-embedding-3-small)
- CLI Obsidian fonctionnelle (wrapper : `bash .claude/skills/forge-brain/scripts/obsidian-cli.sh`)
- Vault ouvert dans Obsidian

## Credentials

- Connection PostgreSQL : voir `.env` ou demander a l'utilisateur
- OpenAI API key : voir `.env` ou demander a l'utilisateur (pour les embeddings uniquement)
- Modele d'embedding : `text-embedding-3-small` (1536 dims, $0.02/1M tokens — le POC coutera ~$0.05 max)
- PAS besoin de cle Anthropic — c'est toi (Claude Code) qui evalues directement
</context>

<instructions>
Implemente le POC complet en 6 phases. Chaque phase produit un livrable testable avant de passer a la suivante. Tout le code va dans `neoteem-brain/poc-pgvector/`.

## Phase 1 — Selection des 50 notes

Selectionner 50 notes representant la diversite du vault :
- 10 notes de `01-Domaines/` (concepts metier)
- 8 notes de `02-Regles/` (regles de calcul, cas particuliers)
- 8 notes de `03-Apps/` (documentation applicative)
- 8 notes de `04-BDD/` (fonctions PG, tables)
- 5 notes de `07-Support/` (FAQ, procedures)
- 5 notes de `06-Decisions/` (ADRs)
- 3 notes de `00-Hub/` (MOCs)
- 3 notes de `Knowledge/`

Criteres de selection :
- Varier les domaines (syndic, gerance, compta, technique)
- Inclure des notes courtes (< 50 lignes) ET longues (> 200 lignes)
- Inclure des notes avec beaucoup de wikilinks (5+) ET peu (0-2)
- Inclure des notes avec aliases riches (5+) ET minimaux (3)

Livrable : `poc-pgvector/notes_selection.json` — liste des 50 chemins + metadata (domaine, type, nb lignes, nb wikilinks, nb aliases).

## Phase 2 — Schema SQL + ingestion

Creer le schema dans un schema dedie `poc_brain` :

```sql
CREATE SCHEMA IF NOT EXISTS poc_brain;

-- Extensions requises
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- TABLES
-- ============================================================

-- 1 ligne par fichier .md
CREATE TABLE poc_brain.documents (
    id SERIAL PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    titre TEXT NOT NULL,
    resume TEXT,
    domaine TEXT NOT NULL,
    type TEXT NOT NULL,
    aliases TEXT[] NOT NULL DEFAULT '{}',
    tags TEXT[] NOT NULL DEFAULT '{}',
    derniere_maj DATE,
    content_hash TEXT NOT NULL,       -- SHA256 pour mode incremental
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 1 ligne par chunk (section ## ou metadata)
CREATE TABLE poc_brain.chunks (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES poc_brain.documents(id) ON DELETE CASCADE,
    position INT NOT NULL,            -- 0 = chunk metadata enrichi, 1+ = sections
    section_title TEXT,               -- NULL pour position 0
    content TEXT NOT NULL,            -- contenu brut avec [[wikilinks]] preserves
    content_for_search TEXT NOT NULL, -- contenu avec wikilinks en texte brut (pour FTS)
    search_vector TSVECTOR GENERATED ALWAYS AS (to_tsvector('french', content_for_search)) STORED,
    embedding vector(1536) NOT NULL,  -- text-embedding-3-small
    UNIQUE(document_id, position)
);

-- wikilinks extraits (graphe de connaissances)
CREATE TABLE poc_brain.links (
    id SERIAL PRIMARY KEY,
    source_chunk_id INT NOT NULL REFERENCES poc_brain.chunks(id) ON DELETE CASCADE,
    source_document_id INT NOT NULL REFERENCES poc_brain.documents(id) ON DELETE CASCADE,
    target_note TEXT NOT NULL,        -- nom de la note cible (sans .md, sans chemin)
    UNIQUE(source_chunk_id, target_note)
);

-- ============================================================
-- INDEX — chaque index a un role precis
-- ============================================================

-- Recherche vectorielle : HNSW pour recall + vitesse
-- m=16 : bon equilibre memoire/qualite pour < 100K vecteurs
-- ef_construction=64 : qualite de construction (defaut=64, augmenter pour plus de precision)
CREATE INDEX idx_chunks_embedding ON poc_brain.chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Recherche full-text francais : colonne GENERATED evite le recalcul a chaque requete
CREATE INDEX idx_chunks_search_vector ON poc_brain.chunks
    USING gin (search_vector);

-- Recherche fuzzy (fautes de frappe) : trigram sur le contenu
CREATE INDEX idx_chunks_trgm ON poc_brain.chunks
    USING gin (content_for_search gin_trgm_ops);

-- Filtrage par domaine/type (utilise dans les clauses WHERE)
CREATE INDEX idx_documents_domaine ON poc_brain.documents (domaine);
CREATE INDEX idx_documents_type ON poc_brain.documents (type);

-- Recherche dans les aliases (pour retrouver un document par synonyme)
CREATE INDEX idx_documents_aliases ON poc_brain.documents USING gin (aliases);

-- Navigation : chunk → document (JOIN frequent)
CREATE INDEX idx_chunks_document_id ON poc_brain.chunks (document_id);

-- Graphe : expand() suit les wikilinks
CREATE INDEX idx_links_source_chunk ON poc_brain.links (source_chunk_id);
CREATE INDEX idx_links_source_doc ON poc_brain.links (source_document_id);
CREATE INDEX idx_links_target ON poc_brain.links (target_note);

-- ============================================================
-- FONCTIONS SQL — recherche hybride optimisee
-- ============================================================

-- Recherche hybride : combine vector + FTS + fuzzy en une seule requete
CREATE OR REPLACE FUNCTION poc_brain.search(
    query_text TEXT,
    query_embedding vector(1536),
    filter_domaine TEXT DEFAULT NULL,
    filter_type TEXT DEFAULT NULL,
    result_limit INT DEFAULT 10
)
RETURNS TABLE (
    chunk_id INT,
    document_id INT,
    document_path TEXT,
    titre TEXT,
    domaine TEXT,
    section_title TEXT,
    content TEXT,
    vector_score FLOAT,
    text_score FLOAT,
    combined_score FLOAT
) AS $$
BEGIN
    -- SET ef_search pour le HNSW (plus haut = plus precis, plus lent)
    PERFORM set_config('hnsw.ef_search', '40', true);

    RETURN QUERY
    SELECT
        c.id AS chunk_id,
        d.id AS document_id,
        d.path AS document_path,
        d.titre,
        d.domaine,
        c.section_title,
        c.content,
        -- Score vectoriel normalise [0,1] (cosine distance → similarity)
        (1 - (c.embedding <=> query_embedding))::FLOAT AS vector_score,
        -- Score full-text normalise [0,1]
        COALESCE(ts_rank_cd(c.search_vector, plainto_tsquery('french', query_text)), 0)::FLOAT AS text_score,
        -- Score combine : 70% vector + 30% FTS
        (0.7 * (1 - (c.embedding <=> query_embedding)) +
         0.3 * COALESCE(ts_rank_cd(c.search_vector, plainto_tsquery('french', query_text)), 0))::FLOAT AS combined_score
    FROM poc_brain.chunks c
    JOIN poc_brain.documents d ON d.id = c.document_id
    WHERE
        (filter_domaine IS NULL OR d.domaine = filter_domaine)
        AND (filter_type IS NULL OR d.type = filter_type)
    ORDER BY combined_score DESC
    LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;

-- Lecture document complet (reconstitue depuis les chunks)
CREATE OR REPLACE FUNCTION poc_brain.read_document(doc_path TEXT)
RETURNS TABLE (
    titre TEXT,
    resume TEXT,
    domaine TEXT,
    type TEXT,
    aliases TEXT[],
    tags TEXT[],
    position INT,
    section_title TEXT,
    content TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.titre, d.resume, d.domaine, d.type, d.aliases, d.tags,
        c.position, c.section_title, c.content
    FROM poc_brain.documents d
    JOIN poc_brain.chunks c ON c.document_id = d.id
    WHERE d.path = doc_path
    ORDER BY c.position;
END;
$$ LANGUAGE plpgsql;

-- Expand : suit les wikilinks d'un chunk
CREATE OR REPLACE FUNCTION poc_brain.expand(
    p_chunk_id INT,
    p_depth INT DEFAULT 1
)
RETURNS TABLE (
    linked_document_path TEXT,
    linked_titre TEXT,
    linked_domaine TEXT,
    linked_resume TEXT,
    link_target TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        d.path AS linked_document_path,
        d.titre AS linked_titre,
        d.domaine AS linked_domaine,
        d.resume AS linked_resume,
        l.target_note AS link_target
    FROM poc_brain.links l
    JOIN poc_brain.documents d ON (
        d.path ILIKE '%/' || l.target_note || '.md'
        OR d.titre ILIKE l.target_note
        OR l.target_note = ANY(d.aliases)
    )
    WHERE l.source_chunk_id = p_chunk_id;
END;
$$ LANGUAGE plpgsql;
```

Le schema est optimise pour ce cas d'usage :
- `search_vector` est une colonne GENERATED STORED — le tsvector est calcule une seule fois a l'insertion, pas a chaque requete
- HNSW avec `m=16, ef_construction=64` — bon equilibre pour < 100K vecteurs
- `hnsw.ef_search=40` dans la fonction search — precision de requete (augmenter si besoin)
- pg_trgm pour la recherche fuzzy (fautes de frappe)
- Index sur TOUS les champs utilises en filtre ou en JOIN (domaine, type, document_id, target_note)
- Fonctions SQL `search()`, `read_document()`, `expand()` — le script Python n'a qu'a appeler ces fonctions
- `expand()` resout les wikilinks par path, titre, OU alias — tolerant aux variations de nommage

Script d'ingestion `poc-pgvector/ingest.py` :
- Parse le frontmatter YAML de chaque note
- Chunk 0 = metadata enrichie : titre + resume + tous les aliases + tous les tags + liste des wikilinks du document
- Chunks 1+ = sections ## (fusionner si < 100 mots, decouper si > 500 mots aux ###)
- Prefixe d'embedding : `[{domaine}] {titre} > {section}` (pas stocke, utilise uniquement pour le calcul de l'embedding)
- Extraction wikilinks `[[...]]` → table links
- content_for_search = contenu avec `[[texte]]` remplace par `texte`
- Hash SHA256 du contenu pour mode incremental

Livrable : les 50 notes ingerees, verifier avec `SELECT count(*) FROM poc_brain.documents` (= 50) et `SELECT count(*) FROM poc_brain.chunks` (= ~150-300).

## Phase 3 — Fonctions de recherche Python

Script `poc-pgvector/search.py` avec 3 fonctions :

`search(query, filters=None, limit=10)` :
- Recherche hybride : cosine similarity sur embeddings + ts_rank sur tsvector francais
- Score combine : `0.7 * vector_score + 0.3 * text_score` (normalises entre 0 et 1)
- Filtres optionnels : domaine, type
- Retourne : chunk_id, document_path, section_title, content (tronque 500 chars), score

`read(document_path)` :
- Retourne le document complet reconstitue (tous les chunks dans l'ordre, avec frontmatter)

`expand(chunk_id, depth=1)` :
- Suit les wikilinks du chunk → retourne les chunks metadata (position 0) des notes cibles
- depth=1 seulement pour le POC

Livrable : script testable en CLI (`python search.py "calcul charges"`)

## Phase 4 — Les 20 requetes test

Creer `poc-pgvector/queries.json` avec 20 requetes reparties en 3 categories :

**10 requetes exactes** (termes precis, vocabulaire metier connu) :
Utiliser des termes qui existent dans les notes selectionnees — titres, noms de fonctions PG, noms de tables, termes du glossaire. Ces requetes doivent etre trouvables par les deux systemes.

**5 requetes reformulees** (synonymes, langage naturel) :
Utiliser des reformulations qui ne correspondent PAS aux titres ou aliases exacts. Exemple : "comment on fait payer les copropietaires" au lieu de "appel de fonds". C'est la ou pgvector devrait briller.

**5 requetes vagues** (questions ouvertes, cross-domaine) :
Questions qui necessitent de croiser plusieurs notes. Exemple : "quel est l'impact d'un depart de locataire sur la comptabilite". C'est la ou la navigation par wikilinks devrait briller.

Pour chaque requete, noter :
- La categorie (exacte / reformulee / vague)
- La ou les notes attendues en reponse (ground truth)
- Le domaine concerne

Livrable : `queries.json` avec les 20 requetes + ground truth.

## Phase 5 — Execution et evaluation

Pour chaque requete, tu fais toi-meme (Claude Code) les deux recherches et tu evalues :

### Etape 1 : Recherche Systeme A (CLI Obsidian)
1. Executer `obsidian-cli vault="neoteem-brain" search:context query="..." limit=5`
2. Lire les snippets retournes
3. Pour les top 3 resultats, executer `obsidian-cli vault="neoteem-brain" read file="..."`
4. Mesurer la latence totale (time avant/apres les commandes)
5. Compter les tokens (caracteres retournes / 4)
6. Noter quelles notes ont ete trouvees

### Etape 2 : Recherche Systeme B (pgvector)
1. Executer `python search.py "..." --limit 5`
2. Lire les chunks retournes
3. Pour les top 3 resultats, executer `python search.py --read "chemin/de/la/note.md"` pour recuperer le document complet (mitigation)
4. Mesurer la latence totale
5. Compter les tokens
6. Noter quelles notes ont ete trouvees

### Etape 3 : Evaluation (toi-meme)

Pour chaque requete, avec le contexte des deux systemes frais en memoire, evalue sur 4 criteres (note de 1 a 5) :

1. **Retrieval** : la bonne note est-elle dans les resultats ? (1 = absente, 5 = premier resultat)
2. **Completude** : le contexte retourne couvre-t-il tous les aspects de la question ? (1 = rien, 5 = complet)
3. **Contexte relationnel** : le systeme fournit-il des liens vers des notes liees ? (1 = isole, 5 = graphe complet)
4. **Tokens** : efficacite — qualite du contexte par rapport au volume de tokens consommes (1 = beaucoup de bruit, 5 = signal pur)

Consigne critique : evalue les CONTEXTES retournes, pas les reponses que tu pourrais generer. La question est "quel systeme donne le meilleur materiau pour repondre ?", pas "quelle reponse est meilleure ?". Tu es capable de generer une bonne reponse avec un mauvais contexte — c'est le contexte qu'on evalue.

Stocker les resultats au fur et a mesure dans `poc-pgvector/results/query_XX.json` (un fichier par requete pour lisibilite) :

```json
{
  "query": "...",
  "category": "exacte|reformulee|vague",
  "ground_truth": ["note1.md", "note2.md"],
  "system_a": {
    "notes_found": ["note1.md"],
    "latency_ms": 234,
    "tokens_context": 1200,
    "response": "... LA REPONSE COMPLETE que Claude donnerait a l'utilisateur en se basant sur le contexte CLI ...",
    "retrieval": 5,
    "completude": 4,
    "contexte_relationnel": 5,
    "tokens_efficiency": 4
  },
  "system_b": {
    "notes_found": ["note1.md", "note3.md"],
    "latency_ms": 187,
    "tokens_context": 900,
    "response": "... LA REPONSE COMPLETE que Claude donnerait a l'utilisateur en se basant sur le contexte pgvector ...",
    "retrieval": 5,
    "completude": 3,
    "contexte_relationnel": 2,
    "tokens_efficiency": 4
  },
  "commentaire": "CLI fournit les wikilinks, pgvector trouve la bonne note mais perd la structure"
}
```

IMPORTANT pour le champ `response` : c'est la reponse FINALE que l'utilisateur lirait — pas le contexte brut, pas les documents. Pour chaque systeme, tu lis le contexte retourne puis tu rediges la reponse comme si un utilisateur t'avait pose la question et que tu n'avais QUE ce contexte. Le lecteur du rapport doit pouvoir comparer les deux reponses cote a cote et juger lui-meme laquelle est meilleure.

AUCUNE LIMITE DE TOKENS. La reponse doit etre aussi longue et complete que necessaire — exactement comme Claude repondrait en conditions reelles. Si la reponse fait 2000 tokens c'est 2000 tokens. Ne pas tronquer, ne pas resumer, ne pas raccourcir. C'est justement la quantite ET la qualite de la reponse qui sont evaluees. Un systeme qui donne plus de contexte utile = une reponse plus riche = c'est un avantage mesurable.

Proceder requete par requete. Pas de batch — tu dois lire et evaluer chaque resultat individuellement.

## Phase 6 — Rapport final

Generer `poc-pgvector/RAPPORT.md` avec :

1. **Resume executif** (5 lignes max) : qui gagne globalement, sur quelles categories, recommandation

2. **Scores moyens par categorie** :
   - Requetes exactes (10) : score moyen A vs B sur chaque critere
   - Requetes reformulees (5) : score moyen A vs B
   - Requetes vagues (5) : score moyen A vs B

3. **Scores moyens par critere** :
   - Retrieval : A vs B
   - Completude : A vs B
   - Contexte relationnel : A vs B
   - Tokens efficiency : A vs B

4. **Metriques techniques** :
   - Latence moyenne par systeme
   - Tokens moyens par systeme
   - Taux de retrieval (bonne note dans le top 3) par systeme

5. **Top 3 requetes ou la CLI gagne le plus** (avec explication)

6. **Top 3 requetes ou pgvector gagne le plus** (avec explication)

7. **Conclusion** : recommandation chiffree — est-ce que pgvector justifie 5-8 jours de dev + 5-10 EUR/mois par rapport a la CLI existante ?
</instructions>

<constraints>
## Ce qu'il ne faut PAS faire

1. **PAS de biais.** Tu es le juge — sois objectif. Si pgvector est meilleur sur une requete, dis-le. Si la CLI est meilleure, dis-le. Pas de favoritisme.

2. **PAS de cherry-picking des notes.** Les 50 notes doivent etre representatives, pas selectionnees pour avantager un systeme. Inclure des notes faciles ET difficiles.

3. **PAS de chunking naif.** Respecter les regles : sections ##, fusion < 100 mots, decoupage > 500 mots, chunk 0 metadata avec aliases.

4. **PAS de sur-engineering.** C'est un POC, pas un produit. Code simple, lisible, un seul fichier par phase. Pas de framework, pas d'abstraction inutile.

5. **PAS d'oubli de la mitigation pgvector.** Apres le search pgvector, TOUJOURS faire un read du document complet pour les top 3. C'est la mitigation qui rend la comparaison equitable — on compare le meilleur de chaque systeme.

6. **PAS d'evaluation des reponses generees.** Evaluer les CONTEXTES retournes par chaque systeme, pas les reponses que tu pourrais generer. La question est : quel systeme donne le meilleur materiau a Claude pour repondre ?

7. **Demander les credentials** (connection PG, API key OpenAI) a l'utilisateur avant de commencer. Ne pas deviner.
</constraints>

<verification>
Le POC est reussi si :

1. 50 notes ingerees dans pgvector, verifiables par `SELECT count(*) FROM poc_brain.documents`
2. Les 20 requetes executees sur les deux systemes sans erreur
3. Les 20 evaluations produites avec scores 1-5 et commentaire
4. Le rapport RAPPORT.md est genere, lisible, et contient des chiffres
5. Le cout total du POC est < $0.10 (embeddings text-embedding-3-small uniquement)
6. Le POC est nettoyable : `DROP SCHEMA poc_brain CASCADE` supprime tout
</verification>
```

---

## Notes pour l'execution

Avant de lancer, preparer :
- `.env` avec `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, `PG_DATABASE`, `OPENAI_API_KEY`
- Obsidian ouvert avec le vault neoteem-brain
- `pip install psycopg2-binary pyyaml openai`

Duree estimee : 2-3 heures avec Claude Code. Cout : ~$0.05 (embeddings).

Pour nettoyer apres le POC : `DROP SCHEMA poc_brain CASCADE;`
