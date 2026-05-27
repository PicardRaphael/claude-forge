---
name: skill-structure-complete
description: Structure complète d'une skill Claude Code — dossier, SKILL.md, scripts/, references/, assets/. Les scripts doivent vivre DANS la skill pas à la racine.
type: feedback
---

Une skill = un dossier complet, pas juste un SKILL.md.

**Structure :**
```
.claude/skills/ma-skill/
  SKILL.md          ← le contenu principal
  scripts/          ← scripts exécutables (bash, python...)
  references/       ← docs de référence (PDF, guides)
  assets/           ← images, templates
```

**Why:** J'ai créé un script `export-schema.sh` à la racine du projet au lieu de le mettre dans `.claude/skills/schema-mcp-postgres/scripts/`. Les scripts associés à une skill doivent vivre dans le dossier de la skill.

**How to apply:** Quand une skill a besoin d'un script, le créer dans `skills/nom-skill/scripts/`. La skill y fait référence via un chemin relatif. Ne jamais mettre de fichiers liés à une skill à la racine du projet.
