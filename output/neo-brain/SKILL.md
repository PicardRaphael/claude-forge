---
name: neo-brain
description: Search, read, and contribute to the neoteem-brain Obsidian vault. Use when you need business context, domain knowledge, database documentation, architecture decisions, or want to capitalize a discovery.
allowed-tools: Bash
---

# Neo Brain — Acces au vault neoteem-brain

Le vault `neoteem-brain` est la **source de verite** pour les connaissances metier Neoteem : tables, fonctions PG, schemas, regles metier, domaines (syndic, gerance, compta), decisions archi, et connaissances accumulees.

**Prerequis :** Obsidian doit etre ouvert avec le vault `neoteem-brain`.

## CLI — REGLE ABSOLUE

**Ne JAMAIS appeler `obsidian` directement.** Sur Windows + Git Bash, `obsidian` resout vers l'app GUI (Obsidian.exe) au lieu de la CLI console (Obsidian.com). Ca casse tout.

**Toujours utiliser le wrapper** — remplacer `obsidian` par `bash .claude/skills/neo-brain/scripts/obsidian-cli.sh` :

```bash
# CORRECT :
bash .claude/skills/neo-brain/scripts/obsidian-cli.sh vault="neoteem-brain" search query="charges" limit=10

# INTERDIT :
obsidian vault="neoteem-brain" search query="charges" limit=10
```

Les exemples ci-dessous utilisent `obsidian` par concision, mais **tu DOIS remplacer par le wrapper dans chaque appel Bash**.

## Apprendre le vault — Exploration systematique

Quand tu dois comprendre un domaine, un concept, ou cartographier les connaissances :

### Etape 1 : Vue d'ensemble (god nodes)

```bash
# Les MOCs sont les noeuds centraux — commencer par la
obsidian vault="neoteem-brain" read file="Home"

# Lire les Maps of Content par domaine
obsidian vault="neoteem-brain" read file="MOC-BDD"
obsidian vault="neoteem-brain" read file="MOC-Domaines"
obsidian vault="neoteem-brain" read file="MOC-Apps"
obsidian vault="neoteem-brain" read file="MOC-Architecture"

# Tags = vue statistique des domaines couverts
obsidian vault="neoteem-brain" tags sort=count counts
```

### Etape 2 : Exploration en profondeur (BFS par domaine)

A partir d'un MOC, suivre TOUS les `[[wikilinks]]` niveau par niveau :

1. **Lire le MOC** — noter chaque `[[lien]]` mentionne
2. **Lire chaque note liee** — noter les `[[wikilinks]]` et `backlinks` de chacune
3. **Suivre les connexions cross-dossier** — un lien de `02-BDD/` vers `01-Domaines/` revele une regle metier implementee en PG. Ces liens transversaux sont les plus precieux.
4. **Repeter** jusqu'a epuiser les connexions du domaine

### Etape 3 : Identifier les lacunes

```bash
# Chercher les notes orphelines (peu de backlinks = sous-documente)
obsidian vault="neoteem-brain" backlinks file="nom-note" counts
# Si counts = 0 ou 1, c'est un concept isole → a investiguer
```

Signaux de lacunes :
- Note avec 0 backlinks = concept orphelin, potentiellement sous-documente
- `[[lien]]` dans le contenu qui ne correspond a aucune note = connaissance manquante
- Domaine present dans les tags mais absent des MOCs = pas encore structure

### Etape 4 : Connexions surprenantes

Les liens les plus instructifs sont ceux qui traversent les frontieres :
- `01-Domaines/` ↔ `02-BDD/` = regle metier implementee en base
- `02-BDD/` ↔ `03-Apps/` = fonction PG appelee par un service
- `05-Decisions/` ↔ n'importe quoi = contexte "pourquoi" derriere un choix
- `Knowledge/` ↔ sources multiples = synthese cross-domaine

Toujours suivre ces liens en priorite — ils revelent les relations non evidentes.

