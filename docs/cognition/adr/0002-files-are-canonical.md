# ADR 0002 — Files are canonical

Status: Accepted

## Decision

Use validated Markdown/YAML plus append-only JSONL as source of truth. SQLite is a disposable projection.

## Consequences

Git gives review, rollback and portability. Writes require atomic replacement and verification; query performance comes from rebuildable indexes.
