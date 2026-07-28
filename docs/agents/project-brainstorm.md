# Global Codex project brainstorm

`$project-brainstorm` orchestrates Product -> Architect -> Reviewer and stops
after the independent Reviewer writes terminal `30-review.md`. The parent Codex
task owns user interaction, Curator actions and sequencing. Brainstorm roles
never spawn agents or implement application code. A separate DEV workflow starts
only after a later explicit user implementation request.

New workflows use `brainstorm-product-design@1.3.0`; exact-version resolution
keeps `1.2.0` workflows on their immutable prior definition. After CDC approval,
Architect first records material completeness. A gap produces precise questions,
no research, and no recommendation. Both initial architecture and review rework
then wait in the same Registry phase until the parent appends a USER
`CLARIFICATION` bound to the exact decision-log prefix and blocked-handoff hash.
AUTO-RUN and architect reassignment remain paused until reconciliation succeeds.

Once complete, Architect performs deep current web research from opened
primary, official, or otherwise authoritative sources, records provenance and
dates/versions, assesses agents/RAG/retrieval/vector/orchestration/stack
relevance from CDC drivers, and compares credible alternatives. A ready
architecture still advances only to the independent Reviewer.

Registry artifact chain: `20-architecture.md` -> `30-review.md` -> STOP -> later explicit DEV intake.

Global TOML agents are direct producers. Product inspects the project read-only
and writes only `10-cdc.md`; Architect writes only `20-architecture.md`; the
independent Reviewer writes only `30-review.md`. Their `workspace-write`
permission exists solely for the assigned handoff, and they never modify
product code or delegate to other agents.

Invoke through `$project-brainstorm` or `/skills`. Codex does not document
`/project-brainstorm` as a native custom-command alias. After `GO_DEV` or
`GO_DEV_WITH_CONDITIONS`, select one bounded handoff slice and explicitly invoke
`$change-delivery-workflow`; brainstorming never invokes DEV agents itself.
