# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: add-approved-cdc-architecture-route
- Type: FEATURE

## Classification

- Primary type: FEATURE
- Secondary tags: SECURITY, INTEGRATION, INFRASTRUCTURE
- Risk level: HIGH
- Risk justification: The change extends the Registry control plane and introduces a cross-repository trust boundary. A false-positive approval, stale hash, unsafe path, version-resolution regression, or premature hook transition could launch architecture from unapproved evidence or alter existing Brainstorm workflows.

## Objective

Add one reusable managed `brainstorm-product-design` route that imports an already approved external CDC package, validates and snapshots its exact evidence, starts at architecture, performs independent design review with bounded architecture rework, and closes before DEV.

## Confirmed requirements

- Satisfy AC-001 through AC-011 from `00-task.md`.
- Reuse only Registry agents, modes, artifacts, statuses, terminals, and counters already used by `brainstorm-product-design`: `architect_brainstorm`, `review_brainstorm`, `ARCHITECTURE_DESIGN`, `ARCHITECTURE_REWORK_REVIEW`, `DESIGN_REVIEW`, `20-architecture.md`, `30-review.md`, the existing review statuses, `architecture_rework_cycles`, and `repeated_finding_threshold`.
- Do not execute `brief_interview`, `cdc`, `cdc_approval`, or any CDC rework phase after valid external approval evidence has been imported.
- Fail closed before `architect_brainstorm` for absent, unreadable, mismatched, non-approved, stale, or internally inconsistent evidence.
- Preserve explicit USER approval and the existing hash-bound USER clarification loop. `AUTO-RUN: YES` must not manufacture either.
- Keep `brainstorm-product-design@1.2.0` and `@1.3.0` exactly resolvable for already compiled workflows.
- Treat the NeoAutomatisation workflow only as read-only import-validation evidence; do not create architecture/review artifacts there.
- Make no product, Git, publication, deployment, or `.workflow.json` manual change.

## Current behavior

- `C:\Users\rapha\.codex\workflow-registry\registry.json` maps `brainstorm-product-design@1.2.0` to an immutable versioned file and `@1.3.0` to the current `brainstorm-product-design.json`. New initialization selects `1.3.0`; exact-version readers resolve persisted versions through the `versions` map.
- Both current routes start at the parent `brief_interview` gate. `FULL_DESIGN` then runs CDC creation and approval before the existing `architecture`, `design_review`, and bounded rework phases.
- `project-brainstorm/scripts/init_brainstorm.py:main` always creates metadata at `brief_interview`, with `route: null`; it has no approved-CDC import mode.
- `hooks/scripts/registry_engine.py:pre_intake_phase` assumes every managed route has the same pre-intake start phase. Adding a route that starts at `architecture` without changing this resolution would remove the shared brief gate or block all intake, depending on how it is added.
- `project-brainstorm/scripts/validate_handoff.py:validate` already verifies the local CDC/approval hash, `APPROVED` status, USER approval fields, and that the bound `DEC-xxx` exists. Architecture and review validation bind the current local upstream artifacts.
- `hooks/scripts/subagent_start.py:main` assigns the declared current phase but does not validate every declared `required_inputs` immediately before assignment.
- `task-intake-workflow/scripts/validate_intake.py:validate` treats every non-empty `Source workflow bindings` section as a completed Brainstorm-to-DEV bridge, so it cannot currently express a BRAINSTORM import containing only CDC, approval, and decision-log evidence.
- The parent has corrected `00-task.md` to carry both registry-native and legacy loop-budget labels. The same current intake contract now passes both `task-intake-workflow/scripts/validate_intake.py` and `change-delivery-workflow/scripts/validate_handoff.py`; implementation remains gated on a fresh independent plan review.
- The supplied NeoAutomatisation package currently validates with the Project Brainstorm validator. Its observed hashes are:
  - `10-cdc.md`: `51E861D4F2D581143C4207C860F71699F9AB129F654F243EBF70AAFBE806E8F0`;
  - `15-cdc-approval.md`: `E0A0636330BDFBBF94A9F71D0ED33A7A7087B840D2BFFA5DBEF6628C4A0C03D0`;
  - `05-decision-log.md`: `42F3685B23421FEE16A46F30712EB551CBBA46115CFDD3EAB4FD25838B232383`.
