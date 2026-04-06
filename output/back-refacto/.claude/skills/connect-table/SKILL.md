---
name: connect-table
description: Connect an existing PostgreSQL table to the API. Use when user says 'connecte une table', 'expose une table existante', 'connect existing table', 'introspect DB', 'brancher Drizzle', 'hook up a table'.
user-invokable: true
argument-hint: "[nom de la table]"
effort: high
---

# Connecter une table PostgreSQL existante

La base Neoteem contient des centaines de tables. On ne les MODIFIE PAS.
On les introspecte et on construit par-dessus.

## 1. Introspection
```bash
bun run db:pull
```
Génère les schémas Drizzle dans `src/infra/postgres/schema/`.

## 2. Nettoyer le schéma généré
- Garder SEULEMENT les colonnes nécessaires pour le use case actuel
- Le premier argument de `pgTable()` = nom RÉEL de la table en DB
- Le premier argument de chaque colonne = nom RÉEL de la colonne en DB
- Le nom de la variable TypeScript peut être plus lisible

## 3. Créer l'entité domaine
Interface dans `src/core/domain/entities/`.
Noms métier propres (camelCase français), PAS les noms de colonnes DB.

## 4. Créer le mapper
Fonction pure dans `src/infra/postgres/mappers/`.
Transforme les noms DB (snake_case) → noms domaine (camelCase).

## 5. Créer le repository
Implémente le port out. Pour les requêtes complexes, utiliser SQL brut :
```typescript
// Simple → API Drizzle
const rows = await db.select().from(table).where(eq(table.id, id));

// Complexe → SQL typé
const rows = await db.execute(sql`SELECT ... FROM ... WHERE ...`);
```

## Règles
- JAMAIS modifier le schéma DB via Drizzle migrate
- Si besoin de nouvelles tables (logs IA, tracking), schéma séparé
- Tester avec la DB réelle : `bun test --filter "[NomRepository]"`
