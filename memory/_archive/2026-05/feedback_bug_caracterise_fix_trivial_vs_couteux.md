---
name: bug-caracterise-fix-trivial-vs-couteux
description: "Bug caractérisé par un test = arbitrer immédiatement. Fix trivial (isolé, <10L, testé) = fix immédiat. Fix coûteux (refonte, risque) = feedback + phase dédiée. Jamais laisser en flou."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Quand un test adverse / audit caractérise un bug RÉEL (épinglé, pas hypothèse), arbitrer immédiatement entre fix-now et defer — ne jamais laisser en flou "on verra".

**Why:** Validé 27 mai (Phase 2). Le bug delegate-guard substring était trivial (4 lignes à retirer, exact-match déjà présent, test prêt à inverser) → fixé immédiatement plutôt que dormir en feedback. À l'inverse, un fix risqué (refonte) mérite une phase dédiée avec la bonne attention, pas une correction à chaud par envie de clore.

**How to apply:**
- **Trivial** (isolé + <~10L + sans nouvelle dépendance + vérifiable + réversible) → fix immédiat dans la foulée. Inverser le test de caractérisation en regression guard (garder, pas supprimer).
- **Coûteux** (refonte, dépendances multiples, risque régression) → feedback mémoire + test qui épingle le comportement actuel + traiter en phase dédiée.
- Dans les DEUX cas : un test épingle le bug. Jamais masquer.

Note canonique : [[bug-caracterise-fix-trivial-vs-couteux]] (04-Techniques/patterns). Cousin : [[zero-dette-technique-nettoyer-completement]], [[tests-adverses-ratio-3-1-hooks-secu]].
