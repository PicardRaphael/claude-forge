---
name: cc-news
description: Use this skill when the user asks about recent Claude Code updates, new features, or when any information might be outdated. Use PROACTIVELY when the user asks "quoi de neuf", "est-ce que X existe maintenant", or when knowledge seems stale. Date de référence : 31 mars 2026.
user-invokable: true
allowed-tools: WebSearch, WebFetch, Read, Write
argument-hint: "fonctionnalité ou sujet à vérifier"
---

# Vérificateur de Nouveautés Claude Code

Date de référence du studio : **31 mars 2026**
Tout ce qui est postérieur à cette date doit être recherché.

## Sources à consulter

### Officielles
1. `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. `https://docs.anthropic.com/en/release-notes/claude-code`
3. `https://code.claude.com/docs/en/changelog`

### Équipe Claude Code (OBLIGATOIRE — vérifier chaque personne)
4. **Boris Cherny** (@bcherny) — créateur de Claude Code
   - `https://howborisusesclaudecode.com`
   - threads.com/@boris_cherny
   - x.com/bcherny
5. **Cat Wu** (@_catwu) — Head of Product Claude Code
   - x.com/_catwu
6. **Lydia Hallie** (@lydiahallie) — Claude Code team
   - x.com/lydiahallie
7. **Noah Zweben** (@noahzweben) — Claude Code team
   - x.com/noahzweben
8. **Thariq Shihipar** (@trq212) — Skills author, Claude Code team
   - x.com/trq212
   - linkedin.com/in/thariq
9. **Jarred Sumner** (@jaraboron) — Bun creator, acquis par Anthropic
   - x.com/jaraboron

## Recherches à effectuer

```
Chercher : Claude Code changelog site:github.com/anthropics/claude-code
Chercher : Claude Code $ARGUMENTS 2026
Chercher : @bcherny Claude Code 2026
Chercher : @_catwu Claude Code 2026
Chercher : @lydiahallie Claude Code 2026
Chercher : @noahzweben Claude Code 2026
Chercher : thariq shihipar claude code skills 2026
Chercher : jarred sumner anthropic claude code 2026
Chercher : Claude Code deprecated OR breaking 2026
```

## Étapes

1. Rechercher TOUTES les sources ci-dessus (officielles + équipe)
2. Identifier ce qui est postérieur à la date de référence
3. Comparer avec les features déjà connues (cc-features-ref + mémoire)
4. Vérifier les dépréciations et breaking changes
5. Résumer les nouveautés à l'utilisateur
6. Mettre à jour la mémoire si découvertes importantes

## Format de réponse

```markdown
## [Date] — Mise à jour cc-news

### Officiel (changelog)
- [version] : [features]

### Équipe Claude Code
- **Boris** : [tips/annonces]
- **Cat** : [insights produit]
- **Lydia** : [features/workshops]
- **Noah** : [features cloud/mobile]
- **Thariq** : [skills patterns]
- **Jarred** : [performance/runtime]

### Dépréciations
- [feature] → [remplacement]

### Communauté
- [observations notables]

Sources : [URLs]
```

- Indiquer la date de la recherche
- Distinguer "officiel" vs "équipe" vs "communauté"
- Si rien de nouveau → dire que le studio est à jour
