# Implementation Report

## Status

READY_FOR_CODE_REVIEW

## Task

enforce-architect-research-dialogue

## Mode

REVIEW_CORRECTION

## Plan and review inputs

- `00-task.md` — SHA-256 `9424747BA4295B23307889F2E42152616402C28C46A6DA9CE239A9DB8EA72DF6`
- `10-plan.md` — approved SHA-256 `5ECDE36B42C3F3EC6400F0695BD8EC3CB46CE6156E36F5192A8FA1356189B69F`
- `20-plan-review.md` — status `APPROVED`, SHA-256 `5287185148C0050DE809995435B5D804C65D6E7EC00B5299D9E93352995F3828`
- `40-code-review.md` — cycle-2 status `CHANGES_REQUIRED`, SHA-256 `EF7A912E90019F643A23BE4DF44F705A2EAD87688360668ACA94758B6D3D7E5F`.

## Requirement and acceptance-criteria coverage

- AC-001–AC-004 — the agent, Skills, handoff template, validator, Registry, and hooks now enforce a machine-readable completeness matrix, `NOT_STARTED_MATERIAL_GAPS`, precise blocking questions, same-phase wait/re-entry, and no research or recommendation before confirmed parent/user evidence.
- AC-003–AC-004 — hook tests cover initial and rework clarification, blocked assignment, AUTO-RUN stop, exact parent append, immutable prefix/handoff anchors, re-entry, repeated clarification, and research-gate ordering.
- AC-005–AC-007 — ready handoffs require credential-free valid HTTP(S) source URLs, `PRIMARY|OFFICIAL|AUTHORITATIVE`, valid non-future ISO access dates, explicit material dates/semantic versions/justified non-applicability, claims/limitations, CDC-driven AI/RAG/stack relevance, and every approved alternative-comparison axis.
- AC-006 — agent/Skill tests assert conditional agents, RAG, retrieval/reranking, vector-storage, orchestration, and stack coverage; the valid E2E fixture marks one relevant stack decision and excludes irrelevant fashionable technologies.
- AC-008 — the existing complete architecture package remains required and gains completeness, research, relevance, and alternatives sections without weakening bindings, slices, traceability, security, operations, rollout, or rollback.
- AC-009 — `READY_FOR_REVIEW` still targets only `design_review`; the E2E exercises an initial review, `REWORK_ARCHITECTURE`, the rework clarification loop, and a second independent review. The historical/current structural comparison proves no other phase or review transition changed.
- AC-010 — active global agent, both architecture Skill surfaces, project orchestration, task intake, template, validators, Registry, hooks, tests, installed documentation, and the two approved repository docs are synchronized on `1.3.0`; no document references an undeclared development handoff.
- AC-011 — automated fixtures cover incomplete CDC, confirmed-answer re-entry, prefix/handoff tampering, every known-utility spoof under both architecture modes, quoted expansion/control syntax, structured-argv sentinel safety, invalid source types/dates/versions/URLs, documentation drift, missing RAG relevance/alternative axes, complete handoffs, independent routing, and historical-version resolution.
- AC-012 — Registry, intake, installation, full E2E, syntax, handoff, transition, hash, authorization PoC, provenance, documentation, and final Git-status checks passed; no product source/configuration, `config.toml`, Git publication, deployment, or unrelated dirty file was changed.

## Files changed

