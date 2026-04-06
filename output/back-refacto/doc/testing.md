# Stratégie de Tests

## Pyramide de tests

```
        ╱╲
       ╱  ╲        E2E (rare, V2+)
      ╱────╲       Tests de l'API complète avec DB réelle
     ╱      ╲
    ╱────────╲     Intégration (modéré)
   ╱          ╲    Repository + DB réelle
  ╱────────────╲
 ╱              ╲  Unitaire (majorité)
╱────────────────╲ Use cases avec mocks
```

| Type | Quoi | Où | Fréquence | DB |
|------|------|----|-----------|----|
| Unitaire | Use cases, value objects, entités | `src/core/` | Chaque use case | Non (mocks) |
| Intégration | Repositories Drizzle | `src/infra/` | Chaque repository | Oui (test DB) |
| API | Routes Hono complètes | `src/api/` | Endpoints critiques | Oui (test DB) |

## Tests unitaires (src/core)

C'est la priorité. Chaque use case a au moins un test.
Les repositories sont mockés — on teste la LOGIQUE MÉTIER.

### Structure

```
src/core/
├── use-cases/
│   ├── queries/
│   │   ├── get-copropriete.use-case.ts
│   │   └── get-copropriete.use-case.test.ts    ← co-localisé
│   └── commands/
│       ├── create-appel-de-fonds.use-case.ts
│       └── create-appel-de-fonds.use-case.test.ts
└── domain/
    └── value-objects/
        ├── montant.ts
        └── montant.test.ts                      ← co-localisé
```

**Les tests sont CO-LOCALISÉS** avec le code qu'ils testent.
Pas de dossier `__tests__/` séparé.

### Exemple test use case

```typescript
// src/core/use-cases/queries/get-copropriete.use-case.test.ts
import { describe, it, expect, mock } from "bun:test";
import { GetCoproprieteUseCase } from "./get-copropriete.use-case";
import { CoproprieteNotFoundError } from "../../domain/errors/copropriete-not-found.error";
import type { CoproprieteRepository } from "../../ports/out/copropriete.repository";

// Mock du repository — on ne touche PAS la DB
const mockRepo: CoproprieteRepository = {
  findById: mock(() => Promise.resolve(null)),
  findAll: mock(() => Promise.resolve([])),
};

describe("GetCoproprieteUseCase", () => {
  it("retourne la copropriété quand elle existe", async () => {
    const copro = {
      id: "123",
      nom: "Les Alpes",
      adresse: "30 chemin du Vieux Chêne, 38240 Meylan",
      nombreLots: 42,
      exerciceEnCours: { debut: "2025-01-01", fin: "2025-12-31" },
      syndic: "Cabinet Martin",
    };

    mockRepo.findById = mock(() => Promise.resolve(copro));

    const useCase = new GetCoproprieteUseCase(mockRepo);
    const result = await useCase.execute("123");

    expect(result).toEqual(copro);
    expect(mockRepo.findById).toHaveBeenCalledWith("123");
  });

  it("lance CoproprieteNotFoundError quand elle n'existe pas", async () => {
    mockRepo.findById = mock(() => Promise.resolve(null));

    const useCase = new GetCoproprieteUseCase(mockRepo);

    expect(useCase.execute("unknown")).rejects.toBeInstanceOf(
      CoproprieteNotFoundError
    );
  });
});
```

### Exemple test value object

```typescript
// src/core/domain/value-objects/montant.test.ts
import { describe, it, expect } from "bun:test";
import { Montant } from "./montant";

describe("Montant", () => {
  it("refuse un montant négatif", () => {
    expect(() => Montant.of(-100)).toThrow();
  });

  it("additionne deux montants", () => {
    const a = Montant.of(100);
    const b = Montant.of(50);
    expect(a.add(b).valeur).toBe(150);
  });

  it("compare deux montants égaux", () => {
    expect(Montant.of(100).equals(Montant.of(100))).toBe(true);
    expect(Montant.of(100).equals(Montant.of(200))).toBe(false);
  });
});
```

## Tests d'intégration (src/infra)

Testent les repositories avec une vraie base PostgreSQL de test.

### Setup

```typescript
// src/infra/test-utils/setup.ts
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "../postgres/schema";

const TEST_DATABASE_URL = process.env.TEST_DATABASE_URL
  ?? "postgresql://test:test@localhost:5433/neoteem_test";

const client = postgres(TEST_DATABASE_URL);
export const testDb = drizzle(client, { schema });

export async function cleanDb() {
  // Truncate toutes les tables de test
  await testDb.execute(`
    DO $$ DECLARE
      r RECORD;
    BEGIN
      FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
      LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
      END LOOP;
    END $$;
  `);
}

export async function closeDb() {
  await client.end();
}
```

