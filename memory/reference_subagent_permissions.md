---
name: subagent-permissions-limitation
description: Bug subagent permissions — PARTIELLEMENT FIXE v2.1.101 (worktree access + MCP tools). permissions.allow/deny toujours non herites.
trigger: subagent, permission, allow, deny, herite, worktree
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

### Permission heritee != sandbox filesystem (verifie empiriquement 18 juin 2026)

`permissions.allow` non herite = le subagent peut RE-PROMPTER pour un chemin, PAS qu'il est murre. Il n'existe AUCUN sandbox filesystem isolant les repos entre eux sur la machine forge (Windows). Test : un subagent lance depuis claude-forge a lu librement `neot-v2/neo_ia/**` et `neot-v2/neoteem-back-ts/**` (Read + Grep + Glob), zero blocage — parce que le settings.json de forge a deja les `Read/Grep/Glob(neot-v2/**)` dans son `allow`.

Consequence pour un design « subagent explore plusieurs repos » (ex. discovery cross-repo ia-workbench) : la capacite technique EXISTE, le seul prerequis est de configurer le `permissions.allow` du repo SOURCE en read-only strict (`Read`/`Grep`/`Glob(neot-v2/**)`, jamais `Write`/`Edit`/`Bash` destructif). Distinct de `repo-scope-guard` (hook neot-v2/ qui BLOQUE volontairement la sortie de scope) — capacite brute != garde-fou intentionnel. Cf [[erreur-architect-neo_ia-fouille-bdd]] (cote garde-fou) + `critique-2026-06-18-ia-workbench-spec-discovery` (cote design discovery).
