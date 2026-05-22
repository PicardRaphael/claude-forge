---
titre: "Vérification — Hooks Claude Code doc officielle Anthropic (events, timeouts, PostCompact)"
resume: "Liste verbatim des hook events officiels, timeouts chiffrés, vérification PostCompact, exit codes, payloads"
aliases:
  - "verif hooks officielle"
  - "hooks anthropic doc"
  - "postcompact hook"
  - "timeout hook agent"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/verification"
  - "#domaine/claude-code"
  - "#technique/hooks"
---

# Vérification — Hooks Claude Code doc officielle

**Source primaire** : https://code.claude.com/docs/en/hooks (redirect canonique depuis docs.claude.com)
**Guide complémentaire** : https://code.claude.com/docs/en/hooks-guide
**Date vérif** : 2026-05-22

## 1. Liste OFFICIELLE et VERBATIM des hook events (29 events)

Extrait verbatim de la table "Hook lifecycle" :

1. `SessionStart`
2. `Setup`
3. `UserPromptSubmit`
4. `UserPromptExpansion`
5. `PreToolUse`
6. `PermissionRequest`
7. `PermissionDenied`
8. `PostToolUse`
9. `PostToolUseFailure`
10. `PostToolBatch`
11. `Notification`
12. `SubagentStart`
13. `SubagentStop`
14. `TaskCreated`
15. `TaskCompleted`
16. `Stop`
17. `StopFailure`
18. `TeammateIdle`
19. `InstructionsLoaded`
20. `ConfigChange`
21. `CwdChanged`
22. `FileChanged`
23. `WorktreeCreate`
24. `WorktreeRemove`
25. `PreCompact`
26. `PostCompact`
27. `Elicitation`
28. `ElicitationResult`
29. `SessionEnd`

→ **29 events officiels** (la rumeur "25+" est correcte, plus précisément 29).

## 2. Limites techniques (timeouts)

Verbatim "Common fields" :

> `timeout` | no | Seconds before canceling. **Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`.** `UserPromptSubmit` lowers the `command`, `http`, and `mcp_tool` default to 30

| Type de hook | Timeout défaut |
|---|---|
| `command` | 600 s (30 s sur `UserPromptSubmit`) |
| `http` | 600 s (30 s sur `UserPromptSubmit`) |
| `mcp_tool` | 600 s (30 s sur `UserPromptSubmit`) |
| `prompt` | 30 s |
| **`agent`** | **60 s** |

**Réponse claim vague 2** : timeout agent hook = **60 secondes**. La doc officielle **NE MENTIONNE PAS** de limite en "tool-use turns" (50 ou autre). Si Boris/un rapport l'a évoqué, ce n'est pas dans la doc officielle visible. Le seul plafond documenté est temporel (60 s).

## 3. Vérification `PostCompact`

**OUI, `PostCompact` existe officiellement.** Verbatim doc :

- Table events : `| PostCompact | After context compaction completes |`
- Table exit code : `| PostCompact | No | Shows stderr to user only |`
- Matcher patterns : `| PreCompact, PostCompact | what triggered compaction | manual, auto |`

**Comportement** :
- Non bloquant (exit 2 → stderr montré à user uniquement, pas à Claude)
- Matcher disponible : `manual` ou `auto` (selon ce qui a déclenché la compaction)
- Pair avec `PreCompact` (lui bloquant via exit 2)

→ Claim Boris (Pragmatic Engineer interview) **CONFIRMÉ**.

## 4. Exit codes — sémantique verbatim

> **Exit 0** = succès. stdout parsé pour JSON. JSON traité uniquement sur exit 0. Pour la plupart des events stdout est en debug log ; exceptions `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart` où stdout est ajouté comme contexte visible par Claude.
>
> **Exit 2** = erreur bloquante. stdout ignoré, stderr renvoyé à Claude comme message d'erreur. Effet dépend de l'event.
>
> **Tout autre code** = erreur non bloquante (sauf `WorktreeCreate` où tout non-zéro abort). Transcript affiche `<hook name> hook error` + première ligne stderr. Exécution continue.

> **Warning** : Exit 1 = non bloquant (contrairement à la convention Unix). Pour enforce une policy, utiliser `exit 2`. Exception : `WorktreeCreate` (any non-zero abort).

Events bloquants sur exit 2 : `PreToolUse`, `PermissionRequest`, `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `ConfigChange`, `PostToolBatch`, `PreCompact`, `Elicitation`, `ElicitationResult`, `WorktreeCreate`.

## 5. `hookSpecificOutput` — exemples verbatim

**PreToolUse** :
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed"
  }
}
```

**PermissionRequest** :
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": { "command": "npm run lint" }
    }
  }
}
```

**PostToolUse / SessionStart** : champ `additionalContext` (string injecté dans le contexte Claude).

**UserPromptSubmit** : supporte `decision: "block"` + `reason` + `hookSpecificOutput.additionalContext` + `sessionTitle`.

## 6. `asyncRewake` — existe-t-il ?

**OUI, officiellement documenté.** Verbatim "Command hook fields" :

> `async` | no | If `true`, runs in the background without blocking.
>
> `asyncRewake` | no | If `true`, runs in the background and **wakes Claude on exit code 2**. Implies `async`. The hook's stderr, or stdout if stderr is empty, is shown to Claude as a system reminder so it can react to a long-running background failure.

→ Mécanisme : background non bloquant + réveil de Claude via exit 2 + injection stderr comme system reminder. Disponible sur les hooks `command`.

## Réponses synthétiques aux 6 questions

1. **Liste exhaustive** : 29 events (voir §1).
2. **Timeout agent hook** : 60 secondes (verbatim doc). Aucune limite "tool-use turns" documentée officiellement.
3. **`PostCompact`** : EXISTE. Non bloquant. Matcher `manual` ou `auto`. Pair avec `PreCompact`.
4. **Exit codes** : 0 = OK (JSON parsé), 2 = bloquant (stderr → Claude), autre = non bloquant (sauf `WorktreeCreate`). Exit 1 ≠ blocking.
5. **`hookSpecificOutput`** : objet contenant `hookEventName` + champs spécifiques (`permissionDecision`, `additionalContext`, `decision.behavior`, `sessionTitle`, `retry`, etc.).
6. **`asyncRewake`** : EXISTE sur hooks `command`. Background + wake Claude sur exit 2 + stderr injecté en system reminder.

## Liens

- [[claude-code-features-2026]]
- [[boris-thariq-bestpractices]]
- [[hook-events-reference]]
