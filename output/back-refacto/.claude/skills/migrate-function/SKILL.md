---
name: migrate-function
description: Migrate a PostgreSQL function (f_/p_/proc_) to an application endpoint (TypeScript or Go). Reads source from functions repo, understands business logic, generates equivalent code. Use when user says "migre", "migrate", "convertis", "transforme f_xxx".
argument-hint: "f_get_proprietaires"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent
---

# Migrer une fonction PostgreSQL → endpoint applicatif

## Étape 1 — Charger la config

Lire `CLAUDE.md` pour récupérer :
- Le chemin du repo fonctions
- Le stack (TypeScript ou Go)

Si pas configuré → voir skill `schema-context`.

## Étape 2 — Trouver et lire la fonction

La fonction demandée est : `$ARGUMENTS`

1. `Glob "{repo}/**/$ARGUMENTS.sql"` → trouver le fichier
2. Lire le source en entier
3. Identifier le dossier parent = schéma/domaine

## Étape 3 — Charger le contexte domaine

1. Lire `doc/schemas/{domaine}.md` — surtout la section **Règles métier extraites**
2. Si besoin de colonnes précises → Grep sur `doc/dump/columns.csv`
3. Si la fonction appelle d'autres fonctions → les lire aussi

## Étape 4 — Analyser la fonction

Extraire et documenter :

- **Entrées** : paramètres (nom, type, valeur par défaut)
- **Sorties** : RETURNS TABLE / RETURNS type / OUT params
- **Tables touchées** : SELECT FROM, JOIN, INSERT INTO, UPDATE, DELETE FROM
- **Jointures** : toutes les conditions JOIN ON, surtout les conditionnelles (AND col = valeur)
- **Valeurs en dur** : WHERE col = 1, CASE WHEN type = 'X'
- **Filtres implicites** : deleted_at IS NULL, active = true
- **Fonctions appelées** : f_*, p_*, proc_* référencées dans le source
- **Logique métier** : CASE WHEN, IF/ELSIF, boucles, curseurs

## Étape 5 — Poser des questions AVANT de coder

**OBLIGATOIRE.** Présenter au dev :

```
## Analyse de {function_name}

**Ce que fait la fonction :**
{résumé en français de la logique}

**Tables :** {liste}
**Appelle :** {fonctions appelées}
**Appelée par :** {si trouvé dans d'autres fonctions}

**Règles métier détectées :**
- {règle 1}
- {règle 2}

**Questions :**
1. {question sur un choix métier ambigu}
2. {question sur les valeurs en dur — "role_id = 1 signifie bien propriétaire ?"}
3. {question sur le endpoint — route, méthode HTTP, auth ?}
```

Attendre les réponses avant de continuer.

## Étape 6 — Générer le code

Selon le stack :

### TypeScript
- Controller/route avec les paramètres d'entrée
- Service avec la logique métier
- Repository/query avec le SQL optimisé (passer à l'agent sql-optimizer si complexe)
- Types/interfaces pour les entrées et sorties

### Go
- Handler avec les paramètres d'entrée
- Service avec la logique métier
- Repository avec le SQL optimisé (passer à l'agent sql-optimizer si complexe)
- Structs pour les entrées et sorties

## Étape 7 — Documenter la migration

Ajouter un commentaire en tête du code généré :

```
// Migré depuis : {schema}/{function_name}.sql
// Tables : {liste}
// Règles métier : {résumé}
// Fonctions PostgreSQL remplacées : {liste}
```

## Apprentissage — Sauvegarder en mémoire projet

Après chaque migration, sauvegarder en mémoire les découvertes utiles pour les prochaines sessions :

- **Règles métier confirmées** par le dev (ex: "role_id = 1 = propriétaire" confirmé)
- **Patterns récurrents** détectés (ex: "toutes les fonctions du domaine copro filtrent sur active = true")
- **Conventions du projet** (structure des fichiers, nommage des routes, style de code)
- **Pièges découverts** (ex: "table X a des colonnes ambiguës, price = HT pas TTC")
- **Valeurs de référence validées** (les IDs magiques confirmés par le dev)

Ne PAS sauvegarder : le détail de chaque migration (c'est dans migration-tracker), le code généré, les infos éphémères.

## Règles

- Ne JAMAIS modifier ou supprimer les fichiers du repo fonctions
- Toujours poser des questions avant de générer le code
- Si la fonction appelle d'autres fonctions non migrées → le signaler au dev
- Si une valeur en dur est ambiguë → demander confirmation
- Pour les requêtes SQL complexes → déléguer à l'agent sql-optimizer
- Respecter les conventions du projet back (linter, structure, nommage)
