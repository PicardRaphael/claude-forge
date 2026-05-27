---
name: recurring-meta-anti-pattern
description: "3 fois en 2 jours j'ai proposé une refonte structurelle suite à 1 incident, malgré la règle Jarvis documentée hier"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81809796-b0ad-4ce1-be46-26766cf16768
---

**Pattern observé** : face à un seul incident utilisateur (TDD frustrant, 12 mocks bloqués, DA qui boucle), réflexe systématique de proposer une refonte structurelle de doctrine. À chaque fois, le DA a tranché "BLOQUER refonte, fix minimal suffit".

**3 occurrences observées en 2 jours** :
1. 21 mai soir — Frustration TDD → "refonte 16 → 6 hooks" → DA "non, 3 kills ciblés"
2. 22 mai matin — 12 mocks bloqués → "refonte allowlist exhaustive 2 repos" → DA "non, exemption tests par-pattern suffit"
3. 22 mai soir — DA qui boucle → "renversement doctrine vault sur 8 agents" → DA "non, juste DRY"

**Règle stricte à appliquer** :
- Quand je sens l'envie de "refondre structurellement", c'est probablement le pattern.
- AVANT de proposer une refonte, lister cran 1 (fix minimal), cran 2 (fix ciblé), cran 3 (refonte). Si je commence par cran 3, c'est suspect.
- **Workaround ≥ 2 fois = bug à diagnostiquer, pas workflow à mémoriser** (règle Jarvis du raisonnement-kill-tdd-strict-hooks-mai-2026). UN incident ≠ pattern récurrent.

**Why:** Le DA d'hier a posé littéralement cette règle dans le vault, et je l'ai oubliée à 11h près, puis à 8h près. Trois fois. C'est une dérive cognitive de fatigue/frustration qui peut coûter cher si l'utilisateur ne challenge pas.

**How to apply:** À chaque proposition de refonte structurelle (architecture, doctrine, multi-repo), AVANT de la formuler à Raphael, vérifier explicitement : (a) est-ce 1 incident ou plusieurs ? (b) ai-je essayé cran 1 (fix minimal) ? (c) le DA validerait-il cran 3 ?

**Liens** : [[raisonnement-kill-tdd-strict-hooks-mai-2026]], [[critique-2026-05-22-architect-guard-allowlist]], [[critique-2026-05-22-vault-doctrine-renversement]]
