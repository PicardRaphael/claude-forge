# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: project-brainstorm
- Type: FEATURE

## Classification

- Primary type: FEATURE
- Secondary tags: AI/agentic, authorization, immutable-data-contracts, global-Codex-configuration, transactional-installer, backward-compatibility
- Risk level: HIGH
- Risk justification: The change adds globally discoverable agents, modifies a security boundary shared by direct reads and physical search indexes, persists workflow state, and manages user-owned Codex configuration. A wrong design could leak private cognition, authorize stale artifacts, or damage global configuration.

## Objective

Create a Codex-native global pipeline `cdc_brainstorm -> architect_brainstorm -> review_brainstorm`, orchestrated by `$project-brainstorm`, backed by the existing `mcp-forge-cognition` and `cognition-store`, and ending at an immutable `development_handoff` consumable by the existing Codex `change-delivery-workflow`. Do not implement application code or create a competing DEV workflow.

## Confirmed requirements

- Canonical sources under `global-config/codex/`; active agents under `~/.codex/agents/`; active Skills under Codex's documented global `$HOME/.agents/skills/` directory.
- Native invocation is `$project-brainstorm` or `/skills`; do not claim unsupported `/project-brainstorm` alias behavior.
- Reuse the existing DEV Skill and agents unchanged except for the minimal Skill-location compatibility bridge.
- Reuse the historical architect's evidence-first, alternatives, components, data, contracts, security, tests, deployment, and readiness lenses while removing stack-specific coupling.
- Use only the existing cognition MCP/store. Startup profile fixes the principal; tools never accept a principal override.
- Product, architect, reviewer, and curator receive exact role-specific capabilities; the three agents never receive curator access or wildcard project access.
- Human CDC approval, stale-revision rejection, targeted rework, two-rework human gate, neutral review packet, and development handoff are server-enforced.
- All pipeline artifacts are append-only, revisioned, and content-hashed. Forbidden reads return the same not-found response as absent data.
- Installer operations are idempotent, conflict-aware, backed up, transactional, and preserve unmanaged/drifted files.
- Security option A is confirmed: role execution uses a dedicated `CODEX_HOME` containing only project-brainstorm configuration and requires one independent Codex login; native global agent descriptors never process project content directly.
- Preserve unrelated current changes, especially `.codex/config.toml` and untracked repository agents/Skills.

## Current behavior

- Global DEV agents exist at `~/.codex/agents/{architect_feature_bug,lead_developer,reviewer_feature_bug}.toml` and reference `~/.agents/skills/change-delivery-workflow/SKILL.md` through `[[skills.config]]`.
- The only active DEV Skill copy is incorrectly located at `~/.codex/skills/change-delivery-workflow/`; the referenced documented global path is absent.
- `mcp-forge-cognition` has Product, Red Team, and Curator principals, a v1 document/project envelope, per-principal SQLite projections, startup-fixed profiles, project/episode/review operations, and 39 passing baseline tests before this task's partial edits.
- The partial task edits add an architect principal and fields directly to v1 models but do not integrate grants into direct reads/index rebuilds. Current evidence is 35 passing and 4 failing tests; these are task-caused failures, not baseline failures.
- `cognition-store/STORE_VERSION` is `1`; `document-v1.yaml` and `project-v1.yaml` are closed schemas.
- No Codex-native brainstorm agents, global project-brainstorm Skill, strict handoff payload schemas, scoped workflow state, or installer exist.

## Root cause

Not applicable as a product bug. The implementation gap is that the original request targeted Claude Code paths and command semantics, while the confirmed target is Codex. The incomplete first implementation also coupled new grant requirements to legacy `AccessPolicy` calls without providing a central grant resolver for direct reads and physical indexes.

## Critical flow and blast radius

