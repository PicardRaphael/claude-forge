---
titre: "OpenAI Codex"
resume: "Agent de code d'OpenAI (CLI, IDE, desktop, cloud). CLI 0.157.0 au 25 sept. 2026 ; depuis GPT-6 Sol/Luna (22 sept.) la doc ne nomme plus de modèle par défaut (« uses a recommended model ») et recommande Sol pour le coding agentique, Luna pour le volume. GPT-5.5 retiré de Codex le 14 oct. 2026. Fiche produit versant industrie ; la doctrine actionnable vit dans le corpus 04-Techniques/codex via MOC-Codex."
aliases:
  - "OpenAI Codex"
  - "codex"
  - "codex openai"
  - "openai coding agent"
  - "codex cli"
  - "codex desktop"
  - "codex cloud"
domaine: openai
type: concurrent
derniere-maj: 2026-09-25
auteur: claude
sources:
  - "https://learn.chatgpt.com/docs/ (doc officielle Codex)"
  - "https://learn.chatgpt.com/docs/changelog (vérifié en primaire le 25 sept. 2026)"
  - "https://learn.chatgpt.com/docs/models"
  - "https://developers.openai.com/api/docs/changelog"
  - "https://github.com/openai/codex"
tags:
  - "#type/concurrent"
  - "#domaine/openai"
---

## Profil

Agent de code d'OpenAI, décliné en **CLI** (terminal, Rust), **extension IDE** (VS Code / Cursor / Windsurf), **application desktop** (devenue la nouvelle app ChatGPT le 9 juil. 2026), **cloud/web** (tâches hébergées parallèles) et **extension Chrome**. Facturation au token depuis le 2 avril 2026.

> ℹ️ **Cette fiche est le versant produit/concurrent.** La doctrine actionnable — comment travailler avec Codex — vit dans un corpus dédié : **[[MOC-Codex]]**, point d'entrée des notes `04-Techniques/codex/`. Ne pas dupliquer ici les mécanismes (nesting AGENTS.md, profils, subagents) : ils y sont vérifiés et datés.

## État au 25 septembre 2026

- **Modèle par défaut** : **plus de défaut nommé dans la doc**. Verbatim `learn.chatgpt.com/docs/models` : *« If you don't specify a model, the ChatGPT desktop app, Codex CLI, or IDE extension uses a recommended model »*. Recommandations : **GPT-6 Sol** pour le coding agentique complexe (effort de départ Medium), **GPT-6 Luna** pour le volume (High), Astra en Light. Des sources tierces disent `gpt-6-sol` défaut — non confirmé en primaire. Historique : `gpt-5.6-sol` du 9 juil. au 3 sept., puis `gpt-6-astra` bundled default en 0.153.4 (4 sept.). → Épingler le modèle dans `config.toml` si le choix compte.
- **Modèles** : `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna` (Sol/Luna sortis le 22 sept., API Responses **et** Chat Completions ; Sol : $2 / $0,20 cache / $10, contexte 1,05M, effort `none`→`max`, défaut `medium`), `gpt-5.6-sol` / `-terra` / `-luna`, `gpt-5.3-codex-spark`, `gpt-5.5`. **`gpt-5.5` retiré de ChatGPT, ChatGPT Work et Codex le 14 oct. 2026** sur tous les plans (remplacement conseillé : `gpt-6-sol`). `gpt-5.4` et `gpt-5.4-mini` retirés pour la connexion ChatGPT depuis le 31 août 2026. Dépréciés : `gpt-5.2`, `gpt-5.3-codex`.
- **CLI** : `0.157.0` (25 sept. 2026) — 0.156.0 (22 sept.), 0.156.1 (23 sept., Sol/Luna dans le sélecteur, le message de rate-limit recommande Luna), 0.157.0 (Sol/Luna sur Amazon Bedrock).
- **Doc officielle** : `learn.chatgpt.com/docs/` — les anciennes URL `developers.openai.com/codex/*` redirigent en 308. Le `docs/config.md` du repo GitHub est un stub.
- **Huit leviers de configuration** : AGENTS.md · config.toml/profils · skills (`.agents/skills`) · subagents (`.codex/agents/*.toml`) · MCP · automations/cloud · hooks (stables depuis v0.124.0) · mémoire `[memories]`. Un **marketplace de plugins en CLI** est apparu en 0.153.0 (3 sept.) — pas encore intégré à la Surface Map, à observer.
- **Modes de sandbox** : `read-only | workspace-write | danger-full-access`. **Approbation** : `untrusted | on-request | never` (`on-failure` déprécié).
- **Changements de comportement récents** : outil de planning **désactivé par défaut** (0.152.0, 1er sept.) ; un projet non-*trusted* ne fournit plus ses instructions `AGENTS.md` (0.150.0, 26 août) ; hooks **Interrupt** ajoutés (0.150.0).
- **Guide officiel « Rethinking skills and prompts for GPT-6 Astra »** (blog développeurs OpenAI, non daté, ~mi-sept.) : imposer une lecture de fichier avant chaque édition gaspille du contexte ; au-delà d'un certain nombre de skills, Codex raccourcit leurs descriptions ; les consignes « lance les tests » sont redondantes car Astra vérifie de lui-même ; définir « terminé » avant de démarrer. À confronter au corpus [[MOC-Codex]] avant toute règle.

