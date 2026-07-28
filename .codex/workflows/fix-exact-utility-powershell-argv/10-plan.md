# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: fix-exact-utility-powershell-argv
- Type: BUG

## Classification

- Primary type: BUG
- Secondary tags: SECURITY
- Risk level: HIGH
- Risk justification: This is a command-authorization defect at the global PowerShell-to-Python trust boundary. Exact installed-path lookup and workflow authorization are sound only after normalization, but PowerShell can first evaluate expression-shaped content in either the raw script-path token or later argv, allowing an architecture subagent to escape its handoff-only boundary.

## Objective

Make every shell-form invocation returned by `known_workflow_utilities()` fail closed before authorization unless the raw script-path token and every later argv token are either safely quoted or deliberately narrow unquoted literal atoms. Prove the script token safe before `expanduser()`/`resolve()` while preserving resolved exact-path identity, `py -3`, utility mutability, actor/provenance, phase, write-policy, and legitimate invocation behavior.

## Confirmed requirements

- AC-001/AC-002: Apply one generic shell-token safety invariant to the raw script path and all argv for every runtime-resolved exact utility, including conditional project-brainstorm utilities. Deny `(Get-Date)`, a harmless parenthesized sentinel expression, script blocks, arrays/subexpressions, and static-member/call expressions both after the script and inside raw `<utility-parent>\<vector>\..\<utility-name>` aliases under initial and rework `architect_brainstorm` assignments before a read-only or mutating allow decision; product and decision-log sentinels must remain byte-identical.
- AC-003: Preserve legitimate exact invocations for all registered utilities, including canonical script paths in both quoted and unquoted form, ordinary unquoted option/enum/path atoms, and safely quoted free text. Do not globally disable utilities.
- AC-004: Do not alter `append_decision.py`'s stricter fixed-order, quote-aware/free-text parser or its structured-argv literal transport; retain all clarification, immutable-anchor, initial/rework, and independent-review behavior.
- AC-005: Pass parser tests, initial/rework hook E2E tests, syntax compilation, Registry validation, installation and full self-tests, current DEV intake validation, and applicable handoff validation.
- AC-006: Leave sufficient evidence for an independent code review to replay the original PoC and return `APPROVED`.
- AC-007: Do not change Registry definitions, workflow phases/routes/transitions, Skills, agents, documentation, product code, unrelated configuration, unrelated dirty files, or Git/publication state.

## Current behavior

- Verified source evidence matches its bindings: `enforce-architect-research-dialogue/30-implementation-report.md` SHA-256 `25F3A747C756D2AD73DCB808804ABD1940C641B3EB039CE43DB5A897094CD37B`; latest `40-code-review.md` SHA-256 `3B8C7DA23C0500407C6D4B92D2CF959694B2353D9D0F9E63E954D978E8E8A3DB`.
- `common.py:_tokenize_safe_shell_command` already retains a `(value, was_quoted)` pair and rejects shell expansion, chaining, redirection, multiline input, unsafe quote escapes, and partial/mismatched quoting.
- `common.py:parse_exact_workflow_utility` calls `tokenize_safe_shell_command`, which discards `was_quoted`, resolves token 2 before exact lookup, and accepts every remaining token as `argv`.
- `pre_tool_guard.py:main` denies a referenced utility when parsing fails, but immediately allows a successfully parsed read-only utility and delegates a parsed mutating utility only to the existing write-policy check.
- The bound review reproduced `py -3 "<exact validate_registry.py>" (Get-Date)` as accepted during an active architecture assignment. PowerShell can evaluate that expression before Python starts.
- `PLAN-REVIEW-001` additionally reproduced unquoted raw script paths such as `...\workflow-registry\(Get-Date)\..\validate_registry.py`, `...\(Clear-Clipboard)\..\validate_registry.py`, and `...\([System.DateTime]::Now)\..\validate_registry.py`. `Path.resolve()` removes the expression-bearing segment and recognizes the installed utility, but host PowerShell evaluates that segment first.
- `self_test.py` applies the requested expression matrix only to `parse_exact_append_decision`; generic utilities receive only an exact `--help` positive. `full_self_test.py:assert_utility_spoofs_denied` covers exact-path/chaining spoofs in both architecture assignments but not unsafe argv for every utility.

