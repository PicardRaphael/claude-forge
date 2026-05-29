---
name: spec-brief-distant-repo-scope
description: BRIEF généré pour un repo distant = CONTRAT + ce que JE fais. JAMAIS fichiers internes ou paths du repo distant.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec62a52f-d59f-492b-9fcb-814a443ac0e4
---

Cf [[pattern-spec-driven-development]] (doctrine : BRIEF multi-repo = QUOI pas COMMENT, architecture M/L/XL, BRIEF-PRODUCTEUR avec section Fichiers vs BRIEF-CONSOMMATEUR sans, cross-BRIEF contradiction detection, déploiement /spec). Doctrine producteur/consommateur + diagnostic + verdict DA : [[critique-2026-05-21-brief-distant-template-spec]].

**Cas empirique(s) :**

- **Incident Jérôme (2026-05-20)** : BRIEF généré depuis ia_back pour neo_ia prescrivait fichiers/modules internes de neo_ia → le dev a suivi la prescription, tout repris quand elle ne collait pas à son archi. Détail complet et verdict DA dans [[critique-2026-05-21-brief-distant-template-spec]].
- **Implémentation 2026-05-21 (ia_back + neo_ia)** : refonte /spec producteur/consommateur (SKILL.md Phase 1 demande le rôle ; BRIEF-CONSOMMATEUR sans section Fichiers, "Surface à consommer" verbatim depuis SPEC.md + Intention attendue + Anti-patterns checklist ; contrat canonique SPEC.md avec bloc json-schema embed — markdown + json-schema, pas OpenAPI, choix advisor pour volume Neoteem 5-10 features L/an ; hook PostToolUse `spec-brief-boundary-guard` qui blacklist patterns internes du repo distant, .ts côté ia_back et .py côté neo_ia).
- **Commits** : ia_back `4f2725f` + `d3adce5` (cleanup), neo_ia `7696635`.

Lié : [[pattern-spec-driven-development]], [[checklist-before-modify-mandatory]], [[subagent-autocommit-violation]], [[forge-is-personal]]
