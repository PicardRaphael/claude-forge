---
name: code-dev-agent
description: Agent code-dev multi-stack dans forge (remplace python-dev) — 4 modes, hook code-lint-dispatch PostToolUse, TDD, skill python-ref
type: reference
originSessionId: 0189dcca-363c-4f81-ae4e-e4860a4bfc24
---

> ⚠️ **Mis à jour 6 juin 2026** — `python-dev` remplacé par `code-dev` (multi-stack).

Agent `code-dev` dans claude-forge pour tout développement.

- Fichier : `.claude/agents/code-dev.md`
- Skill associée : `.claude/skills/python-ref/` (Python) + autres stacks
- 4 modes : avec plan, sans plan, debug, refactoring
- TDD obligatoire, pytest (Python), type hints, dataclasses
- Hook PostToolUse `code-lint-dispatch.py` (à créer via hook-creator) — dispatche ruff/eslint/gofmt/clippy selon la stack
- Délègue aux spécialistes forge (skill-creator, subagent-creator, claudemd-creator)
- ATTENTION : `code-dev` est un agent custom, pas un subagent_type natif. Utiliser `general-purpose` avec contexte dans le prompt si invocation via subagent_type.
