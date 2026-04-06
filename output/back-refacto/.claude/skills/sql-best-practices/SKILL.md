---
name: sql-best-practices
description: PostgreSQL SQL best practices for this project — rules, anti-patterns, pagination, query optimization. Load when writing SQL, Drizzle queries, or reviewing database access patterns.
user-invokable: false
---

# PostgreSQL SQL Best Practices

## Core rules

1. **Never SELECT \*** — always name columns explicitly
2. **Always paginate** — no unbounded queries on large tables
3. **Use parameterized queries** — never interpolate user input into SQL
4. **Index before querying** — check `EXPLAIN ANALYZE` on any query touching >10k rows
5. **Never modify PostgreSQL functions** in the `pg-functions` repo — read-only

## Drizzle query patterns

### Pagination
```typescript
// Always paginate list queries
const rows = await db
  .select()
  .from(coproprietes)
  .orderBy(asc(coproprietes.nom))
  .limit(limit)
  .offset((page - 1) * limit);

const [{ count }] = await db
  .select({ count: sql<number>`count(*)` })
  .from(coproprietes);

return {
  data: rows.map(toCopropriete),
  pagination: { page, limit, total: Number(count), totalPages: Math.ceil(Number(count) / limit) },
};
```

### Null-safe comparisons
```typescript
// Use isNull / isNotNull, not eq(col, null)
.where(isNull(lots.dateCession))
.where(isNotNull(comptes.iban))
```

### Transactions
```typescript
await db.transaction(async (tx) => {
  await tx.insert(ecritures).values(debit);
  await tx.insert(ecritures).values(credit);
});
// If either insert fails, both are rolled back
```

### Calling PostgreSQL functions (read-only)
```typescript
// Call existing f_* or p_* functions via sql tag
const result = await db.execute(
  sql`SELECT * FROM f_get_solde_copropriete(${coproprieteId})`
);
```

## Anti-patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `SELECT *` | Fetches unused columns, breaks on schema change | Name columns |
| Unbounded query | OOM on large tables | Always `.limit()` |
| Logic in SQL | Business rules split between layers | Move to use case |
| Raw string concat | SQL injection | Drizzle parameterizes automatically |
| N+1 queries | Performance collapse | Use JOINs or batch loading |
| `any` on DB results | Type safety lost | Use Drizzle inferred types |

## PostgreSQL function conventions

| Prefix | Purpose |
|--------|---------|
| `f_*` | Read (SELECT) — safe to call anytime |
| `p_*` | Write (INSERT/UPDATE/DELETE) — use in transactions |
| `proc_*` | Orchestration procedure |
| `tr_*` | Trigger — never call directly |

## Performance checklist

- [ ] Query uses an index (check with `EXPLAIN ANALYZE`)
- [ ] No `SELECT *`
- [ ] Lists are paginated (max 100 rows per page)
- [ ] Joins are on indexed columns
- [ ] No correlated subqueries in loops
- [ ] Heavy aggregations use materialized views or are cached

## See also

- `references/advanced-optimization.md` — EXPLAIN, indexes, VACUUM
- `references/typescript-patterns.md` — TypeScript + Drizzle type patterns
