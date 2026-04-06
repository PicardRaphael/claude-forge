# Architecture Hexagonale — Guide de référence

## Principe fondamental

Le domaine métier (src/core) est au centre. Il ne dépend de RIEN.
Tout le reste (HTTP, base de données, services tiers) est un détail
d'implémentation qui se branche autour via des interfaces (ports).

```
                    ┌─────────────────┐
                    │     src/api     │
                    │  (Hono routes)  │
                    └────────┬────────┘
                             │ appelle
                             ▼
              ┌──────────────────────────────┐
              │          src/core             │
              │                              │
              │  ports/in/   ← use cases     │
              │  use-cases/  ← domain logic  │
              │  ports/out/  → interfaces    │
              │  domain/     ← entities      │
              └──────────────┬───────────────┘
                             │ implémenté par
                             ▼
                    ┌─────────────────┐
                    │   src/infra     │
                    │  (Drizzle, PG)  │
                    └─────────────────┘
```

## Structure du projet

```
neoteem-backend/
├── src/
│   ├── index.ts                    # Bootstrap Hono + serveur Bun
│   ├── app.ts                      # Configuration Hono (middleware, routes)
│   ├── di.ts                       # Injection de dépendances (factory)
│   │
│   ├── core/                       # Domaine métier pur (AUCUNE dépendance)
│   │   ├── domain/
│   │   │   ├── entities/           # Objets métier avec identité
│   │   │   │   ├── copropriete.ts
│   │   │   │   ├── lot.ts
│   │   │   │   ├── coproprietaire.ts
│   │   │   │   ├── compte.ts
│   │   │   │   └── appel-de-fonds.ts
│   │   │   ├── value-objects/      # Objets immuables sans identité
│   │   │   │   ├── tantieme.ts
│   │   │   │   ├── montant.ts
│   │   │   │   └── exercice.ts
│   │   │   └── errors/             # Erreurs métier typées
│   │   │       ├── base.error.ts
│   │   │       ├── not-found.error.ts
│   │   │       ├── validation.error.ts
│   │   │       ├── business-rule.error.ts
│   │   │       └── copropriete-not-found.error.ts
│   │   ├── ports/
│   │   │   ├── in/                 # Ce que le monde extérieur peut demander
│   │   │   │   ├── queries/
│   │   │   │   └── commands/
│   │   │   └── out/                # Ce dont le domaine a besoin
│   │   │       ├── copropriete.repository.ts
│   │   │       ├── lot.repository.ts
│   │   │       └── compte.repository.ts
│   │   └── use-cases/              # Orchestration logique métier
│   │       ├── queries/
│   │       │   ├── get-copropriete.use-case.ts
│   │       │   └── get-copropriete.use-case.test.ts
│   │       └── commands/
│   │           ├── create-appel-de-fonds.use-case.ts
│   │           └── create-appel-de-fonds.use-case.test.ts
│   │
│   ├── infra/                      # Adaptateurs techniques
│   │   └── postgres/
│   │       ├── client.ts           # Connexion Drizzle + pool
│   │       ├── schema/             # Tables Drizzle (introspectées)
│   │       │   ├── coproprietes.table.ts
│   │       │   ├── lots.table.ts
│   │       │   └── index.ts
│   │       ├── repositories/       # Implémentent les ports out
│   │       │   ├── copropriete.repository.pg.ts
│   │       │   ├── copropriete.repository.pg.test.ts
│   │       │   └── lot.repository.pg.ts
│   │       └── mappers/            # DB row → Domain entity
│   │           ├── copropriete.mapper.ts
│   │           └── lot.mapper.ts
│   │
│   ├── api/                        # Adaptateur HTTP (Hono)
│   │   ├── routes/
│   │   │   ├── index.ts            # Agrégation des routes
│   │   │   ├── queries/            # GET endpoints
│   │   │   │   └── coproprietes.query.ts
│   │   │   └── commands/           # POST/PUT/DELETE endpoints
│   │   │       └── appels-de-fonds.command.ts
│   │   └── middleware/
│   │       ├── error-handler.ts
│   │       ├── auth.ts
│   │       └── logger.ts
│   │
│   └── shared/                     # Types et utilitaires partagés
│       ├── schemas/                # Schémas Zod (request/response API)
│       │   ├── copropriete.schema.ts
│       │   ├── pagination.schema.ts
│       │   └── error.schema.ts
│       ├── types/                  # Types TypeScript communs
│       │   └── api.types.ts
│       └── config/
│           └── env.ts              # Validation des env vars (Zod)
│
├── .claude/                        # Skills et agents Claude Code
├── docs/                           # Documentation
├── drizzle/                        # Migrations Drizzle générées
├── drizzle.config.ts
├── package.json                    # UN SEUL package.json
├── tsconfig.json                   # UN SEUL tsconfig avec path aliases
├── Dockerfile
├── .env.example
└── README.md
```

