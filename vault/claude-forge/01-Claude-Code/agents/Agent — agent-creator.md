---
titre: "Agent — agent-creator"
resume: "Cree et modifie des subagents Claude Code en posant des questions structurees et en appliquant les best practices"
aliases:
  - "agent-creator"
  - "agent creator"
  - "création agents CC"
  - "subagent creator"
  - "créer un agent"
  - "générateur agents"
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

Use this agent when the user wants to CREATE or MODIFY a Claude Code subagent. Use PROACTIVELY when the user says "cree un agent qui", "j'ai besoin d'un agent pour", or when cc-advisor recommends an agent.

## Tools

- Read, Write, Edit, Glob, Grep, Bash, WebSearch
- Skills : cc-agents-ref, forge-brain, obsidian-cli, obsidian-markdown
- `memory: project` | `color: blue`

## Quand utiliser

- L'utilisateur veut creer ou modifier un subagent Claude Code
- L'utilisateur dit "cree un agent qui", "j'ai besoin d'un agent pour"
- cc-advisor recommande la creation d'un agent

## Liens

- [[MOC-Claude-Code]]
