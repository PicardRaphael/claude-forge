---
name: rules-frontmatter-mandatory
description: "Rules without YAML frontmatter description: field are silently dead — Claude Code never loads them"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2c8f61e9-59a4-4658-863a-864e27242ec9
---

Rules sans frontmatter `description:` ne sont JAMAIS chargées par Claude Code — mortes silencieusement.

**Why:** Audit 2026-05-21 : `agents-color-convention.md` et `outcomes-after-architect.md` étaient mortes sur les 2 repos (ia_back + neo_ia). Le pipeline outcomes-test n'était jamais enforcé.

**How to apply:** Après toute création de rule, vérifier que le fichier commence par `---\ndescription: ...\n---`. Ajouter dans le checklist de création de composants (`check-before-create`).

Lié à : [[checklist-before-modify-mandatory]], [[hooks-enforcement-pattern]]
