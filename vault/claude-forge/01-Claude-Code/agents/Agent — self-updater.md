---
titre: "Agent — self-updater"
resume: "Met a jour les skills de reference de claude-forge quand de nouvelles features Claude Code sont detectees"
aliases:
  - "self-updater"
  - "self updater"
  - "mise à jour skills CC"
  - "auto updater"
  - "update skills forge"
  - "synchronisation références"
projet: claude-forge
type: agent
permission-mode: default
model: sonnet
effort: high
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/agent"
  - "#domaine/claude-code"
---

## Role

Use this agent to update claude-forge reference skills when new Claude Code features are detected. Use PROACTIVELY after cc-news finds changes post reference date.

## Tools

- Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
- Skills : cc-news, cc-features-ref, cc-hooks-ref, cc-agents-ref, cc-skills-ref, forge-brain, obsidian-cli, obsidian-markdown
- `memory: project` | `color: cyan`

## Quand utiliser

- De nouvelles features Claude Code ont ete detectees (post date de reference)
- Apres que cc-news a trouve des changements
- Mise a jour des skills de reference (cc-agents-ref, cc-skills-ref, cc-hooks-ref, cc-features-ref)

## Liens

- [[MOC-Claude-Code]]
