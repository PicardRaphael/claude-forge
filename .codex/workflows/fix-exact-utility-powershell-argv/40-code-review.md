# Code Review

## Status

APPROVED

## Task

fix-exact-utility-powershell-argv

## Verdict

The bounded correction closes the source `CODE-REVIEW-001` and the plan-review path-normalization variant for every runtime exact workflow utility. Raw script tokens are proven inert before path normalization, later argv are subject to the same quote-aware literal-atom contract, legitimate exact invocations remain accepted, and no justified BLOCKING or IMPORTANT finding remains.

## Reviewed evidence

- `00-task.md` — SHA-256 `2D4150B6E48F5A926722A39E3690B2C2EFDD0F63E581F35EDCDFC948CDC2EA8E`.
- Approved `10-plan.md` — SHA-256 `23D586D546823CF772F708586A6E2118E8EEA3FF994CACA215C979DB0626ED74`.
- `20-plan-review.md` — status `APPROVED`, SHA-256 `59470B2241860C85CE69108A381E04F639C8CB28E214E2DB61573CFB8515E008`.
- `30-implementation-report.md` — mode `INITIAL_IMPLEMENTATION`, status `READY_FOR_CODE_REVIEW`, SHA-256 `7A794864D2F47D1B4888D46D23362D00DBEFEC6E3C89B7BC8DF1A309A3EEF371`.
- Bound source implementation report — verified SHA-256 `25F3A747C756D2AD73DCB808804ABD1940C641B3EB039CE43DB5A897094CD37B`.
- Bound source code review and `CODE-REVIEW-001` — verified SHA-256 `3B8C7DA23C0500407C6D4B92D2CF959694B2353D9D0F9E63E954D978E8E8A3DB`.
- Current `C:\Users\rapha\.codex\hooks\scripts\common.py`, `pre_tool_guard.py`, `installer\self_test.py`, and `installer\full_self_test.py`.
- Actual repository Git status, current global-file hashes, runtime exact-utility inventory, parser replay, validator results, and full-test implementation.

## Review scope assessment

The task-attributable implementation is limited to the three approved global files:

- `common.py` — current SHA-256 `5F3D0974EF3ED173BD72AE150C7F8C83D75F05E9BF6AD53A7F288E7E075EB63D`.
- `self_test.py` — current SHA-256 `987512A515F1DE96047A3CD8CA01E1886F2579F635C85C8522A4D79C81249093`.
- `full_self_test.py` — current SHA-256 `338BE628FA8DE07FF323AA93F701418FB9DAF4047B57E9458B536C9A4100AE33`.

`pre_tool_guard.py` remains at the reported unchanged SHA-256 `8179959E4542791B50C0FA8B1D2609D423F56194B351010CA54252E39DB27790`. No Registry phase, route, status, transition, utility inventory, Skill, agent, product-code, repository-configuration, Git, or publication change is attributable to this task. The repository retains extensive unrelated pre-existing modified and untracked work.

The global hook assets have no Git baseline, so historical attribution cannot be reconstructed as a normal Git diff. Current hashes match the implementation report, and direct symbol/test inspection shows only the approved parser boundary and its regression coverage.

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

- AC-001: Satisfied. `parse_exact_workflow_utility` consumes quote-preserving tokens, validates raw token 2 before `expanduser()`/`resolve()`, validates every later argv token, and only then performs exact installed-path lookup.
- AC-002: Satisfied. The tests derive the eight-utility runtime inventory and apply ten post-script vectors plus ten unresolved `vector\..\utility` aliases to every utility. `full_self_test.py:assert_utility_vectors_denied` is invoked in both `architecture` and `architecture_rework_review`, asserting hook denial, byte-identical product and decision-log sentinels, and absence of the static-call sentinel.
- AC-003: Satisfied. Exact canonical paths are exercised quoted and unquoted; every runtime utility has a legitimate full-shape fixture; read-only utilities remain allowed and mutating utilities still reach the unchanged phase/write-policy boundary.
- AC-004: Satisfied. `parse_exact_append_decision`, exact launcher/path behavior, utility classification, structured argv, and the existing workflow behavior remain unchanged.
- AC-005: Satisfied by the recorded complete validation plus independently successful parser, syntax, installation, Registry, intake, and handoff checks. The aggregate handoff validator's known `00-task.md` loop-budget schema mismatch remains upstream and does not affect the implementation.
- AC-006: Satisfied by this independent approval.
- AC-007: Satisfied within the limits of unversioned global assets and the unrelated dirty repository.

## Functional assessment

