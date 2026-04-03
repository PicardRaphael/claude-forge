---
name: update-endpoint
description: Modify an existing endpoint to add fields, change behavior, or extend functionality. Checks PostgreSQL tables and functions to find missing data. Use when user says "ajoute ce champ", "modifie l'endpoint", "il faut aussi retourner", "update the route", "add this field".
argument-hint: "ajoute le nombre de lots à l'endpoint GET /copros"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent
---

# Modifier un endpoint existant

## Étape 1 — Charger la config

Lire `CLAUDE.md` pour :
- Chemin du repo fonctions
- Stack (TypeScript ou Go)

## Étape 2 — Comprendre la demande

Le besoin est : `$ARGUMENTS`

Identifier :
- Quel endpoint modifier ? (route, fichier)
- Quoi ajouter/changer ? (champ, filtre, comportement)

## Étape 3 — Lire l'endpoint existant

1. Trouver le fichier de l'endpoint (Grep sur la route ou le nom)
2. Lire le code : controller/handler + service + repository
3. Identifier la requête SQL actuelle
4. Identifier les tables déjà utilisées

## Étape 4 — Trouver les données manquantes

Pour les nouveaux champs ou comportements demandés :

### 4a. Chercher dans les tables
1. Grep `doc/dump/columns.csv` pour trouver quelle table a la colonne demandée
2. Vérifier les FK dans `doc/dump/fk.csv` — comment joindre cette table à celles déjà utilisées
3. Lire `doc/schemas/{domaine}.md` pour les règles métier

### 4b. Chercher dans les fonctions existantes
1. Grep dans le repo fonctions pour des fonctions qui retournent déjà cette donnée
2. Lire le source → comprendre les jointures et conditions nécessaires
3. Les fonctions sont une **référence**, pas une implémentation à copier

### 4c. Vérifier la performance
Si la modification ajoute des jointures ou change la requête de façon significative → déléguer à l'agent sql-optimizer

## Étape 5 — Proposer avant de modifier

```
## Modification de {endpoint}

**Endpoint actuel :** {méthode} {route}
**Requête actuelle :** {résumé — tables, jointures}

**Modification demandée :** {résumé}

**Ce qu'il faut changer :**
- SQL : ajouter JOIN sur `{table}` via `{fk}`
- Réponse : ajouter le champ `{champ}` ({type})
- {autre changement}

**Règles métier à respecter :**
- {règle du doc domaine}

**Impact performance :**
- {estimation — jointure supplémentaire, index existant ou non}

**Questions :**
1. {si ambigu}
```

Attendre validation.

## Étape 6 — Modifier le code

- Mettre à jour la requête SQL (repository)
- Mettre à jour le type/struct de réponse
- Mettre à jour le service si logique métier ajoutée
- Mettre à jour le commentaire de documentation en tête

## Apprentissage — Sauvegarder en mémoire projet

Après chaque modification, sauvegarder en mémoire :

- **Nouvelles jointures validées** (FK confirmées, chemins entre tables)
- **Colonnes problématiques** (nommage ambigu, types inattendus)
- **Feedback du dev** sur les choix (préférence de structure, format de réponse)
- **Patterns de modification** récurrents (ex: "quand on ajoute un champ, toujours aussi l'ajouter à l'index de recherche")

## Règles

- Ne JAMAIS modifier les fichiers du repo fonctions
- Toujours proposer avant de modifier
- Vérifier les FK pour les nouvelles jointures — ne pas inventer de relations
- Si la colonne demandée n'existe dans aucune table → le dire au dev
- Pour les modifications complexes → agent sql-optimizer
- Respecter le style du code existant
