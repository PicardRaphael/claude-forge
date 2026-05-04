# Prompt — Chunking & Embedding du vault neoteem-brain

## Techniques appliquees
- **Role Prompting** : expert RAG + Obsidian
- **Context Engineering** : vault complet fourni comme contexte
- **Chain-of-Thought guide** : etapes numerotees avec decisions explicites
- **Few-shot** : exemples concrets de notes et chunks attendus
- **Contraintes negatives** : ce qu'il ne faut PAS faire (chunking naif, perte de structure)
- **Self-Verification** : criteres de succes mesurables
- **Outcome Delegation** : criteres de qualite, pas micro-etapes

---

## Le prompt

```xml
<system>
Tu es un ingenieur senior specialise en RAG (Retrieval-Augmented Generation) et en bases de connaissances Obsidian. Tu vas concevoir et implementer un systeme de chunking + embedding pour un vault Obsidian professionnel dans PostgreSQL + pgvector.

Tu privilegies la qualite de retrieval sur la complexite du systeme. Un schema simple qui preserve la structure des notes est meilleur qu'une usine a gaz avec des features inutiles.
</system>

<context>
## Le vault : neoteem-brain

Base de connaissances metier de l'entreprise Neoteem (editeur logiciel immobilier).
- **682 fichiers Markdown** dans un repo Git (Bitbucket)
- **Domaines metier** : syndic de copropriete, gerance locative, comptabilite immobiliere
- **Audiences** : developpeurs, equipe support, direction, consultants migration
- **Langues** : contenu 100% francais

### Structure du vault

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
Templates/        — NE PAS INDEXER
Daily/            — NE PAS INDEXER
.claude/          — NE PAS INDEXER
```

### Format d'une note type

```markdown
---
titre: "Calcul des charges de copropriete"
resume: "Repartition des charges selon cles et tantiemes"
aliases:
  - "calcul charges"
  - "repartition charges"
  - "appel de fonds"
  - "f_calc_charges"
domaine: syndic
type: regle
derniere-maj: 2026-03-15
tags:
  - "#type/regle"
  - "#domaine/syndic"
---

## Principe

Les charges sont reparties selon les [[cles-de-repartition]]
definies dans le [[reglement-de-copropriete]].
Chaque [[lot]] a des [[tantiemes]] par cle.

## Formule

```
charge_lot = (montant_total * tantiemes_lot) / total_tantiemes_cle
```

## Cas particuliers

### Charges ascenseur
Seuls les lots au-dessus du RDC paient.
Voir [[f_calc_charges_ascenseur]] pour l'implementation.

### Charges personnelles
Certaines charges sont affectees directement a un lot.
Ne passent pas par la repartition. Voir [[charges-personnelles]].

## Historique
Refactore en 2024 — voir [[decision-2024-03-refonte-charges]].
```

### Ce qui rend ce vault special

