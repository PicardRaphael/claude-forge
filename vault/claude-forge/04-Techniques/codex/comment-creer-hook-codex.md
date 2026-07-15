---
titre: "Hooks Codex — moteur stable, 10 events, contrat, parité partielle vs Claude Code"
resume: "Note canonique forge — les hooks OpenAI Codex : STABLES depuis v0.124.0 (23 avril 2026, plus expérimentaux), 10 events en 2 scopes, config TOML par blocs hooks.Event, contrat JSON stdin + exit 2/permissionDecision, piège Stop (block=continue), gap additionalContext sur PreToolUse, trust model par hash. Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "hooks codex"
  - "creer hook codex"
  - "codex hooks events"
  - "codex hook trust model"
  - "additionalContext PreToolUse codex"
  - "hooks codex vs claude code"
  - "allow_managed_hooks_only"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/hooks (ex developers.openai.com/codex/hooks, redirect 308)"
  - "https://github.com/openai/codex/releases/tag/rust-v0.124.0 (hooks stable)"
  - "https://github.com/openai/codex/releases/tag/rust-v0.129.0 (/hooks TUI + trust model)"
  - "https://github.com/openai/codex/issues/19385 (parité partielle vs Claude Code)"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/hooks"
  - "#doctrine/2026"
---
# Hooks Codex — moteur stable, 10 events, parité partielle vs Claude Code

> Note canonique forge — les hooks Codex injectent des scripts dans la boucle agentique (logging, blocage, validation, injection de contexte). Vérifié sur `learn.chatgpt.com/docs/hooks` + release tags au **15 juil. 2026**. Mécanismes propres à Codex — ne pas présumer la sémantique Claude Code.

---

## CORRECTION DE PRÉMISSE — les hooks NE SONT PLUS expérimentaux

Une croyance répandue (et le hedge initial de ce chantier) : « hooks Codex expérimentaux, start/stop seulement ». **C'était vrai jusqu'en avril 2026, périmé depuis.** Timeline (release tags GitHub) :

| Version | Date | État |
|---------|------|------|
| v0.114.0 | 11 mars 2026 | moteur **expérimental**, `SessionStart` + `Stop` seulement |
| v0.116.0 | 19 mars 2026 | + `UserPromptSubmit` (*probable*, source secondaire) |
| **v0.124.0** | **23 avril 2026** | **STABLE** — « Hooks are now stable, can be configured inline in `config.toml` and managed `requirements.toml`, and can observe MCP tools as well as `apply_patch` and long-running Bash sessions. » |
| v0.129.0 | 7 mai 2026 | `/hooks` browser TUI + trust model par hash + hooks avant/après compaction + `PreToolUse` context |

**Stable ≠ figé** : plusieurs champs restent « parsed but not implemented » (`async`, `suppressOutput`, `updatedMCPToolOutput`), et des events continuent d'arriver. Traiter les hooks Codex comme un **levier réel de production**, pas un jouet.

---

## COMMENT — 10 events, 2 scopes (CERTAIN)

> Verbatim : « `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, and `Stop` run at turn scope. `SessionStart` and `SubagentStart` run at thread or subagent-start scope. »

| Event | Scope |
|-------|-------|
| `SessionStart`, `SubagentStart` | thread / subagent-start |
| `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop` | turn (reçoivent un `turn_id` sur stdin) |

---

## COMMENT — Configuration (config.toml, CERTAIN)

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"
```

- `matcher` = regex sur le nom d'outil.
- `type = "command"` = **seul type exécuté** aujourd'hui (`prompt`/`agent` parsés puis skippés).
- `timeout` en **secondes**, défaut **600** si omis.
- `command_windows` / `commandWindows` : override Windows.
- Codex accepte aussi la « Claude-style hook config shape » (`hooks.json`), d'où l'impression de portabilité — mais sans parité complète (cf infra).

---

## COMMENT — Contrat entrée/sortie (CERTAIN)

**Entrée** : JSON sur stdin — `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode` (+ `turn_id` en turn scope).

**Bloquer une action** — deux mécanismes :
1. Exit code `2` + raison sur stderr.
2. JSON structuré sur stdout :
```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Destructive command blocked." } }
```
`PermissionRequest` : `decision.behavior` = `allow`/`deny` ; **« any deny wins »** si plusieurs hooks répondent.

**Réécrire l'input d'un outil** (`PreToolUse` only) : `updatedInput`.

**Injecter du contexte** : texte stdout (developer context) sur `SessionStart`/`SubagentStart`/`UserPromptSubmit`, ou champ `additionalContext`.

### ⚠️ Deux pièges de sémantique (à ne PAS présumer depuis Claude Code)

