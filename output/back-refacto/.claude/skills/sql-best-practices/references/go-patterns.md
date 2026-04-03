# Go + PostgreSQL — Patterns type-safe

## Driver recommandé

`pgx/v5` (jackc/pgx) — le standard Go pour PostgreSQL. Supporte les types natifs, le COPY protocol, et les prepared statements.

## Typage des résultats

```go
// Toujours une struct typée
type Copropriete struct {
    ID        int64           `db:"id"`
    Name      string          `db:"name"`
    Active    bool            `db:"active"`
    Budget    decimal.Decimal `db:"budget"`    // shopspring/decimal — jamais float64
    CreatedAt time.Time       `db:"created_at"`
    DeletedAt *time.Time      `db:"deleted_at"` // nullable → pointeur
}
```

## Mapping types PostgreSQL → Go

| PostgreSQL | Go | Note |
|-----------|-----|------|
| `integer` | `int32` | |
| `bigint` | `int64` | |
| `numeric`, `decimal` | `decimal.Decimal` | JAMAIS `float64` |
| `boolean` | `bool` | |
| `text`, `varchar` | `string` | |
| `timestamp`, `timestamptz` | `time.Time` | |
| `jsonb` | `json.RawMessage` ou struct typée | |
| `uuid` | `pgtype.UUID` ou `string` | |
| `integer[]` | `[]int32` | pgx supporte nativement |
| nullable | `*Type` ou `pgtype.X` | |

## Paramètres — toujours des placeholders

```go
// CORRECT
row := db.QueryRow(ctx, "SELECT * FROM users WHERE email = $1 AND active = $2", email, true)

// INTERDIT — injection SQL
row := db.QueryRow(ctx, fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email))
```

## Repository pattern

```go
type CoproprieteRepository struct {
    db *pgxpool.Pool
}

func (r *CoproprieteRepository) FindByID(ctx context.Context, id int64) (*Copropriete, error) {
    var c Copropriete
    err := r.db.QueryRow(ctx,
        `SELECT id, name, active, budget, created_at, deleted_at
         FROM coproprietes
         WHERE id = $1 AND deleted_at IS NULL`,
        id,
    ).Scan(&c.ID, &c.Name, &c.Active, &c.Budget, &c.CreatedAt, &c.DeletedAt)

    if errors.Is(err, pgx.ErrNoRows) {
        return nil, nil
    }
    return &c, err
}

func (r *CoproprieteRepository) FindByFilters(ctx context.Context, f CoproFilters) ([]Copropriete, error) {
    var conditions []string
    var params []any
    paramIdx := 1

    conditions = append(conditions, "deleted_at IS NULL")

    if f.Active != nil {
        conditions = append(conditions, fmt.Sprintf("active = $%d", paramIdx))
        params = append(params, *f.Active)
        paramIdx++
    }
    if f.Search != "" {
        conditions = append(conditions, fmt.Sprintf("name ILIKE $%d", paramIdx))
        params = append(params, "%"+f.Search+"%")
        paramIdx++
    }

    // Cursor-based pagination
    if f.AfterID > 0 {
        conditions = append(conditions, fmt.Sprintf("id > $%d", paramIdx))
        params = append(params, f.AfterID)
        paramIdx++
    }

    limit := f.Limit
    if limit == 0 {
        limit = 20
    }
    params = append(params, limit)

    query := fmt.Sprintf(
        `SELECT id, name, active, budget, created_at
         FROM coproprietes
         WHERE %s
         ORDER BY id
         LIMIT $%d`,
        strings.Join(conditions, " AND "), paramIdx,
    )

    rows, err := r.db.Query(ctx, query, params...)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var results []Copropriete
    for rows.Next() {
        var c Copropriete
        if err := rows.Scan(&c.ID, &c.Name, &c.Active, &c.Budget, &c.CreatedAt); err != nil {
            return nil, err
        }
        results = append(results, c)
    }
    return results, rows.Err()
}
```

## Transaction pattern

```go
func (r *CoproprieteRepository) TransferBudget(ctx context.Context, fromID, toID int64, amount decimal.Decimal) error {
    tx, err := r.db.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback(ctx) // no-op si commit réussi

    _, err = tx.Exec(ctx,
        "UPDATE coproprietes SET budget = budget - $1::numeric WHERE id = $2",
        amount, fromID,
    )
    if err != nil {
        return err
    }

    _, err = tx.Exec(ctx,
        "UPDATE coproprietes SET budget = budget + $1::numeric WHERE id = $2",
        amount, toID,
    )
    if err != nil {
        return err
    }

    return tx.Commit(ctx)
}
```

## Bulk insert avec COPY protocol

```go
func (r *CoproprieteRepository) BulkInsertLots(ctx context.Context, lots []NewLot) error {
    _, err := r.db.CopyFrom(
        ctx,
        pgx.Identifier{"lot_copro"},
        []string{"copropriete_id", "numero", "type", "tantieme"},
        pgx.CopyFromSlice(len(lots), func(i int) ([]any, error) {
            return []any{lots[i].CoproprieteID, lots[i].Numero, lots[i].Type, lots[i].Tantieme}, nil
        }),
    )
    return err
}
```

## Batch queries (pgx)

```go
// Envoyer plusieurs requêtes en un round-trip
batch := &pgx.Batch{}
batch.Queue("SELECT * FROM coproprietes WHERE id = $1", id1)
batch.Queue("SELECT COUNT(*) FROM lot_copro WHERE copropriete_id = $1", id1)

br := db.SendBatch(ctx, batch)
defer br.Close()

var copro Copropriete
br.QueryRow().Scan(&copro.ID, &copro.Name, ...)

var count int
br.QueryRow().Scan(&count)
```

## Error handling

```go
import "github.com/jackc/pgx/v5/pgconn"

var pgErr *pgconn.PgError
if errors.As(err, &pgErr) {
    switch pgErr.Code {
    case "23505": // unique_violation
        return ErrConflict
    case "23503": // foreign_key_violation
        return ErrNotFound
    }
}
```

## Connection pool

```go
config, _ := pgxpool.ParseConfig("postgresql://user:pass@host:5432/db")
config.MaxConns = 25                        // ~2x vCPU
config.MinConns = 5
config.MaxConnLifetime = 30 * time.Minute
config.MaxConnIdleTime = 5 * time.Minute
config.HealthCheckPeriod = 30 * time.Second

pool, err := pgxpool.NewWithConfig(ctx, config)
```
