# ADR 0001 — Separate forge-brain and forge-cognition

Status: Accepted

## Decision

Keep Obsidian knowledge/documentation in `mcp-forge-brain` and operational projects, memories, outcomes and calibration in `mcp-forge-cognition` with sibling store `cognition-store/`.

## Consequences

Each domain keeps a small trust boundary and lifecycle. Cross-system access is explicit and read-only. There is no automatic vault migration.
