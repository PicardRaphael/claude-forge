---
name: python-dev-agent
description: Agent python-dev generique dans forge — 4 modes (plan, sans plan, debug, refactoring), skill python-ref
type: reference
originSessionId: 0189dcca-363c-4f81-ae4e-e4860a4bfc24
---
Agent `python-dev` cree dans claude-forge pour tout dev Python.

- Fichier : `.claude/agents/python-dev.md`
- Skill associee : `.claude/skills/python-ref/`
- 4 modes : avec plan, sans plan, debug, refactoring
- TDD obligatoire, pytest, type hints, dataclasses
- Hook py_compile sur chaque Write/Edit
- Delegue aux specialistes forge (skill-creator, agent-creator, claudemd-optimizer)
- ATTENTION : `python-dev` est un agent custom, pas un subagent_type. Il ne peut pas etre passe en `subagent_type` de l'outil Agent. Utiliser `general-purpose` avec le contexte Python dans le prompt.