### Exemple test repository

```typescript
// src/infra/postgres/repositories/copropriete.repository.pg.test.ts
import { describe, it, expect, beforeEach, afterAll } from "bun:test";
import { PgCoproprieteRepository } from "./copropriete.repository.pg";
import { cleanDb, closeDb, testDb } from "../../test-utils/setup";
import { coproprietes } from "../schema";

describe("PgCoproprieteRepository", () => {
  const repo = new PgCoproprieteRepository();

  beforeEach(async () => {
    await cleanDb();
  });

  afterAll(async () => {
    await closeDb();
  });

  it("findById retourne null si non trouvé", async () => {
    const result = await repo.findById("non-existent-id");
    expect(result).toBeNull();
  });

  it("findById retourne l'entité mappée correctement", async () => {
    // Insérer une ligne de test
    await testDb.insert(coproprietes).values({
      id: "test-123",
      nom: "Les Alpes",
      adresse_numero: "30",
      adresse_rue: "chemin du Vieux Chêne",
      adresse_cp: "38240",
      adresse_ville: "Meylan",
      nombre_lots: 42,
      syndic_nom: "Cabinet Martin",
    });

    const result = await repo.findById("test-123");

    expect(result).not.toBeNull();
    expect(result!.nom).toBe("Les Alpes");
    expect(result!.nombreLots).toBe(42);
    // Vérifie que le mapper a bien transformé snake_case → camelCase
    expect(result!.adresse).toContain("Meylan");
  });
});
```

## Tests API (src/api)

Testent les routes Hono de bout en bout (avec DI mockée ou réelle).

```typescript
// src/api/routes/queries/coproprietes.query.test.ts
import { describe, it, expect } from "bun:test";
import { app } from "../../app";

describe("GET /api/coproprietes/:id", () => {
  it("retourne 200 avec une copropriété valide", async () => {
    const res = await app.request("/api/coproprietes/test-123");
    expect(res.status).toBe(200);

    const body = await res.json();
    expect(body).toHaveProperty("id");
    expect(body).toHaveProperty("nom");
  });

  it("retourne 404 pour une copropriété inexistante", async () => {
    const res = await app.request("/api/coproprietes/non-existent");
    expect(res.status).toBe(404);

    const body = await res.json();
    expect(body.error.code).toBe("COPROPRIETE_NOT_FOUND");
  });

  it("retourne 400 pour un id invalide (pas UUID)", async () => {
    const res = await app.request("/api/coproprietes/not-a-uuid");
    expect(res.status).toBe(400);
  });
});
```

## Conventions de test

### Nommage des fichiers
```
[nom-du-fichier].test.ts    ← TOUJOURS co-localisé avec le source
```

### Structure d'un test
```typescript
describe("[NomDuModule]", () => {
  // Setup commun en beforeEach si nécessaire

  it("[action] [résultat attendu]", async () => {
    // Arrange — préparer les données
    // Act — exécuter
    // Assert — vérifier
  });
});
```

### Règles
- **Nommer le test en français** : `it("retourne 404 quand la copro n'existe pas")`
- **Un test = un comportement** : pas de tests qui vérifient 10 choses
- **Pas de dépendance entre tests** : chaque test est indépendant
- **beforeEach pour le setup, pas beforeAll** (sauf connexion DB)
- **Mocker au niveau du port** : mocker le repository, pas la DB
- **Zéro console.log dans les tests** : utiliser expect()

### Commandes

```bash
bun run test                           # Tous les tests
bun run test --filter "core"           # Tests du package core uniquement
bun run test --filter "GetCopropriete" # Un test spécifique
bun run test --watch                   # Mode watch (dev)
```

### Quand écrire un test

| Situation | Test requis ? |
|-----------|---------------|
| Nouveau use case | **OUI** — unitaire obligatoire |
| Nouveau value object avec logique | **OUI** — unitaire obligatoire |
| Nouveau repository | **OUI** — intégration obligatoire |
| Nouveau endpoint | Recommandé (test API) |
| Bug fix | **OUI** — écrire le test QUI AURAIT ATTRAPÉ le bug |
| Refactoring | Les tests existants doivent passer sans modification |