- Entry point: a parent Codex task invokes `$project-brainstorm` or an individual role Skill from any repository; the Skill calls a deterministic launcher into the isolated runtime.
- Execution flow: product creates project/CDC -> curator records human CDC approval -> architect receives exact CDC -> curator approves architecture and publishes neutral packet -> reviewer records closed verdict -> targeted rework or curator creates development handoff -> parent may initialize the existing DEV workflow.
- Upstream callers: Codex parent tasks, the three global custom agent profiles, installer CLI, and existing cognition clients.
- Downstream dependencies: `FileCanonicalStore`, `MutationCoordinator`, per-principal SQLite indexes, MCP tool registration, global Codex agent/Skill discovery, and the existing DEV workflow handoff contract.
- Consumers and data affected: new pipeline-managed v1 cognition documents, derived SQLite indexes, four MCP profiles, global agent/Skill files, managed MCP entries, documentation, and tests.
- Intentionally unaffected areas: forge-brain vault, legacy non-pipeline cognition documents/projects, application repositories, existing DEV agent behavior, Git publishing, deployment, and product implementation.

## Relevant files and symbols

- `mcp-forge-cognition/src/forge_cognition/domain/models.py`: `Principal`, `CognitionDocument`, `Project` — revert incompatible v1 envelope additions; add pipeline enums/value models without changing v1 serialized fields.
- `mcp-forge-cognition/src/forge_cognition/domain/policies.py`: `AccessPolicy` — preserve legacy path policy; delegate pipeline-managed document decisions to a central authorization resolver.
- `mcp-forge-cognition/src/forge_cognition/domain/pipeline.py` (new): `PipelineState`, `ArtifactPointer`, `ProjectGrant`, `ReviewVerdict`, transition rules, strict payload validation, canonical hashing.
- `mcp-forge-cognition/src/forge_cognition/application/authorization.py` (new): `PipelineAuthorization` — one decision path for direct get, project projection, list, index, and verifier.
- `mcp-forge-cognition/src/forge_cognition/application/service.py`: `context_get`, `project_get`, project artifact/review operations, `_get_authorized_document` — add state-machine use cases and central authorization.
- `mcp-forge-cognition/src/forge_cognition/infrastructure/file_store.py`: `FileCanonicalStore` — resolve latest append-only pipeline-state document and artifact series from existing v1 documents.
- `mcp-forge-cognition/src/forge_cognition/infrastructure/lexical_index.py`: `SQLiteLexicalIndex.rebuild` — use the same authorization resolver and atomically replace projections after grant/rework changes.
- `mcp-forge-cognition/src/forge_cognition/infrastructure/transactions.py`: `MutationCoordinator.execute` — retain canonical write + full index rebuild + rollback boundary.
- `mcp-forge-cognition/src/forge_cognition/infrastructure/verification.py`: `StoreVerifier` — verify effective authorized IDs using the central resolver and recognize the architect profile.
- `mcp-forge-cognition/src/forge_cognition/bootstrap.py`: `build_service` — compose state resolver/authorization for services and indexes.
- `mcp-forge-cognition/src/forge_cognition/presentation/mcp/server.py`: `create_mcp`, `register_for` — expose exact role tools.
- `mcp-forge-cognition/profiles/*.yaml`: startup-fixed product/architect/reviewer/curator profiles with no wildcard project access for brainstorm roles.
- `cognition-store/schemas/*-handoff-v1.yaml`, `review-packet-v1.yaml`, `pipeline-state-v1.yaml` (new): strict payload contracts; existing `document-v1.yaml`, `project-v1.yaml`, and `STORE_VERSION` remain immutable.
- `global-config/codex/agents/*.toml` and `global-config/codex/skills/project-brainstorm/` (new): canonical agents/orchestrator/references.
- `global-config/codex/runtime/config.toml` and `scripts/run-project-brainstorm-role.py` (new): isolated `CODEX_HOME` template, runtime capability/auth preflight, role-only MCP enablement, and bounded execution.
- `global-config/codex/skills/change-delivery-workflow/` (new compatibility import): byte-equivalent canonical copy of the existing DEV Skill, installed at its already referenced official global path.
- `global-config/codex/manifest.yaml`, `VERSION`, and `scripts/install-global-project-brainstorm.py` (new): managed installation and MCP reconciliation.
- `mcp-forge-cognition/tests/**`, `tests/test_global_project_brainstorm_installer.py` (new): domain, ACL, state, MCP, neutralization, compatibility, and installer coverage.
- `docs/agents/project-brainstorm-*.md` and related agent/handoff/install docs (new): operation and recovery.

