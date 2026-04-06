---
name: add-error
description: Create a typed business error. Use when user says 'ajoute une erreur', 'crée une erreur métier', 'create a domain error', 'add error class', 'nouvelle erreur', 'business rule error', 'not found error'.
user-invokable: true
argument-hint: "[nom de l'erreur]"
effort: high
---

# Ajouter une erreur métier

## Catégories

| Classe parente | HTTP | Usage |
|----------------|------|-------|
| `NotFoundError` | 404 | Ressource inexistante |
| `ValidationError` | 400 | Données invalides |
| `BusinessRuleError` | 422 | Règle métier violée |
| `ConflictError` | 409 | Doublon, déjà effectué |
| `ForbiddenError` | 403 | Non autorisé |

## Template

```typescript
// src/core/domain/errors/[nom].error.ts
import { DomainError } from "./base.error";

export class NomDeLErreurError extends DomainError {
  readonly code = "CODE_UNIQUE_SCREAMING_SNAKE";
  readonly httpStatus = 422; // adapter selon catégorie

  constructor(paramUtile: string) {
    super(`Message en français avec ${paramUtile}`);
  }
}
```

## Utilisation dans un use case
```typescript
if (condition) {
  throw new NomDeLErreurError(param);
}
```

Le middleware `error-handler` transforme automatiquement en réponse HTTP.
Pas besoin de modifier le middleware.

## Règles
- `code` unique dans tout le projet, anglais SCREAMING_SNAKE_CASE
- `message` en français, pour les humains
- JAMAIS `throw new Error("...")` ni `throw "string"`
