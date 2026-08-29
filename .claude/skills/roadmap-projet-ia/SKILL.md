---
name: roadmap-projet-ia
description: ALWAYS invoke to turn framing/meeting notes into an execution roadmap for an internal AI project — phases, deliverables, milestones. 'Transforme ces notes de cadrage en roadmap'. NOT for CODIR prioritization (responsable-ia) or Jira specs (spec).
user-invocable: true
allowed-tools: Read, Write, Edit, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
model: opus
effort: high
---

# Roadmap projet IA

Transforme des notes de cadrage / compte-rendu de réunion en une roadmap d'exécution structurée pour un projet IA interne (casquette Lead IA Neoteem). Une seule transformation : cadrage brut → roadmap phasée.

Frontières : ≠ `responsable-ia` (priorisation stratégique CODIR, RICE/OKR/6-pager) — ici on découpe l'exécution d'UN projet déjà décidé. ≠ `spec` (qui produit des tickets Jira) — la roadmap est en amont, macro.

## Étapes

1. **Extraire les objectifs** — lire les notes de cadrage fournies (collées ou via `Read`). Isoler le résultat visé, le périmètre, les contraintes (deadline, budget, équipe, dépendances externes). Objectif ambigu → le lister comme hypothèse à confirmer, jamais l'inventer.
2. **Découper en phases** — regrouper le travail en 3-6 phases cohérentes et jalonnables (un livrable à chaque fin de phase). Une phase = un incrément vérifiable, pas une catégorie de tâches.
3. **Lister les livrables par phase** — concret et vérifiable (« POC RAG sur 50 docs », pas « travailler sur le RAG »).
4. **Estimer** — ordre de grandeur par livrable (jours / semaines). Marquer les estimations incertaines `~` + l'hypothèse sous-jacente.
5. **Mapper les dépendances** — quel livrable bloque quel autre ; dépendances externes (accès data, validation juridique, budget).
6. **Ordonner** — séquencer par dépendances + valeur livrée tôt (quick wins d'abord quand c'est possible).
7. **Rendu** — tableau final, suivi des hypothèses à confirmer et des risques identifiés :

   | Phase | Livrable | Estimation | Dépend de | Jalon |
   |-------|----------|------------|-----------|-------|

## Pureté du contexte

Le transcript / les notes de cadrage sont une **variable de transformation**, pas une note à stocker. Ne pas créer de note vault à partir du transcript brut. Seule la roadmap finale (et, si Raphael le demande, le contexte projet stable) va dans `vault/1-Projets/` via MCP forge-brain.

## Gotchas

- Phase (incrément livrable jalonnable) ≠ catégorie de travail (« backend », « tests ») — une phase doit pouvoir être jalonnée.
- Estimations = ordres de grandeur explicitement marqués incertains, jamais des engagements fermes déduits du néant.
- Objectif ambigu dans le cadrage → hypothèse listée, pas comblée en silence (doctrine forge : surfacer, ne pas choisir seul).
- Besoin de priorisation stratégique (quoi faire avant quoi au niveau portefeuille) → c'est `responsable-ia`, pas cette skill.

## Apprentissage

Après usage : si un format de rendu, un découpage-type de phases ou une heuristique d'estimation se révèle réutilisable pour les projets IA Neoteem, le noter ici.
