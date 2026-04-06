---
name: security-checklist
description: Security audit checklist — SQL injection, authentication, input validation, OWASP Top 10 for this TypeScript/Hono/PostgreSQL API. Load when reviewing security of endpoints or before a release.
user-invokable: true
argument-hint: "[endpoint or module to audit]"
---

# Security Checklist

## 1. SQL Injection

- [ ] All DB queries use Drizzle ORM (parameterized by default)
- [ ] Any raw `sql` tag uses template literals (never string concat)
- [ ] No user input is ever concatenated into a SQL string

```typescript
// ✅ Safe — Drizzle parameterizes
db.select().from(coproprietes).where(eq(coproprietes.id, userId));

// ✅ Safe — sql tag with template literal
db.execute(sql`SELECT * FROM f_get_solde(${coproprieteId})`);

// ❌ UNSAFE — string concat
db.execute(sql.raw(`SELECT * FROM coproprietes WHERE id = '${userId}'`));
```

## 2. Authentication

- [ ] All non-public endpoints require `Authorization: Bearer <API_KEY>` header
- [ ] The `auth` middleware is applied at the app level or explicitly per route
- [ ] API key is loaded from environment variable, not hardcoded
- [ ] API key is at least 32 characters long
- [ ] API key comparison uses constant-time comparison (no timing attacks)

```typescript
// In src/api/middleware/auth.ts — ensure timing-safe comparison
import { timingSafeEqual } from "crypto";
```

## 3. Input validation

- [ ] All route inputs (params, query, body) are validated with Zod schemas
- [ ] UUID params use `z.string().uuid()` (prevents injection via malformed IDs)
- [ ] Pagination params use `z.coerce.number().int().min(1).max(100)` (prevents DoS)
- [ ] String inputs have `.max()` length limits where appropriate
- [ ] No `z.any()` in request schemas

## 4. Output sanitization

- [ ] No internal error details (stack traces, DB errors) in 500 responses
- [ ] No sensitive fields (passwords, tokens, PG function internals) in responses
- [ ] Error messages don't reveal whether a resource exists for unauthenticated users

## 5. Environment variables

- [ ] Validated with Zod at startup (`src/shared/config/env.ts`)
- [ ] `.env` is in `.gitignore`
- [ ] Only `.env.example` with placeholder values is committed
- [ ] `DATABASE_URL` uses SSL in production (`?sslmode=require`)

## 6. Dependencies

- [ ] No known CVEs in dependencies (`bun audit` or `npm audit`)
- [ ] `@hono/zod-openapi` and `drizzle-orm` are up to date
- [ ] No unused packages in `package.json`

## 7. OWASP Top 10 (relevant to this API)

| Risk | Status | Notes |
|---|---|---|
| A01 Broken Access Control | Check per endpoint | All routes behind auth middleware? |
| A02 Cryptographic Failures | N/A V1 | No user passwords stored |
| A03 Injection | Drizzle ORM | All queries parameterized |
| A04 Insecure Design | Architecture | Hexagonal, DomainErrors, no logic in routes |
| A05 Security Misconfiguration | Env vars | Validated at startup |
| A06 Vulnerable Components | bun audit | Check periodically |
| A07 Auth Failures | API key | Review key rotation policy |
| A08 Data Integrity | Zod validation | All inputs validated |
| A09 Logging Failures | error-handler | Logs 500s without exposing details |
| A10 SSRF | N/A | No outbound HTTP calls in V1 |

## 8. PostgreSQL function access

- [ ] The app connects to PostgreSQL with a **read/write user** (not superuser)
- [ ] The DB user does NOT have `DROP`, `CREATE TABLE`, `ALTER TABLE` permissions
- [ ] The repo containing PostgreSQL functions is READ-ONLY — never modified by the app

## Quick audit command

```bash
bun run typecheck    # Type safety
bun run test         # All tests including error cases
grep -r "any" src/   # Hunt for 'any' types
grep -r "sql.raw" src/  # Hunt for raw SQL
```