## Proposed design

### Preserve the closed v1 envelope

Do not evolve `document-v1.yaml`, `project-v1.yaml`, or `STORE_VERSION`. Revert the partial additions of `series_id`, grants, pointers, and workflow state from the serialized `CognitionDocument` and `Project` envelopes. New handoffs and state remain ordinary valid v1 `CognitionDocument` records in existing project zones:

- `attributes.pipeline_managed = true`;
- `attributes.artifact_type` identifies CDC, architecture, review packet/verdict, development handoff, or pipeline state;
- `attributes.series_id`, `attributes.payload_schema`, and exact source ID/revision/hash bindings carry version metadata already permitted by the v1 `attributes` object;
- each revision is a new ULID document with `revision + 1` and `supersedes` pointing backward; old files are never modified and `superseded_by` remains unset.

`pipeline-state-v1` is a strict payload schema stored in an append-only `decision` document in the existing `projects/<project>/decisions/` zone. It contains current pointers, active grants, stage, rework count, and curator-recorded human decision. Handoff payload schemas validate document bodies at the service boundary before canonical serialization. This is an additive application-level contract, not a base-store migration. Old v1 fixtures and mixed legacy/pipeline stores parse identically; unknown payload schema versions are rejected. Rollback of code needs no data rewrite because every new record still conforms to the unchanged v1 envelope.

### Central grant-aware authorization and indexing

Introduce `PipelineAuthorization.can_read(principal, document, relative_path)` and `can_read_project(principal, project_id)`:

1. Curator retains full access.
2. Private namespaces always use `AccessPolicy` owner matching and never grants.
3. Non-pipeline documents retain current legacy `AccessPolicy` behavior for compatibility.
4. Pipeline-managed documents require the latest valid pipeline-state document and an active grant matching principal, project, exact document ID or series, and allowed revision/current pointer.
5. Product receives an owner grant when it creates a pipeline project. Architect receives only the curator-approved CDC/current project context. Reviewer receives only the curator-produced neutral packet/evidence allowlist. Rework publishes a new state revision that revokes downstream grants/pointers.

`FileCanonicalStore` resolves the latest valid state by `series_id`, highest revision, backward `supersedes` consistency, and hash verification. Resolution is cached per authorization snapshot/rebuild, not globally across mutations.

`_get_authorized_document`, `project_get`, list/search, `SQLiteLexicalIndex.rebuild`, and `StoreVerifier._indexes` use the same resolver. `MutationCoordinator` already writes canonical files, rebuilds every profile into temporary SQLite files, atomically replaces them, and rolls canonical files/indexes back on failure. Therefore a new/revoked grant changes direct reads and physical search visibility in the same locked mutation. Tests assert exact index ID sets after grant, revoke, rework, and rollback. All denial paths raise `NotFoundError("resource not found")`.

### Server-enforced state machine

Add idempotent service/MCP operations for: pipeline project creation, CDC draft publication, curator human approval, architecture publication, curator architecture approval/review-packet publication, reviewer verdict, curator human rework decision, private episode/candidate lesson, and development-handoff creation.

Allowed reviewer verdicts are exactly `GO_DEV`, `GO_DEV_WITH_CONDITIONS`, `REWORK_CDC`, `REWORK_ARCHITECTURE`, `PARK`, and `KILL`. Verdict and handoff operations require exact current source IDs/revisions/hashes. Rework appends a new state revision and invalidates incompatible downstream grants/pointers. At two consecutive reworks and thereafter, continuation is refused until Curator appends a scoped human decision. Only Curator may publish neutral packets, approve stages, record the human gate, or create the development handoff.

