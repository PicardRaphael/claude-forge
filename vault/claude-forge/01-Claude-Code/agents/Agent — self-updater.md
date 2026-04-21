---
titre: "Agent — self-updater"
resume: "Met a jour les skills de reference de claude-forge quand de nouvelles features Claude Code sont detectees"
aliases:
  - "self-updater"
projet: claude-forge
type: agent
permission-mode: default
model: sonnet
effort: high
derniere-maj: 2026-04-21
auteur: claude
tags:
  - "#type/agent"
  - "#domaine/claude-code"
---

## Role

Use this agent to update claude-forge reference skills when new Claude Code features are detected. Use PROACTIVELY after cc-news finds changes post reference date.

## Tools

- Read
- Write
- Glob
- Bash
- WebSearch
- WebFetch

## Quand utiliser

- De nouvelles features Claude Code ont ete detectees (post date de reference)
- Apres que cc-news a trouve des changements
- Mise a jour des skills de reference (cc-agents-ref, cc-skills-ref, cc-hooks-ref, cc-features-ref)

## Liens

- [[MOC-Claude-Code]]
