# Security model

## Assets and boundaries

- Product private memory and Red Team private memory are mutually confidential.
- Shared context/procedures/calibration require Curator governance.
- Review packets are the only intentional Product-to-Reviewer project handoff.
- Audit logs contain identifiers, action names, request hashes and safe results, never full documents or evidence.

## Enforcement

- Startup profile fixes the `Principal`; tool schemas expose no principal or path.
- `AccessPolicy` denies unknown roots/zones and applies project scope.
- Unauthorized direct-ID access returns the same `not_found` result as an absent resource.
- Empty search is rejected; it cannot enumerate a profile index.
- Three SQLite files are built from ACL-filtered source sets. Missing application filters therefore cannot reveal a private document.
- Store and vault resolvers reject absolute paths, `..`, symlink escapes and unsupported extensions where a file operation exists.
- `mcp-forge-brain` read-only mode does not register mutations or transcript/tool-event search.

## Covered threats

Path traversal, Windows absolute paths, symlink escape, ID guessing, alias/title guessing, empty-query enumeration, profile override, private-term search, stale writes, duplicate retries, partial file/index/audit failure and audit content leakage are covered by negative tests.

## Residual risks

The deterministic neutralizer depends on canonical section headings; semantic persuasion hidden in a factual section requires a future semantic policy check. Local users with direct filesystem access remain outside the MCP threat boundary. HTTP deployment has no authentication layer in v1 and must remain loopback-only or sit behind authenticated transport.
