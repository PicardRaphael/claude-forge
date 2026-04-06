# TypeScript + Drizzle Patterns

## Type inference from Drizzle schemas

```typescript
// src/infra/postgres/schema/coproprietes.table.ts
import { pgTable, serial, varchar, integer, timestamp } from "drizzle-orm/pg-core";

export const coproprietes = pgTable("coproprietes", {
  id: serial("id").primaryKey(),
  nom: varchar("nom", { length: 255 }).notNull(),
  syndicId: integer("syndic_id"),
  createdAt: timestamp("created_at").defaultNow(),
});

// Infer the SELECT row type
type CoproprieteRow = typeof coproprietes.$inferSelect;
// { id: number; nom: string; syndicId: number | null; createdAt: Date | null }

// Infer the INSERT type
type NewCopropriete = typeof coproprietes.$inferInsert;
// { nom: string; syndicId?: number | null; createdAt?: Date | null }
```

Use `$inferSelect` and `$inferInsert` — never write manual types for DB rows.

## Mapper pattern with full types

```typescript
// src/infra/postgres/mappers/copropriete.mapper.ts
import type { Copropriete } from "@core/domain/entities/copropriete";
import type { coproprietes } from "../schema/coproprietes.table";

type CoproprieteRow = typeof coproprietes.$inferSelect;

// DB row → Domain entity (pure function)
export function toCopropriete(row: CoproprieteRow): Copropriete {
  return {
    id: String(row.id),              // DB uses integer, domain uses string UUID
    nom: row.nom,
    syndicId: row.syndicId ?? null,  // Explicit null handling
    createdAt: row.createdAt?.toISOString() ?? null,
  };
}

// Domain entity → DB insert row
export function toRow(entity: Omit<Copropriete, "id">): NewCopropriete {
  return {
    nom: entity.nom,
    syndicId: entity.syndicId ? Number(entity.syndicId) : null,
  };
}
```

## Zod schema from domain entity

```typescript
// src/shared/schemas/copropriete.schema.ts
import { z } from "zod";

export const CoproprieteSchema = z.object({
  id: z.string(),
  nom: z.string(),
  syndicId: z.string().nullable(),
  createdAt: z.string().datetime().nullable(),
});

export type CoproprieteDto = z.infer<typeof CoproprieteSchema>;
```

Keep the Zod schema for API responses separate from the domain entity type.
The API response type (DTO) may differ from the domain entity.

## Type-safe WHERE clauses

```typescript
import { eq, and, or, isNull, isNotNull, gte, lte, like, inArray } from "drizzle-orm";

// Single condition
.where(eq(coproprietes.id, id))

// Multiple conditions (AND)
.where(and(
  eq(coproprietes.syndicId, syndicId),
  isNotNull(coproprietes.nom)
))

// OR
.where(or(
  eq(coproprietes.id, "1"),
  eq(coproprietes.id, "2")
))

// Range
.where(and(
  gte(ecritures.date, startDate),
  lte(ecritures.date, endDate)
))

// IN list
.where(inArray(lots.coproprieteId, [1, 2, 3]))

// LIKE (search)
.where(like(coproprietes.nom, `%${search}%`))
```

## Handling optional filters

```typescript
async findAll(filters: {
  syndicId?: string;
  search?: string;
} = {}): Promise<Copropriete[]> {
  const conditions = [];

  if (filters.syndicId) {
    conditions.push(eq(coproprietes.syndicId, Number(filters.syndicId)));
  }
  if (filters.search) {
    conditions.push(like(coproprietes.nom, `%${filters.search}%`));
  }

  const rows = await db
    .select()
    .from(coproprietes)
    .where(conditions.length > 0 ? and(...conditions) : undefined)
    .orderBy(asc(coproprietes.nom));

  return rows.map(toCopropriete);
}
```

## Numeric types from PostgreSQL

PostgreSQL `numeric` / `decimal` columns come back as **strings** from `pg` driver.
Always convert explicitly:

```typescript
// ❌ Will be string "1234.56" at runtime
const montant: number = row.montant;

// ✅ Explicit conversion
const montant = Number(row.montant);

// ✅ Or in Zod schema
const schema = z.object({
  montant: z.string().transform(Number),  // or z.coerce.number()
});
```