## Root cause

The quote-aware tokenizer establishes shell lexical safety but the generic exact-utility parser erases its quote metadata and performs no shell-token safety check. It also canonicalizes the raw script token before proving that token cannot trigger PowerShell evaluation, so an expression-bearing segment followed by `..` can normalize to an exact registered utility. This creates an authorization-order bug: `pre_tool_guard.main` sees the normalized exact path and returns the utility allow decision before PowerShell evaluates either the raw script token or later argv. `append_decision.py` is not affected because its dedicated parser consumes quote-aware token items, requires the exact expected script, and requires quoted free-text values.

## Critical flow and blast radius

- Entry point: `pre_tool_guard.py:main` handling a `Bash` `PreToolUse` event with a shell-form `command`.
- Execution flow: raw command → dangerous-command checks → quote-aware tokenization → current premature token-2 `expanduser()`/`resolve()` → exact `known_workflow_utilities()` lookup → read-only immediate allow or mutating `check_source_write` → PowerShell evaluates the original script token and argv → Python utility starts or fails after any pre-launch side effect.
- Upstream callers: parent/root and managed subagents invoking installed task-intake, change-delivery, workflow-status, Registry-validation, and product-design utilities through `py -3`.
- Downstream dependencies: `references_workflow_utility` denial routing, utility `read_only`/`mutating` classification, active workflow lookup, actor/provenance checks, current phase, and write policy.
- Consumers and data affected: global hook authorization; a successful bypass can run PowerShell expressions outside an architect's handoff-only scope and could modify repository or workflow data before the selected utility starts.
- Intentionally unaffected areas: installed utility registry membership/classification, utility CLI implementations, `append_decision.py`, Registry definitions, workflow state, product code, documentation, non-utility shell authorization, MCP controls, Git controls, and structured argv.

## Relevant files and symbols

