---
name: advisor-da-before-proposing
description: "TOUJOURS advisor + DA AVANT de proposer/déployer architecture, pas après rappel Raphael"
metadata:
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Cf rule `.claude/rules/devils-advocate-pipeline.md` (DA conditionnel ciblé livrables majeurs) + [[quartet-analyse-multi-repo]] (advisor strategy Brad Abrams).

**2 incidents empiriques préservés** :
1. **Session lojii 2026-05-13** — proposé 5 agents/skills sans advisor ni DA. DA a trouvé 4 bloquants.
2. **Session CwC 2026-05-21** — déployé Opus→Sonnet sur 3 repos et pushé AVANT advisor. L'advisor a identifié 3 agents mal switchés (test-writer, validator, refactor-pg-function = jugement pas exécution). DA a ensuite trouvé 3 bloquants sur outcomes-test.

**Règle** : changement > 1 repo OU > 3 composants → advisor AVANT coder, DA AVANT push. Absence de verdict ≠ verdict positif.
