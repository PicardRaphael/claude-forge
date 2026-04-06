---
name: api-conventions
description: Neoteem REST API conventions reference. Use when user says 'conventions API', 'comment nommer un endpoint', 'API naming', 'pagination format', 'HTTP status codes', 'crée un endpoint', 'route Hono', 'schéma Zod request/response', 'create a route'.
effort: high
---

# Conventions API REST

## URLs
- Ressources en kebab-case pluriel : `/api/appels-de-fonds`
- Relations via nesting max 2 niveaux : `/api/coproprietes/:id/lots`
- Actions non-CRUD : verbe dans le path `/api/exercices/:id/cloturer`

## Pagination (toutes les listes)
```
GET /api/coproprietes?page=1&limit=20&sort=nom&order=asc

Réponse :
{ "data": [...], "pagination": { "page": 1, "limit": 20, "total": 156, "totalPages": 8 } }
```

Utiliser `PaginationQuerySchema` et `PaginatedSchema()` de `@shared/schemas`.

## Réponses
- Objet unique → retourner directement l'objet (pas d'enveloppe `data`)
- Liste → `{ "data": [...], "pagination": {...} }`
- Erreur → `{ "error": { "code": "SCREAMING_SNAKE_CASE", "message": "Texte français" } }`

## Codes HTTP
200 = Succès lecture/modification · 201 = Création · 204 = Suppression
400 = Requête invalide · 401 = Non authentifié · 403 = Non autorisé
404 = Non trouvé · 409 = Conflit · 422 = Règle métier violée · 500 = Erreur interne

## Auth V1
API Key dans header : `Authorization: Bearer <API_KEY>`

## Schéma-first
Chaque endpoint DOIT utiliser `createRoute()` de `@hono/zod-openapi`.
Les schémas Zod partagés sont dans `src/shared/schemas/`.
Utiliser `z.infer<typeof Schema>` pour dériver les types — pas de types manuels.

## Nommage fichiers
```
routes/queries/[entites].query.ts      → GET endpoints d'un module
routes/commands/[entites].command.ts   → POST/PUT/DELETE d'un module
```
