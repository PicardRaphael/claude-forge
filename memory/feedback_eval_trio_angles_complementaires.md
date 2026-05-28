---
name: eval-trio-angles-complementaires
description: Évaluation/audit forge couverte par TRIO complémentaire (qualitatif fin / stratégique / objectif rubric) — chercher les 3 angles avant conclure gap
type: feedback
---

## Règle

Quand utilisateur demande "as-tu un système d'évaluation/audit/qualité X ?", chercher les 3 angles complémentaires AVANT de conclure que rien n'existe :

1. **Qualitatif fin** (1 composant) — analyse profonde, multi-axes, score → `skill-evolve` pour skills forge
2. **Stratégique gros plan** (setup entier) — verdict KILL/EVOLVE/KEEP/MISSING avec evidence → `forge-review` pour forge
3. **Objectif vs critères pré-écrits** (rubric) — PASS/FAIL/PARTIAL gate 80% → `outcomes-test` (générique, templates par type)

Plus `self-check` (conformité YAML/structure déterministe) en socle.

**Why:** Session 28 mai 2026 : Raphael envisageait construire `/eval-component`. Vérification empirique a révélé 3 outils non-redondants couvrent déjà le besoin à 3 angles. Conclure "rien n'existe" sur 1 seul angle = faux gap → construction doublon → confusion dispatch.

**How to apply:**
- Avant proposer/construire un outil d'éval, lister les 3 angles attendus pour ce besoin
- Pour chaque angle, vérifier empiriquement (lecture SKILL.md, pas inférence par nom) si un composant existe
- Si 2-3 angles couverts : ne pas construire, recommander dispatch entre existants
- Si 1 angle manque : étendre l'existant le plus proche, pas nouvelle skill
- Si 0 angle couvert : construction justifiée

**Pattern cousin** : [[feedback_check_before_create_pattern]] (vérifier l'existant avant créer) mais plus spécifique à la classe "évaluation/audit/qualité".
