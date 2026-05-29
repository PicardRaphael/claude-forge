---
name: test-writer-systematic
description: "test-writer systématique en phase RED (PAS REFACTOR, supprimée). MAX 3 tests/comportement. Effort high (pas xhigh). Révisé 22 mai 2026"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2e41f528-a0ac-468c-a271-ba63d887cbd2
---

Cf [[workflow-claude-code-optimal]] (doctrine : pipeline `architect → test-writer red → dev → code-reviewer`, phase REFACTOR supprimée le 22 mai 2026, effort `high` sauf jugement, Sonnet/Opus split).

> Note : la canonique historiquement liée `[[pipeline-boris-adapte-neoteem]]` ne résout plus dans le vault (mergée/supersédée dans `workflow-claude-code-optimal`). Les éléments ci-dessous (MAX 3 tests + mécanisme `.tdd-bypass`) n'ont PAS de home canonique live → conservés ici.

**Doctrine forge non couverte par une note live (à préserver ici) :**
- **Densité — MAX 3 tests par comportement** : (1) cas nominal happy path, (2) cas limite discriminant (vide/null/erreur principale), (3) edge case unique le plus risqué (optionnel). 2-3 tests bien choisis suffisent. Pattern Willison/Boris 2026 verbatim : *"red-green TDD, it's like five tokens, and that works"*.
- **Bypass TDD** : pour typo/rename/config/hotfix<5L/doc, architect annonce `TESTS: BYPASS` dans son mini-plan S, dev utilise `touch .tdd-bypass` avant la modif.
- test-writer NE LANCE JAMAIS la suite complète — uniquement les fichiers test écrits/modifiés.
- Après bug fix : test de non-régression (le test qui aurait attrapé le bug).
- Description agent : `SYSTEMATICALLY` (pas "Use when user asks").
- Si invoqué en `--phase=refactor` : répondre "Phase refactor supprimée, voir code-reviewer".

**Cas empirique(s) :**
- **Révisé 22 mai 2026** — après audit frustration 4h/feature (ancienne politique "2 passes RED + REFACTOR" doublait le coût pour le même résultat ; code-reviewer fait déjà les edge cases).
- **Anti-pattern interdit constaté** : écrire 6 tests sur 1 SEUL comportement, observé sur `cache_helpers.py` (takeover/known/unknown/empty/no-name/empirical). Overshoot densité.

## Liens
- [[workflow-claude-code-optimal]] — recette complète (recette pipeline + densité + REFACTOR fusionné)
- [[erreur-pipeline-trop-long-frustration]] — pourquoi cette révision (incident cache_helpers détaillé)
- [[feedback_opus47_workflow]] — effort levels révisés (high vs xhigh)
