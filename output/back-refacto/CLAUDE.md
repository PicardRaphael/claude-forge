# Back Refacto — Migration PostgreSQL → Applicatif

## Contexte

Migration d'un back-end full PostgreSQL (200+ tables, 1000+ fonctions) vers une architecture applicative.

## Config

- Repo fonctions : [À CONFIGURER — chemin absolu vers le repo des fonctions SQL]
- Stack : [À CONFIGURER — typescript | go]
- Doc schéma : doc/schemas/
- Export tables : doc/dump/

## Conventions fonctions PostgreSQL

| Préfixe | Rôle |
|---------|------|
| `f_*` | Lecture (SELECT) |
| `p_*` | Écriture (INSERT/UPDATE/DELETE) |
| `proc_*` | Procédure (orchestration) |
| `tr_*` | Trigger |

## Standards de code

- SQL : jamais SELECT *, jamais de jointure implicite, toujours placeholders $1 $2
- numeric/decimal → string (TS) ou decimal.Decimal (Go), jamais float
- Toujours filtrer soft-delete si applicable
- Pagination cursor-based si dataset > 1000
- Chaque endpoint documenté avec sa source (fonction PostgreSQL de référence)

## Règles projet

- Ne JAMAIS modifier ou supprimer les fichiers du repo fonctions
- Les fonctions existantes sont une RÉFÉRENCE, pas une implémentation à copier
- Mettre à jour doc/migration-tracker.md après chaque migration
- Documenter les règles métier découvertes en mémoire projet

## Architecture cible

[À DÉFINIR quand le stack sera choisi]
