# Task

## ID

fix-global-project-brainstorm-interview

## Mode

DEV

## Intake depth

DEEP

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

Repair global Project Brainstorm discovery and Skill-path contracts

## User request

`modifie tout`

## Expected outcome

Selecting `project-brainstorm` starts a parent-led, one-question-at-a-time
interview. The parent does not compile the final intake or invoke
`cdc_brainstorm` until the user explicitly says `brief validé`. Once the brief
is validated, the accumulated confirmed answers can feed the normal
Registry-backed Brainstorm workflow. All active global Codex assets resolve
Skills below `C:\Users\rapha\.codex\skills`, the default is `AUTO-RUN: NO`, and
Skill metadata, agents, Registry/hook-facing behavior, tests, and documentation
describe the same contract.

## Constraints

- Keep every active global Codex component under `C:\Users\rapha\.codex`.
- Preserve the immutable `00-request.md`.
- Preserve unrelated repository and user changes already present in the dirty worktree.
- Preserve explicit `AUTO-RUN: YES` as a supported override while changing the default to `NO`.
- Preserve Registry-driven routing, declared ownership, human gates, and the prohibition on simulated approval.
- Do not modify product code or start a real product Brainstorm workflow.
- Do not create, commit, push, merge, deploy, release, or delete user assets unless separately authorized.
- Implement the smallest coherent cross-contract correction; do not add unrelated workflow behavior.

## Known context

- The target global discovery Skill's App metadata currently defaults to `AUTO-RUN: YES`.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py` currently falls back to `auto_run = YES`.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py` currently falls back to `~/.agents/skills/<skill-name>`.
- Seven installed agent TOML files currently bind `skills.config` to `C:\Users\rapha\.agents\skills\...`.
- `C:\Users\rapha\.codex\workflow-registry\README.md` currently documents `$HOME/.agents/skills`.
- The target product-discovery definition is enabled and `READY`, but its current declared managed routes begin with the `cdc` phase; the parent-led pre-CDC interview contract is not yet represented consistently.
- The repository has extensive pre-existing modified and untracked files unrelated to this intake; they are not evidence of changes made for this task.
- The current DEV intake explicitly has `AUTO-RUN: YES`; that controls this delivery run and is distinct from the requested future default of `AUTO-RUN: NO`.

## Source workflow bindings

None.

## Acceptance criteria

- AC-001: Selecting the installed `project-brainstorm` Skill with an unvalidated initial idea causes the parent to begin an interactive discovery interview before final intake compilation or any `cdc_brainstorm` invocation.
- AC-002: During the pre-CDC interview, each parent turn asks exactly one material question and waits for the user's answer before asking the next question.
- AC-003: Without an explicit user message containing the phrase `brief validé`, automated tests prove that no final `00-task.md` is compiled for the Brainstorm request and `cdc_brainstorm` is not eligible to start.
- AC-004: After the explicit phrase `brief validé`, the confirmed interview answers are available as durable, auditable inputs without mutating the immutable original request, the final intake validates, and the Registry-backed `cdc_brainstorm` phase becomes eligible under its declared write policy.
- AC-005: When no `AUTO-RUN` value is supplied, Skill metadata and hook/session behavior consistently resolve it to `NO`; an explicit `AUTO-RUN: YES` continues to resolve to `YES`.
- AC-006: A bounded scan of active global Codex Skills, agents, hooks, Registry definitions, validators, and documentation finds no reference to `C:\Users\rapha\.agents\skills`, `~/.agents/skills`, or `$HOME/.agents/skills`; installed Skill bindings resolve below `C:\Users\rapha\.codex\skills`.
- AC-007: The `project-brainstorm` Skill body, App metadata, Brainstorm agent contracts, Registry/hook-facing contracts, self-tests, and operator documentation all state the same ordering: parent interview, explicit `brief validé`, validated final intake, then Registry-controlled CDC execution.
- AC-008: Registry and intake validators accept all updated workflow, agent, Skill, route, phase, gate, and path contracts without inventing an undeclared phase, agent, artifact, status, transition, or loop counter.
- AC-009: Automated behavior coverage includes at least the unvalidated-brief path, one-question-per-turn behavior, validated-brief path, default `AUTO-RUN: NO`, explicit `AUTO-RUN: YES`, global Skill-path resolution, and a regression check for the existing DEV route.
- AC-010: Validation and final diff review show no product-code change, no real Brainstorm workflow execution, no Git publication, and no modification or removal of unrelated dirty worktree changes.

