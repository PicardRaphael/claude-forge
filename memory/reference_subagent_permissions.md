---
name: subagent-permissions-limitation
description: Bug subagent permissions — PARTIELLEMENT FIXE v2.1.101 (worktree access + MCP tools). permissions.allow/deny toujours non herites.
type: reference
originSessionId: f3b37008-cac0-4a75-ae36-b058217ea80b
---
## Limitation : permissions non heritees par les subagents

**Statut :** Partiellement fixe en v2.1.101 (10 avril 2026).

### Ce qui est FIXE (v2.1.101)
- Subagents en worktrees isoles ont maintenant acces Read/Edit a leur propre worktree
- Subagents heritent les MCP tools des serveurs injectes dynamiquement
- `permissions.deny` override maintenant `PreToolUse` hook `permissionDecision: "ask"`

### Ce qui n'est PAS encore fixe
- `permissions.allow` de `.claude/settings.json` non propage aux subagents
- `~/.claude/settings.json` (niveau user) non propage
- Flag `--dangerously-skip-permissions` non propage

**Issues principales :**
- #37730 — Subagents re-promptent pour des tools deja approuves
- #27661 — Subagents n'heritent ni hooks, ni permissions, ni CLAUDE.md

**Workarounds restants :**
1. `mode: bypassPermissions` dans le frontmatter — contourne mais supprime toute securite
2. `mode: acceptEdits` — accepte auto les edits, prompte encore pour Bash

**How to apply:** La situation s'ameliore. Pour les cas worktree et MCP, plus de workaround necessaire. Pour permissions.allow, continuer avec `mode: acceptEdits` comme compromis.
