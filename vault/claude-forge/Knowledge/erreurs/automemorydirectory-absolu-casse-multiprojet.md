---
titre: "autoMemoryDirectory en chemin absolu casse le multi-repos"
resume: "Gotcha Claude Code : autoMemoryDirectory est un réglage GLOBAL (user-scope). En chemin absolu vers <repo>/memory/, il s'applique à TOUS les repos → fusion de toutes les mémoires dans un seul dossier. Validé sur un repo isolé, cassé sur le workflow réel multi-projets. La variable ${CLAUDE_PROJECT_DIR} n'y est PAS expansée (valeur statique)."
aliases:
  - "automemorydirectory absolu multi-repos"
  - "automemorydirectory global casse"
  - "fusion memoires multi-projets claude code"
  - "autoMemoryDirectory chemin fixe danger"
  - "memoire claude code multi-repos gotcha"
type: erreur
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/memoire"
---
# autoMemoryDirectory absolu casse le multi-repos

## Le gotcha

Pour rendre la mémoire d'un repo portable cross-machine, la première idée est de pointer `autoMemoryDirectory` (settings user-scope) vers `<repo>/memory/` en chemin absolu. Ça marche — pour ce repo, isolé. Mais `autoMemoryDirectory` est un réglage **global** : en chemin absolu, il s'applique à *tous* les repos de la machine. Résultat : les mémoires de neo_ia, ia_back, neoteem-brain, lojii fusionnent toutes dans le dossier du repo qu'on visait. Validé sur le cas isolé, cassé sur le workflow réel multi-projets.

## La piste morte

`autoMemoryDirectory: "${CLAUDE_PROJECT_DIR}/memory"` résoudrait par-repo. Vérifié empiriquement (doc + env shell) : la variable **n'est PAS expansée** dans ce champ — la valeur est traitée comme un chemin statique. Piste morte.

## Le test décisif

La question discriminante n'était pas « est-ce que ça marche pour ce repo ? » mais « est-ce que ça marche quand il y a 5 repos ? ». Un mécanisme validé sur le cas simplifié d'un seul repo peut être faux sur l'environnement réel multi-projets. Réflexe : avant de valider un réglage **global** pour résoudre un besoin observé sur UN projet, vérifier son impact sur les AUTRES.

## La résolution

Le scoping par-repo est DÉJÀ le défaut (chaque repo a son dossier `~/.claude/projects/<encoded>/memory/`). Le problème n'apparaît que si on force un chemin fixe. Donc ne rien forcer côté auto-memory native ; utiliser un mécanisme **orthogonal** qui s'ajoute sans écraser le défaut : `@memory/MEMORY.md` dans le CLAUDE.md versionné. Attention à son revers documenté dans [[import-ajoute-pas-remplace-automemory]].

## Liens

- [[architecture-decision-memoire-portable-import]] — la chaîne de raisonnement complète qui a mené au pivot @import
- [[decision-memoire-dans-le-repo]] — l'ADR mémoire-dans-le-repo
- [[import-ajoute-pas-remplace-automemory]] — le revers du pivot @import (sa note jumelle)
