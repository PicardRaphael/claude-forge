---
name: skills-complete-guide
description: Resume du guide officiel Anthropic (33p) pour creer des skills — principes cles, categories, structure
type: reference
---

## Guide officiel Anthropic — Skills (lu le 2026-04-03)

Source : guide interne de 33 pages, contenu integre dans les skills de reference cc-skills-ref.

### 9 categories de skills (Thariq)
1. New feature workflow
2. Bug fix workflow
3. Code review checklist
4. Testing strategy
5. Documentation generator
6. Refactoring guide
7. Deployment procedure
8. Performance optimization
9. Security audit

### 8 principes cles
1. Dossiers avec scripts/assets, pas juste du markdown
2. Section Gotchas = contenu le plus important
3. Progressive disclosure — pointer vers des fichiers, Claude lit a la demande
4. Ne pas etre trop specifique — laisser de la flexibilite
5. 1 skill = 1 categorie propre
6. SKILL.md < 500 lignes — deporter dans references/
7. Tester avec des cas reels avant de publier
8. Description YAML : une seule ligne, en anglais, declencheurs clairs

### Structure type
```
.claude/skills/nom-skill/
  SKILL.md          <- Point d'entree, < 500 lignes
  scripts/          <- Scripts executables
  references/       <- Docs de reference detaillees
```

Ce guide est la base de nos skills cc-skills-ref et skill-creator.
