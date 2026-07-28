# Task

## ID

enforce-architect-research-dialogue

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

FEATURE

## Initial risk

HIGH

## Title

Enforce clarification and evidence-led research in `architect_brainstorm`

## User request

est-ce que tu peux faire à ce moment-là des modifications en fait si tu veux, une fois qu'il a le CDC, il me pose des questions s'il comprend pas des choses. Une fois qu'il a tout, il fait des recherches sur internet sur comment les gens, les meilleures pratiques pour répondre au CDC. Ensuite, il me fait une proposition, tiens, faudrait utiliser ça, ça, ça, l'architecture faudrait que ça soit ça, ça, ça. Et en fait, vraiment par contre, je veux qu'il regarde ce que les meilleurs font. Et donc en fait, il lit le CDC, il comprend pas, il me pose des questions. Une fois qu'il a toutes les informations, il fait des recherches sur internet, et avec tout ça, il me fait des propositions. En gros, je veux vraiment que ça se passe comme ça, de A à Z.

## Expected outcome

The active global `architect_brainstorm` agent and `architect-brainstorm` Skill
follow an explicit post-approval sequence: verify and understand the approved
CDC; surface material gaps as precise questions for a parent-mediated dialogue
with the user until the required information is confirmed; only then perform
deep, current, cited Internet research into relevant best practices and
state-of-the-art approaches; compare credible alternatives; and produce a
complete, evidence-backed `20-architecture.md`. When agents, RAG, or stack
choices are relevant to the CDC, the research and comparison cover them
explicitly. The resulting architecture remains subject to the existing
independent design review and never starts product implementation.

## Constraints

- Preserve the exact approved-CDC and SHA-256 approval gate before architecture work.
- Preserve Registry-driven phase ownership, declared artifacts, statuses, transitions, and human gates; do not simulate user approval or invent workflow entities.
- Keep user interaction parent-mediated: the architecture agent identifies and returns precise questions, while the parent owns user communication and any append-only decision-log update.
- Preserve the architecture role's write boundary: it may write only its assigned `20-architecture.md` handoff and must not edit the CDC, approval, decision log, review, product files, or Git state.
- Require current primary, official, or otherwise authoritative sources for material external claims, with dated or version-specific evidence when volatility matters.
- Research agents, RAG, vector stores, orchestration, and stack options only when CDC drivers make them relevant; do not force a fashionable technology or architecture style.
- Preserve the independent reviewer boundary: the architect must not approve or review its own design.
- Implement the smallest coherent global agent/Skill and orchestration-contract correction, including synchronized tests or documentation only where needed for consistency.
- Preserve all unrelated modified and untracked files already present in the dirty worktree.
- Do not modify product source code, product tests, product schemas, migrations, manifests, lockfiles, or production configuration.
- Do not create a commit, push, pull request, merge, deployment, release, or destructive cleanup.

## Known context

- The installed architecture agent currently refuses to design from an incomplete CDC and emits `BLOCKED_NEEDS_INPUT`, but it does not define a complete parent-mediated clarification dialogue before research.
- The installed architecture Skill already requires significant-alternative comparison and a complete architecture package, while its current core sequence does not make deep Internet research after clarification an explicit mandatory stage.
- The installed product-design definition is enabled and `READY`; its architecture phase writes `20-architecture.md`, and its next successful phase is an independent design review.
- The current architecture phase treats `BLOCKED_NEEDS_INPUT` as terminal, so the plan must verify how questions, confirmed answers, and safe re-entry work without inventing a status, transition, or artifact.
- The repository contains extensive pre-existing modified and untracked files unrelated to this request.
- This is a global tooling-behavior change, not implementation of a completed product-design handoff.

## Source workflow bindings

None.

## Acceptance criteria

