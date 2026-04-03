#!/bin/bash
# =============================================================================
# export-schema.sh — Exporte les TABLES PostgreSQL en fichiers CSV
# Les fonctions sont dans un repo séparé, pas besoin de les exporter.
# Usage : ./export-schema.sh <connection_string>
# =============================================================================

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <postgresql_connection_string>"
    echo "Exemple: $0 \"postgresql://user:pass@host:5432/mydb\""
    exit 1
fi

DB_URL="$1"
OUTPUT_DIR="doc/dump"

mkdir -p "$OUTPUT_DIR"

echo "=== Export des tables PostgreSQL ==="
echo "Destination : $OUTPUT_DIR/"

# ─── 1. Schémas ───
echo "[1/6] Schémas..."
psql "$DB_URL" -c "COPY (
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
    ORDER BY schema_name
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/schemas.csv"
NB_SCH=$(tail -n +2 "$OUTPUT_DIR/schemas.csv" | wc -l)
echo "    $NB_SCH schémas"

# ─── 2. Tables ───
echo "[2/6] Tables..."
psql "$DB_URL" -c "COPY (
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
      AND table_type = 'BASE TABLE'
    ORDER BY table_schema, table_name
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/tables.csv"
NB_TABLES=$(tail -n +2 "$OUTPUT_DIR/tables.csv" | wc -l)
echo "    $NB_TABLES tables"

# ─── 3. Foreign keys ───
echo "[3/6] Foreign keys..."
psql "$DB_URL" -c "COPY (
    SELECT
        tc.table_schema AS source_schema,
        tc.table_name AS source_table,
        kcu.column_name AS source_column,
        ccu.table_schema AS target_schema,
        ccu.table_name AS target_table,
        ccu.column_name AS target_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = tc.constraint_name
        AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY'
    ORDER BY tc.table_name, kcu.column_name
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/fk.csv"
NB_FK=$(tail -n +2 "$OUTPUT_DIR/fk.csv" | wc -l)
echo "    $NB_FK foreign keys"

# ─── 4. Colonnes ───
echo "[4/6] Colonnes..."
psql "$DB_URL" -c "COPY (
    SELECT table_schema, table_name, column_name, data_type,
           is_nullable, column_default, ordinal_position
    FROM information_schema.columns
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name, ordinal_position
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/columns.csv"
NB_COLS=$(tail -n +2 "$OUTPUT_DIR/columns.csv" | wc -l)
echo "    $NB_COLS colonnes"

# ─── 5. Indexes uniques ───
echo "[5/6] Indexes uniques..."
psql "$DB_URL" -c "COPY (
    SELECT
        n.nspname AS schema_name,
        t.relname AS table_name,
        i.relname AS index_name,
        array_to_string(array_agg(a.attname ORDER BY k.n), ',') AS columns,
        ix.indisunique AS is_unique
    FROM pg_index ix
    JOIN pg_class t ON t.oid = ix.indrelid
    JOIN pg_class i ON i.oid = ix.indexrelid
    JOIN pg_namespace n ON n.oid = t.relnamespace
    CROSS JOIN LATERAL unnest(ix.indkey) WITH ORDINALITY AS k(attnum, n)
    JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = k.attnum
    WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
      AND ix.indisunique = true
      AND NOT ix.indisprimary
    GROUP BY n.nspname, t.relname, i.relname, ix.indisunique
    ORDER BY t.relname
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/indexes.csv"
NB_IDX=$(tail -n +2 "$OUTPUT_DIR/indexes.csv" | wc -l)
echo "    $NB_IDX indexes uniques"

# ─── 6. Triggers ───
echo "[6/6] Triggers..."
psql "$DB_URL" -c "COPY (
    SELECT
        trigger_schema,
        trigger_name,
        event_manipulation AS event,
        event_object_schema AS table_schema,
        event_object_table AS table_name,
        action_timing AS timing,
        action_statement
    FROM information_schema.triggers
    ORDER BY event_object_table, trigger_name
) TO STDOUT CSV HEADER" > "$OUTPUT_DIR/triggers.csv"
NB_TR=$(tail -n +2 "$OUTPUT_DIR/triggers.csv" | wc -l)
echo "    $NB_TR triggers"

echo ""
echo "=== DONE ==="
echo "Schemas: $NB_SCH | Tables: $NB_TABLES | FK: $NB_FK | Colonnes: $NB_COLS | Indexes: $NB_IDX | Triggers: $NB_TR"
echo ""
ls -lh "$OUTPUT_DIR/"
echo ""
echo "Note : les fonctions sont lues directement depuis le repo, pas besoin de les exporter."
echo "Prochaine étape : demander à Claude 'Analyse ma BDD avec ton agent schema-mapper'"
