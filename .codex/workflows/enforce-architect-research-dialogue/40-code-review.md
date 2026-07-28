# Code Review

## Status

CHANGES_REQUIRED

## Task

enforce-architect-research-dialogue

## Reviewed evidence

- `00-task.md` — SHA-256 `9424747BA4295B23307889F2E42152616402C28C46A6DA9CE239A9DB8EA72DF6`.
- Approved `10-plan.md` — SHA-256 `5ECDE36B42C3F3EC6400F0695BD8EC3CB46CE6156E36F5192A8FA1356189B69F`.
- `20-plan-review.md` — status `APPROVED`, SHA-256 `5287185148C0050DE809995435B5D804C65D6E7EC00B5299D9E93352995F3828`.
- Cycle-2 `30-implementation-report.md` — mode `REVIEW_CORRECTION`, SHA-256 `25F3A747C756D2AD73DCB808804ABD1940C641B3EB039CE43DB5A897094CD37B`.
- Prior cycle-2 `40-code-review.md` — SHA-256 `EF7A912E90019F643A23BE4DF44F705A2EAD87688360668ACA94758B6D3D7E5F`.
- Current global Registry, hook/parser implementation, decision utility, handoff validator, tests, agent/Skill contracts, and both targeted repository documents.
- Actual Git status and relevant repository state.

## Review scope assessment

The final correction remains within the approved global assets and two targeted documents. The executable global files are not Git-versioned, so current source and deterministic tests remain the primary evidence. The repository still contains the previously recorded unrelated dirty cognition/configuration work; no task-attributable product/configuration or publication change was observed.

The exact `1.2.0` and `1.3.0` definitions, initial/rework clarification state, immutable anchors, research gate, and `design_review` successor remain intact.

## Finding summary

| Severity | Count |
|---|---:|
| BLOCKING | 1 |
| IMPORTANT | 0 |
| SUGGESTION | 0 |

## Blocking findings

### CODE-REVIEW-001

- Severity: BLOCKING
- Confidence: HIGH
- Owner: DEVELOPER
- Affected area: AC-003, AC-009, AC-010, AC-011, AC-012; `common.py:parse_exact_workflow_utility`; `pre_tool_guard.py:main`
- Evidence: The shared tokenizer now preserves quoting and `parse_exact_append_decision` correctly rejects all requested unquoted free-text expressions. However, `parse_exact_workflow_utility` at `common.py:675-688` discards quote metadata and accepts arbitrary unquoted argv after an exact read-only utility path. The real parser accepted `py -3 "<exact validate_registry.py>" (Get-Date)` with argv `["(Get-Date)"]`. Under an active `architect_brainstorm` handoff-only assignment, the real `pre_tool_guard.main` returned no denial because `pre_tool_guard.py:315-316` immediately allows an exact read-only utility. PowerShell evaluates `(Get-Date)` before launching Python; parameterless cmdlets or static expressions with the same shape can have side effects.
- Impact: An architecture subagent can again execute PowerShell expressions outside its handoff by attaching them as apparently valid arguments to an exact allow-listed read-only utility. This is a direct shell-evaluation bypass of the global write/command boundary, even though the original prefixed/chained utility PoCs are now denied.
- Required correction: Apply the quote-aware argument contract to every exact workflow utility, not only `append_decision.py`. Validate each utility's permitted argv shape or require all non-option/free-form values to be safely quoted/structured; reject PowerShell expressions, script blocks, arrays/subexpressions, and static calls before returning the read-only allow decision.
- Required verification: For every allow-listed utility, test `(Get-Date)`, a harmless parenthesized sentinel, script blocks, array/subexpression forms, and static method expressions under both initial and rework architect assignments. Assert hook denial and byte-identical product/decision-log sentinels, while legitimate exact invocations continue to pass.

## Important findings

None.

## Suggestions

None.

## Requirement and plan compliance