### Budget tokens

- **Overview** : Home + 4 MOCs + tags = ~2000 tokens, suffisant pour savoir ou creuser
- **Un domaine complet** : 10-30 notes, paginer les grosses (voir "Analyse de fichiers massifs")
- **Recherche ponctuelle** : 2-5 notes suffisent, utiliser la methode ci-dessous

## Consulter (recherche ponctuelle)

Toutes les commandes commencent par `obsidian vault="neoteem-brain"`.

```bash
# Chercher — le CLI utilise l'index Obsidian, pas le filesystem
obsidian vault="neoteem-brain" search query="charges copropriete" limit=10

# Chercher avec contexte (lignes autour du match)
obsidian vault="neoteem-brain" search:context query="f_calc_charges" limit=5

# Lire une note — file= resout comme un wikilink (nom seul, pas de chemin)
obsidian vault="neoteem-brain" read file="calc-charges-copro"

# Backlinks — voir toutes les notes qui pointent vers celle-ci
obsidian vault="neoteem-brain" backlinks file="calc-charges-copro" counts

# Tags — explorer par domaine
obsidian vault="neoteem-brain" tags sort=count counts
```

Voir `references/obsidian-cli-commands.md` pour la liste complete des commandes.

## Methode de recherche — Token-smart

Deux modes selon l'intention. Choisir le bon AVANT de chercher.

### Mode Query (repondre a une question)

Objectif : reponse precise, minimum de tokens.

1. **`search:context`** d'abord — renvoie les snippets autour des matches, PAS le fichier entier
   ```bash
   obsidian vault="neoteem-brain" search:context query="charges copropriete" limit=5
   ```
2. **Trier** — lire les snippets retournes. Identifier les 1-3 notes les plus pertinentes
3. **`read`** seulement si le snippet ne suffit pas — et seulement les notes triees a l'etape 2
4. **Suivre les connexions** uniquement si la reponse est encore incomplete
5. **Stopper** des que la reponse est complete — ne pas lire "au cas ou"

> **Budget** : une query typique = 1 search:context + 1-2 reads. Pas 10.

### Mode Exploration (cartographier un domaine)

Objectif : comprendre en profondeur, lecture complete obligatoire.

1. **Chercher** avec `search query="..."` — laisser l'index trouver
2. **Lire** la note trouvee avec `read file="..."` — lecture complete, pas de raccourci
3. **Suivre les connexions** avec `backlinks file="..."` et les `[[wikilinks]]` dans le contenu
4. **Iterer** — lire les notes liees, suivre les backlinks, jusqu'a avoir le contexte complet

Ce mode est reserve a : repo-analyzer, vault-enricher, et demandes explicites d'exploration.

Ne pas prescrire de chemin — `search` et `file=` resolvent automatiquement.

## Capitaliser (creer un Knowledge)

Quand tu decouvres une regle metier, un comportement PG, ou une decision importante :

```bash
obsidian vault="neoteem-brain" create path="Knowledge/explorations/e-sujet.md" content="---\ntitre: \"Sujet\"\nresume: \"1 ligne — le fait principal\"\naliases:\n  - \"synonyme, formulation alternative\"\ntype: knowledge\ncree: YYYY-MM-DD\nsources:\n  - \"note-source\"\nauteur: claude\nrepo: NOM-DU-REPO\nderniere-maj: YYYY-MM-DD\ntags:\n  - \"#type/knowledge\"\n---\n\n# Sujet\n\n[Resume 2-3 lignes]\n\n## Points cles\n\n- Point 1\n- Point 2\n\n## Fonctionnement detaille\n\n[Details]\n\n## Notes sources\n\n- [[source-1]] - contexte" silent
```

| Sous-dossier | Quand | Prefixe |
|---|---|---|
| `Knowledge/questions/` | Reponse a une question metier | `q-` |
| `Knowledge/syntheses/` | Croisement de 2+ notes | `s-` |
| `Knowledge/explorations/` | Decouverte depuis le code | `e-` |

