---
name: agent-type-hook-detection
description: "Hooks: agent_id = discriminant officiel sub-agent (présent UNIQUEMENT en subagent); agent_type INSUFFISANT (présent aussi en main session --agent); jamais CLAUDE_AGENT env"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 405aaef3-b4d6-4ba2-9292-03dc7f0bab67
---

## Détection subagent dans les hooks (stdin JSON)

**Discriminant officiel : `agent_id`** — doc hooks (code.claude.com/docs/en/hooks, vérifiée 9 juin 2026) : « present only when the hook fires inside a subagent call — use this to distinguish subagent hook calls from main-thread calls ». Test : `Boolean(data.agent_id)`.

```typescript
if (!data.agent_id) process.exit(0); // session principale
```

**`agent_type` est INSUFFISANT** : il est aussi présent quand la main session tourne avec `--agent <nom>` — l'utiliser comme discriminant bloquerait la session principale. Il reste utile pour savoir QUEL agent appelle (bypass ciblé par nom). `subagent_type` n'existe pas dans les payloads hooks.

`CLAUDE_AGENT` n'est PAS une variable d'environnement du runtime Claude Code — jamais settée automatiquement. Tout test dessus = dead code.

**Why:** 2026-05-21 : tdd-guard neo_ia/ia_back testaient `CLAUDE_AGENT` = dead code. 2026-06-09 : la mémoire (qui disait `agent_type` discriminant, observation empirique du 21 mai) contredite par la doc officielle lors de la conception de config-guard.ts neoteem-back-ts — l'écart mémoire/doc n'a été vu que parce que Raphael a exigé la validation web.

**How to apply:** Distinguer main/sub → `agent_id` seul. Identifier l'agent → `agent_type`. Jamais env var. Mémoire technique datée → revalider contre la doc officielle avant de concevoir un garde-fou dessus.

Lié à : [[hooks-enforcement-pattern]], [[marker-ttl-antipattern]]
