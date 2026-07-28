# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: enforce-architect-research-dialogue
- Type: FEATURE

## Classification

- Primary type: FEATURE
- Secondary tags: AI, OBSERVABILITY
- Risk level: HIGH
- Risk justification: The change alters the globally installed Brainstorm state machine, a parent/user evidence gate, active agent instructions, and architecture handoff validation. A drift between Registry, hooks, Skills, or validators could bypass user input, loop automatically, invalidate active `brainstorm-product-design@1.2.0` workflows, or send an incomplete design to independent review.

## Objective

Make `architect_brainstorm` execute a deterministic sequence for an approved CDC: assess material completeness; pause for parent-mediated clarification while gaps remain; resume the same Registry-owned initial or rework architecture phase only after confirmed user answers are appended to `05-decision-log.md`; then perform current, cited, evidence-led web research, compare credible alternatives, and produce a complete `20-architecture.md` for the existing independent review phase.

## Confirmed requirements

- Preserve the exact approved-CDC and approval SHA-256 bindings.
- Preserve parent ownership of user dialogue and append-only decision memory.
- Re-invoke the same registered `architect_brainstorm` role; do not add an agent, phase, status, artifact, or loop counter.
- Prevent research and architecture recommendation while a material product, contract, data, security, compatibility, infrastructure, or irreversible-cost gap remains.
- After completeness, require deep read-only web research from current primary, official, or otherwise authoritative sources, with dates/versions where volatile.
- Compare significant alternatives on requirement fit, complexity, failure modes, security/data consequences, operations, cost, compatibility/migration, reversibility, and reconsideration triggers.
- Cover agents, RAG, retrieval/reranking, vector stores, orchestration, and stack choices only when CDC drivers make them relevant.
- Preserve `design_review` as the only successful successor of a ready architecture.
- Keep product files, Git state, publishing, deployment, and unrelated dirty-worktree changes untouched.

## Current behavior

- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json` declares `brainstorm-product-design@1.2.0`. In `FULL_DESIGN`, `architecture/BLOCKED_NEEDS_INPUT` is terminal `BLOCKED`; `architecture/READY_FOR_REVIEW` alone advances to `design_review`.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py:advance_after_status` clears `current_phase` and sets lifecycle `blocked` for terminal `BLOCKED`; `expected_phase_for_agent` therefore cannot authorize architecture re-entry.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_stop.py:main` validates `20-architecture.md` and immediately applies that transition. `common.py:infer_stage` and `stop_gate.py:main` then expose only a generic blocked workflow, not a parent clarification wait.
- `C:\Users\rapha\.codex\hooks\scripts\common.py:is_known_workflow_utility` recognizes `append_decision.py` by substring, and `pre_tool_guard.py:main` unconditionally allows that mutating command before phase/write-policy enforcement. `append_decision.py` trusts caller-supplied `--actor USER`; an active architect can therefore manufacture the evidence that would unlock its own proposed re-entry.
- Registry resolution is ID-only: `registry_engine.py:definition_path/load_workflow_definition`, `task-intake-workflow/scripts/validate_intake.py:definition`, and the single catalog entry cannot select an historical definition by task version. Because `init_brainstorm.py` accepts any `--repo-root`, a two-root scan cannot prove that no non-closed `1.2.0` workflow exists.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py` and direct Skill assertions still hard-code `brainstorm-product-design@1.2.0`; a Registry-only bump would make every new workflow fail intake version validation.
- `FULL_DESIGN/architecture_rework_review` assigns the same architect after `REWORK_ARCHITECTURE`, but its `BLOCKED_NEEDS_INPUT` is also terminal. The clarification loop must cover this path and still return successful rework to `design_review`.
- `C:\Users\rapha\.codex\agents\architect_brainstorm.toml` and both architecture methods already reject materially incomplete CDCs, but they do not define a durable clarification/resume protocol or a strict clarification-before-research sequence.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py:validate` checks architecture bindings, recommendation, slices, and blocking questions, but not completeness evidence, research gating, source metadata, relevance decisions, or alternative comparison.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` covers the direct approved-CDC-to-ready-architecture path only; it does not exercise blocked clarification, evidence-gated re-entry, or research ordering.
- The installed configuration exposes built-in web search (`tools.web_search = true`, currently cached discovery) while shell network access is disabled. The architecture contract must require opening/verifying current official sources and must block rather than claim completion if authoritative current evidence is unavailable. `C:\Users\rapha\.codex\config.toml` is not to be modified.
- The executable source currently present is the installed suite under `C:\Users\rapha\.codex`; the repository `global-config/` directory contains no files. Do not invent a second source tree in this change. Repository documentation under `docs/agents/` is the existing operator-facing mirror.

