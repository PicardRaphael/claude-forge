---
name: feedback-reviole-3x-regle-insuffisante
description: Un feedback comportemental existant re-violé ≥3 fois (malgré sa présence en mémoire chargée) = signal que la règle écrite ne suffit pas. Ne pas juste ré-enrichir le texte — formuler un réflexe pré-action concret OU envisager un garde-fou structurel (hook). La répétition de l'enrichissement sans changement de comportement = boucle.
trigger: encore, deja dit, tu recommences, re-viole, toujours pareil
metadata:
  type: feedback
---

Quand je re-viole un feedback mémoire qui existe DÉJÀ et est chargé en contexte (ex : `mcp-alias-ambigu-chemin-exact` violé 3× les 27 mai), le réflexe « j'enrichis le feedback » ne corrige pas la cause. Le texte était déjà correct ; c'est l'application au moment de l'action qui manque.

**Why:** 27 mai — `append_note(file="log")` puis `append_note(file="log vault")` au lieu d'éditer le chemin exact, alors que le feedback disait noir sur blanc « NE JAMAIS append_note par alias sur stem multi-dossier, Edit chemin exact ». 3e violation du même feedback. Ré-enrichir le texte une 4e fois ne briserait pas la boucle.

**How to apply:**
- Feedback re-violé 1× → ré-enrichir suffit. Re-violé ≥3× malgré présence en contexte → STOP, le problème n'est plus le texte.
- Formuler un **réflexe pré-action** ancré sur le déclencheur concret : « avant TOUT `append_note`, vérifier que le stem est unique dans le vault ; sinon Read+Edit chemin exact ».
- Si le réflexe est mécanisable à 100% → candidat hook (la doctrine 22 mai autorise les hooks lint/scope, et un garde sur `append_note(file=<stem multi-dossier>)` est un garde de scope, pas de workflow).
- Marquer le compteur de violations DANS le feedback re-violé (« 3e violation ») pour rendre le signal visible à la prochaine lecture.

Cf [[mcp-alias-ambigu-chemin-exact]] (le feedback re-violé), [[recurring-meta-anti-pattern]] (workaround ≥2× = bug — analogue côté code).
