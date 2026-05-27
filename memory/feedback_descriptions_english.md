---
name: descriptions-always-english
description: Les descriptions YAML des skills et agents doivent TOUJOURS être en anglais pour un meilleur matching par le modèle. Le contenu du SKILL.md peut être en français.
type: feedback
---

Les descriptions dans le frontmatter YAML (skills et agents) doivent être en anglais.

**Why:** Boris et Anthropic recommandent l'anglais pour les descriptions — c'est ce que le modèle matche le mieux pour le triggering automatique. Le contenu du skill/agent peut rester en français.

**How to apply:** 
- `description:` dans le YAML → toujours en anglais
- Contenu du SKILL.md ou agent .md → français OK
- Inclure les triggers en français ET anglais dans la description si les utilisateurs parlent français (ex: `Use when user says "migre", "migrate"`)
