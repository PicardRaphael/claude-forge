---
name: agent-tools-enforce-delegation
description: Pour forcer un orchestrateur à déléguer, utiliser tools: Agent(agent1, agent2), Read — PAS de Bash/Grep/Write. Le prompt seul ne suffit JAMAIS.
type: feedback
---

Cf [[comment-creer-agent]] (doctrine : restriction de `tools`/`disallowedTools` est le seul levier structurellement fiable pour forcer la délégation ; le prompt ne peut PAS overrider la disponibilité d'un outil ; agent orchestrateur sans Bash/Grep/Write/Edit).

**Cas empirique(s) :**

- Le CTO avait `tools: Read, Grep, Glob, Bash, Agent`. Malgré des instructions explicites, il lançait des Bash pour explorer au lieu de déléguer à schema-mapper et repo-functions-analyzer. **Testé 2 fois, même résultat. Même après renforcement du prompt → toujours pareil.**
