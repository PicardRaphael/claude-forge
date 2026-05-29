---
name: anti-reentrance-sub-agents
description: "Sub-agent ne peut PAS invoquer un autre sub-agent (boucle infinie + tool_use conflits). Doctrine Anthropic implicite. Pattern d'escalade = STOP + signal ESCALADE REQUISE markdown vers session principale."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Cf [[anti-reentrance-sub-agents-pattern-escalade]] (doctrine : sub-agent ne peut pas invoquer un autre sub-agent ; pattern STOP + format ESCALADE REQUISE 5 champs vers la session principale ; anti-patterns "deleguer"/"rediriger" ; `Agent` hors frontmatter `tools:`).

**Cas empirique(s) :**

- Detection in-situ par Raphael session 23 mai 2026 (neo_ia). J'avais ecrit "Hors scope (deleguer) → dev-shared-utils" dans `dev-neochat.md` commit **6426e8a** et dans `dev-shared-utils.md` commit **f39794d**. Raphael : "un sub-agent peut pas appeler de sub-agent je crois comment résoudre le souci ?". Verif doctrine [[comment-creer-agent]] section Architecture anti-pattern.
