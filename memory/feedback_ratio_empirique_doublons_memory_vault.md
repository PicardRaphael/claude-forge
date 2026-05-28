---
name: ratio-empirique-doublons-memory-vault-pilote
description: "Pilote 29 fichiers memory/ = 38% doublons vault confirmés empiriquement. Ancre seuils hook saturation et /clean-memory"
metadata:
  type: feedback
---

Cf [[pattern-maintenance-hybride-corpus-accumulatif]] section "Architecture cognitive — trois acteurs" pour la doctrine et les workflows. Ce feedback porte uniquement la **mesure empirique** qui ancre la doctrine.

**Cas empirique 2026-05-28 — pilote 29 fichiers** (clusters verify-empirique 13 + advisor-da 6 + audit-methode 11, échantillon stratifié sur 274 fichiers memory/) :

| Classification | Count | % | Action appliquée |
|---|---|---|---|
| DOUBLON COMPLET (purge) | 3 | 10% | rm + retrait index |
| DOUBLON PARTIEL (pointeur 1 ligne) | 8 | 28% | body réécrit en 2-3 lignes "Cf [[note-vault]]" |
| SPÉCIFIQUE (keep) | 18 | 62% | aucune action |

**Patterns observés** :
- Cluster `verify-empirique` (13 fichiers) = 23% doublons → cluster sain, dimensions distinctes (brief faillible / line numbers / claim sécu / etc.)
- Cluster `advisor-da` (6 fichiers) = 50% doublons → modérément redondant avec rule `devils-advocate-pipeline.md` + `Knowledge/erreurs/`
- Cluster `audit-methode` (11 fichiers) = 45% doublons → **fort recouvrement avec canonique [[audit-claude-folder-pattern]]** qui absorbe 2-3 feedbacks complets

**Données ancrent les seuils hook `memory-saturation-watcher.py`** :
- WARNING ≥ 80 fichiers (signal "planifier /clean-memory prochainement")
- CRITICAL ≥ 100 fichiers (signal "lancer /clean-memory en session dédiée")
- Cible doctrine ≤ 100 fichiers cohérente avec workflow 4 étapes (search_brain vault d'abord = filtre amont)

**Projection** : si 38% est représentatif sur les 245 fichiers restants, ~93 candidats POINTEUR/PURGE et ~152 KEEP. Cible atteignable ≤ 100 fichiers via amend chirurgical séquentiel (pas refonte massive). À vérifier batch par batch.

**How to apply** : avant de relancer un audit redondance memory/vault, ne pas re-mesurer en bloc (coût tokens élevé). Trancher cluster par cluster avec ce ratio comme baseline. Si un cluster donne > 60% doublons → fort signal canonique vault dominante. Si < 20% → cluster sain à conserver tier-1/tier-2.