- `C:\Users\rapha\.codex\workflow-registry\registry.json` — current plus exact-version definition mapping.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design-1.2.0.json` — immutable historical `1.2.0` behavior.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design.json` — current `1.3.0` definition and evidence-gated self-loops on both architecture phases.
- `C:\Users\rapha\.codex\workflow-registry\validate_registry.py` — validates version maps, unique ID/version pairs, current mapping, and safe resume-evidence self-loops.
- `C:\Users\rapha\.codex\workflow-registry\README.md` — exact-version and clarification-loop operator contract.
- `C:\Users\rapha\.codex\hooks\scripts\registry_engine.py` — exact-version resolution, wait anchoring, suffix reconciliation, and assignment gating.
- `C:\Users\rapha\.codex\hooks\scripts\common.py` — parent-visible waiting state, fail-closed quote/control tokenizer, exact installed utility registry, exact command parsers, and removal of every substring allow-list.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py` — parent/root provenance, exact utility and append target/shape/phase/write-policy/actor/type/artifact/hash authorization.
- `C:\Users\rapha\.codex\hooks\scripts\subagent_stop.py` — captures decision-log prefix and blocked-handoff anchors.
- `C:\Users\rapha\.codex\hooks\scripts\stop_gate.py` — reconciles later evidence and pauses pending/invalid clarification, including continuous automation.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — unit/contract coverage for versions, every exact utility, quote/control rejection, docs, immutable prefix, and exact legacy equivalence.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — initial/rework E2E plus utility spoof, shell-expansion sentinel, strict provenance, documentation, negative handoff, and independent-review tests.
- `C:\Users\rapha\.codex\hooks\README.md` — hook security and resume behavior.
- `C:\Users\rapha\.codex\agents\architect_brainstorm.toml` — mandatory completeness, deep research, conditional relevance, comparison, and completion contract.
- `C:\Users\rapha\.codex\skills\architect-brainstorm\SKILL.md` — directly invokable ordered architecture workflow.
- `C:\Users\rapha\.codex\skills\architect-brainstorm\references\architecture-method.md` — clarification-before-research method.
- `C:\Users\rapha\.codex\skills\architect-brainstorm\references\handoff-template.md` — completeness, research, source, relevance, and comparison fields.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` — `1.3.0`, exact parent append command, evidence loop, research, and independent-review contract.
- `C:\Users\rapha\.codex\skills\project-brainstorm\agents\openai.yaml` — synchronized App activation/default prompt.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\architecture-method.md` — managed architecture method.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\pipeline.md` — parent-mediated clarification and rework pipeline.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\workflow-states.md` — both evidence-gated self-loops and unchanged terminal behavior.
- `C:\Users\rapha\.codex\skills\project-brainstorm\references\handoff-contracts.md` — blocked/ready research and exact provenance-format invariants.
- `C:\Users\rapha\.codex\skills\project-brainstorm\assets\templates\20-architecture.md` — machine-readable architecture evidence and strict provenance fields.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\append_decision.py` — fail-closed prefix/handoff verification and byte-preserving append.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\init_brainstorm.py` — new workflows select `1.3.0`.
- `C:\Users\rapha\.codex\skills\project-brainstorm\scripts\validate_handoff.py` — status-specific completeness/research/relevance/alternative validation plus URL/type/date/version provenance checks.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md` — current selection versus exact historical execution.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\references\workflow-registry.md` — exact ID/version resolution contract.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py` — validates the task-selected exact definition version.
- `docs/agents/project-brainstorm.md` — operator-facing `1.3.0` sequence, evidence loop, terminal `30-review.md`, and later explicit DEV intake.
- `docs/agents/project-brainstorm-architect.md` — operator-facing completeness/research/relevance behavior and exact architect/reviewer terminal ownership.

## Implementation decisions

- Kept `1.2.0` and `1.3.0` side by side; current selection exposes only `1.3.0`, while persisted tasks/metadata resolve an exact mapped version and unknown versions fail closed.
- Reused the existing architecture phases, statuses, handoff, decision log, architect role, and independent reviewer. No phase, agent, artifact, human gate, or loop counter was added.
- Stored only technical anchors in hook-owned metadata: phase, source handoff hash, complete decision-log prefix length/hash, and last decision ID.
- Required a fixed-order, non-chained `py -3` invocation. PreToolUse proves parent/root provenance and exact target/contract; the utility independently rechecks the prefix and source before a byte-preserving append.
- Replaced all workflow-utility filename matching with exact resolved installed paths. Read-only utilities are single non-chained invocations; mutating initializers additionally pass parent/root provenance and the active phase/write policy.
- Rejected shell variables, command substitution, backticks, redirection, separators, control operators, multiline values, quote escapes, and mismatched/nested quoting in every quote mode. Structured argv remains the safe transport for arbitrary user text.
- Validated deterministic source provenance formats while leaving substantive source authority and claim fit to independent review.
- Kept deterministic validation structural. Independent design review remains responsible for substantive source authority, recency, claim fit, and architecture quality.

## Plan deviations

None.

## Tests added or updated

