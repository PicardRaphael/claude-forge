---
name: schema-data-source
description: Guide to read PostgreSQL schema structure via MCP (preferred) or CSV fallback (doc/dump/), and functions from the SQL repo. Structure only, no data.
user-invokable: false
---

# Sources de données

## Source 1 — Structure des tables

### Mode A : MCP PostgreSQL (préféré)

Si un MCP PostgreSQL est configuré, l'utiliser pour récupérer la **structure uniquement** (pas de données).

**Détection :** chercher les outils MCP contenant `postgres`, `query`, `sql`, `execute` dans la session.

**Serveurs connus :**

| Serveur | Outil requête |
|---------|--------------|
| `@modelcontextprotocol/server-postgres` | `query` |
| `crystaldba/postgres-mcp` | `execute SQL` |
| `sgaunet/postgresql-mcp` | `execute_query` |

**RÈGLE : STRUCTURE UNIQUEMENT. Jamais SELECT sur les données. Uniquement `information_schema` et `pg_catalog`.**

**Requêtes autorisées (dans cet ordre progressif) :**

Phase 1 — Vue d'ensemble :
```sql
-- Schémas
SELECT schema_name FROM information_schema.schemata
WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
ORDER BY schema_name;

-- Tables
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
AND table_type = 'BASE TABLE' ORDER BY table_schema, table_name;
```

Phase 2 — Relations :
```sql
-- Foreign keys
SELECT tc.table_schema AS source_schema, tc.table_name AS source_table,
  kcu.column_name AS source_column, ccu.table_schema AS target_schema,
  ccu.table_name AS target_table, ccu.column_name AS target_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
  ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' ORDER BY tc.table_name;
```

Phase 3 — Colonnes (PAR CLUSTER, jamais tout d'un coup) :
```sql
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = '{schema}' AND table_name IN ('{table1}', '{table2}')
ORDER BY table_name, ordinal_position;
```

Phase 4 — Indexes et triggers :
```sql
-- Indexes uniques
SELECT n.nspname AS schema_name, t.relname AS table_name, i.relname AS index_name,
  array_to_string(array_agg(a.attname ORDER BY k.n), ',') AS columns, ix.indisunique
FROM pg_index ix
JOIN pg_class t ON t.oid = ix.indrelid
JOIN pg_class i ON i.oid = ix.indexrelid
JOIN pg_namespace n ON n.oid = t.relnamespace
CROSS JOIN LATERAL unnest(ix.indkey) WITH ORDINALITY AS k(attnum, n)
JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = k.attnum
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND ix.indisunique = true AND NOT ix.indisprimary
GROUP BY n.nspname, t.relname, i.relname, ix.indisunique ORDER BY t.relname;

-- Triggers
SELECT trigger_schema, trigger_name, event_manipulation AS event,
  event_object_schema AS table_schema, event_object_table AS table_name,
  action_timing AS timing, action_statement
FROM information_schema.triggers ORDER BY event_object_table;
```

**Requêtes avancées (à la demande) :**

```sql
-- Tables les plus référencées
SELECT ccu.table_name, COUNT(*) as fk_entrantes
FROM information_schema.table_constraints tc
JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
GROUP BY ccu.table_name ORDER BY fk_entrantes DESC LIMIT 20;

-- Colonnes notables (soft-delete, status, montants)
SELECT table_name, column_name, data_type FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema') AND (
  column_name IN ('deleted_at', 'archived_at', 'active', 'is_deleted', 'is_active')
  OR column_name LIKE '%status%' OR column_name LIKE '%state%'
  OR (data_type IN ('numeric', 'decimal', 'money')
    AND (column_name LIKE '%price%' OR column_name LIKE '%amount%'
      OR column_name LIKE '%total%' OR column_name LIKE '%montant%'))
) ORDER BY table_name;
```

**INTERDIT via MCP :**
- SELECT sur les données des tables (SELECT * FROM coproprietes)
- INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE
- Toute requête hors information_schema / pg_catalog

### Mode B : CSV (fallback sans MCP)

Si pas de MCP → utiliser les fichiers CSV dans `doc/dump/`.
Exportés via `scripts/export-schema.sh`.

| Fichier | Contenu | Colonnes |
|---------|---------|----------|
| `schemas.csv` | Schémas | schema_name |
| `tables.csv` | Tables | table_schema, table_name |
| `fk.csv` | Foreign keys | source_schema, source_table, source_column, target_schema, target_table, target_column |
| `columns.csv` | Colonnes | table_schema, table_name, column_name, data_type, is_nullable, column_default, ordinal_position |
| `indexes.csv` | Indexes uniques | schema_name, table_name, index_name, columns, is_unique |
| `triggers.csv` | Triggers → tables | trigger_schema, trigger_name, event, table_schema, table_name, timing, action_statement |

**Ne JAMAIS lire `columns.csv` en entier.** Grep par cluster.

### Détection automatique du mode

1. Chercher les outils MCP PostgreSQL dans la session
2. Si trouvé → Mode A (MCP)
3. Si pas trouvé → vérifier si `doc/dump/` existe → Mode B (CSV)
4. Si ni MCP ni CSV → STOP et afficher les instructions ci-dessous

## Source 2 — Fonctions (repo SQL séparé)

Le chemin du repo est dans CLAUDE.md. Structure :

```
repo-functions/
  {schema}/              ← un dossier par schéma PostgreSQL
    f_*.sql              ← lecture (SELECT)
    p_*.sql              ← écriture (INSERT/UPDATE/DELETE)
    proc_*.sql           ← procédures stockées
    tr_*.sql             ← fonctions de trigger
```

**Les dossiers = les schémas PostgreSQL = des domaines métier potentiels.**

## Conventions de nommage

| Préfixe | Rôle | Opérations typiques |
|---------|------|---------------------|
| `f_*` | Lecture | SELECT, RETURN QUERY |
| `p_*` | Écriture | INSERT, UPDATE, DELETE |
| `proc_*` | Procédure | Orchestration, multi-étapes |
| `tr_*` | Trigger | BEFORE/AFTER sur événements table |

## Stratégie de lecture

### Tables (MCP ou CSV)

**Ne JAMAIS récupérer toutes les colonnes d'un coup.**

Ordre :
1. Schémas → vue d'ensemble
2. Tables → liste complète
3. FK → graphe de relations
4. Triggers → mapping trigger → table
5. Indexes → contraintes
6. Colonnes → PAR CLUSTER uniquement

### Fonctions (repo)

1. Glob `{repo}/**/*.sql` → inventaire
2. Compter par dossier/convention → stats
3. Lire le source par domaine en cours d'analyse

### Dépendances entre fonctions

- Appels : `Grep pattern="f_\w+|p_\w+|proc_\w+" path="{fichier}.sql"`
- Tables : `Grep pattern="FROM\s+\w+|JOIN\s+\w+|INTO\s+\w+|UPDATE\s+\w+" path="{fichier}.sql"`

## Si rien n'est disponible

STOP et afficher :

```
Pas de MCP PostgreSQL ni de fichiers CSV dans doc/dump/.

Option 1 — MCP (recommandé) :
Configurer .mcp.json à la racine du projet :
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${POSTGRES_URL}" }
    }
  }
}

Option 2 — Export CSV (si pas de MCP possible) :
  cp .claude/skills/schema-data-source/scripts/export-schema.sh .
  chmod +x export-schema.sh
  ./export-schema.sh "postgresql://USER:PASS@HOST:5432/DB"

Les fonctions sont lues depuis le repo SQL.
Précisez le chemin : "le repo des fonctions est à /path/to/repo"
```
