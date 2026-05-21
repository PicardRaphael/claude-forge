---
titre: "Déploiement Opus→Sonnet pushé sur 3 repos sans advisor ni DA"
resume: "Changement modèles agents pushé sur forge+ia_back+neo_ia avant validation advisor/DA. 3 agents mal switchés (jugement pas exécution), commit messages trompeurs ('Advisor Strategy' ≠ model downgrade), 3 mémoires contradictoires."
aliases:
  - "erreur deploy sans DA"
  - "erreur opus sonnet sans advisor"
  - "erreur push avant validation"
  - "model downgrade sans review"
type: knowledge
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/erreur"
  - "#erreur/comportement"
  - "#domaine/claude-code"
---

## Ce qui s'est passé

Session 2026-05-21 : analyse CwC 2026 → décision de passer certains agents Opus en Sonnet (Advisor Strategy pattern). Les changements ont été pushés sur 3 repos AVANT de consulter advisor ou DA.

## Pourquoi c'était une erreur

1. **3 agents mal switchés** : test-writer, validator, refactor-pg-function = travail de jugement (edge cases, bug-finding, traduction architecturale), pas d'exécution mécanique. L'advisor l'a identifié immédiatement.
2. **Commits trompeurs** : disaient "Advisor Strategy pattern" alors que c'est juste du model downgrade. La vraie Advisor Strategy = tool-based Sonnet→Opus dans un même agent (API Messages).
3. **3 mémoires contradictoires** : feedback_all_opus (zero sonnet), feedback_opus47_workflow (gates=sonnet), état réel (mix). Piège à boucle de reverts.

## Quoi faire à la place

1. Identifier les agents par type (jugement vs exécution) AVANT de changer
2. Lancer advisor avec la proposition AVANT de coder
3. Lancer DA AVANT de push
4. Nommer honnêtement ce qu'on fait ("model downgrade pour économie" pas "Advisor Strategy")

## Liens

- [[critique-2026-05-21-repartition-opus-sonnet]]
- [[Effort Levels Guide]]
- [[Code with Claude 2026]]
