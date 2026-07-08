---
aliases:
  - frameworks-priorisation-comparatif
  - quel-framework-priorisation
  - priorisation-framework-cheatsheet
  - RICE-ICE-WSJF-MoSCoW-comparison
  - choisir-framework-priorisation
resume: "Table actionnable des 8 frameworks de priorisation produit — formule, taille équipe min, type de décision, recommandation pour Lead IA Neoteem équipe 1-5."
derniere-maj: 2026-05-25
tags:
  - "#type/cheatsheet"
  - "#domaine/priorisation"
  - "#casquette/responsable-ia"
---

## TL;DR

- Équipe 1-5 personnes : **RICE par défaut** pour roadmap IA Loji
- **WSJF** uniquement si compliance/dépendances cross-équipe (RGPD, sécurité)
- **Kano** 1-2× par an pour audit perception client (syndics + locataires)
- **MoSCoW** pour un release scope, jamais pour une roadmap continue

## Table comparative

| Framework | Formule | Taille équipe min | Type décision | Output | Exemple Neoteem 1 ligne |
|---|---|---|---|---|---|
| **RICE** | (Reach × Impact × Confidence) / Effort | 1+ | Roadmap features continue | Score numérique | NeoChat classification mandats = 1067 |
| **ICE** | Impact × Confidence × Ease | 1+ | Brainstorm rapide, growth | Score 1-1000 | Tag auto fiches mandat = 320 |
| **WSJF** | (BV + TC + RR/OE) / Job Size | 3+ | Compliance, dépendances | Score Fibonacci | Patch RGPD logs NeoChat = 13 |
| **MoSCoW** | Must / Should / Could / Won't | 1+ | Scope release fixe | 4 buckets | MVP NeoDocs : Must = OCR + signature |
| **Kano** | Basic / Performance / Delight | 5+ | Audit perception (1-2×/an) | Catégorie qualitative | Auto-réponse 24/7 = Performance |
| **Value-Effort 2x2** | Matrice visuelle | 1+ | Workshop trimestriel | Quadrants | Quick wins Q3 = scoring locataire |
| **Opportunity Scoring** | Importance × (Importance - Satisfaction) | 5+ | Discovery client | Score 1-20 | Génération fiches mandat = 14.2 |
| **Story Mapping** | User journey × backbone | 2+ | Découpage release | Map 2D | Onboarding syndic Loji |

## Recommandation Neoteem (équipe 1-5)

### Par défaut

**RICE** pour 80% des décisions roadmap IA (NeoChat, NeoDocs, Aurore). Voir [[rice-en-pratique]].

### Cas spéciaux

- **WSJF** si : compliance RGPD, patch sécu critique, dépendance dev/devops. Voir [[wsjf-pour-equipe-petite]].
- **Kano** : audit 1-2×/an avec 10-20 syndics. Identifier "delighters" vs "basics".
- **MoSCoW** : scoping release majeure (ex : NeoDocs v1.0).
- **Opportunity Scoring** : avant gros investissement R&D agent (ex : Aurore v2).

### À éviter

- **ICE seul** : confondu avec RICE, pas de Reach = biais features cool sans impact
- **Story Mapping** : overkill pour équipe 1-5, utile en équipe 10+

## Cadence d'usage

| Cadence | Framework | Output |
|---|---|---|
| Hebdo | RICE quick (5 min) | Top 3 sprint |
| Mensuel | RICE complet + intake review | Refresh Now/Next/Later |
| Trimestriel | Value-Effort 2x2 workshop | OKR draft |
| Semestriel | Kano survey | Repositionnement |
| Annuel | Opportunity Scoring | Investissement majeur |

## Anti-patterns

- Mixer 3 frameworks sur la même roadmap = paralysie analytique
- RICE sans Confidence = features ambitieuses passent toujours (biais optimisme)
- WSJF en équipe 1 personne = théâtre process
- MoSCoW continu = Must explose (60% des items deviennent Must)
- Changer de framework chaque trimestre = pas de baseline comparable

## Sources

- Sean McBride, Intercom — https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- Donald Reinertsen, "Principles of Product Development Flow" (2009) — WSJF origine SAFe
- Noriaki Kano (1984) — "Attractive quality and must-be quality"
- Marty Cagan, SVPG — https://www.svpg.com/product-strategy-overview/
- Janna Bastow, ProdPad — https://www.prodpad.com/blog/now-next-later-roadmap/

## Voir aussi

- [[index]]
- [[rice-en-pratique]]
- [[wsjf-pour-equipe-petite]]
- [[roadmap-now-next-later]]
- [[okr-equipe-ia-wodtke]]
- intake-no-factory-yes-if
