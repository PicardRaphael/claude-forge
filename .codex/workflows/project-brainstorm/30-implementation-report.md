# Implementation Report

## Status

BLOCKED

## Task

project-brainstorm

## Mode

REVIEW_CORRECTION

## Plan and review inputs

- `.codex/workflows/project-brainstorm/00-task.md`
- `.codex/workflows/project-brainstorm/10-plan.md`
- `.codex/workflows/project-brainstorm/20-plan-review.md` — `APPROVED`
- `.codex/workflows/project-brainstorm/40-code-review.md` — `CHANGES_REQUIRED`, all five findings corrected.

## Requirement and acceptance-criteria coverage

- AC-001 — Three canonical fail-closed TOML descriptors are under
  `global-config/codex/agents/`, installed under `~/.codex/agents/`, parse in
  `tests/test_global_project_brainstorm_package.py`, and match manifest hashes.
- AC-002 — `$project-brainstorm`, `$cdc-brainstorm`, `$architect-brainstorm`, and
  `$review-brainstorm` are canonical/installed under the documented global Skill
  path. The orchestrator stops at the DEV bridge and documents that
  `/project-brainstorm` is not a native alias.
- AC-003/AC-003A — The isolated runtime renders four disabled-by-default absolute
  MCP definitions, apps/memories disabled, read-only sandbox and no-approval
  policy. The main `~/.codex/config.toml` SHA-256 remained
  `4E5D21B83D0620ADB2DD426216C21DECD1BEF0C204F62D16CE8BA4203270B7AA`
  before/after install and update. Runtime role execution remains correctly
  blocked by independent login; see the blocker section below.
- AC-004 — `PipelineAuthorization` governs direct reads, project projection,
  physical indexes and verification. All Product/Architect/Reviewer private
  namespace pairs, exact grants, revocation, direct-ID non-disclosure and index
  removal are tested.
- AC-005 — Five strict handoff schemas plus strict append-only pipeline state are
  implemented without changing `STORE_VERSION`, `document-v1.yaml`, or
  `project-v1.yaml`. Duplicate/broken series, canonical hashes and stale pointers
  are rejected.
- AC-006 — Human CDC approval, all six closed verdicts, targeted architecture
  rework, stale packet hashes, two-rework human gate and conditional GO to an
  immutable development handoff are server-enforced and tested.
- AC-007 — Manifest hashes, unmanaged collisions, idempotent install/update,
  backups/journal, compensation, drift-preserving uninstall, main-config
  immutability and local masking are tested. The corrected real install manages
  30 copied files plus five generated isolated-runtime files with zero hash mismatch.
- AC-008 — `development-handoff-v1` carries bound inputs, ADRs, slices,
  acceptance criteria, tests, risks and reviewer conditions. The Skill reference
  maps one slice into `00-task.md` before an explicit `$change-delivery-workflow`
  invocation and never invokes DEV agents.
- AC-009 — Installer visibility checks passed from two clean temporary Git
  repositories and correctly reported a third local masking fixture. Fresh role
  execution/E2E was not run because preflight stopped before project input on
  `LOGIN_REQUIRED`.
- AC-009A — Managed uninstall orders entry points first; the server startup guard
  emits `pipeline_runtime_too_old` for pipeline records requiring a newer runtime.
- AC-010 — Unit, integration, ACL, neutralization, state, rollback, installer,
  package and lint checks pass: 65 cognition tests and 29 package/runtime tests.
  The first independent CODE_REVIEW findings were corrected and await re-review.

## Files changed

- `mcp-forge-cognition/src/forge_cognition/domain/models.py` — adds only the
  Architect principal; v1 serialized envelopes remain unchanged.
- `mcp-forge-cognition/src/forge_cognition/domain/pipeline.py` — strict payloads,
  state, grants, pointers, verdicts and canonical hashing.
- `mcp-forge-cognition/src/forge_cognition/application/authorization.py` — one
  pipeline/legacy/private read decision path.
- `mcp-forge-cognition/src/forge_cognition/application/service.py` — append-only
  project-brainstorm state machine and exact stale/human gates.
