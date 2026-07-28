# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: fix-global-project-brainstorm-interview
- Type: BUG

## Classification

- Primary type: BUG
- Secondary tags: AI, INFRASTRUCTURE
- Risk level: HIGH
- Risk justification: The defect spans the globally active Codex discovery Skill, parent orchestration, Registry phase graph, hooks, seven custom-agent Skill bindings, and installer validation. A bad correction can start CDC from an unvalidated idea or make all managed DEV/BRAINSTORM agents unable to load their Skills.

## Objective

Make Project Brainstorm begin with a parent-led, one-material-question-per-turn interview; require explicit USER evidence containing `brief validé` in the append-only decision log before final intake compilation and CDC eligibility; default new App/session behavior to `AUTO-RUN: NO` while preserving explicit `YES`; and resolve every active managed Skill binding below `C:\Users\rapha\.codex\skills`.

## Confirmed requirements

- Preserve immutable `00-request.md`; record confirmed interview answers and validation evidence only in parent-owned append-only `05-decision-log.md`.
- Declare a parent human-gate phase before `cdc` in both managed `brainstorm-product-design` routes. Do not invent an agent or another workflow artifact.
- Before `brief validé`, the parent asks exactly one material question per turn, waits, does not produce final `00-task.md`, and does not invoke `cdc_brainstorm`.
- The validation phrase must be explicit USER evidence for the exact normalized phrase `brief validé`; silence, enthusiasm, or a parent assertion is insufficient.
- After the gate, final intake uses both the immutable request and confirmed decision-log entries, validates normally, and only then makes Registry-controlled CDC eligible.
- An omitted auto-run value resolves to `NO`; explicit `AUTO-RUN: YES` remains supported.
- Active Skill paths resolve under `C:\Users\rapha\.codex\skills`; historical sessions, attachments, caches, logs, and unrelated `.agents` assets are not cleanup targets.
- Preserve unrelated dirty repository and user changes; do not run a real product Brainstorm workflow or publish Git changes.

## Current behavior

- `project-brainstorm/agents/openai.yaml` starts with `AUTO-RUN: YES` and directs intake compilation before any parent interview.
- `hooks/scripts/user_prompt_mode.py:main` falls back to `state.get("auto_run", "YES")`.
- `task-intake-workflow/agents/openai.yaml` and `change-delivery-workflow/agents/openai.yaml` also inject `AUTO-RUN: YES`.
- `task-intake-workflow/scripts/init_intake.py` defaults `--auto-run` to `YES` and `--automation` to `continuous`; `project-brainstorm/scripts/init_brainstorm.py` and `change-delivery-workflow/scripts/init_workflow.py` default to `continuous`.
- `hooks/scripts/common.py:workflow_loop_budget` treats an absent `automatic_continuation` as true, while `hooks/scripts/stop_gate.py:main` treats missing workflow metadata as `continuous`.
- Both Registry routes in `workflow-registry/workflows/brainstorm-product-design.json` use `cdc` as `start_phase`; installer tests assert that `cdc_approval` is the only human gate.
- `project-brainstorm/SKILL.md` and `references/pipeline.md` describe `00-request -> 00-task -> 05-decision-log -> 10-cdc`, so the CDC agent receives no required pre-CDC interview contract.
- `hooks/scripts/registry_engine.py:skill_root`, `hooks/scripts/common.py:skill_root`, and `hooks/scripts/common.py:intake_skill_root` fall back to `.agents/skills`.
- Seven installed agent TOMLs bind `skills.config.path` to `C:\Users\rapha\.agents\skills\...`: `task_intake_compiler`, `architect_feature_bug`, `reviewer_feature_bug`, `lead_developer`, `cdc_brainstorm`, `architect_brainstorm`, and `review_brainstorm`.
- `workflow-registry/README.md` documents `$HOME/.agents/skills`.

## Root cause

The parent discovery interview is only an intended conversational behavior, not a Registry-owned gate with durable evidence. The App prompt and session hook therefore route directly to task compilation, while the Registry considers CDC its first managed phase. Separately, installation assets were moved to `.codex/skills` without updating agent bindings, hook fallbacks, documentation, or regression checks. Default auto-run values also remained independently hardcoded to `YES`, creating contract drift.

## Critical flow and blast radius