Neutral packets are constructed from typed allowlisted payload fields, not arbitrary headings. Forbidden persuasion/history metadata is rejected; adversarial fixtures cover known phrases and nested metadata. Residual semantic bias within an otherwise allowed factual field is documented.

### Codex package, isolated runtime, and DEV bridge

Security option A is mandatory. The installer creates one independent runtime home at the system-home equivalent of `~/.codex-project-brainstorm/`; it contains a minimal `config.toml`, no plugins/marketplaces, `apps._default.enabled = false`, no hooks, no memories, and only the four project-brainstorm MCP definitions. All MCP profiles are disabled by default. The deterministic launcher sets `CODEX_HOME` only for its child process, enables exactly one role MCP through CLI config overrides, forces read-only sandbox/no approval escalation, supplies the canonical role prompt, and verifies the effective MCP/tool inventory before sending project input. Curator runs only for explicit parent consolidation operations.

The isolated home owns separate authentication by Codex design. The installer never copies, links, displays, or modifies `~/.codex/auth.json`. `--check` reports `LOGIN_REQUIRED` until the user runs the printed one-time login command against the isolated home. No runtime execution is claimed until that check passes.

The three global TOML files are discoverable dispatcher descriptors only: high reasoning, read-only, no MCP profiles, no project content processing, and instructions to return the deterministic individual-role Skill/launcher path to the parent. Secure execution is through `$project-brainstorm`, `$cdc-brainstorm`, `$architect-brainstorm`, or `$review-brainstorm`; a native spawned descriptor must fail closed instead of acting as the role. This preserves individual invocation while preventing inherited global MCP/apps from handling the role workload.

Runtime preflight resolves every `codex` candidate, records the exact executable/version, and executes a capability probe for `CODEX_HOME`, `exec`, config overrides, MCP listing, apps default-disable, and read-only sandbox. The currently first-on-PATH npm CLI `0.42.0` fails this gate. The installer does not upgrade Codex automatically; it prints the official upgrade command and stops until the user approves or performs the upgrade. The inaccessible WindowsApps binary is not accepted as evidence.

Copy the existing `~/.codex/skills/change-delivery-workflow/` byte-for-byte into the canonical package, record its hash, and install it conflict-aware at `~/.agents/skills/change-delivery-workflow/`, which is both Codex's documented global Skill location and the existing DEV agents' configured path. Do not edit the three DEV agents. If the destination already exists with a different unmanaged hash, preflight fails without mutation. The brainstorm package manifest owns only the newly installed copy; uninstall removes it only when its managed hash/state still match.

`development_handoff` contains approved CDC/architecture bindings, ADRs, slices, acceptance criteria, tests, risks, and reviewer conditions. A Skill reference maps one slice into `.codex/workflows/<task-id>/00-task.md`; the parent then explicitly invokes `$change-delivery-workflow`. Brainstorming itself never spawns DEV agents.

## Alternatives considered

- **Base document/project schema v2 plus store migration:** rejected as unnecessary. Existing v1 `attributes` and existing project zones can represent typed pipeline payloads without changing the closed envelope, so migration risk buys no capability.
- **Mutable grants in `project.yaml`:** rejected because it changes project-v1 and makes rollback/revision history harder. Append-only pipeline-state documents preserve auditability.
- **Authorization only at MCP tool registration:** rejected because direct-ID reads, indexes, verifier, and future adapters could bypass it.
- **Edit the three existing DEV agent TOMLs to point into `~/.codex/skills`:** rejected because `$HOME/.agents/skills` is the documented global Skill path and the agents already reference it. Installing one managed canonical copy is smaller and cross-task compatible.

## Implementation sequence

