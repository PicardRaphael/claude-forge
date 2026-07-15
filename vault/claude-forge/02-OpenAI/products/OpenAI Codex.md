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
- [[MOC-Outils-IA]]


## Mises à jour mai 2026

- **Remote control mode** : `codex remote-control` pour app-server headless
- **Bedrock auth** : credentials AWS console-login
- **Image attachments** : screenshots/wireframes dans le CLI
- **Mid-turn steering** : rediriger le comportement en temps réel
- **Chrome extension** : fonctionne avec apps/sites dans le browser, parallèle multi-tabs
- **Workspace agents** : agents répétables pour workflows entreprise (ChatGPT + Slack)
- **GPT-5.5** remplace GPT-5.4 comme modèle principal

## Mise à jour 15 juillet 2026 (doctrine Codex forge)

> Cette fiche produit (versant industrie/concurrent) date de mai 2026 (GPT-5.4/5.5) et reste un instantané historique. L'état verrouillé au **15 juil. 2026** et la doctrine actionnable vivent désormais dans un corpus dédié : **[[MOC-Codex]]** (10 notes 04-Techniques/codex/ + [[personnalisation-chatgpt-app]]).

État verrouillé (sources primaires 15/07/2026) :
- **Modèle défaut CLI** : `gpt-5.6-sol` (alias `gpt-5.6`, preset Power medium) depuis la GA GPT-5.6 du 9 juil. Famille **Sol/Terra/Luna**. Dépréciés : gpt-5.2, gpt-5.3-codex. Sunset legacy 23 juil.
- **CLI** `0.144.4` (14 juil.). Doc officielle migrée : `developers.openai.com/codex/*` → redirige `learn.chatgpt.com/docs/*` ; `docs/config.md` du repo = stub.
- **8 leviers** : AGENTS.md · config.toml/profils · skills (`.agents/skills`) · subagents (`.codex/agents/*.toml`) · MCP · automations/cloud · hooks (stables v0.124.0) · mémoire `[memories]`.
- Prix API (short ctx, $/1M) : Sol 5/30 · Terra 2.5/15 · Luna 1/6 · GPT-5-Codex 1.25/10 (ctx 400K).

Point d'entrée doctrine : [[MOC-Codex]] · [[workflow-codex-optimal]] · [[codex-vs-chatgpt-seul]].