- Entry point: selection of the installed `project-brainstorm` Skill/App or an explicit `$project-brainstorm` request in `MODE: BRAINSTORM`.
- Execution flow: App metadata and `user_prompt_mode.py` establish BRAINSTORM/step mode -> parent preserves `00-request.md` and appends each confirmed answer to `05-decision-log.md` -> Registry-declared `brief_interview` human gate remains pending while the parent asks one question and waits -> explicit USER `brief validé` is appended and validated -> `task_intake_compiler` compiles final `00-task.md` from request plus decision log -> intake and Registry validators pass -> `cdc_brainstorm` becomes eligible under the existing `cdc` write policy.
- Upstream callers: Codex App Skill selection, natural-language `$project-brainstorm` invocation, session prompt hook, and task-intake parent orchestration.
- Downstream dependencies: task intake validator/compiler, Registry phase resolution, `cdc_brainstorm`, human CDC approval, architecture/review phases, hook installer self-tests, and seven agent Skill loaders.
- Consumers and data affected: global Codex workflow metadata and temporary workflow artifacts only; no product data or source code.
- Intentionally unaffected areas: DEV phase order and statuses, CDC approval semantics, architecture/review transitions, product repositories, connector permissions, Git policy, historical sessions/logs/caches, and explicit `AUTO-RUN: YES`.

## Relevant files and symbols

- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md`: activation, durable memory, and parent interview ordering.
- `C:\Users\rapha\.codex\skills\project-brainstorm\agents\openai.yaml`: App default and initial parent instruction.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\pipeline.md`: canonical end-to-end sequence and gate ownership.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\cdc-method.md`: CDC inputs and prohibition on replacing the parent interview.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md`: delayed final compilation contract and decision-log input.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\agents\openai.yaml`: generic intake App auto-run default.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\init_intake.py`: request/metadata auto-run normalization.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py`: workflow-version and validated-brief intake checks.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py`: pre-intake metadata and default step-mode initialization.
- `C:\Users\rapha\.codex\skills\change-delivery-workflow\agents\openai.yaml`: DEV App auto-run default.
- `C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\init_workflow.py`: DEV workflow automation default.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json`: both route graphs, `start_phase`, parent gate, required inputs, statuses, and write ownership.
- `C:\Users\rapha\.codex\workflow-registry\validate_registry.py`: declared pre-intake phase/evidence contract validation.
- `C:\Users\rapha\.codex\workflow-registry\README.md`: operator sequence and canonical Skill root.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py:main`: default auto-run resolution and pre-CDC interview context.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py:expected_phase_for_agent`, `skill_root`: pre-intake assignment eligibility, phase/evidence resolution, and generic global Skill-root fallback.
- `C:\Users\rapha\.codex\hooks\scripts\common.py:infer_stage`, `workflow_loop_budget`, `skill_root`, `intake_skill_root`: state-machine projection, continuation fallback, validator/Skill fallbacks, and parent-gate status extraction.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_start.py:main`: reject compiler or CDC assignment while the brief gate is pending.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py:allowed_workflow_artifacts`, `current_assignment`: allow only parent append utility during interview and deny premature `00-task.md`/other artifact writes.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_stop.py:main`: allow an unassigned premature compiler to return without a handoff; synchronize only a validated final intake.
- `C:\Users\rapha\.codex\hooks\scripts\stop_gate.py:main`, `reconcile_parent_phase`: one-question stop boundary, pending behavior, evidence revalidation, and step-mode fallback.
- `C:\Users\rapha\.codex\agents\{task_intake_compiler,architect_feature_bug,reviewer_feature_bug,lead_developer,cdc_brainstorm,architect_brainstorm,review_brainstorm}.toml`: installed `skills.config.path` bindings.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py:main`: static installation/Registry/Skill-root contract tests.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py:main`: end-to-end unvalidated and validated interview paths plus DEV regression coverage.

## Proposed design

Version `brainstorm-product-design` from `1.1.0` to `1.2.0` because adding a start phase, evidence source, status, and write contract changes the executable graph. Add one Registry-declared parent phase, `brief_interview`, as the `start_phase` of `DISCOVERY_ONLY` and `FULL_DESIGN`. It is a human gate owned by the parent, writes only append-only `05-decision-log.md`, and transitions to the existing `cdc` phase only on `BRIEF_VALIDATED`. Its declarative evidence contract requires a latest applicable decision with `Actor: USER`, `Type: BRIEF_VALIDATION`, and an Evidence field containing Unicode-normalized, case-insensitive `brief validé`. The parent records each prior confirmed answer as `Type: CLARIFICATION`. No `00-brief.md`, interview agent, hidden session memory, or private reasoning is introduced.

