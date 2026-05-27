---
name: behavioral-test-after-setup
description: "Apres setup/audit/modif massive, produire un prompt de test comportemental PASS/FAIL que Raphael lance en session fraiche"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f5b2dc6e-0c01-4af2-b57a-7b090d010a1d
---

Après tout setup, audit ou modification massive (agents, skills, hooks, rules), livrer une suite de tests comportementaux dans output/.

**Why:** Session 2026-05-21 — les tests ont trouvé 3 vrais bugs (Drizzle fantôme, chemin bdd, api-designer ne consulte pas neo-brain) + 1 faille IDOR. Sans les tests, ces bugs seraient restés invisibles.

**How to apply:**
- Produire le prompt de test AVANT de déclarer le travail terminé
- Critères = observables de transcript (agent invoqué, hook exit 2), pas processus mental
- Prompts avec des noms de fichiers/tables réels du repo (sinon l'architect refuse légitimement)
- Hooks en cascade = 1 sous-prompt par hook (dispatch-guard bloque avant architect-guard)
- Les agents refusent souvent AVANT les hooks (niveau 1 > niveau 2) — c'est le meilleur résultat
- Voir vault [[pattern-behavioral-dispatch-test]] pour le pattern complet
