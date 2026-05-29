---
name: quartet-analyse-multi-repo
description: "Pattern d'analyse repo en quartet d'agents forge (project-analyzer + project-auditor + codebase-scanner + devils-advocate). Validé neo_ia 25 mai."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9fc162ca-a588-4679-a6fe-8d764e8a155c
---

Pour analyser un repo en profondeur, dispatcher **4 agents forge en parallèle** :

1. **`project-analyzer`** — vue projet haut niveau + recommandations CC
2. **`project-auditor`** — audit `.claude/` par cluster (1 agent par catégorie = agents/skills/hooks/rules+CLAUDE.md)
3. **`codebase-scanner`** — code applicatif réel (étape 1b/1c/1d/5 methode-analyser-repo)
4. **`devils-advocate`** — critique livrables majeurs (conditionnel)

**Why:** Avant 25 mai : `general-purpose` catch-all ou agent local par repo. Solution forge agnostique évite réinventer le prompt à chaque analyse.

**How to apply:** Dispatcher en 1 message multi-Agent dès que user dit "analyse poussée X", "propose-moi config CC pour X", "audit complet". Sub-pattern : 4 project-auditor par cluster `.claude/` + 1 codebase-scanner = 5 sub-agents en //. Puis vagues P0/P1/P2/P3 (cf [[audit-puis-vagues-paralleles]]).

Sources : [[quartet-analyse-multi-repo]] + [[audit-puis-vagues-paralleles]] vault forge.
