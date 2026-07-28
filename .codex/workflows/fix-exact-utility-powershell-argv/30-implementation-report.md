# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

fix-exact-utility-powershell-argv

## Mode

INITIAL_IMPLEMENTATION

## Plan and review inputs

- `00-task.md` — SHA-256 `2D4150B6E48F5A926722A39E3690B2C2EFDD0F63E581F35EDCDFC948CDC2EA8E`.
- Corrected `10-plan.md` — SHA-256 `23D586D546823CF772F708586A6E2118E8EEA3FF994CACA215C979DB0626ED74`.
- Approved `20-plan-review.md` — SHA-256 `59470B2241860C85CE69108A381E04F639C8CB28E214E2DB61573CFB8515E008`, status `APPROVED`.
- `40-code-review.md` — Not applicable for initial implementation.

## Requirement and acceptance-criteria coverage

- AC-001 — `common.py:parse_exact_workflow_utility` now retains quote metadata, validates raw token 2 before `expanduser()`/`resolve()`, and validates every later argv token with the same quoted-or-literal-atom predicate. Expressions, script blocks, arrays/subexpressions, commas, brackets/static calls, partial quotes, and existing expansion/control syntax fail parsing before exact utility authorization.
- AC-002 — `full_self_test.py:assert_utility_vectors_denied` applies ten unsafe post-script vectors and ten unresolved raw path-alias vectors to every runtime utility under both `architecture` and `architecture_rework_review`; every result is denied at the malformed/non-exact boundary while product and decision-log bytes remain identical and the static-call sentinel remains absent.
- AC-003 — `self_test.py` and `full_self_test.py` require an exact fixture set equal to `known_workflow_utilities()`. Every utility passes canonical quoted and unquoted script paths with a full legitimate shape before activation; read-only shapes pass during both architect assignments and mutating shapes reach the unchanged phase/write-policy denial.
- AC-004 — The existing `parse_exact_append_decision` implementation and its positive, malformed shell, and structured-argv coverage were unchanged; the installation and full E2E suites replayed clarification, immutable-anchor, initial/rework, and independent-review behavior successfully.
- AC-005 — Syntax compilation, installation self-test, full E2E self-test, Registry validation, DEV intake validation, and individual plan/review/report handoff validation passed. The aggregate workflow-directory handoff command reports a pre-existing `00-task.md` loop-budget key mismatch; the canonical intake validator passes that unchanged task.
- AC-006 — Implementation and replay evidence are ready for the independently assigned `CODE_REVIEW` phase; this initial implementation does not self-approve.
- AC-007 — Task-attributable writes are limited to the three approved global files and this report. `pre_tool_guard.py` remained byte-identical at SHA-256 `8179959E4542791B50C0FA8B1D2609D423F56194B351010CA54252E39DB27790`; no Registry, Skill, agent, product, unrelated configuration, Git, publication, or deployment action was performed.

## Files changed

- `C:\Users\rapha\.codex\hooks\scripts\common.py` — added the conservative literal-atom grammar and enforced quote-aware raw-script/argv safety before path normalization and exact utility lookup. SHA-256 changed from `70728A60FD7347C6E923310E03DA060BF343D7911AB7DF2AEE0B8AADC4396D57` to `5F3D0974EF3ED173BD72AE150C7F8C83D75F05E9BF6AD53A7F288E7E075EB63D`.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — added all-runtime-utility inventory equality, canonical quoted/unquoted full-shape positives, safe literal and quoted free-text positives, and complete post-script/raw-alias negative matrices. SHA-256 changed from `3DDD0AAFCF04CBF43338D18AA8AFAE218218D5844DC27A90183D9F36AEFAF303` to `987512A515F1DE96047A3CD8CA01E1886F2579F635C85C8522A4D79C81249093`.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — derives the runtime utility inventory, verifies exact fixture equality, tests full canonical shapes as parent/root, and exercises both unsafe matrices plus sentinel integrity and phase-policy compatibility under initial and rework architect assignments. Post-change SHA-256 is `338BE628FA8DE07FF323AA93F701418FB9DAF4047B57E9458B536C9A4100AE33`; the initial capture began `A2A47C5C056FE20C49615171841B1D495BDE2E85C56DE0BBC7A35CE3B282A9` but the console table truncated its final two characters.
- `.codex/workflows/fix-exact-utility-powershell-argv/30-implementation-report.md` — records the implementation and deterministic evidence required for independent review.

## Implementation decisions