Voir `references/knowledge-conventions.md` pour les conventions completes.

## Enrichir une note existante

```bash
obsidian vault="neoteem-brain" append file="q-charges-copro" content="\n\n## Complement\n\n- Nouvelle info"
obsidian vault="neoteem-brain" property:set name="derniere-maj" value="YYYY-MM-DD" file="q-charges-copro"
```

## Corriger une note (info obsolete ou fausse)

Quand l'utilisateur signale qu'une info est fausse ou obsolete (table supprimee, fonction renommee, processus change) :

1. **Trouver la note source** avec `search:context query="..."` 
2. **Mettre a jour la note** avec `append` — ajouter une section `## Obsolete` ou corriger le contenu
3. **Mettre a jour `derniere-maj`** avec `property:set`
4. **Chercher les Knowledge qui referent cette note** avec `backlinks file="..."` 
5. **Mettre a jour chaque Knowledge impacte** — corriger l'info, pas creer un nouveau Knowledge

```bash
# Exemple : la table t_xyz n'existe plus
obsidian vault="neoteem-brain" append file="t-xyz" content="\n\n> [!warning] Obsolete\n> Cette table a ete supprimee le YYYY-MM-DD. Remplacee par [[t-abc]]."
obsidian vault="neoteem-brain" property:set name="derniere-maj" value="YYYY-MM-DD" file="t-xyz"
obsidian vault="neoteem-brain" property:set name="statut" value="obsolete" file="t-xyz"
```

**Regle** : ne JAMAIS creer une nouvelle note pour corriger une ancienne. Corriger sur place + propager aux backlinks.

## Analyse de fichiers massifs — REGLE ABSOLUE (mode Exploration uniquement)

Cette regle s'applique en **mode Exploration** (repo-analyzer, vault-enricher, exploration explicite). En mode Query, voir "Methode de recherche — Token-smart" ci-dessus.

**En exploration, les notes du brain et les fichiers source des repos peuvent faire 1000+ lignes. Ne JAMAIS couper l'analyse.**

1. **Paginer pour tout couvrir** — utiliser `Read` avec `offset`/`limit` (ou `head`/`tail`) pour diviser en morceaux digestibles (ex: 500 lignes), mais **continuer jusqu'a la derniere ligne**
2. **Ne jamais s'arreter au milieu** — un fichier de 1822 lignes lu en 4 passes de 500 = OK. Lu en 1 passe de 80 = INTERDIT
3. **Documenter chaque section au fur et a mesure** — noter les sections trouvees (role, acces, contacts, lots, compta, historique, locataires, factures, contrats, membres CS, etc.)
4. **Un fichier = lecture complete** — si un dossier contient plusieurs fichiers, les lire UN PAR UN integralement
5. **Prendre son temps** — 5 passes completes valent mieux qu'une seule incomplete. Ne JAMAIS dire "c'est massif, je ne peux pas tout lire" — paginer et tout couvrir

## Gotchas

- Obsidian doit etre lance — la CLI parle a l'instance ouverte, pas au filesystem
- `file=` resout comme un wikilink (nom seul), `path=` est le chemin exact — ne pas confondre
- Ne jamais modifier les notes dans `01-Domaines/`, `02-BDD/`, `03-Apps/` — seulement lire
- Ecriture autorisee dans `Knowledge/` et en `append` sur notes existantes
- Utiliser `silent` sur `create` pour ne pas ouvrir la note dans Obsidian
- Mettre le nom du repo courant dans `repo:` du frontmatter (pas un repo en dur)

## Apprentissage

Quand tu utilises cette skill et que tu decouvres :
- Une commande CLI qui ne fonctionne pas comme prevu → noter ici
- Un pattern de recherche plus efficace → noter ici
- Une convention du vault non documentee → noter ici