## Path aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@core/*": ["src/core/*"],
      "@infra/*": ["src/infra/*"],
      "@api/*": ["src/api/*"],
      "@shared/*": ["src/shared/*"]
    }
  }
}
```

Cela permet des imports propres :
```typescript
import type { Copropriete } from "@core/domain/entities/copropriete";
import { CoproprieteSchema } from "@shared/schemas/copropriete.schema";
```

## Graphe de dépendances

```
src/index.ts + src/di.ts (bootstrap)
       │
       ▼
   src/api ──────→ src/core ←────── src/infra
       │               │                │
       └───────────────▼────────────────┘
                  src/shared
```

**Règle absolue :** `src/core/` ne dépend JAMAIS de `src/infra/` ni de `src/api/`.
Les flèches vont toujours vers le centre (inversion de dépendance).

## Les 4 dossiers et leurs responsabilités

### src/core/ (le cœur — AUCUNE dépendance technique)

**Règles strictes :**
- JAMAIS d'import depuis `@infra/`, `hono`, `drizzle-orm`, `pg`
- Seule dépendance autorisée : `zod` (pour les schémas de domaine)
- Les use cases reçoivent les repositories par injection (constructeur)
- Les entités ne sont PAS des classes Drizzle — ce sont des interfaces TS pures
- Les erreurs étendent `DomainError`

**Exemple d'entité :**
```typescript
// src/core/domain/entities/copropriete.ts
export interface Copropriete {
  readonly id: string;
  readonly nom: string;
  readonly adresse: string;
  readonly nombreLots: number;
  readonly exerciceEnCours: Exercice;
  readonly syndic: string;
}
```

**Exemple de value object :**
```typescript
// src/core/domain/value-objects/montant.ts
export class Montant {
  private constructor(
    readonly valeur: number,
    readonly devise: "EUR" = "EUR"
  ) {
    if (valeur < 0) throw new MontantNegatifError(valeur);
  }

  static of(valeur: number, devise: "EUR" = "EUR"): Montant {
    return new Montant(valeur, devise);
  }

  add(autre: Montant): Montant {
    return Montant.of(this.valeur + autre.valeur, this.devise);
  }

  equals(autre: Montant): boolean {
    return this.valeur === autre.valeur && this.devise === autre.devise;
  }
}
```

### src/infra/ (adaptateurs techniques)

**Règles strictes :**
- Chaque repository implémente EXACTEMENT une interface de `@core/ports/out/`
- Les mappers transforment TOUJOURS les lignes DB en entités domaine
- JAMAIS retourner un objet Drizzle directement
- La connexion DB est centralisée dans `client.ts`

### src/api/ (point d'entrée HTTP)

**Règles strictes :**
- Les routes NE CONTIENNENT PAS de logique métier
- Les routes valident (Zod), appellent un use case, retournent la réponse
- Le middleware `error-handler` transforme les `DomainError` en HTTP
- L'injection se fait dans `src/di.ts`

### src/shared/ (types communs)

Pas de logique. Juste des types, schémas Zod, et configuration.

## Injection de dépendances

```typescript
// src/di.ts
import { PgCoproprieteRepository } from "@infra/postgres/repositories/copropriete.repository.pg";
import { GetCoproprieteUseCase } from "@core/use-cases/queries/get-copropriete.use-case";

const coproprieteRepo = new PgCoproprieteRepository();
export const getCopropriete = new GetCoproprieteUseCase(coproprieteRepo);
```

## Flux d'une requête

```
Agent IA → GET /api/coproprietes/123
  → src/api/routes/queries/coproprietes.query.ts   (valide avec Zod)
  → src/core/use-cases/queries/get-copropriete.use-case.ts  (logique métier)
  → src/core/ports/out/copropriete.repository.ts   (INTERFACE)
  → src/infra/postgres/repositories/copropriete.repository.pg.ts  (Drizzle)
  → src/infra/postgres/mappers/copropriete.mapper.ts  (DB → Domain)
  → Retour JSON
```

## Checklist nouveau module

1. [ ] Entité dans `src/core/domain/entities/`
2. [ ] Value objects si nécessaires dans `src/core/domain/value-objects/`
3. [ ] Erreurs métier dans `src/core/domain/errors/`
4. [ ] Port out (interface) dans `src/core/ports/out/`
5. [ ] Use case dans `src/core/use-cases/`
6. [ ] Test unitaire du use case (co-localisé)
7. [ ] Schéma Drizzle dans `src/infra/postgres/schema/`
8. [ ] Mapper dans `src/infra/postgres/mappers/`
9. [ ] Repository dans `src/infra/postgres/repositories/`
10. [ ] Schéma Zod dans `src/shared/schemas/`
11. [ ] Route dans `src/api/routes/`
12. [ ] Enregistrer dans `src/di.ts`

## Évolution future vers monorepo

Si un jour le frontend rejoint le même repo, la migration est simple :
- `src/core/` → `packages/core/src/`
- `src/infra/` → `packages/infra/src/`
- Ajouter Turborepo + workspaces
- Le code ne change pas, seul le packaging change
