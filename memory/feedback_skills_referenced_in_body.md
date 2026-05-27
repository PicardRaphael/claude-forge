---
name: skills-must-be-referenced-in-body
description: Skills declarees dans le frontmatter DOIVENT etre referencees dans le body de l'agent avec instructions d'usage
type: feedback
originSessionId: 00ed39aa-17db-4d58-bcdc-ef097926d20a
---
Avoir une skill dans `skills:` du frontmatter la rend DISPONIBLE mais ne garantit pas que l'agent SAIT quand l'utiliser.

**Why:** Session 8 mai 2026 — audit a montré que `obsidian-markdown` était dans 9 agents mais jamais mentionnée dans le body. `python-ref` dans python-dev pareil. Résultat : les agents n'utilisaient jamais ces skills.

**How to apply:**
- Chaque skill dans `skills:` doit être mentionnée dans le body avec instructions : QUAND l'utiliser et COMMENT
- Exemple : "Consulter la skill **python-ref** pour les best practices Python 3.11+ avant d'implémenter"
- Vérifier avec : `grep skill_name body` — si 0 match = problème
- Audit disponible : script Python dans la session qui vérifie toutes les skills de tous les agents
