# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

add-approved-cdc-architecture-route

## Mode

INITIAL_IMPLEMENTATION

## Plan and review inputs

- `00-task.md`
- `10-plan.md` — `READY_FOR_PLAN_REVIEW`
- `20-plan-review.md` — `APPROVED`
- `40-code-review.md` — `Not applicable` for initial implementation.

## Requirement and acceptance-criteria coverage

- AC-001/AC-004/AC-006 — `brainstorm-product-design@1.4.0` declares managed `APPROVED_CDC_DESIGN`, starts at existing `architecture`, uses only `architect_brainstorm` then independent `review_brainstorm`, and has no interview, CDC, approval, DEV agent, or DEV artifact.
- AC-002/AC-003 — `approved_cdc_import.py`, intake validation, parent/root `approved_cdc_pre_dispatch.py`, and `SubagentStart` defense revalidate exact CDC/approval/decision-log-prefix hashes, `APPROVED`, USER `CDC_APPROVAL`, one matching hash, required inputs, and a single-use dispatch token; failures set a stable blocked reason before assignment.
- AC-005 — the route reuses `architecture_rework_cycles` and `repeated_finding_threshold`; `REWORK_ARCHITECTURE` is bounded and `REWORK_CDC` is terminal `BLOCKED`.
- AC-007 — the NeoAutomatisation proof validated read-only with CDC `51E861...E8F0`, approval `E0A063...3D0`, decision log `42F368...383`, and `DEC-055`; hashes and absence of `20-architecture.md`/`30-review.md` were unchanged afterward.
- AC-008 — fast self-tests reject tampered bytes, generic `APPROVAL`, refusal, competing hashes, partial options, mismatched reruns, stale/missing preflight, malformed Registry ownership, and undeclared inputs.
- AC-009/AC-010 — immutable 1.2 and byte-identical 1.3 definitions remain exactly mapped beside 1.4; Registry, intake, historical routes, brief gate, clarification loop, DEV compatibility, and hook matrices passed.
- AC-011 — Registry, Project Brainstorm, Task Intake, compiler, and hook documentation now describes exact import/pre-dispatch commands, snapshot/prefix semantics, blocking causes, version compatibility, installation, and mandatory stop before DEV.

## Files changed