- Its certificate is `APPROVED`, binds the exact CDC hash, and references `DEC-055`; that entry is a USER `CDC_APPROVAL` for the same CDC. `20-architecture.md` and `30-review.md` are absent.

## Root cause

Not applicable as a defect. The verified capability gap is that the Registry has architecture/review phases and exact-version resolution, but no route, initializer contract, intake binding shape, or pre-assignment evidence gate for reusing an approved CDC from another workflow.

## Critical flow and blast radius

- Entry point: parent invocation of `project-brainstorm/scripts/init_brainstorm.py` with an explicit approved source workflow and expected hashes.
- Execution flow: canonicalize and validate fixed source files -> atomically snapshot `05-decision-log.md`, `10-cdc.md`, and `15-cdc-approval.md` into a new workflow -> create hook-owned metadata pinned to the new exact version/route -> compile and dual-validate `00-task.md` -> parent runs mandatory pre-dispatch evidence validation -> only a successful result permits the parent to call `spawn_agent` for `architect_brainstorm` -> `SubagentStart` revalidates before assignment as defense in depth -> `architecture` -> `design_review` -> optional bounded `architecture_rework_review` -> independent `design_review` -> terminal stop.
- Upstream callers: parent Project Brainstorm activation, `task_intake_compiler`, and exact workflow-utility authorization in `hooks/scripts/common.py`.
- Downstream dependencies: Registry definition/version resolution, Project Brainstorm validator, intake validator, SubagentStart/Stop and Stop hooks, decision-log resume anchoring, installer self-tests.
- Consumers and data affected: temporary workflow metadata and imported local evidence snapshots only; the external source remains read-only.
- Intentionally unaffected areas: `brainstorm-product-design@1.2.0` and `@1.3.0`, `DISCOVERY_ONLY`, `FULL_DESIGN`, all DEV routes/agents, product repositories, Git policy, MCP policy, and the NeoAutomatisation source workflow.

## Relevant files and symbols

