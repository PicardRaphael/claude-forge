---
name: error-patterns
description: Error handling patterns for PostgreSQL migration - maps PostgreSQL errors to HTTP codes, logging patterns, common migration error scenarios. Loaded by debugger agent.
user-invokable: false
---

# Error Patterns

## Mapping erreurs PostgreSQL → HTTP

| Code PostgreSQL | Signification | HTTP | Réponse |
|----------------|---------------|------|---------|
| `23505` | Unique violation | 409 Conflict | "Resource already exists" |
| `23503` | FK violation | 404 / 422 | "Referenced resource not found" |
| `23502` | NOT NULL violation | 400 | "Field X is required" |
| `23514` | CHECK violation | 422 | "Value out of range" |
| `22P02` | Invalid text representation | 400 | "Invalid format for field X" |
| `42P01` | Undefined table | 500 | Log + "Internal server error" |
| `42703` | Undefined column | 500 | Log + "Internal server error" |
| `57014` | Query cancelled (timeout) | 504 | "Request timeout" |
| `53300` | Too many connections | 503 | "Service temporarily unavailable" |

**Règle :** Les erreurs 42xxx et 53xxx ne doivent JAMAIS arriver en prod — c'est un bug de code ou d'infra.

## Patterns de logging

### Ce qu'il faut logger
```
[ERROR] {timestamp} {request_id} {endpoint} {user_id}
  message: {description humaine}
  pg_code: {code PostgreSQL si applicable}
  query: {requête SQL masquée — pas les valeurs des paramètres}
  stack: {stack trace}
```

### Ce qu'il ne faut JAMAIS logger
- Mots de passe
- Tokens
- Données personnelles (email, téléphone)
- Valeurs des paramètres SQL (peuvent contenir des données sensibles)

## Erreurs typiques de migration

| Symptôme | Cause probable | Diagnostic |
|----------|---------------|-----------|
| 404 sur un endpoint migré | Route mal définie ou paramètre manquant | Comparer la route avec le plan de l'architecte |
| 500 "column does not exist" | Nom de colonne changé ou typo dans la requête SQL | Vérifier doc/dump/columns.csv |
| Résultats vides inattendus | Filtre soft-delete manquant OU valeur en dur incorrecte | Comparer chaque WHERE avec la fonction originale |
| Doublon dans les résultats | JOIN mal conditionné | Vérifier les FK dans doc/dump/fk.csv |
| Erreur de type (string vs number) | Mapping type incorrect (numeric PostgreSQL → float au lieu de string) | Vérifier le mapping types dans sql-best-practices |
| Timeout | Index manquant sur colonne de filtre | Vérifier doc/dump/indexes.csv |
| 409 Conflict inattendu | Unique constraint non documentée | Vérifier doc/dump/indexes.csv (is_unique) |

## Pattern de gestion d'erreur dans le code

### TypeScript
```typescript
try {
  const result = await db.query(sql, params);
  return result.rows;
} catch (err) {
  if (err instanceof DatabaseError) {
    switch (err.code) {
      case '23505': throw new ConflictError(err.detail);
      case '23503': throw new NotFoundError('Referenced resource not found');
      default: 
        logger.error({ pg_code: err.code, query: sql, err });
        throw new InternalError();
    }
  }
  throw err;
}
```

### Go
```go
var pgErr *pgconn.PgError
if errors.As(err, &pgErr) {
    switch pgErr.Code {
    case "23505":
        return nil, ErrConflict
    case "23503":
        return nil, ErrNotFound
    default:
        slog.Error("db error", "pg_code", pgErr.Code, "query", sql, "err", err)
        return nil, ErrInternal
    }
}
```

## Apprentissage

Après chaque debug, sauvegarder en mémoire :
- Nouveaux codes d'erreur PostgreSQL rencontrés
- Patterns d'erreur spécifiques au projet
- Erreurs récurrentes (même cause dans plusieurs endpoints)
