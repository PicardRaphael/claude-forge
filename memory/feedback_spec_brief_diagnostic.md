---
name: spec-brief-distant-repo-scope
description: BRIEF généré pour un repo distant = CONTRAT + ce que JE fais. JAMAIS fichiers internes ou paths du repo distant.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec62a52f-d59f-492b-9fcb-814a443ac0e4
---

Quand `/spec` est lancée depuis un repo A et produit un BRIEF pour un repo B (ex: BRIEF-NEOIA généré depuis ia_back) :

**Le BRIEF distant DOIT contenir** :
- Le contrat sortant complet : endpoint(s), méthode, headers, params, body schema champ-par-champ avec types, schéma réponse exhaustif (200 + erreurs) avec exemples JSON littéraux, auth, codes d'erreur et sémantique
- Ce que A a fait/fournit
- L'intention attendue côté B (objectif métier, cas d'usage déclencheurs)
- Critères d'acceptation observables côté A (logs, requêtes attendues)
- Anti-patterns connus en checklist (id vs message_id, qui crée la ressource, pagination, auth header vs body)

**Le BRIEF distant NE DOIT JAMAIS contenir** :
- Quels fichiers du repo B modifier
- Quel agent/module/composant interne de B toucher
- Quel mapping client B étendre
- La signature du code à écrire dans B
- Toute hypothèse sur l'architecture interne de B

**Why:** A ne connaît pas (et n'a pas à connaître) les internes de B. L'incident Jérôme venait justement de A qui prescrivait à B comment faire = drift + dev hors spec quand B découvre que la prescription ne colle pas à son archi. Symétriquement vrai dans l'autre sens.

**How to apply:**
- Auditer un template multi-repo : section "Fichiers à créer/modifier" pour le repo distant = red flag immédiat, à supprimer.
- Template `BRIEF-DISTANT.md` à créer (réutilisé symétriquement) : sections Contrat fourni + Intention attendue, PAS de section Fichiers.
- Diagnostic d'une skill /spec multi-repo : commencer par `output-templates.md`, pas par le SKILL.md (le SKILL.md gère les gardes-fous d'écriture, c'est rarement le bug ; les templates gèrent le scope du contenu, c'est là que ça fuit).

**Implémentation 2026-05-21 (ia_back + neo_ia)** :
- SKILL.md Phase 1 demande producteur/consommateur (1 question AskUserQuestion)
- Template BRIEF-PRODUCTEUR avec section Fichiers (légitime, paths locaux)
- Template BRIEF-CONSOMMATEUR sans section Fichiers, "Surface à consommer" (verbatim du contrat) + Intention attendue + Anti-patterns checklist
- Contrat canonique dans SPEC.md avec bloc json-schema embed (markdown + json-schema, pas OpenAPI — choix advisor pour volume Neoteem 5-10 features L/an)
- Hook `spec-brief-boundary-guard` (PostToolUse) qui blacklist patterns internes du repo distant dans sections "À faire" et "Surface à consommer"
- Hooks dans la stack de chaque repo : .ts côté ia_back, .py côté neo_ia (feedback `hooks-same-stack`)
- Commits : ia_back `4f2725f` + `d3adce5` (cleanup), neo_ia `7696635`

Lié : [[spec-driven-development-pattern]], [[checklist-before-modify-mandatory]], [[subagent-autocommit-violation]], [[forge-is-personal]]
