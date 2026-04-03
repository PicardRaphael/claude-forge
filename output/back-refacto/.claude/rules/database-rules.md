# Database Rules - MANDATORY

## Structure only — JAMAIS les donnees

Via MCP ou CSV, on ne recupere que la STRUCTURE (tables, colonnes, FK, indexes, triggers).
On ne fait JAMAIS de SELECT sur les donnees des tables.

## SQL dans le code applicatif

### OBLIGATOIRE
- Placeholders `$1, $2` — jamais de concatenation de string
- Lister les colonnes explicitement — jamais de `SELECT *`
- `JOIN ... ON` explicite — jamais de jointure dans WHERE
- Filtre soft-delete (`deleted_at IS NULL`) si applicable
- Cursor-based pagination si dataset > 1000 lignes
- `CREATE INDEX CONCURRENTLY` en production

### INTERDIT
- Concatenation de variables utilisateur dans du SQL (injection)
- `OFFSET > 1000` (utiliser cursor-based)
- `float` pour les montants (utiliser string en TS, decimal.Decimal en Go)
- `SELECT *`
- Jointure implicite dans WHERE

## Repo fonctions PostgreSQL

- **LECTURE SEULE** — ne JAMAIS modifier les fichiers du repo fonctions
- Les fonctions sont une REFERENCE pour comprendre la logique metier
- Ne pas copier les requetes telles quelles — les adapter et optimiser
- Documenter les regles metier decouvertes dans chaque fonction

## Migration tracker

Apres chaque migration, mettre a jour `doc/migration-tracker.md` :
- Passer la fonction de ⬜ a ✅
- Ajouter l'endpoint, la date
- Recalculer les pourcentages