## Root cause

Not applicable as a defect root cause. The feature gap spans four contracts: both architecture phases model clarification as terminal; the decision utility bypasses parent-only write ownership; Registry lookup cannot preserve an older definition by selected version; and initialization remains pinned to `1.2.0`. No declared, provenance-safe transition connects a blocked handoff to new parent-owned `CLARIFICATION` entries and phase-local re-entry, and validation does not make research ordering or evidence quality machine-observable.

## Critical flow and blast radius

- Entry point: `brainstorm-product-design/FULL_DESIGN` reaches the existing `architecture` phase after a valid `15-cdc-approval.md`.
- Execution flow: `architect_brainstorm` validates bindings and performs a completeness assessment -> on material gaps writes `20-architecture.md` as `BLOCKED_NEEDS_INPUT` with precise questions and no research -> `subagent_stop.py` applies a Registry-declared evidence-gated self-loop to the current `architecture` or `architecture_rework_review` phase and records immutable decision-log prefix plus handoff anchors -> parent relays questions and invokes the canonical append utility against the exact active workflow -> `pre_tool_guard.py` proves no subagent is active and validates the exact command/target/actor/type/artifact/anchors before allowing mutation -> the utility rechecks the prefix before append -> hook reconciliation verifies only later suffix entries while the anchored prefix and blocked handoff are unchanged -> the same agent type becomes assignable again -> when complete, architect performs source-backed research and comparison, writes `READY_FOR_REVIEW`, and the unchanged phase-local transition advances to `design_review`.
- Upstream callers: parent orchestration through `$project-brainstorm`, hook `SubagentStart`/`SubagentStop`/`Stop`, and the `brainstorm-product-design` Registry.
- Downstream dependencies: architecture validator, independent `review_brainstorm`, session/compaction state restoration, installer self-tests, and operator documentation.
- Consumers and data affected: global Codex Brainstorm workflows and hook-owned `.workflow.json`; only append-only `05-decision-log.md` gains user-confirmed clarification entries.
- Intentionally unaffected areas: `DISCOVERY_ONLY`; CDC creation/approval semantics; design-review verdicts and rework counters; DEV workflows; MCP mutation policy; product source, tests, schemas, migrations, manifests, lockfiles, and `C:\Users\rapha\.codex\config.toml`.

## Relevant files and symbols

- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design-1.2.0.json` (new immutable compatibility definition) and `brainstorm-product-design.json` (current `1.3.0`): side-by-side exact version behavior; both initial and rework architecture transition contracts in `1.3.0`.
- `C:\Users\rapha\.codex\workflow-registry\registry.json`: current definition plus version-indexed historical definition mapping for the same workflow ID.
- `C:\Users\rapha\.codex\workflow-registry\validate_registry.py`: `validate_def` and catalog validation for unique `(id, version)` resolution and evidence-gated self-loops without new workflow entities.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py`: `definition_path`, `load_workflow_definition`, `selected_definition`, `sync_metadata_from_task`, `advance_after_status`, `expected_phase_for_agent`, and `next_action`.
- `C:\Users\rapha\.codex\hooks\scripts\common.py`: replace the substring mutation allow-list in `is_known_workflow_utility`; add exact decision-invocation parsing, `infer_stage` parent-visible waiting state, and compaction-safe next action.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py`: parent-only clarification mutation authorization against active workflow and anchored wait state.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_stop.py`: persist the clarification anchor after a blocked architecture handoff.
- `C:\Users\rapha\.codex\hooks\scripts\stop_gate.py`: reconcile newly appended clarification evidence and always stop for the user while evidence is pending, including continuous automation.
- `C:\Users\rapha\.codex\agents\architect_brainstorm.toml`: completeness, question, research, citation, relevance, and completion-response contract.
- `C:\Users\rapha\.codex\skills\architect-brainstorm\SKILL.md` and `references/{architecture-method,handoff-template}.md`: directly invokable architecture behavior and handoff structure.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md`, `agents/openai.yaml`, and `references/{architecture-method,pipeline,workflow-states,handoff-contracts}.md`: active managed-workflow, initializer version, App prompt, and parent orchestration contract.
- `C:\Users\rapha\.codex\skills\project-brainstorm\assets\templates\20-architecture.md`: explicit completeness, research, relevance, and alternative evidence fields.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\append_decision.py`: fail-closed prefix/handoff anchor verification for canonical parent clarification appends.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py`: bind every new workflow to `brainstorm-product-design@1.3.0`.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py`: deterministic status-specific architecture checks.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py`, `SKILL.md`, and `references/workflow-registry.md`: resolve and validate the task's exact `(Workflow ID, Workflow version)` while selection continues to expose only the current version.
- `C:\Users\rapha\.codex\hooks\installer\{self_test,full_self_test}.py`: Registry schema and end-to-end clarification/research-gate regression coverage.
- `C:\Users\rapha\.codex\workflow-registry\README.md`, `C:\Users\rapha\.codex\hooks\README.md`, and `docs/agents/{project-brainstorm,project-brainstorm-architect}.md`: installed and repository operator documentation.

## Proposed design

Version `brainstorm-product-design` from `1.2.0` to `1.3.0` without replacing the old executable contract. Copy the byte-equivalent current `1.2.0` definition to an immutable versioned definition, keep `brainstorm-product-design.json` as the current `1.3.0` definition, and extend the catalog entry with a validated version-to-definition map. Registry APIs accept an optional version: pre-intake discovery and route selection expose only the current definition, while any workflow with `workflow_version` in `.workflow.json` or `## Workflow version` in `00-task.md` resolves that exact definition. Unknown or mismatched versions fail closed. This side-by-side strategy protects active, blocked, parked/closed, and historical workflows in any repository supported by `init_brainstorm.py`; no global filesystem inventory, metadata rewrite, or migration is required.

Update `init_brainstorm.py`, `$project-brainstorm`, its App prompt/version statements, and installer assertions so all newly initialized workflows persist `1.3.0`. Update `validate_intake.py` to resolve the exact task version, while the task compiler's Registry selection sees only current definitions. Tests must prove that arbitrary second-repository active and blocked `1.2.0` workflows continue against immutable terminal semantics, historical `1.2.0` validation remains possible, and fresh `1.3.0` initialization/validation uses the new contract.

Replace `BLOCKED_NEEDS_INPUT` in both `architecture` and `architecture_rework_review` with phase-local self-loops whose `next` is the same existing phase and whose transition declares the same `resume_evidence` object. It identifies `05-decision-log.md`, `Actor: USER`, `Type: CLARIFICATION`, `20-architecture.md` as the affected artifact, and the requirement for at least one complete decision entry appended after the captured prefix. Registry validation accepts it only on a subagent self-loop when the evidence artifact is a required input and a managed append-only parent artifact. Preserve each phase's declared inputs and `READY_FOR_REVIEW -> design_review` transition unchanged.

At blocked transition, persist only technical wait metadata in hook-owned `.workflow.json`: exact phase ID, SHA-256 of the blocked `20-architecture.md`, byte length and SHA-256 of the complete decision-log prefix, and last decision ID. While waiting, `expected_phase_for_agent` returns no architect assignment, `infer_stage` tells the parent to relay the precise questions, and `stop_gate` permits the turn to stop even under AUTO-RUN. Reconciliation requires the current handoff hash to equal the anchor, the first anchored byte length of the current log to hash exactly to the stored prefix SHA-256, and every accepted answer to be a complete, strictly later `DEC-xxx` suffix entry matching USER/CLARIFICATION/`20-architecture.md`. Editing any prior byte plus appending cannot unlock the gate.

