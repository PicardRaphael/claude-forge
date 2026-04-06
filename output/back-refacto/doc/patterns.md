# Design Patterns — Référence obligatoire

## Patterns TOUJOURS utilisés

### 1. Repository Pattern

Chaque accès aux données passe par un repository.
L'interface est dans `core/ports/out/`, l'implémentation dans `infra/`.

```typescript
// INTERFACE — src/core/ports/out/lot.repository.ts
export interface LotRepository {
  findById(id: string): Promise<Lot | null>;
  findByCopropriete(coproprieteId: string): Promise<Lot[]>;
  save(lot: Lot): Promise<void>;
}

// IMPLÉMENTATION — src/infra/postgres/repositories/lot.repository.pg.ts
export class PgLotRepository implements LotRepository {
  async findById(id: string): Promise<Lot | null> {
    const row = await db.select().from(lots).where(eq(lots.id, id)).limit(1);
    return row[0] ? toLot(row[0]) : null;
  }
  // ...
}
```

**Règles :**
- Un repository = une entité racine (aggregate root)
- Le repository retourne TOUJOURS des entités domaine (pas des rows DB)
- Le repository ne contient AUCUNE logique métier
- Nommage : `[entité].repository.ts` (interface), `[entité].repository.pg.ts` (implémentation)

### 2. Use Case Pattern

Chaque opération métier est un use case isolé dans son propre fichier.

```typescript
// src/core/use-cases/commands/create-appel-de-fonds.use-case.ts
export class CreateAppelDeFondsUseCase {
  constructor(
    private readonly coproprieteRepo: CoproprieteRepository,
    private readonly compteRepo: CompteRepository
  ) {}

  async execute(input: CreateAppelDeFondsInput): Promise<AppelDeFonds> {
    // 1. Charger les données nécessaires
    const copro = await this.coproprieteRepo.findById(input.coproprieteId);
    if (!copro) throw new CoproprieteNotFoundError(input.coproprieteId);

    // 2. Appliquer les règles métier
    if (copro.exerciceEnCours.estCloture) {
      throw new ExerciceClotureError(copro.id);
    }

    // 3. Créer l'entité
    const appel: AppelDeFonds = {
      id: crypto.randomUUID(),
      coproprieteId: copro.id,
      montant: Montant.of(input.montant),
      dateAppel: new Date(),
      trimestre: input.trimestre,
    };

    // 4. Persister
    await this.compteRepo.enregistrerAppel(appel);

    return appel;
  }
}
```

**Règles :**
- Un fichier = un use case = une méthode `execute()`
- Le use case reçoit ses dépendances par constructeur (injection)
- Le use case orchestre : il charge, valide, crée, persiste
- Le use case NE gère PAS la transaction HTTP (pas de try/catch pour les 500)
- Input et Output sont des types/interfaces simples
- Nommage : `[verbe]-[entité].use-case.ts`

### 3. Mapper Pattern (Data Mapper)

Conversion systématique entre les couches. Jamais de fuite d'abstraction.

```
DB Row (Drizzle) ──mapper──→ Domain Entity (Core) ──schema──→ API Response (Zod)
API Request (Zod) ──────────→ Use Case Input ──────────────→ Domain Entity
```

```typescript
// src/infra/postgres/mappers/copropriete.mapper.ts
// DB → Domain
export function toCopropriete(row: CoproprieteRow): Copropriete {
  return {
    id: row.id,
    nom: row.nom,
    adresse: `${row.adresse_numero} ${row.adresse_rue}, ${row.adresse_cp} ${row.adresse_ville}`,
    nombreLots: row.nombre_lots,
    // ... transformation des noms DB → noms domaine
  };
}
```

**Règles :**
- Un mapper par entité
- Les noms de colonnes DB (snake_case) ne fuient JAMAIS dans le domaine (camelCase)
- Les mappers sont des fonctions pures (pas de classes)
- Nommage : `[entité].mapper.ts`

### 4. Error Hierarchy Pattern

Toutes les erreurs métier héritent de `DomainError`.
Le middleware `error-handler` les transforme en réponses HTTP.