- AC-001: Given an exactly approved CDC, the architecture role first produces an explicit completeness assessment against material scope, scenarios, business rules, data, integrations, security, operations, acceptance criteria, and architecture drivers before selecting technologies or proposing a target architecture.
- AC-002: If the completeness assessment finds a material gap, the role returns precise, decision-relevant questions for the parent to relay to the user, does not mark the architecture `READY_FOR_REVIEW`, and does not silently convert the gap into an assumption or product decision.
- AC-003: Automated or deterministic workflow coverage proves that confirmed parent/user answers can be supplied back to the architecture role through declared inputs, that the role consumes them on re-entry, and that clarification repeats until no material blocker remains or the role reports an explicit unresolved blocker.
- AC-004: Deterministic sequence coverage proves that deep Internet research does not begin while material clarification gaps remain and does begin after the approved CDC plus confirmed answers satisfy the completeness gate.
- AC-005: For every structurally significant recommendation that depends on external state or technical practice, `20-architecture.md` contains current cited evidence from primary, official, or authoritative Internet sources, records source dates or versions when material, and clearly distinguishes evidence, inference, assumptions, and open questions.
- AC-006: When the CDC materially involves agents, RAG, retrieval/reranking, vector storage, orchestration, or stack selection, the research explicitly covers relevant current best practices, failure modes, security concerns, evaluation or observability needs, operational cost, and state-of-the-art alternatives; when these concerns are irrelevant, the handoff does not introduce them speculatively.
- AC-007: Each significant architecture decision compares credible alternatives on requirement fit, delivery and cognitive complexity, failure modes, security and data consequences, operational burden, cost, compatibility or migration, reversibility, and reconsideration triggers, and records why the recommended option is preferred.
- AC-008: A ready architecture handoff remains complete against the installed architecture template: approved CDC binding, AS-IS evidence when applicable, TO-BE components and ownership, domain/data/contracts/flows, security, reliability, observability, performance, cost, tests, deployment, rollout/rollback, ADRs, reversible slices, guardrails, risks, and requirement-to-design traceability are present or explicitly justified as not applicable.
- AC-009: The independent `review_brainstorm` design-review phase remains the only next successful reviewer of `20-architecture.md`; tests or validators reject self-approval, review bypass, product implementation, and any source or design change that is not followed by the Registry-declared re-review path.
- AC-010: The active installed global agent, Skill, relevant parent-orchestration contract, templates, validators, tests, and operator documentation describe the same clarification-then-research-then-proposal sequence without inventing an undeclared phase, agent, artifact, status, transition, or loop counter.
- AC-011: Targeted automated coverage includes at least an incomplete-CDC clarification path, confirmed-answer re-entry, research gating, source/citation requirements, relevant agents-or-RAG-or-stack research, irrelevant-technology exclusion, alternative comparison, complete-handoff validation, and independent-review routing.
- AC-012: Native validation and final diff review show that active global behavior is updated, no product code or product configuration was changed, no unrelated dirty-worktree change was overwritten, and no Git publication or deployment occurred.

## Investigation targets

