---
name: 80-percent-confidence-ship-now
description: "Si convergence 80%+ sur \"game-changer\", coder direct avec tests adverses rigoureux plutôt qu'attendre 7j de mesure usage_stats. Raphael trance ce trade-off explicitement"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3751b01a-33d9-4962-b652-428c951e42d4
---

## Pattern

Sur des features où la valeur est convergente (ex: bulk_update_property observé 16x dans la session, read_section économie 30x prouvée, embed resolution pour MOC) :

- **Advisor recommande** : mesurer usage_stats 7-30 jours avant ajouter, éviter feature creep
- **Raphael préfère** : "Si on est sûr à 80% game-changer, fais-le sans attendre tests"

C'est un trade-off de **vitesse vs validation empirique**. Sur cette session, le ratio a marché : 3 outils ajoutés v1.3 (bulk/section/resolved) + 14 tests adverses passent.

## Why

Raphael a verbalisé explicitement : "Si bulk_update_property, read_section, embeds resolution est parfait fait le pas attendre les test si on est sur a 80% que cest game changer".

Coût d'attendre 7j sur outils convergents = perte d'usage pendant la fenêtre + risque que l'opportunité de capitalisation passe. Coût d'ajouter et de retirer si jamais utilisé = `usage_stats` permet pruning a posteriori.

## How to apply

Quand convergence claire (multiple cas d'usage observés dans la session OU verbalisation explicite "game-changer") :

1. **Vérifier l'évidence** : 2-3 cas d'usage concrets cette session ? Oui → ship
2. **Tests adverses rigoureux** : pas négociable. DA pattern obligatoire (cf [[feedback_da_dicte_tests_adverses]])
3. **Logger usage** : ajouter à `usage_stats` pour future pruning si jamais inutile
4. **Note canonique** : capitaliser dans vault Knowledge/syntheses ou 04-Techniques pour réutilisation

Sur features spéculatives (jamais observé en usage) → AU CONTRAIRE attendre data.

**Heuristique** : "Cette session je l'aurais utilisé combien de fois ?". Si 5+ → ship. Si 0-1 → attendre.

## Liens

- [[feedback_da_dicte_tests_adverses]] — tests adverses obligatoires sur code rewriting/destructif
- [[feedback_carte_blanche_commit_push]] — exécuter direct quand validé
