---
titre: "Agent Teams — Multi-agent orchestration"
resume: "Feature Claude Code permettant plusieurs agents collaboratifs sur un meme projet — delegation parallele, specialisation, worktrees isoles."
aliases:
  - "Agent Teams"
  - "agent teams CC"
  - "multi-agent claude code"
  - "equipes agents"
  - "teams claude code"
type: feature
domaine: claude-code
derniere-maj: 2026-06-24
auteur: claude
sources: []
tags:
  - "#type/feature"
  - "#domaine/claude-code"
---

## Description

Agent Teams permet d'orchestrer plusieurs agents Claude Code travaillant en parallele sur un meme projet. Chaque agent a sa specialisation, ses outils, et peut travailler dans un worktree isole.

## Liens

- [[MOC-Claude-Code]]
- [[cowork-architecture]]
- [[Session Sharing]]

## ⚠️ Mécanique de création changée (v2.1.178, 15 juin 2026)

`TeamCreate`/`TeamDelete` supprimés → **équipe implicite** : avec `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, on spawn un teammate directement via le paramètre `name` du tool `Agent`. `team_name` accepté mais ignoré. Détail + amendement daté : [[agent-teams-natif-anthropic]] section « AJOUT 24 juin 2026 ».