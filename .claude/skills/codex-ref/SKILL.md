---
name: codex-ref
description: ALWAYS load when user asks about OpenAI Codex (the coding agent) — its AGENTS.md, config.toml, skills, hooks, subagents, loops, memory, or Codex vs Claude Code. Stable spine here; read MOC-Codex for detail, cc-news for anything newer. NOT for Claude Code features (cc-features-ref).
user-invocable: false
---

# OpenAI Codex — squelette de référence

_État au 15 juil. 2026. Cette skill embarque le SQUELETTE STABLE de Codex. Pour tout ce qui est VOLATIL (prix, versions, modèle défaut) : re-vérifier via `read_note("MOC-Codex")` ou la skill `cc-news`. Codex bouge chaque semaine._

Doctrine complète = 10 notes vault `04-Techniques/codex/` + `04-Techniques/chatgpt/`. Point d'entrée : `read_note("MOC-Codex")`.

## 3 prémisses souvent fausses (corrigées à la source)

- **Hooks Codex NE sont PAS expérimentaux** — stables depuis v0.124.0 (23 avril 2026). Levier de production.
- **`on-failure` (approbation) est DÉPRÉCIÉ** — valeurs actuelles : `untrusted | on-request | never`.
- **Défaut CLI = `gpt-5.6-sol`** (alias `gpt-5.6`), pas GPT-5-Codex (depuis GA 9 juil.).
- Bonus : doc officielle migrée `developers.openai.com/codex/*` → `learn.chatgpt.com/docs/*` (le `docs/config.md` du repo = stub).

## Surface Map — les 8 leviers (ordre d'application)

```
prompt → AGENTS.md → config.toml → skills → plugins → MCP → automations → hooks
```

| Levier | Rôle | Note vault |
|--------|------|-----------|
| AGENTS.md | conventions repo (≈ CLAUDE.md) | `agents-md-codex` |
| config.toml + profils | réglages machine, profils nommés | `config-toml-profils-codex` |
| Skills (`.agents/skills`) | how-to réutilisable | `comment-creer-skill-codex` |
| Subagents (`.codex/agents/*.toml`) | délégation parallèle | `subagents-cloud-codex` |
| MCP | accès données | `mcp-vs-skills-doctrine` |
| Automations / cloud | loops planifiés, exécution hébergée | `loops-codex` |
| Hooks | enforcement déterministe | `comment-creer-hook-codex` |
| Mémoire `[memories]` | compounding auto | `loop-apprentissage-codex` |

## Mécanismes stables (le noyau qui ne bouge pas)

- **AGENTS.md** : cap **32 KiB** (`project_doc_max_bytes`, taille combinée), nesting racine→CWD (concat root-first), `AGENTS.override.md` remplace le `.md` frère, global `~/.codex/AGENTS.md`. Section `## Review guidelines` pour la review PR.
- **config.toml / profils** : user `~/.codex/` vs projet `.codex/` (trusted) ; managé `requirements.toml` écrase tout. **Profils depuis 0.134.0 = 1 fichier par profil** (`~/.codex/<nom>.config.toml` + `--profile`) ; l'ancien `[profiles.NAME]` fait **crasher** au boot.
- **Skills** : `SKILL.md` sous `.agents/skills` (PAS `.claude/skills`), 4 scopes (REPO/USER/ADMIN/SYSTEM), frontmatter `name`+`description`, sidecar `agents/openai.yaml` (UI + `allow_implicit_invocation`), cap listing 2%/8000 chars. Noyau standard Agent Skills partagé avec CC mais **portabilité NON byte-identique**.
- **Subagents** : fichiers TOML `.codex/agents/*.toml`, champs `name`/`description`/`developer_instructions`, built-ins `default`/`worker`/`explorer`, `[agents] max_threads=6 max_depth=1`, effort 8 valeurs (ultra…none).
- **Hooks** : 10 events (2 scopes), config TOML `[[hooks.Event]]` + matcher, `type:"command"` seul exécuté. Blocage exit 2 ou `permissionDecision:"deny"`. **Piège `Stop` : `block` = CONTINUER (inversé vs Claude Code)**. `additionalContext` **non supporté sur PreToolUse**. **Trust model par hash** (hook modifié = skippé jusqu'à re-trust).
- **Loops** : `codex exec` (headless, `--json`, `--output-schema`, `CODEX_API_KEY` exec-only) ; automations planifiées RFC 5545 (équivalent natif du pattern Boris) ; CI `openai/codex-action@v1`.
- **Compounding** : mémoire auto `[memories]` (background, redaction secrets) + skills + scheduled task « scan sessions → update skills ». Pas de hook « auto-memory » dédié.

## Codex vs ChatGPT-app

Codex = agent de code (AGENTS.md/config/skills/hooks/subagents/exec). ChatGPT-app = conversationnel (custom instructions/Projects/mémoire native/GPTs). Leviers NON transférables. Détail : `read_note("codex-vs-chatgpt-seul")` + `read_note("personnalisation-chatgpt-app")`.

## Pour aller plus loin (pointeurs, 1 niveau)

- Détail complet : `read_note("MOC-Codex")` puis la note du levier concerné.
- Nouveautés postérieures au 15 juil. 2026 : skill `cc-news`.
- Setup d'un repo pour Codex (scaffolder AGENTS.md/config/skills) : **pas encore construit** — backlog, à créer quand un repo Neoteem passera réellement sous Codex.

## Gotchas

- Ne PAS confondre avec `cc-features-ref` (features Claude Code) ni `cc-news` (veille active).
- Ne PAS présumer l'identité Codex ↔ Claude Code : TOML vs markdown, `.agents/skills` vs `.claude/skills`, sémantique `Stop` inversée, trust model par hash absent de CC.
- Tout chiffre volatil (prix, context window, version) : cette skill ne le porte PAS — aller au vault ou cc-news.

## Apprentissage

_Aucune entrée pour le moment._
