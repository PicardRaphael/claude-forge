# Code Review

## Status

APPROVED

## Task

project-brainstorm

## Reviewed evidence

- `.codex/workflows/project-brainstorm/{00-task,10-plan,20-plan-review,30-implementation-report}.md`.
- Actual Git status, tracked diff, and relevant untracked implementation files.
- Corrected launcher, isolated runtime config generation, managed server wrapper, manifest, installer transaction/recovery paths, cognition authorization/service transitions, real profiles, and focused tests.
- Installed package state and main Codex configuration hash.
- Parent-directed treatment of `RUNTIME-LOGIN-001` as an external acceptance blocker rather than a deterministic code finding.

## Review scope assessment

The reviewed implementation remains bounded to `mcp-forge-cognition/`, `cognition-store/`, `global-config/codex/`, the three project-brainstorm scripts, package tests, and `docs/agents/`. The pre-existing `.codex/config.toml`, unrelated repository-local Codex agents, and unrelated `.agents/skills/**` are outside scope and were not attributed to this change. The five prior findings were rechecked against the corrected code and targeted tests. Missing isolated login prevents authenticated runtime acceptance evidence but does not make the deterministic diff scope ambiguous.

## Finding summary

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| IMPORTANT | 0 |
| SUGGESTION | 0 |

No justified findings remain.

## Blocking findings

None.

## Important findings

None.

## Suggestions

None.

## Prior finding closure

- `CODE-REVIEW-001` closed: generated definitions now carry exact per-role `enabled_tools`; strict config/hash checks, effective inventory verification, and a version/hash/tool handshake execute before project input is read.
- `CODE-REVIEW-002` closed: updates preserve prior state and bytes, journal before/after hashes and collision-free backups, recover unfinished transactions before operations, and cover failed state writes, replay, obsolete entries, and uninstall.
- `CODE-REVIEW-003` closed: the installed wrapper survives source downgrade, binds execution to the managed server hash/runtime version/tool set, pre-feature fixtures fail before server startup for all four roles, and uninstall removes entrypoints first.
- `CODE-REVIEW-004` closed: centralized authorization preserves the real deny-by-default Product/Reviewer legacy create-to-review flow while pipeline-managed documents continue to require state grants.
- `CODE-REVIEW-005` closed: state-only transitions return the newly appended state document; tests compare returned ID, revision, and hash with `latest_pipeline_state()`.

## Requirement and plan compliance

The corrected implementation satisfies the deterministic portions of the approved plan and acceptance criteria: exact isolated role surfaces, fail-closed runtime configuration, recoverable installation/update, downgrade protection, legacy compatibility, append-only pipeline transitions, and the existing DEV bridge. No unjustified divergence or unrelated implementation change was found in the reviewed scope.

## Functional assessment

The execution paths for CDC approval, architecture/review, rework gating, development handoff, legacy Product/Reviewer operation, and returned state bindings are coherent with the documented contracts. The five previously identified defects are corrected at their source rather than masked in callers or tests.

## Test assessment

The updated tests exercise observable failure and recovery behavior: unsafe config and tool drift before input, version/hash/tool handshake mismatch, four-role pre-feature downgrade blocking, interrupted and failed installer updates, real-profile legacy flow, and latest-state response binding. The implementation report's full cognition suite and lint results are credible; this review independently reran the bounded correction-focused suites.

## Security, compatibility, and operational assessment

Role execution is fail-closed behind an exact server/tool allowlist and a managed wrapper bound to server source hash and runtime version. Apps and memories are disabled and unexpected top-level configuration is rejected. Installer recovery preserves ownership metadata, main Codex config stayed byte-identical, and entrypoint-first removal keeps downgrade failure safe. Pipeline-managed access remains grant/revision scoped; legacy compatibility does not widen pipeline grants.

## Architecture and maintainability assessment

The wrapper provides a stable compatibility boundary outside the downgradable server source, while `PipelineAuthorization` remains the central compatibility and access path. The installer journal now has sufficient information for deterministic rollback/replay. The changes remain proportionate to the identified failures.

## Validations independently executed

| Command or inspection | Result | Notes |
|---|---|---|
| Git status and complete relevant correction diff inspection | PASS | Unrelated user changes separated |
| `uv run --project mcp-forge-cognition --python 3.11 --extra dev python -m pytest -q tests` | PASS | 29 passed in 1.51s |
| Four focused cognition tests for real profiles, approval binding, human-decision binding, and role registrations | PASS | 4 passed in 16.47s |
| `py scripts/install-global-project-brainstorm.py --check` from a clean directory | PASS | `READY_FOR_RUNTIME_PREFLIGHT`; no missing files or local masks |
| Main `.codex/config.toml` SHA-256 before/after check | PASS | Byte-identical: `4E5D21B83D0620ADB2DD426216C21DECD1BEF0C204F62D16CE8BA4203270B7AA` |
| Full cognition suite and Ruff checks | RELIED ON | Implementation report records 65 tests passed and both Ruff selections passed; not redundantly rerun |
| Authenticated isolated-runtime inventory/E2E | NOT RUN | External `RUNTIME-LOGIN-001`; no project input was sent |

## Review blockers

None for the deterministic code-review verdict. `RUNTIME-LOGIN-001` remains an external acceptance gate before claiming authenticated end-to-end runtime verification.

## Required corrections

None.

## Residual risks

- Authenticated fresh-process inventory and bounded idea-to-development-handoff E2E remain to be executed after the isolated Codex login.
- Codex CLI behavior is version-dependent, so the implemented capability probes remain a required operational gate.
- Structural neutralization cannot mechanically prove semantic neutrality inside otherwise allowed factual fields.
