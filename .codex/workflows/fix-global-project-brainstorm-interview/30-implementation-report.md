# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

fix-global-project-brainstorm-interview

## Mode

REVIEW_CORRECTION

## Plan and review inputs

- `.codex/workflows/fix-global-project-brainstorm-interview/00-task.md`
- `.codex/workflows/fix-global-project-brainstorm-interview/10-plan.md`
- `.codex/workflows/fix-global-project-brainstorm-interview/20-plan-review.md` — `APPROVED`
- `.codex/workflows/fix-global-project-brainstorm-interview/40-code-review.md` — `CHANGES_REQUIRED`

## Requirement and acceptance-criteria coverage

- AC-001 through AC-004 — `brainstorm-product-design@1.2.0` now starts both managed routes at the identical parent-owned `brief_interview` gate. The public App/Skill activation contract deterministically runs specialized `init_brainstorm.py --request` before generic intake; the E2E test begins with no workflow files and proves initialization, `NEEDS_BRIEF_INTERVIEW`, compiler/CDC/task-write denial, question cardinality, USER-only unlock, final intake validation, and post-intake CDC reconciliation.
- AC-005 — all three App prompts default to `AUTO-RUN: NO`; all three initializers, fresh/persisted session state, loop-budget fallback, and stop fallback map absent values to `NO/step`, while explicit `YES/continuous` remains covered.
- AC-006 — all seven managed agent TOMLs bind Skills below `C:\Users\rapha\.codex\skills`; all three hook fallback functions use the same root; the bounded active-asset stale-root scan is clear.
- AC-007 and AC-008 — Project Brainstorm Skill, App prompt, pipeline, CDC method, decision-log template, task-intake Skill, compiler/CDC agent contracts, Registry definition/validator, and operator README describe the same ordering. The template explicitly declares USER-owned `BRIEF_VALIDATION` with `brief validé` in Evidence. Registry validation accepts version `1.2.0`, both routes, the evidence contract, existing downstream phases, statuses, transitions, gates, and loop counters.
- AC-009 — `self_test.py` and `full_self_test.py` cover the actual no-preseed activation command, pending/validated briefs, zero/one/multiple questions, USER/actor/field/Unicode evidence cases, decision-template semantics, omitted/NO/YES continuation controls, fresh/persisted session state, all initializers, legacy `1.1.0` rejection, Skill roots, full Brainstorm flow, and the existing DEV smoke route.
- AC-010 — the preflight found no bounded `brainstorm-product-design@1.1.0` workflow before mutation; final scans found no real `1.2.0` product workflow, no stale active root/default, and no repository product-code or unrelated-worktree change caused by this implementation.

## Files changed

- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json` — versioned the workflow to `1.2.0` and declared the shared parent interview/evidence gate before CDC.
- `C:\Users\rapha\.codex\workflow-registry\validate_registry.py` — validates declarative evidence contracts and their parent-gate, artifact, normalization, and status invariants.
- `C:\Users\rapha\.codex\workflow-registry\README.md` — documents the interview-first ordering and canonical `.codex/skills` root.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py` — resolves the shared pre-intake phase, USER decision-log evidence, assignment eligibility, and `.codex/skills` fallback.
- `C:\Users\rapha\.codex\hooks\scripts\common.py` — projects `NEEDS_BRIEF_INTERVIEW`, defaults continuation to false, and fixes delivery/intake Skill roots.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py` — applies the declared parent pre-intake write policy before final task compilation.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_stop.py` — lets a rejected premature compiler return safely and reconciles valid brief evidence after final intake.
- `C:\Users\rapha\.codex\hooks\scripts\stop_gate.py` — keeps missing evidence pending, enforces one observable question per interview turn, and defaults to step mode.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py` — defaults fresh sessions to `AUTO-RUN: NO`, preserves explicit persisted controls, and supplies interview-first parent context.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — adds Registry, evidence normalization, App/default, initializer, root, agent-contract, and compatibility assertions.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — adds behavioral pending/validated interview gates, assignment/write/stop barriers, session controls, legacy-version rejection, full Brainstorm flow, and DEV regression coverage.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` — defines the parent interview, append-only confirmation, explicit phrase, delayed intake, and separate CDC approval.
- `C:\Users\rapha\.codex\skills\project-brainstorm\agents\openai.yaml` — defaults to `NO` and starts with one-question parent discovery.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\pipeline.md` — aligns the canonical sequence and human-gate ownership.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\cdc-method.md` — makes validated parent discovery and final intake CDC preconditions.
- `C:\Users\rapha\.codex\skills\project-brainstorm\assets\templates\05-decision-log.md` — declares `BRIEF_VALIDATION`, mandatory USER ownership, explicit Evidence phrase, and separation from CDC approval.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py` — accepts an explicit raw `--request` without a precreated file and initializes step mode plus the pre-intake Registry routing hints for version `1.2.0`.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md` — delays Project Brainstorm compilation until the decision-log evidence gate is satisfied.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\agents\openai.yaml` — defaults generic intake to `AUTO-RUN: NO`.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\init_intake.py` — derives consistent omitted/single-sided controls and rejects contradictory pairs.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py` — rejects Brainstorm intake without valid brief evidence and preserves deterministic version mismatch.
- `C:\Users\rapha\.codex\skills\change-delivery-workflow\agents\openai.yaml` — defaults DEV App execution to `AUTO-RUN: NO`.
- `C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\init_workflow.py` — defaults new DEV workflow metadata to step mode.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml` — fixes the Skill binding and adds the delayed Brainstorm intake contract.
- `C:\Users\rapha\.codex\agents\architect_feature_bug.toml` — fixes the change-delivery Skill binding.
- `C:\Users\rapha\.codex\agents\reviewer_feature_bug.toml` — fixes the change-delivery Skill binding.
- `C:\Users\rapha\.codex\agents\lead_developer.toml` — fixes the change-delivery Skill binding.
- `C:\Users\rapha\.codex\agents\cdc_brainstorm.toml` — fixes the Project Brainstorm Skill binding and requires validated parent discovery before CDC.
- `C:\Users\rapha\.codex\agents\architect_brainstorm.toml` — fixes the Project Brainstorm Skill binding.
- `C:\Users\rapha\.codex\agents\review_brainstorm.toml` — fixes the Project Brainstorm Skill binding.

