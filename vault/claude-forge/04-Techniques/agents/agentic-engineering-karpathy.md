---
titre: "Agentic Engineering — Karpathy Sequoia AI Ascent 2026"
resume: "Framework Software 3.0 de Karpathy : vibe coding vs agentic engineering, jagged intelligence, shifted scarcity, agent-native infrastructure"
aliases:
  - "agentic engineering karpathy"
  - "software 3.0"
  - "sequoia AI ascent"
  - "karpathy agentic engineering"
  - "jagged intelligence"
  - "shifted scarcity"
domaine: claude-code
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=96jN2OCOfLs"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Description

Framework de reference pour le developpement assiste par agents IA, presente par Andrej Karpathy a Sequoia AI Ascent (mai 2026).

## Software 3.0

| Era | Mecanisme |
|-----|-----------|
| 1.0 | Code explicite |
| 2.0 | Datasets/objectifs → poids appris |
| 3.0 | Prompts, contexte, outils, memoire → LLM interprete |

Context window = programme. LLM = interpreteur.

## Vibe Coding vs Agentic Engineering

- **Vibe coding** : releve le plancher. Tout le monde peut creer.
- **Agentic engineering** : releve le plafond. Orchestrer agents faillibles en maintenant qualite, securite, taste.

Responsabilites agentic engineer :
- Design specs
- Supervise agent plans
- Inspecte diffs
- Ecrit/execute boucles d'eval
- Gere permissions
- Isole worktrees
- Preserve integrite systeme

## Jagged Intelligence

`capability spike = verifiabilite x training attention x data coverage x economic value`

> "Traditional software automates what you can specify. LLMs automate what you can verify."

## Shifted Scarcity

| Moins rare | Plus rare |
|------------|-----------|
| Generation code | Jugement system design |
| Rappel APIs | Taste & esthetique |
| Boilerplate | Design evals |
| Setup repetitif | Securite/hardening |
| Premiers brouillons | Orchestration agents |
| | Savoir quand le modele a tort |

## Workflow Karpathy

- Claude Code + Codex CLI + Cursor + Gemini
- Delegue macro-actions aux agents
- Ecrit/supervise specs et plans
- Review diffs pour correctness systeme
- Construit LLM knowledge bases (wikis)

## Agent-Native Infrastructure

Tout doit etre reecrit pour les agents :
- Markdown docs, CLIs, APIs, MCP servers
- Logs structures, schemas machine-readable
- Instructions copy-pastable, permissions safe
- Actions auditables, setup headless

## Citations cles

> "I have never felt more behind as a programmer."
> "You can outsource your thinking, but you can't outsource your understanding."
> "Vibe coding raises the floor. Agentic engineering is about extrapolating the ceiling."
> "Don't just ask what AI can help you build faster. Ask what AI makes unnecessary."

## Application forge

- architect-first = plan-driven
- Agents paralleles worktrees = Boris workflow
- Session principale orchestre = humain operateur
- test-writer systematique = verification output
- forge-brain/neo-brain = LLM knowledge bases
- CLAUDE.md concis + skills progressives = context window comme programme
- Piste d'amelioration : evals systematiques

## Quand utiliser

Cadre conceptuel pour toute decision d'architecture agentic : quand deleguer aux agents, quand garder le controle humain, comment structurer l'infrastructure pour les agents.

## Liens

- [[MOC-Techniques]]
- [[Andrej Karpathy]]
- [[vibe-coding-setup-complet]]
- [[pattern-agentic-engineering]]
