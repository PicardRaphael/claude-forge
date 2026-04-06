---
name: debugging-methodology
description: Root-cause debugging methodology — 5 levels of investigation, PostgreSQL migration bugs, TypeScript errors. Load when investigating a bug, unexpected behavior, or test failure.
user-invokable: true
argument-hint: "[description of the bug or failing test]"
---

# Debugging Methodology — Root Cause First

**Rule:** Never patch a symptom. Find the root cause, then fix it.

## The 5 levels

Work through these in order. Stop at the level where you find the root cause.

### Level 1 — Reproduce reliably

Before investigating, confirm the bug is reproducible:
```bash
bun test --filter "[FailingTest]"   # Does it fail consistently?
bun run dev                          # Does the server reproduce the issue?
```

If not reproducible → it's a flaky test or race condition (different problem).

### Level 2 — Read the full error

Read the entire error message and stack trace:
- What is the exact error type? (`TypeError`, `ZodError`, `DomainError`, etc.)
- What file and line number?
- What was the call stack?

Common mistakes: reading only the first line, ignoring the stack trace.

### Level 3 — Check the data flow

Trace the request through the hexagonal layers:
```
API Route → Use Case → Repository Interface → Repository Implementation → DB
```

At which layer does the data stop being correct?

```typescript
// Temporary debug logging (remove after fixing)
console.log("[DEBUG route] input:", input);
console.log("[DEBUG use-case] copro:", copro);
console.log("[DEBUG mapper] raw row:", row);
```

### Level 4 — Verify types and contracts

Type errors often manifest as runtime bugs:
```bash
bun run typecheck    # Find all TypeScript errors
```

Check:
- Are the Zod schemas matching the actual DB column types?
- Are mapper functions handling all nullable columns?
- Are use case inputs/outputs typed correctly?

### Level 5 — Isolate with a minimal test

Write a minimal failing test that demonstrates the bug:
```typescript
it("reproduces bug #X", async () => {
  // Minimal setup
  // Exact scenario that fails
  // Assert the expected behavior
});
```

This test becomes the regression test once the bug is fixed.

## PostgreSQL migration bugs — common patterns

### Pattern: Mapper missing a field
**Symptom:** API returns `undefined` for a field that exists in DB
**Cause:** `toEntity()` mapper doesn't include that column
**Fix:** Add the field to the mapper function

### Pattern: Type mismatch on numeric columns
**Symptom:** `NaN` or string where number expected
**Cause:** PostgreSQL returns decimals as strings; Drizzle preserves this
**Fix:** `Number(row.montant)` or use `z.coerce.number()` in Zod schema

### Pattern: NULL vs undefined mismatch
**Symptom:** Condition `if (!value)` triggers when value is `0` or `""`
**Cause:** Falsy check instead of null check
**Fix:** `if (value === null || value === undefined)`

### Pattern: Business rule in PG function not ported
**Symptom:** Old behavior allowed/blocked something the new API doesn't
**Cause:** Rule was implicit in the PG function, not documented
**Fix:** Read the PG function carefully, port the rule to the use case

### Pattern: Zod coercion issue
**Symptom:** Query param arrives as string, `z.number()` rejects it
**Cause:** HTTP query params are always strings
**Fix:** Use `z.coerce.number()` for query params

## Decision tree

```
Bug reported
  ↓
Reproducible? → No → Flaky test / race condition → separate investigation
  ↓ Yes
Type error (tsc)? → Yes → Fix TypeScript types first
  ↓ No
Test failure? → Yes → Write minimal failing test → find root cause
  ↓ No
Runtime error? → Yes → Add debug logging at each layer → find where data corrupts
  ↓ No
Wrong output (no error)? → Trace data flow → check mapper → check business rule
```

## After fixing

1. Remove all debug `console.log` statements
2. Confirm the test that reproduced the bug now passes
3. Run full test suite: `bun run test`
4. Run typecheck: `bun run typecheck`
5. If the bug was a missing business rule, document it in project memory
