---
name: brief-prescrit-travail-deja-fait-veille
description: Brief auto-mode peut prescrire création/audit déjà fait 24-48h avant. search_brain + derniers ajouts canoniques AVANT exécution Phase 1, pas après recadrage.
metadata:
  type: feedback
---

# Brief prescrit travail déjà fait la veille — vérifier l'historique vault avant exécution

## Règle

Quand un brief auto-mode prescrit une création de note canonique OU un audit empirique massif, **AVANT de lancer Phase 1** :

1. `search_brain` sur le sujet du brief (pas seulement sur "doublon")
2. `read_note` EN ENTIER des notes pertinentes des dernières 24-72h
3. Vérifier si AJOUT récent (`## AJOUT YYYY-MM-DD`) couvre déjà le pattern
4. Vérifier si raisonnement récent (`Knowledge/raisonnements/`) capitalise déjà la méta

Si le travail est déjà fait → **surfacer**, présenter options (skip / AJOUT incrémental / nouvelle note avec angle distinct), demander arbitrage.

## Why

28 mai 2026. Brief Phase 1-6 prescrivait :
- Phase 1 : créer `workflow-vault-consultation-search-then-read.md`
- Phase 2 : auditer 49 skills + 13 agents tous composants

Vérification empirique (3 search_brain + 3 read_note avant Phase 1) :
- Canonique déjà créée hier 28 mai (`pattern-mcp-brief-then-direct` AJOUT 28 mai "Grille d'audit empirique vault-invocation par catégorie de composant")
- Audit déjà fait hier (49 skills + 13 agents → 2 AMEND ciblés cc-advisor + evolve)
- Raisonnement méta capitalisé hier (`audit-lifecycle-classification-categories`)

Si exécution aveugle : doublon canonique + re-audit redondant + violation `single_source_truth_vault_canonique` + violation `consolidate-searches`.

Distinct de `brief-premisse-fausse-verifier-avant-executer` (prémisse factuellement fausse) : ici la prémisse est **obsolète** — vraie il y a 48h, périmée maintenant. Le risque vient de la cadence rapide forge où plusieurs sessions peuvent capitaliser le même sujet à 24h d'intervalle.

## How to apply

- Brief mentionne "créer note canonique X" → `search_brain "X"` + `list_notes("04-Techniques/...")` filtrés `derniere-maj` ≥ J-3
- Brief mentionne "audit tous composants pour pattern Y" → vérifier `Knowledge/raisonnements/` et `Knowledge/syntheses/` des 72 dernières heures pour audit déjà conduit
- Brief mentionne phase massive de propagation → vérifier CHANGELOG vault des 3 derniers jours
- Surfacer 3 options minimum : skip / AJOUT incrémental / nouvelle note avec angle distinct confirmé
- Pas de Phase 1 destructive (création/AMEND) avant arbitrage si overlap détecté

Anti-pattern : "le brief dit Phase 1, je commence Phase 1" sans vérifier que Phase 1 n'est pas déjà du travail d'hier sous un autre nom.

## Liens

- [[brief-premisse-fausse-verifier-avant-executer]] — feedback voisin (prémisse fausse vs obsolète)
- [[consolidate-searches]] — règle anti-doublon recherches
- [[single-source-truth-vault-canonique]] — règle anti-doublon notes
- [[pattern-mcp-brief-then-direct]] — canonique déjà à jour 28 mai
- [[audit-lifecycle-classification-categories]] — raisonnement méta 28 mai
