# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

enforce-brainstorm-opt-in-strict

## Mode

REVIEW_CORRECTION

## Plan and review inputs

- `00-task.md`
- `10-plan.md`
- `20-plan-review.md`
- `40-code-review.md` — `CHANGES_REQUIRED`; `CODE-REVIEW-001`, `CODE-REVIEW-002`, `CODE-REVIEW-003`, and round-2 `CODE-REVIEW-004` accepted and corrected.

## Requirement and acceptance-criteria coverage

- AC-001 — `user_prompt_mode.py`, the global router contract, and the two intake Skills now require a current-prompt `$project-brainstorm` token or autonomous `MODE: BRAINSTORM` header before creating a new Brainstorm target. Narrative, quoted, listed, escaped, inline, fenced, and historical occurrences do not activate it. Source and runtime full suites verify that prose cannot initialize or write a CDC.
- AC-002 — conflicting mode headers and materially ambiguous requests fail closed with instructions for one parent-owned mode question; generic intake rejects `AUTO`, `BRAINSTORM`, and `GENERAL` before directory creation. Tests verify the no-side-effect rejection.
- AC-003 — explicit Brainstorm activation still initializes the declared normal routes at `brief_interview`; the existing USER/`BRIEF_VALIDATION`/`brief validé` gate remains covered by the full integration suite.
- AC-004 — the explicit approved-CDC import, exact Registry version/route and hash-bound snapshot checks remain unchanged and pass the full source and runtime integration suites. A historical Brainstorm opt-in cannot initialize a new import target.
- AC-005 — managed-target classification now occurs only after lexical canonicalization. Absolute/relative aliases, `.`/`..`, parent-before-`workflows`, Win32 trailing-dot/space aliases, extended/device paths, case aliases of protected filenames, junctions, and file-level symlink/reparse targets fail closed before Registry authorization. Write/Edit and every apply-patch target use the same resolver. Every `mcp__*` call is independently default-denied unless its exact capability ID has one unambiguous contract.
- AC-006 — valid phase-owner writes remain allowed only for the canonical direct regular artifact under the exact bound workflow. Existing components are checked with `lstat` through the artifact file immediately before authorization; valid regular-file CDC writes still pass while cross-workflow, case-alias, junction, symlink, and mixed-patch writes fail.
- AC-007 — the global router preserves parent-owned DEV inference and GENERAL read-only behavior. Exact MCP classification is the sole entry authority: explicitly registered read-only tools may run, explicitly registered remote mutations require DEV and existing policy, local mutation requires an exact enabled adapter, and every unknown or conflicting ID is denied in every mode. No verb or input-field heuristic remains.
- AC-008 — no Registry definition was modified. Registry validation and route/gate/import snapshot integration tests pass for `brainstorm-product-design` and `dev-change-delivery`.
- AC-009 — the fast and full suites now additionally cover Write/Edit/apply-patch alias matrices, exact MCP read-only/remote/local/unknown contracts, neutral unclassified IDs (`modify`, `execute_action`, `apply_operation`) with path/destination/list/content lures in every mode, contract conflicts, real Windows task junction and artifact-file symlink targets, external-target preservation, canonical regular-file authorization, and the residual TOCTOU contract. No reparse test was skipped.
- AC-010 — after the correction suites passed on source, the official installer completed; source/runtime SHA-256 parity is exact for all 14 Python hook files, `hooks.json` is byte-identical to its installer backup, and `config.toml` is textually identical to the initial pre-install backup. With zero global-hook trust entries observable, state remains `RESTART_RETRUST_REQUIRED`, never `TRUSTED_READY`.
- AC-011 — final Registry validation, source fast/full suites, runtime fast/full suites, parity, static scans, and scope inspection pass after all three review corrections. No product repository, Registry semantic, local project hook, Git history, or external system was changed.

## Files changed

