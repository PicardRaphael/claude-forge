---
name: kill-pragmatique-vide-doctrinal-assume
description: KILL pragmatique acceptable quand 0 ref empirique + doublon partiel + aucune canonique vault ne supporte ni contredit. Tracer assumé dans CHANGELOG. Pattern applicable aux audits lifecycle futurs.
metadata:
  type: feedback
---

KILL pragmatique acceptable quand un composant cumule : 0 ref empirique + doublon partiel avec composants conformes + aucune canonique vault ne le supporte ni le contredit.

**Why:** Pendant audit lifecycle 28 mai 2026, `/forge-status` candidat KILL — décision mécanique solide (0 ref hors test + doublon partiel `/recap` + `/install-forge`) mais aucune canonique vault ne le mentionnait dans un sens ou l'autre. Refuser de trancher sous prétexte "pas de canonique" = paralysie. Inventer une canonique post-hoc pour justifier = doctrine drift. Solution médiane : KILL assumé sans support doctrinal, tracer explicitement dans CHANGELOG comme "pragmatique non-doctrinal" pour relecture future.

**How to apply:**
- Avant tout KILL non supporté par canonique vault → vérifier cumul (0 ref + doublon partiel + vide doctrinal)
- Si cumul réuni → KILL acceptable, mais tracer explicite "KILL pragmatique sans support doctrinal" dans le message commit + CHANGELOG
- Backup défensif obligatoire avant exécution (zip ou git stash) — permet restore si canonique émerge après-coup
- Ne s'applique PAS si une canonique existe et contredit (alors KEEP/AMEND obligatoire)
- Ne s'applique PAS si simple 0 ref sans doublon (DORMANTE ACTIVE possible)

Lien : [[pattern-mcp-brief-then-direct]] section "KILL > faire marcher" (critère structurel) ; ce feedback étend au cas vide doctrinal non-structurel.
