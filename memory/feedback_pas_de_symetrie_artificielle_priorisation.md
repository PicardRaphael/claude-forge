---
name: pas-de-symetrie-artificielle-priorisation
description: "Audit multi-axes : ne PAS distribuer du P0/P1 par axe pour l'équilibre. Prioriser sur l'impact réel sans complexe — un audit de N axes peut n'avoir qu'un seul P0. Le reste P2/P3 capitalisé."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Quand j'audite un sujet à plusieurs axes (tests, vitrine, portabilité, sécu, etc.), ne pas forcer un P0/P1 sur chaque axe pour la symétrie. Prioriser franchement sur l'impact RÉEL et PRÉSENT. Un seul axe peut mériter P0 ; les autres vont en P2/P3 capitalisé (différés, avec déclencheur de réactivation).

**Why:** Pattern méta observé 2 fois en 27 mai :
- Phase 2 : un ratio 3:1 de tests adverses "à atteindre" m'a tenté de padder avec des cas hors-scope. L'advisor a corrigé : ratio réel (5.3:1, 8:1) sur des cas in-scope, pas de quota artificiel.
- Phase 3 : 5 axes audités, advisor a tranché net sur 1 seul P0 (cœur MCP non testé). Distribuer du P0/P1 sur 5 axes aurait dilué l'effort sur du théorique.
La symétrie artificielle gonfle le travail sur des trous théoriques et dilue l'effort sur le vrai risque.

**How to apply:**
- Avant de classer un axe P0/P1, test de discrimination : risque réel/présent ou théorique/anticipé ? Impact maximal (cœur) ou cosmétique ? Je le classe haut parce qu'il le mérite ou pour ne pas laisser un axe "vide" ?
- Théorique → P2/P3 + déclencheur de réactivation dans une note ADR.
- Capitaliser franchement les différés vaut mieux qu'un P1 bâclé pour l'équilibre.

Canonique vault : [[audit-puis-vagues-paralleles]] section "Phase 3bis — Pas de symétrie artificielle". Cousins : [[tests-adverses-ratio-3-1-hooks-secu]] (le 3:1 ne doit pas être artificiel), [[bug-caracterise-fix-trivial-vs-couteux]].
