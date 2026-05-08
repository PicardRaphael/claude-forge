---
titre: "Erreur — Keyword stuffing dans descriptions YAML skills"
resume: "Descriptions bourrées de triggers FR entre guillemets au lieu de triggers sémantiques anglais"
aliases:
  - "erreur keyword stuffing"
  - "description YAML bourree"
  - "skill description triggers"
  - "keyword stuffing descriptions"
  - "descriptions non semantiques"
type: erreur
auteur: claude
derniere-maj: 2026-04-23
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
---

# Erreur — Keyword stuffing dans descriptions YAML

## Ce qui s'est passe

En creant 4 skills pour le plugin neoteem-backlog-hub, j'ai ecrit des descriptions YAML comme :

```
description: ... Use when the user says "bonjour", "mon programme", "prepare-moi pour la reunion", "reponds a ce mail", "reponds au mail de X", "resume mes mails", "j'ai rate quoi", "trouve-moi un creneau" ...
```

## Pourquoi c'etait une erreur

1. **Claude fait du matching semantique, pas du keyword matching** — lister des phrases exactes entre guillemets n'ameliore pas le routing, ca dilue le signal
2. **Melange FR/EN** — les descriptions doivent etre en anglais (regle forge)
3. **Trop longues** — descriptions > 200 chars perdent en precision
4. **Violation des regles connues** — description = trigger semantique en 3e personne, pas "Use when the user says X, Y, Z"

## Correction appliquee

Avant :
```
Use when the user says "bonjour", "mon programme", "prepare-moi pour la reunion", "reponds a ce mail", "reponds au mail de X"...
```

Apres :
```
Use when the user greets, asks about their agenda, prepares for a meeting, replies to or searches for emails, wants a mail summary, or needs to find available time slots.
```

## Regle a retenir

**Description = verbes d'intention semantiques en anglais.** Pas de phrases entre guillemets, pas de FR, pas de liste exhaustive de formulations. Claude comprend l'intention, pas les mots exacts.

## Liens

- [[erreur-edit-direct-skills]]
- [[Best practices Boris Thariq]]
