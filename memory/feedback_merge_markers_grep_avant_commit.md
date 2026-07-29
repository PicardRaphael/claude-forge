---
name: merge-markers-grep-avant-commit
description: "Résolution de conflit = grep des 3 marqueurs AVANT commit (un marqueur a été committé le 10 juin)"
trigger: conflit, merge, resolution, marqueur, HEAD, commit
metadata:
  type: feedback
---

Après TOUTE résolution de conflit de merge : `grep -c "<<<<<<<\|>>>>>>>\|^======="` sur les fichiers résolus et exiger 0 AVANT `git add` + commit. Vérifier le compte AVANT, pas dans une chaîne `&&` (grep exit 1 quand 0 match casse la chaîne).

**Why:** 10 juin 2026 — un `>>>>>>> develop` résiduel committé sur la branche us/N2-111279 de Jérôme (l'Edit avait traité un bloc mais pas le second marqueur) ; corrigé par commit de rattrapage. Les conflits CHANGELOG sont STRUCTURELS sur ce workflow (entrées en tête de fichier × branches parallèles) — ça se reproduira.

**How to apply:** chaque merge avec conflit, surtout CHANGELOG.md (fusion zéro-perte des deux blocs : les entrées des deux branches se cumulent).
