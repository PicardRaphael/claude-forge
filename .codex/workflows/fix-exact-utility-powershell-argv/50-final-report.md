# Final Report

## Status

READY_FOR_HUMAN_REVIEW

## Task

fix-exact-utility-powershell-argv

## Delivered behavior

The remaining exact-workflow-utility PowerShell authorization bypass is closed.
The shared parser now proves the raw script token safe before path expansion or
normalization, then applies the same quote-aware literal-atom contract to every
later argument before any read-only allow or mutating write-policy decision.

All eight runtime workflow utilities are covered under initial and rework
architecture assignments. Canonical quoted and unquoted invocations remain
supported, while expression-shaped argv and expression-bearing path aliases are
denied before Python starts.

## Files and components affected

- `C:\Users\rapha\.codex\hooks\scripts\common.py` — quote-aware raw-path and argv authorization.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py` — all-utility parser matrices and legitimate positives.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py` — both-phase hook matrices and sentinel integrity.

## Validation evidence

| Command | Result | Notes |
|---|---|---|
| Python syntax compilation | PASS | Relevant hook and test files compile. |
| Installation `self_test.py` | PASS | All exact utilities and parser contracts validate. |
| Full `full_self_test.py` | PASS | Recorded same-hash E2E covers all utilities, both vector locations, both architecture phases, sentinels, and legitimate invocations. |
| Workflow Registry validator | PASS | All installed workflows remain valid. |
| DEV intake validator | PASS | The correction workflow intake is valid. |
| Individual handoff validators | PASS | Plan, plan review, implementation report, and code review validate. |

## Review result

Independent CODE_REVIEW status: `APPROVED`.

Findings: zero BLOCKING, zero IMPORTANT, zero SUGGESTION. The source argv bypass
and the path-normalization variant are both closed across the complete
runtime-resolved utility inventory.

## Assumptions and residual risks

- Global hook assets are not Git-versioned; attribution relies on recorded
  before/after hashes, direct inspection, deterministic tests, and preserved
  repository status.
- The literal grammar is intentionally conservative. Future punctuation support
  must include PowerShell-safety evidence and matching positive/negative tests.
- The aggregate change-delivery validator has a pre-existing loop-budget naming
  mismatch with the intake compiler. The authoritative intake validator and all
  individual handoff validators pass.

## Out-of-scope follow-ups

Align the task-intake and change-delivery validators' loop-budget field names in
a separate bounded maintenance task.

## Git and pull request

- Branch: Not applicable; global Codex hook assets were modified outside the repository Git root.
- Commits: None requested or created.
- Draft PR: None requested or created.
