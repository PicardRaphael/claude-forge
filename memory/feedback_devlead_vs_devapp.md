---
name: devlead-vs-devapp-dispatch
description: "Utiliser dev-lead quand le fix traverse les frontières d'apps dans un monorepo, dev-app sinon"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 649f50c5-33e7-4af3-a91c-04ff856cc277
---

Fix cross-app (libs core + plusieurs apps) → dev-lead. Fix intra-app → dev-neochat/dev-neomail/dev-neodoc.

**Why:** dev-lead a la vue monorepo entière et la légitimité de toucher libs/ + apps/*. Les agents app-spécifiques connaissent mieux leur app mais ne devraient pas modifier les libs partagées ni les fichiers d'autres apps.

**How to apply:** Avant de dispatcher un fix dans neo_ia, vérifier quels fichiers sont touchés. Si ça reste dans `apps/<une-app>/` → agent app-spécifique. Si ça touche `libs/` ou plusieurs apps → dev-lead.