- `C:\Users\rapha\.codex\agents\architect_brainstorm.toml`, including its required inputs, evidence rules, blocked behavior, write policy, completion response, and Skill binding.
- `C:\Users\rapha\.codex\skills\architect-brainstorm\SKILL.md` and the architecture method, stack/archetype, reverse-architecture, data/contracts, guardian, and handoff-template references relevant to clarification, research, alternatives, and completeness.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` and its parent orchestration, decision-log, workflow-state, research, validation, and architecture-phase contracts.
- The installed `brainstorm-product-design` Registry definition, especially the architecture, design-review, architecture-rework, declared-input, status, transition, and human-gate contracts.
- The canonical source or installation/synchronization mechanism for the active global agent and Skills, plus any repository documentation and tests that must remain aligned with the installed copies.
- Available read-only web/research tooling and permission boundaries for the architecture role, including how source provenance, dates, versions, and citations are represented and validated.
- Existing validators and test fixtures for `20-architecture.md`, parent/agent question handoff, decision-log evidence, phase re-entry, independent review, and no-product-code enforcement.
- Repository-native commands for targeted contract tests, workflow/Registry validation, Skill validation, and final diff review.

## Material unknowns

- PLAN_VALIDATION: Determine the Registry-compatible parent/agent dialogue mechanism that can relay architect questions and confirmed user answers without giving the architect ownership of user approval or the append-only decision log.
- PLAN_VALIDATION: Determine whether the existing terminal `BLOCKED_NEEDS_INPUT` behavior can support safe architecture re-entry or whether a Registry, Skill, or parent-orchestration contract must change; do not invent statuses, transitions, phases, counters, or artifacts.
- PLAN_VALIDATION: Locate the canonical source of truth and synchronization path for the installed global agent and Skills so the correction is durable rather than a one-copy patch.
- PLAN_VALIDATION: Define a proportional completeness gate that blocks on material product, data, security, contract, compatibility, infrastructure, or irreversible-cost gaps without turning every lower-risk uncertainty into a user interruption.
- IMPLEMENTATION_VALIDATION: Verify which read-only Internet tools are actually available to the architecture role and how to test research ordering and citation quality deterministically without relying on a flaky live-network assertion.
- IMPLEMENTATION_VALIDATION: Define evidence-based relevance triggers for agents, RAG, retrieval/reranking, vector storage, orchestration, and stack research so required coverage is neither skipped nor imposed speculatively.

## Delegation directive

Execute the enabled managed `FULL` route sequentially and follow only these
Registry-declared statuses and transitions:

1. `architecture`: spawn `architect_feature_bug` in `ARCHITECTURE` mode to write only `10-plan.md`. `READY_FOR_PLAN_REVIEW` advances to `plan_review`; `BLOCKED_NEEDS_INPUT` terminates as `BLOCKED`.
2. `plan_review`: spawn `reviewer_feature_bug` in `PLAN_REVIEW` mode to write only `20-plan-review.md`. `APPROVED` advances to `implementation`; `APPROVED_WITH_REQUIRED_CHANGES` advances to `plan_correction` using `plan_correction_cycles`; `REJECTED` terminates as `BLOCKED`.
3. `plan_correction`: spawn `architect_feature_bug` in `PLAN_CORRECTION` mode to update only `10-plan.md`. `READY_FOR_PLAN_REVIEW` returns to `plan_review`; `BLOCKED_NEEDS_INPUT` terminates as `BLOCKED`.
4. `implementation`: spawn `lead_developer` in `INITIAL_IMPLEMENTATION` mode to implement the approved change and write `30-implementation-report.md`. `READY_FOR_CODE_REVIEW` advances to `code_review`; `BLOCKED` terminates as `BLOCKED`.
5. `code_review`: spawn `reviewer_feature_bug` in `CODE_REVIEW` mode to write only `40-code-review.md`. `APPROVED` advances to `final_report`; `CHANGES_REQUIRED` advances to `review_correction` using `code_correction_cycles`; `BLOCKED` terminates as `BLOCKED`.
6. `review_correction`: spawn `lead_developer` in `REVIEW_CORRECTION` mode to correct the implementation and update `30-implementation-report.md`. `READY_FOR_CODE_REVIEW` returns to `code_review`; `BLOCKED` terminates as `BLOCKED`.
7. `final_report`: the parent runs `FINAL_INTEGRATION` and writes only `50-final-report.md`. `READY_FOR_HUMAN_REVIEW` terminates as `COMPLETE`; `INCOMPLETE` or `BLOCKED` terminates as `BLOCKED`.

Do not run phases in parallel. Validate each assigned handoff before following
its Registry-declared transition.

## Human gates

None.

## Loop budget

- plan_correction_cycles: 2
- code_correction_cycles: 2
- repeated_finding_threshold: 2
- automatic_continuation: YES

## Open questions

None material before the architecture phase. Resolve the recorded
plan-validation and implementation-validation unknowns from current installed
assets, Registry contracts, and tests without expanding product behavior.

## Out of scope

- Designing an architecture for a real product or running a real product-discovery workflow from a CDC.
- Modifying a real product CDC, approval, architecture, review, decision log, source code, tests, schemas, migrations, manifests, lockfiles, or production configuration.
- Implementing product features, application boilerplate, infrastructure, deployment, or migrations proposed by any architecture handoff.
- Making agents, RAG, vector databases, multi-agent orchestration, microservices, or any particular stack mandatory when the CDC does not justify them.
- Removing the explicit CDC approval gate, weakening parent-owned user decisions, allowing architect self-review, or bypassing independent design review.
- Unrelated cleanup or refactoring of global Codex assets, repository files, historical workflows, caches, sessions, logs, or current dirty-worktree changes.
- Git commit, push, pull request, merge, branch management, deployment, release, publication, or destructive cleanup.
