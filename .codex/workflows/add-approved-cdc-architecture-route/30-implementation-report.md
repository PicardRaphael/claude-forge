# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

add-approved-cdc-architecture-route

## Mode

REVIEW_CORRECTION

## Plan and review inputs

- `00-task.md`
- `10-plan.md` — `READY_FOR_PLAN_REVIEW`
- `20-plan-review.md` — `APPROVED`
- `40-code-review.md` — `CHANGES_REQUIRED`, correction cycle 2 (final budget).

## Requirement and acceptance-criteria coverage

- AC-001/AC-004/AC-006 — `brainstorm-product-design@1.4.0` declares managed `APPROVED_CDC_DESIGN`, starts at existing `architecture`, uses only `architect_brainstorm` then independent `review_brainstorm`, and has no interview, CDC, approval, DEV agent, or DEV artifact.
- AC-002/AC-003 — `approved_cdc_import.py`, intake validation, parent/root `approved_cdc_pre_dispatch.py`, and `SubagentStart` defense require the exact canonical French USER `CDC_APPROVAL` statement, a valid task bound to `brainstorm-product-design@1.4.0/APPROVED_CDC_DESIGN`, exact snapshot hashes, a fully authenticated decision-log head, and a single-use dispatch token; failures block before token or assignment.
- AC-005 — the route reuses `architecture_rework_cycles` and `repeated_finding_threshold`; `REWORK_ARCHITECTURE` is bounded and `REWORK_CDC` is terminal `BLOCKED`.
- AC-007 — the NeoAutomatisation proof validated read-only with CDC `51E861...E8F0`, approval `E0A063...3D0`, decision log `42F368...383`, and `DEC-055`; hashes and absence of `20-architecture.md`/`30-review.md` were unchanged afterward.
- AC-008 — fast self-tests accept only `L'utilisateur approuve sans condition le CDC consolidé 10-cdc.md dont l'empreinte SHA-256 est <64HEX>.`; every other wording, including modal, undecided, conditional, future-intent, suffix/prefix variation, English, pending/postponed/suspended/denied/refused/revoked, competing hashes, absent/stale/binding-mismatched intake, progressed initializer reruns, or unauthenticated log suffixes fails closed.
- AC-009/AC-010 — immutable 1.2 and byte-identical 1.3 definitions remain exactly mapped beside 1.4; Registry, intake, historical routes, brief gate, clarification loop, DEV compatibility, and hook matrices passed.
- AC-011 — Registry, Project Brainstorm, Task Intake, compiler, and hook documentation now describes exact import/pre-dispatch commands, snapshot/prefix semantics, blocking causes, version compatibility, installation, and mandatory stop before DEV.

## Files changed

