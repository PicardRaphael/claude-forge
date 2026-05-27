---
name: neo_ia_analysis
description: NeoIA project analysis - Python/FastAPI/LangGraph monorepo with 7 agents, 17 skills, 7 rules, 9 hooks. Key findings on context budget overload and missing NeoMail delegation.
type: project
---

## 2026-04-03 -- NeoIA (Python 3.13 / FastAPI / LangGraph / Gemini 2.5 Flash)

### Architecture Claude Code
- 7 agents, 17 skills (8300 lignes total), 7 rules (627L), 9 hooks, 5 commands
- "Claude Brain" custom system (patterns, traps, instincts, observations) via .claude-brain/
- MCP: context7, docs-langchain. Plugins: superpowers, plugin-dev, claude-hud

### Patterns utiles
- Hierarchical CLAUDE.md per component (root + apps + packages) -- works well for navigation
- Agent delegation rule (345L) with workflow diagrams per task type -- excellent reference
- guard-check.js (Stop hook) uses git diff to detect py changes and verify lint/test/changelog -- effective guard
- observe.js auto-creates instinct files from repeated tool usage patterns -- clever but heavy
- Brain load at SessionStart + sync at PreCompact and PreToolUse(git push) -- good lifecycle

### Problemes identifies
- Skills budget depasse: dev agents charge 8-11 skills chacun (~4-5% contexte)
- neoia-conventions (225L), neoia-testing (244L), claude-brain (99L) sont triples: dans agents body + skill + rule
- NeoMail app exists since 2026-03-19 but no dev-neomail agent and no delegation rules
- on-env-protect.py uses old env var API instead of stdin -- fragile
- gemini-prompting has duplicate template file in templates/ and references/
- continuous-learning-v2 skill may overlap with observe.js hook

### Hooks efficaces
- PostToolUse Write|Edit auto-format with ruff (timeout 10s) -- zero friction
- Stop guard-check verifies git diff for py changes then checks transcript for pytest/ruff/CHANGELOG
- PreToolUse on-env-protect blocks edits to .env files

### A retenir pour projets similaires
- Monorepo Python avec agents specialises par app = le pattern agent-delegation.md est la cle
- Brain system (patterns/traps/instincts) is custom-built, not native Auto Memory -- two systems coexist
- Rules are the best ROI: auto-loaded every session, no need to attach manually
- skill-navigator rule that redirects to a skill is an anti-pattern -- just put the content in the rule
- When project has 3+ apps, having per-app dev agents with shared skills is good but watch the skill count
