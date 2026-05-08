---
titre: "CC Mai 2026 — Code with Claude Drop"
resume: "Desktop GUI, web UI, Plan mode, Auto mode, Security, Dreaming, CLI updates, deprecations Sonnet 4/Opus 4"
aliases:
  - "Code with Claude mai 2026"
  - "CC mai 2026"
domaine: claude-code
type: changelog
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://www.anthropic.com/news"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Features majeures (6 mai)

- **Claude Code on the web** — coder sans terminal (claude.ai/code)
- **Claude Code on Desktop** — GUI plein ecran avec preview, images, rich outputs
- **Plan mode** — review du plan avant execution
- **Auto mode** (research preview Team) — alternative safe a --dangerously-skip-permissions
- **Claude Security** — scan vulnerabilites repos (public beta Enterprise)
- **Claude Design** — prototypes visuels
- **Claude Mythos Preview** — cybersecurite (Project Glasswing)
- **Dreaming** (research preview) — auto-review sessions passees overnight
- **Routines** (Boris) — "higher-order prompts", automations async

## CLI updates

- `CLAUDE_CODE_FORK_SUBAGENT=1` en sessions non-interactives
- Skill folder protection (skip-permissions ne prompt plus pour .claude/skills/)
- MCP auto-retry (3 tentatives) sur erreur transitoire
- `alwaysLoad` option MCP — skip tool-search deferral
- `claude plugin prune` — nettoyage dependances orphelines
- `/model` picker via gateway /v1/models

## Deprecations

- `TaskOutput` tool deprecie → utiliser Read
- **claude-sonnet-4-20250514** et **claude-opus-4-20250514** retirement API **15 juin 2026**
- 1M context beta Sonnet 4/4.5 retiree

## Metrics

- CC = 4% des commits GitHub publics (Boris, CNBC)
- Rate limits 5h doubles (Pro/Max/Enterprise)
- Suppression throttling peak hours

## Liens

- [[Code with Claude Conference]]
- [[Managed Agents]]
- [[Cowork GA]]
- [[MOC-Claude-Code]]
