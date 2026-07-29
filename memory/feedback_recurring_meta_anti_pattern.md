---
name: recurring-meta-anti-pattern
description: "3 fois en 2 jours j'ai proposé une refonte structurelle suite à 1 incident, malgré la règle Jarvis documentée hier"
trigger: refonte, restructurer, repenser, incident, workaround
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81809796-b0ad-4ce1-be46-26766cf16768
---

Cf [[raisonnement-kill-tdd-strict-hooks-mai-2026]] (doctrine : règle Jarvis "workaround ≥ 2 fois = bug à diagnostiquer, pas workflow à mémoriser" + raisonner par friction/valeur, pas par budget de comptage).

**Pattern observé** : face à un seul incident utilisateur (TDD frustrant, 12 mocks bloqués, DA qui boucle), réflexe systématique de proposer une refonte structurelle de doctrine. À chaque fois, le DA a tranché "BLOQUER refonte, fix minimal suffit".

**Cas empirique(s) — 3 occurrences en 2 jours :**
- 21 mai soir — Frustration TDD → "refonte 16 → 6 hooks" → DA "non, 3 kills ciblés"
- 22 mai matin — 12 mocks bloqués → "refonte allowlist exhaustive 2 repos" → DA "non, exemption tests par-pattern suffit"
- 22 mai soir — DA qui boucle → "renversement doctrine vault sur 8 agents" → DA "non, juste DRY"

**Garde-fou empirique (cran 1/2/3)** : AVANT de proposer une refonte structurelle (architecture, doctrine, multi-repo), lister cran 1 (fix minimal), cran 2 (fix ciblé), cran 3 (refonte). Si je commence par cran 3, c'est suspect. Vérifier (a) 1 incident ou plusieurs ? (b) cran 1 essayé ? (c) le DA validerait-il cran 3 ? Dérive cognitive de fatigue/frustration : règle vault oubliée à 11h près, puis à 8h près, trois fois.

**Liens** : [[raisonnement-kill-tdd-strict-hooks-mai-2026]], [[critique-2026-05-22-architect-guard-allowlist]], [[critique-2026-05-22-vault-doctrine-renversement]]
