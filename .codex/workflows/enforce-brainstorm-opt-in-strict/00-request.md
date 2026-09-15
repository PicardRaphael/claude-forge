# Original Request

## Captured at

2026-08-04T09:22:22.187370+00:00

## Explicit mode

DEV

## Requested intake depth

DEEP

## Auto-run

YES

## Raw request

go correction opt-in strict

## Explicit constraints

- Implement the previously audited strict opt-in contract: BRAINSTORM may start only from explicit $project-brainstorm or MODE: BRAINSTORM; ambiguous requests must ask instead of silently selecting BRAINSTORM.
- Global Codex hooks must fail closed for CDC, approval, architecture, and design-review artifacts when no valid managed workflow and phase assignment exists.
- Preserve existing DEV inference for explicit implementation, bug-fix, refactor, migration, testing, configuration, and delivery requests; GENERAL remains read-only.
- Preserve existing Registry route semantics: DISCOVERY_ONLY and FULL_DESIGN start at brief_interview; APPROVED_CDC_DESIGN requires the explicit approved-package importer and exact bindings.

## User-provided acceptance criteria

- Natural-language idea, requirements, CDC, or architecture prose without explicit Brainstorm activation cannot initialize or write a Brainstorm workflow artifact.
- Explicit $project-brainstorm and MODE: BRAINSTORM activations still initialize at brief_interview and cannot reach cdc_brainstorm before USER brief validé evidence.
- APPROVED_CDC_DESIGN still starts at architect_brainstorm only through the explicit hash-bound importer.
- Global hooks are installed, trusted-state readiness is reported honestly, and source/runtime tests cover positive and negative routing cases.

## User-provided exclusions

- Do not modify product repositories or create any product CDC, architecture, review, implementation, commit, push, PR, deployment, or release.

## Source

Codex App user prompt.
