---
titre: "Agent — project-analyzer"
resume: "Analyse un projet complet et propose une strategie d'automatisation Claude Code avec rapport priorise"
aliases:
  - "project-analyzer"
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

Use this agent when the user wants to analyze any project and get full Claude Code recommendations. Use PROACTIVELY when the user says "j'ai un projet", "analyse mon projet", "qu'est-ce que je peux faire", or shares a path or GitHub URL. Uses opus thinking + web search + memory.

## Tools

- Read
- Grep
- Glob
- Bash
- WebFetch
- WebSearch

## Quand utiliser

- L'utilisateur veut analyser un projet et obtenir des recommandations Claude Code
- L'utilisateur dit "j'ai un projet", "analyse mon projet", "qu'est-ce que je peux faire"
- L'utilisateur partage un chemin ou une URL GitHub

## Liens

- [[MOC-Claude-Code]]
