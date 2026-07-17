# ADR 0005 — No embeddings in v1

Status: Accepted

## Decision

Start with deterministic SQLite FTS5 ranking and no vector or graph engine.

## Consequences

The system has no external infrastructure, lower leakage surface and simple rebuilds. Semantic retrieval requires a labeled benchmark and measurable gain.
