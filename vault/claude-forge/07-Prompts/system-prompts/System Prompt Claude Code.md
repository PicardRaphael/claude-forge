---
titre: "System Prompt Claude Code — Architecture"
resume: "Context engineering dynamique de Claude Code : assemblage conditionnel, 512K lignes, Piebald-AI repo"
aliases:
  - "claude code system prompt"
  - "piebald system prompts"
  - "CC system prompt"
  - "context engineering claude code"
  - "piebald-ai repo"
domaine: claude-code
type: prompt
cible: claude
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://github.com/Piebald-AI/claude-code-system-prompts"
tags:
  - "#type/prompt"
  - "#domaine/claude-code"
---

## Objectif

Comprendre comment Claude Code construit son contexte dynamiquement.

## Architecture

Le leak du code source (31 mars 2026, 512K lignes TS) a révélé :

- **Assemblage dynamique conditionnel** — le system prompt est construit à la volée selon :
  - Le mode (plan, auto, default)
  - Les outils disponibles
  - Les hooks configurés
  - Les skills chargées
  - Les rules actives
  - Les MCP servers connectés
- **Pas un prompt statique** — c'est du context engineering

## Piebald-AI

Repo public qui track les system prompts Claude Code :
- 186+ versions archivées (au 22 mai 2026)
- Token counts par version
- v2.1.149 = version la plus récente archivée (au 22 mai 2026 — chiffres mis à jour : précédemment "157 / v2.1.114" périmés)

## Quand utiliser

Pour comprendre comment structurer le contexte de ses propres agents/skills.

## Liens

- [[Context Engineering]]
- [[Piebald-AI System Prompts]]
- [[MOC-Prompts]]
