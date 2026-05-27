---
name: db-immutable-check
description: Pour Neoteem, le schema PG est IMMUTABLE. Toujours vérifier que db:generate/db:migrate ne sont pas dans les agents.
type: feedback
---

Dans le projet Neoteem (back2.0), le schéma PostgreSQL est immutable — on ne crée jamais de tables.

**Why:** Le dev agent contenait `bun run db:generate` et `bun run db:migrate` alors que `database-rules` interdit explicitement toute modification du schéma. C'est un bug critique qui aurait pu casser la DB de prod.

**How to apply:** Seule commande autorisée : `bun run db:pull` (introspection). Quand on génère ou audite un agent dev/schema, toujours vérifier qu'il ne contient pas db:generate, db:migrate, db:push. Cette vérification s'applique à tout projet avec DB existante immuable.
