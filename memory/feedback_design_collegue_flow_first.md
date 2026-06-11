---
name: design-collegue-flow-first
description: "Outiller un collègue = partir du flow (nb commandes) + vérifier l'existant"
metadata:
  type: feedback
---

Quand un setup est destiné à un collègue (« il faut que ça soit facile »), concevoir depuis le flow utilisateur final (combien de commandes il tape) et vérifier ce que les briques existantes du repo couvrent déjà — jamais depuis la mécanique sous-jacente.

**Why:** 11 juin 2026, worktrees neoteem-back-ts : conçu un script new-us.ts (worktree manuel + branche + copie env) alors que `claude -w` + `/feature` suffisaient — l'étape 2 de /feature créait déjà la branche, non vérifié. « Comment Jérôme va faire ? » a tué le script. Cf [[worktree-natif-vs-convention-develop]].

**How to apply:** Avant tout script/wrapper d'outillage : (1) dérouler le flow cible en commandes du point de vue de l'utilisateur final, (2) relire les skills/pipelines existants pour ce qu'ils gèrent déjà, (3) le mécanisme neuf ne se justifie que pour le delta restant.
