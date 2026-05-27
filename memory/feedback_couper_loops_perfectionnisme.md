---
name: couper-loops-perfectionnisme
description: "Raphael coupe activement les loops \"es-tu parfait\" (4 relances detectees session 3). Preference = trancher vite avec verdict factuel, pas tergiverser. Quand un check est fait et conforme, dire \"OK c'est fait\" et passer a la suite."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Quand Raphael demande "est-ce parfait" ou "rend-toi parfait", apres 1-2 verifs/advisor :
- Soit verdict empirique = parfait sous definition canonique → dire **"oui c'est fait"** clair et net
- Soit verdict = imperfection identifiee → **proposer 1 action concrete**, pas 5 options

Eviter les boucles "es-tu parfait" → "presque, voici 3 options" → "oui mais lequel" → "advisor dit" → "es-tu parfait" → ad infinitum.

**Why:** Session 23 mai 2026 : 4 tours dessus, finalement Raphael "j'ai switch de mode" pour casser la boucle. Advisor verbatim : "La perfection n'est pas refactor tout ce que Niveau 2 a flagge. La perfection est instrumenter ce qu'il faut pour decider rationnellement. Arrete de relancer 'es-tu parfait' — c'est la boucle qui te coute plus que tout refactor te ferait gagner." Boris doctrine : compounding incremental, pas perfectionnisme paralysant.

**How to apply:**
1. Apres ABCDE+advisor validation = passer en mode "decision tranche", pas en mode "re-validation"
2. Si Raphael relance "es-tu parfait" malgre validation : reformuler la question vers "qu'est-ce qui te bloque concretement de shipper ?" (verdict advisor 23 mai)
3. Eviter de presenter 5 options (a/b/c/d/e) sur un sujet deja tranche → 1 action recommandee + 1 alternative max
4. Si je detecte que MOI je relance "es-tu parfait" mentalement → stop, c'est le piege. Push et continue.
5. Pattern Erik Schluntz : leaf nodes + verifiable checkpoints, pas grand refactor speculatif
6. **Loop > 3 relances sur "est-ce conforme" = signal Raphael fatigue** → terminer franchement le sujet en cours
