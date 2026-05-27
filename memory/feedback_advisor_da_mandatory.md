---
name: advisor-da-before-proposing
description: "TOUJOURS lancer advisor + devil's advocate AVANT de proposer ou déployer une architecture/setup, pas après rappel Raphael. 2 incidents documentés."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Quand on propose un setup complet OU quand on déploie des changements cross-repo, TOUJOURS lancer advisor + devil's advocate AVANT.

**Why:** 2 incidents identiques :
1. Session lojii 2026-05-13 — proposé 5 agents/skills sans advisor ni DA. DA a trouvé 4 bloquants.
2. Session CwC 2026-05-21 — déployé Opus→Sonnet sur 3 repos et pushé AVANT advisor. L'advisor a identifié 3 agents mal switchés (test-writer, validator, refactor-pg-function = jugement pas exécution) et que les commits disaient "Advisor Strategy" alors que c'était juste du model downgrade. DA a ensuite trouvé 3 bloquants sur outcomes-test (rubric manquant, rule advisory, évaluation plans vs code).

**How to apply:**
- Changement touchant > 1 repo ou > 3 composants : advisor AVANT de coder, DA AVANT de push
- Changement de modèle/effort sur des agents : advisor pour valider chaque switch individuellement
- Ne JAMAIS push avant que advisor + DA aient validé. L'absence de verdict ≠ verdict positif
