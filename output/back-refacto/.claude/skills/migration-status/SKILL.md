---
name: migration-status
description: Track PostgreSQL function migration progress to Drizzle/TypeScript. Load when user asks about migration status, what has been migrated, what remains, or to update the tracker after completing a migration.
user-invokable: true
argument-hint: "[domain or function name to check/update]"
---

# Migration Status Tracker

## Tracker file

All migration progress is tracked in `doc/migration-tracker.md`.

**Rule 10 from CLAUDE.md:** Update `doc/migration-tracker.md` after EVERY completed migration.

## How to read the tracker

```markdown
## Domain: Copropriétés
| Function | Status | Notes |
|---|---|---|
| f_get_copropriete | ✅ migrated | GET /api/coproprietes/:id |
| f_list_coproprietes | ✅ migrated | GET /api/coproprietes |
| p_create_copropriete | 🔄 in progress | |
| f_get_solde | ⏳ pending | Depends on comptes domain |
```

**Status codes:**
- ✅ migrated — endpoint exists, tested, functional
- 🔄 in progress — currently being worked on
- ⏳ pending — not started
- ❌ blocked — dependency issue, document the blocker
- 🚫 skip — not needed (internal function, trigger, etc.)

## After completing a migration

1. Update `doc/migration-tracker.md` — change status to ✅
2. Add the API route path in the Notes column
3. If business rules were discovered, add them to project memory

## Migration checklist (per function)

- [ ] Read the PostgreSQL function source (in pg-functions repo — READ ONLY)
- [ ] Identify inputs, outputs, business rules
- [ ] Create domain entity / value objects if needed
- [ ] Create typed errors for each failure mode
- [ ] Create use case with `execute()` method
- [ ] Write unit tests (mock repository)
- [ ] Create Drizzle mapper
- [ ] Create repository implementation
- [ ] Create Hono route with Zod schemas
- [ ] Verify behavioral equivalence (same inputs → same outputs)
- [ ] Update migration-tracker.md

## Domain groupings

Organize migration by domain to maximize coherence:

| Domain | Key tables | Key functions |
|---|---|---|
| Copropriétés | coproprietes, syndicats | f_get_copropriete, f_list_coproprietes |
| Lots & tantièmes | lots, tantiemes | f_get_lots_copropriete, f_calcul_tantiemes |
| Comptabilité | comptes, ecritures | f_get_solde, f_list_ecritures |
| Appels de fonds | appels_de_fonds | f_list_appels, p_create_appel |
| Copropriétaires | coproprietaires | f_get_coproprietaires_lot |

## Progress summary format

When asked for a status update, produce this format:

```
Migration progress: X/Y functions (Z%)

✅ Migrated (X):
  - domain: function → endpoint

🔄 In progress (X):
  - domain: function

⏳ Pending (X):
  - domain: function (blocker if any)
```
