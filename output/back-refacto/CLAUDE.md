# Neoteem Backend

## Projet

ERP SaaS pour administrateurs de biens immobiliers (syndic, gérance).
Backend API entre PostgreSQL existant (200+ tables, 1000+ fonctions) et les consommateurs (app IA, frontend).

## Stack

Bun · Hono · @hono/zod-openapi · Zod · Drizzle ORM · bun:test

## Config

- Repo fonctions PostgreSQL : [À CONFIGURER — chemin absolu]
- Doc schéma : doc/schemas/ (généré par schema-mapper)
- Export tables : doc/dump/ (CSV exportés par export-schema.sh)

## Architecture hexagonale — Règle d'or

```
src/api  →  src/core  ←  src/infra
                ↓
           src/shared
```

- `src/core/` = domaine métier PUR. Zéro dépendance technique.
- `src/infra/` = implémente les interfaces de core (Drizzle, PG).
- `src/api/` = Hono, routes, middleware, injection de dépendances.
- `src/shared/` = schémas Zod, types, config.

**INTERDIT** : importer `@infra/` depuis `src/core/`.

## Path aliases (tsconfig.json)

```
@core/*    → src/core/*
@infra/*   → src/infra/*
@api/*     → src/api/*
@shared/*  → src/shared/*
```

## Commandes

```bash
bun install          # Install
bun run dev          # Dev mode (bun --watch src/index.ts)
bun run build        # Build prod
bun run test         # Tests
bun run typecheck    # Vérif types (tsc --noEmit)
bun run db:pull      # Introspection PG existant
```

## Conventions fonctions PostgreSQL

| Préfixe | Rôle |
|---------|------|
| `f_*` | Lecture (SELECT) |
| `p_*` | Écriture (INSERT/UPDATE/DELETE) |
| `proc_*` | Procédure (orchestration) |
| `tr_*` | Trigger |

## Règles critiques

1. Zéro `any` — utiliser `unknown`
2. Zéro logique métier dans les routes — valider et déléguer
3. Zéro logique métier dans les repositories — lire/écrire, c'est tout
4. Toute erreur métier = classe typée qui étend `DomainError`
5. Un fichier = une responsabilité
6. `src/core/` n'importe JAMAIS `@infra/` ni `@api/`
7. Chaque endpoint a un schéma Zod request + response
8. Chaque use case a au moins un test unitaire
9. Ne JAMAIS modifier les fichiers du repo fonctions PostgreSQL
10. Mettre à jour doc/migration-tracker.md après chaque migration
11. Documenter les règles métier découvertes en mémoire projet

## Comportement

Consulter `.claude/rules/` pour les règles de délégation agents, le mindset CTO, et la navigation skills.
**Avant de coder, lire les docs pertinentes dans `doc/`.**
