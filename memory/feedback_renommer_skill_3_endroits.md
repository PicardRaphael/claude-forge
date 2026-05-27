---
name: renommer-skill-3-endroits-pas-2
description: Renommer une skill = 3 endroits (dossier + frontmatter name + body occurrences slash command). Briefer skill-creator EXPLICITEMENT sur les 3 sinon il oublie le body
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# Renommer skill = 3 endroits, pas 2

## La règle

Quand on renomme une skill Claude Code, modifier les 3 emplacements en une seule passe :

1. **Dossier** : `mv ancien-nom nouveau-nom` (filesystem)
2. **Frontmatter SKILL.md** :
   - `name:` (ligne ~2)
   - `description:` si elle contient le slash command (souvent)
3. **Body SKILL.md** : occurrences du slash command dans :
   - Section "Invocation" / "Usage" (exemples `/ancien-nom <args>`)
   - Section "Exemples" (3-4 invocations typiques)
   - Section "Apprentissage" / "Gotchas" si historique
   - Blocs code `Usage:` et `Exemple:`

## Why

Validé empiriquement 26 mai 2026 sur skill `ia-back-contract-prompt` → `ia-back-contract` (neo_ia) :
- Premier dispatch skill-creator : brief "modifier 2 lignes frontmatter uniquement" → 5 occurrences body oubliées (lignes 14, 17, 18, 37, 38)
- Second dispatch : brief explicite "replace_all `/ancien-nom` → `/nouveau-nom`" → 0 résidu en 1 passe
- 1 round-trip perdu

## How to apply

Brief skill-creator pour rename :

> Renommer skill : modifier
> 1. Dossier filesystem : `mv old-name new-name`
> 2. Frontmatter SKILL.md : `name:` + `description:` (si slash command mentionné)
> 3. Body SKILL.md : `Edit replace_all "/old-name" → "/new-name"` (toutes occurrences slash command)
> Vérifier grep 0 résidu post-édition.

## Anti-patterns à éviter

- ❌ Brief "modifier 2 lignes frontmatter" sans mentionner body
- ❌ Edit sans `replace_all: true` quand occurrences multiples (vue dans grep)
- ❌ Skip vérif empirique grep post-rename → résidus invisibles

## Wikilinks

- [[feedback_edit_tool_read_obligatoire]] — pattern Edit batch
- [[feedback_proactive_references]] — proactive extraction
