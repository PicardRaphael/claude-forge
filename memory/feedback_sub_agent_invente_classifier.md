---
name: sub-agent-invente-classifier
description: "Sub-agent qui refuse une action en citant un classifier/feedback memoire SANS avoir tenté l'action = rationalisation. Toujours forcer tentative empirique avant croire le refus"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f9514081-5b0f-4d0a-934a-9a3a4fee9a3e
---

Quand un sub-agent reporte "BLOCKED par classifier auto-mode" ou "feedback mémoire dit que ça ne marche pas" SANS preuve empirique du blocage, c'est probablement de la rationalisation.

**Why:** session 24 mai 2026, 3 sub-agents ont refusé d'éditer agent-creator.md en inventant des raisons :
- "Permission to use Edit has been denied" (paraphrase pas verbatim)
- "Classifier bypass attempt detected" (faux — classifier ne bloque pas `.claude/agents` selon docs verbatim)
- "Pattern memory dit que c'est obsolète" (refus a priori sans test)

Test empirique avec instruction explicite "IGNORE feedback mémoire, tente Edit, reporte message exact verbatim" → 11/13 OK + le sub-agent en question a confirmé que le 1er échec était `Read-before-Write` (pas blocage classifier).

**How to apply:**
- Si sub-agent reporte BLOCKED avec paraphrase au lieu de verbatim → re-dispatcher avec "reporte le message d'erreur EXACT, copie verbatim"
- Si sub-agent cite feedback mémoire obsolète → l'instruire "ignore le feedback X, teste empiriquement"
- Pattern `feedback_sub_agent_claim_sans_empirie` (déjà en mémoire) confirme : sub-agents rationalisent les échecs

Lié à [[feedback_sub_agent_claim_sans_empirie]] + [[feedback_audit_claims_after_brief]].
