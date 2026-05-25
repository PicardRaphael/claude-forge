---
aliases:
  - Now-Next-Later
  - roadmap-NNL
  - Janna-Bastow-roadmap
  - roadmap-sans-dates
  - ProdPad-roadmap
resume: "Roadmap Now/Next/Later de Janna Bastow (ProdPad 2012) — pas de dates, cone of uncertainty, template Neoteem complet, cadence par audience."
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#domaine/roadmap"
  - "#casquette/responsable-ia"
---

## TL;DR

- Janna Bastow, ProdPad, 2012 — roadmap **sans dates**
- 3 horizons : **Now** (en cours), **Next** (~12 sem), **Later** (themes)
- Communique l'incertitude croissante (cone of uncertainty)
- Cadence revue mensuelle, publication adaptée par audience
- Anti-Gantt : refuse les promesses de dates

## Pourquoi sans dates — les 3 mensonges roadmaps datées

| Mensonge | Réalité |
|---|---|
| "Q3 = feature X livrée" | Estimation à 6 mois fiable à ±50% (étude Standish) |
| "Notre roadmap est ferme" | 70% des items roadmap > 6 mois sont remplacés (étude ProductPlan) |
| "Le client peut s'engager dessus" | Engagement → contractualisation → blocage pivot |

Les dates **fixent une réalité qui n'existe pas encore**. Result : trust détruit quand on glisse.

## Cone of uncertainty

```
NOW         NEXT          LATER
|-----------|-------------|-------------------------|
±10%        ±50%          ±200%
détaillé    initiatives   themes seulement
```

Plus on s'éloigne, moins on est précis. Le Now est concret, le Later est une direction.

## Template roadmap Neoteem (à copier)

```markdown
# Roadmap IA Loji — [date de revue]

## Now (sprint en cours + sprint suivant)

| Initiative | Outcome attendu | Owner | Statut |
|---|---|---|---|
| Aurore v1 classification mandats | 80% précision sur 500 mandats test | Raphael | dev |
| NeoChat anti-hallucination guardrails | Hallucination 8% → 3% | Raphael | QA |
| RGPD logs NeoChat | Audit interne PASS | Raphael+devops | en cours |

## Next (~12 semaines)

| Initiative | Problème à résoudre | Confidence |
|---|---|---|
| Scoring locataire ML v2 | Gestionnaires perdent 15 min/dossier vérif | 80% |
| NeoDocs OCR fiches mandat | Saisie manuelle ralentit onboarding | 70% |
| Génération réponses email locataires | 30% emails = questions répétitives | 60% |

## Later (themes, pas features)

- **Theme : Productivité gestionnaire** — automatiser tâches récurrentes
- **Theme : Expérience locataire** — auto-réponse 24/7, suivi temps réel
- **Theme : Intelligence portefeuille** — analytics gérance, prédiction renouvellement
- **Theme : Compliance & sécurité** — HDS, audit trail, anonymisation

> Pas de feature nommée ici. Themes seulement.
```

## Cadence revue interne

| Cadence | Action | Durée |
|---|---|---|
| Hebdo (lundi) | Status Now | 15 min |
| Mensuel | Refresh Next + promotions Later→Next | 1h |
| Trimestriel | Revue Themes Later + alignement OKR | 2h |
| Semestriel | Revue stratégique themes vs vision | 1/2 journée |

Voir [[okr-equipe-ia-wodtke]] pour cadence Mon/Fri.

## Cadence publication par audience

| Audience | Vue | Cadence | Format |
|---|---|---|---|
| **Équipe IA (toi)** | Now + Next + Later complet | Hebdo | Confluence + Jira board |
| **Direction Neoteem** | Now outcomes + Next themes | Mensuel | Slide 1 page |
| **Métier (gestionnaires Loji)** | Themes Later + Next confidence ≥80% | Trimestriel | Newsletter |
| **Clients (syndics)** | Themes Later uniquement | Semestriel | Public roadmap page |

**Règle d'or** : plus l'audience est externe, moins on engage de spécifique.

## Trois colonnes — règles strictes

### Now

- En cours sprint actuel + suivant
- Outcome **mesurable** (pas "améliorer X")
- Owner nommé
- Confidence ≥ 90%

### Next

- 6-12 semaines
- Problème > solution (la solution peut pivoter)
- Confidence 50-80%
- Pas plus de **5-7 items** (équipe 1-5)

### Later

- **Themes uniquement** — pas de feature nommée
- 3-6 mois et au-delà
- Direction stratégique, pas commitment

## Anti-patterns

- Mettre des dates "indicatives" → elles deviennent des commitments
- 30 items dans Next → c'est plus une roadmap, c'est un backlog
- Later rempli de features précises → engagement implicite
- Publier la même vue à tout le monde → direction lit comme métier qui lit comme client
- Ne jamais bouger un item de Next à Later (downgrade) → roadmap toujours optimiste, jamais réaliste
- Roadmap à 18 mois → cone of uncertainty rend l'exercice théâtral
- Refuser de communiquer "quand" → frustrer stakeholders. Réponse : "Confidence X% sur le trimestre Y" pas une date

## Communiquer "quand" sans dates

Au lieu de "Q3 2026" :
- "En cours" (Now)
- "Prochain trimestre, confidence 70%" (Next)
- "Cette année si validation discovery" (Later)
- "Theme stratégique, pas encore engagé" (Later sans confidence)

## Sources

- Janna Bastow, ProdPad — https://www.prodpad.com/blog/now-next-later-roadmap/
- Janna Bastow, talk Mind the Product — https://www.mindtheproduct.com/why-i-hate-feature-roadmaps-and-what-i-prefer-instead/
- Bruce Mccarthy, "Product Roadmaps Relaunched" (2017)

## Voir aussi

- [[index]]
- [[frameworks-comparatif]]
- [[okr-equipe-ia-wodtke]]
- [[intake-no-factory-yes-if]]
