---
name: create-endpoint
description: Create an application endpoint (TypeScript or Go) from a business need. Searches relevant PostgreSQL tables and functions, asks questions, generates code with optimized SQL. Use when user says "j'ai besoin d'un endpoint", "create a route", "add an endpoint", "I need an API for".
argument-hint: "récupérer les informations des copros"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent
---

# Créer un endpoint à partir d'un besoin métier

## Étape 1 — Charger la config

Lire `CLAUDE.md` pour récupérer :
- Le chemin du repo fonctions
- Le stack (TypeScript ou Go)

Si pas configuré → voir skill `schema-context`.

## Étape 2 — Comprendre le besoin

Le besoin est : `$ARGUMENTS`

Poser immédiatement les premières questions :

```
## Besoin : {$ARGUMENTS}

Avant de chercher, quelques précisions :

1. C'est de la lecture (GET), écriture (POST/PUT), ou suppression (DELETE) ?
2. Quels filtres / paramètres d'entrée ? (par ID, par recherche, paginé ?)
3. Quelles données en sortie ? (tout, un résumé, des champs spécifiques ?)
4. Y a-t-il des droits/rôles à vérifier ?
```

## Étape 3 — Chercher dans la doc et le repo

En parallèle :

### 3a. Chercher les tables
1. Lire `doc/schemas/RAPPORT.md` → identifier le(s) domaine(s) concerné(s)
2. Lire `doc/schemas/{domaine}.md` → tables, FK, règles métier
3. Grep `doc/dump/columns.csv` pour les colonnes des tables pertinentes

### 3b. Chercher les fonctions existantes
1. Grep dans le repo fonctions pour les mots-clés du besoin
2. Identifier les `f_*` (lecture) ou `p_*` (écriture) qui font quelque chose de similaire
3. Lire le source des fonctions trouvées

### 3c. Comparer
- Les fonctions existantes couvrent-elles le besoin ?
- Manque-t-il des données ? → regarder directement les tables
- Les fonctions sont-elles optimales ? → signaler si jointures inutiles ou requêtes N+1

## Étape 4 — Proposer une approche

Présenter au dev :

```
## Proposition pour : {besoin}

**Domaine(s) :** {liste}
**Tables principales :** {liste avec colonnes clés}

**Fonctions existantes pertinentes :**
- `f_{name}` → {ce qu'elle fait, ce qu'elle couvre}
- `p_{name}` → {ce qu'elle fait}

**Ce que les fonctions ne couvrent PAS :**
- {donnée manquante, filtre absent, etc.}

**Approche proposée :**
- Route : {méthode} {path}
- Requête SQL : {description de la requête, basée sur les tables directement}
- Données retournées : {liste des champs}

**Règles métier à respecter :**
- {règle extraite du doc domaine}
- {filtre implicite}

**Questions :**
1. {question sur un choix}
2. {question sur les données à retourner}
```

Attendre validation avant de coder.

## Étape 5 — Générer le code

### La requête SQL

**Ne PAS copier la requête de la fonction PostgreSQL.** Écrire une requête optimisée directement sur les tables :
- Utiliser les FK de `doc/dump/fk.csv` pour les jointures
- Respecter les règles métier extraites (filtres implicites, valeurs de référence)
- Pour les requêtes complexes → déléguer à l'agent sql-optimizer

### Le code applicatif

Selon le stack (TypeScript ou Go) — même structure que `/migrate-function` :
- Controller/Handler + Service + Repository
- Types/Structs
- Validation des entrées

## Étape 6 — Documenter

Commentaire en tête :

```
// Endpoint : {méthode} {route}
// Besoin : {description}
// Tables : {liste}
// Fonctions PostgreSQL de référence : {liste} (non utilisées directement, consultées pour la logique)
// Règles métier : {résumé}
```

## Apprentissage — Sauvegarder en mémoire projet

Après chaque endpoint créé, sauvegarder en mémoire :

- **Règles métier découvertes** et confirmées par le dev
- **Patterns d'architecture** du projet (structure routes, middleware, validation)
- **Tables de référence** et leurs valeurs (codes, types, statuts)
- **Jointures validées** qui pourront resservir (ex: "pour avoir les lots d'une copro, toujours passer par lot_copro")
- **Pièges confirmés** (ex: "ne jamais joindre users avec admin_users")

## Règles

- Ne JAMAIS modifier ou supprimer les fichiers du repo fonctions
- Toujours poser des questions AVANT de coder
- Ne PAS juste envelopper une fonction PostgreSQL dans un endpoint — requêter les tables directement
- Utiliser les fonctions existantes comme **référence** pour comprendre la logique, pas comme implémentation
- Si une requête est complexe (3+ jointures, sous-requêtes, agrégations) → agent sql-optimizer
- Respecter les conventions du projet back
