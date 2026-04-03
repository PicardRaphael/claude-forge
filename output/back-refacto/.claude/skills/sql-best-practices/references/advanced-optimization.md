# PostgreSQL — Optimisation avancée pour grosses BDD

## 1. Indexing avancé

### Partial Indexes — indexer uniquement ce qui est requêté
```sql
CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'pending';
CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;
```

### Covering Indexes — éviter les heap fetches
```sql
CREATE INDEX idx_orders_covering ON orders (status) INCLUDE (created_at, total_amount);
```

### BRIN Indexes — pour données séquentielles (logs, time-series)
```sql
-- ~100 KB vs ~2 GB pour un B-tree sur 100M lignes
CREATE INDEX idx_logs_brin ON logs USING BRIN (log_date);
```
Uniquement si la colonne corrèle avec l'ordre d'insertion physique.

### GIN Indexes — JSONB, arrays, full-text
```sql
-- jsonb_path_ops = 2-3x plus petit, supporte @> uniquement
CREATE INDEX idx_doc_data ON documents USING GIN (data jsonb_path_ops);
CREATE INDEX idx_tags ON products USING GIN (tags);
CREATE INDEX idx_fts ON articles USING GIN (to_tsvector('french', title || ' ' || body));
```

### Expression Indexes
```sql
CREATE INDEX idx_lower_email ON users (lower(email));
-- Requête : WHERE lower(email) = 'user@example.com'
```

### Composite — l'ordre compte
```sql
-- Colonne filtrée en premier, triée en second
CREATE INDEX idx_orders_status_date ON orders (status, created_at DESC);
```

### Détecter les indexes inutilisés
```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes WHERE idx_scan = 0 ORDER BY tablename;
-- DROP INDEX CONCURRENTLY idx_unused;
```

## 2. EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE, FORMAT JSON) SELECT ...;
```
Coller le JSON dans explain.dalibo.com pour visualiser.

| Signal | Problème | Fix |
|--------|----------|-----|
| `Seq Scan` sur grosse table | Index manquant | Ajouter index |
| Estimated << Actual rows | Stats obsolètes | `ANALYZE table_name;` |
| `Sort Method: external merge Disk` | `work_mem` trop bas | Augmenter par session |
| Nested Loop sur gros sets | Mauvais plan | Tester `SET enable_nestloop = off;` |

### Corriger les estimations
```sql
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ANALYZE orders;
```

## 3. Partitioning

### Quand partitionner
- Table > 100 GB ou dizaines de millions de lignes
- Requêtes filtrent toujours sur une dimension (date, tenant)
- Besoin de supprimer des anciennes données rapidement

### Range (le plus courant — time-series)
```sql
CREATE TABLE orders (...) PARTITION BY RANGE (created_at);
CREATE TABLE orders_2026_q1 PARTITION OF orders FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');
```

### Suppression rapide de données
```sql
-- Au lieu de DELETE FROM orders WHERE created_at < '2025-01-01' (lent, WAL)
ALTER TABLE orders DETACH PARTITION orders_2024_q4;
DROP TABLE orders_2024_q4; -- instantané
```

### Règle critique
Le `WHERE` doit TOUJOURS contenir la partition key sinon scan de TOUTES les partitions.

## 4. Materialized Views

```sql
CREATE MATERIALIZED VIEW mv_customer_stats AS
SELECT customer_id, COUNT(*) AS total_orders, SUM(total) AS lifetime_value
FROM orders GROUP BY customer_id
WITH DATA;

CREATE UNIQUE INDEX ON mv_customer_stats (customer_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_customer_stats;
```

| Cas | Utiliser |
|-----|---------|
| Agrégation complexe, tolère du stale | Materialized View |
| Requête one-shot, récursion | CTE |
| Données temps réel | Vue classique ou inline |

## 5. Bulk operations

### COPY — insert le plus rapide
```sql
COPY orders (customer_id, total, created_at) FROM '/tmp/orders.csv' WITH (FORMAT csv, HEADER true);
```

### Upsert
```sql
INSERT INTO products (sku, name, price)
VALUES ('ABC', 'Widget', 9.99)
ON CONFLICT (sku) DO UPDATE SET price = EXCLUDED.price
WHERE products.price <> EXCLUDED.price;
```

### Bulk UPDATE via staging
```sql
CREATE TEMP TABLE price_updates (sku TEXT, new_price DECIMAL);
COPY price_updates FROM '/tmp/prices.csv' WITH (FORMAT csv);
UPDATE products p SET price = pu.new_price FROM price_updates pu WHERE p.sku = pu.sku AND p.price <> pu.new_price;
DROP TABLE price_updates;
```

### Batch large UPDATE par range d'ID
```sql
-- Éviter les transactions longues sur millions de lignes
-- Batcher par tranches de 10 000
UPDATE orders SET status = 'archived'
WHERE id > $last_id AND id <= $last_id + 10000 AND created_at < '2024-01-01';
```

## 6. Window functions > sous-requêtes

```sql
-- INTERDIT : sous-requête corrélée (N+1)
SELECT o.*, (SELECT SUM(total) FROM orders o2 WHERE o2.customer_id = o.customer_id) FROM orders o;

-- CORRECT : window function (un seul pass)
SELECT o.*, SUM(total) OVER (PARTITION BY customer_id) AS cust_total FROM orders o;

-- Dernière commande par client
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders
) ranked WHERE rn = 1;
```

## 7. JSONB

```sql
-- Index pour @>
CREATE INDEX idx_data ON events USING GIN (data jsonb_path_ops);
-- WHERE data @> '{"status": "active"}'

-- Champs chauds → colonnes générées
ALTER TABLE events ADD COLUMN status TEXT GENERATED ALWAYS AS (data->>'status') STORED;
CREATE INDEX ON events (status) WHERE status = 'active';
```

Éviter `jsonb_set()` en boucle — chaque update réécrit le document entier.

## 8. Locks et concurrence

```sql
-- File d'attente sans blocage entre workers
SELECT id, payload FROM job_queue WHERE status = 'pending'
ORDER BY created_at LIMIT 10 FOR UPDATE SKIP LOCKED;

-- Optimistic locking
UPDATE products SET price = 19.99, version = version + 1
WHERE id = 1 AND version = 3; -- 0 rows = conflit → retry
```

- `SET statement_timeout = '30s';`
- `SET idle_in_transaction_session_timeout = '60s';`
- Transactions longues = bloquent autovacuum = bloat

## 9. Vacuum et bloat

```sql
-- Vérifier les dead tuples
SELECT relname, n_live_tup, n_dead_tup,
  round(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_pct
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
```

### Tuning autovacuum pour tables à fort trafic
```sql
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- 1% au lieu de 20% par défaut
  autovacuum_vacuum_threshold = 1000,
  autovacuum_vacuum_cost_delay = 2
);
```

### postgresql.conf pour 200+ tables
```ini
autovacuum_max_workers = 5
autovacuum_naptime = 30s
autovacuum_vacuum_cost_delay = 2ms
```
