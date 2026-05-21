---
titre: "Critique — Optimisations TDD Sprint Contract (ia_back + neo_ia)"
resume: "0 bloquant, 4 avertissements (advisory step 0 ~80% compliance, criteres validation divergent cross-repo, deadlock /go non adresse, monitoring rejections non defini). Proposition chirurgicale, LIVRER AVEC CORRECTIONS."
aliases:
  - "critique tdd optimizations handshake"
  - "DA sprint contract step 0"
  - "critique contrats testables ia_back"
  - "devil advocate tdd handshake 21 mai"
  - "critique architect test-writer handshake"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: devils-advocate
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/neo-ia"
  - "#projet/ia-back"
  - "#domaine/claude-code"
sources:
  - "Session 2026-05-21 — optimisations TDD sprint contract"
---

## Devils Advocate — Optimisations TDD Sprint Contract (ia_back + neo_ia)

**Intention declaree :** Rendre le pipeline TDD plus efficace en ajoutant des contrats testables dans le plan architect ia_back (parite avec neo_ia), en creant un handshake bidirectionnel architect-test-writer (Sprint Contract step 0), et en alignant les rules ia_back sur le pipeline test-first.

---

### Verdict

**Bloquants :** 0 | **Avertissements :** 4 | **Nitpicks :** 2

**Decision recommandee :** LIVRER AVEC CORRECTIONS

Proposition chirurgicale qui applique correctement les lecons de la critique du 19 mai (REWORK). Les 4 bloquants de la proposition originale sont tous evites. Les modifications sont a portee limitee et reversibles. 4 avertissements a corriger ou surveiller.

---

### Si je devais le faire marcher malgre mes objections

1. **Harmoniser les criteres step 0** — ajouter commentaire dans chaque test-writer justifiant POURQUOI les criteres different entre repos (Functional/DeepEval sur neo_ia, absent sur ia_back). Intentionnel = documenter. Accidentel = corriger.

2. **Documenter le comportement /go autonome** — dans quality-gates.md : "Si test-writer refuse en mode autonome, la session principale DOIT re-invoquer architect avec le message de refus, max 1 retry."

3. **Tracker rejections step 0 pendant 30 jours** — <10% = advisory OK. 10-30% = affiner instructions architect. >30% = construire hook contract-guard (pattern marker+guard). Ne pas decider maintenant.

4. **Ajouter "Drizzle migration" comme BYPASS explicite dans la matrice ia_back** — le hook l'exempte, la matrice non. Incoherence document/runtime.

---

### Angle Technique

- AVERTISSEMENT : Sprint Contract step 0 est advisory (~80% compliance attendue per [[erreur-advisory-rules-insuffisantes]])
- AVERTISSEMENT : Criteres validation divergent entre repos sans justification explicite
- NITPICK : Matrice ia_back ne mentionne pas "Migration Drizzle = BYPASS" (hook l'exempte deja)

### Angle Strategique

- Aucun bloquant. Proposition correcte, incrementale, respecte les decisions de la critique precedente.
- AVERTISSEMENT : Mode autonome /go non adresse — test-writer STOP = deadlock silencieux en batch

### Angle Pratique

- AVERTISSEMENT : Si taux rejet step 0 >30%, sera percu comme bruit et retire. Definir criteres succes/echec maintenant.
- NITPICK : Co-localisation tests ia_back vs structure dossier neo_ia = point confusion cross-repo

---

### Vault — Historique pertinent

- [[critique-tdd-neo-ia-proposal]] — 4 bloquants, verdict REWORK. Les 3 modifications actuelles evitent tous les bloquants.
- [[critique-2026-05-21-dispatch-guard-livraison]] — Pattern agent_type confirme, dispatch-guard fonctionne. Sprint Contract = prochain maillon logique.
- [[critique-2026-05-21-color-tdd-cto-mindset]] — Timeline coherente, chaque livrable repond a la critique precedente.
- [[erreur-advisory-rules-insuffisantes]] — 3 incidents, ~80% compliance advisory. Step 0 est advisory → surveiller.
- [[erreur-marker-ttl-blocage-agents]] — Aucun TTL dans cette proposition (lecon appliquee).
