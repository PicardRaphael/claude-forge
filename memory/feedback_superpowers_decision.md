---
name: superpowers-neo-ia-keep-ia-back-skip
description: Garder superpowers dans neo_ia (executing-plans utile pour L), ne pas ajouter a ia_back (TaskCreate suffit). Toujours optimiser, ne pas garder un truc juste parce qu'il est la.
type: feedback
originSessionId: 7344c917-42fa-4a63-8a92-bc680e8d28e4
---
## Superpowers plugin : executing-plans UNIQUEMENT sur les deux repos

- **brainstorming + writing-plans** : SUPPRIMES des deux repos. L'architect fait ca nativement avec les skills domaine et la memoire projet. Les templates generiques superpowers marchent SUR les pieds de l'architect.
- **executing-plans** : GARDE sur neo_ia ET ia_back. Seul apport unique = batch de 3 taches + checkpoints de review entre batches. Utile pour les taches L (>5 fichiers).

**Why:** Le user veut TOUJOURS le meilleur. Ne jamais garder un truc juste parce qu'il est la. Brainstorming/writing-plans = overhead inutile car l'architect a deja le domaine. Executing-plans = vrai delta car ni l'architect ni TaskCreate ne font du batching + checkpoints.

**How to apply:** Sur tout projet avec agent architect + dev agents : activer UNIQUEMENT `executing-plans` pour les taches L. Ne JAMAIS ajouter brainstorming/writing-plans si un architect avec skills domaine existe. Si CC ajoute un pattern natif de batching → supprimer executing-plans.
