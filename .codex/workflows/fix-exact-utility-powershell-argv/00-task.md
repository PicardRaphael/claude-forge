# Task

## ID

fix-exact-utility-powershell-argv

## Mode

DEV

## Intake depth

STANDARD

## Workflow ID

dev-change-delivery

## Workflow version

1.0.0

## Workflow readiness

READY

## Delivery path

FULL

## Type

BUG

## Initial risk

HIGH

## Title

Close the exact-workflow-utility PowerShell argv authorization bypass

## User request

`go correction sécurité`

Limit the change to the remaining blocking `CODE-REVIEW-001` from the source workflow `enforce-architect-research-dialogue`: apply quote-aware/free-text argv safety to every exact workflow utility, verify the PowerShell attack matrix under initial and rework architecture assignments, preserve legitimate exact invocations, run the full validation suite, and obtain independent code-review approval.

## Expected outcome

Every exact installed workflow utility is authorized only after its shell-form argv has been proven safe from PowerShell expression evaluation. PowerShell expressions, script blocks, arrays/subexpressions, and static calls are denied before the exact read-only or mutating utility allow decision; legitimate exact utility invocations remain permitted; deterministic validation passes; and an independent code review returns `APPROVED`.

## Constraints

- Treat source finding `CODE-REVIEW-001` as normative: the generic exact-utility argv path must no longer allow PowerShell evaluation before Python starts.
- Apply the safety contract to every utility returned by the installed exact workflow utility registry, not only `append_decision.py` and not only read-only utilities.
- Preserve exact installed-path matching, `py -3`, utility read-only/mutating classification, actor/provenance checks, active phase and write-policy checks, and existing `append_decision.py` safety.
- Cover both initial and rework `architect_brainstorm` assignments.
- Preserve legitimate exact invocations and ordinary safe argument values; do not solve the defect by disabling workflow utilities globally.
- Keep the correction global and minimal: no Registry phase, route, status, transition, human-gate, artifact, agent, or loop-counter change.
- Do not modify product code, unrelated repository configuration, or unrelated dirty files.
- Do not perform Git staging, commit, push, pull-request, merge, publication, deployment, cleanup, reset, or history rewrite.
- Use repository-native Windows invocation conventions and the `py -3` launcher.

## Known context

- The source DEV workflow is `C:\Users\rapha\Documents\claude-forge\.codex\workflows\enforce-architect-research-dialogue`.
- Source implementation report: `C:\Users\rapha\Documents\claude-forge\.codex\workflows\enforce-architect-research-dialogue\30-implementation-report.md`, SHA-256 `25F3A747C756D2AD73DCB808804ABD1940C641B3EB039CE43DB5A897094CD37B`, status `READY_FOR_CODE_REVIEW`, mode `REVIEW_CORRECTION`.
- Latest source code review: `C:\Users\rapha\Documents\claude-forge\.codex\workflows\enforce-architect-research-dialogue\40-code-review.md`, SHA-256 `3B8C7DA23C0500407C6D4B92D2CF959694B2353D9D0F9E63E954D978E8E8A3DB`, status `CHANGES_REQUIRED`.
- The latest independent review contains one HIGH-confidence BLOCKING finding, `CODE-REVIEW-001`, and no IMPORTANT or SUGGESTION findings.
- Verified defect path: `common.py:parse_exact_workflow_utility` discards quote metadata and returns arbitrary unquoted argv; `pre_tool_guard.py` then allows an exact read-only utility before PowerShell evaluates that argv.
- Verified proof of defect: `py -3 "<exact validate_registry.py>" (Get-Date)` was accepted under an active architecture handoff-only assignment.
- The installed exact utility registry currently covers task-intake initialization/validation, change-delivery initialization/handoff validation, workflow status, Registry validation, and product-design initialization/handoff validation.
- Existing tests already cover exact-path utility spoofing and `append_decision.py` shell vectors, but do not apply the PowerShell expression matrix to generic exact utility argv.
- The working tree contains extensive unrelated modified and untracked work that must remain untouched.
- The source workflow exhausted its own two code-correction cycles; this new independently compiled DEV task is the bounded route for the remaining security correction.

## Source workflow bindings

None.

## Acceptance criteria

