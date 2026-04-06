---
name: architecture-rules
description: Hexagonal architecture rules and design patterns for the Neoteem project. Use AUTOMATICALLY when creating, modifying, or moving files in src/core, src/infra, or src/api. Also use when user says 'crée un module', 'create a use case', 'nouveau repository', 'nouvelle entité', 'architecture hexagonale'.
effort: high
---

# Architecture hexagonale — Règles

## Principe

Le domaine métier (`src/core/`) est au centre. Il ne dépend de RIEN.

```
src/api (Hono) → src/core (domaine pur) ← src/infra (Drizzle)
```

## Path aliases

```
@core/*    → src/core/*
@infra/*   → src/infra/*
@api/*     → src/api/*
@shared/*  → src/shared/*
```

## Règles absolues

- `src/core/` n'importe JAMAIS `@infra/`, `hono`, `drizzle-orm`, `pg`
- Seule dépendance autorisée dans core : `zod`
- Les use cases reçoivent les repositories par injection (constructeur)
- Les entités sont des interfaces TypeScript, PAS des classes Drizzle
- Les erreurs étendent `DomainError` (jamais `throw new Error("...")`)
- Les repositories retournent des entités domaine (jamais des rows DB)
- Les routes ne contiennent AUCUNE logique métier

## Structure

```
src/
├── core/
│   ├── domain/entities/        # Objets métier avec identité
│   ├── domain/value-objects/   # Objets immuables sans identité
│   ├── domain/errors/          # Erreurs métier (étendent DomainError)
│   ├── ports/in/queries/       # Interfaces d'entrée lecture
│   ├── ports/in/commands/      # Interfaces d'entrée écriture
│   ├── ports/out/              # Interfaces repository
│   └── use-cases/              # Orchestration logique métier
│       ├── queries/            # Ne modifient JAMAIS la base
│       └── commands/           # Peuvent lire ET écrire
├── infra/postgres/
│   ├── schema/                 # Tables Drizzle (introspectées)
│   ├── repositories/           # Implémentent les ports out
│   ├── mappers/                # DB row → Domain entity
│   └── client.ts               # Connexion Drizzle + pool
├── api/
│   ├── routes/queries/         # GET endpoints
│   ├── routes/commands/        # POST/PUT/DELETE endpoints
│   └── middleware/              # Auth, error-handler, logger
├── shared/
│   ├── schemas/                # Schémas Zod (request/response)
│   ├── types/                  # Types TS communs
│   └── config/                 # Env vars validées
├── di.ts                       # Injection de dépendances (factory)
├── app.ts                      # Config Hono
└── index.ts                    # Bootstrap serveur
```

## 5 patterns OBLIGATOIRES

### 1. Repository Pattern
Interface dans `@core/ports/out/`, implémentation dans `@infra/postgres/repositories/`.
Un repository = une entité racine. Retourne TOUJOURS des entités domaine.

### 2. Use Case Pattern
Un fichier = un use case = une méthode `execute()`.
Reçoit ses dépendances par constructeur.

### 3. Mapper Pattern
DB row → Domain entity. Fonctions pures. snake_case ne fuit JAMAIS dans le domaine.

### 4. Error Hierarchy
Chaque erreur a un `code` (SCREAMING_SNAKE_CASE) et un `httpStatus`.
Le middleware error-handler transforme automatiquement en réponse HTTP.

### 5. Schema-first API
`createRoute()` de `@hono/zod-openapi`. Le schéma Zod = la documentation.

## Patterns INTERDITS

- ❌ `any`
- ❌ Logique métier dans les routes ou repositories
- ❌ Retourner un type Drizzle depuis un repository
- ❌ `throw new Error("message")`
- ❌ `as` (type assertion) sauf tests
- ❌ `// @ts-ignore`
- ❌ Import de `@infra/` dans `src/core/`

## Checklist nouveau module

1. Entité dans `src/core/domain/entities/`
2. Value objects si nécessaires
3. Erreurs métier dans `src/core/domain/errors/`
4. Port out (interface) dans `src/core/ports/out/`
5. Use case dans `src/core/use-cases/`
6. Test unitaire du use case (co-localisé)
7. Schéma Drizzle dans `src/infra/postgres/schema/`
8. Mapper dans `src/infra/postgres/mappers/`
9. Repository dans `src/infra/postgres/repositories/`
10. Schéma Zod dans `src/shared/schemas/`
11. Route dans `src/api/routes/`
12. Enregistrer dans `src/di.ts`
