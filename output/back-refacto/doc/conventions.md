# Conventions de code

## Nommage des fichiers

```
*.query.ts           → Endpoint de lecture (GET)
*.command.ts         → Endpoint d'écriture (POST/PUT/DELETE)
*.use-case.ts        → Logique métier orchestrée
*.use-case.test.ts   → Test du use case
*.repository.ts      → Interface (port out dans core)
*.repository.pg.ts   → Implémentation PostgreSQL (dans infra)
*.mapper.ts          → Transformation DB ↔ Domain
*.table.ts           → Schéma Drizzle d'une table
*.schema.ts          → Schéma Zod (validation)
*.error.ts           → Erreur métier typée
*.types.ts           → Types TypeScript purs
*.test.ts            → Test (co-localisé avec le source)
```

Tout en **kebab-case** : `appel-de-fonds.use-case.ts`, pas `appelDeFonds.use-case.ts`.

## Nommage du code

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Fichier | kebab-case + suffixe | `create-appel-de-fonds.use-case.ts` |
| Classe | PascalCase | `CreateAppelDeFondsUseCase` |
| Interface | PascalCase (pas de prefix I) | `CoproprieteRepository` (pas ~~ICoproprieteRepository~~) |
| Fonction | camelCase | `toCopropriete()` |
| Variable | camelCase | `const coproprieteRepo` |
| Constante | SCREAMING_SNAKE_CASE | `const MAX_PAGE_SIZE = 100` |
| Type | PascalCase | `type AppelDeFonds = {...}` |
| Colonne DB | snake_case | `nombre_lots`, `syndic_nom` |
| Endpoint API | kebab-case pluriel | `/api/appels-de-fonds` |
| Code d'erreur | SCREAMING_SNAKE_CASE | `COPROPRIETE_NOT_FOUND` |
| Schéma Zod | PascalCase + Schema | `CoproprieteSchema` |

## Structure d'un use case

```typescript
// TOUJOURS cette structure
export class [Verbe][Entité]UseCase {
  constructor(
    // Dépendances injectées — readonly + private
    private readonly nomRepo: NomRepository
  ) {}

  // UNE seule méthode publique
  async execute(input: [Verbe][Entité]Input): Promise<[ReturnType]> {
    // 1. Charger les données
    // 2. Valider les règles métier (throw DomainError si invalide)
    // 3. Effectuer l'opération
    // 4. Persister si command
    // 5. Retourner le résultat
  }
}
```

## Structure d'une route

```typescript
// TOUJOURS cette structure
export const create[Entité]Routes = (
  // Injection des use cases
  useCase: [Verbe][Entité]UseCase
) => {
  const router = new OpenAPIHono();

  // 1. Déclarer la route (schéma OpenAPI)
  const route = createRoute({
    method: "get" | "post" | "put" | "delete",
    path: "/...",
    tags: ["[Module]"],
    summary: "Description courte",
    request: { /* schémas Zod */ },
    responses: { /* schémas Zod */ },
  });

  // 2. Implémenter le handler
  router.openapi(route, async (c) => {
    const input = c.req.valid("json" | "param" | "query");
    const result = await useCase.execute(input);
    return c.json(result, 200);
  });

  return router;
};
```

**JAMAIS dans une route :**
- De la logique métier
- Des appels directs à la DB
- Des imports de `drizzle-orm`

## Structure d'un repository (implémentation)

```typescript
export class Pg[Entité]Repository implements [Entité]Repository {
  // Chaque méthode = une requête DB + mapping
  async findById(id: string): Promise<Entité | null> {
    const row = await db.select().from(table).where(eq(table.id, id)).limit(1);
    return row[0] ? toEntité(row[0]) : null;
  }
}
```

**JAMAIS dans un repository :**
- De la logique métier (if/else sur des règles de gestion)
- Des appels à d'autres repositories
- Du formatage de données pour l'API

## Imports

### Ordre des imports (appliqué automatiquement)

```typescript
// 1. Modules externes
import { OpenAPIHono } from "@hono/zod-openapi";
import { z } from "zod";

// 2. Packages internes (@core/*, @infra/*, @shared/*)
import type { Copropriete } from "@core/domain/entities/copropriete";
import { CoproprieteSchema } from "@shared/schemas";

// 3. Imports relatifs
import { errorHandler } from "../middleware/error-handler";
```

### Règles d'import

- Utiliser `import type` quand on importe UNIQUEMENT un type
- JAMAIS d'import circulaire
- JAMAIS d'import de `@infra` dans `@core`
- Les re-exports sont dans `index.ts` de chaque package

## TypeScript strict

### tsconfig.base.json

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### Règles TypeScript

- **Zéro `any`** — utiliser `unknown` puis type guard
- **Zéro `as` (type assertion)** sauf pour les tests
- **Zéro `!` (non-null assertion)** — utiliser une vérification explicite
- **Zéro `// @ts-ignore`** — corriger le problème
- **Toujours `readonly`** sur les propriétés injectées
- **Préférer `interface` à `type`** pour les objets (extensible)
- **Préférer `type` à `interface`** pour les unions et intersections

## Gestion des erreurs

```typescript
// ✅ BON — erreur typée
throw new CoproprieteNotFoundError(id);

// ❌ MAUVAIS — erreur générique
throw new Error("Copropriété non trouvée");

// ❌ MAUVAIS — string
throw "Copropriété non trouvée";
```

## Variables d'environnement

Toujours validées avec Zod au démarrage :

```typescript
// src/shared/config/env.ts
import { z } from "zod";

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  API_KEY: z.string().min(32),
});

export const env = envSchema.parse(process.env);
export type Env = z.infer<typeof envSchema>;
```

**Si une variable manque, l'app CRASH au démarrage** — pas en runtime au milieu d'une requête.

## Commentaires

- **Pas de commentaires évidents** : `// Retourne la copropriété` est inutile
- **Commenter le POURQUOI, pas le QUOI** : `// Règle métier : les tantièmes doivent totaliser 10000`
- **Les noms de fonctions et variables remplacent les commentaires**
- **Les TODO sont autorisés** avec format : `// TODO(nom): description`
