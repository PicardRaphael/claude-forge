---
name: validation-checklist
description: Checklist for validating migrated PostgreSQL functions. Compares original SQL function behavior with new application code. Loaded by validator agent.
user-invokable: false
---

# Checklist de validation — Migration PostgreSQL → Applicatif

## 1. Équivalence comportementale

| Check | Comment vérifier |
|-------|-----------------|
| Mêmes entrées | Les paramètres de la fonction SQL correspondent aux paramètres de l'endpoint |
| Mêmes sorties | Les colonnes retournées par la fonction = les champs de la réponse API |
| Mêmes filtres | Chaque WHERE de la fonction est reproduit dans la requête applicative |
| Mêmes jointures | Chaque JOIN de la fonction est reproduit (vérifier avec doc/dump/fk.csv) |
| Mêmes conditions | Les CASE WHEN, IF/ELSIF sont reproduits dans la logique applicative |
| Valeurs en dur | Chaque valeur magique (role_id = 1, type = 'H') est identique |
| Soft-delete | Si la fonction filtre `deleted_at IS NULL`, le code aussi |
| Tri | ORDER BY reproduit si pertinent pour l'API |
| Pagination | Si la fonction avait un LIMIT, l'endpoint aussi |

## 2. Qualité SQL

| Check | Règle |
|-------|-------|
| Pas de SELECT * | Colonnes listées explicitement |
| JOIN explicites | Pas de jointure dans WHERE |
| Placeholders | $1, $2 — jamais de concaténation |
| Index couverts | Les colonnes de JOIN et WHERE ont des indexes (vérifier doc/dump/indexes.csv) |
| Pas de N+1 | Pas de requête dans une boucle |
| Pagination | Cursor-based si dataset > 1000 |
| Types numériques | numeric/decimal → string (TS) ou decimal.Decimal (Go), jamais float |

## 3. Qualité code

| Check | Règle |
|-------|-------|
| Conventions respectées | Le code suit les patterns des fichiers existants |
| Types/Structs complets | Entrées et sorties typées, pas de any/interface{} |
| Validation entrées | Paramètres validés avant la requête |
| Gestion erreurs | Erreurs SQL catchées et mappées en HTTP codes |
| Documentation | Commentaire en tête avec source (fonction PostgreSQL de référence) |

## 4. Cohérence projet

| Check | Comment vérifier |
|-------|-----------------|
| Pas de duplication | L'endpoint ne fait pas la même chose qu'un existant |
| Migration tracker | doc/migration-tracker.md mis à jour |
| Règles métier documentées | Les valeurs en dur et filtres implicites sont commentés |
| Dépendances | Si la fonction appelait d'autres fonctions, c'est signalé |

## 5. Régressions potentielles

| Check | Quoi vérifier |
|-------|--------------|
| Fonctions dépendantes | D'autres fonctions PostgreSQL appellent-elles la fonction migrée ? |
| Triggers | Y a-t-il des triggers sur les tables modifiées ? |
| Autres endpoints | D'autres endpoints touchent-ils les mêmes tables ? |
| Effets de bord | La fonction originale avait-elle des effets cachés (logs, audit, notifications) ? |

## Format de sortie du validator

```
## Validation

**Fonction originale :** {schema}.{function_name}
**Endpoint migré :** {méthode} {route}

### Équivalence comportementale
- ✅ | ❌ Mêmes entrées : {détail}
- ✅ | ❌ Mêmes sorties : {détail}
- ✅ | ❌ Mêmes filtres : {détail}
- ✅ | ❌ Mêmes jointures : {détail}
- ✅ | ❌ Valeurs en dur : {détail}

### Qualité
- ✅ | ❌ SQL : {détail}
- ✅ | ❌ Code : {détail}
- ✅ | ❌ Types : {détail}

### Régressions
- ✅ | ❌ Dépendances : {détail}

### Verdict : ✅ PASS | ❌ FAIL

### Corrections requises (si FAIL)
1. {correction}
```