- `self_test.py` — version-map schema/current selection, exact active/blocked/closed `1.2.0` resolution in an arbitrary second repository, unknown-version failure, strict command parsing, contract synchronization, prefix tamper rejection, and exact legacy/current structural equivalence.
- `self_test.py` — exact positive parsing for every installed utility, ordinary punctuation round-trip, all-quote-mode rejection for `$()`, backticks, variables, newlines, redirection, separators, control/escape forms, nested/mismatched quotes, unquoted PowerShell expressions/script blocks/arrays/static calls, and exact terminal-document assertions.
- `full_self_test.py` — every utility prefixed/suffixed/aliased/quoted/chained spoof under initial and rework architect assignments, byte-identical decision-log/product sentinels, positive exact invocations, and phase/write-policy denial for mutating initializers.
- `full_self_test.py` — shell-form substitution, parenthesized expression, script-block, array/subexpression, and static-call denial plus structured-argv parenthesized/literal sentinel execution proving no side effect outside the decision log.
- `full_self_test.py` — blocked/ready handoffs and negative/positive provenance fixtures for URL, all three source-type enums, ISO access date, material version/date, relevance, alternatives, and independent re-review.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `py -3 -m py_compile C:\Users\rapha\.codex\hooks\scripts\common.py C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py C:\Users\rapha\.codex\workflow-registry\validate_registry.py C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\validate_handoff.py` | PASS | The changed parser and its directly exercised validators compiled successfully. |
| `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills` | PASS | Registry validation passed; all three workflow IDs registered. |
| `py -3 C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\validate_intake.py --workflow-dir C:\Users\rapha\Documents\claude-forge\.codex\workflows\enforce-architect-research-dialogue --registry-root C:\Users\rapha\.codex\workflow-registry` | PASS | Current DEV intake remained valid after exact-version support. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py` | INVALID INVOCATION | The test harness rejected the incomplete invocation because its six required root arguments were missing; the complete invocation immediately below passed. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | `V8.2.0 installation self-test passed`. |
| `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents` | PASS | Full Registry/DEV/Brainstorm/human-gate/MCP/hook E2E passed, including both new loops and negative fixtures. |
| `Get-FileHash -Algorithm SHA256 00-task.md,10-plan.md,20-plan-review.md` | PASS | Upstream hashes remained exactly `9424747…`, `5ECDE36…`, and `52871851…`. |
| Transition and allow-list inspection plus `git status --short --branch` | PASS | Both blocked self-loops and unchanged `READY_FOR_REVIEW -> design_review` observed; generic append bypass absent; dirty-worktree snapshot preserved. |

## Review findings addressed

- `CODE-REVIEW-001` — Accepted. Removed `is_known_workflow_utility` and every substring allow path. Exact installed scripts use `py -3`, safe tokenization, no chaining, read-only/mutating classification, parent/root provenance where applicable, and active Registry write policy. Initial/rework PoC loops cover every former utility name and preserve decision-log/product bytes.
- `CODE-REVIEW-002` — Accepted. The shared tokenizer preserves quote metadata and requires every shell-form free-text value to be one complete safely quoted argument. Tests cover `$()`, backticks, variables, redirection/control, `(Get-Date)`, parenthesized sentinel calls, script blocks, arrays/subexpressions, static methods, quote/escape failures, and structured-argv parenthesized prose/literal injection without creating a sentinel.
- `CODE-REVIEW-003` — Accepted. `SRC-xxx` now enforces valid credential-free HTTP(S) URLs with hostname, the three declared source types, valid non-future ISO access dates, and explicit ISO date/semantic version/justified non-applicability. Positive and negative fixtures pass.
- `CODE-REVIEW-004` — Accepted. Removed both obsolete `development_handoff` and undeclared `architecture-handoff-v1`, named Registry-owned `20-architecture.md`, and asserted the exact chain `20-architecture.md -> 30-review.md -> STOP -> later explicit DEV intake` in both targeted docs.

## Documentation updated

- Installed Registry and hook READMEs document exact-version selection, fail-closed clarification, exact utility authorization, and no-shell free-text transport.
- Project/App/architecture Skill contracts and both approved repository agent docs describe the same completeness → clarification → deep sourced research → comparison → proposal → terminal independent review → later explicit DEV intake sequence.

## Remaining limitations

- Deterministic validators verify source structure and provenance, not whether a source is substantively authoritative or the recommendation is correct; `review_brainstorm` remains the mandatory independent quality gate.
- Hook interception is a guardrail rather than a security sandbox; enforcement is duplicated in the append utility for the mutation boundary covered by this change.

## Blockers

None.

## Out-of-scope observations

- The repository began and remains heavily dirty with unrelated modified and untracked product/cognition work, including pre-existing `.codex/config.toml` changes. Those files were not edited, reset, cleaned, staged, committed, or published.