Move decision-log mutation behind an exact parent-only invocation contract. `append_decision.py` is no longer accepted by substring in the generic utility bypass. For an architecture wait, `pre_tool_guard.py` parses one non-chained, fixed-order command only: `py -3 <exact project-brainstorm append_decision.py> --workflow-dir <exact active workflow> --actor USER --type CLARIFICATION --decision <confirmed answer> --evidence <user-message evidence> --affected-artifacts 20-architecture.md --consequence <architecture consequence> --invalidates <invalidated assumptions or None> --expected-prefix-length <anchored length> --expected-prefix-sha256 <anchored hash> --source-artifact-sha256 <blocked handoff hash>`. Require parent/root event context and no active/assigned subagent in metadata. Reject duplicate/unknown arguments, shell operators, a different executable/script, relative or wrong workflow target, wrong phase, absent wait metadata, wrong actor/type/artifact, or stale anchors before allowing execution. Free-text fields are parsed as inert single argument values. The utility independently resolves the target, loads the hook-owned wait anchors, verifies the exact prefix and source handoff, and only then appends; ordinary parent brief/approval decision appends retain their existing phase-specific authorization through separately enumerated exact command shapes, not a substring bypass. A denied or failed call must leave the log byte-identical.

After valid append-only evidence appears, reconciliation clears the wait metadata but retains the phase that blocked (`architecture` or `architecture_rework_review`); the same registered agent type is then re-invoked with that phase's unchanged declared inputs. Repeated blocked runs create fresh handoff/prefix anchors and repeat the same evidence gate without a counter.

Make the architect method explicitly ordered:

1. Validate exact CDC/approval bindings and read all confirmed decision-log entries.
2. Complete a proportional matrix for scope, scenarios, rules, data, integrations, security/privacy, operations, acceptance criteria, compatibility, infrastructure/cost, and architecture drivers.
3. If any material item is unresolved, write only a blocked handoff with decision-relevant questions, mark research `NOT_STARTED_MATERIAL_GAPS`, and make no stack or target-architecture recommendation.
4. When the matrix is complete, derive a research brief from the CDC drivers. Use read-only web search for discovery, open current primary/official/authoritative sources, record URL, publisher, source type, access date, material version/date, supported claim, and limitations. If current authoritative evidence cannot be verified, block explicitly.
5. Record whether agents, RAG, retrieval/reranking, vector storage, orchestration, and stack selection are relevant, with CDC-driver evidence. Research relevant topics deeply, including security, evaluation/observability, failure modes, and cost; explicitly justify non-applicability without introducing them.
6. Compare every structurally significant alternative on the AC-007 axes, then produce the complete existing architecture package and `READY_FOR_REVIEW`.

Synchronize the active agent, both architecture Skill surfaces, the managed project Skill, template, validator, tests, and operator docs. The validator should require machine-readable completeness and research-gate markers; reject URLs/recommendations in a materially blocked handoff; require a ready handoff to contain source records with HTTP(S) URLs and date/version metadata, a relevance assessment, credible alternative comparison, complete bindings, slices, traceability, and no blocking questions. It should validate structure and provenance fields, not attempt subjective live-web ranking.

## Alternatives considered

