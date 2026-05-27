---
name: test-writer-systematic
description: "test-writer systématique en phase RED (PAS REFACTOR, supprimée). MAX 3 tests/comportement. Effort high (pas xhigh). Révisé 22 mai 2026"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2e41f528-a0ac-468c-a271-ba63d887cbd2
---

**Révisé 22 mai 2026** — après audit frustration 4h/feature.

## Règle

test-writer apparaît dans CHAQUE pipeline après architect, AVANT dev (phase RED uniquement).

**Why:** Sans test-writer, dev Sonnet écrit du code sans contrat de vérification. Mais l'ancienne politique "2 passes RED + REFACTOR" doublait le coût pour le même résultat — code-reviewer fait déjà le travail edge cases.

## How to apply (RÉVISÉ)

### Phase RED uniquement (avant dev)

- Pipeline : `architect → test-writer red → dev → code-reviewer → [gates conditionnels] → commit`
- test-writer NE LANCE JAMAIS la suite complète — uniquement les fichiers test écrits/modifiés
- Après bug fix : test de non-régression (le test qui aurait attrapé le bug)
- Description agent : `SYSTEMATICALLY` (pas "Use when user asks")

### Phase REFACTOR — SUPPRIMÉE le 22 mai 2026

❌ Ne PLUS faire de phase REFACTOR. Fusionnée dans code-reviewer (section "Edge cases à ajouter", light, 1-3 max).
✅ test-writer répond "Phase refactor supprimée, voir code-reviewer" si invoqué en --phase=refactor.

### Densité — MAX 3 tests par comportement

Pattern Willison/Boris 2026 ("red-green TDD, it's like five tokens, and that works") :

1. Cas nominal (happy path) — 1 test
2. Cas limite discriminant (vide/null/erreur principale) — 1 test
3. Edge case unique le plus risqué — 1 test optionnel

**Anti-pattern interdit** : écrire 6 tests sur 1 seul comportement (constaté sur cache_helpers.py — takeover/known/unknown/empty/no-name/empirical). 2-3 tests bien choisis suffisent.

### Effort — high (pas xhigh)

Effort `high` suffit pour générer des tests. xhigh est diminishing returns. Voir [[feedback_opus47_workflow]].

### Bypass TDD

Pour typo/rename/config/hotfix<5L/doc : architect annonce `TESTS: BYPASS` dans son mini-plan S, dev utilise `touch .tdd-bypass` avant la modif. Voir [[pipeline-boris-adapte-neoteem]].

## Liens
- [[pipeline-boris-adapte-neoteem]] — recette complète
- [[erreur-pipeline-trop-long-frustration]] — pourquoi cette révision
- [[feedback_opus47_workflow]] — effort levels révisés
