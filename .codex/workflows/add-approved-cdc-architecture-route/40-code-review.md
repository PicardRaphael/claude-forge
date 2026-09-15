# Code Review

## Status

APPROVED

## Task

add-approved-cdc-architecture-route

## Reviewed evidence

- `.codex/workflows/add-approved-cdc-architecture-route/{00-request.md,00-task.md,10-plan.md,20-plan-review.md,30-implementation-report.md}`
- Previous code-review findings `CODE-REVIEW-001` through `CODE-REVIEW-005`
- Current repository Git status and the reported installed control-plane files under `C:\Users\rapha\.codex`
- `workflow-registry/{registry.json,validate_registry.py,README.md,workflows/brainstorm-product-design*.json}`
- `skills/project-brainstorm/{SKILL.md,references/pipeline.md,references/workflow-states.md,references/handoff-contracts.md,scripts/approved_cdc_import.py,scripts/append_decision.py,scripts/init_brainstorm.py,scripts/validate_handoff.py,assets/templates/05-decision-log.md,assets/templates/15-cdc-approval.md}`
- Task Intake validator, Project Brainstorm pre-dispatch integration, hook source, installer tests, global hook configuration, and installed runtime
- Read-only NeoAutomatisation package `E:\Projets IA\Automatisation\.codex\workflows\cdc-maintenance-documentaire-rag-v2-2-officialisation`

## Review scope assessment

This is correction cycle 2, the final configured code-correction cycle. The `claude-forge` Git worktree contains only the updated `30-implementation-report.md` and this review in the task path. The implementation is installed under `C:\Users\rapha\.codex`, which is not a Git worktree, so no complete Git diff exists for those files. I resolved that scope limitation by inspecting the installed files named in the implementation report, exercising the changed approval path directly, running the native source and runtime validations, and comparing all installed hook runtime bytes with their source counterparts. No NeoAutomatisation product file or source workflow artifact was modified.

## Finding summary

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| IMPORTANT | 0 |
| SUGGESTION | 0 |

## Blocking findings

None.

## Important findings

None.

## Suggestions

None.

## Requirement and plan compliance

- AC-001, AC-004, AC-005, AC-006, AC-009, AC-010, and AC-011 remain satisfied by the validated `brainstorm-product-design@1.4.0/APPROVED_CDC_DESIGN` graph, exact-version mappings, bounded architecture rework, independent review, stop-before-DEV terminals, documentation, and compatibility matrices.
- AC-002, AC-003, and AC-008 are now satisfied. `approved_cdc_import.py:canonical_cdc_approval_hash` full-matches one exact French statement and compares its sole uppercase SHA-256 capture with the CDC. No semantic free-text inference or finite linguistic denylist remains in the approval validation path.
- AC-007 remains satisfied by the real NeoAutomatisation package: `DEC-055` and the three declared hashes validate, while `20-architecture.md` and `30-review.md` remain absent.
- The correction follows the approved plan's stronger deterministic approval invariant and introduces no product, Registry-graph, compatibility, or scope deviation.

## Closure of previous findings

- `CODE-REVIEW-001`: closed. The prior positive-regex/denylist was replaced by a single exact canonical decision form. The previously accepted `may approve`, `has not decided`, `approves if`, and `plans to approve` probes now each fail with `INVALID_DECISION_BINDING`, while the real canonical `DEC-055` succeeds.
- `CODE-REVIEW-002`: remains closed. Every imported-route phase requires the exact compiled task, and pre-dispatch plus `SubagentStart` validate its route and snapshot bindings before token issuance or assignment.
- `CODE-REVIEW-003`: remains closed. The imported log prefix and authenticated full-log head fail closed against unauthenticated suffixes; only anchored USER clarification reconciliation may advance the head.
- `CODE-REVIEW-004`: remains closed. The full source matrix executes the positive route, clarification/resume, independent review, architecture rework, budget exhaustion, and `REWORK_CDC -> BLOCKED` through real validators and hooks.
- `CODE-REVIEW-005`: remains correctly separated as `BLOCKED_USER_ACTIVATION`. Runtime installation is statically valid, but restart and explicit review/trust of the global user hooks are a USER-owned operational gate and were not simulated.

## Functional assessment

The canonical validator, approval producer, templates, documentation, pre-dispatch path, and tests now agree on one byte-exact approval contract:

`L'utilisateur approuve sans condition le CDC consolidé 10-cdc.md dont l'empreinte SHA-256 est <64HEX>.`