- **`Stop` inversé** : « For `Stop`, `decision: "block"` doesn't reject the turn — it tells Codex to continue, using `reason` as a new continuation prompt. » → sur `Stop`, `block` = **forcer la continuation**, pas arrêter. (Corollaire forge : si on porte un jour un Stop hook forge vers Codex — learning-reminder, anti-rationalization — la sémantique `block` s'INVERSE. Nos hooks forge tournant sous Claude Code ne sont pas affectés en l'état.)
- **`additionalContext` sur `PreToolUse` = NON supporté** : erreur dure « PreToolUse hook returned unsupported additionalContext ». Supporté sur `SessionStart`/`UserPromptSubmit`/`PostToolUse` seulement. **`PreToolUse` en Codex = guardrail/blocage, PAS injection de contexte** — contrairement à Claude Code. C'est le gap de parité le plus notable.

---

## COMMENT — Trust model par hash (CERTAIN, absent de Claude Code)

Depuis v0.129.0 : « Codex records trust against the hook's current hash, so new or changed hooks are marked for review and skipped until trusted. » Un hook nouveau ou modifié est **skippé tant que non trusté** — durcissement de sécurité que Claude Code n'a pas. Bypass : `--dangerously-bypass-hook-trust`. `/hooks` (TUI) pour parcourir/toggler.

---

## COMMENT — Managed hooks (requirements.toml)

```toml
allow_managed_hooks_only = true      # UNIQUEMENT dans requirements.toml (sans effet en config.toml)

[hooks]
managed_dir = "/enterprise/hooks"

[[hooks.PreToolUse]]
matcher = "^Bash$"
[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
timeout = 30
```
Managed hooks « can't be disabled from the user hook browser ». Codex ne distribue PAS les scripts (l'outillage enterprise les installe). Désactiver tout : `[features] hooks = false`.

---

## Cas d'usage officiels (CERTAIN)

Logging/analytics · bloquer des clés API accidentellement pastées · **résumer les conversations en mémoires persistantes** (cas d'usage, PAS un event dédié — à câbler soi-même, cf [[loop-apprentissage-codex]]) · validation au turn-stop · customiser le prompt selon le répertoire.

---

## Hooks Codex vs Claude Code (synthèse)

| Aspect | Codex | Claude Code |
|--------|-------|-------------|
| Config | TOML `[[hooks.Event]]` (+ `hooks.json` Claude-style accepté) | JSON settings.json |
| Events | 10 (ajoute `PermissionRequest`, `PostCompact`, `SubagentStart`, `SubagentStop`) | ~ mêmes noms de base |
| `additionalContext` sur PreToolUse | ❌ non supporté (guardrail only) | ✅ supporté |
| `Stop` `block` | = **continuer** (sémantique inversée) | = bloquer l'arrêt (cf hooks forge) |
| Trust model | par hash (skip tant que non trusté) | absent |
| Parité champs de sortie | **incomplète** (verbatim issue #19385) | référence |

*À vérifier* : diff event-par-event exhaustif (cette synthèse s'appuie sur l'issue OpenAI #19385, pas un fetch frais de la doc Anthropic — croiser avec [[comment-creer-hook]] pour un diff bilatéral).

---

## ANTI-PATTERNS

- ❌ **Traiter les hooks Codex comme « expérimentaux »** — stables depuis v0.124.0 (23 avril).
- ❌ **Présumer la sémantique `Stop` de Claude Code** — en Codex, `block` = continuer.
- ❌ **Injecter du contexte via `additionalContext` sur `PreToolUse`** — non supporté, erreur dure.
- ❌ **Compter sur `type: prompt`/`agent`, `async`, `suppressOutput`** — parsés, pas implémentés.
- ❌ **`allow_managed_hooks_only` dans config.toml** — requirements.toml only.
- ❌ **Oublier le trust model** — un hook modifié est skippé jusqu'à re-trust.

---

## SOURCES

- `learn.chatgpt.com/docs/hooks` (15/07/2026).
- Release tags `rust-v0.114.0` (naissance), `rust-v0.124.0` (stable), `rust-v0.129.0` (TUI + trust).
- `github.com/openai/codex/issues/19385` (parité partielle vs Claude Code).

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître (Surface Map)
- [[config-toml-profils-codex]] — où les hooks sont configurés + requirements.toml
- [[comment-creer-hook]] — hooks Claude Code (miroir + doctrine 22 mai advisory)
- [[loop-apprentissage-codex]] — le « summarize→memory » n'est pas un event, se câble via Stop/PostCompact
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine forge : hooks lint/security/scope, jamais workflow agentique
