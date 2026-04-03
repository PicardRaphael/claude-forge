---
name: api-design-patterns
description: REST API design patterns - route naming, HTTP methods, status codes, pagination, filtering, versioning, error responses. Loaded by architect for endpoint design.
user-invokable: false
---

# API Design Patterns

## Nommage des routes

```
GET    /copros                    → liste (collection)
GET    /copros/:id                → détail (ressource)
POST   /copros                    → créer
PUT    /copros/:id                → remplacer entièrement
PATCH  /copros/:id                → modifier partiellement
DELETE /copros/:id                → supprimer

GET    /copros/:id/lots           → sous-collection
GET    /copros/:id/lots/:lotId    → sous-ressource
```

### Règles nommage
- Pluriel pour les collections : `/copros` pas `/copro`
- Kebab-case : `/appels-fonds` pas `/appels_fonds`
- Pas de verbes dans l'URL : `/copros` pas `/getCopros`
- Nesting max 2 niveaux : `/copros/:id/lots` OK, `/copros/:id/lots/:lotId/tantiemes` → aplatir

## Codes HTTP

| Code | Quand |
|------|-------|
| 200 | GET réussi, PUT/PATCH réussi |
| 201 | POST créé (+ header Location) |
| 204 | DELETE réussi (pas de body) |
| 400 | Validation échouée (paramètres invalides) |
| 401 | Non authentifié |
| 403 | Authentifié mais pas autorisé |
| 404 | Ressource non trouvée |
| 409 | Conflit (doublon, version conflict) |
| 422 | Entité non traitable (validation métier) |
| 500 | Erreur serveur inattendue |

## Pagination

### Réponse paginée standard
```json
{
  "data": [...],
  "pagination": {
    "cursor": "abc123",
    "hasMore": true,
    "total": 1523
  }
}
```

### Paramètres
- `?limit=20` — nombre de résultats (max 100, default 20)
- `?cursor=abc123` — cursor-based (OBLIGATOIRE si dataset > 1000)
- `?offset=40` — acceptable uniquement pour petits datasets

## Filtrage

```
GET /copros?active=true&search=rivoli&sort=-created_at
```

- Filtres exacts : `?status=active`
- Recherche texte : `?search=mot`
- Tri : `?sort=name` (asc) ou `?sort=-name` (desc)
- Filtres dates : `?created_after=2025-01-01&created_before=2026-01-01`

## Format d'erreur standard

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Le champ 'name' est obligatoire",
    "details": [
      { "field": "name", "message": "required" }
    ]
  }
}
```

## Versioning

Préférer le header : `Accept: application/vnd.api+json; version=1`
Alternative : préfixe URL `/v1/copros` (plus simple mais moins flexible)

## Apprentissage

Sauvegarder en mémoire projet :
- Conventions de nommage choisies par l'équipe
- Format d'erreur validé
- Stratégie de pagination confirmée
