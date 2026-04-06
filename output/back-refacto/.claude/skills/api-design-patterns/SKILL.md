---
name: api-design-patterns
description: REST API design patterns for this project — routes, HTTP codes, pagination format, error format, authentication, OpenAPI. Load when designing or reviewing API endpoints.
user-invokable: false
---

# API Design Patterns

Full documentation: `doc/api-design.md`

## URL design rules

```
GET    /api/coproprietes              # List (paginated)
GET    /api/coproprietes/:id          # Single resource
GET    /api/coproprietes/:id/lots     # Sub-resource (max 2 levels)
GET    /api/coproprietes/:id/solde    # Computed value

POST   /api/appels-de-fonds          # Create
PUT    /api/appels-de-fonds/:id      # Full update
PATCH  /api/appels-de-fonds/:id      # Partial update
DELETE /api/appels-de-fonds/:id      # Delete

POST   /api/exercices/:id/cloturer   # Non-CRUD action (verb in path)
```

- Resource names: **kebab-case, plural** — `/appels-de-fonds`, NOT `/appelDeFonds`
- Maximum 2 nesting levels
- Verbs in path only for non-CRUD actions

## HTTP status codes

| Code | Usage |
|------|-------|
| 200 | Success (read, update) |
| 201 | Created |
| 204 | Deleted (no body) |
| 400 | Validation error (Zod) |
| 401 | Missing or invalid API key |
| 403 | Authenticated but not permitted |
| 404 | Resource not found |
| 409 | Conflict (duplicate, inconsistent state) |
| 422 | Business rule violated |
| 500 | Unexpected internal error |

## Response format

### Single resource (no envelope)
```json
{
  "id": "abc-123",
  "nom": "Les Alpes",
  "adresse": "30 chemin du Vieux Chêne"
}
```

### Paginated list (with envelope)
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "totalPages": 8
  }
}
```

### Error (all errors)
```json
{
  "error": {
    "code": "COPROPRIETE_NOT_FOUND",
    "message": "Copropriété abc-123 introuvable"
  }
}
```

## Pagination schema (shared)

```typescript
// src/shared/schemas/pagination.schema.ts
export const PaginationQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.string().optional(),
  order: z.enum(["asc", "desc"]).default("asc"),
});
```

Always use `z.coerce.number()` for query params — HTTP sends strings.

## Route structure (Hono + OpenAPI)

```typescript
// src/api/routes/queries/coproprietes.query.ts
export const createCoproprieteRoutes = (useCase: GetCoproprieteUseCase) => {
  const router = new OpenAPIHono();

  const route = createRoute({
    method: "get",
    path: "/coproprietes/{id}",
    tags: ["Copropriétés"],
    summary: "Fetch a single copropriété",
    request: {
      params: z.object({ id: z.string().uuid() }),
    },
    responses: {
      200: {
        content: { "application/json": { schema: CoproprieteSchema } },
        description: "Copropriété found",
      },
      404: { description: "Not found" },
    },
  });

  router.openapi(route, async (c) => {
    const { id } = c.req.valid("param");
    const result = await useCase.execute(id);
    return c.json(result, 200);
  });

  return router;
};
```

## Authentication

```
Authorization: Bearer <API_KEY>
```

API key is validated by `src/api/middleware/auth.ts`.
All routes require auth by default in V1.

## OpenAPI spec

Auto-generated at `GET /openapi.json` by `@hono/zod-openapi`.
The Zod schema IS the documentation — keep it accurate.

## What NEVER goes in a route

- Business logic
- Direct DB calls
- Imports from `drizzle-orm` or `@infra/`
- Try/catch for domain errors (the error-handler middleware handles these)