- The shared parser consumes `_tokenize_safe_shell_command` directly so each token retains its `was_quoted` bit.
- One full-match allowlist, `[A-Za-z0-9_./\\:+=~-]+`, covers proven options, identifiers/enums, hashes, numbers, timestamps, key/value atoms, and Windows/POSIX paths. Any token outside that grammar must arrive safely quoted and must still pass the existing conservative tokenizer.
- Raw token 2 is checked before any path expansion or resolution; all later argv tokens are checked before installed-path lookup and authorization. Resolved path identity, utility kind, `py -3`, and returned plain argv remain unchanged.
- `pre_tool_guard.py` required no edit because E2E evidence confirms parser failures reach its existing malformed/non-exact denial before read-only allow or mutating write-policy evaluation.

## Plan deviations

None.

## Tests added or updated

- `self_test.py` exact utility parser coverage — reproduced the pre-fix acceptance of `(Get-Date)`, then covers every runtime utility with ten unsafe post-script vectors, ten unresolved path-alias vectors, canonical quoted/unquoted paths, full per-utility shapes, quoted punctuation/free text, empty quoted values, and safe unquoted atoms.
- `full_self_test.py:utility_command_shapes` — defines one legitimate full command shape for every runtime read-only and mutating utility and fails if runtime registry coverage drifts.
- `full_self_test.py:assert_utility_vectors_denied` — runs both unsafe vector locations for all eight runtime utilities in both architecture assignments, asserts the exact denial boundary, product/decision-log byte identity, static-call sentinel absence, read-only compatibility, and unchanged mutating policy denial.
- Existing append-decision, structured argv, exact-path spoof, actor/provenance, immutable anchor, human-gate, initial/rework, and independent-review cases remain active in the successful suites.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` before the production edit | EXPECTED FAIL | First failure: `py -3 "<exact init_intake.py>" --help (Get-Date)` returned a parsed utility, reproducing the bypass tests-first. |
| `py -3 -m py_compile C:\Users\rapha\.codex\hooks\scripts\common.py C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py C:\Users\rapha\.codex\hooks\installer\self_test.py C:\Users\rapha\.codex\hooks\installer\full_self_test.py` | PASS | Exit code 0 after final edits. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | `V8.2.0 installation self-test passed`. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | `V8.2 registry, DEV compatibility, explicit Brainstorm stop, memory, human-gate, MCP, and hook self-test passed`; stderr empty. |
| `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills` | PASS | Registry validation passed for the three registered workflows. |
| `py -3 C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py --workflow-dir C:\Users\rapha\Documents\claude-forge\.codex\workflows\fix-exact-utility-powershell-argv --registry-root C:\Users\rapha\.codex\workflow-registry` | PASS | Current DEV intake validation passed. |
| `py -3 C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\validate_handoff.py C:\Users\rapha\Documents\claude-forge\.codex\workflows\fix-exact-utility-powershell-argv\10-plan.md`, then `20-plan-review.md`, then `30-implementation-report.md` | PASS | Each implementation-phase handoff validated independently; the report validator passed after the final report edit. |
| `py -3 C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\validate_handoff.py --workflow-dir C:\Users\rapha\Documents\claude-forge\.codex\workflows\fix-exact-utility-powershell-argv` | FAIL — PRE-EXISTING UPSTREAM | The aggregate validator rejects unchanged `00-task.md` because it expects loop-budget keys `plan`, `code`, `repeat`, and `auto`; the task contains compiled Registry keys `plan_correction_cycles`, `code_correction_cycles`, `repeated_finding_threshold`, and `automatic_continuation`. The authoritative intake validator passes the task. |

## Review findings addressed

None for initial implementation.

## Documentation updated

None. The approved contract excludes documentation changes.

## Remaining limitations

- The global hook assets are outside the repository Git baseline. Scope attribution therefore relies on the initial/post hashes, direct changed-symbol inspection, deterministic full-suite evidence, and the preserved repository dirty-state snapshot.
- The parser intentionally remains conservative: free text or punctuation outside the literal atom grammar must be quoted, and syntax already rejected globally by the existing tokenizer remains rejected even when quoted.
- The aggregate handoff validator has a pre-existing schema mismatch with the unchanged compiled `00-task.md`. Individual `10-plan.md`, `20-plan-review.md`, and this report validate, and `validate_intake.py` validates `00-task.md`; correcting either upstream artifact or validator is outside this implementation phase's write policy.

## Blockers

None.

## Out-of-scope observations

- The repository still contains extensive pre-existing modified and untracked work listed by `git status --short`; none of it was edited, staged, cleaned, reset, committed, or published by this implementation.
