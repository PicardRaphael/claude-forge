---
titre: "Bug caractérisé : fix trivial = immédiat, fix coûteux = feedback pour phase dédiée"
resume: "Pattern décisionnel post-découverte de bug : quand un test adverse révèle un bug, arbitrer immédiatement entre fix immédiat (trivial, isolé, testé) et report en feedback mémoire (coûteux, risqué, hors-scope)."
aliases:
  - "bug caracterise fix trivial"
  - "fix immediat vs phase dediee"
  - "bug trivial fix immediat"
  - "quand fixer un bug decouvert"
  - "characterized bug fix decision"
  - "fix now or defer bug"
derniere-maj: 2026-05-27
auteur: claude
type: pattern
tags:
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#domaine/testing"
---
# Bug caractérisé : fix trivial = immédiat, fix coûteux = feedback pour phase dédiée

> Pattern décisionnel forge — que faire quand un test adverse (ou un audit) révèle un bug réel.

## QUOI

## Étape préalable : le test rouge encode-t-il un bug ou une hypothèse ?

Avant d'appliquer le pattern fix-trivial/coûteux, confirmer que le test révèle un **bug réel** et non une **hypothèse erronée du testeur** sur le fonctionnement interne.

| Type d'assert | Interprétation | Action |
|---|---|---|
| Encode une **exigence** (le code DOIT faire X, contrat public) | Comportement incorrect = **bug réel** → appliquer fix trivial/coûteux | Fixer le code |
| Encode une **hypothèse** sur l'implémentation interne (je SUPPOSE que le code fait X en interne) | Le code fait Y de façon cohérente et sensée → ce n'est pas un bug | Corriger l'assert + renommer le test pour pinner le comportement réel (test de caractérisation) |

**Réflexe** : test rouge sur du code non touché → lire le code AVANT de conclure "bug". Si le comportement réel est cohérent et sensé, c'est l'assert qui est faux.

**Exemple (27 mai 2026, forge-brain MCP)** : `test_resolve_prefix` a échoué car le testeur supposait que `resolve_note` testait le tier 3 (préfixe `name-%`) avant le tier 2 (substring `%-name%`). Le code fait l'inverse (tier 2 ligne 246, tier 3 ligne 254). Aucun bug — hypothèse sur l'ordre. Fix : renommer en `test_resolve_tier2_beats_tier3` pour pinner l'ordre RÉEL.

**Règle absolue** : ne jamais modifier le code source pour faire passer un test dont l'assert encodait une hypothèse non vérifiée. Cf [[comment-creer-hook]] (tests adverses = vérifier le contrat, pas l'implémentation interne).

Quand un test adverse, un audit ou une revue **caractérise un bug réel** (comportement épinglé par un test, pas une hypothèse), il faut arbitrer **immédiatement** entre deux voies — ne jamais laisser un bug caractérisé dans un flou "on verra".

## La règle

| Profil du fix | Action | Pourquoi |
|---------------|--------|----------|
| **Trivial** (isolé, < ~10 lignes, sans dépendance, test déjà prêt à inverser, comportement vérifiable) | **Fix immédiat** dans la foulée | Le coût de re-contextualiser plus tard dépasse le coût du fix maintenant. Le bug est frais, le test existe déjà. |
| **Coûteux** (refonte, dépendances multiples, risque de régression, nécessite design/validation) | **Feedback mémoire** + test de caractérisation qui épingle le comportement actuel | Fixer à chaud un bug risqué = précipitation. On documente, on épingle, on traite en phase dédiée avec le bon niveau d'attention. |

## Critères de "trivial"

Un fix est trivial si TOUS ces points sont vrais :
- **Isolé** : touche une seule fonction/bloc, pas d'effet de bord ailleurs.
- **Petit** : ordre de grandeur < 10 lignes.
- **Sans nouvelle dépendance** : pas de refonte d'interface, pas de nouveau module.
- **Vérifiable** : un test prouve le avant/après (idéalement le test de caractérisation existe déjà et il suffit de l'inverser).
- **Réversible** : si ça casse, le rollback est immédiat.

Si UN seul point manque → traiter comme coûteux (feedback + phase dédiée).

## Dans les deux cas : caractériser, jamais masquer

Que l'on fixe ou que l'on reporte, le bug DOIT être épinglé par un test :
- **Fix immédiat** : le test de caractérisation devient un **regression guard** (inverser l'assertion, garder le test, documenter l'historique dans le docstring). Ne JAMAIS supprimer le test — il prouve que le bug ne reviendra pas.
- **Report** : le test épingle le comportement ACTUEL (`assert ... # current buggy behavior`) + feedback mémoire avec le chemin de fix prévu.

## Exemple réel (27 mai 2026, Phase 2 forge)

Tests adverses sur les hooks critiques → 2 bugs trouvés :
- **security-guard sans `main()` gardé** (non testable) → fix **trivial** (refactor en main() + garde, comportement inchangé) → fixé immédiatement.
- **delegate-guard substring match agent_id** (bypass indu) → fix **trivial** (supprimer 4 lignes, le exact-match existait déjà) → fixé immédiatement, test de caractérisation inversé en regression guard (`test_agent_id_substring_does_not_grant_bypass`).

Les deux étaient triviaux → fix immédiat. Si delegate-guard avait nécessité de repenser tout le modèle de bypass (sources 1-4), il aurait été reporté en feedback.

## Anti-patterns

- ❌ **Laisser un bug caractérisé en flou** ("c'est noté, on verra") sans décider fix-now/defer.
- ❌ **Fixer à chaud un bug risqué** par envie de clore — précipitation = régression.
- ❌ **Supprimer le test** après fix (au lieu de l'inverser en regression guard) — on perd la preuve de non-régression.
- ❌ **Reporter un fix trivial** par paresse — le re-contextualiser coûtera plus cher que le faire maintenant.

## WIKILINKS

- [[comment-creer-hook]] — étape 5, tests adverses ≥3:1 (révèlent les bugs caractérisés)
- [[feedback_tests_adverses_obligatoires]]
- [[feedback_zero_dette_technique]] — dette découverte = nettoyage complet immédiat (cousin de ce pattern)
- [[feedback_da_blocking_must_block]] — verdict bloquant doit bloquer (ne pas laisser en flou)