- `C:\Users\rapha\.codex\hooks\scripts\common.py`: `_tokenize_safe_shell_command`, `tokenize_safe_shell_command`, `known_workflow_utilities`, `parse_exact_workflow_utility`, and `parse_exact_append_decision` — shared lexical trust boundary and exact utility inventory.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py`: `main` — existing fail-closed parse-error route and read-only/mutating authorization order; inspect after the parser change but no production edit is expected.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`: current runtime utility loop and append-decision attack matrix — first failing parser regression and positive compatibility coverage.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py`: `assert_utility_spoofs_denied`, pre-workflow exact positives, and its initial/rework call sites — hook-level attack matrix, sentinel integrity, phase coverage, and legitimate invocation coverage.

## Proposed design

Keep `known_workflow_utilities()` and its `Path -> read_only|mutating` contract unchanged. In `parse_exact_workflow_utility`, consume `_tokenize_safe_shell_command` directly so quote metadata survives through validation of token 2 and all later argv. Preserve the existing launcher, resolved exact script-path lookup, returned `script`/`kind`/plain `argv` shape, and all existing error paths.

Apply one safety predicate before any path expansion, normalization, or exact lookup:

1. Validate raw script token 2 first. Accept it when marked quoted after the existing conservative tokenizer succeeds. If unquoted, require the same explicit literal-atom/path grammar used for argv. Only after this proof may `expanduser()` and `resolve()` run and the canonical result be compared with `known_workflow_utilities()`.
2. Apply the same predicate to every token after the script path. Quoted tokens are the transport for whitespace, parentheses, commas, and other ordinary free text.
3. Accept an unquoted token only when it matches a single explicit literal-atom grammar limited to characters required by existing options, identifiers/enums, hashes/numbers, timestamps, and Windows/POSIX paths (letters/digits plus `_ . / \ : + = ~ -`). Empty unquoted tokens are impossible and must not be introduced.
4. Reject every other unquoted script/argv token with a deterministic unsafe-token error. The exclusion necessarily covers PowerShell parentheses, braces, brackets/static-member syntax, commas/array construction, at-sign subexpressions, quotes, whitespace, wildcards, stop-parsing/comment syntax, and other expression punctuation. Existing global rejection continues to cover `$`, backticks, separators, redirection, control operators, multiline input, and quote escapes.

A quoted non-canonical script spelling may still normalize to an installed utility because quoting has already made it inert to PowerShell; an unquoted expression-bearing alias must be denied before normalization. Exact utility membership and mutability continue to be determined only from the final resolved path.

This is shell-safety validation, not a duplicate implementation of each utility's `argparse` grammar. The utility remains responsible for semantic CLI validation after launch; the guard owns only proving that PowerShell cannot evaluate argv before launch. Because `references_workflow_utility()` already turns any parse failure mentioning a registered utility into a denial, no change to `pre_tool_guard.py` should be needed.

For tests, make the runtime-resolved utility inventory the coverage source. Assert that the expected installed paths, including both conditional product-design utilities, match the inventory used by the negative and positive matrices so a newly registered exact utility cannot silently escape coverage.

## Alternatives considered

- Duplicate each utility's complete positional/option grammar in the hook. Rejected because it creates eight parallel CLI contracts, can drift independently from `argparse`, and is unnecessary to prove pre-launch shell safety.
- Require every argv token, including `--help`, enum values, hashes, and task IDs, to be quoted. Rejected because it breaks established legitimate commands without adding protection beyond a narrow unquoted literal grammar.
- Add another denial branch after the read-only allow in `pre_tool_guard.py`. Rejected because the parser is the shared authorization boundary for both read-only and mutating utilities; validating there closes the class once and preserves the current guard ordering.

## Implementation sequence

1. In `self_test.py`, first extend the loop over `common.known_workflow_utilities()` with two table-driven failing matrices for every utility: unsafe argv appended after the canonical script, and raw unquoted script aliases constructed as `<utility-parent>\<vector>\..\<utility-name>` without resolving the test string. Include `(Get-Date)`, `(Clear-Clipboard)`, a harmless parenthesized sentinel literal, `{Get-Date}`, `@(Get-Date)`, `$(Get-Date)`, `1,2`, `[System.DateTime]::Now`, and parenthesized static-member/call forms wherever the existing tokenizer permits the path-shaped spelling. Assert each generic parse returns `None`. Run the installation self-test and record the expected pre-fix failures for both post-script argv and token-2 normalization aliases.
2. Still tests-first in `self_test.py`, add table-driven valid shell commands covering every registered utility with its ordinary shape: canonical script path quoted and unquoted; `--help`; task IDs/enums; quoted `--repo-root`, `--workflow-dir`, and other path values; Registry root/agents/skills options; and safely quoted request/title free text for the initializer utilities. Assert both canonical script spellings resolve to the same exact path and preserve kind/plain argv. Preserve the existing append-decision positive/negative matrix unchanged.
3. In `common.py`, add one narrowly named/testable helper or compiled pattern for safe unquoted exact-utility shell atoms, switch `parse_exact_workflow_utility` to `_tokenize_safe_shell_command`, validate token 2 before calling `expanduser()`/`resolve()`, then validate every later argv token with the same predicate before returning the existing result object. Do not change `known_workflow_utilities`, `tokenize_safe_shell_command`, `parse_exact_append_decision`, or utility classification.
4. Run the targeted installation self-test. Adjust only the literal character set when an existing legitimate positive proves a required shell-literal character; do not add expression delimiters or weaken the quote requirement to make a test pass.
5. In `full_self_test.py`, extend/rename `assert_utility_spoofs_denied` so it derives or verifies the complete runtime utility set and applies both the full unsafe post-script argv matrix and the raw `<utility-parent>\<vector>\..\<utility-name>` path-alias matrix to every exact utility. Its existing call sites exercise both initial `architecture` and `architecture_rework_review` assignments. For every vector, assert denial at the malformed/unsafe exact-utility boundary, byte-identical `product.py` and `05-decision-log.md` sentinels, and absence of any dedicated static-call sentinel.
6. Expand the E2E positives before workflow activation to authorize one legitimate full-shape command for every read-only and mutating utility as parent/root, with each canonical exact script path tested quoted and unquoted. During both architecture assignments, assert canonical quoted and unquoted read-only shapes still pass and existing legitimate mutating initializer shapes are denied by the unchanged phase/write-policy boundary, not by script/argv safety.
7. Inspect `pre_tool_guard.py:main` after the parser tests pass to confirm unsafe exact utilities reach the existing malformed/non-exact denial before lines that allow read-only or check mutating utilities. Modify it only if an observed failing E2E proves the existing parse-error route is bypassed; otherwise keep it byte-identical.
8. Run the complete validation set, inspect exact task-attributable file hashes/diffs and Git status, and report only changes to `common.py`, `self_test.py`, and `full_self_test.py` unless step 7 produced evidence requiring the minimal guard correction.

## Tests-first strategy

- First failing test: for every path from `known_workflow_utilities()`, both `py -3 "<canonical path>" --help (Get-Date)` and an unquoted raw `<parent>\(Get-Date)\..\<name> --help` alias must return no parsed utility, followed by the complete post-script and path-alias matrices. The current parser accepts both classes, proving the regression before production changes.
- Unit coverage: table-driven generic parser negatives for expression/script/array/subexpression/static-call shapes in argv and raw script-path aliases; quoted equivalents and ordinary quoted punctuation/free text as inert positive argv; canonical script paths in quoted and unquoted forms; canonical option/enum/path/hash/numeric values; exact `py -3`, exact resolved identity, and preserved `kind`/`argv`; unchanged append-decision matrix.
- Integration coverage: the complete installation `self_test.py`, including an assertion that its runtime utility set covers task-intake init/validation, change-delivery init/validation, workflow status, Registry validation, and conditional product-design init/validation.
- End-to-end coverage when justified: use the real `pre_tool_guard.py` in `full_self_test.py` for every utility and both vector locations under initial and rework architect assignments. Assert denial occurs at PreToolUse before read-only/mutating authorization, product and decision-log bytes do not change, static-call sentinel is absent, canonical quoted/unquoted read-only invocations remain allowed, and mutating utilities still follow the existing write-policy denial.
- Edge and failure cases: quoted canonical script paths and quoted parenthesized prose/comma punctuation remain literal; unquoted canonical Windows paths, later Windows/POSIX paths, task IDs, enum values, hashes, integers, and ISO-like timestamps remain literal; unsafe raw path aliases are constructed without test-side normalization; empty quoted values remain shell-safe and are left to utility CLI validation; nested/partial/mismatched quotes and existing expansion/control syntax remain denied.
- Compatibility checks: replay exact-path spoofing, `append_decision.py` shell vectors and structured-argv literal transport, parent/root initializer authorization, actor/provenance checks, initial/rework phase checks, immutable anchors, independent-review routing, and Registry validation.
- Repository-derived commands:
  - `py -3 -m py_compile C:\Users\rapha\.codex\hooks\scripts\common.py C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py C:\Users\rapha\.codex\hooks\installer\self_test.py C:\Users\rapha\.codex\hooks\installer\full_self_test.py`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills`
  - `py -3 C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py --workflow-dir C:\Users\rapha\Documents\claude-forge\.codex\workflows\fix-exact-utility-powershell-argv --registry-root C:\Users\rapha\.codex\workflow-registry`
  - `py -3 C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\validate_handoff.py --workflow-dir C:\Users\rapha\Documents\claude-forge\.codex\workflows\fix-exact-utility-powershell-argv`

