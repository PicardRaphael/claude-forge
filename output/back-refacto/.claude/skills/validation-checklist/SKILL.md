---
name: validation-checklist
description: Checklist for validating a migrated PostgreSQL function — behavioral equivalence, edge cases, error handling. Load when validating or reviewing a completed migration.
user-invokable: true
argument-hint: "[function name or endpoint to validate]"
---

# Migration Validation Checklist

Goal: ensure the new TypeScript endpoint is **behaviorally equivalent** to the original PostgreSQL function.

## 1. Input/Output equivalence

- [ ] Same required parameters
- [ ] Same optional parameters with same defaults
- [ ] Same output shape (field names, types, nullability)
- [ ] Same pagination behavior (if applicable)
- [ ] Same ordering (if the PG function had ORDER BY)

## 2. Business rules

- [ ] All business rules from the PG function are implemented in the use case
- [ ] Each business rule is covered by a unit test
- [ ] Rule violations throw the correct typed `DomainError` subclass
- [ ] Error codes match the expected HTTP status (404 / 400 / 409 / 422)

## 3. Edge cases

- [ ] Empty result set returns `[]` not `null`
- [ ] Not found returns 404 with typed error, not 500
- [ ] Invalid input caught by Zod validation (400), not reaching the use case
- [ ] NULL DB values handled explicitly (not silently converted to `undefined`)
- [ ] Numeric overflow / division by zero cases handled

## 4. Data mapping

- [ ] All DB columns are mapped to domain entity fields
- [ ] snake_case → camelCase conversion is complete
- [ ] No DB column leaks into the API response
- [ ] Dates are serialized consistently (ISO 8601 string)
- [ ] Decimal/numeric columns use appropriate TypeScript type (string or number)

## 5. Tests

- [ ] Unit test: nominal case (success path)
- [ ] Unit test: not found error
- [ ] Unit test: business rule violation(s)
- [ ] Unit test: invalid input
- [ ] All tests pass: `bun test --filter "[UseCaseName]"`

## 6. Types

- [ ] No `any` types in use case, repository, or mapper
- [ ] `bun run typecheck` passes with zero errors
- [ ] Repository interface updated if new methods added

## 7. API contract

- [ ] Route registered in `src/api/routes/index.ts`
- [ ] OpenAPI spec auto-generates (`GET /openapi.json`)
- [ ] Request schema (Zod) validates all inputs
- [ ] Response schema (Zod) matches actual output shape
- [ ] HTTP method and path follow REST conventions (see `doc/api-design.md`)

## 8. Final verification

```bash
bun run typecheck       # Zero type errors
bun run test            # All tests pass
bun run dev             # Server starts without errors
curl localhost:3000/api/[endpoint]  # Returns expected data
```

## Behavioral equivalence matrix

When uncertain if behavior matches, test both old (via direct DB call) and new (via API) with the same inputs:

```sql
-- Old: call PG function directly
SELECT * FROM f_get_copropriete('123');

-- New: call API
-- GET /api/coproprietes/123
-- → Compare field by field
```