- AC-001 through AC-008 are implemented and independently validated: completeness precedes research, clarification loops work in both architecture phases, immutable anchors fail closed, and strict research provenance/relevance/alternative structures are enforced.
- `CODE-REVIEW-002` is closed for `append_decision.py`: `(Get-Date)`, parenthesized sentinel, script block, array/subexpression, dollar subexpression, and static-method shell forms are denied; structured argv preserves the same text literally without creating a sentinel.
- `CODE-REVIEW-003` remains closed: `BLOG` and `yesterday` fail deterministically.
- `CODE-REVIEW-004` is closed: both obsolete names are absent, and both documents contain the exact `20-architecture.md -> 30-review.md -> STOP -> later explicit DEV intake` chain.
- `CODE-REVIEW-001` remains open through an adjacent exact-utility argv path, so AC-009 through AC-012 cannot pass final integration.

## Functional assessment

The product-design workflow behavior itself is correct: `1.2.0` remains immutable and terminal on architecture blocking; `1.3.0` pauses and resumes the same initial or rework phase only after anchored USER clarification; ready architecture advances only to independent `design_review`.

No functional defect was found in completeness, research ordering, source provenance, alternative validation, or clarification reconciliation. The remaining defect is in the command authorization envelope around those phases.

## Test assessment

Registry validation, installation self-test, full E2E, intake validation, and corrected implementation-report validation all passed independently. The requested append-decision PowerShell vectors, structured-argv sentinel, utility-chain PoCs, provenance PoC, and exact documentation chain were also replayed successfully.

The current tests do not apply the new PowerShell expression matrix to generic exact utility argv. That omission permits the remaining blocking bypass despite otherwise strong coverage.

## Security, compatibility, and operational assessment

Parent-only append mutation, immutable decision-log/source anchors, exact-version compatibility, and no-research-before-completeness are sound. The original generic filename substring bypass is removed.

Security remains unsafe because exact read-only utility authorization can still cause shell expression evaluation. The correction-loop budget has reached cycle 2; the parent must apply the workflow's bounded-loop/escalation policy rather than silently entering an unbounded automatic correction.

## Architecture and maintainability assessment

The versioned Registry and generic resume-evidence design remain proportionate. The quote-aware tokenizer fix is sound for `append_decision.py`, but applying different argv safety guarantees to append versus other exact utilities leaves a high-risk inconsistency in a shared authorization layer.

## Validations independently executed

| Command or inspection | Result | Notes |
|---|---|---|
| Upstream/cycle-2 SHA-256 verification | PASS | Bound artifacts match |
| Workflow Registry validator | PASS | All workflows valid |
| Installation `self_test.py` | PASS | `V8.2.0 installation self-test passed` |
| Full `full_self_test.py` | PASS | Initial/rework, utility, provenance, and review E2E passed |
| DEV intake validator | PASS | Current task valid |
| Cycle-2 implementation-report validator | PASS | Report structurally valid |
| `(Get-Date)` append parser PoC | PASS | Denied |
| Parenthesized sentinel append PoC | PASS | Denied; no sentinel |
| Script block append PoC | PASS | Denied |
| Array/subexpression append PoCs | PASS | Denied |
| Static-method append PoC | PASS | Denied |
| Structured argv literal/sentinel PoC | PASS | Literal preserved; no sentinel |
| CODE-REVIEW-001 original chained utility PoCs | PASS | Both denied |
| Exact utility plus `(Get-Date)` PoC | FAIL | Parser and active-architect hook allow it |
| CODE-REVIEW-003 provenance PoC | PASS | Invalid type/date rejected |
| CODE-REVIEW-004 document check | PASS | Obsolete names absent; exact chain present twice |
| Exact 1.2/1.3 transition inspection | PASS | Compatibility and review routing preserved |
| Final Git status inspection | PASS WITH LIMITATION | Global assets lack Git baseline; unrelated dirty files remain |

## Review blockers

None. Evidence is sufficient for `CHANGES_REQUIRED`.

## Required corrections

- Correct the exact-utility argv authorization described in `CODE-REVIEW-001`.
- Because the configured two code-correction cycles are exhausted, return control to the parent for bounded-loop escalation instead of continuing automatically.

## Residual risks

- Global pre-change files are not Git-versioned; historical identity relies on structural-equivalence tests and approved evidence.
- Deterministic validators cannot judge substantive source authority or recommendation quality; independent `review_brainstorm` remains mandatory.
- Unrelated repository dirt continues to limit Git-based attribution for untracked task documents.