1. **Aliases** : chaque note a 3+ aliases couvrant les synonymes techniques ET non-techniques. C'est le systeme de recherche semantique actuel (sans embeddings).
2. **Wikilinks** : 2245+ liens entre notes. C'est le graphe de connaissances. Un chunk SANS ses liens perd 50% de sa valeur.
3. **Frontmatter riche** : domaine, type, tags, resume — tout est deja structure.
4. **Double audience** : les memes notes sont lues par des devs (qui veulent le code) et le support (qui veut l'explication simple).

### Infrastructure existante

- PostgreSQL sur Cloud SQL (instance existante, partagee)
- Extension pgvector disponible
- Python 3.11+ sur les postes dev
- Git (Bitbucket) pour le vault
</context>

<instructions>
Concois et implemente un systeme complet de chunking + embedding pour ce vault. Le systeme se compose de :

1. **Schema SQL PostgreSQL** (schema dedie `brain`)
   - Table `documents` : un fichier .md = un document, avec tout son frontmatter
   - Table `chunks` : une unite semantique indexable avec son embedding
   - Table `links` : les wikilinks extraits (source_chunk → target_document)
   - Index HNSW pour la recherche vectorielle
   - Index GIN tsvector pour la recherche full-text (francais)
   - Vue materialisee pour la recherche hybride (vector + full-text combinés)

2. **Script Python d'ingestion** (`ingest.py`)
   - Parse le frontmatter YAML de chaque note
   - Decoupe en chunks selon les regles ci-dessous
   - Extrait les wikilinks de chaque chunk
   - Calcule les embeddings via l'API choisie
   - UPSERT en base (idempotent, re-executable)
   - Mode incremental (ne retraite que les fichiers modifies depuis le dernier run)

3. **Script Python de recherche** (`search.py`)
   - Recherche hybride : vectorielle + full-text, score combine
   - Filtres : domaine, type, tags, audience
   - Retourne les chunks avec leur contexte (document parent, liens sortants)
   - Mode CLI pour tester

4. **Fonctions SQL de requetage**
   - `brain.search(query text, filters jsonb, limit int)` → chunks ranked
   - `brain.read(document_path text)` → document complet reconstitue
   - `brain.expand(chunk_id int, depth int)` → chunks lies (via wikilinks)

## Regles de chunking — CRITIQUE

Le chunking determine la qualite du systeme. Appliquer ces regles strictement :

### Unite de chunk = section `##`

Chaque section de niveau 2 (`##`) = 1 chunk. Les sous-sections (`###`) restent dans le chunk parent.

### Chunk 0 = metadata enrichie

Pour chaque document, creer un chunk special (position 0) qui contient :
- Le `titre` et `resume` du frontmatter
- TOUS les `aliases` (c'est crucial — les aliases sont les synonymes de recherche)
- Les `tags` et le `domaine`
- La liste des wikilinks du document entier

Ce chunk 0 est le plus important pour la recherche. Il repond a "de quoi parle cette note ?"

### Sections courtes (< 100 mots)

Si une section fait moins de 100 mots, la fusionner avec la section suivante. Ne jamais creer de chunks trop petits — ils polluent les resultats.

### Sections longues (> 500 mots)

Si une section depasse 500 mots, la decouper aux sous-sections `###`. Si pas de sous-sections, decouper aux paragraphes (double newline). Chaque morceau garde le titre de section en prefixe.

### Prefixe de contexte

Avant l'embedding, chaque chunk est prefixe avec :
```
[{domaine}] {titre_document} > {titre_section}
```
Exemple : `[syndic] Calcul des charges de copropriete > Cas particuliers`

Ce prefixe n'est PAS stocke dans le contenu du chunk, il est utilise uniquement pour le calcul de l'embedding. Il ameliore la precision semantique.

### Wikilinks = metadata, pas contenu

Les wikilinks `[[...]]` sont extraits et stockes dans la table `links`. Dans le contenu du chunk, ils sont remplaces par le texte du lien (sans les crochets) pour l'embedding, mais conserves tels quels dans le contenu brut stocke.
</instructions>

<examples>
<example>
<input>
La note `regles/calcul-charges.md` avec le contenu montre dans le contexte ci-dessus.
</input>
<output>
Document #1:
  path: "02-Regles/calcul-charges.md"
  titre: "Calcul des charges de copropriete"
  domaine: "syndic"
  type: "regle"
  aliases: ["calcul charges", "repartition charges", "appel de fonds", "f_calc_charges"]
  tags: ["#type/regle", "#domaine/syndic"]

Chunk #1-0 (metadata):
  content: "Calcul des charges de copropriete. Repartition des charges selon cles et tantiemes. Aliases: calcul charges, repartition charges, appel de fonds, f_calc_charges. Domaine: syndic. Type: regle. Liens: cles-de-repartition, reglement-de-copropriete, lot, tantiemes, f_calc_charges_ascenseur, charges-personnelles, decision-2024-03-refonte-charges."
  embedding_prefix: "[syndic] Calcul des charges de copropriete"
  position: 0

Chunk #1-1:
  section: "Principe"
  content: "Les charges sont reparties selon les [[cles-de-repartition]] definies dans le [[reglement-de-copropriete]]. Chaque [[lot]] a des [[tantiemes]] par cle."
  embedding_prefix: "[syndic] Calcul des charges de copropriete > Principe"
  position: 1

Chunk #1-2:
  section: "Formule"
  content: "charge_lot = (montant_total * tantiemes_lot) / total_tantiemes_cle"
  — FUSIONNE avec chunk precedent (< 100 mots)

Chunk #1-3:
  section: "Cas particuliers"
  content: "### Charges ascenseur\nSeuls les lots au-dessus du RDC paient.\nVoir [[f_calc_charges_ascenseur]] pour l'implementation.\n\n### Charges personnelles\nCertaines charges sont affectees directement a un lot.\nNe passent pas par la repartition. Voir [[charges-personnelles]]."
  embedding_prefix: "[syndic] Calcul des charges de copropriete > Cas particuliers"
  position: 2

Chunk #1-4:
  section: "Historique"
  content: "Refactore en 2024 — voir [[decision-2024-03-refonte-charges]]."
  — FUSIONNE avec chunk precedent (< 100 mots)

Links:
  chunk #1-1 → "cles-de-repartition"
  chunk #1-1 → "reglement-de-copropriete"
  chunk #1-1 → "lot"
  chunk #1-1 → "tantiemes"
  chunk #1-3 → "f_calc_charges_ascenseur"
  chunk #1-3 → "charges-personnelles"
  chunk #1-4 → "decision-2024-03-refonte-charges"
</output>
</example>
</examples>

<constraints>
## Ce qu'il ne faut PAS faire

1. **PAS de chunking par tokens fixes** (500 tokens, 1000 tokens). Toujours decouper aux frontieres semantiques (sections ##). Un chunk qui coupe au milieu d'une phrase est un bug.

2. **PAS de perte d'aliases**. Les aliases sont le systeme de synonymes. Si "appel de fonds" est un alias de "calcul charges", l'embedding du chunk 0 DOIT contenir les deux termes.

3. **PAS de perte de wikilinks**. Les liens entre notes sont le graphe de connaissances. Un chunk sans ses liens est un chunk ampute. Stocker les liens dans une table dediee ET dans le chunk 0.

4. **PAS d'indexation des dossiers exclus** : Templates/, Daily/, .claude/, doc/, neo-brain/, neo-brain-support/, fichiers a la racine du vault. Seuls 00-Hub/ a 07-Support/ et Knowledge/ sont des notes.

5. **PAS de schema complexe inutile**. 3 tables + 1 vue materialisee. Pas de chunk_relations avec 15 types de relations, pas de hierarchie de chunks parent/enfant sur 5 niveaux. Simple et efficace.

6. **PAS de re-embedding systematique**. Mode incremental obligatoire : hash SHA256 du contenu, skip si inchange. Les embeddings coutent de l'argent.

7. **PAS de modele d'embedding anglophone uniquement**. Le contenu est 100% francais. Choisir un modele multilingual performant.

## Decisions techniques a prendre

- **Modele d'embedding** : recommander le meilleur rapport qualite/prix pour du texte technique francais. Justifier le choix avec des benchmarks.
- **Dimension des vecteurs** : adapter au modele choisi. Pas de surdimensionnement.
- **Strategie de recherche hybride** : ponderation vector vs full-text. Proposer une formule et expliquer pourquoi.
- **Gestion du multilingual** : le contenu est francais mais contient des termes techniques anglais (noms de fonctions, SQL, etc.).
</constraints>

<verification>
Le systeme est reussi si :

1. **Recherche "appel de fonds"** retourne la note "Calcul des charges" en premier (grace aux aliases dans le chunk 0)
2. **Recherche "comment marche l'ascenseur en syndic"** retourne le chunk "Cas particuliers" de la note charges (recherche semantique)
3. **Recherche "f_calc_charges"** retourne la note charges ET la note de la fonction PG (full-text exact)
4. **Aucun chunk** ne coupe au milieu d'une phrase ou d'un bloc de code
5. **expand(chunk_id, depth=1)** retourne les chunks des notes liees par wikilinks
6. **Re-run du script** sans modification du vault = 0 embeddings recalcules
7. **682 notes** ingerees en < 10 minutes (embedding compris)
</verification>
```

---

## Notes d'implementation

- Placer le script dans `neoteem-brain/scripts/embedding/`
- Config via `.env` (connection PG, API key embedding, vault path)
- Requirements : `psycopg2-binary`, `pyyaml`, `openai` ou `voyageai` (selon modele choisi)
- Le script doit etre executable en standalone (`python ingest.py`) et en mode cron