## Comparaison avec Claude Code (au 25 septembre 2026)

| | Codex | Claude Code |
|---|---|---|
| Modèle par défaut | « recommended model » non nommé (Sol recommandé) | `claude-opus-5-5` (Fable 5.1 en step-up) |
| Format d'agent | TOML (`.codex/agents/*.toml`) | Markdown + frontmatter YAML |
| Instructions projet | `AGENTS.md` (nesting racine→CWD, cap combiné) | `CLAUDE.md` (imports `@path`) ; lit `AGENTS.md` si aucun `CLAUDE.md` (v2.1.277) |
| Parallélisme déclaratif | `max_threads` / `max_depth` | pas d'équivalent déclaratif ; `/batch` en fan-out |
| Computer use | natif macOS | via MCP |
| Multi-agent | subagents + cloud tasks | subagents, Agent Teams (expérimental, off par défaut) |
| MCP | natif | natif |
| Worktrees | non documenté | natif |
| Planification récurrente | automations (RRULE, web/desktop) | `/schedule` |

⚠️ Les lignes de ce tableau reflètent l'état vérifié à la date du titre. Les comparaisons de volumétrie (nombre de plugins, utilisateurs hebdomadaires) ont été **retirées** : les chiffres portés par cette fiche depuis mai 2026 (111 plugins, 3M utilisateurs/semaine) n'ont jamais été recroisés et une comparaison chiffrée non datée vieillit mal.

## Tarifs

Prix API relevés au **15 juillet 2026**, non reconfirmés depuis ($/1M, contexte court) : Sol 5.6 5/30 · Terra 2.5/15 · Luna 1/6 · GPT-5-Codex 1.25/10 (contexte 400K). Confirmés en primaire le **25 sept. 2026** : **GPT-6 Astra $10 / $1 cache / $50**, **GPT-6 Sol $2 / $0,20 / $10** ; au-delà de 272K tokens d'entrée, toute la requête passe à ×2 input/cache et ×1,5 output (cf [[GPT-6 Astra]]). GPT-6 Luna ($0,10 / $0,01 / $0,50) : repris du changelog API, fiche modèle non consultée.

## Historique

État antérieur de cette fiche, conservé comme trace datée — **ne pas lire comme l'état courant** :

- **Avril 2026** : « mega update » du 17 avril (computer use, plugins, navigateur intégré, multi-agent) ; GPT-Rosalind (life sciences) le 16 avril. Classification « High capability » cybersécurité au Preparedness Framework. GPT-5.3 présenté comme premier modèle instrumental dans sa propre création.
- **Mai 2026** : `codex remote-control` (app-server headless), auth Bedrock, pièces jointes image dans le CLI, mid-turn steering, extension Chrome, workspace agents. **GPT-5.5 remplace GPT-5.4** comme modèle principal.
- **Juillet 2026** : GA de GPT-5.6 le 9 juil., famille Sol/Terra/Luna, `gpt-5.6-sol` devient le défaut CLI ; sunset des modèles legacy le 23 juil. ; migration de la doc vers `learn.chatgpt.com`.
- **Septembre 2026 (1re quinzaine)** : GPT-6 Astra (3 sept.) devient le défaut bundled en CLI 0.153.4 (4 sept.) ; marketplace de plugins CLI (0.153.0).

⚠️ **Trou de couverture connu** : le changelog Codex de **mars à juillet 2026** n'a pas pu être récupéré en source primaire lors de la vérification du 5 sept. — les faits de cette période viennent des vérifications de juillet.

## Liens

- [[MOC-Codex]] — point d'entrée de la doctrine Codex
- [[workflow-codex-optimal]] — note maître du workflow
- [[codex-vs-chatgpt-seul]] — arbitrage Codex / app ChatGPT
- [[GPT-6 Astra]] — flagship GPT-6
- [[GitHub Copilot]] · [[Cursor]] — concurrents
- [[MOC-Outils-IA]]
