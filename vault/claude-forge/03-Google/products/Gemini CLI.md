---
titre: "Gemini CLI"
resume: "CLI IA Google, chapters, subagents YAML, context compression, 1M+ tokens/agent"
aliases:
  - "gemini cli"
  - "gemini-cli"
  - "google gemini cli"
  - "gemini terminal"
  - "gemini coding agent"
domaine: gemini
type: concurrent
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "https://geminicli.com/docs/changelogs/latest/"
tags:
  - "#type/concurrent"
  - "#domaine/gemini"
---

## Profil

CLI IA de Google pour le developpement. Open source, YOLO mode par defaut, 1M+ tokens par agent.

## Features clés

- **Chapters** (v0.38.1) — Groupement thématique des conversations
- **Context Compression Service** — Compression contexte intelligent
- **Terminal Buffer mode** — Buffer terminal dédié
- **Subagents** — YAML frontmatter (même pattern que Claude Code), `~/.gemini/agents`, remote via A2A
- **Code Customization** — Repos privés indexés, étendu au CLI et Agent Mode
- **YOLO mode** par défaut (auto-approve tout)

## Dernières mises à jour

- **v0.39.0-preview** (14 avril) : Subagents refactorisés en `invoke_subagent` unique, `/memory inbox` pour skill extraction, Plan Mode avec confirmation skill
- **v0.38.0** (14 avril) : Chapters Narrative Flow, Context Compression Service, `/memory inbox`, ContextManager architecture découplée, fix memory leaks + PTY exhaustion
- **v0.38.1** (16 avril) : Bugfixes MCP progress leak, Ctrl+G, Gemini 3 dispo pour tous
- **v0.37.1** (9 avril) : Sandbox dynamique, worktrees, Chapters, browser agent
- **Code Assist intégration** : code customization supportée en CLI + agent mode, persistent memory sur GitHub, `/deploy` Cloud Run depuis agent mode
- **Subscriptions** : AI Pro = 5x limites, AI Ultra = 20x limites (partagées CLI + Code Assist)

## Comparaison avec Claude Code

| Feature | Gemini CLI | Claude Code |
|---------|-----------|-------------|
| Context | 1M+ tokens/agent | 200K-1M |
| Subagents | YAML frontmatter | YAML frontmatter |
| Auto-approve | YOLO mode défaut | Permission system |
| Plugins | Pas de marketplace | 2500+ plugins |
| Skills | Skills in Chrome | Skills in CLI |

## Liens

- [[MOC-Outils-IA]]


## Mises à jour mai 2026

- **v0.42.0-preview.2** (6 mai) : Auto Memory inbox flow, `--delete` flag sur `/exit`, `/bug-memory`, [[Gemma 4]] activé par défaut
- **v0.41.0** (stable) : Real-time Voice Mode (cloud + local)
- **v0.40.0** (28 avril) : Bundled ripgrep, GitHub-style colorblind themes, MCP resource tools, four-tier prompt-driven memory, Gemma local setup simplifié
- **Google I/O 2026** (19 mai) : Gemini 4.0 major update attendu
