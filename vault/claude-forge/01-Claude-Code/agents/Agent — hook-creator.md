---
titre: "Agent — hook-creator"
resume: "Cree et modifie des hooks Claude Code (formatting, notifications, blocage, evenements lifecycle)"
aliases:
  - "hook-creator"
  - "hook creator"
  - "création hooks CC"
  - "hook builder"
  - "créer un hook"
  - "automatisation lifecycle"
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

Use this agent when the user wants to CREATE or MODIFY a Claude Code hook. Use PROACTIVELY when the user wants automatic formatting, notifications, blocking dangerous actions, or anything triggered automatically on lifecycle events. Also suggests /loop or /schedule when more appropriate.

## Tools

- Read, Write, Edit, Glob, Grep, Bash
- Skills : cc-hooks-ref, cc-features-ref, forge-brain, obsidian-cli, obsidian-markdown
- `memory: project` | `color: orange`

## Quand utiliser

- L'utilisateur veut creer ou modifier un hook Claude Code
- Besoin de formatting automatique, notifications, blocage d'actions dangereuses
- Tout ce qui doit etre declenche automatiquement sur des evenements lifecycle
- Suggere /loop ou /schedule quand c'est plus adapte

## Liens

- [[MOC-Claude-Code]]
