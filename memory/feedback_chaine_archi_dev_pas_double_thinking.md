---
name: chaine-archi-dev-pas-double-thinking
description: Archi Opus produit plan → Dev Sonnet exécute. JAMAIS Opus xhigh sur les deux (double facturation thinking). Sonnet pour exécution avec plan donné = bon pattern.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Pattern soulevé par Raphael 26 mai 2026 : *"L'architecte travaille avec les développeurs, peut-être qu'on fait travailler 2 fois si tous les deux réfléchissent profond."*

**Why** : Si archi (Opus xhigh) produit un plan détaillé puis dev (Opus xhigh aussi) refait du raisonnement profond pour exécuter → double facturation thinking pour un travail déjà fait. Pattern coûteux et redondant.

**Bonne pratique vérifiée empiriquement dans nos repos** :
- **ia_back** : architect-deep (Opus xhigh, plan/read-only) → dev (**Sonnet high**, Write/Edit). ✅ Pas de double thinking profond. Sonnet exécute le plan sans tout réinventer.
- **neo_ia** : 
  - S/M scope : architect-quick (Sonnet, 5 lignes plan) → dev-* (Sonnet) ✅
  - L scope : dev-lead (Opus xhigh) fait TOUT lui-même (archi + code) — pas de délégation Opus→Opus

**How to apply** :
1. **JAMAIS deux Opus xhigh en chaîne** archi → dev sur même feature
2. Archi Opus = plan / spec / contrats. Dev Sonnet = exécution.
3. Si tâche trop complexe pour Sonnet → 1 SEUL agent Opus xhigh qui fait archi+code (pattern dev-lead)
4. Vérifier dans frontmatter : si dev a `model: opus` ET un archi Opus le précède dans le workflow → revoir

**Anti-pattern à détecter** : agent `dev-*.md` avec `model: opus` + `effort: xhigh` qui est appelé après un `architect-*.md` Opus.

**Liens** : [[effort-opus-47-doctrine-anthropic-2026]], [[sonnet-46-supporte-effort-parameter]]
