---
name: argument-hint-champ-officiel
description: argument-hint est un champ frontmatter OFFICIEL Anthropic pour les slash commands — ne jamais le signaler comme erreur lors d'un audit
metadata:
  type: feedback
---

`argument-hint` est un champ frontmatter **officiel Anthropic** présent dans les skills de type slash command. Il affiche un indice d'argument quand l'utilisateur tape `/nom-skill` dans l'interface.

**Exemple** : `argument-hint: "[rough prompt to expand]"` dans la skill `expand`.

**Why:** Lors de l'audit de `expand` (session 2026-06-06), ce champ a été classé CRITIQUE (champ hors liste fermée) — c'était un faux positif. La liste fermée de `checklist-skill-parfaite.md` l'avait omis.

**How to apply:** Lors d'un audit frontmatter skill, ne JAMAIS signaler `argument-hint` comme erreur. Ce champ est valide uniquement pour les skills invocables via slash command. La checklist locale (`skill-creator/references/checklist-skill-parfaite.md`) a été mise à jour en conséquence (ligne 43).

Champs frontmatter valides complets : `name`, `description`, `user-invocable`, `allowed-tools`, `model`, `effort`, `disable-model-invocation`, `argument-hint`.
