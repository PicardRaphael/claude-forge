---
name: codex-ref
description: ALWAYS load when user asks about OpenAI Codex (the coding agent) — AGENTS.md, config.toml, skills, plugins, hooks, subagents, automations, memory, or Codex vs Claude Code/ChatGPT. Use official OpenAI docs for volatile facts and cc-news for newer. NOT for Claude Code features (cc-features-ref).
---

# OpenAI Codex — squelette de référence

_Vérifié le 27 août 2026 contre la documentation officielle OpenAI. Cette skill embarque le SQUELETTE STABLE de Codex. Pour tout ce qui est VOLATIL (prix, versions, modèle recommandé, disponibilité par plan) : re-vérifier la documentation officielle puis confronter `read_note("MOC-Codex")`. Codex bouge chaque semaine._

Doctrine complète = 10 notes vault `04-Techniques/codex/` + `04-Techniques/chatgpt/`. Point d'entrée : `read_note("MOC-Codex")`.

## Prémisses souvent fausses (corrigées à la source)

- **Hooks Codex NE sont PAS expérimentaux** — 11 événements documentés et handlers `command` + `mcp_tool`; les hooks non managés restent soumis à review/trust.
- **`on-failure` (approbation) est DÉPRÉCIÉ** — utiliser `untrusted | on-request | never`, ou la forme granulaire documentée quand seuls certains prompts doivent rester interactifs.
- **Le modèle n'est pas un invariant** — au 27 août, le réglage recommandé « Power » utilise `gpt-5.6-sol` avec effort medium et `gpt-5.6` route vers Sol ; re-vérifier avant toute recommandation durable.
- **Mémoire locale ≠ mémoire ChatGPT** — elle est désactivée par défaut, s'active avec `[features] memories = true`, se contrôle par chat via `/memories` et se met à jour en arrière-plan, donc pas nécessairement dès la fin du chat.
- La documentation Codex canonique est sous `learn.chatgpt.com/docs/*`; les plugins restent documentés sous `developers.openai.com/plugins/*`.

## Surface Map — leviers (ordre d'application)

```
prompt → AGENTS.md → config.toml → skills/plugins → MCP/apps → agents → automations → hooks → memories
```

| Levier | Rôle | Note vault |
|--------|------|-----------|
| AGENTS.md | conventions globales et repo, imbriquées jusqu'au CWD | `agents-md-codex` |
| config.toml + profils | réglages machine, profils nommés | `config-toml-profils-codex` |
| Skills (`.agents/skills`) | how-to réutilisable | `comment-creer-skill-codex` |
| Plugins | distribution de skills, MCP, hooks et assets | `MOC-Codex` |
| Subagents (`.codex/agents/*.toml`) | délégation parallèle | `subagents-cloud-codex` |
| MCP | accès données | `mcp-vs-skills-doctrine` |
| Automations | tâches planifiées ou déclenchées par événements | `loops-codex` |
| Hooks | enforcement déterministe | `comment-creer-hook-codex` |
| Mémoire locale | rappel optionnel et asynchrone | `loop-apprentissage-codex` |

## Mécanismes stables (le noyau qui ne bouge pas)