- Keep terminal `BLOCKED` and manually restart the workflow: rejected because `advance_after_status` clears the phase, loses deterministic ownership, and makes re-entry depend on out-of-band state repair.
- Add a `clarification` phase, new status, question artifact, or loop counter: rejected because the existing architecture handoff and decision log already contain the questions and confirmed answers, and the task explicitly forbids new workflow entities.
- Change `BLOCKED_NEEDS_INPUT` directly to an unguarded `next: architecture`: rejected because AUTO-RUN could immediately re-spawn the architect before the user answers and create a tight loop.
- Let the architect ask the user or write `05-decision-log.md`: rejected because it violates parent ownership, append-only decision authority, and the agent write boundary.
- Test live search responses: rejected because network results are non-deterministic. Contract/order/provenance are tested deterministically; actual source quality remains reviewer-verifiable evidence in each handoff.
- Replace `1.2.0` after a bounded or environment-wide filesystem scan: rejected because arbitrary `--repo-root` values and session-state references make completeness unprovable, especially for blocked workflows. Exact side-by-side resolution is smaller operationally and preserves old behavior without locating every repository.
- Migrate active/blocked `1.2.0` metadata to `1.3.0`: rejected because it rewrites user workflow state and silently changes terminal semantics.

## Implementation sequence

1. Add failing Registry and intake tests for current-version selection plus exact historical resolution. Preserve current `1.2.0` as the versioned compatibility fixture; assert duplicate `(id, version)`, missing current definition, mismatched definition version, and unknown selected version fail.
2. Implement version-aware catalog/engine/intake resolution, publish current `1.3.0` beside immutable `1.2.0`, and update `init_brainstorm.py`, Skill/App direct version bindings, and installer assertions. Prove fresh initialization persists and validates `1.3.0`.
3. Add failing PreToolUse/utility tests before changing mutation code: active architect exact/substring/aliased/chained append attempts are denied and byte-preserving; wrong workflow, script, artifact, actor, type, prefix length/hash, and handoff hash are denied; an exact parent invocation in the active wait succeeds.
4. Replace the append substring bypass with exact parsing and target/provenance checks in `common.py`/`pre_tool_guard.py`; add prefix/source verification to `append_decision.py` while preserving explicit parent brief/approval append paths.
5. Add failing hook-engine tests for both architecture phases: blocked anchoring, denial before later clarification, immutable-prefix enforcement, valid suffix acceptance, repeated cycles, AUTO-RUN pause, compaction restoration, and unchanged ready-to-review routing.
6. Implement generic `resume_evidence` self-loop support in `registry_engine.py`, `subagent_stop.py`, `common.py`, and `stop_gate.py`; declare it identically on `architecture` and `architecture_rework_review`; prove no new workflow entity exists.
7. Add failing handoff-validator fixtures for blocked-with-research, blocked-with-recommendation, ready-without completeness, ready-without current source metadata, ready-without alternatives/relevance, and a complete ready package. Then update template and validator status checks.
8. Update `architect_brainstorm.toml`, both architecture Skill surfaces, and project-brainstorm method/pipeline/state/handoff contracts with the same ordered sequence, phase-local resume behavior, exact parent append command, and version `1.3.0`.
9. Extend full E2E coverage for initial clarification and `design_review -> REWORK_ARCHITECTURE -> architecture_rework_review -> BLOCKED_NEEDS_INPUT -> parent clarification -> architecture_rework_review -> READY_FOR_REVIEW -> design_review`, including premature re-entry denial and a second independent review.
10. Add second-repository compatibility fixtures for active and blocked `1.2.0`, a closed historical `1.2.0` fixture, and a fresh `1.3.0` workflow. Synchronize operator docs, run validators/self-tests, compare hashes/diff, and confirm only approved global assets and named docs changed.

## Tests-first strategy

