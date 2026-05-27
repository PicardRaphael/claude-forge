---
name: fix-application-3-vagues-paralleles
description: "Pour appliquer N fix indépendants après audit, structurer en 3 vagues parallèles (doctrine rapide / structurelles / dérives) avec agents spécialisés en parallèle dans chaque vague. Validé Raphael 22 mai sur neo_ia + ia_back."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

**Règle** : Après audit produisant 20-30+ fix indépendants, ne PAS appliquer en séquentiel. Structurer en 3 vagues parallèles.

**Why:**
- Raphael a choisi "Tout (vagues 1+2+3)" sans hésitation sur les 2 audits (neo_ia + ia_back) → preference confirmée
- Séquentiel = 1h+ pour 30 fix. 3 vagues × 4-5 agents parallèles = 15-20 min
- Vagues triées par RISQUE : V1 zéro risque (compteurs, descriptions) → V3 plus surface (renaming, refactor)
- Vérification empirique ENTRE chaque vague (pas juste à la fin) — détecte les dérives sub-agents tôt

**How to apply:**
1. **Vague 1 — Bloquants doctrine** : compteurs, descriptions, effort, matchers, dédup simples. Rapide, zéro risque.
2. **Vague 2 — Bloquants structurels** : renaming rules, fix bloquants spécifiques, nettoyage sédiments. Plus de surface.
3. **Vague 3 — Dérives + optimisations** : renaming naming patterns, dédup rules, CLAUDE.md taille, gotchas vides.

Dans chaque vague, lancer 3-5 agents spécialisés en parallèle (1 message, plusieurs tool calls Agent) :
- `claudemd-optimizer` pour CLAUDE.md + rules
- `agent-creator` pour agents
- `skill-creator` pour skills
- `hook-creator` pour hooks + settings.json

Entre les vagues : Bash vérif empirique (`grep` compteurs, `ls` filesystem, vérif renaming).

**Anti-pattern observé** : sub-agents peuvent lire des états intermédiaires inconsistants pendant vague (cas CLAUDE.md neo_ia : sub-agent a vu "19 rules" parce qu'il a lu après V1 mais avant V2 renaming). Solution : vérif empirique post-vague avant lancer la suivante.

Réf : [[audit-claude-folder-pattern]] section Phase 5.