## Rollout and rollback

- Rollout is immediate when the installed global hook files are updated; there is no schema, data, Registry, service, or staged deployment. Gate the change on the targeted parser regression, both-phase E2E matrix, full self-tests, and independent review before final integration.
- Record pre-change and post-change hashes for the task-attributable global files because they lack a clean Git baseline. If a legitimate invocation regresses, keep the authorization boundary fail closed and narrow the correction to the literal-atom grammar plus its positive fixture. Do not restore the arbitrary unquoted-argv behavior; revert only unrelated test/helper changes after exact hash/diff attribution if necessary.

## Architecture fitness checks

- Executable invariant: every key returned by `known_workflow_utilities()` participates in the same post-script argv matrix, raw path-alias matrix, and canonical quoted/unquoted positive matrix.
- Authorization invariant: no exact utility reaches resolved-path lookup, read-only allow, or mutating write-policy evaluation when the raw script token or any later argv token is neither safely quoted nor a safe literal atom.
- Normalization invariant: token-2 shell safety is proven before `expanduser()`/`resolve()`; only then may the resolved path determine exact installed identity and mutability.
- Compatibility invariant: canonical quoted and unquoted installed paths, launcher, utility kind, returned plain argv, append-decision contract, and actor/phase/write-policy behavior remain unchanged.

