---
titre: "Gemini CLI"
resume: "CLI IA Google, open-source Apache 2.0 — service coupé le 18 juin 2026 pour les comptes INDIVIDUELS uniquement (entreprise et clés API payantes conservées). Remplacé par Antigravity CLI + Antigravity 2.0, non open-source."
aliases:
  - "gemini cli"
  - "gemini-cli"
  - "google gemini cli"
  - "gemini terminal"
  - "gemini coding agent"
  - "antigravity cli"
  - "antigravity 2.0"
domaine: gemini
type: concurrent
derniere-maj: 2026-09-05
auteur: claude
sources:
  - "https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/"
  - "https://github.com/google-gemini/gemini-cli"
  - "https://geminicli.com/docs/changelogs/latest/"
tags:
  - "#type/concurrent"
  - "#domaine/gemini"
---

## Statut au 5 septembre 2026 — transition vers Antigravity

> ⚠️ **Ni mort, ni pleinement vivant.** La nuance compte, et une lecture rapide se trompe dans les deux sens.

- **18 juin 2026** : Gemini CLI et les extensions IDE Gemini Code Assist **cessent de servir les requêtes** — verbatim : *« On June 18, 2026, Gemini CLI and Gemini Code Assist IDE extensions will stop serving requests for Google AI Pro and Ultra, as well as those using it free of charge »*. La coupure vise donc **les comptes individuels** : Google AI Pro, Google AI Ultra, et l'usage gratuit.
- **Conservent l'accès** : les entreprises sous licence Gemini Code Assist Standard/Enterprise ou via Google Cloud, et les détenteurs de **clés API payantes** Gemini / Gemini Enterprise Agent Platform.
- **Le dépôt GitHub reste public et actif** (Apache 2.0, ~107k stars), sans bannière d'archivage. En déduire « projet mort » depuis GitHub seul est une erreur de lecture : c'est le **service backend gratuit** qui s'est arrêté, pas le code.
- **Remplaçants officiels** : **Antigravity CLI** (terminal) et **Antigravity 2.0** (application desktop), qui *« share the same agent architecture »*.
- ⚠️ **Antigravity CLI n'est PAS open-source**, contrairement à Gemini CLI — ce qui a provoqué un backlash développeur (The Register, 20 mai 2026).

## Profil (état historique du produit)

CLI IA de Google pour le développement. Open source Apache 2.0, YOLO mode par défaut, 1M+ tokens par agent.

## Features clés

- **Chapters** (v0.38.1) — Groupement thématique des conversations
- **Context Compression Service** — Compression contexte intelligent
- **Terminal Buffer mode** — Buffer terminal dédié
- **Subagents** — YAML frontmatter (même pattern que Claude Code), `~/.gemini/agents`, remote via A2A
- **Code Customization** — Repos privés indexés, étendu au CLI et Agent Mode
- **YOLO mode** par défaut (auto-approve tout)

## Historique des versions (avant la transition)

- **v0.42.0-preview.2** (6 mai) : Auto Memory inbox flow, `--delete` flag sur `/exit`, `/bug-memory`, [[Gemma 4]] activé par défaut
- **v0.41.0** (stable) : Real-time Voice Mode (cloud + local)
- **v0.40.0** (28 avril) : Bundled ripgrep, GitHub-style colorblind themes, MCP resource tools, four-tier prompt-driven memory, Gemma local setup simplifié
- **v0.39.0-preview** (14 avril) : Subagents refactorisés en `invoke_subagent` unique, `/memory inbox` pour skill extraction, Plan Mode avec confirmation skill
- **v0.38.0** (14 avril) : Chapters Narrative Flow, Context Compression Service, `/memory inbox`, ContextManager architecture découplée, fix memory leaks + PTY exhaustion
- **v0.38.1** (16 avril) : Bugfixes MCP progress leak, Ctrl+G, Gemini 3 dispo pour tous
- **v0.37.1** (9 avril) : Sandbox dynamique, worktrees, Chapters, browser agent
- **Subscriptions** : AI Pro = 5x limites, AI Ultra = 20x limites (partagées CLI + Code Assist)

## Comparaison avec Claude Code

| Feature | Gemini CLI (→ Antigravity) | Claude Code |
|---------|-----------|-------------|
| Context | 1M+ tokens/agent | 200K–1M |
| Subagents | YAML frontmatter | YAML frontmatter |
| Auto-approve | YOLO mode défaut | Permission system |
| Licence | Apache 2.0 → **Antigravity non-OSS** | Propriétaire |
| Accès individuel | **Coupé le 18 juin 2026** | Actif |

## Correction du 5 septembre 2026

Deux assertions actives de cette note étaient fausses et ont été remplacées :

1. **« Google I/O 2026 (19 mai) : Gemini 4.0 major update attendu »** → faux. L'annonce phare de l'I/O 2026 était **Gemini 3.5 Flash**, pas Gemini 4.0. Gemini 4.0 n'a **aucune date de sortie annoncée** au 5 sept. 2026. Cf [[MOC-Modeles]] § Google.
2. La note décrivait le CLI comme pleinement actif, sans mentionner la coupure du 18 juin ni la transition Antigravity — corrigé ci-dessus.

## Liens

- [[MOC-Outils-IA]]
- [[MOC-Modeles]] — catalogue Gemini réel et dépréciations
- [[Gemma 4]] — modèle open-source Google
