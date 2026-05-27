---
name: premier-auteur-vs-senior-papers-academiques
description: "Quand on crée/audite une fiche leader autour d'un paper, vérifier arXiv ordre auteurs : si le leader est senior (dernier), écrire 'co-auteur senior'. JAMAIS attribuer comme premier auteur sans vérif."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c6c61616-50af-4cd8-8b0b-68932b824064
---

Pattern récurrent détecté sur audit 07 (23 mai 2026) : 5 fiches leaders du vault attribuaient un paper au leader comme premier auteur alors qu'il est en fait **senior** (dernier auteur) :

| Paper | Vault attribuait à | Réel premier auteur | Leader = senior |
|-------|--------------------|--------------------|-----------------|
| Self-Consistency (2203.11171) | Denny Zhou | Xuezhi Wang | Zhou |
| SWE-agent NeurIPS 2024 | Shunyu Yao | John Yang | Yao co-auteur middle |
| BEIR NeurIPS 2021 | Nils Reimers | Nandan Thakur | Reimers co-auteur |
| AWQ MLSys 2024 Best Paper | Song Han | Ji Lin | Song Han |
| FlashAttention-4 MLSys 2026 | Tri Dao | Zadouri/Shah/Hohnerbach co-leads | Tri Dao |

**Why** : confusion fréquente parce que le leader (Zhou, Yao, Reimers, Song Han, Tri Dao) est plus visible publiquement que le premier auteur (souvent PhD student). Mais l'attribution scientifique correcte = premier auteur fait le travail, senior dirige.

**How to apply** :
- Avant d'attribuer un paper à un leader dans une fiche vault, ouvrir arXiv et regarder l'**ordre exact des auteurs**
- Si leader = senior : écrire "co-auteur **senior**" ou "X et al. (incl. [Leader])"
- Si leader = premier auteur : OK "auteur principal"
- Vérification rapide : 1 WebFetch arXiv abstract suffit

**Anti-pattern** : présenter un paper comme "Le paper X de [Leader]" sans vérifier l'ordre. Génère des inexactitudes systématiques sur les fiches leaders.

Lié : [[feedback_audit_thematique_methode]] — sub-agent cluster "papers arXiv" doit systématiquement reporter `Auteurs exacts arXiv` + position du leader (premier / middle / senior).
