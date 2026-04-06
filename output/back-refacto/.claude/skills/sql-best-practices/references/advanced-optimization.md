# Advanced PostgreSQL Optimization

## EXPLAIN ANALYZE

Always use `EXPLAIN (ANALYZE, BUFFERS)` to diagnose slow queries:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT c.*, COUNT(l.id) AS lot_count
FROM coproprietes c
LEFT JOIN lots l ON l.copropriete_id = c.id
WHERE c.syndic_id = 42
GROUP BY c.id;
```

**Key metrics to read:**
- `Seq Scan` on large tables → missing index
- `Hash Join` vs `Nested Loop` → hash join is better for large result sets
- `rows=X` vs `actual rows=Y` — large discrepancy = stale statistics
- `Buffers: shared hit=X read=Y` — high `read` = data not in cache

Run `ANALYZE [table_name]` to update statistics.

## Index patterns

### B-tree (default) — for equality and range
```sql
CREATE INDEX idx_lots_copropriete_id ON lots(copropriete_id);
CREATE INDEX idx_ecritures_date ON ecritures(date_ecriture);
CREATE INDEX idx_coproprietes_syndic_nom ON coproprietes(syndic_id, nom);  -- composite
```

### When Drizzle adds indexes:
```typescript
// In the table schema
export const lots = pgTable("lots", {
  id: serial("id").primaryKey(),
  coproprieteId: integer("copropriete_id").references(() => coproprietes.id),
  // ...
}, (table) => ({
  coproprieteIdx: index("idx_lots_copropriete_id").on(table.coproprieteId),
}));
```

## Common slow query patterns

### N+1 — fetch list then query each item
```typescript
// ❌ N+1
const lots = await repo.findByCopropriete(id);
for (const lot of lots) {
  lot.tantiemes = await repo.findTantiemesByLot(lot.id); // N queries!
}

// ✅ Single JOIN query
const lotsWithTantiemes = await db
  .select()
  .from(lots)
  .leftJoin(tantiemes, eq(tantiemes.lotId, lots.id))
  .where(eq(lots.coproprieteId, id));
```

### Unbounded aggregation
```sql
-- ❌ Counts every row, every time
SELECT COUNT(*) FROM ecritures;

-- ✅ Use pg_stat_user_tables for approximate counts on large tables
SELECT reltuples::bigint AS estimate
FROM pg_class WHERE relname = 'ecritures';
```

## VACUUM and autovacuum

PostgreSQL's MVCC creates dead tuples. `autovacuum` cleans them automatically.
If a table has high write volume and queries slow down:

```sql
-- Check table bloat
SELECT schemaname, tablename, n_dead_tup, n_live_tup,
       round(n_dead_tup::numeric/NULLIF(n_live_tup,0)*100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Manual vacuum if needed (DBA task)
VACUUM ANALYZE coproprietes;
```

## Connection pooling

In production, use PgBouncer or similar. Drizzle's postgres.js has a built-in pool:

```typescript
// src/infra/postgres/client.ts
import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";

const client = postgres(env.DATABASE_URL, {
  max: 10,        // Max connections in pool
  idle_timeout: 30,
  connect_timeout: 10,
});

export const db = drizzle(client, { schema });
```
