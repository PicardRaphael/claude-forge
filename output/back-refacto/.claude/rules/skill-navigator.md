# Skill Navigator - MANDATORY

## Quand consulter ce guide
- Tâche touche 2+ domaines
- Pas sûr quelle skill charger
- Demande ambiguë

## Decision Tree

### "Je dois CRÉER quelque chose"
| Quoi ? | Skill |
|--------|-------|
| Nouvel endpoint REST | `add-endpoint` (11 étapes) |
| Connecter une table PG existante | `connect-table` |
| Nouvelle erreur métier | `add-error` |

### "Je dois COMPRENDRE l'existant"
| Quoi ? | Skill / Doc |
|--------|------------|
| Architecture hexagonale | `architecture-rules` (auto) + `doc/architecture.md` |
| Conventions REST | `api-conventions` (auto) + `doc/api-design.md` |
| Patterns/anti-patterns | `doc/patterns.md` |
| Erreurs et hiérarchie | `doc/error-handling.md` |
| Conventions code | `doc/conventions.md` |
| Tests | `doc/testing.md` |
| Choix techniques (pour la direction) | `doc/choix-techniques.md` |

### "Je dois écrire du SQL"
| Quoi ? | Skill |
|--------|-------|
| Règles de base | `sql-best-practices` |
| Indexing avancé, EXPLAIN | `sql-best-practices/references/advanced-optimization.md` |
| Patterns TypeScript + Drizzle | `sql-best-practices/references/typescript-patterns.md` |
| Optimiser une requête | Agent `performance-engineer` ou `sql-optimizer` |

### "Je dois valider / auditer"
| Quoi ? | Skill |
|--------|-------|
| Équivalence migration PG → TS | `validation-checklist` |
| Sécurité | `security-checklist` |
| Debugging | `debugging-methodology` + `error-patterns` |

### "Je dois suivre la migration"
| Quoi ? | Skill |
|--------|-------|
| Avancement par domaine | `migration-status` |

### "Je dois analyser la BDD"
| Quoi ? | Skill |
|--------|-------|
| Config (chemin repo, MCP) | `schema-context` |
| Lire structure via MCP/CSV | `schema-data-source` |
| Format docs générés | `schema-output-format` |

## Competing Skills

| Situation | Use THIS | Not THAT |
|-----------|----------|----------|
| Créer un endpoint | `add-endpoint` | `api-design-patterns` (référence) |
| Comprendre conventions REST | `api-conventions` | `add-endpoint` (création) |
| Migrer une fonction PG | Agent `refactor-pg-function` | `add-endpoint` |
| Bug applicatif | `debugging-methodology` | `validation-checklist` |
| Régression migration | `validation-checklist` | `debugging-methodology` |
