# Final Report

## Status

READY_FOR_HUMAN_REVIEW

## Task

enforce-brainstorm-opt-in-strict

## Delivered behavior

Codex no longer starts a new Brainstorm workflow from ordinary prose about an idea, a CDC, or an architecture. A new Brainstorm target now requires an explicit current-prompt `$project-brainstorm` invocation or an autonomous `MODE: BRAINSTORM` header. Persisted Brainstorm state may continue only the exact compatible workflow already bound to the session; it cannot initialize another target.

Normal Brainstorm routes still begin at `brief_interview`, require the explicit `brief validé` human gate before CDC production, preserve CDC approval, and keep the approved-CDC architecture importer hash-bound. DEV inference remains parent-owned for explicit implementation work, while GENERAL remains read-only.

Managed handoff writes now fail closed unless the exact canonical workflow, READY Registry definition, managed route, phase, actor, artifact, and write policy authorize them. The protection covers Write, Edit, every apply-patch target, exact workflow utilities, path aliases, traversal, Win32 aliases, junctions, file symlinks/reparse points, and all MCP calls. MCP permissions are based on exact registered capabilities rather than verb heuristics: unknown or conflicting IDs are denied, exact read-only tools may proceed, exact remote mutations require DEV, and no filesystem-local mutation is enabled without an exact adapter.

The corrected hook runtime is installed globally under `C:\Users\rapha\.codex\hooks\workflow-suite`. No Registry route, product repository, project-local hook, Git history, trust hash, connector, deployment, or external system was modified.

## Files and components affected

- `C:\Users\rapha\.codex\AGENTS.md` — strict global mode routing, current-prompt opt-in, MCP contract, path/reparse and TOCTOU rules.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml` — DEV-only generic intake and no Brainstorm inference from prose.
- `C:\Users\rapha\.codex\skills\task-intake-workflow` — explicit routing, ambiguity gate and fail-before-write intake.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md` — explicit initial activation versus bound continuation.
- `C:\Users\rapha\.codex\hooks\scripts` — mode provenance, canonical binding, pending initialization transaction, exact target adapters and exhaustive MCP capability classification.
- `C:\Users\rapha\.codex\hooks\installer` — fast and full adversarial regression suites.
- `C:\Users\rapha\.codex\hooks\workflow-suite` — installed runtime, SHA-256-identical to the 14 source Python files.
- `C:\Users\rapha\.codex\hooks\README.md` — operator, installation, trust and residual-risk guidance.
- `C:\Users\rapha\.codex\hooks.json` and `C:\Users\rapha\.codex\config.toml` — installer-managed global hook configuration; existing project trust entries preserved.

## Validation evidence

| Validation | Result | Notes |
|---|---|---|
| Workflow Registry validator | PASS | Registered Brainstorm, DEV and GENERAL workflows validate; Registry semantics are unchanged. |
| Final source fast suite | PASS | Activation, binding, aliases, real Windows reparse targets and exact MCP contracts pass. |
| Final source full suite | PASS | Complete V8.2 Registry, DEV compatibility, explicit Brainstorm, memory, human-gate, MCP and hook matrix passes. |
| Official runtime installation | PASS | Canonical installer completed with recoverable backups. |
| Final installed-runtime fast suite | PASS | Re-executed by the parent after the final correction. |
| Final installed-runtime full suite | PASS | Completed after `CODE-REVIEW-004`; all adversarial and valid flows pass. |
| Source/runtime parity | PASS | 14 source Python files, 14 runtime files, zero SHA-256 mismatch. |
| Windows reparse coverage | PASS | Real task junction and artifact-file symlink tests ran without skip and were denied before mutation. |
| Handoff and workflow validators | PASS | Plan, reviews, implementation report and workflow directory validate. |

## Review result

Independent CODE_REVIEW status: `APPROVED`.

The reviewer reported zero BLOCKING, zero IMPORTANT and zero SUGGESTION findings. `CODE-REVIEW-001` through `CODE-REVIEW-004` are closed on source and runtime: canonical path aliases are denied, reparse targets are denied, every MCP is classified before policy evaluation, neutral unknown IDs fail closed, exact read-only and remote DEV contracts retain their intended positive behavior, and the former verb heuristic is absent.

## Assumptions and residual risks

- Operational state is `RESTART_RETRUST_REQUIRED`, not `TRUSTED_READY`: Codex App must be restarted and the changed global hooks from `C:\Users\rapha\.codex\hooks.json` must be explicitly reviewed/trusted before relying on them. Zero global trust entries were written or simulated; the 10 existing project-local entries were preserved.
- A PreToolUse check and the later filesystem open cannot be atomic. Existing path components are checked with `lstat` through the artifact immediately before authorization, but a local attacker capable of racing filesystem replacement retains a residual TOCTOU window. Hooks remain guardrails and do not replace sandboxing or least privilege.
- Global Codex control-plane files live outside this repository's Git history. Recovery relies on the installer backup and the targeted pre-install snapshot recorded in `30-implementation-report.md`.

## Out-of-scope follow-ups

- After restart and trust approval, run one smoke test with ordinary CDC/architecture prose and confirm that no Brainstorm workflow is initialized, then run one explicit `$project-brainstorm` activation and confirm it begins at `brief_interview`.
- No product implementation, CDC creation, architecture execution, connector mutation, deployment or release was performed.

## Git and pull request

- Branch: unchanged.
- Commits: none requested or created.
- Draft PR: none requested or created.
