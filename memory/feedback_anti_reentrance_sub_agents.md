---
name: anti-reentrance-sub-agents
description: "Escalade STOP + signal ESCALADE REQUISE vers session principale = DÉFAUT recommandé (contexte propre, coût maîtrisé). Prémisse « sub-agent ne PEUT PAS invoquer Agent » PÉRIMÉE depuis CC v2.1.172 (nesting possible) — le design survit, pas l'impossibilité."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Cf [[anti-reentrance-sub-agents-pattern-escalade]] (pattern STOP + format ESCALADE REQUISE 5 champs vers la session principale ; anti-patterns "deleguer"/"rediriger" ; `Agent` hors frontmatter `tools:`).

**⚠️ AMENDE 16 juin 2026 — prémisse factuelle corrigée :**

CC **v2.1.172 (10 juin 2026)** : « Sub-agents can now spawn their own sub-agents (up to 5 levels deep) ». Le claim « un sub-agent ne PEUT PAS invoquer Agent » est donc **faux techniquement**. MAIS c'est une **amende, pas un pivot** (cf [[amende-vs-pivot-couche-factuelle-design]]) :
- **Couche factuelle** (« impossible ») → corrigée : possible, et hérité par défaut (un agent qui omet `tools:` reçoit `Agent`).
- **Couche design** (escalade vers session principale = défaut) → **survit** : contexte propre, coût maîtrisé (la doc CONFIRME l'explosion de contexte), debugging lisible. Le nesting s'active sélectivement (reviewer→verifier/finding).
- **Nouveau levier d'enforcement** : `disallowedTools: Agent` ou `tools:` explicite sans `Agent` ; `permissions.deny: ["Agent(model:opus)"]` (v2.1.178).
- **Audit corrigé** : grep `^tools:` est TROMPEUR — repérer les agents qui OMETTENT `tools:`. forge sain (5 agents, tous `tools:` explicite) ; à re-vérifier sur ia_back/neo_ia.

Foyers amendés en cohérence (16 juin) : notes vault [[anti-reentrance-sub-agents-pattern-escalade]], [[limites-subagents-claude-code]], [[comment-creer-agent]] + `subagent-creator` SKILL.

**Cas empirique(s) :**

- Detection in-situ par Raphael session 23 mai 2026 (neo_ia). J'avais ecrit "Hors scope (deleguer) → dev-shared-utils" dans `dev-neochat.md` commit **6426e8a** et dans `dev-shared-utils.md` commit **f39794d**. Raphael : "un sub-agent peut pas appeler de sub-agent je crois comment résoudre le souci ?". Verif doctrine [[comment-creer-agent]] section Architecture anti-pattern.
- 16 juin 2026 (run cc-news) : découverte que la prémisse est périmée depuis v2.1.172. Amende multi-foyers via la séquence anti-drift (chercher TOUS les foyers, dont la source amont `comment-creer-agent`).
