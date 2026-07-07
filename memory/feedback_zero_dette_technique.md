---
name: zero-dette-technique-nettoyer-completement
description: "Quand on découvre une référence morte / drift / incohérence dans les .claude/, nettoyer COMPLÈTEMENT (tous fichiers vivants) immédiatement, pas \"on verra plus tard\"."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df277af9-47f3-4793-8326-bf2e183d5f4a
---

Quand une dette technique est découverte (référence morte, drift de nommage, incohérence entre rules), Raphael veut le nettoyage COMPLET immédiat sur tous les fichiers vivants — jamais "hors scope, on verra plus tard".

**Why :** 27 mai 2026 — drift `architect-quick` (agent qui n'existe pas, c'est la skill architect-sanity-check) trouvé dans 5 fichiers de rules + 1 description d'agent sur 2 repos. J'avais proposé de laisser pour plus tard ("hors scope tâche du jour"). Raphael : "Comble je veux plus de dette technique." Réponse claire : on nettoie tout, maintenant.

**How to apply :**
- Dès qu'un grep révèle une référence morte / incohérence → la corriger dans TOUS les fichiers vivants
- Distinguer fichiers VIVANTS (rules, agents, skills, CLAUDE.md → corriger) des LOGS historiques (RECAP.md, journalier.md → laisser, c'est la trace de ce qui s'est passé)
- Vérifier exhaustivement avec grep AVANT de déclarer "zéro dette" (cf [[feedback_verify_exhaustive_claims]])
- Ne PAS dire "hors scope, plus tard" sur de la dette — la dette ne se résorbe jamais toute seule

Lien : [[methode-pivoter-doctrine]], [[pattern-spec-driven-development]]