## Investigation targets

- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md`, its `agents\openai.yaml`, parent-orchestration references, templates, and validators.
- `C:\Users\rapha\.codex\skills\task-intake-workflow` and `change-delivery-workflow` metadata or references that define default auto-run or Skill-root examples.
- All active `C:\Users\rapha\.codex\agents\*.toml` `skills.config` bindings and the parent/CDC role boundaries.
- `C:\Users\rapha\.codex\workflow-registry\registry.json`, referenced definitions, validation tooling, and Registry documentation.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py`, `registry_engine.py`, related session/transition guards, installer tests, and full self-tests.
- Repository or global operator documentation that describes Project Brainstorm activation, Skill locations, intake order, or automatic continuation.
- Existing native test and validation commands discovered from the installed Skill and hook tooling.

## Material unknowns

- PLAN_VALIDATION: Determine the Registry-compatible durable location for interview answers and the `brief validé` evidence without changing immutable `00-request.md` or inventing an undeclared artifact.
- PLAN_VALIDATION: Determine the smallest hook/Skill boundary that prevents both final intake compilation and `cdc_brainstorm` startup before brief validation while preserving generic Registry extensibility.
- IMPLEMENTATION_VALIDATION: Inventory every active generated or installed copy that can resolve a Skill path; exclude logs, sessions, caches, and historical workflow evidence from mutation while still testing active configuration comprehensively.
- IMPLEMENTATION_VALIDATION: Define phrase normalization only as needed to recognize the explicitly required `brief validé` phrase without accepting silence or unrelated enthusiasm as approval.
- IMPLEMENTATION_VALIDATION: Confirm how the new default applies to new session state while preserving an explicit existing `AUTO-RUN` value.

## Delegation directive

Execute the enabled managed `FULL` route sequentially:

1. `architecture`: spawn `architect_feature_bug` in `ARCHITECTURE` mode to write only `10-plan.md`.
2. `plan_review`: spawn `reviewer_feature_bug` in `PLAN_REVIEW` mode to write only `20-plan-review.md`.
3. If the declared transition requires it, `plan_correction`: spawn `architect_feature_bug` in `PLAN_CORRECTION` mode to update only `10-plan.md`, then return to `plan_review`.
4. `implementation`: spawn `lead_developer` in `INITIAL_IMPLEMENTATION` mode to implement the approved change and write `30-implementation-report.md`.
5. `code_review`: spawn `reviewer_feature_bug` in `CODE_REVIEW` mode to write only `40-code-review.md`.
6. If the declared transition requires it, `review_correction`: spawn `lead_developer` in `REVIEW_CORRECTION` mode to correct the implementation and update `30-implementation-report.md`, then return to `code_review`.
7. `final_report`: the parent runs `FINAL_INTEGRATION` and writes only `50-final-report.md`.

Do not run phases in parallel. Validate each assigned handoff before following
its Registry-declared transition.

## Human gates

None.

## Loop budget

- Plan correction cycles: 2
- Code correction cycles: 2
- Repeated-finding threshold: 2
- Automatic continuation: YES
- plan_correction_cycles: 2
- code_correction_cycles: 2
- repeated_finding_threshold: 2
- automatic_continuation: YES

## Open questions

None material before architecture. Resolve the recorded plan- and
implementation-validation unknowns from current global assets and tests without
expanding product behavior.

## Out of scope

- Product discovery or creation of a real product CDC.
- Changes to product source code, tests, schemas, migrations, manifests, lockfiles, or production configuration.
- A new workflow unrelated to `project-brainstorm`, task intake, Skill resolution, or the required default-auto-run behavior.
- Cleanup of historical sessions, logs, caches, unrelated `.agents` content, or unrelated dirty repository files.
- Git commit, push, pull request, merge, deployment, release, or destructive cleanup.