```typescript
// Hiérarchie
DomainError (abstract)
├── NotFoundError (abstract, httpStatus: 404)
│   ├── CoproprieteNotFoundError
│   ├── LotNotFoundError
│   └── CompteNotFoundError
├── ValidationError (abstract, httpStatus: 400)
│   ├── MontantNegatifError
│   ├── TantiemeInvalideError
│   └── ExerciceClotureError
├── ConflictError (abstract, httpStatus: 409)
│   └── AppelDejaExistantError
└── ForbiddenError (abstract, httpStatus: 403)
    └── OperationNonAutoriseeError
```

```typescript
// Middleware qui transforme DomainError → HTTP Response
// src/api/middleware/error-handler.ts
export const errorHandler = (err: Error, c: Context): Response => {
  if (err instanceof DomainError) {
    return c.json(
      {
        error: {
          code: err.code,
          message: err.message,
        },
      },
      err.httpStatus as StatusCode
    );
  }

  // Erreur inattendue → 500 sans détails
  console.error("Unhandled error:", err);
  return c.json(
    { error: { code: "INTERNAL_ERROR", message: "Erreur interne" } },
    500
  );
};
```

**Règles :**
- JAMAIS `throw new Error("message")` — toujours une classe typée
- Chaque erreur a un `code` unique (pour l'agent IA) et un `httpStatus`
- Le message est en français (destiné aux humains/logs)
- Le code est en SCREAMING_SNAKE_CASE anglais (destiné aux machines)

### 5. Schema-first API Pattern

Chaque endpoint est défini schema-first avec Zod + OpenAPI.

```typescript
// L'endpoint est DÉCLARATIF — le schéma EST la documentation
const route = createRoute({
  method: "get",
  path: "/coproprietes/{id}/lots",
  tags: ["Lots"],
  summary: "Liste des lots d'une copropriété",
  request: {
    params: z.object({
      id: z.string().uuid(),
    }),
    query: z.object({
      page: z.coerce.number().int().min(1).default(1),
      limit: z.coerce.number().int().min(1).max(100).default(20),
    }),
  },
  responses: {
    200: {
      content: {
        "application/json": {
          schema: PaginatedSchema(LotSchema),
        },
      },
      description: "Liste paginée des lots",
    },
    404: { description: "Copropriété non trouvée" },
  },
});
```

**Règles :**
- Le schéma Zod est la source de vérité (pas les types manuels)
- Utiliser `z.infer<typeof Schema>` pour dériver les types
- Les schémas partagés sont dans `src/shared/schemas/`
- Tout endpoint produit un OpenAPI spec valide automatiquement

## Patterns INTERDITS

### ❌ God Use Case
Un use case qui fait trop de choses. Si `execute()` dépasse 40 lignes, découper.

### ❌ Anemic Domain
Des entités qui ne sont que des sacs de données sans comportement.
Si une règle métier existe (ex: "un montant ne peut pas être négatif"),
elle est DANS le value object ou l'entité, pas dans le use case.

### ❌ Smart Repository
Un repository qui contient de la logique métier.
Le repository charge et persiste. C'est tout.

### ❌ Leaky Abstraction
Retourner un type Drizzle directement depuis un repository.
TOUJOURS mapper vers une entité domaine.

### ❌ Shotgun Surgery
Un changement métier qui nécessite de modifier 10 fichiers.
Si c'est le cas, le découpage est mauvais — revoir les boundaries.

### ❌ any
Jamais. Utiliser `unknown` puis type-guard si nécessaire.

## Patterns À UTILISER QUAND NÉCESSAIRE (pas en V1 systématiquement)

### Result Pattern (alternatif aux exceptions)

Si un use case a plusieurs modes d'échec prévisibles,
utiliser un type Result au lieu d'exceptions :

```typescript
type Result<T, E = DomainError> =
  | { success: true; data: T }
  | { success: false; error: E };
```

**Quand l'utiliser :** quand l'appelant doit réagir différemment
selon le type d'erreur (fréquent dans les commandes complexes).
**Quand NE PAS l'utiliser :** pour les cas simples (not found, validation).

### Specification Pattern

Pour les filtres de recherche complexes :

```typescript
interface LotSpecification {
  toWhereClause(): SQL; // Drizzle SQL expression
}

class LotAvecImpayes implements LotSpecification { ... }
class LotParEtage implements LotSpecification { ... }
```

**Quand l'utiliser :** quand les filtres sont combinables et complexes.
**Quand NE PAS l'utiliser :** pour un simple `findById` ou `findAll`.
