---
titre: "Critique — Template BRIEF-DISTANT pour /spec multi-repo"
aliases: ["critique brief distant", "DA brief consommateur", "spec cross-repo critique"]
resume: "Verdict devil's advocate sur la refonte BRIEF producteur/consommateur de /spec — 3 bloquants identifiés (asymétrie rôles, duplication contrat, advisory vs hook) → fix appliqué"
derniere-maj: 2026-05-21
type: critique
auteur: devils-advocate
tags: ["#type/critique", "#domaine/claude-code", "#domaine/cross-repo", "#projet/neoteem"]
---

## Contexte

Refonte de la skill `/spec` (ia_back + neo_ia) après l'incident "Jérôme" (2026-05-20) où un BRIEF généré depuis ia_back pour neo_ia prescrivait des fichiers/modules internes de neo_ia → dev a suivi, tout repris.

Proposition initiale : template `BRIEF-DISTANT.md` symétrique avec interdiction explicite de mentionner internes du repo distant.

## Verdict DA

**Bloquants : 3 | Avertissements : 6 | Verdict : LIVRER AVEC CORRECTIONS**

### Bloquant 1 — Asymétrie source/destination non modélisée
"Template symétrique" est faux : dans une feature donnée, un seul des deux repos est PRODUCTEUR du contrat. Symétrie de structure ≠ asymétrie de rôle. Sans rôle explicite, le bug Jérôme se reproduit.
→ Fix : rôles producteur/consommateur inscrits dans SPEC.md `## Repos touchés` colonne `Rôle`, demandés en Phase 1.

### Bloquant 2 — Contradiction structurelle avec template L existant
SPEC.md L contient déjà `## Contrat d'interface` (lignes 116-131). Rajouter le contrat dans BRIEF-DISTANT.md = deux sources de vérité → drift garanti.
→ Fix : BRIEF-CONSOMMATEUR cite verbatim depuis SPEC.md, pas de duplication.

### Bloquant 3 — Aucun enforcement, juste une "note"
"Le template INTERDIT explicitement (avec note)" = advisory = 80% compliance (cf. `feedback enforce-not-advise`). Negative prompting anti-pattern Claude.
→ Fix : hook PostToolUse `spec-brief-boundary-guard` qui grep paths internes du repo distant + omission de la section "Fichiers" par construction (pas par interdiction textuelle).

## Avertissements clés

- "Code d'erreur exhaustifs" sous-spécifié : producteur ne connaît pas ses erreurs réelles avant impl. → CONTRACT.md vit avec le code.
- "Raison métier des choix" dangereuse cross-repo : raisons internes du producteur ≠ utiles au consommateur.
- Anti-patterns mélange contradictions de contrat (id vs message_id) et d'ownership (qui crée) — niveaux différents.
- Maintenance manuelle de la symétrie ia_back ↔ neo_ia : 2 copies à maintenir, drift à 3 mois garanti (pattern observé sur `/decompose-ticket`).

## Alternatives non considérées initialement

- OpenAPI/JSON-schema attaché (`contracts/api-spec.json` — pattern GitHub Spec Kit) : tranché par advisor en faveur de markdown + bloc json-schema embed pour le volume Neoteem (5-10 features L/an).
- Contract-as-code (gen types Zod + pydantic depuis schéma unique) : ROI <30 contrats/an douteux, écarté.
- Spine Pattern (meta-repo coordination) : référence valide mais hors scope court terme.
- BRIEF inversé (consommateur demande endpoint inexistant) : non adressé dans cette itération.

## Implémentation finale (2026-05-21)

- SKILL.md Phase 1 demande rôle producteur/consommateur
- BRIEF-PRODUCTEUR garde section Fichiers (paths locaux légitimes)
- BRIEF-CONSOMMATEUR sans Fichiers, "Surface à consommer" verbatim + Intention attendue + Anti-patterns checklist
- Contrat canonique dans SPEC.md avec bloc json-schema embed
- `contradiction-prompt.md` patché avec Exemple 5 "Prescription cross-repo"
- Hook `spec-brief-boundary-guard` (PostToolUse) déployé : .ts ia_back, .py neo_ia (respect `hooks-same-stack`)

**Rejeté en cours** : single-source claude-forge + script deploy (proposé par advisor, retiré par Raphael — claude-forge reste personnel, repos autonomes via `repo-autonomy-mandatory`).

## Patterns à mémoriser

1. Toute proposition de "template alternatif" doit être challengée sur 3 axes : single-source-of-truth, enforcement (hook vs advisory), asymétrie de rôles.
2. Negative prompting ("ce template INTERDIT X") = anti-pattern Claude. Préférer structure qui rend X impossible (omission par construction).
3. Diagnostic d'une skill /spec multi-repo : commencer par `output-templates.md`, pas par le SKILL.md.

## Liens

- [[pattern-spec-driven-development]]
- [[pattern-spec-skill-deployment]]
- [[erreur-stop-critique-position-gotcha-fin]]
- [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]]
