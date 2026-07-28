# Plan Review

## Status

APPROVED

## Task

project-brainstorm

## Verdict

The Option A security delta is implementation-ready. It moves role execution out of native inherited-tool subagents into an independently authenticated, capability-gated `CODEX_HOME`, keeps the user's main Codex configuration read-only, and defines fail-closed startup and downgrade behavior.

## Reviewed evidence

- Updated `.codex/workflows/project-brainstorm/00-task.md`.
- Updated `.codex/workflows/project-brainstorm/10-plan.md`.
- Previously approved v1 compatibility, centralized authorization/indexing, state-machine, installer, and DEV bridge contracts.
- Delta sections covering the isolated runtime, dispatcher descriptors, CLI capability/authentication preflight, rollout/rollback, downgrade guard, runtime tests, and operational risks.
- Installed CLI fact recorded in the plan: the first-on-PATH npm `codex-cli 0.42.0` is treated as incompatible until capability probes pass.
- Applicable `change-delivery-workflow` handoff and review contracts.

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

None before implementation.

Security delta closure:

- **Isolated execution:** one managed `~/.codex-project-brainstorm/` runtime contains only the four disabled-by-default cognition definitions, with apps/plugins/hooks/memories absent or disabled; the launcher enables exactly one role MCP in a read-only child.
- **Fail-closed dispatch:** the globally discoverable TOMLs are explicitly dispatch descriptors, receive no role MCP configuration, perform no role workload, and direct the parent to the deterministic Skill/launcher path. Runtime tests cover direct descriptor invocation and require no project-content/tool execution.
- **Independent login:** authentication is neither copied nor linked from the main home. `--check` returns `LOGIN_REQUIRED` and prints the isolated one-time login command; execution remains blocked until validation succeeds.
- **Capability gate:** executable path and behavior probes, rather than a guessed version threshold, must prove `CODEX_HOME`, `exec`, config overrides, MCP listing, apps default-disable, and read-only sandbox. The installer refuses the known incompatible CLI and never upgrades it automatically.
- **Main config protection:** installation and runtime manage only isolated-home files and canonical global agents/Skills. The user's main `~/.codex/config.toml` is read-only throughout install, update, execution, rollback, and uninstall.
- **Downgrade guard:** managed role entry points are disabled before older code can be selected; non-Curator isolated profiles are removed/disabled and startup checks for pipeline-managed records before serving, returning `pipeline_runtime_too_old` on incompatibility.

## Requirement and acceptance-criteria coverage

- AC-001/AC-002 remain covered by discoverable dispatcher TOMLs and the orchestrating/individual Skills, without using the native descriptors as the security boundary.
- AC-003/AC-003A are covered by absolute isolated MCP definitions, disabled-by-default profiles, exact single-role enabling, executable/capability/auth gates, and the prohibition on main-config mutation.
- AC-004 through AC-008 retain the previously approved server-side authorization, append-only state, closed transition, installer, and DEV bridge contracts.
- AC-009 adds fresh isolated processes, exact effective inventories, dispatcher fail-closed probes, two clean repositories, and masking coverage.
- AC-009A is covered by ordered entry-point shutdown plus the store compatibility guard before any older runtime serves pipeline-managed data.
- AC-010 retains the full regression/security/schema/neutralization/installer/runtime and independent review gates.

## Scope assessment

The isolated runtime is a justified addition, not a competing agent framework. It is the smallest enforceable response to the confirmed Option A decision because native custom agents inherit ambient capabilities. The design still uses one cognition MCP/store, three user-facing roles, one parent orchestrator, and the existing downstream DEV workflow.

## Architecture assessment

The security boundary is now explicit: role prompts and project inputs cross only into a preflighted child process whose home, config, authentication, sandbox, apps, and single MCP are controlled. Native TOMLs are discovery/dispatch metadata rather than privileged workers. This cleanly separates global UX from execution authority while preserving the previously approved service-layer controls.

## Tests and validation assessment

The updated matrix tests the observable security properties rather than trusting static TOML: effective single-role tool inventory, disabled curator access, fail-closed descriptors, isolated authentication failure, incompatible CLI failure, main-config byte preservation, downgrade ordering/guard, clean-repository discovery, masking, and bounded E2E. Existing cognition regression, ACL, index, schema, installer, and rollback checks remain required.

## Security, compatibility, and operational assessment

The delta materially improves isolation. It avoids authentication copying, ambient apps/plugins, inherited MCP use for role workloads, silent CLI upgrades, and mutation of the user's primary config. Missing login, unsupported CLI behavior, inventory mismatch, or an older runtime all fail before project input is supplied. Backups/journaling remain limited to managed isolated/global artifacts, and unmanaged authentication/configuration must survive uninstall.

## Validations independently executed

- `python C:\Users\rapha\.codex\skills\change-delivery-workflow\scripts\validate_handoff.py .codex\workflows\project-brainstorm\10-plan.md`: **validation passed**.
- Targeted read-only inspection confirmed all six Option A controls are represented in requirements, design, implementation sequence, tests, rollout/rollback, risks, and acceptance criteria.
- No source, configuration, authentication, runtime-home, Skill, agent, store, test, or Git state was modified by this review.

## Approved implementation contract

- Treat the isolated child process, not a native descriptor, as the only role-execution boundary.
- Never send project input until executable, capability, authentication, sandbox, apps, and exact single-role MCP inventory checks all pass.
- Keep the main `~/.codex/config.toml` byte-identical; do not copy/link/read out authentication secrets or auto-upgrade Codex.
- Dispatcher descriptors must make zero tool calls and return only the deterministic secure invocation path, including under adversarial role input.
- Curator execution remains an explicit parent consolidation action and is never available to Product, Architect, or Reviewer children.
- Implement downgrade as an ordered managed operation: disable entry points first, then enforce the compatibility check before any older cognition runtime is launched against pipeline-managed data.
- Preserve isolated `auth.json` as unmanaged user state during update, rollback, and uninstall.
- Retain every previously approved v1, authorization/index, state-machine, neutralization, installer, DEV bridge, regression, and code-review gate.

## Residual risks

- Independent authentication requires a one-time user action; implementation may complete while runtime acceptance remains correctly blocked on `LOGIN_REQUIRED`.
- The installed CLI is currently known incompatible. No global runtime success may be claimed until the user installs an official compatible CLI and the behavioral gate passes.
- Dispatcher fail-closed behavior is an agent instruction/evaluation boundary, not a capability boundary; security therefore depends on never routing project content through it and on the isolated launcher being the documented and tested role path.
- Codex CLI configuration semantics can change; behavioral capability and effective-inventory probes remain release gates on every install/update.
