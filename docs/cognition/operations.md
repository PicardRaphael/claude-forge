# Operations

Use Python 3.11 through `uv`. Run tests before starting a profile. Rebuild one profile with `forge-cognition rebuild-index --profile <profile>` and verify all canonical/index invariants with `forge-cognition verify-store --profile curator`.

## Backup and restore

Back up `cognition-store/` through Git. SQLite indexes do not need backup. To restore, check out canonical Markdown/YAML/JSONL, remove local SQLite projections if necessary, run all three rebuild commands, then run `verify-store`.

## Migration

Increment `STORE_VERSION`, add a versioned schema and write a deterministic file migration with a dry run and rollback. Rebuild indexes only after canonical files validate. No migration copies the existing Obsidian vault automatically.

## Failure handling

A conflict returns the current hash and leaves files unchanged. An idempotency key reused with different data is rejected. A lock timeout is retryable. Index or audit failure triggers rollback; run `verify-store` before retrying if the process was terminated externally.