- `mcp-forge-cognition/src/forge_cognition/{bootstrap.py,infrastructure/file_store.py,infrastructure/lexical_index.py,infrastructure/verification.py,infrastructure/runtime_compat.py,presentation/mcp/server.py}`
  — composition, series resolution, grant-aware indexes/verifier, downgrade guard
  and role MCP tools.
- `mcp-forge-cognition/profiles/{forge-product,architect-brainstorm,red-team,curator}.yaml`
  — startup identities; brainstorm agent profiles have no wildcard project grant
  (`curator.yaml` is unchanged).
- `mcp-forge-cognition/{README.md,integrations/README.md,mcp.example.json}` and
  `cognition-store/README.md` — topology/security/operator documentation.
- `cognition-store/schemas/{cdc-handoff,architecture-handoff,review-packet,review-verdict,development-handoff,pipeline-state}-v1.yaml`
  — additive closed payload contracts; base schemas unchanged.
- `cognition-store/{inbox,private}/architect-brainstorm/**/.gitkeep` — canonical
  isolated Architect inbox/private zones.
- `mcp-forge-cognition/tests/{conftest.py,unit/test_project_brainstorm_domain.py,security/test_acl_and_paths.py,security/test_pipeline_authorization.py,integration/test_project_brainstorm_pipeline.py,integration/test_neutralization_and_index.py}`
  — domain, state, ACL, MCP, rollback and regression coverage.
- `global-config/codex/agents/*.toml`, `global-config/codex/skills/{project-brainstorm,cdc-brainstorm,architect-brainstorm,review-brainstorm}/**`,
  `global-config/codex/runtime/**`, `global-config/codex/{VERSION,manifest.yaml}`
  — canonical global Codex package.
- `global-config/codex/skills/change-delivery-workflow/**` — byte-equivalent
  canonical import of the current global DEV Skill, without changing DEV agents.
- `scripts/{run-project-brainstorm-role.py,install-global-project-brainstorm.py,generate-project-brainstorm-manifest.py}`
  — isolated launcher, transactional installer and deterministic manifest build.
- `tests/{test_project_brainstorm_runtime.py,test_global_project_brainstorm_installer.py,test_global_project_brainstorm_package.py}`
  — package/runtime/installer validation.
- `docs/agents/project-brainstorm*.md` — overview, three roles, handoffs, ACL,
  installation/recovery and historical Architect reuse matrix.

The pre-existing/user-owned `.codex/config.toml`, repository `.agents/skills/**`,
repository `.codex/agents/**`, and hooks were not edited or reverted by this task.

## Implementation decisions

- Pipeline metadata remains inside ordinary v1 cognition document `attributes`
  and strict bodies. State is an append-only decision-document series; no store
  migration or base-envelope field was introduced.
- Pipeline authorization augments legacy access only for pipeline-managed/exactly
  granted documents; private namespaces always retain owner-only path policy.
- Curator constructs review packets from typed allowlisted fields. Mechanical
  structural neutrality is enforced; semantic neutrality is explicitly not
  claimed.
- Native global agents are discovery-only descriptors. Only the independently
  authenticated isolated launcher is allowed to process project content.
- The current DEV Skill was copied byte-for-byte to its documented global path;
  the three existing DEV agent TOMLs were not modified.

## Plan deviations

None in repository implementation. Real fresh-process role execution and the
bounded runtime E2E stopped at the plan-mandated independent authentication gate;
no login, credential copy, CLI upgrade, or project input was attempted.

## Tests added or updated

- `test_project_brainstorm_domain.py` — unchanged v1 envelopes, strict schemas,
  closed verdicts, grant/state validation and canonical payload hashes.
- `test_pipeline_authorization.py` and `test_acl_and_paths.py` — legacy
  compatibility, exact/revoked grants, all-pairs private ACL, index non-disclosure,
  MCP role inventories and downgrade guard.
- `test_project_brainstorm_pipeline.py` — CDC approval gate, architecture/review,
  six verdicts, stale hash, two-rework human gate, append-only revisions,
  development handoff and canonical/index rollback.
- Root package tests — fail-closed descriptors, byte-equivalent DEV Skill,
  manifest/source hashes, launcher preflight/inventory, installer collisions,
  idempotence, drift, masking and failure compensation.

