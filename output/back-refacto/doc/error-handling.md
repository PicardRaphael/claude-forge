# Gestion des erreurs — Guide complet

## Philosophie

Chaque erreur dans Neoteem est **typée, prévisible et exploitable par une machine**.
L'agent IA qui consomme l'API doit pouvoir réagir programmatiquement au `code`
sans parser le `message`.

## Classe de base

```typescript
// src/core/domain/errors/base.error.ts
export abstract class DomainError extends Error {
  abstract readonly code: string;       // Machine-readable, SCREAMING_SNAKE_CASE
  abstract readonly httpStatus: number; // Code HTTP correspondant

  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
      },
    };
  }
}
```

## Hiérarchie

```
DomainError (abstract)
│
├── NotFoundError (abstract, 404)
│   ├── CoproprieteNotFoundError        COPROPRIETE_NOT_FOUND
│   ├── LotNotFoundError                LOT_NOT_FOUND
│   ├── CompteNotFoundError             COMPTE_NOT_FOUND
│   └── CopropriétaireNotFoundError     COPROPRIETAIRE_NOT_FOUND
│
├── ValidationError (abstract, 400)
│   ├── MontantNegatifError             MONTANT_NEGATIF
│   ├── TantiemeInvalideError           TANTIEME_INVALIDE
│   ├── DateInvalideError               DATE_INVALIDE
│   └── FormatSiretInvalideError        FORMAT_SIRET_INVALIDE
│
├── BusinessRuleError (abstract, 422)
│   ├── ExerciceClotureError            EXERCICE_ALREADY_CLOSED
│   ├── SoldeInsuffisantError           SOLDE_INSUFFISANT
│   ├── AppelDejaCreeError              APPEL_DEJA_CREE
│   └── OperationHorsExerciceError      OPERATION_HORS_EXERCICE
│
├── ConflictError (abstract, 409)
│   ├── DoublonCoproprieteError         DOUBLON_COPROPRIETE
│   └── EcritureDejaClotureeError       ECRITURE_DEJA_CLOTUREE
│
└── ForbiddenError (abstract, 403)
    └── OperationNonAutoriseeError      OPERATION_NON_AUTORISEE
```

## Classes abstraites intermédiaires

```typescript
// src/core/domain/errors/not-found.error.ts
export abstract class NotFoundError extends DomainError {
  readonly httpStatus = 404;
}

// src/core/domain/errors/validation.error.ts
export abstract class ValidationError extends DomainError {
  readonly httpStatus = 400;
}

// src/core/domain/errors/business-rule.error.ts
export abstract class BusinessRuleError extends DomainError {
  readonly httpStatus = 422;
}

// src/core/domain/errors/conflict.error.ts
export abstract class ConflictError extends DomainError {
  readonly httpStatus = 409;
}

// src/core/domain/errors/forbidden.error.ts
export abstract class ForbiddenError extends DomainError {
  readonly httpStatus = 403;
}
```

## Exemple concret

```typescript
// src/core/domain/errors/exercice-cloture.error.ts
import { BusinessRuleError } from "./business-rule.error";

export class ExerciceClotureError extends BusinessRuleError {
  readonly code = "EXERCICE_ALREADY_CLOSED";

  constructor(coproprieteId: string, exercice: string) {
    super(
      `L'exercice ${exercice} de la copropriété ${coproprieteId} est déjà clôturé. ` +
      `Aucune opération comptable n'est possible sur un exercice clôturé.`
    );
  }
}
```

## Middleware error-handler

```typescript
// src/api/middleware/error-handler.ts
import type { Context } from "hono";
import type { StatusCode } from "hono/utils/http-status";
import { DomainError } from "@core/domain/errors/base.error";
import { ZodError } from "zod";

export const errorHandler = (err: Error, c: Context): Response => {
  // Erreurs métier → code HTTP du domaine
  if (err instanceof DomainError) {
    return c.json(err.toJSON(), err.httpStatus as StatusCode);
  }

  // Erreurs de validation Zod → 400
  if (err instanceof ZodError) {
    return c.json(
      {
        error: {
          code: "VALIDATION_ERROR",
          message: "Données invalides",
          details: err.errors.map((e) => ({
            path: e.path.join("."),
            message: e.message,
          })),
        },
      },
      400
    );
  }

  // Erreurs inattendues → 500 sans détails sensibles
  console.error("Unhandled error:", err);
  return c.json(
    {
      error: {
        code: "INTERNAL_ERROR",
        message: "Une erreur interne est survenue",
      },
    },
    500
  );
};
```

## Réponse d'erreur côté API

```json
// 404 - Not Found
{
  "error": {
    "code": "COPROPRIETE_NOT_FOUND",
    "message": "Copropriété abc-123 introuvable"
  }
}

// 400 - Validation (Zod)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Données invalides",
    "details": [
      { "path": "montant", "message": "Le montant doit être positif" }
    ]
  }
}

// 422 - Business Rule
{
  "error": {
    "code": "EXERCICE_ALREADY_CLOSED",
    "message": "L'exercice 2025 de la copropriété abc-123 est déjà clôturé."
  }
}
```

## Usage dans un use case

```typescript
export class CreateAppelDeFondsUseCase {
  async execute(input: CreateAppelInput): Promise<AppelDeFonds> {
    // 1. Not Found
    const copro = await this.coproprieteRepo.findById(input.coproprieteId);
    if (!copro) {
      throw new CoproprieteNotFoundError(input.coproprieteId);
    }

    // 2. Business Rule
    if (copro.exerciceEnCours.estCloture) {
      throw new ExerciceClotureError(copro.id, copro.exerciceEnCours.annee);
    }

    // 3. Validation (si pas déjà faite par Zod au niveau route)
    if (input.montant <= 0) {
      throw new MontantNegatifError(input.montant);
    }

    // 4. Conflict
    const existant = await this.appelRepo.findByTrimestreEtCopro(
      input.trimestre, copro.id
    );
    if (existant) {
      throw new AppelDejaCreeError(copro.id, input.trimestre);
    }

    // ... logique de création
  }
}
```

## Règles

- JAMAIS `throw new Error("message")` dans core ou infra
- JAMAIS `try/catch` dans un use case pour attraper ses propres erreurs
  (laisser remonter au middleware)
- Un `try/catch` dans un use case est acceptable UNIQUEMENT pour
  transformer une erreur technique en erreur métier
- Le `code` est l'identifiant stable — le `message` peut changer
- Chaque erreur est testée unitairement

## Tests d'erreurs

```typescript
it("lance ExerciceClotureError quand l'exercice est clôturé", async () => {
  const copro = { ...coproBase, exerciceEnCours: { estCloture: true } };
  mockRepo.findById = mock(() => Promise.resolve(copro));

  const uc = new CreateAppelDeFondsUseCase(mockRepo, mockAppelRepo);

  expect(uc.execute(input)).rejects.toBeInstanceOf(ExerciceClotureError);
  expect(uc.execute(input)).rejects.toHaveProperty("code", "EXERCICE_ALREADY_CLOSED");
});
```