- **AGENTS.md** : cap **32 KiB** combiné par défaut (`project_doc_max_bytes`), découverte globale puis racine→CWD, un fichier par niveau ; `AGENTS.override.md` remplace le `AGENTS.md` frère. Pour la review GitHub, utiliser `## Code Review Rules`.
- **config.toml / profils** : user `~/.codex/config.toml` puis projet `.codex/config.toml` si trusted ; `requirements.toml` contraint les réglages sensibles. Depuis 0.134.0, un profil est `~/.codex/<nom>.config.toml` sélectionné par `--profile`; les anciennes tables `[profiles.NAME]` ne sont plus lues, elles ne sont pas un format valide à conserver.
- **Permissions** : sandbox et approbation restent séparés. `--approve-for-me` / `approvals_reviewer = "auto_review"` délègue l'examen d'approbations éligibles sans élargir les droits filesystem ou réseau.
- **Skills** : `SKILL.md` sous `.agents/skills` (PAS `.Codex/skills`), 4 scopes REPO/USER/ADMIN/SYSTEM, frontmatter `name`+`description`, sidecar `agents/openai.yaml` (UI, dépendances, `allow_implicit_invocation`), budget initial 2% du contexte ou 8 000 caractères. Le user scope canonique est `$HOME/.agents/skills`.
- **Plugins** : format de distribution portable pour skills, MCP, hooks et assets. Le CLI sait parcourir des catalogues local/personnel/workspace/distant ; `/import` importe les éléments supportés depuis Claude Code ou Cursor. Ne pas confondre import et synchronisation continue.
- **Subagents** : agents built-in `default`/`worker`/`explorer`; agents personnels `~/.codex/agents/*.toml` ou projet `.codex/agents/*.toml`, avec `name`/`description`/`developer_instructions`. `[agents]` expose notamment `enabled`, `max_concurrent_threads_per_session`, `default_subagent_model`, `default_subagent_reasoning_effort`; `max_threads` n'est plus qu'un alias legacy et `max_depth` n'est pas dans le schéma public actuel.
- **Hooks** : 11 événements (`SessionStart`, `SubagentStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop`, `SessionEnd`), sources JSON ou TOML, handlers `command` et `mcp_tool`. `PreToolUse` sait bloquer, ajouter `additionalContext` et réécrire `updatedInput`. **Piège `Stop` : `decision:"block"` = CONTINUER**. Toute définition non managée modifiée doit être re-trustée.
- **Automations** : `codex exec` reste le mode headless (`--json`, `--output-schema`; clé via `CODEX_API_KEY` pour l'automatisation). Les tâches planifiées se créent/gèrent depuis ChatGPT web ou l'app desktop, pas depuis le CLI/IDE ; l'app locale peut cibler checkout ou worktree, et le web supporte désormais les triggers Gmail/Slack/GitHub. CI : `openai/codex-action@v1`.
- **Mémoire** : store local séparé de ChatGPT sous `~/.codex/memories/`, généré de façon différée. `[features] memories = true` active la fonctionnalité ; `memories.generate_memories` et `memories.use_memories` séparent écriture et lecture. Garder les règles obligatoires dans AGENTS.md ou la documentation versionnée.
- **Intégration** : `codex mcp-server` est déprécié pour embarquer Codex dans une application ; utiliser le Codex app server.

## Codex vs ChatGPT-app

Codex = agent de code (AGENTS.md/config/skills/hooks/subagents/exec). ChatGPT-app = conversationnel (custom instructions/Projects/mémoire native/GPTs). Leviers NON transférables. Détail : `read_note("codex-vs-chatgpt-seul")` + `read_note("personnalisation-chatgpt-app")`.

## Pour aller plus loin (pointeurs, 1 niveau)

- Détail complet : `read_note("MOC-Codex")` puis la note du levier concerné.
- Nouveautés postérieures au 27 août 2026 : documentation officielle OpenAI, puis skill `cc-news` pour la veille.
- Setup d'un repo pour Codex (scaffolder AGENTS.md/config/skills) : **pas encore construit** — backlog, à créer quand un repo Neoteem passera réellement sous Codex.

## Sources officielles vérifiées

- [What's new](https://learn.chatgpt.com/docs/whats-new)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
- [Memories](https://learn.chatgpt.com/docs/customization/memories)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations)

## Gotchas

- Ne PAS confondre avec `cc-features-ref` (features Codex) ni `cc-news` (veille active).
- Ne PAS présumer l'identité Claude Code ↔ Codex : TOML vs markdown, `.agents/skills` vs `.claude/skills`, sémantique `Stop` et trust model différents.
- Tout chiffre volatil (prix, context window, version) : cette skill ne le porte PAS — aller au vault ou cc-news.

## Apprentissage

_Aucune entrée pour le moment._