- First failing test: in `full_self_test.py`, submit a valid `BLOCKED_NEEDS_INPUT` architecture handoff, assert metadata retains `current_phase == "architecture"`, then prove the still-active architect's canonical and substring-spoofed append commands are denied without changing the log; after agent stop, prove only an exact parent invocation bound to workflow/prefix/handoff succeeds and unlocks the same agent type.
- Unit coverage: version-indexed definition lookup and current selection; Registry `resume_evidence` schema on both phase-local loops; exact command parsing; parent/subagent provenance; byte-prefix and handoff hashing; suffix decision parsing; stale/wrong evidence; repeated self-loop; status-specific architecture validator rules.
- Integration coverage: `subagent_start -> blocked handoff -> subagent_stop -> stop_gate -> exact parent append_decision.py -> same-phase subagent_start -> ready handoff -> design_review`, for initial and rework architecture, including compaction restore and AUTO-RUN.
- End-to-end coverage when justified: extend the existing isolated `full_self_test.py` Brainstorm workflow; do not exercise a real network or mutate external systems.
- Edge and failure cases: active-subagent impersonation, substring/alias/chained utility invocation, wrong workflow/artifact/actor/type, missing or edited prefix, stale handoff, duplicate/out-of-order IDs, unrelated or empty clarification, unavailable current source, irrelevant fashionable technology, self-approval, review bypass, and product-file write attempt.
- Compatibility checks: arbitrary-repository active and blocked `1.2.0` exact resolution, closed historical `1.2.0`, fresh initialized/validated `1.3.0`, unknown-version failure, `DISCOVERY_ONLY`, brief interview, CDC approval/rework, architecture review rework, DEV workflow, generic hook routing, and existing no-product-write/Git guards.
- Repository-derived commands:
  - `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - Extend the self-test CLI minimally with `--architect-skill-root C:\Users\rapha\.codex\skills\architect-brainstorm` only if direct Skill synchronization is asserted there.
  - `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py --workflow-dir <isolated-test-workflow>`

## Rollout and rollback

Roll out atomically as a side-by-side global-suite change: install version-aware readers and the immutable `1.2.0` definition before making `1.3.0` current and updating initialization. Validate active, blocked, and historical `1.2.0` fixtures plus fresh `1.3.0`; do not inventory, migrate, or edit their artifacts/metadata. Rollback changes only the catalog's current pointer and new-workflow initializer to `1.2.0` while retaining the `1.3.0` definition if any `1.3.0` workflow exists, so both versions remain resolvable; remove `1.3.0` support only after a proven absence of every selected `1.3.0` workflow or explicit user disposition.

## Architecture fitness checks

- Registry validation proves the clarification path is a guarded self-loop to the existing phase and that `READY_FOR_REVIEW` still targets only `design_review`.
- Registry/intake tests prove exact side-by-side resolution: current selection yields `1.3.0`, while any located active, blocked, or historical `1.2.0` workflow uses its immutable definition.
- PreToolUse and utility tests prove an architect cannot self-author unlock evidence, denied calls preserve bytes, and only the exact parent invocation for the active anchored wait mutates the log.
- Hook tests prove no architect assignment before later confirmed evidence, immutable prefix/handoff bindings, no AUTO-RUN continuation, and identical behavior in initial and rework architecture phases.
- Handoff validation proves mutually exclusive blocked/no-research and ready/researched states.
- Self-tests compare route phase IDs, statuses, managed artifacts, human gates, and counters against the pre-change sets.
- Full-path tests prove independent review and all product/Git write guards remain intact.

## Data and migration impact

No product data or schema migration. Hook-owned `.workflow.json` gains bounded clarification-wait metadata for `1.3.0` runs only; `05-decision-log.md` keeps its existing append-only `DEC-xxx` format and `CLARIFICATION` type. The Registry retains immutable `1.2.0` and current `1.3.0` definitions side by side; historical and non-closed `1.2.0` artifacts remain untouched.

## Security and privacy impact

The architect retains read-only repository/external retrieval and handoff-only writes. An active subagent is denied the decision utility before any allow-list bypass; the parent remains the sole user-facing caller and decision-log writer through an exact target- and anchor-validated invocation. Only byte-prefix-preserving, USER-confirmed later evidence unlocks re-entry. No MCP mutation, secret access, product write, approval simulation, or self-review is added. Research citations must not include secrets, private payloads, or hidden memory.

## Performance and operational impact

Clarification may add deliberate user round trips and deep research may increase latency/token cost, both bounded by material architecture drivers rather than fixed source counts. Hook work is local parsing/hashing of small workflow artifacts. Operators gain an explicit waiting stage and actionable resume instruction; no service deployment or infrastructure cost changes.

## Documentation impact

Synchronize installed Registry/hooks READMEs and repository `docs/agents/project-brainstorm*.md` with the exact completeness -> clarification -> research -> proposal -> independent-review sequence, version `1.3.0`, evidence gate, and failure behavior. Do not create a new documentation tree or revive the empty `global-config/` directory.

## Risks

- Unguarded self-loop could spin under AUTO-RUN; mitigate with Registry-declared resume evidence, assignment denial, and stop-gate tests.
- A subagent could impersonate USER through the decision utility; mitigate at both PreToolUse provenance and utility prefix/source validation, with byte-preservation tests for every denied form.
- Stale, edited, or unrelated decisions could unlock architecture; mitigate with exact byte-length/prefix SHA-256 and handoff SHA-256 anchors, strict later `DEC-xxx`, actor/type/artifact checks, and append-only validation.
- Prompt-only rules could drift from executable behavior; mitigate with synchronized templates/validators and content assertions across both Skills and the active agent.
- Citation validation could reward superficial URLs; validate only deterministic provenance structure and leave substantive authority/claim fit to independent review.
- Version-aware resolution could accidentally expose historical definitions as new choices or select the wrong route; mitigate by separating current selection from exact selected-version resolution and testing active, blocked, historical, new, and unknown-version cases.
- Existing unrelated dirty files could be attributed accidentally; snapshot the initial status/hashes, restrict changes to the named assets/docs, and review the final delta.

## Assumptions

- “Same architect” means re-invoking the same Registry-declared `architect_brainstorm` agent type with durable artifacts, not preserving one hidden model process or private reasoning.
- Multiple material questions may require multiple parent/user turns; each re-entry consumes only confirmed append-only evidence and may block again.
- The parent may append one or more complete clarification entries after a block; every accepted suffix entry is parsed after the immutable anchored prefix, while re-entry requires at least one matching entry.
- Current web search remains available to the agent through inherited read-only tooling; cached results are discovery aids, not sufficient proof for volatile claims without opening a current authoritative source.
- The currently installed `C:\Users\rapha\.codex` suite is the executable source to update; no maintained repository source mirror exists in the inspected workspace.

## Blocking questions

None.

## Out of scope

- Product discovery, CDC changes or approval, product architecture execution, implementation, deployment, and Git publication.
- A new clarification agent, phase, artifact, status, counter, external memory store, or architect-owned decision log.
- Mandatory agents, RAG, vector databases, orchestration, microservices, or stack changes without CDC evidence.
- Live-network assertions, automated subjective ranking of sources, or scraping/private connector mutations.
- Cleanup of existing workflows, caches, `global-config/`, unrelated global assets, or the dirty worktree.

## Reviewer checklist

- [ ] Requirements and AC-001 through AC-012 are represented.
- [ ] The verified terminal-block root cause and exact execution path are supported by current Registry/hook evidence.
- [ ] The self-loop cannot auto-run or re-enter before later confirmed user evidence.
- [ ] PLAN-REVIEW-001 is closed by exact parent-only mutation authorization, target validation, immutable-prefix and handoff hashes, and byte-preserving denial tests.
- [ ] PLAN-REVIEW-002 is closed by side-by-side exact version resolution for active, blocked, and historical workflows in arbitrary repositories.
- [ ] PLAN-REVIEW-003 is closed by `init_brainstorm.py`, direct Skill/App bindings, and fresh `1.3.0` initialization/intake tests.
- [ ] PLAN-REVIEW-004 is closed by the same guarded self-loop on `architecture_rework_review` and a second-review E2E path.
- [ ] No new phase, status, artifact, agent, human gate, or counter is introduced.
- [ ] Blocked handoffs cannot research/recommend; ready handoffs expose current source provenance, relevance, alternatives, and complete architecture fields.
- [ ] `design_review` remains the sole successful successor and self-approval/product implementation remain impossible.
- [ ] Side-by-side compatibility, rollback, security, and dirty-worktree protections are proportionate.
