---
name: permissionmode-enum-valid-values
description: permissionMode frontmatter agent accepte UNIQUEMENT acceptEdits | plan | bypassPermissions. default est invalide silencieux. Utiliser plan pour agents read-only sauf Bash
metadata: 
  node_type: memory
  type: reference
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# permissionMode enum valeurs valides — frontmatter agents

## La règle

`permissionMode` frontmatter agent Claude Code accepte 3 valeurs :

| Valeur | Usage |
|--------|-------|
| `acceptEdits` | Agents créateurs (skill-creator, agent-creator, hook-creator, claudemd-optimizer) — auto-accept Edit/Write |
| `plan` | Agents read-only + Bash (outcomes-grader, prompt-eval-runner, codebase-analyst) — interaction Bash mais pas d'edit |
| `bypassPermissions` | Agents critiques sensibles — bypass total (rare, justifier) |

## Gotcha — `default` INVALIDE

`permissionMode: default` n'est PAS valide silencieusement. Aucun warning, juste comportement non spécifié. Découvert via agent-creator sub-agent qui a auto-corrigé `default` → `plan` pour `prompt-eval-runner` neo_ia (26 mai 2026).

Référence canonique : skills officielles Anthropic, agents Anthropic, et agents forge (vérifié outcomes-grader.md qui utilise `plan` pour profil read+bash).

## Mapping rapide par type d'agent

| Type d'agent | tools | disallowedTools | permissionMode |
|--------------|-------|-----------------|----------------|
| Créateur (skill/agent/hook/claudemd) | All | (none) | acceptEdits |
| Read-only + Bash (eval, audit, analyzer) | Read, Glob, Bash | Write, Edit | plan |
| Read-only pur (Explore, codebase-scanner) | Read, Grep, Glob | Write, Edit, Bash | plan |
| Reviewer/grader | Read, Grep | Write, Edit, Bash | plan |
| DA / critique | Read, Grep, Glob, Bash | (limité) | plan |
