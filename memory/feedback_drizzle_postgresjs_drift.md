---
name: ia-back-postgresjs-stack-drift-pattern
description: "ia_back avait 17 fichiers `.claude/` référençant Drizzle alors que stack = postgres.js depuis migration. Pattern : migration code finie mais migration `.claude/` oubliée. Toujours auditer cohérence stack-code↔stack-prompts."
trigger: drizzle, postgres, ia_back, migration, stack, drift
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

Découvert pendant audit ia_back 22 mai 2026.

**Règle :** Quand un repo migre de stack (ex Drizzle→postgres.js), les prompts `.claude/` ne sont jamais purgés automatiquement. Drift inévitable.

**Why:** Migration code = visible (tests cassent, build fail). Migration prompts = invisible (advisory, ne casse rien). Les sub-agents continuent à proposer Drizzle alors que le code est postgres.js.

**How to apply:**
- Sur tout audit `.claude/`, grep la stack OLD vs NEW (`Drizzle` vs `postgres.js`, `Express` vs `Hono`, `Vue 2` vs `Vue 3 Composition API`)
- Si > 5 fichiers contaminés → chantier dédié de purge, batch via skill-creator + claudemd-optimizer + agent-creator
- Sur ia_back : `connect-table` et `sql-best-practices` ont nécessité **réécriture intégrale**, pas juste find/replace
- Faux positifs OK : mentions historiques ("avant on utilisait Drizzle") et corrections explicatives ("postgres.js PAS Drizzle") restent légitimes
