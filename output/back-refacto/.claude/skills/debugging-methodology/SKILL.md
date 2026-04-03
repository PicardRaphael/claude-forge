---
name: debugging-methodology
description: Root-cause-first debugging methodology. 5 levels of isolation, common patterns for PostgreSQL migration bugs, SQL debugging techniques. Loaded by debugger agent.
user-invokable: false
---

# Méthodologie de debugging

## Les 5 niveaux d'isolation

Toujours descendre du symptôme vers la cause racine :

```
Niveau 1 — Endpoint/Route
  Est-ce le bon endpoint qui est appelé ?
  Les paramètres arrivent-ils correctement ?

Niveau 2 — Service/Logique métier
  La logique de traitement est-elle correcte ?
  Les conditions/validations sont-elles bonnes ?

Niveau 3 — Repository/Requête SQL
  La requête retourne-t-elle les bonnes données ?
  Les jointures sont-elles correctes ?
  Les filtres sont-ils appliqués ?

Niveau 4 — Données
  Les données en base sont-elles correctes ?
  Y a-t-il des incohérences (orphelins, doublons) ?

Niveau 5 — Infrastructure
  Connexion DB OK ? Timeout ? Pool saturé ?
```

## Bugs typiques de migration PostgreSQL → Applicatif

| Symptôme | Cause probable | Comment vérifier |
|----------|---------------|-----------------|
| Données manquantes | Filtre soft-delete oublié (`deleted_at IS NULL`) | Comparer la requête migrée avec la fonction originale |
| Mauvaises données | Valeur en dur incorrecte (role_id = 2 au lieu de 1) | Lire la fonction originale, vérifier les valeurs |
| Erreur jointure | FK incorrecte ou table manquante | Vérifier doc/dump/fk.csv |
| Résultats vides | Condition WHERE trop restrictive | Comparer chaque WHERE avec l'original |
| Doublons | JOIN manquant ou mal conditionné | Vérifier la fonction originale |
| Erreur type | numeric → float au lieu de string | Vérifier le mapping types |
| Lenteur soudaine | Index manquant sur colonne de filtre | Vérifier doc/dump/indexes.csv |
| Crash NULL | Colonne nullable non gérée | Vérifier is_nullable dans doc/dump/columns.csv |

## Techniques de diagnostic SQL

### Vérifier une requête suspecte
1. Lire la requête dans le code
2. La comparer avec la fonction PostgreSQL originale — diff ligne par ligne
3. Vérifier chaque JOIN avec doc/dump/fk.csv
4. Vérifier chaque colonne avec doc/dump/columns.csv
5. Chercher les valeurs en dur et les comparer avec l'original

### Trouver quel endpoint utilise une table
```
Grep pattern="FROM\s+{table}|JOIN\s+{table}|INTO\s+{table}" path="src/"
```

### Trouver la fonction originale d'un endpoint migré
Lire le commentaire en tête du fichier : `// Migré depuis : {schema}/{function}.sql`

## Apprentissage

Après chaque debug, sauvegarder en mémoire :
- **Patterns de bugs récurrents** (même cause dans plusieurs endroits)
- **Pièges BDD découverts** (colonnes ambiguës, données incohérentes)
- **Fonctions mal migrées** identifiées
