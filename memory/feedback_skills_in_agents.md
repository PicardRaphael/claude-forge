---
name: skills-auto-loaded-in-agents
description: Toujours injecter les skills pertinentes dans le frontmatter skills: des agents — les subagents n'heritent pas des skills du parent
type: feedback
---

Toujours ajouter `skills:` dans le frontmatter des agents avec les skills pertinentes pour leur travail.

**Why:** Les subagents n'heritent PAS les skills du parent (breaking change v2.1). Sans `skills:` explicite, l'agent travaille sans les conventions/references. Oublie sur le kit bdd le 2026-04-07 — les 3 agents n'avaient aucune skill injectee. back2.0 avait 8 skills ref dans ses agents.

**How to apply:** Pour chaque agent cree, se demander : "De quelles skills cet agent a besoin pour bien travailler ?" et les lister dans `skills:`. Exemples :
- Agent d'ecriture → skill de conventions + skill de review
- Agent de debug → skill de review + skill d'impact + skill de recherche
- Agent de migration → skill d'impact