### Pre-intake state machine

| State | Authoritative evidence | Allowed action | Denied action | Transition |
|---|---|---|---|---|
| `INTERVIEW_PENDING` | `00-request.md` exists; no valid USER `BRIEF_VALIDATION` entry | Parent appends one confirmed clarification through `append_decision.py`, asks exactly one material question, then stops | Registry assignment of `task_intake_compiler`/`cdc_brainstorm`; write of `00-task.md` or any role handoff; automatic continuation | Remain pending after an ordinary answer; move to `BRIEF_VALIDATED` only from valid log evidence |
| `BRIEF_VALIDATED` | Append-only log contains valid USER evidence with exact normalized phrase | Assign `task_intake_compiler`; compile final `00-task.md` from request plus all confirmed log entries | CDC assignment before intake validation; mutation/replacement of request or prior log entries | Successful intake validation and metadata synchronization -> `INTAKE_COMPILED` |
| `INTAKE_COMPILED` | Valid `00-task.md` records workflow version `1.2.0` and one declared route | Re-enter its Registry `brief_interview` start phase and revalidate the same log evidence | Direct jump to `cdc`; acceptance of stale, PARENT, or malformed evidence | `BRIEF_VALIDATED` phase status -> existing `cdc` |
| `CDC_ELIGIBLE` | Validated task plus successfully reconciled parent gate | Assign `cdc_brainstorm` under the existing `cdc` write policy | Any other undeclared phase or write | Existing Registry graph |

Before `00-task.md`, `init_brainstorm.py` persists only hook-owned routing hints needed to locate `brainstorm-product-design@1.2.0` and the pending gate; the decision log remains authoritative. `registry_engine.expected_phase_for_agent` returns no assignment for compiler or CDC while pending. `subagent_start.py` reports the rejected assignment and keeps the spawned process read-only (Codex `SubagentStart` cannot cancel process creation). `pre_tool_guard.py` is the deterministic write barrier: it permits the known append-only decision utility and denies `00-task.md`, role handoffs, and source writes. `subagent_stop.py` lets a rejected premature agent return without demanding a handoff and never synchronizes metadata.

`common.infer_stage` reports `NEEDS_BRIEF_INTERVIEW`, not `NEEDS_TASK_COMPILATION`, until valid evidence exists. `stop_gate.py` always permits a valid pending interview turn to stop regardless of auto-run; it rejects zero or multiple observable interrogatives and asks the parent to correct the response to one. This punctuation rule proves question cardinality, while the Skill retains responsibility for semantic materiality. Missing or malformed evidence returns the pending state and never calls `advance_after_status`, so it cannot become `INVALID_STATUS`. After final intake synchronization, `reconcile_parent_phase` resolves the declared decision-log evidence; only then does `advance_after_status` move to `cdc`.

Use one shared gate-evidence resolver in `registry_engine.py`/`common.py`. It reads the phase’s declarative evidence rule, normalizes with Unicode NFKC plus `casefold`, collapses internal whitespace, requires the accented phrase, and returns `BRIEF_VALIDATED` only for the correct USER log block. Session state and `.workflow.json` may cache the projected state but never substitute for the log.

### Auto-run normalization

The invariant is `AUTO-RUN: NO <-> automation: step <-> automatic_continuation: NO`; `YES <-> continuous <-> YES`. Apply it to every active producer/fallback:

- Set all three installed App defaults to `AUTO-RUN: NO`: `project-brainstorm`, `task-intake-workflow`, and `change-delivery-workflow`.
- In `init_intake.py`, make omitted values resolve to `NO/step`. Preserve legacy callers by deriving the missing half when exactly one of `--auto-run` or `--automation` is supplied; reject contradictory pairs instead of silently choosing.
- In `init_brainstorm.py` and `init_workflow.py`, default `--automation` to `step`; explicit `continuous` remains supported and renders `YES` in request/task metadata.
- In `user_prompt_mode.py`, initialize an absent session key to `NO`, preserve an already persisted explicit `YES`, and let a new explicit header replace the stored value.
- In `common.workflow_loop_budget`, default missing `automatic_continuation` to false. In `stop_gate.py`, default missing metadata automation to `step` and missing task continuation to false.
- Existing workflow metadata that explicitly stores `YES`/`continuous` is read unchanged; defaults apply only when values are absent or a new workflow is initialized.

