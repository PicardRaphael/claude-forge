---
name: security-checklist
description: Security audit checklist adapted for PostgreSQL migration projects - SQL injection, auth, data exposure, dependency scanning, OWASP Top 10 adapted. Loaded by security-auditor agent.
user-invokable: false
---

# Security Checklist

## Priorité #1 — Injection SQL

C'est la surface d'attaque #1 de ce projet (migration SQL → applicatif).

### FAIL automatique si :
- Concaténation de string dans une requête SQL
- Template literal avec des variables utilisateur dans une requête
- `req.params`, `req.body`, `req.query` utilisé directement dans du SQL

### Vérification
```
Grep pattern="query\(`.*\$\{|query\(.*\+.*req\.|Exec.*fmt\.Sprintf.*req\." path="src/"
```

### Pattern correct
```sql
-- TOUJOURS : placeholders
SELECT * FROM users WHERE id = $1 AND active = $2
-- JAMAIS : concaténation
SELECT * FROM users WHERE id = ' + req.params.id + '
```

## Priorité #2 — Authentification / Autorisation

### Checks
- [ ] Chaque endpoint a un middleware d'authentification (sauf les publics explicitement listés)
- [ ] Les endpoints de modification (POST/PUT/PATCH/DELETE) vérifient les rôles/permissions
- [ ] Les tokens JWT ont une expiration raisonnable
- [ ] Les endpoints ne permettent pas d'accéder aux données d'un autre utilisateur (IDOR)

### Pattern IDOR (Insecure Direct Object Reference)
```
// VULNÉRABLE — l'utilisateur peut accéder à n'importe quelle copro
GET /copros/:id

// SÉCURISÉ — vérifier que l'utilisateur a le droit
GET /copros/:id → WHERE id = $1 AND (owner_id = $currentUserId OR role = 'admin')
```

## Priorité #3 — Exposition de données

### FAIL automatique si :
- Un endpoint retourne des mots de passe (même hashés)
- Un endpoint retourne des tokens ou clés API
- Un endpoint retourne des données sensibles non nécessaires (email, téléphone dans une liste publique)

### Vérification
```
Grep pattern="password|token|secret|api_key|private_key" path="src/" --type ts
```
Vérifier que ces champs ne sont JAMAIS dans les types de réponse.

## Priorité #4 — Validation des entrées

### Checks
- [ ] Chaque paramètre d'entrée est typé et validé
- [ ] Les IDs sont des nombres (pas des strings arbitraires)
- [ ] Les strings ont une longueur max
- [ ] Les enums sont validés contre une liste blanche
- [ ] Les dates sont parsées correctement

### Pattern
```typescript
// Validation avec zod (TS)
const schema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(255),
  status: z.enum(['active', 'inactive']),
});
```

## Priorité #5 — Configuration

### Checks
- [ ] Pas de secrets hardcodés dans le code
- [ ] CORS configuré (pas `*` en prod)
- [ ] Rate limiting activé sur les endpoints publics
- [ ] Headers de sécurité (HSTS, X-Content-Type-Options, X-Frame-Options)
- [ ] Variables d'environnement pour les secrets

### Vérification secrets hardcodés
```
Grep pattern="password\s*=\s*['\"]|secret\s*=\s*['\"]|api_key\s*=\s*['\"]" path="src/"
```

## Priorité #6 — Dépendances

### Commandes d'audit
```bash
# TypeScript
npm audit
npx audit-ci --critical

# Go
govulncheck ./...
```

### Sévérité
- CVE critique ou haute → FAIL
- CVE moyenne → avertissement
- CVE basse → informatif

## Apprentissage

Après chaque audit, sauvegarder en mémoire :
- Patterns de sécurité validés (middleware auth, validation)
- Vulnérabilités trouvées et corrigées (pour ne pas les reproduire)
- Dépendances à risque identifiées
