# mcp-forge-cognition

`mcp-forge-cognition` manages operational memory, project state, evidence, hypotheses, decisions, experiments, outcomes, learned procedures and calibration. It is deliberately separate from `mcp-forge-brain`, which remains the Obsidian knowledge/documentation server.

## Security properties

- The principal is fixed by `--profile` at process startup and is absent from every tool input.
- Tools are business operations; there is no generic file/path/list/move/delete tool.
- Product, Architect and Reviewer write candidates/private memories to separate namespaces.
- Only Curator can commit, deprecate, supersede or rebuild.
- Each profile searches a physically separate FTS5 index containing only authorized documents.
- Files are canonical; indexes are disposable.
- Mutations use a lock, expected hashes where relevant, atomic replacement, index rebuild, append-only audit and rollback.

## Install and test

```powershell
cd mcp-forge-cognition
uv sync --python 3.11 --extra dev
uv run --python 3.11 --extra dev python -m pytest -q
```

## Start

The repository-level Claude Code and Codex configurations attach the primary session to the
`curator` profile over stdio. The MCP client starts this process when the session opens and stops
it with the session; no `SessionStart` hook or persistent port is involved. A newly added
project-scoped MCP server may require one-time approval in the client.

Project-brainstorm roles use the isolated global runtime documented in
`docs/agents/project-brainstorm.md`. Every role MCP starts with a fixed principal,
absolute configuration and no wildcard project access. Never attach Curator to a
Product, Architect or Reviewer child.

Manual launch commands:

```powershell
uv run --project mcp-forge-cognition python mcp-forge-cognition/start_stdio.py --profile forge-product
uv run --project mcp-forge-cognition python mcp-forge-cognition/start_stdio.py --profile architect-brainstorm
uv run --project mcp-forge-cognition python mcp-forge-cognition/start_stdio.py --profile red-team
uv run --project mcp-forge-cognition python mcp-forge-cognition/start_stdio.py --profile curator
```

Streamable HTTP is optional:

```powershell
uv run --project mcp-forge-cognition python mcp-forge-cognition/start.py --profile curator
```

## Operations

```powershell
uv run --project mcp-forge-cognition forge-cognition rebuild-index --profile forge-product
uv run --project mcp-forge-cognition forge-cognition rebuild-index --profile red-team
uv run --project mcp-forge-cognition forge-cognition rebuild-index --profile curator
uv run --project mcp-forge-cognition forge-cognition verify-store --profile curator
```

See `mcp.example.json` for launch configuration. Attach only the server matching an agent's role; do not expose the Curator endpoint to Product or Red Team.

## Tool examples

Create a project:

```json
{"name":"Paid pilot","slug":"paid-pilot","objective":"Validate willingness to pay","owner":"raphael","initial_constraints":["No external infrastructure"],"idempotency_key":"project-paid-pilot-v1"}
```

Publish a review packet:

```json
{"project_id":"PRJ-2026-001","source_brief_id":"01J...","included_evidence_ids":[],"included_hypothesis_ids":[],"expected_hash":"sha256:...","idempotency_key":"packet-prj-001-v1"}
```

Curator validation:

```json
{"candidate_id":"01J...","decision":"validated","target_namespace":"shared/context","expected_hash":"sha256:...","idempotency_key":"commit-01J-v1","reason":"Source and outcome verified"}
```

## Known v1 limits

- Lexical FTS5 only; no embeddings, reranker or graph.
- Global store lock favors correctness over high write throughput.
- Pipeline review packets use strict allowlisted fields. Structural neutralization cannot prove semantic neutrality inside otherwise factual text.
- Full production prompts and evaluated Skills are intentionally deferred until their own interview/eval workflow.