- `C:\Users\rapha\.codex\AGENTS.md` — defines the strict current-prompt Brainstorm opt-in decision table, ambiguity behavior, continuation boundary, and preserved DEV/GENERAL routing.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml` — prevents the compiler from inferring Brainstorm from prose and constrains generic intake to an already resolved DEV request.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md` — documents strict routing and fail-before-write initialization.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\agents\openai.yaml` — aligns the app-facing intake contract with explicit mode selection.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\references\ambiguity-and-escalation.md` — defines the one-question ambiguity gate and no-initialization behavior.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\init_intake.py` — rejects every generic non-DEV initialization before creating a directory.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` — distinguishes explicit initial activation from assigned internal continuation and forbids historical state from creating a new target.
- `C:\Users\rapha\.codex\hooks\README.md` — documents activation grammar, exact binding/recovery, tool adapters, install/parity checks, and restart/re-trust states.
- `C:\Users\rapha\.codex\hooks\scripts\common.py` — adds canonical target resolution before classification, full reparse inspection, and one exhaustive exact-ID MCP contract registry for read-only, remote mutation, filesystem-local mutation, conflict, and unclassified states; removes verb heuristics and mtime selection.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py` — implements autonomous header/token parsing, conflict handling, current-prompt provenance, compatible continuation, and explicit task-id resume intent.
- `C:\Users\rapha\.codex\hooks\scripts\session_context.py` — reconciles pending initialization and binds only an explicitly resumed or unique valid candidate.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py` — classifies every `mcp__*` ID before any mode/mutation decision, allows only exact read-only contracts, requires DEV for exact remote mutation, denies unclassified/conflicting/local-without-adapter capabilities, and preserves canonical filesystem/Registry authorization.
- `C:\Users\rapha\.codex\hooks\scripts\post_tool_review.py` — promotes or rolls back pending bindings only after command-fingerprint and workflow-state reconciliation.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_start.py` — reconciles pending initialization before managed dispatch.
- `C:\Users\rapha\.codex\hooks\scripts\workflow_status.py` — replaces mtime-based status selection with deterministic unique-candidate resolution.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — adds targeted routing, initialization, canonical-path, transaction, and no-mtime regression tests.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — adds end-to-end fail-closed and valid-managed-flow coverage across source and installed runtime.
- `C:\Users\rapha\.codex\hooks\workflow-suite\common.py`, `post_tool_review.py`, `pre_tool_guard.py`, `session_context.py`, `subagent_start.py`, `user_prompt_mode.py`, and `workflow_status.py` — official installer runtime copies, SHA-256-identical to their sources; correction changed `common.py` and `pre_tool_guard.py` relative to the first review.
- `C:\Users\rapha\.codex\config.toml` — rewritten by the official installer with line-ending-only byte drift; line-normalized content is identical to the pre-install backup and existing project-hook trust entries were preserved.
- `C:\Users\rapha\.codex\hooks.json.backup-20260804-125412`, `hooks.json.backup-20260804-135207`, and `hooks.json.backup-20260804-143809` — recoverable installer backups for the initial and correction rollouts; current `hooks.json` is byte-identical to the latest backup.
- `C:\Users\rapha\AppData\Local\Temp\codex-opt-in-strict-backup-20260804-1254\` — manual pre-install recovery snapshot of runtime hooks, `hooks.json`, and `config.toml`.
- `.codex/workflows/enforce-brainstorm-opt-in-strict/30-implementation-report.md` — this implementation evidence handoff.

## Implementation decisions

- Kept semantic classification at the parent boundary. Hooks parse only explicit autonomous control syntax and never classify ordinary prose with a lexical DEV/BRAINSTORM heuristic.
- Made `current_brainstorm_opt_in` ephemeral and required it for every new Brainstorm target. Persisted Brainstorm state can only continue the exact compatible workflow already bound to the session.
- Replaced implicit filesystem discovery with exact canonical paths and explicit binding. Zero candidates stays unbound, one valid candidate may bind only during declared resume, and multiple candidates require `RESUME_WORKFLOW: <task-id>`.
- Used a pending/reserve/promote transaction around initializer commands so failed or mismatched initialization cannot leave a stale binding.
- Authorized filesystem mutation by tool-specific destination adapters. Unknown local destination aliases, malformed patches, partial multi-target authorization, computed shell destinations, and direct managed-artifact shell writes fail closed.
- Canonicalized every filesystem target before deciding whether it is managed. Canonical classification is lexical and non-following; every existing component through the file is then inspected with `lstat`, and the file's strict resolution must remain the expected direct child.
- Classified every MCP call by exact capability ID before all other MCP decisions. Exact built-ins or `CODEX_READ_ONLY_MCP_TOOLS` register read-only capabilities; exact built-ins or `CODEX_REMOTE_ONLY_MCP_MUTATORS` register remote mutation. Conflicting and unknown IDs fail closed in all modes, remote mutation requires DEV and existing policy, and the filesystem-local adapter table remains empty/disabled.
- Kept the installed Registry read-only and preserved all workflow versions, routes, gates, transitions, artifacts, and import semantics.
- Used the official installer after source validation, retained recoverable backups, and did not write or simulate any `[hooks.state]` trust entry.

## Plan deviations

None material. `workflow_status.py` was updated as the necessary read-only consumer of the approved no-mtime binding rule; this stays within the planned binding design and does not change Registry semantics.

## Tests added or updated

- `hooks/installer/self_test.py` — adds exact MCP read-only/remote/local/unclassified/conflict contract assertions and an explicit regression that `MUTATING_TOOL_HINTS` is absent, alongside canonical alias/reparse/binding tests.
- `hooks/installer/full_self_test.py` — adds neutral unknown MCP IDs with `path`, `destination`, multi-target lists, and content lures; unknown denial in unresolved/DEV/BRAINSTORM/GENERAL; exact read-only allow across modes; exact remote mutation allow only in DEV; and preserves the prior alias/reparse/gate/import matrices.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | Round-2 frozen-source run: `V8.2.0 installation self-test passed` in 34.6 s. Before code correction, the new regression failed because `MUTATING_TOOL_HINTS` still existed, matching `CODE-REVIEW-004`. Real Windows reparse tests remained unskipped. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | Round-2 frozen-source run reported the complete V8.2 PASS; neutral IDs, exact read-only, exact remote mutation, all modes, prior path/reparse cases, and unchanged Registry routes passed. |
| `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\rapha\.codex\hooks\install.ps1` | PASS | Official installer reported updated global hooks/configuration and installed workflow suite V8.2.0; recoverable backups were retained. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\workflow-suite --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | Round-2 installed-runtime fast suite reported `V8.2.0 installation self-test passed` in 37.1 s. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\workflow-suite --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | Round-2 installed-runtime full suite reported the complete V8.2 PASS after 8m31; stderr empty. |
| `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills` | PASS | Registry validation passed; registered workflows remain `brainstorm-product-design`, `dev-change-delivery`, and `general-read-only`. |
| Source/runtime SHA-256 parity audit | PASS | Final post-suite audit: 14 source Python files, 14 runtime Python files, 0 missing files, 0 mismatches. |
| Global install/trust audit | PASS with human gate | 10 hook events, 20 `workflow-suite` references, `[features] hooks = true`, current `hooks.json` equals its backup, config text equals its backup, 0 trust entries for global `hooks.json`, and 10 preserved entries for the project-local hook file. State: `RESTART_RETRUST_REQUIRED`. |
| Static regression scan and `git status --short` | PASS | Removed implementation patterns are absent (`latest_mtime` occurs only in the negative test assertion); only pre-existing workflow artifacts and this workflow directory appear in Git status. |

## Review findings addressed

- `CODE-REVIEW-001` — accepted. Canonicalization now precedes managed classification; all target adapters call the same resolver, aliases and extended forms fail closed, protected filename case is exact, and apply-patch partitions only from canonical resolver results. Regression coverage includes Write, Edit, and apply-patch absolute/relative `.` aliases, parent segments before `workflows`, Windows separators, case, trailing-dot, and valid canonical phase-owner authorization. Final source/runtime fast and full suites pass.
- `CODE-REVIEW-002` — accepted. Added exact MCP capability classification with an empty local adapter allowlist; unknown/local mutations fail closed regardless of `path`, `destination`, multi-target arrays, or content lures. Exact built-in or `CODEX_REMOTE_ONLY_MCP_MUTATORS` remote registrations proceed only in DEV and remain subject to active write policy; BRAINSTORM/GENERAL deny. Final source/runtime full suites pass the synthetic remote-only and unknown-local matrices.
- `CODE-REVIEW-003` — accepted. Reparse inspection now uses `lstat`, includes every existing component through the artifact file, rejects strict resolution away from the expected direct child, and is repeated immediately before authorization. Real Windows task junction and artifact-file symlink tests both ran without skip; resolver and PreToolUse denied them, the external file remained unchanged, and a direct regular CDC file remained authorized. The unavoidable post-hook TOCTOU window is documented in code, AGENTS, README, and Remaining limitations.
- `CODE-REVIEW-004` — accepted. Removed `MUTATING_TOOL_HINTS`, `mutating_mcp_tool()`, and the mutation-only classification gate. `mcp_tool_capability()` now classifies every `mcp__*` exact ID before any decision; only one unambiguous read-only, remote-mutation, or filesystem-local contract is recognized, and everything else is denied in every mode. Regression fixtures cover `modify`, `execute_action`, and `apply_operation` with every requested lure/target form, exact read-only allow, exact remote DEV compatibility, mutation denial outside DEV, contract conflict, and the intentionally empty local adapter table. Source/runtime fast/full suites all pass.

## Documentation updated

- `C:\Users\rapha\.codex\AGENTS.md` — strict global mode contract.
- `C:\Users\rapha\.codex\hooks\README.md` — runtime activation, binding, recovery, adapters, installation, and trust guidance.
- `C:\Users\rapha\.codex\AGENTS.md` and `hooks\README.md` — exhaustive exact-ID MCP classification, `CODEX_READ_ONLY_MCP_TOOLS`, remote mutation registration, empty local-adapter rule, canonical/reparse enforcement, and residual TOCTOU limitation.
- Task-intake and project-brainstorm Skill contracts and app-facing metadata — explicit activation and fail-before-write behavior.

## Remaining limitations

- Operational state is `RESTART_RETRUST_REQUIRED`: Codex App must be restarted and the changed global hooks reviewed/trusted through the application before a post-restart smoke test can establish `TRUSTED_READY`. No trust hash was written or simulated during implementation.
- The complete Windows integration suites are intentionally subprocess-heavy and take several minutes; both source and installed-runtime executions completed successfully.
- PreToolUse authorization and the later tool filesystem open are not atomic. The resolver checks canonical path and all existing reparse components as close as possible to authorization, but a local attacker able to race filesystem replacement retains a residual TOCTOU window; hooks remain guardrails and require sandboxing and least privilege.

## Blockers

None.

## Out-of-scope observations

- Pre-existing changes under `.codex/workflows/add-approved-cdc-architecture-route/` were preserved and not modified.
- The hook-owned `.workflow.json`, Registry definitions, product repositories, project-local hooks, Git history, connectors, deployments, and external systems were not modified.
