---
titre: "Agent — project-auditor"
resume: "Audite la configuration .claude/ d'un projet (agents, skills, hooks, rules, settings) et produit un rapport avec corrections"
aliases:
  - "project-auditor"
projet: claude-forge
type: agent
permission-mode: default
model: opus
effort: high
derniere-maj: 2026-04-21
auteur: claude
tags:
  - "#type/agent"
  - "#domaine/claude-code"
---

## Role

Use when asked to audit a project's .claude/ setup, verify agents/skills/hooks/rules quality, or check for issues like missing colors, bad descriptions, wrong tools, deprecated features. Produces a report with fixes.

## Tools

- Read
- Glob
- Grep
- Agent

## Quand utiliser

- L'utilisateur demande un audit de la configuration .claude/ d'un projet
- Verification de la qualite des agents, skills, hooks, rules
- Detection de problemes : couleurs manquantes, descriptions incorrectes, outils inadaptes, features deprecees

## Liens

- [[MOC-Claude-Code]]