1. Revert only the incomplete task additions to v1 envelope fields/policy behavior, preserving the architect principal; add regression assertions restoring the 39-test baseline.
2. Add failing domain tests and `domain/pipeline.py` for closed stages/verdicts, strict payload schemas, append-only pointers/state, canonical hashes, stale input rejection, and v1 envelope compatibility.
3. Add `FileCanonicalStore` pipeline-state/series resolution and centralized `PipelineAuthorization`; write direct-ID/project/all-pairs grant/revoke/private/non-disclosure tests first.
4. Inject the resolver into `SQLiteLexicalIndex`, `CognitionService`, and `StoreVerifier`; add exact physical-index tests for grant, revoke, stale revision, rework, rollback, and legacy documents.
5. Add state-machine service methods and strict schema files; test human CDC approval, architecture gate, all verdicts, targeted rework, two-rework human gate, conditional GO, stale review, and development handoff.
6. Register exact MCP tools per startup-fixed principal, add architect/reviewer profile directories/indexes, and test tool inventory plus absence of principal override/curator tools.
7. Create canonical Codex dispatcher agents, the four secure orchestration/individual Skills, isolated runtime template/launcher, and the byte-equivalent DEV Skill compatibility import. Validate TOML/frontmatter, fail-closed descriptors, and effective isolated role boundaries.
8. Implement manifest and transactional installer with Codex binary/capability/auth preflight, journal, backups, exact isolated MCP definitions using absolute paths, rollback, masking detection, and safe uninstall; cover failure injection. Do not mutate the user's main `.codex/config.toml`.
9. Add documentation and a development-handoff-to-`00-task.md` example without invoking DEV.
10. Run full regression/security/schema/installer validation, install globally, verify hashes, then run fresh Codex checks from two clean repositories plus one masking fixture and a bounded E2E to development handoff.
11. Produce `30-implementation-report.md`, run independent CODE_REVIEW, fix all blocking/important findings, rerun validation, and write final evidence.

## Tests-first strategy

- First failing test: restore existing reviewer packet access through the legacy path while a new pipeline-managed packet remains denied until an exact reviewer grant exists.
- Unit coverage: pipeline payload schemas, enums/transitions, canonical hashing, append-only state/series, stale pointers, human gate.
- Integration coverage: product -> approval -> architecture -> neutral review -> every verdict/rework -> development handoff; atomic index rebuild and rollback.
- End-to-end coverage when justified: fresh isolated Codex processes from two clean temporary Git repositories, exact single-role tool inventories, dispatcher fail-closed behavior, and a complete fixture ending at `development_handoff`.
- Edge and failure cases: direct forbidden ID, empty search, cross-project grant, revoked/stale revision, unknown payload schema, malformed neutral packet, local masking, config collision, partial install failure, drifted uninstall.
- Compatibility checks: all original 39 tests, unchanged v1 schema fixtures, mixed legacy/pipeline documents, existing DEV agent TOMLs, byte-equivalent DEV Skill, and no application-repository writes.
- Repository-derived commands: `uv run --python 3.11 --extra dev python -m pytest -q` from `mcp-forge-cognition`; `uv run --python 3.11 --extra dev ruff check .`; `py .../validate_handoff.py`; installer `--check`; `codex --version`; bounded `codex exec` runtime probes.

## Rollout and rollback

1. Run all tests and installer `--check` before external writes.
2. Back up each managed destination and any pre-existing isolated-runtime files; write a journal before mutation. The main Codex config is read-only throughout.
3. Copy canonical files and isolated configuration with absolute paths, require the one-time isolated login, validate fresh processes, then mark state committed.
4. On any install/update failure, restore file backups, remove only newly created managed files, and rerun `--check`.
5. Code downgrade is fail-closed: first disable/remove the three dispatcher agents, role Skills, launcher, and all non-Curator isolated profiles; refuse to start old Product/Red Team code against a store containing `pipeline_managed` artifacts. A tested compatibility guard emits `pipeline_runtime_too_old` before serving. New records are never exposed through legacy policy.
6. Uninstall removes only destinations recorded as package-created and still matching the managed hash. Drifted/unmanaged content is preserved and reported.

## Architecture fitness checks

