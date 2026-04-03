# Skill Navigator Rule - MANDATORY

## Quand consulter ce guide

- La tache touche **2+ domaines** (tables + fonctions + SQL)
- Tu n'es **pas sur** quelle skill charger
- La demande est **ambigue**

## Decision Tree

### "Je dois MIGRER une fonction"
| Quoi ? | Skill |
|--------|-------|
| Migrer f_xxx vers un endpoint | `migrate-function` |
| Creer un endpoint from scratch | `create-endpoint` |
| Modifier un endpoint existant | `update-endpoint` |
| Pas sur si migration ou creation | Lire la demande : mentionne une fonction = migration, mentionne un besoin = creation |

### "Je dois ecrire du SQL"
| Quoi ? | Skill |
|--------|-------|
| Regles de base (jointures, placeholders, anti-patterns) | `sql-best-practices` |
| Indexing avance, partitioning, EXPLAIN | `sql-best-practices/references/advanced-optimization.md` |
| Patterns TypeScript + PostgreSQL | `sql-best-practices/references/typescript-patterns.md` |
| Patterns Go + PostgreSQL | `sql-best-practices/references/go-patterns.md` |
| Optimiser une requete specifique | Agent `sql-optimizer` (pas une skill) |

### "Je dois comprendre la BDD"
| Quoi ? | Skill |
|--------|-------|
| Config (chemin repo, stack) | `schema-context` |
| Structure des CSV / MCP | `schema-data-source` |
| Format des docs generes | `schema-output-format` |
| Lire les domaines documentes | `doc/schemas/*.md` directement |

### "Je dois valider / auditer"
| Quoi ? | Skill |
|--------|-------|
| Equivalence migration (original vs migre) | `validation-checklist` |
| Securite (injection, auth, deps) | `security-checklist` |
| Debugging (diagnostic, error mapping) | `debugging-methodology` + `error-patterns` |

### "Je dois designer une API"
| Quoi ? | Skill |
|--------|-------|
| Routes, methodes, pagination, erreurs | `api-design-patterns` |

### "Je dois suivre la migration"
| Quoi ? | Skill |
|--------|-------|
| Avancement, tracker | `migration-status` |

## Competing Skills — Boundary Table

| Situation | Use THIS | Not THAT |
|-----------|----------|----------|
| Migrer une fonction existante | `migrate-function` | `create-endpoint` (pas de fonction source) |
| Creer un endpoint sans fonction source | `create-endpoint` | `migrate-function` (pas de migration) |
| Modifier un endpoint existant | `update-endpoint` | `create-endpoint` (endpoint existe deja) |
| SQL de base (regles) | `sql-best-practices` | `sql-optimizer` agent (optimisation specifique) |
| Optimiser une requete precise | `sql-optimizer` agent | `sql-best-practices` (reference, pas action) |
| Comprendre la BDD (structure) | `schema-data-source` | `schema-context` (config seulement) |
| Bug applicatif | `debugging-methodology` | `validation-checklist` (equivalence migration) |
| Regression de migration | `validation-checklist` | `debugging-methodology` (bug general) |
