---
name: bash-permission-format
description: Format correct des permissions Bash dans settings.json — espace, jamais deux-points
type: feedback
originSessionId: e77630b2-f4bd-4590-9fdc-a7261be2f68f
---
Le format correct pour les permissions Bash dans settings.json est `Bash(git commit *)` avec un **espace** avant le `*`, PAS `Bash(git commit:*)` avec un `:`.

Le format `Bash(prefix:*)` ne matche rien du tout — les commandes ne sont jamais autorisees et Claude demande la permission a chaque fois.

**Why:** Erreur propagee par moi sur 9 fichiers settings across claude-forge, ia_back, neo_ia, neoteem-brain, bdd, neopsql, neoauth. Toutes les permissions Bash etaient cassees silencieusement.

**How to apply:** A chaque fois qu'on ecrit ou modifie une permission Bash dans un settings.json, utiliser le format `Bash(command_prefix *)` avec un espace. Verifier systematiquement qu'aucun `:` ne se glisse dans le pattern. Exemples corrects :
- `Bash(git *)` — toutes les commandes git
- `Bash(git commit *)` — uniquement git commit
- `Bash(ls *)` — ls
- `Bash(bash .claude/skills/script.sh *)` — script specifique
