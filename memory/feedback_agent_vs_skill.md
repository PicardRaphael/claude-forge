---
name: agent-vs-skill-invocation
description: Différence claire entre agents et skills dans Claude Code — les deux sont utiles, ne pas les confondre.
type: feedback
---

## Agents (`.claude/agents/`)
- Claude les dispatch via l'outil `Agent` (subagent_type ou prompt)
- Invoqués par : l'utilisateur en langage naturel ("utilise ton agent X", "analyse ma BDD avec ton agent"), OU Claude décide seul via la `description`, OU un autre agent les lance comme sous-agent
- PAS des slash commands — mais PAS besoin d'en être un pour fonctionner

## Skills (`.claude/skills/`)
- Slash commands : l'utilisateur tape `/nom`
- Point d'entrée explicite et rapide

## Les deux sont complémentaires
- Agent = Claude décide ou l'utilisateur demande en langage naturel
- Skill = raccourci `/command` pour lancement direct
- On peut avoir les deux pour le même outil (agent pour l'orchestration, skill pour le raccourci)

**Why:** J'ai dit à l'utilisateur que `/schema-mapper` ne marchait pas parce que c'était un agent. En réalité l'agent marchait très bien — l'utilisateur pouvait dire "analyse ma BDD avec ton agent" et Claude l'aurait lancé. La skill est un PLUS, pas un remplacement obligatoire.

**How to apply:** Ne jamais présenter un agent comme "cassé" parce qu'il n'est pas un slash command. Expliquer les deux modes d'invocation. Proposer la skill comme raccourci optionnel, pas comme correction.
