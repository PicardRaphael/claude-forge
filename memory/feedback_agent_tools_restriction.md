---
name: agent-tools-enforce-delegation
description: Pour forcer un orchestrateur à déléguer, utiliser tools: Agent(agent1, agent2), Read — PAS de Bash/Grep/Write. Le prompt seul ne suffit JAMAIS.
type: feedback
---

Un agent orchestrateur qui a `Bash` ou `Grep` fera le travail lui-même au lieu de déléguer. Le prompt "ne fais jamais le travail" est ignoré.

**Why:** Le CTO avait `tools: Read, Grep, Glob, Bash, Agent`. Malgré des instructions explicites, il lançait des Bash pour explorer au lieu de déléguer à schema-mapper et repo-functions-analyzer. Testé 2 fois, même résultat. Même après renforcement du prompt → toujours pareil.

**How to apply:**

### Orchestrateur (CTO, Lead)
```yaml
tools: Agent(architect, dev, debugger, ...), Read, Glob
```
- `Agent(nom1, nom2)` = ne peut spawner QUE ces agents nommés
- `Read` et `Glob` uniquement pour vérifier les résultats
- PAS de Bash, Grep, Write, Edit

### `disallowedTools` (alternative denylist)
```yaml
disallowedTools: Bash, Write, Edit, MultiEdit
```
Retire ces outils de la liste héritée. Utile si on veut garder la plupart des outils.

### Worker (Dev, Debugger, Architect)
Gardent tous les outils nécessaires car ils FONT le travail.

### Règle générale
- Le prompt ne peut PAS overrider la disponibilité d'un outil
- Seule la restriction de tools est structurellement fiable
- Si un agent ne doit pas faire X → retirer l'outil qui permet X