- `C:\Users\rapha\.codex\workflow-registry\registry.json`: catalog `definition` and `versions` map.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json`: current definition and reusable architecture/review phase contracts.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design-1.2.0.json`: immutable compatibility baseline.
- `C:\Users\rapha\.codex\workflow-registry\validate_registry.py`: `validate_def`, route graph, input/output, transition, and counter validation.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py`: `main`, safe task ID, deterministic initialization.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py`: `validate`, `decision_log_errors`, workflow-level binding validation.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\append_decision.py`: existing append-only clarification anchors; behavior must be reused unchanged.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` and `references/{pipeline,workflow-states,handoff-contracts}.md`: route/import/operator contract.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py`: `definition`, `validate`, route-specific source binding validation.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md` and `references/{compiled-task-contract,routing-and-depth}.md`: compiled BRAINSTORM import binding shape.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml`: permit the Registry-pinned import route without weakening normal brief validation.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py`: `pre_intake_phase`, exact-version selection, route start, transitions, loop budgets, and resume evidence.
- `C:\Users\rapha\.codex\hooks\scripts\workflow_status.py` plus a narrowly scoped parent pre-dispatch helper: observable evidence validation before any `architect_brainstorm` spawn.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_start.py`: fail-closed required-input preflight before phase assignment.
- `C:\Users\rapha\.codex\hooks\scripts\common.py`: workflow utility allowlist and validator dispatch.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`: deterministic Registry/version/import/path/binding tests.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py`: end-to-end initializer, intake, hooks, rework, terminal, and non-regression tests.
- `E:\Projets IA\Automatisation\.codex\workflows\cdc-maintenance-documentaire-rag-v2-2-officialisation\{05-decision-log.md,10-cdc.md,15-cdc-approval.md}`: read-only acceptance evidence.

## Proposed design

### 1. Side-by-side Registry versioning

- Copy the current `brainstorm-product-design.json` byte-for-byte to a new immutable `brainstorm-product-design-1.3.0.json` before changing the current definition.
- Publish the current definition as `1.4.0`, add `1.3.0` and `1.4.0` entries to the catalog `versions` map, and keep `definition` pointing to the `1.4.0` file.
- Add managed route `APPROVED_CDC_DESIGN` with `start_phase: architecture`, no human-gate phase, and only:
  1. the existing `architecture` contract;
  2. the existing `architecture_rework_review` contract;
  3. the existing independent `design_review` contract.
- Declare only `architecture_rework_cycles` and `repeated_finding_threshold`.
- Keep all existing design-review terminals. Map `REWORK_CDC` to existing terminal `BLOCKED` because the imported approved CDC is immutable in this route; do not dispatch `cdc_brainstorm`. Keep `REWORK_ARCHITECTURE` on the existing bounded counter.
- Preserve `GO_DEV` and `GO_DEV_WITH_CONDITIONS` as terminal `COMPLETE` advice only. No DEV phase, agent, artifact, or Git authorization is added.
- Add one generic route-level Registry field, `parent_append_only_artifacts`, with `["05-decision-log.md"]` on `APPROVED_CDC_DESIGN`. This declares parent ownership without adding a phase or replaying interview/approval.
- Extend `validate_registry.py` so `parent_append_only_artifacts` is allowed only on managed routes, contains unique declared managed artifacts, and cannot overlap a subagent-mutable output. Resolve every `resume_evidence.artifact` against the union of parent-phase append-only ownership and this route-level declaration; keep all existing source-artifact, affected-artifact, actor USER, type CLARIFICATION, self-loop, and required-input checks. A missing declaration, mutable policy, undeclared artifact, or non-parent ownership remains invalid.
- Extend the Registry engine and PreTool guard with a single accessor for route-level parent append-only ownership. It must block direct patch/shell/MCP mutation by every subagent and by the parent outside an active anchored clarification wait. During that wait, the existing exact parent/root `append_decision.py` authorization, prefix/hash anchors, and suffix reconciliation remain the only write path.
- Strengthen `validate_registry.py` generically so phase outputs and required inputs must resolve to declared request/task/managed artifacts or a route phase output, while retaining existing agent, status, target, counter, and path-containment checks.

### 2. Snapshot import, not live reference

- Add a small Project Brainstorm import helper used by the initializer and validator. It accepts only a source workflow directory plus expected CDC, approval, and decision-log SHA-256 values.
- Resolve an absolute source directly; resolve a relative source against explicit `--repo-root`, never process cwd. Use strict canonical resolution, fixed child names, and reject missing/non-regular files, symlink/reparse escapes, source/target equality, globs, and any resolved child outside the canonical source directory.
- Read the three source files into memory once, hash those exact bytes, and validate the captured package before creating the target. This closes hash/copy time-of-check gaps.
- Validate:
  - all three expected hashes;
  - complete `10-cdc.md` handoff structure;
  - certificate `Status: APPROVED`;
  - certificate CDC hash equals both the expected and captured CDC hash;
  - certificate `Human decision` is USER with timestamp and explicit evidence;
  - certificate’s bound `DEC-xxx` exists in the captured log;
  - that entry has `Actor: USER`, exact `Type: CDC_APPROVAL`, and affects `10-cdc.md`;
  - the normalized `Decision` contains an explicit affirmative CDC-approval term, contains exactly one SHA-256, and that hash equals the captured/imported CDC hash;
  - the decision contains no rejection/refusal term and no competing SHA-256. Generic `APPROVAL`, a missing hash, another artifact/hash, a rejection, or ambiguous positive/negative wording is invalid.
  - decision-log structure and ordered unique IDs.
- Materialize byte-for-byte local snapshots as the already declared `05-decision-log.md`, `10-cdc.md`, and `15-cdc-approval.md`. Stage under `.codex/.workflow-staging/<random-id>/`, a sibling outside `.codex/workflows/`; do not create `00-request.md`, `00-task.md`, or active metadata anywhere discoverable by `workflow_candidates`. After fsync/verification, publish with one same-volume atomic directory rename to `.codex/workflows/<task-id>`.
- Use an exclusive final rename: with two concurrent initializers, exactly one publishes. The loser may report idempotent success only when the existing final workflow is still in the untouched imported pre-intake state and its raw request semantics, intake/automation controls, complete initializer-owned metadata projection, canonical source provenance, imported prefix length/hash, and all three snapshot bytes/hashes equal the attempted initialization. Any progressed workflow or differing request, metadata, source, or proof fails without overwrite.
- Preserve source provenance and import bindings in hook-owned metadata until intake compilation, then copy them into `00-task.md`. Architecture reads only the local snapshot. The source may become unavailable afterward without invalidating the run.
- Treat the imported decision log as a bound prefix: store its byte length and SHA-256. Preflight requires the current local log to start with that exact prefix, while allowing only later parent-owned append entries through the existing hash-bound clarification mechanism. Review continues to bind the complete current decision log.

### 3. Initializer and intake ergonomics

- Extend `init_brainstorm.py` with one mutually exclusive import mode, for example:
  `--approved-cdc-workflow`, `--cdc-sha256`, `--approval-sha256`, and `--decision-log-sha256`.
  All four options are required together; without them, initialization remains unchanged.
- Import mode pins `workflow_version: 1.4.0`, `route: APPROVED_CDC_DESIGN`, and `current_phase: architecture` in newly created hook-owned metadata. It does not create `00-task.md`, `20-architecture.md`, or `30-review.md`.
- Make `registry_engine.pre_intake_phase` route-aware:
  - a metadata-pinned route uses only that route’s declared start;
  - normal unpinned initialization still derives and enforces the common parent evidence gate of discovery routes;
  - the pinned approved-CDC route permits `task_intake_compiler` because its evidence has already passed the import contract.
- Add a BRAINSTORM-specific `Source workflow bindings` shape for `APPROVED_CDC_DESIGN`: source workflow ID/version/directory, `Import mode: SNAPSHOT`, CDC hash, approval hash, imported decision-log prefix hash and length, and approval decision entry.
- Keep the existing completed-Brainstorm-to-DEV binding shape unchanged. Branch validation by compiled mode and route so neither contract can masquerade as the other.
- Intake validation compares `00-task.md` against hook-owned import metadata and the local snapshots, confirms the exact route/version and prefix, and rejects missing/extra/mismatched import fields. Update `task_intake_compiler.toml` only to describe this Registry-pinned exception; generic BRAINSTORM initialization still requires USER `brief validé`.

### 4. Pre-assignment and downstream gates

- Add one parent/root-only pre-dispatch utility that calls the shared import validator for the exact active workflow and expected `architect_brainstorm` phase. Project Brainstorm parent orchestration must run it immediately before invoking `spawn_agent`; this is the authoritative dispatch decision, not `SubagentStart`.
- On pre-dispatch failure, atomically set hook-owned lifecycle to `blocked` with a stable reason such as `INVALID_IMPORTED_CDC_EVIDENCE:<invariant>`, emit a non-zero/blocked result naming the failed invariant without payload contents, and prohibit the parent from calling `spawn_agent`. The observable sequence is validation failure -> blocked workflow -> zero `architect_brainstorm` spawn calls and zero `SubagentStart` events.
- On pre-dispatch success, return the exact workflow ID/version/route/phase and current CDC, approval, and imported-prefix hashes; only that immediate success authorizes the parent’s next `spawn_agent` call. Do not reuse a stale success after any intervening workflow mutation.
- Retain `subagent_start.py` as defense in depth: before recording an assignment, independently validate every declared required input and import binding. If a caller bypasses the parent preflight or evidence changes between preflight and spawn, leave assignment metadata unset, inject read-only failure context, and let PreToolUse deny `20-architecture.md`. This does not claim to cancel the already started subagent.
- Reuse the 1.3 hash-bound `BLOCKED_NEEDS_INPUT` self-loop unchanged for both initial and rework architecture. It does not consume the rework counter and requires exact later USER clarification.
- Reuse the existing SubagentStop transition engine for independent review and bounded rework. Exhaustion, persistent findings, `REWORK_CDC`, or blocking verdicts stop without DEV.

## Alternatives considered

- Live-reference external files: rejected because source mutation or drive unavailability would change an active workflow and current validators/agents expect local canonical filenames.
- Copy only CDC and approval: rejected because the certificate validator, architecture input contract, clarification loop, and final review all depend on `05-decision-log.md`.
- Add an import/preflight phase or new evidence artifact: rejected because deterministic import can happen before task compilation and be enforced by initializer/intake/pre-assignment validation without inventing an agent, phase, status, or artifact.
- Add a fake parent phase solely to own `05-decision-log.md`: rejected because it would add an executable graph step and could accidentally replay a human gate. The route-level `parent_append_only_artifacts` schema declares ownership directly and preserves the existing anchored parent utility as the sole mutation mechanism.
- Relax the Registry requirement that resume evidence be parent-owned: rejected because it would weaken every clarification self-loop. The generic schema extension preserves and makes that invariant explicit for routes whose parent participates only during a wait.
- Modify `1.3.0` in place: rejected because persisted workflows resolve that exact version and would silently change behavior.
- Allow `REWORK_CDC` to edit the imported CDC: rejected because it would invalidate the external approval and reintroduce the skipped CDC approval chain.

## Implementation sequence

1. Add failing assertions first in `hooks/installer/self_test.py` for immutable 1.2/1.3 resolution, new 1.4 current selection, route graph equality/restrictions, exact agents/modes/artifacts, counters, stop-before-DEV terminals, and valid route-level parent append-only ownership. Negative Registry fixtures must reject missing ownership, mutable/subagent ownership, and malformed route-level ownership for both architecture self-loops.
2. Add failing import-helper tests for valid captured bytes and for missing file, wrong expected hash, altered CDC, non-`APPROVED` certificate, wrong CDC binding, unknown/non-USER decision, malformed decision log, unsafe relative/absolute path, link escape, partial-option invocation, existing-target mismatch, and source immutability. Add explicit DEC fixtures for another hash, rejection/refusal, generic `APPROVAL`, another artifact, no hash, and two competing hashes; only exact affirmative USER `CDC_APPROVAL` for the captured hash may pass.
3. Freeze `brainstorm-product-design-1.3.0.json`, add 1.4/current catalog mapping and `APPROVED_CDC_DESIGN`, then extend Registry validation only for generic artifact/input graph invariants.
4. Implement the shared approved-CDC evidence parser/validator and non-discoverable atomic snapshot import; extend `init_brainstorm.py` with the all-or-none import CLI while preserving its old invocation byte-for-byte behavior. Test `workflow_candidates` and `find_active_workflow` after every staging write, then two same-target initializers with identical and differing request/metadata/evidence.
5. Add failing intake tests for the new BRAINSTORM source-binding shape, local snapshot/prefix matching, exact-version resolution, malformed bindings, and isolation from the existing DEV bridge; then update intake Skill, validator, references, and compiler instructions.
6. Add failing orchestration tests proving the normal unpinned brief gate still blocks intake, a valid pinned import permits intake without brief/CDC/approval phases, and tampering with each binding after intake makes the parent pre-dispatch utility return blocked before the mocked spawn function is called. Assert zero `architect_brainstorm` spawn calls and zero `SubagentStart` events. Add a separate direct-`SubagentStart` bypass test that starts the agent fixture but refuses assignment/write as defense in depth.
7. Implement route-aware pre-intake resolution, the parent/root pre-dispatch utility and blocked-state result, required-input defense-in-depth validation in `SubagentStart`, and route-level append-only enforcement in Registry/PreToolUse.
8. Extend `full_self_test.py` with a synthetic cross-repository import flow covering parent pre-dispatch, initial architecture, clarification wait/resume, independent review, bounded architecture rework, `REWORK_CDC` fail-closed behavior, budget exhaustion, terminal closure, absence of DEV artifacts/agents, and unchanged source bytes. Exercise both initial and rework USER clarification through the route-owned append-only contract.
9. Update only the Registry/Skill/hook control documentation named above, including the exact safe initializer and parent pre-dispatch commands, route-level parent append-only schema, relative-path base, required hashes, snapshot/prefix semantics, failure reasons, version compatibility, rollback, and mandatory stop before DEV.
10. Run the actual NeoAutomatisation package through the read-only import validator using all three observed hashes; assert its exact affirmative `DEC-055` binding passes and no `20-architecture.md` or `30-review.md` exists before and after. Do not initialize or execute its architecture workflow.
11. Re-run both upstream validators against the same corrected `00-task.md`, then run targeted validators, fast self-test, full self-test, compile checks, and final diffs of only the approved global workflow infrastructure.

## Tests-first strategy

- First failing test: `self_test.py` expects `brainstorm-product-design@1.4.0` and `APPROVED_CDC_DESIGN` while asserting 1.2/1.3 remain exact; it must fail against the current 1.3-only Registry.
- Unit coverage: evidence byte parsing; exact affirmative `CDC_APPROVAL`/SHA binding; SHA-256 normalization/comparison; decision-log prefix; safe path resolution; non-discoverable atomic/idempotent initialization; route-aware pre-intake selection; route-level parent append-only ownership; route graph and counter invariants.
- Integration coverage: initializer -> hidden staging -> atomic publication -> local snapshots/metadata -> task intake -> parent pre-dispatch -> spawn only on success -> SubagentStart defense -> architecture -> review -> architecture rework -> review -> terminal.
- End-to-end coverage when justified: full hook self-test for valid and tampered imports, absence of spawn/SubagentStart on failed parent preflight, clarification anchors under route-level parent ownership, loop exhaustion, source immutability, and no DEV transition.
- Edge and failure cases: absent/unreadable source, absolute/relative paths, spaces and another drive, symlink/reparse escape, wrong or mixed hashes, certificate changed after CDC, DEC approval of another hash, rejected/refused CDC, generic `APPROVAL`, another artifact, zero or multiple decision hashes, USER/decision mismatch, appended local clarification, stale imported prefix, source unavailable after successful import, concurrent initializers, rerun over an existing progressed/different target, and `AUTO-RUN: YES`.
- Compatibility checks: old initializer invocation; current `DISCOVERY_ONLY` and `FULL_DESIGN` flow; exact 1.2 and 1.3 workflow resolution in active/blocked/closed lifecycles; existing DEV intake bridge; existing Git/MCP/human-gate guards.
- Repository-derived commands:
  - `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py --workflow-dir E:\Projets IA\Automatisation\.codex\workflows\cdc-maintenance-documentaire-rag-v2-2-officialisation`

## Rollout and rollback

- Roll out the Registry definition, archived 1.3 file, Project Brainstorm Skill/scripts, Task Intake Skill/validator/compiler instructions, and hook sources as one validated control-plane unit; install hooks only after fast and full tests pass.
- No persistent-data migration is required. Existing workflow metadata retains its exact version.
- Rollback by repointing the catalog’s current `definition` and normal initializer to immutable `1.3.0`, while retaining the `1.4.0` mapping/file so any already compiled 1.4 workflow still resolves exactly. Reinstall the prior hook/Skill set and rerun exact-version tests; never rewrite active `.workflow.json`.
- If an imported 1.4 workflow is already active, pause and complete or explicitly close it under 1.4 rather than downgrading its metadata.

## Architecture fitness checks

- Registry validator rejects unknown phases, agents, modes, artifacts, transitions, counters, paths escaping Registry root, and required inputs outside the declared artifact graph.
- Registry validator accepts both clarification self-loops only with explicit route-level parent append-only ownership and rejects missing, mutable, or subagent ownership.
- Exact-version tests prove 1.2, 1.3, and 1.4 resolve side-by-side and unknown versions fail closed.
- Import contract tests prove captured source bytes, exact affirmative USER `CDC_APPROVAL` hash, local snapshots, task bindings, and decision-log prefix are mutually consistent.
- Parent orchestration tests prove invalid evidence yields a blocked result with no architect spawn or SubagentStart event; direct SubagentStart remains a separate assignment/write defense.
- Hook tests prove only `architect_brainstorm` then independent `review_brainstorm` can run, architecture rework is bounded, and every terminal stops before DEV.

## Data and migration impact

- No product data or schema migration.
- Three existing workflow artifacts are copied as temporary local snapshots. The imported decision log becomes an immutable prefix with permitted append-only local clarification entries.
- The source workflow is never modified. No architecture or review artifact is created in it.

## Security and privacy impact

- The external workflow is untrusted cross-repository input. Fixed filenames, canonical containment, link-escape rejection, exact caller-provided hashes, captured-byte validation, approval/decision cross-binding, atomic target creation, and pre-assignment revalidation provide default-deny behavior.
- Do not log CDC or decision contents; diagnostics identify only path, artifact, failed invariant, and hashes needed for repair.
- Existing BRAINSTORM read-only MCP, no-publish, parent-only decision append, and human clarification controls remain unchanged.

## Performance and operational impact

- Import performs three bounded local file reads and SHA-256 computations; the supplied package is small enough that captured-byte validation is appropriate. No runtime service or external network dependency is introduced.
- Validation adds negligible subprocess/file-check work at intake and subagent assignment.
- Operational failure states must be explicit and actionable: invalid source path, hash mismatch, invalid approval, invalid decision binding, snapshot mismatch, prefix mutation, unknown version/route, or exhausted loop budget.

## Documentation impact

- Update Registry README/version notes, Project Brainstorm activation/routes/pipeline/states/handoff contract, Task Intake routing/source-binding contract, and hook README.
- Document one exact Windows `py -3` initializer invocation and a read-only validation invocation, including quoting paths with spaces.
- State clearly that import snapshots evidence, does not transfer implementation permission, and that positive review closes BRAINSTORM only.

## Risks

- Route addition could weaken the normal brief gate because route starts differ. Mitigation: route-pinned pre-intake resolution plus explicit regression tests for unpinned discovery initialization.
- A route without a parent phase could lose append-only ownership. Mitigation: validated `parent_append_only_artifacts` Registry schema plus the unchanged exact parent/root anchored append utility; never waive ownership validation.
- A hook-only preflight would occur after spawn. Mitigation: mandatory parent pre-dispatch utility before the spawn call, observable blocked state and zero-spawn tests; SubagentStart is defense in depth only.
- A copied decision log must allow later clarifications without losing import integrity. Mitigation: bind the imported byte prefix, then reuse existing append-only anchored suffix validation.
- Duplicate phase JSON could drift from `FULL_DESIGN`. Mitigation: self-tests deep-compare the reused phase contracts and allow only the declared `REWORK_CDC -> BLOCKED` transition difference.
- Global control-plane files are outside the repository and not protected by this worktree’s Git diff. Mitigation: enumerate exact files, snapshot 1.3 before mutation, run complete validators/self-tests, and review global file diffs or checksums explicitly.
- A source may change during import. Mitigation: validate and copy the same captured bytes rather than hash then reopening by path.

## Assumptions

- `brainstorm-product-design@1.4.0` is the next compatible workflow version; adding a managed route and import contract is additive for new workflows but must not mutate prior exact versions.
- Valid reusable evidence is a Project Brainstorm-compatible package containing `05-decision-log.md`, `10-cdc.md`, and `15-cdc-approval.md`; arbitrary CDC formats remain out of scope.
- Imported approval evidence uses exact USER `CDC_APPROVAL` semantics with one explicit matching CDC SHA-256. Generic `APPROVAL` has no proven equivalent repository contract and is rejected by this route.
- Relative external workflow paths are resolved against explicit target `--repo-root`; canonical absolute paths remain supported across repositories and drives.

## Blocking questions

None.

## Out of scope

- Producing or reviewing NeoAutomatisation architecture.
- Importing arbitrary non-Project-Brainstorm CDC formats.
- Editing or re-approving an imported CDC in the new route.
- Creating a new agent, phase, status, artifact, counter, workflow, DEV bridge, product file, commit, push, PR, merge, deployment, or release.
- Refactoring the Registry engine, hook suite, or existing routes beyond the minimal compatibility and preflight changes above.

## Reviewer checklist

- [ ] AC-001 through AC-011 are represented with observable validation.
- [ ] 1.2 and 1.3 remain immutable and exactly resolvable beside 1.4.
- [ ] Import is snapshot-based, atomic, path-safe, and bound across CDC, approval, decision entry, task, and local prefix.
- [ ] Route-level Registry ownership makes `05-decision-log.md` parent-only append-only for both architecture clarification self-loops without a fake interview/approval phase.
- [ ] Invalid evidence is blocked in the parent before spawn; tests observe zero `architect_brainstorm` spawn calls and zero `SubagentStart` events.
- [ ] `DEC-055` succeeds only because its exact affirmative USER `CDC_APPROVAL` decision contains the imported CDC hash; generic, rejected, absent, competing, or different-hash decisions fail.
- [ ] Hidden sibling staging is never discoverable; concurrent/rerun behavior compares request, initializer metadata, provenance, prefix, and every evidence byte.
- [ ] The corrected `00-task.md` is accepted by both intake and change-delivery validators.
- [ ] Normal brief and CDC approval gates are not weakened.
- [ ] Initial architecture, clarification, independent review, bounded architecture rework, and `REWORK_CDC` blocking are fully declared.
- [ ] Every terminal closes before DEV and source proof remains byte-for-byte untouched.
- [ ] Tests fail before implementation and cover positive, negative, compatibility, rollback, and actual read-only proof cases.
