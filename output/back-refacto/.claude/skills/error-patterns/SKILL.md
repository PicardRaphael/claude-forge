---
name: error-patterns
description: Error handling patterns for this project — DomainError hierarchy, PostgreSQL error codes to HTTP status mapping, Zod validation errors. Load when creating new errors or handling error cases.
user-invokable: false
---

# Error Handling Patterns

See full documentation: `doc/error-handling.md`

## Class hierarchy

```
DomainError (abstract, src/core/domain/errors/base.error.ts)
├── NotFoundError          → HTTP 404
├── ValidationError        → HTTP 400
├── BusinessRuleError      → HTTP 422
├── ConflictError          → HTTP 409
└── ForbiddenError         → HTTP 403
```

## Creating a new error

```typescript
// src/core/domain/errors/[name].error.ts
import { NotFoundError } from "./not-found.error";

export class CoproprieteNotFoundError extends NotFoundError {
  readonly code = "COPROPRIETE_NOT_FOUND";  // SCREAMING_SNAKE_CASE, English

  constructor(id: string) {
    super(`Copropriété ${id} introuvable`);  // Message in French (for humans/logs)
  }
}
```

## HTTP status mapping

| DomainError subclass | HTTP | When to use |
|---|---|---|
| `NotFoundError` | 404 | Entity does not exist |
| `ValidationError` | 400 | Input fails a domain validation rule |
| `BusinessRuleError` | 422 | Business rule violated (entity exists, rule says no) |
| `ConflictError` | 409 | Duplicate / state conflict |
| `ForbiddenError` | 403 | Action not permitted for current actor |

Zod validation errors → 400 (handled automatically by error-handler middleware)
Unhandled errors → 500 (no details exposed to client)

## PostgreSQL error codes → DomainError

| PG code | Meaning | Map to |
|---|---|---|
| `23505` | unique_violation | `ConflictError` (409) |
| `23503` | foreign_key_violation | `NotFoundError` (404) or `BusinessRuleError` (422) |
| `23514` | check_violation | `BusinessRuleError` (422) |
| `22003` | numeric_value_out_of_range | `ValidationError` (400) |
| `P0001` | raise_exception (custom) | Parse the message → appropriate DomainError |

Example — catching a PG unique violation in a repository:
```typescript
import { DatabaseError } from "pg";

async save(entity: Copropriete): Promise<void> {
  try {
    await db.insert(coproprietes).values(toRow(entity));
  } catch (err) {
    if (err instanceof DatabaseError && err.code === "23505") {
      throw new DoublonCoproprieteError(entity.id);
    }
    throw err; // Re-throw unknown errors
  }
}
```

## Error response format

```json
{
  "error": {
    "code": "COPROPRIETE_NOT_FOUND",
    "message": "Copropriété abc-123 introuvable"
  }
}
```

For Zod validation errors (400), the response includes `details`:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Données invalides",
    "details": [
      { "path": "montant", "message": "Le montant doit être positif" }
    ]
  }
}
```

## Rules

- NEVER `throw new Error("message")` — always a typed class
- NEVER catch and swallow errors silently
- NEVER expose stack traces or internal DB errors to the API client
- The `code` is stable (machine-readable) — the `message` can change
- Each error class has at least one unit test
