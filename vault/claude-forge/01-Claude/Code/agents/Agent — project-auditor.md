---
titre: "Agent — project-auditor"
resume: "Audite la configuration .claude/ d'un projet (agents, skills, hooks, rules, settings) et produit un rapport avec corrections"
aliases:
  - "project-auditor"
  - "project auditor"
  - "audit config CC"
  - "quality checker"
  - "vérifier configuration projet"
  - "audit agents skills hooks"
projet: claude-forge
type: agent
permission-mode: default
model: opus
effort: high
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/agent"
  - "#domaine/claude-code"
---

## Role

Use when asked to audit a project's .claude/ setup, verify agents/skills/hooks/rules quality, or check for issues like missing colors, bad descriptions, wrong tools, deprecated features. Produces a report with fixes.

## Tools

- Read, Write, Edit, Glob, Grep, Bash, Agent
- Skills : cc-agents-ref, cc-skills-ref, cc-hooks-ref, cc-features-ref, cc-prompt-ref, forge-brain, obsidian-cli, obsidian-markdown
- `memory: project` | `color: red`

## Quand utiliser

- L'utilisateur demande un audit de la configuration .claude/ d'un projet
- Verification de la qualite des agents, skills, hooks, rules
- Detection de problemes : couleurs manquantes, descriptions incorrectes, outils inadaptes, features deprecees

## Liens

- [[MOC-Claude-Code]]
