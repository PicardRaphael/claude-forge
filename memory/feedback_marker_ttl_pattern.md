---
name: marker-ttl-antipattern
description: Ne jamais mettre de TTL sur les markers architect/code-reviewer — vérification existence seule, hooks PostToolUse quality en async
type: feedback
originSessionId: b83cf0a3-7f05-46e9-9772-44ba96f1eaef
---
Markers architect-guard et commit-guard doivent vérifier l'EXISTENCE du fichier, jamais un TTL temporel. Le TTL bloque les sessions longues légitimes.

**Why:** TTL 60min bloquait les dev agents au milieu de features longues. Combiné avec hooks synchrones (ruff, typecheck) et hooks user-level (NeoBoard, no-inline-python), ça causait des cascades de blocage et des "Tool result missing due to internal error" à 149+ tool calls.

**How to apply:**
- Hooks guard (PreToolUse) : check binaire exists/not-exists, jamais de logique temporelle
- Hooks quality (PostToolUse) comme ruff/typecheck/format : toujours `async: true`
- Hooks user-level (~/.claude/) : éviter, ils s'appliquent à TOUS les projets
- Permissions Bash : wildcards (`Bash(uv *)`) jamais de commandes exactes
