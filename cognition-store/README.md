# cognition-store

Canonical, Git-versioned operational cognition store for `mcp-forge-cognition`.

- Markdown and YAML files are authoritative.
- `indexes/` contains disposable per-profile SQLite projections.
- `audit/events.jsonl` is append-only and contains metadata, hashes and safe results, never full documents.
- Agents write candidates to their inbox or private/project-authorized zones. Only Curator promotes shared memories.
- Project-brainstorm handoffs and state are append-only v1 documents with strict payload schemas; base document/project schemas remain unchanged.

Do not place this directory inside `vault/claude-forge/`.
