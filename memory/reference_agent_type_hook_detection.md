---
name: agent-type-hook-detection
description: "Hooks PreToolUse detects subagent via agent_type/subagent_type in stdin JSON, NOT via CLAUDE_AGENT env var (never auto-set)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 405aaef3-b4d6-4ba2-9292-03dc7f0bab67
---

## Détection subagent dans les hooks PreToolUse

`CLAUDE_AGENT` n'est PAS une variable d'environnement automatique du runtime Claude Code. Elle n'est JAMAIS settée automatiquement quand un subagent s'exécute.

La bonne méthode : lire `agent_type` ou `subagent_type` dans le JSON stdin du hook. Le runtime CC injecte ces champs quand le hook s'exécute dans un subagent nommé.

**Toujours utiliser le multi-field fallback** (le nom du champ varie selon les versions CC) :
```python
agent_type = data.get("agent_type", "") or data.get("subagent_type", "")
```
```typescript
const agentType = String(data.agent_type ?? data.subagent_type ?? "");
```

**Confirmation empirique (2026-05-21)** : tests E2E sur neo_ia + ia_back. Payloads runtime capturés. Le champ runtime est **`agent_type`** (top-level). Main session = champ ABSENT. Subagents = valeur = nom de l'agent (`"test-writer"`, `"dev-neochat"`, `"dev"`). `subagent_type` non observé mais le fallback reste correct par sécurité.

**Why:** Session 2026-05-21 : les tdd-guard des 2 repos avaient `CLAUDE_AGENT == "test-writer"` = dead code. Le bypass test-writer ne fonctionnait que parce que test-writer écrit dans tests/ (exempté par une autre règle). Le vrai problème serait apparu avec dispatch-guard (bloquerait TOUS les subagents si seul `agent_type` était vérifié et que le runtime utilise `subagent_type`).

**How to apply:** Tout hook qui doit distinguer main session vs subagent → JSON stdin, multi-field. Jamais env var. Vérifier dans les hooks existants de chaque repo.

Lié à : [[hooks-enforcement-pattern]], [[marker-ttl-antipattern]]
