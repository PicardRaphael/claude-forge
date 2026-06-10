---
name: permissionmode-enum-valid-values
description: permissionMode agent = default | acceptEdits | auto | dontAsk | bypassPermissions | plan (doc officielle 9 juin 2026). Parent auto mode = frontmatter ignoré. plan pour read-only+Bash
metadata: 
  node_type: memory
  type: reference
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# permissionMode enum valeurs valides — frontmatter agents

## La règle (doc officielle code.claude.com/docs/en/sub-agents, vérifiée 9 juin 2026)

`permissionMode` frontmatter agent accepte **6 valeurs** : `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`.

| Valeur | Usage |
|--------|-------|
| `default` | Prompts de permission standards |
| `acceptEdits` | Agents créateurs — auto-accept Edit/Write + commandes filesystem du working dir |
| `auto` | Classifier en arrière-plan évalue les commandes |
| `dontAsk` | Auto-refuse les prompts (les outils explicitement allowed passent) |
| `bypassPermissions` | Bypass total (rare, justifier) |
| `plan` | Agents read-only (+ Bash lecture) |

**Précédence parent** : si la session parent est en `bypassPermissions` ou `acceptEdits`, ça prime (non overridable). Si parent en **auto mode**, le `permissionMode` frontmatter du sub-agent est **IGNORÉ** — le classifier évalue ses tool calls avec les règles du parent.

`hooks`, `mcpServers`, `permissionMode` sont **ignorés pour les agents de plugins** (sécurité).

## Historique — correction 9 juin 2026

L'ancienne version de cette mémoire (26 mai) disait « acceptEdits | plan | bypassPermissions UNIQUEMENT, `default` invalide silencieux » — contredite par la doc officielle actuelle qui liste `default` comme valeur valide. Leçon récurrente : revalider la mémoire technique contre la doc officielle avant de s'en servir comme référence d'audit (même pattern que agent_type→agent_id).

## Mapping rapide par type d'agent

| Type d'agent | tools | disallowedTools | permissionMode |
|--------------|-------|-----------------|----------------|
| Créateur (skill/agent/hook/claudemd) | All | (none) | acceptEdits |
| Read-only + Bash (eval, audit, analyzer) | Read, Glob, Bash | Write, Edit | plan |
| Read-only pur (Explore, codebase-scanner) | Read, Grep, Glob | Write, Edit, Bash | plan |
| Reviewer/grader | Read, Grep | Write, Edit, Bash | plan |
| DA / critique | Read, Grep, Glob, Bash | (limité) | plan |
