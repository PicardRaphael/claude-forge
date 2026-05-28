---
name: auto-violation-doctrine-fraichement-inscrite
description: "Respecter immediatement la doctrine qu'on vient d'ecrire, pas l'oublier au tour suivant"
metadata:
  type: feedback
---

Quand une regle vient d'etre inscrite dans un composant (skill, CLAUDE.md, rule), elle s'applique IMMEDIATEMENT y compris au prochain artefact produit dans la meme session. Pas de "delai d'absorption" — la regle est doctrine des qu'ecrite.

**Why:** Observe 28 mai 2026. Inscrit dans `done` SKILL.md "description feedback < 80 chars". Tour suivant, cree feedback `chiffre-baseline-brief-verifier-empiriquement` avec resume 92 chars dans MEMORY.md — auto-violation immediate de la regle. Pattern d'oubli en sortie de chantier ("c'est fait, je passe a la suite").

**How to apply:** Apres chaque modification de doctrine en session, garder mentalement la nouvelle regle active pour tous les artefacts produits jusqu'a fin de session. Avant ecriture d'un artefact apparente, relire mentalement les contraintes fraichement inscrites.
