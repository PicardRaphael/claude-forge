# Baseline Checklist — What forge should have

Source of truth for MISSING verdicts in forge-review. Each item is a deliberate design decision.
If a component below is absent from forge, it qualifies as MISSING (pending forge-brain confirmation).

Last updated: 2026-05-08

---

## Skills (slash commands)

| Item | Expected | Rationale |
|------|----------|-----------|
| Project analysis | `repo-inspector` (mode=analyze) | Audit CC config of external repos |
| Self-check | `/self-check` | Validate forge's own conformity |
| Strategic review | `/forge-review` | Monthly status-quo challenge |
| News/updates | `/cc-news` | Stay current on CC/models |
| Vault audit | `/vault-audit` | Vault quality maintenance |
| Prompt crafting | `/craft-prompt` | Multi-LLM prompt engineering |
| Context recap | `/recap` | Session context snapshot |
| Evolution proposals | `/evolve` | External project product evolution |
| CC skills reference | `skill-creator` | Skills creation/optimization/audit |
| CC agents reference | `subagent-creator` | Agents format/patterns |
| CC hooks reference | `hook-creator` | Hooks format/patterns |
| Forge brain query | `forge-brain` | Vault CLI wrapper |

---

## Agents

| Item | Expected | Rationale |
|------|----------|-----------|
| Skill creator | `skill-creator` | Enforced by delegate-guard hook |
| Agent creator | `subagent-creator` | Enforced by delegate-guard hook |
| Hook creator | `hook-creator` | Standardize hook authoring |
| CLAUDE.md optimizer | `claudemd-creator` | Enforced by delegate-guard hook |
| Repo inspector | `repo-inspector` | Repo analyze/audit/scan (modes) — fusion de project-analyzer/auditor/codebase-scanner |
| CC Advisor | `cc-advisor` | Strategic CC setup advice |

---

## Rules

| Item | Expected | Rationale |
|------|----------|-----------|
| Delegate to specialists | `delegate-to-specialists.md` | Route writes to right agents |
| Proactive behavior / dispatch | `comportement-proactif.md` | Session routing table |
| Memory discipline | `memory-discipline.md` | Enforce memory reads/writes |
| Forge brain proactive | `forge-brain-proactive.md` | Vault query as reflex |
| Changelog vault | `changelog-vault.md` | Vault change tracking |
| Agent limits | `agent-limits.md` | Max operations per agent |

---

## Hooks

| Item | Expected | Rationale |
|------|----------|-----------|
| Delegate guard | `delegate-guard.py` | Block direct edits to protected files |
| Learning reminder | Claude: conditional non-blocking detector; Codex: no Stop parity required | Surface only uncaptured deterministic signals |
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