## Data and migration impact

None. No persistent format, workflow artifact, Registry schema, data store, or migration changes.

## Security and privacy impact

This closes the verified PowerShell pre-execution authorization bypass in both expression-shaped argv and expression-bearing script-path aliases by proving the raw token safe before path normalization. It does not broaden permissions, expose data, alter secret handling, or treat the hook as a full sandbox. Residual shell-control risk remains bounded by the existing conservative tokenizer and resolved exact installed-path checks.

## Performance and operational impact

One linear scan/regular-expression check over the already tokenized argv is negligible. Denial diagnostics should remain deterministic and actionable. No service, network, deployment, telemetry, or alerting change is required.

## Documentation impact

None. The requested correction is internal and explicitly excludes Registry, Skill, agent, repository-documentation, and product changes.

## Risks

- An overly narrow atom grammar could reject a legitimate unquoted punctuation value. Mitigation: enumerate representative real command shapes for every utility, require quoting for free text/punctuation, and expand only with characters proven literal under PowerShell.
- A permissive atom grammar could admit another PowerShell expression form. Mitigation: use an allowlist rather than enumerating known attacks, retain all existing tokenizer denials, and independently replay the full expression matrix.
- Path normalization could hide unsafe input if validation is accidentally moved after `expanduser()`/`resolve()`. Mitigation: make raw token-2 validation an explicit ordered invariant and cover every utility with unresolved `vector\..\name` regressions.
- Hard-coded E2E inventory could drift from the installed utility registry. Mitigation: derive it from or assert exact equality with `known_workflow_utilities()` under the test environment.
- Global hook files are outside the repository's clean Git baseline. Mitigation: capture exact hashes, keep the implementation to three expected files, review complete task-attributable diffs, and preserve the initial dirty-state snapshot.
- Editing `pre_tool_guard.py` unnecessarily could disturb authorization ordering. Mitigation: plan no guard edit; require a failing E2E as evidence before any minimal change there.

## Assumptions

- The safety boundary applies to shell-form command strings. Structured argv remains inert transport and is already tested separately for `append_decision.py`.
- Utility CLI semantic validation remains owned by each utility; the global guard needs to prove only exact identity, authorization, and lack of PowerShell evaluation before launch.
- Existing legitimate values containing whitespace or expression punctuation can be safely quoted without changing utility semantics.
- The runtime `known_workflow_utilities()` inventory observed under the installed Registry is the authoritative exact-utility set for this change.

## Blocking questions

None.

## Out of scope

- Per-utility CLI reimplementation, new utilities, Registry/phase/route/status/version changes, hook-framework redesign, PowerShell replacement, or broad command-parser refactoring.
- Changes to `append_decision.py`, workflow artifacts other than this handoff, product/cognition code, Skills, agents, documentation, unrelated configuration, manifests, lockfiles, Git state, or publication.
- Reopening the source workflow's completeness, clarification, research, provenance, alternatives, or independent-review behavior.

## Reviewer checklist

- [ ] AC-001 through AC-007 are represented with observable tests and validation commands.
- [ ] The verified source hashes and `CODE-REVIEW-001` execution path support the root cause.
- [ ] The proposed literal-atom grammar is applied to raw token 2 before path normalization and to all later argv, excluding every PowerShell expression delimiter while preserving proven option/identifier/path/hash/time forms and quoted free text.
- [ ] Every runtime-resolved utility, including conditional product-design utilities, is covered by post-script argv negatives, unresolved path-alias negatives, and canonical quoted/unquoted positives.
- [ ] Initial and rework architect assignments both deny both complete matrices and preserve product/decision-log bytes.
- [ ] Legitimate read-only utilities still pass and mutating utilities retain parent/actor/phase/write-policy behavior.
- [ ] `append_decision.py`, structured argv, exact paths, `py -3`, Registry definitions, workflow contracts, and unrelated dirty files remain unchanged.
- [ ] The rollout/rollback strategy remains fail closed and proportionate to unversioned global hook assets.
