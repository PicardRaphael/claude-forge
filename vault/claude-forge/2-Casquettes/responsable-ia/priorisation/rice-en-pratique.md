---
aliases:
  - RICE
  - RICE-scoring
  - RICE-Intercom
  - RICE-pratique-Neoteem
  - methode-RICE
resume: "Méthode RICE de Sean McBride (Intercom) appliquée à la roadmap IA Loji — formule, échelles, exemple chiffré Aurore mandats locataires, template scoring sheet."
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#domaine/priorisation"
  - "#casquette/responsable-ia"
---

## TL;DR

- **Formule** : `RICE = (Reach × Impact × Confidence) / Effort`
- Reach et Effort = chiffres réels (utilisateurs/mois, person-month)
- Impact et Confidence = échelles fixes (anti-biais optimisme)
- **Confidence < 50% → discovery d'abord, pas scoring**
- Pour Neoteem : exécuter en 30 min/sprint sur 5-10 items

## Les 4 facteurs

### Reach — combien d'utilisateurs touchés / période

Unité = nombre d'utilisateurs ou d'événements **par période fixe** (mois recommandé).

Sources données Neoteem :
- Nombre de syndics actifs sur Loji
- Nombre de mandats locataires/mois traités
- Nombre de requêtes NeoChat/mois

### Impact — échelle fixe McBride

| Score | Label | Définition |
|---|---|---|
| 3 | Massive | Impact transformationnel sur l'utilisateur |
| 2 | High | Impact fort, mesurable |
| 1 | Medium | Impact net |
| 0.5 | Low | Petit gain |
| 0.25 | Minimal | À peine perceptible |

**Pas d'inflation** : si tout est 3, l'échelle est cassée.

### Confidence — anti-bullshit

| Score | Sens |
|---|---|
| 100% | Données quantitatives + tests utilisateurs |
| 80% | Données qualitatives + précédent similaire |
| 50% | Intuition équipe, pas de data |
| < 50% | Spéculation → ne pas scorer, faire discovery |

### Effort — person-month

Somme dev + design + PM + ops. Arrondir au 0.5 pm près. Si > 6pm, découper.

## Exemple chiffré complet — Aurore (agent IA classification mandats)

### Contexte

Aurore = agent qui classe automatiquement les mandats locataires reçus par email pour les gestionnaires Loji (extraction document, scoring locataire, routage).

### Scoring

| Facteur | Valeur | Justification |
|---|---|---|
| Reach | 2000 mandats/mois | Base actuelle Loji syndics actifs |
| Impact | 2 (High) | Gestionnaire gagne ~10 min/mandat |
| Confidence | 80% | POC NeoDocs OCR validé, 2 syndics pilotes prêts |
| Effort | 3 pm | 1.5pm dev back2.0, 1pm IA tuning, 0.5pm UX |

**RICE = (2000 × 2 × 0.80) / 3 = 1067**

### Comparatif 3 alternatives

| Feature | Reach | Impact | Conf | Effort | RICE |
|---|---|---|---|---|---|
| Aurore classification mandats | 2000 | 2 | 0.80 | 3 | **1067** |
| NeoChat FAQ syndics multilang | 500 | 1 | 0.50 | 2 | 125 |
| Scoring locataire ML v2 | 2000 | 3 | 0.50 | 5 | 600 |
| Dashboard analytics gérance | 150 | 2 | 1.00 | 1.5 | 200 |

→ **Aurore en tête, scoring v2 second** (mais Confidence faible = discovery d'abord).

## Template scoring sheet (à copier)

```markdown
| Feature | Reach (/mois) | Impact (3/2/1/0.5/0.25) | Confidence (1.0/0.8/0.5) | Effort (pm) | RICE | Notes |
|---|---|---|---|---|---|---|
| [Nom] | | | | | =(R*I*C)/E | |
| | | | | | | |
```

## Cadence Neoteem

- **Hebdo (5 min)** : RICE quick sur 3 nouveaux items intake
- **Mensuel (30 min)** : recalibrage RICE sur backlog top 15
- **Trimestriel** : audit Confidence — items à 80%+ depuis 3 mois sans data = repasser à 50%

## Piège : la fausse précision

RICE = 1067 vs RICE = 1043 n'est **pas** un signal. Marges d'erreur réelles : ±30%.

Règle : ne comparer RICE qu'avec un écart ≥ 1.5× ou ≥ 200 points absolus.

## Anti-patterns

- Inventer un Reach pour justifier une feature ("tous les gestionnaires français = 50 000")
- Confidence 100% sans données réelles
- Impact = 3 par défaut sur ses propres idées
- Effort sous-estimé × 2 systématique (multiplier par 1.5 en équipe IA)
- Scorer une feature avec Confidence < 50% → faire discovery, pas scorer
- Ne pas dater le score → un RICE d'il y a 6 mois n'est plus valide

## Sources

- Sean McBride, Intercom (2015) — https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- Itamar Gilad, "Evidence-Guided" — https://itamargilad.com/the-tool-that-will-help-you-choose-better-product-ideas/
- Lenny Rachitsky, RICE in practice — https://www.lennysnewsletter.com/p/how-the-most-successful-b2b-startups

## Voir aussi

- [[index]]
- [[frameworks-comparatif]]
- [[wsjf-pour-equipe-petite]]
- [[intake-no-factory-yes-if]]
