---
name: import-ajoute-pas-remplace-automemory
description: "@import dans CLAUDE.md AJOUTE une source mémoire, ne remplace PAS l'auto-memory native ~/.claude/projects/. Les deux coexistent et divergent (test 27 mai : 231L repo vs 229L native tronquée, 2 items manquants). Désactiver la native pour single source."
metadata:
  type: feedback
---

Test de validation de l'architecture mémoire portable (27 mai 2026, session dédiée) : l'`@memory/MEMORY.md` versionné dans CLAUDE.md (L100) charge BIEN le `<repo>/memory/MEMORY.md` portable — étiqueté *"checked into the codebase"* dans le contexte injecté. Le mécanisme `@import` fonctionne.

**Mais l'auto-memory native ne disparaît pas pour autant.** Le harness continue d'injecter `~/.claude/projects/<repo-encoded>/memory/MEMORY.md` en parallèle (bloc *"user's auto-memory, persists across conversations"*). Résultat : **double-source simultanée**, et elle **diverge** :
- Repo : 231 lignes, commence à `claude-forge-self-contained-rien-hors-clone` + `cd-sous-dossier-fausse-chemins-relatifs`.
- Native : 229 lignes, **tronquée au chargement** (`WARNING: Only part of it was loaded`), commence directement à `commit-message-no-herestring-bash-tool` — les 2 premiers items du repo manquent.

**Why :** L'`@import` est un mécanisme ORTHOGONAL qui s'AJOUTE au défaut, il ne l'écrase pas. C'est précisément la divergence silencieuse à 2 sources de vérité que l'option "script de sync" avait été rejetée pour éviter ([[decision-memoire-dans-le-repo]]) — sauf qu'ici elle réapparaît par la porte de derrière, sans script. Le `git status` montre `D .claude/projects/.../memory/MEMORY.md` : la suppression de la native est stagée mais le harness la régénère/réinjecte tant qu'elle existe sur disque ou que l'auto-memory reste activée.

**How to apply :** Après avoir mis en place `@import` pour une mémoire portable, NE PAS considérer la migration finie au seul test "l'@import charge le repo". Vérifier qu'il n'y a pas une 2e source native injectée en parallèle (chercher le bloc *"user's auto-memory"* dans le contexte). Pour atteindre la single source visée : désactiver l'auto-memory native (réglage settings à confirmer) OU vider/supprimer `~/.claude/projects/<encoded>/memory/`. Tant que les deux coexistent, le contexte porte ~460 lignes de mémoire redondante/divergente + risque de lire une version tronquée obsolète. Lié à [[architecture-decision-memoire-portable-import]] (le raisonnement se terminait sur "reste à valider par test" — c'est ce test).
