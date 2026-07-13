---
name: cartographie-exhaustive-avant-delegation
description: "Avant de déléguer une modif à un creator (skill/agent/hook), cartographier le fichier cible par grep EXHAUSTIF — pas les 2-3 lignes supposées. Le brief doit lister TOUTES les occurrences, sinon patch partiel (chemin natif résiduel)."
metadata:
  type: feedback
---

Avant de briefer un sub-agent creator (skill-creator, agent-creator, hook-creator) pour modifier un fichier, la SESSION doit d'abord grep exhaustivement le fichier cible sur tous les patterns pertinents — jamais annoncer "il y a 2 lignes à changer" sur la base d'une lecture partielle. Distinguer dans la cartographie les occurrences ACTIVES (à changer) des occurrences DESCRIPTIVES (mot dans une phrase, titre, format) à ne pas toucher.

**Why:** Session Mémoire Portable (27 mai 2026). Raphael a exigé 3× la cartographie exhaustive avant délégation : "n'annonce pas 2 lignes sans avoir grep le fichier". Sur /recap, le grep a révélé 5 occurrences de patterns mémoire dont 3 descriptives (description, titre, format rapport) et 2 actives — sans le grep, risque de toucher les mauvaises ou d'en rater. Le brief incomplet produit un patch partiel que le creator applique fidèlement (il ne devine pas ce qui manque). Distinct de [[verify-exhaustive-claims]] (grep AVANT déclaration, en aval) : ici c'est AVANT délégation, en amont.

**How to apply:** Avant tout dispatch creator pour modifier un composant : (1) `wc -l` du fichier, (2) grep -ni de tous les patterns concernés, (3) classer chaque occurrence active/descriptive, (4) mettre la cartographie complète dans le brief. Le creator reçoit la liste exhaustive, pas "change ce qui ressemble à X". Vérifier empiriquement le résultat post-dispatch (grep de contrôle). Lié à [[sub-agent-claim-sans-empirie]] et [[session-consulte-vault-avant-brief]].