Change the global fallback root to `codex_home() / "skills"` (or the existing `CODEX_SKILLS_ROOT`/specific environment override) in both hook modules. Rebind all seven agent TOMLs to the corresponding absolute `C:\Users\rapha\.codex\skills\<skill>\SKILL.md`. Extend installation tests to parse every managed agent TOML and prove the resolved path is inside the supplied `.codex/skills` root.

### Version and in-flight policy

The current Registry has one definition per workflow ID and cannot execute `1.1.0` and `1.2.0` concurrently. Before changing global assets, scan the two bounded known roots (`C:\Users\rapha\Documents\claude-forge\.codex\workflows` and `C:\Users\rapha\.codex\workflows`) for non-closed tasks selecting `brainstorm-product-design` version `1.1.0`. Do not scan arbitrary repositories, mutate artifacts, or infer migration permission. If any active `1.1.0` workflow is found, stop implementation with `BLOCKED_NEEDS_INPUT` and ask the parent/user whether to finish it on the old suite or abandon/restart it; never rewrite its `00-task.md` or `.workflow.json`. Closed/historical `1.1.0` evidence remains read-only.

When the bounded scan is clear, install the `1.2.0` Registry, hooks, Skills, agents, tests, and docs atomically. `validate_intake.py` continues to reject a `1.1.0` task against the single current `1.2.0` definition with a clear version-mismatch blocker; this is deterministic incompatibility, not silent migration. Rollback restores the coherent `1.1.0` set only after a bounded scan proves no active `1.2.0` workflow was created; otherwise rollback also requires user disposition.

## Alternatives considered

- Skill/prompt instructions without a Registry gate: rejected because they cannot make CDC ineligibility deterministic or auditable.
- A new interview subagent or `00-brief.md`: rejected because discovery is explicitly parent-led and `05-decision-log.md` already provides declared, append-only durable memory.
- Treating `brief validé` as CDC approval: rejected because brief validation gates CDC creation, while `cdc_approval` remains a separate later human decision bound to `10-cdc.md`.

## Implementation sequence

1. Run the bounded active-workflow preflight. If an active `brainstorm-product-design@1.1.0` workflow exists, make no global mutation and return `BLOCKED_NEEDS_INPUT`; otherwise record the clear preflight in the implementation report.
2. Add failing hook tests for all four pre-intake states and enforcement boundaries: compiler assignment rejection, denied `00-task.md` write, safe premature-agent return, CDC rejection, zero/one/multiple question stop behavior, non-USER evidence rejection, valid USER unlock, post-intake gate reconciliation, and pending-not-invalid behavior.
3. Add failing default tests for all three App metadata files; omitted/NO/YES cases for `init_intake.py`; step/continuous cases for `init_brainstorm.py` and `init_workflow.py`; fresh and persisted session state; missing and explicit stop-gate metadata/task continuation.
4. Add failing version/root tests: both routes report `1.2.0` and start at the identical parent gate; a new `1.2.0` task validates; a `1.1.0` fixture blocks deterministically; all seven TOMLs and three hook fallback functions resolve below `.codex/skills`.
5. Bump `brainstorm-product-design.json` to `1.2.0`, declare the identical `brief_interview` phase/evidence rule in both routes, and extend Registry validation for that contract without altering existing downstream phases or loop counters.
6. Implement the generic evidence/state resolver and enforcement in `registry_engine.py`, `common.py`, `subagent_start.py`, `pre_tool_guard.py`, `subagent_stop.py`, and `stop_gate.py`. Keep the log authoritative and missing evidence pending.
7. Normalize all active auto-run producers/fallbacks in the three App metadata files, three initializers, `user_prompt_mode.py`, `common.workflow_loop_budget`, and `stop_gate.py`, including contradiction rejection and persisted explicit-YES compatibility.
8. Align Project Brainstorm Skill/pipeline/CDC method, task-intake Skill/validator, version fixtures, and Registry README; rebind the seven agent TOMLs.
9. Run targeted tests, Registry validation, full hook self-test, bounded stale-root/default scans, and final diff review. Prove no unrelated dirty file or real product workflow changed.

