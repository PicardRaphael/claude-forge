---
name: ccnews-confronter-existant
description: "cc-news doit confronter chaque finding à l'existant (notes vault + composants) et agir, pas juste résumer"
metadata:
  type: feedback
---

Un run cc-news ne s'arrête pas à chercher + résumer. Pour chaque finding majeur vérifié, confronter à l'existant sur 2 plans : (1) notes vault — modifier la note existante ou en créer une ; (2) composants `.claude/` — le finding rend-il obsolète une skill/agent/hook/rule/CLAUDE.md ? Si oui, le signaler avec reco (gate humaine, délégation aux créateurs). Gravé en étape 7 de la skill cc-news le 2 juin 2026.

**Why:** Demande explicite de Raphael (2 juin). Sans ça, un finding comme `workflow`→`ultracode` (v2.1.160) ne déclenche jamais la vérif d'une rule qui mentionne « workflow » comme déclencheur → drift silencieux entre la veille et la config réelle.
**How to apply:** À chaque cc-news. Anti-cascade : seulement findings MAJEURS vérifiés source primaire, pas les 30 findings bruts. Modification de composant = jamais directe, toujours via gate + agent spécialisé. Cf [[reference_workflow_ultracode_keyword]].