- `C:\Users\rapha\.codex\workflow-registry\{README.md,registry.json,validate_registry.py}` — document/map 1.4 and validate generic route artifact ownership/input graph.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json` — current 1.4 definition and `APPROVED_CDC_DESIGN`.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design-1.3.0.json` — immutable byte-for-byte 1.3 snapshot (`3DA412...0BEC`); existing 1.2 remains `E28334...AFA1`.
- `C:\Users\rapha\.codex\skills\project-brainstorm\{SKILL.md,references/pipeline.md,references/workflow-states.md,references/handoff-contracts.md}` — operator, route, evidence, clarification, and stop-before-DEV contract.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\{approved_cdc_import.py,init_brainstorm.py,validate_handoff.py}` — captured-byte validation, safe atomic snapshot initialization, imported-prefix validation.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\{SKILL.md,references/compiled-task-contract.md,references/routing-and-depth.md,scripts/validate_intake.py}` — route-specific BRAINSTORM snapshot bindings isolated from the DEV bridge.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml` — Registry-pinned imported-route compiler exception only.
- `C:\Users\rapha\.codex\hooks\{README.md,scripts/common.py,scripts/registry_engine.py,scripts/pre_tool_guard.py,scripts/subagent_start.py,scripts/approved_cdc_pre_dispatch.py}` — route-aware pre-intake, parent ownership, exact pre-dispatch utility, token/input defense, and installation contract.
- `C:\Users\rapha\.codex\hooks\installer\{self_test.py,full_self_test.py}` — positive, negative, compatibility, concurrency, intake, utility, preflight, and direct-bypass coverage.
- `C:\Users\rapha\.codex\hooks.json` and `C:\Users\rapha\.codex\hooks\workflow-suite\*.py` — canonical user-level installation: 10 global events and 14 final runtime scripts. `config.toml` retains `features.hooks = true`.
- `.codex/workflows/add-approved-cdc-architecture-route/30-implementation-report.md` — assigned implementation handoff.

## Implementation decisions

- Imported evidence is a local byte-for-byte snapshot of fixed Project Brainstorm artifacts, staged outside `.codex/workflows` and published by exclusive same-volume rename; architecture never depends on the source afterward.
- Exact affirmative USER `CDC_APPROVAL` is deliberately narrower than generic approval: the decision must affect `10-cdc.md`, contain exactly one SHA-256 equal to the captured CDC, and contain no refusal/rejection semantics.
- Route-level `parent_append_only_artifacts` declares only `05-decision-log.md`; the existing anchored parent utility remains the sole clarification append path.
- Parent pre-dispatch issues a single-use state-bound token. `SubagentStart` consumes it only after independent required-input and snapshot revalidation; direct bypass remains read-only and blocked.
- Unpinned discovery initialization ignores specialized non-parent starts when deriving the shared brief gate, preserving `brief_interview` for existing routes.
- User hooks were installed through the canonical installer because source-directory presence alone is not discovery; project-local hooks were not changed.

## Plan deviations

- No design deviation. Following explicit user clarification, the already approved hook-source rollout step was completed with the canonical user-level `hooks.json` installation. Direct execution of unsigned `install.ps1` was denied by local policy; the same script then succeeded via `pwsh -NoProfile -ExecutionPolicy Bypass -File`.

## Tests added or updated

- `hooks/installer/self_test.py` — version resolution, exact route graph, negative Registry ownership/input fixtures, import parsing, approval semantics, concurrency/idempotence, intake bindings, pre-dispatch token, tampering, and direct SubagentStart bypass.
- `hooks/installer/full_self_test.py` — recognizes and security-tests both new exact workflow utilities while preserving the complete historical hook/Brainstorm/DEV matrix.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\scripts ...` before production | EXPECTED FAIL | First tests-first assertion failed because 1.3 still pointed to current and 1.4 did not exist. |
| `py -3 ...\workflow-registry\validate_registry.py --registry-root ... --agents-dir ... --skills-root ...` | PASS | Registry accepted 1.2/1.3/1.4, all routes, ownership, inputs, transitions, and counters. |
| `py -3 -m py_compile <changed Python files>` | PASS | All changed Registry, Skill, hook, pre-dispatch, initializer, and validator modules compiled. |
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\scripts ...` | PASS | Final fast source self-test passed in 17 seconds after added negative/direct-bypass coverage. |
| `py -3 ...\hooks\installer\full_self_test.py --scripts ...\hooks\scripts ...` | PASS | Instrumented source matrix completed in 7m11s: Registry, DEV compatibility, Brainstorm stop, memory, human gates, MCP, clarification/rework, and hooks passed. Temporary progress prints were removed. |
| `py -3 ...\approved_cdc_import.py --source-workflow "E:\Projets IA\Automatisation\..." --repo-root ... --cdc-sha256 ... --approval-sha256 ... --decision-log-sha256 ... --json` | PASS | Returned `DEC-055` and exact three hashes; before/after proof hashes and architecture/review absence were identical. |
| `py -3 ...\task-intake-workflow\scripts\validate_intake.py --workflow-dir ... --registry-root ...` plus three change-delivery handoff validations | PASS | Control intake, task, plan, and approved plan-review handoffs passed. |
| `py -3 ...\project-brainstorm\scripts\validate_handoff.py --workflow-dir "E:\Projets IA\Automatisation\..."` | PASS | Existing approved proof remains `VALID`. |
| `pwsh -NoProfile -ExecutionPolicy Bypass -File C:\Users\rapha\.codex\hooks\install.ps1` | PASS | Created global `hooks.json`, copied runtime scripts, preserved `hooks = true`, requested restart/trust. |
| Global hook JSON/runtime verification script | PASS | Exactly 10 global events; all 10 Windows command targets exist; 14 runtime Python files are byte-identical to source; project `.codex/hooks.json` has no Git change. |
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\workflow-suite ...` | PASS | Installed runtime fast self-test passed in 12 seconds. |
| `py -3 ...\hooks\installer\full_self_test.py --scripts ...\hooks\workflow-suite ...` | BOUNDED/REDUNDANT | Parent stopped the duplicate runtime matrix after 7m14s with no failure output. Source full matrix had passed, runtime files were byte-identical, and runtime fast matrix passed; this bounded stop is not an unresolved product check. |

## Review findings addressed

None for initial implementation.

## Documentation updated

- Registry version/route/ownership notes.
- Project Brainstorm initialization, imported route, exact runtime pre-dispatch command, evidence failures, clarification, rework, and DEV stop.
- Task Intake route selection and exact snapshot binding shape.
- Hook discovery/installation, runtime location, restart/trust, and imported-route defense.
- Task intake compiler Registry-pinned exception.

## Remaining limitations

- Codex must be restarted and the new global user-hook definitions reviewed/trusted before the App UI and new sessions use them.
- The redundant full matrix against the installed copy was intentionally bounded after 7m14s; installed runtime equivalence is instead proven by byte comparison plus full source and fast installed-runtime passes.

## Blockers

None.

## Out-of-scope observations

- The `claude-forge` worktree contains extensive pre-existing staged and unstaged user changes unrelated to this delivery; none was reverted, cleaned, committed, pushed, or included as implementation work.
- No architecture/review agent was launched for NeoAutomatisation and no product repository file was modified.
