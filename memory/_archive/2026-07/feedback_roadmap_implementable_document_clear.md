---
name: roadmap-implementable-document-clear
description: "Un plan d'action différé doit être self-contained (chemins exacts, skeleton, tests, capitalisation, dépendances) — implémentable sans recharger le contexte de la session qui l'a produit."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a69d9c8e-be6b-4653-abfc-532e2dc0ce5d
---

Quand une session produit un plan d'action qu'on n'implémente PAS tout de suite (option "on fait ça en session dédiée /clear"), la roadmap doit être enrichie pour être implémentable seule. Pour chaque item du plan : (1) chemin exact du composant à créer/modifier, (2) skeleton du contenu attendu (format, triggers, UX), (3) tests prévus si applicable + état des tests existants, (4) capitalisation post-implémentation (note vault ? feedback ? amendement rule ?), (5) dépendances et ordre entre items.

**Why:** Phase 4 Hermes (27 mai 2026) — option 3 retenue (analyse seule, pas d'implémentation). Raphael a explicitement demandé d'enrichir le plan A avant de clore, pour que A1/A2/A3 soient implémentables "sans recharger tout le contexte". C'est le pattern Document & Clear de Boris appliqué à un plan d'action : le .md doit suffire à une session future qui n'a pas vu l'analyse.

**How to apply:** Dès qu'un plan d'action est différé (pas exécuté dans la session courante), avant de clore : transformer la liste de gaps en spécification self-contained. Ne pas laisser des items vagues type "skill /X à créer, effort 2h" — toujours chemin + skeleton + tests + capitalisation + ordre. Lié à [[carte-blanche-commit-push-tranche-pas-revalider]] (exécution directe) et au workflow Boris dans CLAUDE.md.