## Implementation decisions

- The decision log is the sole authority for the brief gate. Metadata may locate the phase but never substitutes for USER evidence.
- Project Brainstorm activation has one explicit entry point: App/Skill/user-prompt contracts require the specialized initializer with explicit task ID, repository root, request, intake depth, and automation. Generic `init_intake.py` is explicitly excluded from initial Project Brainstorm activation.
- Evidence normalization is exactly Unicode NFKC, casefold, and collapsed whitespace. Accent stripping is not performed; `brief valide` remains invalid.
- The latest applicable `BRIEF_VALIDATION` entry controls the gate, preventing an earlier valid entry from masking a later invalid/retracted validation record.
- The two routes carry byte-equivalent `brief_interview` phase objects, allowing generic pre-intake resolution before a final route exists.
- `subagent_start.py` required no direct edit: its existing unassigned/read-only response is now driven correctly by the updated generic resolver.
- Continuation controls use one invariant: `NO == step == false` and `YES == continuous == true`; contradictory initializer input is rejected.

## Plan deviations

None.

## Tests added or updated

- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — static and unit-level Registry/evidence/root/default/initializer/version coverage plus App/Skill activation-command and decision-template semantics.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — end-to-end behavior beginning with the real specialized initialization command and no precreated workflow files, through all pre-intake barriers, validated intake, existing Brainstorm completion, and DEV compatibility.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| Bounded scan of `C:\Users\rapha\Documents\claude-forge\.codex\workflows` and `C:\Users\rapha\.codex\workflows` for active `brainstorm-product-design@1.1.0` before initial mutation and review correction | PASS | Both preflights were clear; no active matching task found. |
| `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills` | PASS | Registered workflows `brainstorm-product-design`, `dev-change-delivery`, and `general-read-only` validated. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | `V8.2.0 installation self-test passed`; activation command and template semantics asserted. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | No-preseed specialized activation, all interview barriers/unlock, full Brainstorm path, and DEV regression passed. |
| Bounded active-asset `rg` scan for `.agents/skills`, `~/.agents/skills`, and `$HOME/.agents/skills` | PASS | `STALE_ROOT_SCAN_CLEAR`. |
| Bounded active producer/fallback `rg` scan for legacy missing-value `continuous/YES/true` defaults | PASS | `STALE_DEFAULT_SCAN_CLEAR`. |
| Bounded final scan for any real `brainstorm-product-design@1.2.0` workflow in the two known roots | PASS | `NO_REAL_BRAINSTORM_1_2_WORKFLOW_CREATED`. |
| `git status --short --branch` in `C:\Users\rapha\Documents\claude-forge` before and after implementation | PASS | Pre-existing modified/untracked repository paths remain; no product-code path was added by this task. |

## Review findings addressed

### CODE-REVIEW-001

- Disposition: Accepted.
- Correction: Wired the public Project Brainstorm App, Skill, pipeline, and user-prompt context to the specialized `init_brainstorm.py` command with explicit activation inputs; added direct `--request` support and prohibited generic `init_intake.py` as the initial path.
- Verification: `full_self_test.py` now starts with no workflow directory, executes the real initializer, asserts immutable request/log/metadata creation and `NEEDS_BRIEF_INTERVIEW`, then verifies compiler/CDC/task-write barriers, 0/1/2-question handling, USER-only unlock, final intake validation, and CDC eligibility.

### CODE-REVIEW-002

- Disposition: Accepted.
- Correction: Added `BRIEF_VALIDATION` to `assets/templates/05-decision-log.md` with mandatory `Actor: USER`, explicit `brief validé` Evidence semantics, and separation from CDC `APPROVAL`.
- Verification: `self_test.py` reads the active template and asserts all three Registry-aligned semantics.

## Documentation updated

- Project Brainstorm Skill, App prompt, pipeline, and CDC method now distinguish brief validation from later CDC approval.
- Project Brainstorm activation documentation now exposes the specialized initializer command and explicitly excludes generic intake initialization before the brief gate.
- The decision-log template now documents the exact USER evidence needed to close the brief gate.
- Task Intake Skill documents decision-log input and delayed Project Brainstorm compilation.
- Registry README documents the parent interview ordering and `.codex/skills` root.
- Compiler and CDC agent contracts state the same pre-CDC ordering.

## Remaining limitations

- Hook enforcement proves one observable interrogative per pending turn; whether the question is materially useful remains a semantic parent/Skill responsibility, as approved.
- The Registry remains single-version. Active legacy-workflow preflight is still required before any future incompatible Registry rollout or rollback.

## Blockers

None.

## Out-of-scope observations

- The repository contained extensive unrelated modified and untracked work before implementation; it was preserved and not inspected as implementation scope.
- No historical workflow, session, log, attachment, unrelated `.agents` asset, product source, connector, Git publication, deployment, or release was changed or invoked.
