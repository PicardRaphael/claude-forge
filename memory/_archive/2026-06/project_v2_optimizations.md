---
name: v2-optimizations-back-refacto
description: Optimisations V2 pour Neoteem backend. Certaines resolues (stack choisi), reste Domain Leads, Scribe, Test TDD.
type: project
---

## V2 — Optimisations restantes

### Resolus (2026-04-04)
- Stack choisi : TypeScript (Bun + Hono + Drizzle)
- Skills specifiques stack : integrees dans le kit fusionne (15 skills)
- Modeles agents : ajustes dans le kit fusionne

### Encore pertinents
- **Domain Leads** : un agent lead par domaine metier (copro, gestion loc, compta...). Pertinent quand schema-mapper aura identifie les domaines.
- **Scribe agent** : capture les decisions d'architecture au fil des sessions. Empêche la perte de connaissance sur 1000+ fonctions.
- **Test agent TDD** : avec une vraie BDD de test, execute le code migre et compare avec la fonction PG originale.
- **Agent Teams** (TeamCreate) quand le flag experimental sera stable
- MCP `timescale/pg-aiguide` pour sql-best-practices (si autorise par l'entreprise)

**Why:** La V1 est prete et deployee. La V2 s'active quand les domaines sont identifies et le volume de travail parallele le justifie.

**How to apply:** Proposer les optimisations V2 quand l'utilisateur commence a travailler activement sur la migration (pas avant).