- AC-001: For every utility returned by the installed exact workflow utility registry, shell-form authorization rejects unsafe argv before any read-only or mutating allow decision, including `(Get-Date)`, a harmless parenthesized sentinel expression, script blocks, array/subexpression forms, and static method expressions.
- AC-002: Automated tests exercise the complete unsafe argv matrix against every exact workflow utility under both initial and rework `architect_brainstorm` assignments; each case produces a hook denial and leaves the product sentinel and decision-log sentinel byte-identical.
- AC-003: Automated positive tests prove that legitimate exact invocations for every registered utility still pass with their valid option/value shapes, including safely quoted free-text where applicable, without weakening exact-path, launcher, actor, provenance, phase, write-policy, or mutability enforcement.
- AC-004: The existing `append_decision.py` quote-aware/free-text safety and its structured-argv literal transport remain passing, with no regression in clarification, immutable-anchor, initial/rework, or independent-review workflow behavior.
- AC-005: The targeted parser and hook tests, Python syntax compilation, global Registry validation, installation self-test, full end-to-end self-test, current DEV intake validation, and applicable workflow handoff validation all execute successfully with observed passing results.
- AC-006: An independent `reviewer_feature_bug` code review verifies the implementation and test evidence and returns `APPROVED` with no remaining BLOCKING finding for exact-utility argv authorization.
- AC-007: Final scope inspection shows no Registry phase/route/transition change, no product-code or unrelated-configuration change, no unrelated dirty-file modification, and no Git publication action attributable to this task.

## Investigation targets

- `C:\Users\rapha\.codex\hooks\scripts\common.py`: quote-preserving tokenization, `known_workflow_utilities`, and `parse_exact_workflow_utility`.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py`: exact read-only/mutating utility authorization order and denial boundary.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`: parser-level negative matrix and legitimate exact utility positives.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py`: initial/rework hook PoCs, all-utility coverage, and byte-identical sentinels.
- The source `30-implementation-report.md` and latest `40-code-review.md` bound by SHA-256 in `Known context`.
- The installed workflow Registry and validators needed to confirm no route/phase regression and to execute full validation.

## Material unknowns

- PLAN_VALIDATION: Determine the smallest generic argv contract that distinguishes options, fixed values, paths, and free-text across every registered utility without breaking legitimate invocations.
- IMPLEMENTATION_VALIDATION: Confirm the runtime-resolved exact utility set, including the conditional project-brainstorm utilities, matches the complete positive and negative test matrix.
- IMPLEMENTATION_VALIDATION: Confirm whether safety can be enforced once in the shared quote-aware parser or requires bounded per-utility argv-shape validation for any utility whose legitimate grammar cannot be proven generically.
- NON_BLOCKING: Global installed hook and Registry assets do not have a clean Git baseline; deterministic tests, exact current-file inspection, source hashes, and final dirty-state attribution are the required evidence.

## Delegation directive

Execute the enabled managed `FULL` route sequentially in Registry order:

1. `architect_feature_bug` in `ARCHITECTURE` mode writes only `10-plan.md`.
2. `reviewer_feature_bug` in `PLAN_REVIEW` mode writes only `20-plan-review.md`.
3. If the declared transition requires correction and budget remains, `architect_feature_bug` in `PLAN_CORRECTION` mode updates only `10-plan.md`, then return sequentially to plan review.
4. After plan approval, `lead_developer` in `INITIAL_IMPLEMENTATION` mode implements the bounded correction and writes `30-implementation-report.md`.
5. `reviewer_feature_bug` in `CODE_REVIEW` mode independently reviews the implementation and writes only `40-code-review.md`.
6. If the declared transition requires correction and budget remains, `lead_developer` in `REVIEW_CORRECTION` mode performs only the required correction and updates `30-implementation-report.md`, then return sequentially to code review.
7. After code-review approval, the parent in `FINAL_INTEGRATION` mode writes only `50-final-report.md`.

Use only Registry-declared statuses and transitions. Do not substitute agents, skip independent review, self-approve, or run write phases in parallel.

## Human gates

None.

## Loop budget

- plan_correction_cycles: 2
- code_correction_cycles: 2
- repeated_finding_threshold: 2
- automatic_continuation: YES

## Open questions

None material. The approved architect must resolve the recorded plan-validation unknown from current code and legitimate utility grammars before implementation; any scope, compatibility, or security-boundary expansion requires parent escalation.

## Out of scope

- Reopening or expanding the completed completeness, clarification, research-provenance, relevance, alternatives, documentation, or Brainstorm versioning changes from the source workflow.
- Changing Registry phases, routes, statuses, transitions, human gates, artifacts, agents, versions, readiness, or loop policy.
- Adding a new workflow utility, replacing PowerShell, redesigning the hook framework, or broadly refactoring command parsing beyond what is necessary to close `CODE-REVIEW-001`.
- Modifying application/product code, cognition work, unrelated project configuration, or unrelated documentation.
- Git staging, commit, push, pull request, merge, publication, deployment, destructive cleanup, or history changes.
