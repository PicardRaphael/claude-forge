---
name: workaround-becomes-sediment
description: Un workaround autouse ajouté pour résoudre un bug urgent devient dette permanente si pas loggé — signaler ce risque dès le diagnostic
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4737c3cd-d380-4c1b-b98a-0978cfcbc5cd
---

Pattern observé : un bug urgent (asyncio event loop, flaky tests, etc.) déclenche un fix rapide via fixture `autouse=True` globale. Le fix "marche", personne ne revient dessus, le coût se cumule sur tous les tests pour toujours. Au bout de 6 mois, plus personne ne sait pourquoi c'est là.

**Why:** neo_ia commit 460b597 (5 mars 2026) ajoute `clean_caches` autouse avec 2 gc.collect() pour réparer 77 tests cassés post-bug asyncio (commit aab8a8c). 2 mois plus tard : 16 minutes de tests, root cause asyncio jamais fixée, workaround sédimenté. Coût permanent : ~975s par run complète.

**How to apply:**
- Quand je propose un fix autouse global pour débloquer : TOUJOURS créer une dette technique loggée (`Knowledge/erreurs/` + ticket) avec la condition de retrait ("retirer quand X est fixé")
- Quand je diagnostique un projet lent : chercher `autouse=True` dans conftest.py racine + git log de ce fichier pour identifier les workarounds qui ont sédimenté
- Signaler à l'utilisateur : "ce workaround a un coût X par test, le fixer proprement libérera Y"
