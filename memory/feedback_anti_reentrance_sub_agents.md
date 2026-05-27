---
name: anti-reentrance-sub-agents
description: "Sub-agent ne peut PAS invoquer un autre sub-agent (boucle infinie + tool_use conflits). Doctrine Anthropic implicite. Pattern d'escalade = STOP + signal ESCALADE REQUISE markdown vers session principale."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Quand tu ecris `agent.md` (sub-agent type) et que la tache touche un scope d'un autre sub-agent, ne JAMAIS utiliser les mots **"deleguer a X"** ou **"rediriger vers X"** dans la section Hors scope. Ces formulations suggerent une invocation Agent() depuis le sub-agent, interdite par doctrine.

Pattern canonique : **STOP + ESCALADE REQUISE** (signal markdown structure vers la session principale qui orchestre).

**Why:** Detection in-situ par Raphael session 23 mai 2026. J'avais ecrit dans dev-neochat.md commit 6426e8a et dev-shared-utils.md commit f39794d "Hors scope (deleguer) → dev-shared-utils". Raphael : "un sub-agent peut pas appeler de sub-agent je crois comment résoudre le souci ?". Verif doctrine [[comment-creer-agent]] section Architecture anti-pattern : "Un sub-agent ne devrait pas avoir le tool Agent sauf cas explicite documente". Risques : boucle infinie + tool_use partages conflictuels + debugging impossible (transcripts JSONL fragmentes).

**How to apply:** Pour TOUT agent.md de type sub-agent, dans la section Hors scope :

1. Eviter mots "deleguer", "rediriger", "appeler X" sans clarification
2. Preferer formulation explicite : **"STOP + escalade session principale"**
3. Inclure le format markdown ESCALADE REQUISE avec 5 champs obligatoires :
   - **Detection** : description precise tache hors scope
   - **Raison** : pourquoi hors scope
   - **Agent recommande** : sub-agent cible (ou architect-deep si breaking)
   - **Etat actuel** : fichiers touches, etat du repo
   - **Suite recommandee** : prompt pret-a-l'emploi pour la session principale
4. Preciser : "tu **NE TENTES PAS** d'invoquer l'autre agent via le tool Agent"
5. NE PAS inclure `Agent` dans le frontmatter `tools:` du sub-agent (sauf cas explicite documente type orchestrateur tests paralleles)

Reference complete : [[anti-reentrance-sub-agents-pattern-escalade]] vault forge (note canonique 8 aliases + 2 exemples concrets).