## Validation executed

| Command | Result | Evidence |
|---|---|---|
| `uv run --python 3.11 --extra dev python -m pytest -q` in `mcp-forge-cognition` | PASS | 65 passed in 49.82s |
| `uv run --python 3.11 --extra dev ruff check .` in `mcp-forge-cognition` | PASS | All checks passed |
| `uv run --project mcp-forge-cognition --python 3.11 --extra dev python -m pytest -q tests` | PASS | 29 passed in 1.58s |
| `uv run --project mcp-forge-cognition --python 3.11 --extra dev ruff check scripts/... tests` | PASS | All checks passed |
| `py scripts/install-global-project-brainstorm.py --update` after review corrections | PASS | 35 managed/generated files; recoverable transaction committed |
| Main config SHA-256 comparison around install/update | PASS | Hash byte-identical before/after |
| Manifest-to-installed SHA-256 comparison | PASS | 30 copied files, 0 mismatches; five runtime files generated and state-tracked |
| `py scripts/install-global-project-brainstorm.py --check` | PASS | `READY_FOR_RUNTIME_PREFLIGHT`, no missing files or local masks |
| Installer `--check` from two clean temp Git repos | PASS | Both `READY_FOR_RUNTIME_PREFLIGHT` |
| Installer `--check` from local masking fixture | PASS | `LOCAL_MASKING` with exact colliding agent path |
| Installed launcher `--check` | BLOCKED (expected external gate) | npm candidate `LOGIN_REQUIRED`; WindowsApps candidates `CLI_INCOMPATIBLE`; no project input sent |
| `git diff --check` | PASS | No whitespace errors |
| Base v1 schema/store diff inspection | PASS | No diff for `STORE_VERSION`, `document-v1.yaml`, or `project-v1.yaml` |

## Review findings addressed

- `CODE-REVIEW-001` — exact per-role `enabled_tools`, strict managed-config
  hash/capability checks, effective inventory, and server handshake now run before input.
- `CODE-REVIEW-002` — prior ownership state and bytes recover after update failure;
  journals include unique backups and support interrupted-transaction replay.
- `CODE-REVIEW-003` — a managed version/hash/tool wrapper survives source downgrade;
  four pre-feature server fixtures stop before startup, and entrypoints uninstall first.
- `CODE-REVIEW-004` — real deny-by-default profiles preserve legacy non-pipeline
  Product/Reviewer flow through centralized authorization without widening pipeline grants.
- `CODE-REVIEW-005` — state-only transitions return the newly appended state binding,
  verified against `latest_pipeline_state()`.

## Documentation updated

- `docs/agents/project-brainstorm*.md` documents operation, roles, handoffs,
  memory/ACL, installation/recovery, runtime isolation, native invocation and DEV bridge.
- Cognition/store READMEs and MCP example document the Architect principal,
  isolated runtime and structural-neutralization residual risk.

## Remaining limitations

- Structural allowlisting cannot prove semantic neutrality inside an allowed
  factual string; this is documented and retained as residual review risk.
- The installer visibility fixture directory under the system temp root could not
  be removed because the shell safety policy rejected recursive cleanup; it
  contains only three empty temporary Git repositories and one empty masking file.

## Blockers

- `RUNTIME-LOGIN-001`: the isolated `~/.codex-project-brainstorm/` home has no
  independent Codex authentication. The installed launcher returns
  `LOGIN_REQUIRED` for `C:\Users\rapha\AppData\Roaming\npm\codex.cmd` and rejects
  the other discovered candidates. Per the approved Option A contract, a user
  must perform the one-time login against this isolated `CODEX_HOME`; only then
  can the exact effective tool inventory, two fresh child processes and bounded
  idea-to-`development_handoff` runtime E2E be executed. Authentication was not
  copied, displayed, linked or initiated by this implementation.

## Out-of-scope observations

- The first-on-PATH CLI reports `codex-cli 0.42.0`. Behavioral probes reached the
  independent-login gate; the installer did not upgrade it. After login, the
  complete capability/inventory probe remains authoritative.
