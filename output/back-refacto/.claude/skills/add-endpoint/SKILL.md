---
name: add-endpoint
description: Complete procedure to add a new REST endpoint. Use when user says 'ajoute un endpoint', 'crée une route', 'create a route', 'new API endpoint', 'expose data via API', 'nouvel endpoint', 'nouvelle route REST'.
user-invokable: true
argument-hint: "[description de l'endpoint]"
effort: high
---

# Ajouter un endpoint — 11 étapes

Suivre ces étapes DANS L'ORDRE. Ne pas sauter d'étape.
Lire `.claude/skills/architecture-rules/SKILL.md` avant de commencer.

## 1. Entité (si nouvelle)
Créer dans `src/core/domain/entities/[entite].ts`.
Interface TypeScript readonly. Pas de classe.

## 2. Port out (interface repository)
Créer dans `src/core/ports/out/[entite].repository.ts`.
Interface avec les méthodes nécessaires (findById, findAll, save...).

## 3. Use case
Créer dans `src/core/use-cases/queries/` ou `commands/`.
Fichier : `[verbe]-[entite].use-case.ts`.
Classe avec constructeur (injection repos) et méthode `execute()`.

## 4. Test du use case
Créer co-localisé : `[verbe]-[entite].use-case.test.ts`.
Mocker le repository. Tester le cas nominal + les erreurs.
Lancer : `bun test --filter "[NomUseCase]"`

## 5. Schéma Drizzle (si nouvelle table)
Soit `bun run db:pull` (introspection auto), soit créer manuellement
dans `src/infra/postgres/schema/[entites].table.ts`.
NE PAS modifier le schéma DB existant.

## 6. Mapper
Créer dans `src/infra/postgres/mappers/[entite].mapper.ts`.
Fonction pure `toEntite(row) → Entite`. Transformer snake_case → camelCase.

## 7. Repository (implémentation)
Créer dans `src/infra/postgres/repositories/[entite].repository.pg.ts`.
Implémenter l'interface du port out. Utiliser Drizzle. Mapper chaque résultat.

## 8. Schéma Zod
Créer dans `src/shared/schemas/[entite].schema.ts`.
Schéma request ET response. Exporter le type inféré.

## 9. Route
Créer dans `src/api/routes/queries/` ou `commands/`.
Utiliser `createRoute()` de `@hono/zod-openapi`.
La route valide (Zod), appelle le use case, retourne la réponse. C'est TOUT.

## 10. Injection de dépendances
Dans `src/di.ts` : instancier le repo, instancier le use case, exporter.

## 11. Enregistrer la route
Dans `src/api/routes/index.ts` : `router.route("/", createXxxRoutes(useCase))`.

## Vérification finale
```bash
bun run typecheck && bun run test && bun run dev
# Tester : curl localhost:3000/api/[endpoint]
```
