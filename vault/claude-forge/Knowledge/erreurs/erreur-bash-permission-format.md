---
titre: "Erreur : mauvais format permissions Bash dans settings.json"
resume: "Bash(git commit:*) avec deux-points au lieu de Bash(git commit *) avec espace — permissions cassees sur 9 fichiers"
aliases:
  - bash permission format
  - settings permission syntax
  - Bash colon bug
  - "permission Bash deux-points"
  - "settings.json permissions cassees"
type: erreur
auteur: claude
derniere-maj: 2026-04-22
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
---

# Erreur : mauvais format permissions Bash dans settings.json

## Ce qui s'est passe

Utilise `Bash(git commit:*)` avec deux-points au lieu de `Bash(git commit *)` avec espace dans les permissions allow de settings.json. Propage sur **9 fichiers** dans 7 projets (claude-forge, ia_back, neo_ia, neoteem-brain, bdd, neopsql, neoauth).

## Pourquoi c'etait une erreur

- Le format `Bash(prefix:*)` ne matche aucune commande — les permissions etaient silencieusement cassees
- Claude demandait la permission a chaque commande git, bash, ls, etc.
- Aucune erreur explicite, juste des prompts de permission inattendus
- L'utilisateur a cru que c'etait un probleme de session ou de config

## Le bon format

```json
"Bash(git *)"          // toutes les commandes git
"Bash(git commit *)"   // uniquement git commit
"Bash(ls *)"           // ls
"Bash(cd * && git *)"  // cd + git (quand Claude prefixe avec cd)
```

**JAMAIS** de `:` entre le prefix et le `*`.

## Ce qu'il fallait faire

Verifier la documentation Claude Code ou chercher sur le web AVANT de propager un format de syntaxe dans plusieurs fichiers. Une erreur de format propagee = dette multipliee par le nombre de fichiers.

## Liens

- [[claude-code-settings]]
- [[permissions-bash]]
