# Baseline Checklist — What forge should have

Source of truth for MISSING verdicts in forge-review. Each item is a deliberate design decision.
If a component below is absent from forge, it qualifies as MISSING (pending forge-brain confirmation).

Last updated: 2026-05-08

---

## Skills (slash commands)

| Item | Expected | Rationale |
|------|----------|-----------|
| Project analysis | `/analyze-project` or equivalent | Audit CC config of external repos |
| Self-check | `/self-check` | Validate forge's own conformity |
| Strategic review | `/forge-review` | Monthly status-quo challenge |
| News/updates | `/cc-news` | Stay current on CC/models |
| Vault audit | `/vault-audit` | Vault quality maintenance |
| Prompt crafting | `/craft-prompt` | Multi-LLM prompt engineering |
| Context recap | `/recap` | Session context snapshot |
| Evolution proposals | `/evolve` | External project product evolution |
| CC skills reference | `cc-skills-ref` | Skills format/patterns |
| CC agents reference | `cc-agents-ref` | Agents format/patterns |
| CC hooks reference | `cc-hooks-ref` | Hooks format/patterns |
| Forge brain query | `forge-brain` | Vault CLI wrapper |

---

## Agents

| Item | Expected | Rationale |
|------|----------|-----------|
| Skill creator | `skill-creator` | Enforced by delegate-guard hook |
| Agent creator | `agent-creator` | Enforced by delegate-guard hook |
| Hook creator | `hook-creator` | Standardize hook authoring |
| CLAUDE.md optimizer | `claudemd-optimizer` | Enforced by delegate-guard hook |
| Project auditor | `project-auditor` | Multi-repo CC config audit |
| CC Advisor | `cc-advisor` | Strategic CC setup advice |

---

## Rules

| Item | Expected | Rationale |
|------|----------|-----------|
| Delegate to specialists | `delegate-to-specialists.md` | Route writes to right agents |
| Proactive behavior / dispatch | `comportement-proactif.md` | Session routing table |
| Check before create | `check-before-create.md` | Prevent blind creation |
| Memory discipline | `memory-discipline.md` | Enforce memory reads/writes |
| Forge brain proactive | `forge-brain-proactive.md` | Vault query as reflex |
| Changelog vault | `changelog-vault.md` | Vault change tracking |
| Agent limits | `agent-limits.md` | Max operations per agent |

---

## Hooks

| Item | Expected | Rationale |
|------|----------|-----------|
| Delegate guard | `delegate-guard.py` | Block direct edits to protected files |
| Learning reminder | `learning-reminder.py` or equivalent | Periodic memory compounding prompt |
| Session health | `session-health.py` or equivalent | Session quality monitoring |

---

## CLAUDE.md standards

| Check | Standard |
|-------|----------|
| Line count | < 100 lines (prune regularly) |
| Gotchas section | Present |
| Priority of sources | Documented (forge-brain > memory > skills) |
| Model aliases | Documented (sonnet/opus/haiku mapping) |
| No routing logic | Routing in .claude/rules/, not CLAUDE.md |

---

## Memory system

| Item | Expected | Rationale |
|------|----------|-----------|
| MEMORY.md index | `.claude/agent-memory/skill-creator/MEMORY.md` | Project memory index |
| Feedback files | `feedback_*.md` per significant lesson | Prevent repeating mistakes |
| Reference files | `reference_*.md` per external system/pattern | Lookup without re-searching |

---

## Vault (forge-brain)

| Item | Expected | Rationale |
|------|----------|-----------|
| MOC per domain | 6 MOCs in 00-Hub/ | Navigation index |
| Knowledge/erreurs/ | Error notes with template | Prevent error repetition |
| Knowledge/questions/ | Resolved questions | Avoid re-researching |
| Templates/ | 10 templates (feature, changelog, etc.) | Consistent note creation |
| MCP forge-brain | `mcp-forge-brain/` (port 8091, auto-start) | Vault access |
