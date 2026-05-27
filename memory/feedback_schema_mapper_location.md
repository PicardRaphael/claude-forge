---
name: schema-mapper-not-in-forge
description: Les composants créés pour d'autres projets ne doivent PAS être dans le .claude de claude-forge. Les mettre dans un dossier séparé ou directement dans le .claude du projet cible.
type: feedback
---

Ne JAMAIS ajouter dans `.claude/` de claude-forge des agents/skills destinés à un autre projet.

**Why:** Le schema-mapper (agent + skills) est destiné au projet du collègue, pas à claude-forge. En le mettant dans `.claude/` de claude-forge, on pollue le projet avec des composants qui ne le concernent pas.

**How to apply:**
- Si on a accès au dossier du projet cible → créer directement dans son `.claude/`
- Sinon → créer dans un dossier de livraison séparé (ex: `output/nom-projet/`) que le collègue copiera
- claude-forge `.claude/` = uniquement les composants de claude-forge lui-même
