---
name: schema-output-format
description: Templates and format conventions for schema-mapper generated files in doc/schemas/. Load when creating or updating schema documentation, or when running schema-mapper.
user-invokable: false
---

# Schema Output Format

## File location

Schema documentation lives in `doc/schemas/`.
One Markdown file per domain (not per table).

```
doc/schemas/
├── coproprietes.md
├── lots-tantiemes.md
├── comptabilite.md
├── coproprietaires.md
└── ...
```

## File template

```markdown
# [Domain Name] — Schema

_Generated: YYYY-MM-DD_

## Tables

### [table_name]

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | integer | NO | nextval(...) | Primary key |
| nom | varchar(255) | NO | | Display name |
| syndic_id | integer | YES | | FK → syndicats.id |
| created_at | timestamp | YES | now() | |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE: `(nom, syndic_id)`
- INDEX: `syndic_id` (FK index)

**Foreign keys:**
- `syndic_id` → `syndicats(id)` ON DELETE SET NULL

---

### [second_table_name]

...

## Relationships

```
coproprietes 1──N lots
coproprietes 1──N appels_de_fonds
coproprietes N──1 syndicats
```

## Key PostgreSQL functions for this domain

| Function | Type | Description |
|----------|------|-------------|
| `f_get_copropriete(id)` | f_* (read) | Fetch single copropriété with computed fields |
| `f_list_coproprietes()` | f_* (read) | Paginated list |
| `p_create_copropriete(...)` | p_* (write) | Create with validation |

## Migration status

| Function | Migrated | API endpoint |
|---|---|---|
| `f_get_copropriete` | ✅ | `GET /api/coproprietes/:id` |
| `f_list_coproprietes` | ✅ | `GET /api/coproprietes` |
| `p_create_copropriete` | ⏳ | — |
```

## Rules for schema-mapper output

1. **One file per domain** — group related tables, not one file per table
2. **Always include**: columns, types, nullability, foreign keys, indexes
3. **Include migration status** for all `f_*` and `p_*` functions
4. **Note computed fields** — fields that PG functions add that don't exist as columns
5. **Note enum values** — if a column is `varchar` used as enum, list the allowed values
6. **Note conventions** — e.g., soft-delete via `deleted_at`, status codes in `etat`

## Updating schema docs

When `bun run db:pull` updates the Drizzle schema, also update the relevant `doc/schemas/*.md`.
When a migration is completed, update the migration status table.
