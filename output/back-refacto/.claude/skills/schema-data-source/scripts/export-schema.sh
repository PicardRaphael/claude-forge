#!/usr/bin/env bash
# export-schema.sh — Export PostgreSQL schema to CSV files in doc/dump/
# Usage: .claude/skills/schema-data-source/scripts/export-schema.sh
#
# Requires: psql and DATABASE_URL environment variable (or .env file)
# Output: doc/dump/<table_name>.csv for each table in public schema

set -euo pipefail

# Load .env if present
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ -z "${DATABASE_URL:-}" ]; then
  echo "ERROR: DATABASE_URL is not set. Set it in .env or as an environment variable."
  exit 1
fi

OUTPUT_DIR="doc/dump"
mkdir -p "$OUTPUT_DIR"

echo "Exporting schema from: $DATABASE_URL"
echo "Output directory: $OUTPUT_DIR"

# Get list of tables
TABLES=$(psql "$DATABASE_URL" -t -c "
  SELECT table_name
  FROM information_schema.tables
  WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
  ORDER BY table_name;
" | tr -d ' ' | grep -v '^$')

COUNT=0
for TABLE in $TABLES; do
  OUTPUT_FILE="$OUTPUT_DIR/${TABLE}.csv"

  psql "$DATABASE_URL" -c "
    COPY (
      SELECT
        column_name,
        data_type,
        is_nullable,
        column_default,
        character_maximum_length,
        numeric_precision,
        numeric_scale
      FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = '${TABLE}'
      ORDER BY ordinal_position
    ) TO STDOUT WITH CSV HEADER;
  " > "$OUTPUT_FILE"

  echo "  ✓ $TABLE → $OUTPUT_FILE"
  COUNT=$((COUNT + 1))
done

echo ""
echo "Done. Exported $COUNT tables to $OUTPUT_DIR/"
echo ""
echo "To read a table schema:"
echo "  cat doc/dump/<table_name>.csv"
