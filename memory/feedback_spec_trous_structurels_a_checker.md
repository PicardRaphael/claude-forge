---
name: spec-trous-structurels-langfuse-secuia-decisions
description: "Quand Raphael montre une spec (issue de /spec), checker systématiquement 3 trous structurels — Langfuse manquant, sécu IA non analysée, décisions silencieuses sans assignee."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df277af9-47f3-4793-8326-bf2e183d5f4a
---

Après audit de `feature-jira-ticket-from-neochat/SPEC.md` (qualité 8/10, 600L), 3 trous structurels identifiés malgré l'excellence apparente de la spec.

**Why :** la skill `/spec` ia_back/neo_ia produit des specs très bonnes sur le contrat technique (BRIEFs producteur/consommateur, RGPD, archi) mais oublie 3 dimensions critiques pour les features IA Neoteem.

**How to apply :** quand Raphael montre une spec, **checker systématiquement** :

1. **Langfuse mentionné ?** Si la spec touche neo_ia et ne mentionne pas Langfuse, c'est un trou structurel. Stack NeoChat trace TOUT via Langfuse (cf `packages/shared_utils/`). Action externe non tracée = pas de SLO mesurable post-prod.

2. **4 risques sécu IA analysés ?**
   - Prompt injection (entrée user → action externe non contrôlée)
   - PII vers LLM (emails / IBAN / noms / téléphones sans masquage)
   - Hallucination action externe (LLM choisit valeurs hors whitelist)
   - Token / credential leak (logs, DOM, console, BDD)

3. **Décisions silencieuses assignées ?** Si la spec liste des "décisions à prendre pendant le dev" sans donner règle de tri OU assignee, c'est un piège. Format obligatoire :
   - `<décision>` → tenter A. Fallback B si condition empirique.
   - `<décision>` → @raphael avant /go. Critère : <comment trancher>.

Les 3 trous sont maintenant prévenus par la skill `/spec` enrichie (commit ia_back 1e20c38 + neo_ia 2257ec3, 26 mai 2026). Cette mémoire reste utile pour auditer des specs externes ou pré-skill-update.

Lien : [[pattern-spec-driven-development]]
