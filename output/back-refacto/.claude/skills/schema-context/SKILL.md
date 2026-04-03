---
name: schema-context
description: Loads database context (doc/schemas/ + SQL functions repo) for migrate-function and create-endpoint skills. Do not invoke directly.
user-invokable: false
---

# Contexte BDD

## Configuration requise

Le fichier `CLAUDE.md` du projet doit contenir :

```markdown
## Config BDD
- Repo fonctions : /chemin/absolu/vers/repo-functions
- Stack : typescript | go
```

Si cette config n'existe pas, STOP et demander au dev :
1. Le chemin absolu du repo des fonctions PostgreSQL
2. Le stack choisi (TypeScript ou Go)

Puis proposer d'ajouter la config dans CLAUDE.md.

## Sources disponibles

### 1. Documentation domaines (locale)

`doc/schemas/*.md` — générés par l'agent schema-mapper. Chaque fichier contient :
- Tables du domaine + arbre FK
- Fonctions associées (f_, p_, proc_, tr_)
- **Règles métier extraites du code** (valeurs en dur, jointures conditionnelles, filtres implicites)
- Jointures fréquentes avec SQL

`doc/schemas/RAPPORT.md` — vue d'ensemble de tous les domaines.

### 2. Tables (locale)

`doc/dump/*.csv` — export brut des tables :
- `tables.csv`, `fk.csv`, `columns.csv`, `indexes.csv`, `triggers.csv`
- Utiliser Grep pour extraire les colonnes d'une table spécifique, ne jamais lire columns.csv en entier

### 3. Fonctions (repo externe)

Structure du repo :
```
{repo}/
  {schema}/           ← un dossier par schéma PostgreSQL
    f_*.sql           ← lecture
    p_*.sql           ← écriture
    proc_*.sql        ← procédures
    tr_*.sql          ← triggers
```

## Comment trouver le contexte pour une tâche

### A partir d'un nom de fonction (ex: `f_get_proprietaires`)

1. Identifier le préfixe → convention (f_ = lecture)
2. Chercher le fichier : `Glob "{repo}/**/f_get_proprietaires.sql"`
3. Le dossier parent = le schéma/domaine
4. Charger `doc/schemas/{domaine}.md` pour le contexte tables + règles métier
5. Lire le source de la fonction

### A partir d'un besoin métier (ex: "infos des copros")

1. Chercher le domaine dans `doc/schemas/RAPPORT.md`
2. Charger `doc/schemas/{domaine}.md`
3. Identifier les tables pertinentes
4. Chercher les fonctions existantes : `Grep pattern="{mot_clé}" path="{repo}/{domaine}/"` 
5. Lire les sources des fonctions trouvées

### A partir d'une table (ex: `copropriete`)

1. Grep dans les doc/schemas/ pour trouver le domaine
2. Grep dans le repo pour trouver quelles fonctions utilisent cette table
3. Lire les colonnes : `Grep pattern=",copropriete," path="doc/dump/columns.csv"`