## Tests-first strategy

- First failing test: in `hooks/installer/full_self_test.py`, submit a Project Brainstorm request without `brief validé`, attempt `task_intake_compiler` start and an `00-task.md` write, and assert unassigned/read-only start context plus deterministic `pre_tool_guard` denial; attempt CDC and assert it is unassigned.
- Unit coverage: decision-log gate parsing for exact lowercase, uppercase, extra whitespace, and Unicode-composed/decomposed `brief validé`; reject `brief valide`, PARENT-authored evidence, phrase outside the Evidence field, silence, and unrelated enthusiasm. Verify missing/malformed evidence maps to `INTERVIEW_PENDING`, not an invalid status.
- Stop-boundary coverage: pending assistant responses with zero, exactly one, and multiple observable interrogatives; only exactly one may stop, and pending interview turns never auto-continue. The Skill/prompt assertion separately requires that question to be material.
- Integration coverage: both Registry routes declare `brief_interview -> cdc`; the pre-intake runtime rejects compiler/task/CDC before valid evidence; task compilation consumes `00-request.md` plus clarification/validation decisions; a valid final intake re-enters and reconciles the gate before resolving the existing CDC phase/write policy.
- End-to-end coverage when justified: extend `full_self_test.py` through pending interview, multiple one-question turns, USER validation, final intake, CDC start, existing CDC approval stop, architecture/review completion, and the existing DEV smoke route.
- Auto-run matrix: parse all three App prompts; run each initializer with omitted values, explicit step/NO, and explicit continuous/YES; reject contradictory `init_intake.py` pairs; exercise new session state, persisted YES, explicit prompt override, missing workflow metadata, and explicit continuous metadata. Assert request headings, `.workflow.json`, loop budget, and stop behavior agree.
- Edge and failure cases: phrase in non-USER or non-evidence fields; malformed/rewritten decision log; rejected compiler stopping without a handoff; stale `.agents` Skill binding; missing environment overrides; explicit step versus continuous mode.
- Compatibility checks: Registry version/phase/status validation; new `1.2.0` task acceptance; deterministic `1.1.0` mismatch blocker without mutation; unchanged CDC approval/rework loops; explicit `AUTO-RUN: YES`; existing DEV route; all agent TOMLs parse with `tomllib`.
- Repository-derived commands:
  - `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - Bounded `rg` scans over `agents`, `hooks`, `workflow-registry`, and the three managed Skills for `C:\Users\rapha\.agents\skills`, `~/.agents/skills`, and `$HOME/.agents/skills`, excluding sessions, logs, caches, attachments, and historical workflow evidence.

## Rollout and rollback

Preflight the bounded known workflow roots before mutation. With no active `1.1.0` workflow, update the Registry to `1.2.0` and install tests/contracts/hooks/agents/docs as one coherent set; do not expose a mixed graph/runtime. Validate the complete installed suite, but do not start a real product workflow. If validation fails before any `1.2.0` workflow is created, restore the coherent `1.1.0` set together. If an active `1.1.0` is found before rollout, or an active `1.2.0` exists before rollback, stop for explicit disposition rather than rewriting workflow artifacts. The single-definition Registry does not promise concurrent 1.1/1.2 execution.

## Architecture fitness checks

- Registry validation proves version `1.2.0` and every route transition, actor, status, output, human gate, required input, evidence source, and append-only write policy are declared.
- Hook tests prove pending state rejects compiler assignment, denies task writes, allows one question then stop, and keeps CDC unassigned; installer tests prove only USER phrase evidence closes the gate.
- Default-matrix tests prove every active App, initializer, session producer, loop-budget fallback, and stop fallback maps missing values to NO/step while preserving explicit YES/continuous.
- Version fixtures prove a new `1.2.0` task validates and a legacy `1.1.0` task blocks without mutation.
- A bounded active-asset scan proves no managed Skill resolver or binding points to `.agents/skills`.
- The DEV smoke route proves the generic hook changes did not hardcode Brainstorm behavior into unrelated workflows.

## Data and migration impact

No persistent product-data migration. Existing Brainstorm decision logs remain valid; new interview entries use the existing append-only `DEC-xxx` structure. No existing `00-task.md` or `.workflow.json` is rewritten. Active `1.1.0` workflows cannot coexist with the single installed `1.2.0` definition and therefore block rollout pending explicit disposition.

## Security and privacy impact

The gate reduces unauthorized automation by requiring explicit USER evidence and preserving it locally. Do not store private chain-of-thought, secrets, or raw hidden transcripts; record only concise confirmed answers and the explicit validation message. Existing read-only Brainstorm MCP and human CDC approval boundaries remain unchanged.

## Performance and operational impact

Negligible local parsing overhead. The intended operational change is additional user turns before CDC and step mode by default. Failures must surface as a pending gate with the next required question or missing evidence, never as silent CDC eligibility.

## Documentation impact

Align the Project Brainstorm Skill, App prompt, pipeline and CDC method, task-intake ordering, and Registry README. Documentation must distinguish pre-CDC brief validation from later CDC approval and show `.codex/skills` as the only active global root.

## Risks

- Registry/task chicken-and-egg: mitigate by treating `brief_interview` as the declared parent gate whose evidence is collected before final compilation and revalidated when the compiled route activates; test both sides explicitly.
- Hook cancellation limitation: `SubagentStart` cannot cancel process creation; mitigate by returning no Registry assignment, deterministic `pre_tool_guard` denial, and a safe `subagent_stop` path that produces no handoff or metadata transition.
- False phrase acceptance: mitigate with declarative USER/evidence-field checks and narrow Unicode-aware normalization without accent stripping.
- Version skew: mitigate with the `1.2.0` bump, bounded preflight, deterministic legacy mismatch, atomic install/rollback, and mandatory human disposition for active workflows.
- Partial global update: mitigate with one installation test covering Registry, hooks, App metadata, agent TOMLs, and docs, plus a bounded stale-root scan.
- Generic hook regression: mitigate by keeping evidence interpretation driven by phase configuration and retaining the DEV end-to-end smoke test.
- Dirty-worktree overwrite: inspect status/diff before each edit group and never restore, format, or include unrelated files.

## Assumptions

- `05-decision-log.md` is the declared durable interview memory and may contain `CLARIFICATION` plus brief-validation entries before CDC without changing its existing append-only ownership.
- The current Registry cannot serve multiple versions. No active `1.1.0` Brainstorm workflow exists in the two bounded roots already inspected; implementation must repeat that preflight and stop if the state changes.
- Exactly one material question is enforced as one interrogative in the parent’s pending-gate turn; explanatory context may precede it but must not introduce additional questions.

## Blocking questions

None.

## Out of scope

- Product discovery for a real product or creation of real CDC/architecture artifacts.
- New interview agents, extra workflow artifacts, product code, schemas, migrations, manifests, or lockfiles.
- Changes to CDC approval semantics, Brainstorm-to-DEV authorization, connector permissions, Git policy, deployment, or publishing.
- Cleanup of historical sessions, logs, caches, attachments, unrelated `.agents` content, or unrelated dirty repository files.

## Reviewer checklist

- [ ] AC-001 through AC-010 are represented, including pre-intake ordering and explicit phrase evidence.
- [ ] The parent gate is declared before CDC in both routes without conflating brief validation and CDC approval.
- [ ] Compiler assignment, `00-task.md` write, and CDC assignment are each denied at a named hook boundary while evidence is pending; missing evidence remains pending.
- [ ] Zero/one/multiple question stop behavior is tested behaviorally.
- [ ] `05-decision-log.md` remains the sole append-only interview memory; no undeclared artifact or agent is introduced.
- [ ] All three App defaults, all three initializers, fresh/persisted session state, loop-budget fallback, and stop fallback agree on NO/step; explicit YES/continuous remains compatible.
- [ ] Registry version is `1.2.0`; active legacy preflight, deterministic `1.1.0` blocker, and rollback policy are explicit and tested.
- [ ] All seven agent bindings and all active hook fallbacks resolve below `.codex/skills`.
- [ ] Tests fail on the current defects before implementation and retain the DEV route regression.
- [ ] Scope excludes unrelated dirty changes, historical assets, product code, and Git publication.
