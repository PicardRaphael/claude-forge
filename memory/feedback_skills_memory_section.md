---
name: skills-must-have-memory-section
description: Toute skill qui découvre du contexte métier, des patterns ou reçoit du feedback doit avoir une section "Apprentissage" pour instruire Claude de sauvegarder en mémoire projet.
type: feedback
---

Les skills n'ont pas de champ `memory` en frontmatter (réservé aux agents). Mais elles DOIVENT avoir une section "Apprentissage — Sauvegarder en mémoire projet" qui liste explicitement ce que Claude doit retenir après utilisation.

**Why:** Sans cette section, les découvertes faites pendant l'utilisation d'une skill (règles métier, patterns, feedback dev) sont perdues entre les sessions. L'agent principal a `memory: project` mais les skills invoquées dans le contexte principal n'instruisent pas Claude de sauvegarder les apprentissages.

**How to apply:**
- Ajouter une section `## Apprentissage — Sauvegarder en mémoire projet` dans chaque skill qui interagit avec du contexte métier
- Lister ce qu'il faut retenir (règles métier, patterns, pièges, feedback) et ce qu'il ne faut PAS retenir (détails éphémères, code généré)
- Pour les agents : `memory: project` dans le frontmatter suffit
- Pour les skills purement techniques/référence (ex: sql-best-practices) → pas besoin, elles ne découvrent rien de nouveau
