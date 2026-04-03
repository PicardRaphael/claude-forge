---
name: sql-best-practices
description: PostgreSQL SQL best practices for large databases (200+ tables, millions of rows). Covers query optimization, indexing, anti-patterns, and type-safe patterns. Loaded by sql-optimizer, migrate-function, create-endpoint, update-endpoint.
user-invokable: false
---

# PostgreSQL SQL — Best practices

## Règles absolues

1. **Jamais de SELECT *** — toujours lister les colonnes
2. **Jamais de jointure implicite** — toujours `JOIN ... ON`
3. **Jamais de OFFSET > 1000** — cursor-based pagination
4. **Jamais de N+1** — une requête avec JOIN, pas une boucle
5. **Jamais de string concatenation SQL** — placeholders `$1, $2`
6. **Toujours le filtre soft-delete** si le projet en utilise
7. **Toujours typer les résultats** — pas de `any` ou `interface{}`
8. **numeric/decimal PostgreSQL → string (TS) ou decimal.Decimal (Go)** — jamais float
9. **CREATE INDEX CONCURRENTLY** en production — jamais sans CONCURRENTLY
10. **EXISTS au lieu de IN** pour sous-requêtes corrélées

## Jointures

```sql
-- CORRECT : explicite
SELECT u.name, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.deleted_at IS NULL

-- INTERDIT : implicite
SELECT u.name, o.total FROM users u, orders o WHERE o.user_id = u.id
```

- Table la plus restrictive en premier dans le FROM
- Filtres sur la table jointe dans le `ON`, pas dans le `WHERE`
- `LEFT JOIN` uniquement si on veut les lignes sans correspondance
- Max 5-6 jointures par requête — au-delà, CTE ou découper

## Pagination

```sql
-- Petits datasets (<1000)
SELECT * FROM coproprietes WHERE active = true ORDER BY name LIMIT 20 OFFSET 40;

-- Grands datasets — cursor-based (OBLIGATOIRE si offset > 1000)
SELECT * FROM coproprietes WHERE active = true AND id > $1 ORDER BY id LIMIT 20;
```

## Anti-patterns critiques

| Anti-pattern | Fix |
|-------------|-----|
| `WHERE LOWER(col) = 'x'` | `WHERE col ILIKE 'x'` ou expression index |
| `SELECT DISTINCT` sur grosse table | `GROUP BY` |
| Sous-requête corrélée par ligne | Window function (`SUM() OVER()`) |
| `OR` sur colonnes différentes | `UNION` |
| UUIDv4 comme PK | UUIDv7 ou `BIGSERIAL` |
| `OFFSET 50000` | Cursor-based pagination |

## Références détaillées

Pour les techniques avancées, consulter dans `references/` :
- `advanced-optimization.md` — indexing avancé (BRIN, GIN, partial, covering), EXPLAIN ANALYZE, partitioning, materialized views, bulk ops, window functions, JSONB, locks, connection pooling, vacuum
- `typescript-patterns.md` — patterns type-safe pour TypeScript + PostgreSQL
- `go-patterns.md` — patterns type-safe pour Go + PostgreSQL
