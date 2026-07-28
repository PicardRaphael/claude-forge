# Project brainstorm handoffs

Five strict payloads are versioned under `cognition-store/schemas/`:

- `cdc-handoff-v1`
- `architecture-handoff-v1`
- `review-packet-v1`
- `review-verdict-v1`
- `development-handoff-v1`

`pipeline-state-v1` stores current pointers, active grants, stage, consecutive
reworks and the latest scoped human decision. Every artifact revision is a new
v1 cognition document with a new ULID, increasing revision, `supersedes` link and
content hash. Existing envelope schemas and `STORE_VERSION=1` remain unchanged.
Stale or forked chains are rejected.

The development handoff binds approved CDC, architecture and verdict and carries
ADRs, slices, acceptance criteria, tests, risks and reviewer conditions. Map one
slice into a new DEV `00-task.md`; never treat the handoff as application code.
