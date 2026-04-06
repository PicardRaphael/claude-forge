# Database Rules - MANDATORY

## MCP PostgreSQL disponible

Le MCP PostgreSQL est configuré. L'utiliser pour :
- Explorer la structure (tables, colonnes, FK, indexes, triggers)
- Lire le source des fonctions (f_*, p_*, proc_*, tr_*)
- Vérifier les types de colonnes

**INTERDIT via MCP :**
- SELECT sur les données (sauf tables de référence < 100 lignes)
- INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE

## Drizzle ORM — Règles

- `bun run db:pull` pour introspection — JAMAIS `drizzle migrate`
- Le schéma PostgreSQL est IMMUTABLE — ne jamais modifier la structure
- Garder uniquement les colonnes nécessaires dans le schéma Drizzle
- Requêtes simples → Drizzle API
- Requêtes complexes → `sql\`\`` raw

## SQL dans le code

- Placeholders `$1, $2` — jamais de concaténation
- Lister les colonnes — jamais `SELECT *`
- `JOIN ... ON` explicite — jamais de jointure dans WHERE
- Filtre soft-delete si applicable
- Cursor-based pagination si > 1000 lignes
- `numeric/decimal` → `string` en TypeScript, jamais `number`

## Repo fonctions PostgreSQL

- **LECTURE SEULE** — ne JAMAIS modifier
- Les fonctions sont une RÉFÉRENCE pour comprendre la logique métier
- Ne pas copier les requêtes telles quelles — adapter pour Drizzle
- SQL reste dans les repositories, logique métier dans les use cases

## Migration tracker

Après chaque migration : mettre à jour `doc/migration-tracker.md`
