# Plan Review

## Status

APPROVED

## Task

fix-exact-utility-powershell-argv

## Verdict

The corrected plan closes `PLAN-REVIEW-001`: it proves the raw script-path token shell-safe before any expansion or normalization, applies the same predicate to all later argv, covers unresolved path-alias and post-script vectors for every runtime utility in both architecture assignments, and preserves canonical quoted and unquoted invocations. No required correction remains.

## Reviewed evidence

- `.codex/workflows/fix-exact-utility-powershell-argv/00-task.md`.
- Corrected `.codex/workflows/fix-exact-utility-powershell-argv/10-plan.md`, SHA-256 `23D586D546823CF772F708586A6E2118E8EEA3FF994CACA215C979DB0626ED74`.
- Prior `20-plan-review.md` finding `PLAN-REVIEW-001`.
- Source `enforce-architect-research-dialogue/30-implementation-report.md`, verified SHA-256 `25F3A747C756D2AD73DCB808804ABD1940C641B3EB039CE43DB5A897094CD37B`.
- Source `enforce-architect-research-dialogue/40-code-review.md`, verified SHA-256 `3B8C7DA23C0500407C6D4B92D2CF959694B2353D9D0F9E63E954D978E8E8A3DB`.
- `C:\Users\rapha\.codex\hooks\scripts\common.py`: `known_workflow_utilities`, `_tokenize_safe_shell_command`, `parse_exact_workflow_utility`, and `parse_exact_append_decision`.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py:main`.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py:assert_utility_spoofs_denied` and its initial/rework call sites.
- Current eight-utility runtime inventory, including both conditional project-brainstorm utilities.

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

## Required changes

None.

## Requirement and acceptance-criteria coverage

- AC-001: Covered. One quote-aware predicate applies to raw token 2 before `expanduser()`/`resolve()` and to every later argv token before authorization.
- AC-002: Covered. Both unresolved `<parent>\<vector>\..\<name>` aliases and post-script vectors run against every runtime utility under initial and rework `architect_brainstorm`, with denial-boundary and sentinel assertions.
- AC-003: Covered. Every utility receives ordinary full-shape positives, and canonical script paths are tested in quoted and unquoted form while actor, phase, mutability, and write-policy checks remain intact.
- AC-004: Covered. `append_decision.py`, structured argv, clarification, immutable-anchor, rework, and independent-review behavior remain unchanged and are replayed.
- AC-005: Covered by targeted parser/E2E tests, syntax compilation, installation/full self-tests, Registry validation, intake validation, and workflow handoff validation.
- AC-006: Covered by replayable parser and real-hook evidence for both vector locations and both architecture assignments.
- AC-007: Covered. The plan excludes Registry definitions, Skills, agents, documentation, product code, unrelated configuration and dirty files, and all Git/publication actions.

## Scope assessment

The plan remains within the selected security slice. Expected edits are limited to `common.py`, `self_test.py`, and `full_self_test.py`; `pre_tool_guard.py` is eligible only if an observed failing E2E proves the existing malformed-utility denial route needs a minimal correction. No Registry, Skill, agent, documentation, product, workflow-definition, or unrelated repository change is proposed.

## Architecture assessment

The corrected order is safe and proportionate: quote-aware tokenization, lexical validation of raw token 2, only then path expansion/normalization and exact membership lookup, followed by the same validation for later argv. Resolved exact-path identity and utility classification remain authoritative after the raw token is proven inert. The plan avoids duplicating eight `argparse` contracts and preserves the existing authorization architecture.

## Tests and validation assessment

The tests-first sequence is executable and closes the prior gap. It requires pre-fix failures for both post-script argv and unresolved token-2 aliases, derives or exactly verifies the complete runtime inventory, and exercises both negative matrices for all utilities. Canonical quoted/unquoted paths and per-utility legitimate full shapes protect compatibility. Parser assertions establish rejection before mutating phase policy, while real-hook tests under both architecture assignments verify authorization order and byte-identical sentinels.

## Security, compatibility, and operational assessment

The literal atom grammar is restricted to alphanumerics and `_ . / \ : + = ~ -`; PowerShell expression delimiters remain excluded, while the existing tokenizer continues to reject expansion, control, redirection, multiline, and unsafe quoting syntax. Quoted tokens remain the inert transport for free text and punctuation. Compatibility, performance, immediate rollout, fail-closed rollback, and hash-based attribution for unversioned global assets are proportionate.

## Validations independently executed

| Command or inspection | Result | Notes |
|---|---|---|
| Corrected `10-plan.md` handoff validator | PASS | Structurally valid |
| Source workflow SHA-256 verification | PASS | Both cited artifacts match |
| Corrected token-2 ordering inspection | PASS | Lexical safety explicitly precedes `expanduser()`/`resolve()` |
| All-utility matrix inspection | PASS | Both vector locations cover the runtime inventory |
| Initial/rework phase coverage inspection | PASS | Existing call sites are explicitly reused for both assignments |
| Canonical-path compatibility inspection | PASS | Quoted and unquoted exact paths are required positives |
| Scope inspection | PASS | No Registry, Skill, agent, documentation, product, or Git change planned |

## Approved implementation contract

- In `common.py`, retain quote metadata and validate raw token 2 before `expanduser()`/`resolve()`, then validate every later argv token with the same quoted-or-safe-literal predicate.
- Preserve `known_workflow_utilities()`, exact resolved identity, utility classification, returned plain argv, `py -3`, and `parse_exact_append_decision`.
- In `self_test.py`, apply post-script and unresolved path-alias negative matrices to every runtime utility and add per-utility canonical quoted/unquoted full-shape positives.
- In `full_self_test.py`, apply both matrices to every utility under initial and rework architecture assignments, assert malformed/unsafe-boundary denial and byte-identical sentinels, and preserve legitimate read-only and mutating-policy behavior.
- Keep production/test changes to `common.py`, `self_test.py`, and `full_self_test.py`; modify `pre_tool_guard.py` only when a failing E2E demonstrates the minimal need.
- Run and report the complete validation set exactly as specified in `10-plan.md`.
- Do not change Registry definitions, Skills, agents, documentation, product code, unrelated configuration or dirty files, workflow contracts, or Git/publication state.

## Residual risks

- Global hook assets have no clean Git baseline; implementation review must use pre/post hashes, complete task-attributable diffs, deterministic tests, and the preserved initial dirty-state snapshot.
- The grammar is deliberately conservative. Any character-set expansion during implementation requires a demonstrated installed-utility compatibility case and must not admit PowerShell expression delimiters.
