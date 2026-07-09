---
name: anthropic-doctrine-biais-full-thune
description: "Anthropic recommandation effort/tokens = biais commercial. xhigh +3% pour 2x tokens vs high. Raphael paie le réel. Tjs questionner \"Anthropic dit X\" vs économie utilisateur."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Recadrage Raphael 26 mai 2026 : *"Anthropic réfléchit avec des tokens illimités, moi je paie le réel. xhigh partout = leur intérêt commercial, pas le mien."*

**Why** : Anthropic recommande "xhigh pour coding/agentic" mais leur benchmark mesure exploration multi-tours longue (cas favorable à xhigh). xhigh = 71% @ 100k tokens. high = ~65-68% @ ~50k. **+3-6 points pour 2x tokens**. Pour 70% des tâches (comparatif structuré, grader, reviewer, designer avec checklist), `high` suffit largement.

**How to apply** :
1. **Questionner systématiquement** une reco Anthropic qui maximise tokens
2. **Calibrer par TYPE de tâche réelle** :
   - Exploration agentique multi-tours profonde → xhigh (architect-deep, refactor-pg, project-auditor, dev-lead L scope)
   - Comparatif structuré vs critères → high (graders, reviewers, designers)
   - Mécanique pur (scan, maintenance, inspection PG) → medium ou low
3. **Mesurer empiriquement** avant de bump : 1 run high vs 1 run xhigh sur même tâche, comparer output
4. **Notre pivot 22 mai 2026 était DANS LE PRINCIPE bon** (xhigh sélectif), juste mal calibré sur 1-2 agents
5. Ne JAMAIS appliquer aveuglément "Anthropic dit xhigh default"

**Liens** : [[effort-opus-47-doctrine-anthropic-2026]], [[opus47-workflow-decisions]]