- Existing cognition store remains the sole canonical operational store.
- Base document/project v1 envelopes and legacy non-pipeline behavior remain compatible.
- One authorization decision function governs direct read, project projection, search index, and verifier.
- Role processes run in an isolated `CODEX_HOME`, are read-only outside scoped MCP mutations, have apps/plugins/hooks/memories disabled, and expose exactly one role MCP; dispatcher descriptors process no project content.
- The new architecture agent is project-level; the existing DEV architect remains bounded-change planning.
- No new framework, database, embedding store, graph, or product implementation is introduced.

## Data and migration impact

No base-store migration. `STORE_VERSION`, `document-v1.yaml`, and `project-v1.yaml` remain unchanged. New strict payload schemas and append-only v1 documents are additive. Deployment tests old v1-only stores, mixed stores, unknown payload versions, interrupted mutations, and rollback. Indexes remain disposable and are rebuilt from canonical files.

## Security and privacy impact

High impact. Controls include startup-fixed principal, no principal tool argument, deny-by-default production profiles, exact project/artifact/revision grants, private namespace ownership, identical not-found denials, curator-only gates, server-side neutralization, exact tool inventories, and atomic index revocation. Residual semantic bias in allowed factual text is documented and cannot be fully eliminated mechanically.

## Performance and operational impact

Full index rebuild already occurs after every mutation. Grant-aware state resolution adds document scanning; cache the latest state once per rebuild/operation snapshot to avoid repeated scans. The store is intentionally small and lexical; add a measured regression threshold rather than a new index backend. Isolated MCP profiles use absolute paths and bounded startup/tool timeouts. Process startup adds latency; record it in runtime evidence.

## Documentation impact

Add pipeline overview, three agent guides, handoff contracts, memory/ACL rules, global install/update/uninstall/recovery, native Codex invocation, local masking, and the bridge into `change-delivery-workflow`. Explicitly state that `/project-brainstorm` is not a documented native alias.

## Risks

- Resolver/index divergence could leak or hide data; mitigate with one injected authorization function and exact physical-ID assertions.
- Append-only latest-state selection could accept a fork; reject duplicate revisions, broken `supersedes`, hash mismatch, and unknown schemas.
- Isolated runtime config mutation could damage that managed environment; never mutate the main Codex config and manage isolated files with backups, journaling, comparison, and rollback.
- Isolated Codex authentication is independent and cannot be copied safely; require one explicit login and treat missing or invalid auth as a release blocker.
- Downgrading the server could bypass pipeline grants; disable role entry points first and enforce a store compatibility guard before legacy startup.
- Importing the existing DEV Skill could create two divergent copies; canonicalize the current bytes, hash both source/destination, fail on unmanaged conflict, and document the official location.
- Codex runtime behavior is version-dependent; fresh-process tests are a release gate and unsupported aliases are not claimed.

## Assumptions

- A modern Codex CLI supporting global custom agents, global Skills, `CODEX_HOME`, `exec`, MCP configuration, apps default-disable, and read-only sandbox can be installed by the user; capability probes, not a guessed version string, are authoritative.
- The current `~/.codex/skills/change-delivery-workflow` is the intended existing DEV Skill source; it will be compared byte-for-byte before canonical import.
- Existing partial edits in `models.py` and `policies.py` belong to this interrupted task and may be corrected; unrelated dirty files remain untouched.

## Blocking questions

None. The user confirmed Codex as the target and authorized autonomous execution.

## Out of scope

- Exact `/project-brainstorm` alias emulation through deprecated custom prompts.
- Claude Code global agents/Skills.
- Replacing or redesigning the existing DEV workflow.
- Migrating forge-brain, changing application repositories, implementing a brainstormed product, publishing Git changes, deployment, release, embeddings, or alternate cognition backends.

## Reviewer checklist

- [ ] Requirements and acceptance criteria are represented.
- [ ] Root cause or expected behavior is supported by evidence.
- [ ] Scope is minimal and complete.
- [ ] Tests-first strategy is sufficient.
- [ ] Compatibility, security, data, and rollout risks are proportionate.
