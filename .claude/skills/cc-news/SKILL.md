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

1. `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. `https://docs.anthropic.com/en/release-notes/claude-code`
3. Threads de @bcherny (threads.com/@boris_cherny)
4. `https://howborisusesclaudecode.com`

## Recherches à effectuer

```
Chercher : Claude Code changelog site:github.com/anthropics/claude-code
Chercher : @bcherny Claude Code nouvelles features 2026
Chercher : Claude Code $ARGUMENTS 2026
```

## Étapes

1. Rechercher les sources ci-dessus
2. Identifier ce qui est postérieur au 31 mars 2026
3. Comparer avec les features déjà connues (cc-features-ref)
4. Résumer les nouveautés à l'utilisateur
5. Mettre à jour la mémoire

```markdown
## [Date] — Mise à jour cc-news

Nouvelles features : [...]
Sources : [URLs]
```

## Format de réponse

- Indiquer la date de la recherche
- Distinguer "officiel" vs "communauté"
- Si rien de nouveau → dire que le studio est à jour
