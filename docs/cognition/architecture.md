# Architecture

`mcp-forge-brain` owns general knowledge, Obsidian notes, wikilinks, watch material and documentation. `mcp-forge-cognition` owns operational state and outcome-grounded learning. `cognition-store/` is a sibling of the vault, never a child.

The implementation follows a pragmatic Clean Architecture:

- `domain/`: entities, lifecycle transitions, access policy, learning thresholds and calibration formulas; no FastMCP, SQLite or filesystem imports.
- `application/`: authorized use cases and ports.
- `infrastructure/`: canonical files, FTS5 projections, audit, lock, atomic mutation, clock, IDs and verification.
- `presentation/mcp/`: typed inputs, fixed-principal tool registration and non-revealing error mapping.

Mutation order is validation → authorization → lock → current state/hash → temporary write/atomic replace → index rebuild → audit event → unlock. Any exception, including interruption, restores prior files, truncates a partial audit append and rebuilds indexes from canonical files.

V1 uses one global mutation lock. This makes the safety argument small and testable. A future sharded lock must preserve cross-document transactions and idempotency semantics.
