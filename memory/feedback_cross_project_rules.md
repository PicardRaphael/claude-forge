---
name: cross-project-rules-not-inherited
description: When analyzing external projects from forge, forge rules (delegation, check-before-create) are NOT automatically enforced — must be explicitly reminded or hooks deployed to target project
type: feedback
originSessionId: d8d939df-a3a5-40ee-a82f-8efda6c1e9a6
---
## Decouverte critique (2026-04-26)

Quand claude-forge analyse un autre projet (ia_back, neo_ia, neoteem-brain, bdd), les rules forge (.claude/rules/) NE S'APPLIQUENT PAS dans le contexte du projet cible. Le hook delegate-guard.py ne se declenche que dans le workspace forge.

## Consequences

- L'analyse de ia_back a ignore toutes les rules forge (delegation, check-before-create, forge-brain, memory-discipline)
- 6 skills + 14 agents edites directement sans agents specialises
- Tout le travail a du etre refait

## Solutions

1. **Hooks dans chaque projet** : deployer delegate-guard.py dans les settings.json de CHAQUE projet analyse
2. **Instructions explicites dans le prompt d'analyse** : quand project-analyzer ou tout agent travaille sur un projet externe, le prompt DOIT rappeler les regles forge (delegation aux specialists, check forge-brain, check memoire)
3. **Le project-analyzer doit inclure ces regles dans son propre prompt**

**Why:** Les rules de forge sont locales au workspace forge. Un agent dispatche sur un autre projet ne les herite pas. C'est un defaut d'architecture, pas un oubli ponctuel.

**How to apply:** Avant TOUTE analyse cross-projet, verifier que le projet cible a les hooks de protection OU inclure les regles explicitement dans le prompt de l'agent.