The source PoC `py -3 "<exact validate_registry.py>" (Get-Date)` no longer parses as an exact utility. The same result holds for all eight runtime utilities and all ten documented vectors. The path-normalization variant is also closed because an unquoted expression-bearing raw path alias is rejected before `Path.resolve()` can erase its unsafe segment.

The parser still returns the established `{script, kind, argv}` shape for legitimate commands, retains `py -3`, resolved exact-path identity, and the read-only/mutating classification. `pre_tool_guard.py` already denies a referenced utility when parsing fails before its read-only allow or mutating write-policy branches, so no guard edit is necessary.

## Test assessment

The regression tests are behavior-focused and inventory-complete:

- 160 independently replayed parser negatives: 8 utilities × 10 vectors × 2 locations.
- 16 independently replayed canonical-path positives: quoted and unquoted paths for all 8 utilities.
- Full-shape positives cover all runtime utilities and fail on inventory drift.
- Initial and rework E2E call sites apply the complete negative matrix and sentinel assertions.
- Existing append-decision, exact-path spoof, actor/provenance, phase, immutable-anchor, clarification, and independent-review coverage remains present.

The independent full E2E invocation exceeded the review command's 184-second output window and completed afterward, so its exit output was not recoverable. This is not treated as a failure: the same current-file hashes have a recorded successful full-suite result, the complete E2E assertions and both phase call sites were inspected, and the narrower independently executed checks passed.

## Security, compatibility, and operational assessment

The new allowlist `[A-Za-z0-9_./\\:+=~-]+` admits only the demonstrated unquoted literal atoms. Parentheses, braces, brackets/static expressions, comma arrays, dollar/at subexpressions, partial quoting, and the tokenizers' existing expansion/control/redirection syntax are rejected before authorization. Quoted tokens remain inert transport, subject to the tokenizer's existing conservative expansion checks.

No authentication, authorization actor, provenance, phase, write-policy, append-only, or publication boundary was weakened.

## Compatibility and operational assessment

Canonical Windows paths remain accepted quoted and unquoted, and representative options, enums, hashes, numbers, timestamps, paths, key/value atoms, empty quoted values, and quoted free text remain compatible. The correction is a linear lexical check with negligible performance impact and no schema, migration, deployment-order, data, or rollback complication.

## Architecture and maintainability assessment

The shared parser is the correct single trust boundary. It avoids eight duplicated `argparse` contracts while keeping semantic CLI validation in each utility. Runtime inventory equality in both test suites prevents a newly registered exact utility from silently escaping the security matrix.

## Validations independently executed

| Command or inspection | Result | Evidence |
|---|---|---|
| Source workflow SHA-256 verification | PASS | Both bound artifacts match `00-task.md` |
| Current workflow input SHA-256 verification | PASS | Plan and plan-review hashes match the approved inputs; report hash recorded above |
| Current `common.py` and `pre_tool_guard.py` execution-path inspection | PASS | Raw token validation precedes normalization; parse failure precedes utility allow |
| Runtime inventory inspection | PASS | Eight exact utilities, including both conditional project-brainstorm utilities |
| Targeted parser matrix | PASS | 160 unsafe checks and 16 canonical positives; zero failures |
| In-memory syntax compilation | PASS | Four relevant Python files compiled without writing generated files |
| Installation `self_test.py` | PASS | `V8.2.0 installation self-test passed` |
| Workflow Registry validator | PASS | Three registered workflows valid |
| Current DEV intake validator | PASS | Intake validation passed |
| Individual plan, plan-review, and implementation-report validators | PASS | All three handoffs valid |
| Full E2E implementation inspection | PASS | Both architecture assignments, all utilities, positives, denial boundary, and byte-identical sentinels are asserted |
| Independent full E2E process | INCONCLUSIVE OUTPUT | Process completed after the execution wrapper timed out; no exit output was captured |
| Final Git status and global-file hash inspection | PASS WITH LIMITATION | Unrelated repository dirt remains; global assets lack a Git baseline |

## Review blockers

None. The uncaptured output from one expensive independent rerun does not prevent a reliable verdict because targeted replay, current code/test inspection, successful installation validation, and the recorded same-hash full-suite result provide sufficient evidence.

## Required corrections

None.

## Residual risks

- Historical line-by-line attribution remains limited because the installed global hook assets are not Git-versioned.
- The literal grammar is intentionally conservative; future legitimate punctuation requirements must be added only with PowerShell-safety evidence and matching positive/negative tests.
- The aggregate change-delivery validator still disagrees with the intake compiler's loop-budget key names in unchanged `00-task.md`; the authoritative intake validator and all implementation-phase handoff validators pass.
