# API Design — Conventions REST

## Principes

Cette API est consommée par un agent IA (Python/LangGraph) puis un frontend.
Elle doit être **prévisible, bien documentée (OpenAPI), et explicite dans ses erreurs**.

## URL Design

```
GET    /api/coproprietes                    # Lister
GET    /api/coproprietes/:id                # Détail
GET    /api/coproprietes/:id/lots           # Sous-ressource
GET    /api/coproprietes/:id/solde          # Donnée calculée

POST   /api/appels-de-fonds                 # Créer
PUT    /api/appels-de-fonds/:id             # Modifier entièrement
PATCH  /api/appels-de-fonds/:id             # Modifier partiellement
DELETE /api/appels-de-fonds/:id             # Supprimer
```

**Règles :**
- Noms de ressource en **kebab-case pluriel** : `/appels-de-fonds`, pas `/appelDeFonds`
- Relations via nesting : `/coproprietes/:id/lots`
- Maximum 2 niveaux de nesting : pas `/coproprietes/:id/lots/:lid/charges`
- Verbes dans le path SEULEMENT pour les actions non-CRUD : `/api/exercices/:id/cloturer`

## Pagination

Toutes les listes sont paginées par défaut.

```
GET /api/coproprietes?page=1&limit=20&sort=nom&order=asc
```

**Réponse :**
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

**Schéma Zod partagé :**
```typescript
// src/shared/schemas/pagination.schema.ts
export const PaginationQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.string().optional(),
  order: z.enum(["asc", "desc"]).default("asc"),
});

export function PaginatedSchema<T extends z.ZodTypeAny>(itemSchema: T) {
  return z.object({
    data: z.array(itemSchema),
    pagination: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
      totalPages: z.number(),
    }),
  });
}
```

## Format de réponse

### Succès

```json
// Objet unique
{
  "id": "abc-123",
  "nom": "Les Alpes",
  "adresse": "30 chemin du Vieux Chêne"
}

// Liste paginée
{
  "data": [...],
  "pagination": { ... }
}
```

Pas d'enveloppe `{ "data": ... }` pour les objets uniques — directement l'objet.
L'enveloppe `data` est réservée aux listes paginées.

### Erreur

```json
{
  "error": {
    "code": "COPROPRIETE_NOT_FOUND",
    "message": "Copropriété abc-123 introuvable"
  }
}
```

**Toujours :**
- `code` : identifiant machine en SCREAMING_SNAKE_CASE
- `message` : texte humain en français

Le code d'erreur permet à l'agent IA de réagir programmatiquement.
Le message est pour les logs et le debug.

### Codes HTTP utilisés

| Code | Usage |
|------|-------|
| 200 | Succès lecture / modification |
| 201 | Création réussie |
| 204 | Suppression réussie (pas de body) |
| 400 | Requête invalide (validation Zod) |
| 401 | Non authentifié |
| 403 | Non autorisé |
| 404 | Ressource introuvable |
| 409 | Conflit (doublon, état incohérent) |
| 422 | Erreur métier (règle de gestion violée) |
| 500 | Erreur interne inattendue |

## Authentification

V1 : API Key simple dans le header.

```
Authorization: Bearer <API_KEY>
```

```typescript
// src/api/middleware/auth.ts
export const auth = (): MiddlewareHandler => {
  return async (c, next) => {
    const authHeader = c.req.header("Authorization");

    if (!authHeader?.startsWith("Bearer ")) {
      return c.json(
        { error: { code: "UNAUTHORIZED", message: "API key manquante" } },
        401
      );
    }

    const apiKey = authHeader.slice(7);

    if (apiKey !== env.API_KEY) {
      return c.json(
        { error: { code: "UNAUTHORIZED", message: "API key invalide" } },
        401
      );
    }

    await next();
  };
};
```

**V2+ :** migrer vers JWT si le frontend a des utilisateurs individuels.

## OpenAPI / Documentation

L'API génère automatiquement un spec OpenAPI grâce à `@hono/zod-openapi`.
Accessible sur `GET /openapi.json`.

Cela permet :
- Documentation automatique (Swagger UI si besoin)
- Génération de clients typés pour le frontend
- Conversion future vers MCP (les outils MCP sont décrits comme des endpoints)
- L'agent IA peut lire le spec pour découvrir les endpoints

## Versioning

Pas de versioning en V1. Quand nécessaire (breaking changes avec des clients existants) :
- Préfixe URL : `/api/v2/coproprietes`
- Les anciennes versions restent actives pendant une période de transition
