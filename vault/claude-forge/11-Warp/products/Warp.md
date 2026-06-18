---
titre: "Warp — Agentic Development Environment (ADE)"
resume: "Terminal Rust de Zach Lloyd devenu ADE (Warp 2.0) : 4 piliers Code/Agents/Terminal/Drive, 71% SWE-bench Verified, #1 Terminal-Bench (52%), plateforme cloud Oz pour orchestrer Claude Code/Codex/Warp Agent. Thèse : le terminal est le workbench naturel de l'IA."
aliases:
  - "Warp"
  - "Warp terminal"
  - "Warp 2.0"
  - "Warp ADE"
  - "agentic development environment"
  - "Warp Code"
  - "Oz Agent Platform"
type: concurrent
derniere-maj: 2026-06-18
auteur: claude
sources:
  - "https://www.warp.dev/blog/reimagining-coding-agentic-development-environment"
  - "https://sequoiacap.com/podcast/making-the-case-for-the-terminal-as-ais-workbench-warps-zach-lloyd/"
  - "https://thenewstack.io/how-warp-went-from-terminal-to-agentic-development-environment/"
  - "https://x.com/zachlloydtweets/status/2066908445425496348"
tags:
  - "#type/concurrent"
  - "#domaine/warp"
---

## Vue d'ensemble

Terminal moderne écrit en **Rust**, lancé en 2022 par [[Zach Lloyd]] (ex-Principal Eng Google Docs) pour réinventer la ligne de commande des développeurs. La montée des agents de code a transformé la trajectoire : Warp s'est repositionné en **Agentic Development Environment (ADE)** plutôt que terminal.

Thèse fondatrice de Lloyd : **le terminal est le workbench naturel de l'IA**. Son interface texte + temporelle est idéale pour orchestrer des agents, multitâcher, et logger — *« You can multitask agents in the terminal really easily »*. Warp parie sur la convergence terminal ⨯ IDE en un poste de travail conçu pour le prompting et l'orchestration d'agents.

## Features clés

- **Warp 2.0 / ADE — 4 piliers** :
  1. **Code** — agent de codage (top-5 SWE-bench, #1 Terminal-Bench)
  2. **Agents** — UI de gestion multi-agents pour lancer des tâches en parallèle
  3. **Terminal** — la CLI moderne d'origine
  4. **Drive** — base de connaissance partagée humains + agents
- **Warp Code** — éditeur de fichiers intégré, revue du code écrit par l'agent, fichiers **WARP.md** pour piloter l'agent (équivalent CLAUDE.md / AGENTS.md)
- **Oz (Oz Agent Platform)** — plateforme **cloud** d'orchestration multi-agents, **séparée** de l'ADE local : intègre et pilote Claude Code, Codex, Warp Agent « et la suite » à l'échelle
- **Support des CLI tierces** — Claude Code, Codex, Gemini CLI, OpenCode dans des onglets verticaux, avec notifications, code review natif, remote control

## Benchmarks (source primaire warp.dev, vérifiée 18 juin 2026)

| Benchmark | Score |
|---|---|
| SWE-bench Verified | **71%** |
| Terminal-Bench | **#1, 52%** |

> Chiffres marketing à manier avec prudence : Warp annonce aussi « 75M lignes générées à 95% d'acceptation » chez ses early testers, « +240% productivité » chez un cabinet de conseil, onboarding « une semaine plus rapide ». Métriques auto-déclarées, non auditées indépendamment.

## Les 3 stades du coding IA (framing Lloyd)

1. **Complétions inline** — GitHub Copilot, premier Cursor
2. **Coding agentique** — l'agent prend des tâches de bout en bout (transition « des derniers mois »)
3. **Déclenché par événements système** — l'agent est invoqué automatiquement : *« a crash detected through your crash reporting system, let's have an agent fix that »* ; un ticket utilisateur sur un défaut UI lance un fix. (Convergent avec la 3e phase prédite par Lloyd, et avec les routines/CI auto-fix d'Anthropic.)

## Thèse stratégique — l'intention humaine, prochain goulot

Lloyd : *« coding will be solved »* d'ici quelques années. Quand générer du code fonctionnel devient ubiquitaire, le vrai goulot devient la **capacité humaine à exprimer clairement l'intention** et à guider les agents. Horizon 2030 : pas la disparition des ingénieurs, mais **beaucoup plus de logiciel** produit par des résolveurs de problèmes opérant à un niveau d'abstraction supérieur. Convergent avec [[Boris Cherny]] (« engineer's value shifts to decisions above the code ») et [[addy-osmani]] (jugement/taste/systems thinking = le bottleneck réel).

## Comparaison avec Claude Code

| Feature | Warp ADE | Claude Code |
|---|---|---|
| Surface | Terminal Rust natif (ADE) | CLI + extensions IDE |
| Multi-agent | UI « Agents » + Oz (cloud) | Agent Teams + Routines |
| Pilotage projet | WARP.md | CLAUDE.md / AGENTS.md |
| Orchestration cloud | Oz (pilote AUSSI Claude Code/Codex) | Managed Agents, web |
| Drive (knowledge) | Drive partagé humains+agents | vault/MCP externe (pas natif) |
| Terminal-Bench | #1 (52%) | — |

Point notable : **Oz orchestre Claude Code lui-même** — Warp se positionne en couche méta au-dessus des CLI concurrentes, pas seulement en alternative.

## Liens

- [[Zach Lloyd]] — fondateur, thèses terminal-as-workbench
- [[Gemini CLI]] · [[Cursor]] · [[GitHub Copilot]] — autres environnements de dev IA
- [[harness-engineering]] — l'ADE = un harness produit packagé
- [[concevoir-loops-travail]] — le stade 3 (event-triggered) = un loop déclenché par événement
- [[MOC-Outils-IA]]
