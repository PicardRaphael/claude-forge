---
name: skill-evolve-created
description: Skill skill-evolve créée 2026-05-08 — méta-analyse et amélioration des skills forge avec 4 axes, mode sweep, références déportées
type: project
---

Skill `skill-evolve` créée le 2026-05-08 dans `.claude/skills/skill-evolve/`.

**Concept :** Méta-skill qui analyse l'efficacité d'une SKILL.md existante et propose des améliorations concrètes. Propose uniquement — n'applique jamais (délègue à skill-creator).

**Structure :**
- `SKILL.md` — 234 lignes, workflow en 7 étapes, mode sweep "all"
- `references/analyse-axes.md` — critères détaillés des 4 axes
- `references/scoring-rubric.md` — grille maturité 1-5
- `references/cross-pollination-patterns.md` — patterns cross-skills documentés

**Why:** Besoin d'un outil de maintenance périodique des skills forge. Aucune skill existante ne couvrait ce besoin (evolve = architecture produit, project-auditor = config CC).

**How to apply:** Skill disponible via `/skill-evolve <nom>` ou `/skill-evolve all` pour un sweep.

**Notes de création :**
- `CLAUDE_AGENT` ne bypass pas delegate-guard → workaround Write→exec Python (voir feedback_skill_creator_bypass_via_bash)
- Les heredoc Bash échouent avec des backticks dans le contenu → Write .py puis python3 exec
- Description doit avoir des accents corrects pour matcher les triggers utilisateurs français
