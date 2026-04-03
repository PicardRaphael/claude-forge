# TypeScript + PostgreSQL — Patterns type-safe

## Driver recommandé

`pg` (node-postgres) ou `postgres` (postgres.js) avec types génériques.

## Typage des résultats

```typescript
// Toujours définir une interface pour le résultat
interface Copropriete {
  id: number;
  name: string;
  active: boolean;
  budget: string;        // numeric PostgreSQL → string (précision décimale)
  created_at: Date;
  deleted_at: Date | null;
}

// Query typée
const result = await db.query<Copropriete>(
  'SELECT id, name, active, budget, created_at, deleted_at FROM coproprietes WHERE id = $1',
  [id]
);
const copro: Copropriete = result.rows[0];
```

## Mapping types PostgreSQL → TypeScript

| PostgreSQL | TypeScript | Note |
|-----------|-----------|------|
| `integer`, `bigint` | `number` | bigint > 2^53 → `string` ou `BigInt` |
| `numeric`, `decimal`, `money` | `string` | JAMAIS `number` (perte de précision) |
| `boolean` | `boolean` | |
| `text`, `varchar` | `string` | |
| `timestamp`, `timestamptz` | `Date` | |
| `jsonb` | `Record<string, unknown>` | Typer plus précisément si possible |
| `uuid` | `string` | |
| `integer[]` | `number[]` | |

## Paramètres — toujours des placeholders

```typescript
// CORRECT
const result = await db.query('SELECT * FROM users WHERE email = $1 AND active = $2', [email, true]);

// INTERDIT — injection SQL
const result = await db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

## Repository pattern

```typescript
class CoproprieteRepository {
  constructor(private db: Pool) {}

  async findById(id: number): Promise<Copropriete | null> {
    const { rows } = await this.db.query<Copropriete>(
      `SELECT id, name, active, budget, created_at
       FROM coproprietes
       WHERE id = $1 AND deleted_at IS NULL`,
      [id]
    );
    return rows[0] ?? null;
  }

  async findByFilters(filters: CoproFilters): Promise<PaginatedResult<Copropriete>> {
    const conditions: string[] = ['deleted_at IS NULL'];
    const params: unknown[] = [];
    let paramIndex = 1;

    if (filters.active !== undefined) {
      conditions.push(`active = $${paramIndex++}`);
      params.push(filters.active);
    }
    if (filters.search) {
      conditions.push(`name ILIKE $${paramIndex++}`);
      params.push(`%${filters.search}%`);
    }

    // Cursor-based pagination
    if (filters.afterId) {
      conditions.push(`id > $${paramIndex++}`);
      params.push(filters.afterId);
    }

    params.push(filters.limit ?? 20);

    const { rows } = await this.db.query<Copropriete>(
      `SELECT id, name, active, budget, created_at
       FROM coproprietes
       WHERE ${conditions.join(' AND ')}
       ORDER BY id
       LIMIT $${paramIndex}`,
      params
    );

    return {
      data: rows,
      nextCursor: rows.length > 0 ? rows[rows.length - 1].id : null,
    };
  }
}
```

## Transaction pattern

```typescript
async function transferBudget(fromId: number, toId: number, amount: string): Promise<void> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    await client.query(
      'UPDATE coproprietes SET budget = budget - $1::numeric WHERE id = $2',
      [amount, fromId]
    );
    await client.query(
      'UPDATE coproprietes SET budget = budget + $1::numeric WHERE id = $2',
      [amount, toId]
    );

    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

## Bulk insert

```typescript
// UNNEST pour insert multi-lignes en une requête
async function insertLots(lots: NewLot[]): Promise<void> {
  await db.query(
    `INSERT INTO lot_copro (copropriete_id, numero, type, tantieme)
     SELECT * FROM UNNEST($1::int[], $2::text[], $3::text[], $4::numeric[])`,
    [
      lots.map(l => l.coproprieteId),
      lots.map(l => l.numero),
      lots.map(l => l.type),
      lots.map(l => l.tantieme),
    ]
  );
}
```

## Error handling

```typescript
import { DatabaseError } from 'pg';

try {
  await db.query('INSERT INTO users (email) VALUES ($1)', [email]);
} catch (err) {
  if (err instanceof DatabaseError) {
    if (err.code === '23505') {
      // Unique violation
      throw new ConflictError('Email already exists');
    }
    if (err.code === '23503') {
      // Foreign key violation
      throw new NotFoundError('Referenced entity does not exist');
    }
  }
  throw err;
}
```