`append_decision.py` recomputes the current `10-cdc.md` hash, requires actor `USER`, requires the `10-cdc.md,15-cdc-approval.md` artifact set, and rejects a caller-provided non-canonical decision. The imported route still starts at architecture, assigns only `architect_brainstorm` then independent `review_brainstorm`, bounds rework with the declared counters, and terminates before DEV.

## Test assessment

The regression coverage is behavior-focused and adequate for the corrected boundary. The fast matrix exercises canonical production and rejection of English/French modal, undecided, conditional, future-intent, altered-text, punctuation, case, and competing-hash forms through import and dispatch defenses. The full source matrix covers the integrated route and historical workflow behavior. Independent probes reproduced the four formerly accepted statements against the real DEC-055 package with recalculated decision-log hashes; all four were rejected and the genuine package passed.

## Security, compatibility, and operational assessment

- Security: Approval is now an allowlisted exact machine contract rather than inferred natural language. Snapshot hashes, certificate binding, USER/type/artifact checks, authenticated decision-log state, exact task validation, and single-use dispatch-token checks remain fail-closed.
- Compatibility: `brainstorm-product-design@1.2.0` remains SHA-256 `E283342E8FCA0272379BB9030FBD6AEAA0E5246B3CD5497F5137FFC6DC90AFA1`; `@1.3.0` remains `3DA4124D8235F6C1C515AE2E88AA50EDEDDCD5FB83B4160CE95F09AB53690BEC`; `1.4.0` is mapped as the current definition.
- Runtime: All 14 source hook Python files have byte-identical installed counterparts, all ten configured global event targets exist, and `features.hooks = true`.
- Activation: `config.toml` contains project-local trusted hook hashes but no trust entries for `C:\Users\rapha\.codex\hooks.json`. This is the documented USER activation gate, not a code-review defect or simulated success.

## Architecture and maintainability assessment

The correction reduces complexity at the trust boundary: one canonical producer and one exact validator replace an extensible natural-language heuristic. The route's existing snapshot, authenticated-head, exact-version, parent pre-dispatch, independent-review, and bounded-rework boundaries remain intact and proportionate.

## Validations independently executed

| Command or inspection | Result | Notes |
|---|---|---|
| Registry validator | PASS | All installed workflows, versions, routes, ownership, inputs, transitions, and counters accepted |
| Fast source self-test | PASS | `V8.2.0 installation self-test passed` |
| Fast installed-runtime self-test | PASS | Passed against `hooks/workflow-suite` |
| Full source self-test | PASS | Completed in 62.5 seconds; Registry, DEV compatibility, Brainstorm stop, memory, human gates, MCP, and hook matrix passed |
| Exact canonical implementation inspection | PASS | One full-match regex and one producer function; no prior inference/denylist symbols remain |
| Real NeoAutomatisation DEC-055 probe | PASS | Accepted `DEC-055` and exact CDC, approval, and decision-log hashes |
| `may approve` probe | PASS | Rejected with `INVALID_DECISION_BINDING` |
| `has not decided` probe | PASS | Rejected with `INVALID_DECISION_BINDING` |
| `approves if` probe | PASS | Rejected with `INVALID_DECISION_BINDING` |
| `plans to approve` probe | PASS | Rejected with `INVALID_DECISION_BINDING` |
| Approval producer probe | PASS | Non-canonical statement rejected; canonical statement emitted with recomputed current CDC hash |
| Source/runtime byte comparison | PASS | 14 source files, 14 runtime files, zero missing files, zero mismatches |
| NeoAutomatisation import CLI and handoff validator | PASS | Exact `DEC-055` package accepted read-only |
| NeoAutomatisation architecture/review absence | PASS | Neither `20-architecture.md` nor `30-review.md` exists |
| Intake and implementation-report validators | PASS | Current task intake and correction handoff valid |
| Global hook trust inspection | BLOCKED_USER_ACTIVATION | Installed and enabled; restart plus explicit user review/trust remains required |

## Review blockers

None. The code verdict is reliable. `BLOCKED_USER_ACTIVATION` is a separate post-review human gate rather than unavailable review evidence.

## Required corrections

None.

## Residual risks

- `BLOCKED_USER_ACTIVATION`: do not rely on the new global hook enforcement in a new operational workflow until the user restarts Codex and explicitly reviews/trusts the global hook definitions.
- The installed control plane remains outside Git. Its installer backups, immutable version files, checksums, and source/runtime identity checks remain necessary for future auditability and rollback.
- Parent/root remains the trust source for caller-provided hashes; the route proves package consistency and controlled evolution, not an external signer identity.

## Final verdict

The implementation is correct, adequately tested, compatible, and ready for final integration; only the separate USER-owned global-hook activation gate remains before operational use.