- `C:\Users\rapha\.codex\workflow-registry\{README.md,registry.json,validate_registry.py}` — document/map 1.4 and validate generic route artifact ownership/input graph.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json` — current 1.4 definition and `APPROVED_CDC_DESIGN`.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design-1.3.0.json` — immutable byte-for-byte 1.3 snapshot (`3DA412...0BEC`); existing 1.2 remains `E28334...AFA1`.
- `C:\Users\rapha\.codex\skills\project-brainstorm\{SKILL.md,references/pipeline.md,references/workflow-states.md,references/handoff-contracts.md}` — operator, route, fail-closed approval, authenticated decision-log, clarification, and stop-before-DEV contract.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\{approved_cdc_import.py,append_decision.py,init_brainstorm.py,validate_handoff.py}` — canonical CDC approval production/validation, safe atomic snapshot initialization, and imported-prefix validation.
- `C:\Users\rapha\.codex\skills\project-brainstorm\assets\templates\{05-decision-log.md,15-cdc-approval.md}` — exact canonical statement and producer-field contract for new approvals.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\{SKILL.md,references/compiled-task-contract.md,references/routing-and-depth.md,scripts/validate_intake.py}` — route-specific BRAINSTORM snapshot bindings isolated from the DEV bridge.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml` — Registry-pinned imported-route compiler exception only.
- `C:\Users\rapha\.codex\hooks\{README.md,scripts/common.py,scripts/registry_engine.py,scripts/pre_tool_guard.py,scripts/subagent_start.py,scripts/subagent_stop.py,scripts/approved_cdc_pre_dispatch.py}` — route-aware pre-intake, task and evidence validation, parent ownership, authenticated append reconciliation, exact pre-dispatch utility, token/input defense, and installation contract.
- `C:\Users\rapha\.codex\hooks\installer\{self_test.py,full_self_test.py}` — positive, negative, compatibility, concurrency, intake, utility, preflight, and direct-bypass coverage.
- `C:\Users\rapha\.codex\hooks.json` and `C:\Users\rapha\.codex\hooks\workflow-suite\*.py` — canonical user-level installation: 10 global events and 14 final runtime scripts. `config.toml` retains `features.hooks = true`.
- `.codex/workflows/add-approved-cdc-architecture-route/30-implementation-report.md` — assigned implementation handoff.

## Implementation decisions

- Imported evidence is a local byte-for-byte snapshot of fixed Project Brainstorm artifacts, staged outside `.codex/workflows` and published by exclusive same-volume rename; architecture never depends on the source afterward.
- A USER `CDC_APPROVAL` is not inferred from language. Its Decision must byte-for-byte match the single documented French canonical statement with one bound uppercase 64-hex CDC hash. There is deliberately no English or free-text variant.
- `append_decision.py` recomputes the current `10-cdc.md` hash and produces `CDC_APPROVAL` only for USER, the exact `10-cdc.md,15-cdc-approval.md` artifact set, and the canonical statement.
- Route-level `parent_append_only_artifacts` declares only `05-decision-log.md`. The initial full-log head equals the imported prefix; only a canonical, anchored USER `CLARIFICATION` accepted by reconciliation advances that authenticated head.
- Parent pre-dispatch issues a single-use state-bound token only after the exact imported-route task passes the Task Intake validator. `SubagentStart` repeats task/input/evidence validation before consuming the token; direct bypass remains read-only and blocked.
- Snapshot initialization is idempotent only while the target contains the exact pristine initializer state. Intake, token, assignment, resume, blocked, or other progress metadata makes rerun fail closed without overwrite.
- Unpinned discovery initialization ignores specialized non-parent starts when deriving the shared brief gate, preserving `brief_interview` for existing routes.
- User hooks were installed through the canonical installer because source-directory presence alone is not discovery; project-local hooks were not changed.

## Plan deviations

- No approved product or architecture deviation. Correction cycle 2 replaces the review-rejected linguistic inference/denylist with the plan's stronger deterministic human-approval invariant.

## Tests added or updated

- `hooks/installer/self_test.py` — exact canonical positive, producer acceptance/rejection, English/French modal/undecided/conditional/future-intent and non-canonical negative packages, preflight/token/assignment denial, plus retained task/log/version/compatibility/concurrency/tamper coverage.
- `hooks/installer/full_self_test.py` — three real `APPROVED_CDC_DESIGN` flows cover initial architecture, anchored clarification/resume, independent review, architecture rework and positive closure, rework-budget exhaustion, and `REWORK_CDC -> BLOCKED`, while preserving the historical Brainstorm/DEV/hook matrix.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\scripts ...` before correction cycle 2 | EXPECTED FAIL | The modal/undecided/conditional/future-intent regression reached `Invalid CDC approval decision was accepted` under the prior denylist. |
| `py -3 ...\workflow-registry\validate_registry.py --registry-root ... --agents-dir ... --skills-root ...` | PASS | Registry accepted 1.2/1.3/1.4, all routes, ownership, inputs, transitions, and counters. |
| `py -3 -m py_compile <changed Python files>` | PASS | Canonical approval validator/producer and both test modules compiled. |
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\scripts ...` | PASS | Final fast source matrix passed; all eleven non-canonical semantic packages failed import, preflight, token issuance, and assignment, and the producer rejected a modal statement. |
| `py -3 ...\hooks\installer\full_self_test.py --scripts ...\hooks\scripts ...` | PASS | Final full source matrix completed in 61.4 seconds; normal CDC approval uses the canonical producer and all imported clarification/review/rework/exhaustion/terminal flows passed. |
| `py -3 ...\approved_cdc_import.py --source-workflow "E:\Projets IA\Automatisation\..." --repo-root ... --cdc-sha256 ... --approval-sha256 ... --decision-log-sha256 ... --json` | PASS | Returned `DEC-055` and exact three hashes; before/after proof hashes and architecture/review absence were identical. |
| `py -3 ...\task-intake-workflow\scripts\validate_intake.py --workflow-dir ... --registry-root ...` plus three change-delivery handoff validations | PASS | Control intake, task, plan, and approved plan-review handoffs passed. |
| `py -3 ...\project-brainstorm\scripts\validate_handoff.py --workflow-dir "E:\Projets IA\Automatisation\..."` | PASS | Existing approved proof remains `VALID`. |
| `pwsh -NoProfile -ExecutionPolicy Bypass -File C:\Users\rapha\.codex\hooks\install.ps1` | PASS | Created global `hooks.json`, copied runtime scripts, preserved `hooks = true`, requested restart/trust. |
| Global hook JSON/runtime verification script | PASS | Exactly 10 global events; all 10 Windows command targets exist; 14 runtime Python files are byte-identical to source; project `.codex/hooks.json` has no Git change. |
| `py -3 ...\hooks\installer\self_test.py --scripts ...\hooks\workflow-suite ...` | PASS | Fast installed-runtime matrix passed after final installation and byte-identity proof. |

## Review findings addressed

- `CODE-REVIEW-001` — Accepted and corrected again for cycle 2. The linguistic positive-regex/denylist was removed. Import now full-matches one exact French canonical statement and compares its sole captured hash to the CDC. English/French modal, undecided, conditional, future-intent, added-text, punctuation/wording, and all prior adverse variants fail import and pre-dispatch without token or assignment. `append_decision.py` and templates now produce/document only that form.
- `CODE-REVIEW-002` — Accepted. All imported-route phases require `00-task.md`; pre-dispatch and `SubagentStart` run the Task Intake validator against the exact 1.4 route/import metadata. Pristine-only initializer idempotence rejects token, assignment, resume, blocked, or other progressed state. Missing/stale/binding-mismatched task probes create neither token nor assignment.
- `CODE-REVIEW-003` — Accepted. Initial decision log must equal the imported authenticated head. Preflight, assignment, and phase transition reject any raw/unanchored suffix. Only canonical contiguous USER `CLARIFICATION` entries with exact actor/type/artifact and active anchors can reconcile and advance the full-log head.
- `CODE-REVIEW-004` — Accepted. The full source matrix now executes positive, exhausted-rework, and `REWORK_CDC` imported-route flows through the actual initializer, intake validator, pre-dispatch, SubagentStart/Stop, stop reconciliation, reviewer, and Registry transitions.
- `CODE-REVIEW-005` — Accepted as a user-owned operational gate, not a developer mutation. Runtime installation and static/fast validation are complete; restart and explicit global-hook review/trust remain `BLOCKED_USER_ACTIVATION` and were not simulated.

## Documentation updated

- Registry version/route/ownership notes.
- Project Brainstorm initialization, one exact machine-verifiable CDC approval statement, canonical approval producer/templates, exact task/runtime pre-dispatch contract, authenticated log-head progression, clarification, rework, and DEV stop.
- Task Intake route selection and exact snapshot binding shape.
- Hook discovery/installation, runtime location, restart/trust, and imported-route defense.
- Task intake compiler Registry-pinned exception.

## Remaining limitations

- `BLOCKED_USER_ACTIVATION`: Codex must be restarted and the global user-hook definitions explicitly reviewed/trusted before relying on this route in new sessions. This human action was not simulated.

## Blockers

None.

## Out-of-scope observations

- The `claude-forge` worktree contains extensive pre-existing staged and unstaged user changes unrelated to this delivery; none was reverted, cleaned, committed, pushed, or included as implementation work.
- No architecture/review agent was launched for NeoAutomatisation and no product repository file was modified.
