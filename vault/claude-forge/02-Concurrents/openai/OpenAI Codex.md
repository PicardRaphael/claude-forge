---
titre: "OpenAI Codex"
resume: "Agent coding OpenAI — GPT-5.4, computer use macOS, 111 plugins, 3 modes, subagents, 3M devs/semaine"
aliases:
  - "OpenAI Codex"
  - "codex"
  - "codex openai"
  - "openai coding agent"
  - "GPT-5.3 Codex"
  - "gpt 5.3 codex"
  - "codex cli"
domaine: openai
type: concurrent
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.buildfastwithai.com/blogs/openai-codex-for-almost-everything-2026"
  - "https://www.startuphub.ai/ai-news/tech/2026/gpt-5-3-codex-powers-github-copilot-cursor"
tags:
  - "#type/concurrent"
  - "#domaine/openai"
---

## Profil

CLI IA d'OpenAI pour le développement. 3M utilisateurs/semaine (+1M/mois). Premier modèle instrumental dans sa propre création (GPT-5.3). Classifié "High capability" cybersécurité (Preparedness Framework).

## Features clés

- **Trois modes** : Read-only / Auto / Full Access
- **Computer Use** sur macOS (contrôle desktop apps)
- **111 plugins** natifs (GitHub/Slack/Notion/Google/GitLab/Atlassian/CircleCI)
- **Subagents** : multi-agent workflows (write/debug/test en parallèle)
- **MCP support** : outils tiers via terminal
- **Mémoire inter-sessions** (contexte persistant)
- **Navigateur intégré** avec commenting + image gen (gpt-image-1.5)
- **Local code review** : scan changes avant PR
- **GPT-5.4** + **GPT-5.3-Codex-Spark** (1000+ tok/s sur Cerebras)
- Context 1M tokens = plan Pro $200/mo (Plus $20 = fenêtre réduite)
- Token-based billing depuis 2 avril 2026

## Dernières mises à jour

- **17 avril** : Mega update — computer use, plugins, browser, multi-agent
- **16 avril** : GPT-Rosalind (life sciences), Agents SDK update

## Comparaison avec Claude Code

| Feature | Codex | Claude Code |
|---------|-------|-------------|
| Computer Use | macOS natif | Via MCP |
| Plugins | 111 natifs | 2500+ marketplace |
| Multi-agent | Subagents parallèles | Agent Teams |
| MCP | Support natif | Support natif |
| Modèle | GPT-5.4 | Opus 4.7 |
| Worktrees | Non | Natif (`claude -w`) |
| Tooling CLI | Basique | /loop, /schedule, /batch |
| Users | 3M/semaine | Non communiqué |

## Liens

- [[GitHub Copilot]]
- [[Cursor]]
- [[MOC-Concurrents]]


## Mises à jour mai 2026

- **Remote control mode** : `codex remote-control` pour app-server headless
- **Bedrock auth** : credentials AWS console-login
- **Image attachments** : screenshots/wireframes dans le CLI
- **Mid-turn steering** : rediriger le comportement en temps réel
- **Chrome extension** : fonctionne avec apps/sites dans le browser, parallèle multi-tabs
- **Workspace agents** : agents répétables pour workflows entreprise (ChatGPT + Slack)
- **GPT-5.5** remplace GPT-5.4 comme modèle principal
