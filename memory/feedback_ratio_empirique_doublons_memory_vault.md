---
name: ratio-empirique-doublons-memory-vault-pilote
description: "Pilote 29 fichiers memory/ = 38% doublons vault confirmés empiriquement. Ancre seuils hook saturation et /clean-memory"
metadata:
  type: feedback
---

Cf [[pattern-maintenance-hybride-corpus-accumulatif]] (doctrine : architecture cognitive 3 acteurs MEMORY.md/vault/memory + workflow décision 4 étapes + seuils saturation WARNING 80 / CRITICAL 100 / cible ≤ 100 fichiers). Ce feedback ne porte que la **mesure empirique granulaire** du pilote, non absorbée par la canonique.

**Cas empirique(s) :**

- **2026-05-28 — pilote 29 fichiers** (échantillon stratifié sur 274 fichiers `memory/`, clusters verify-empirique 13 + advisor-da 6 + audit-methode 11). Classification : DOUBLON COMPLET (purge) = 3 fichiers / 10 % (rm + retrait index) · DOUBLON PARTIEL (pointeur 1 ligne) = 8 fichiers / 28 % (body réécrit "Cf [[note-vault]]") · SPÉCIFIQUE (keep) = 18 fichiers / 62 % (aucune action).
- **Ratios par cluster mesurés** : `verify-empirique` (13 fichiers) = 23 % doublons → cluster sain, dimensions distinctes (brief faillible / line numbers / claim sécu). `advisor-da` (6 fichiers) = 50 % doublons → modérément redondant avec rule `devils-advocate-pipeline.md` + `Knowledge/erreurs/`. `audit-methode` (11 fichiers) = 45 % doublons → fort recouvrement avec canonique [[audit-claude-folder-pattern]] qui absorbe 2-3 feedbacks complets.
- **Projection corpus complet** : si 38 % représentatif sur les 245 fichiers restants → ~93 candidats POINTEUR/PURGE et ~152 KEEP. Cible ≤ 100 atteignable via amend chirurgical séquentiel (pas refonte massive), à vérifier batch par batch.
- **Heuristique de tri par cluster (baseline pilote)** : cluster > 60 % doublons → fort signal canonique vault dominante. Cluster < 20 % → cluster sain à conserver tier-1/tier-2. Trancher cluster par cluster avec ce ratio plutôt que re-mesurer en bloc (coût tokens).
