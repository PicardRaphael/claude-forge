---
aliases:
  - priorisation-roadmap-ia
  - hub-priorisation
  - roadmap-ia
  - prioriser-ia
  - frameworks-prio
resume: Hub priorisation roadmap IA — RICE, ICE, WSJF, MoSCoW, Kano, opportunity scoring. Real Options, Three Horizons. OKR, GIST, Now/Next/Later. Hidden Tech Debt ML.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/priorisation"
  - "#domaine/produit"
---

# Priorisation roadmap IA — hub

> **Pain point #2 de Raphael.** Arbitrer R&D IA, demandes business, dette technique.

## Stack recommandé pour Neoteem (équipe 1-5)

1. **Stratégique annuel** : Vision + Strategic Intent (Perri)
2. **Trimestriel** : 1 OKR équipe IA (Wodtke cadence Mon/Fri) + 1-2 big bets
3. **Roadmap publique** : Now/Next/Later (Bastow) avec dates uniquement sur Now
4. **Discovery continu** : OST (Torres) + 2 interviews/semaine
5. **Priorisation backlog** : RICE pour delivery + WSJF pour features à CoD chiffrable + Kano pour pricing
6. **Spike R&D** : Real Options (small bets reversibles) + Bet/Believe matrix
7. **Allocation capacity** : **60/20/15/5** (delivery/R&D/model-debt/exploration)
8. **Intake demandes** : formulaire + SLA 5j + "Yes if..." framing + Parking Lot
9. **Build pipeline** : Discovery → Spike → MVP → A/B → Scale → Maintain → Sunset
10. **Mesure** : NSM + 3-5 inputs leading + KR modèle (accuracy, hallucination, latency, cost)

## Frameworks de priorisation — quand utiliser quoi

| Framework | Formule | Quand |
|---|---|---|
| **RICE** | (Reach × Impact × Confidence) ÷ Effort | Backlog ≥ 20 items, comparaison features hétérogènes |
| **ICE** | Impact × Confidence × Ease | A/B tests growth, sprint hebdo |
| **WSJF** | Cost of Delay ÷ Job Size | Équipe ≥ 8, dépendances, compliance |
| **MoSCoW** | Must/Should/Could/Won't | Périmètre MVP négocié |
| **Kano** | Basic/Performance/Excitement | Roadmap annuelle, pricing |
| **Value vs Effort 2x2** | Quadrant | Whiteboard 10 min, 5-15 items |
| **Opportunity Scoring** | Importance + max(I-S, 0) | Phase discovery initiale |
| **Story Mapping** | Visuel parcours utilisateur | MVP, refonte parcours |

### Détails RICE (recommandé Neoteem)

- **Reach** : nb users/événements touchés/période
- **Impact** : 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal
- **Confidence** : 100% / 80% / 50%
- **Effort** : person-months

Piège : "fausse précision". RICE est **relatif**, pas exact.

### Détails WSJF
`CoD = Business Value + Time Criticality + Risk Reduction/Opp Enablement`
Échelle Fibonacci modifiée (1, 2, 3, 5, 8, 13, 20).

Exemple : Patch sécu RGPD CoD=20, size=2 → WSJF=10. Nouvelle intégration CoD=13, size=8 → WSJF=1.6. Le patch passe d'abord.

## Spécificité IA — prioriser l'inestimable

### Real Options Theory (arXiv 2025)
Un spike = option qu'on achète peu cher pour se réserver le droit (pas l'obligation) d'investir plus. **Multiplier petits spikes 2 semaines plutôt qu'un gros bet 3 mois.**

### Three Horizons (McKinsey)
- **H1** (1-3 ans) core
- **H2** (2-5 ans) adjacent
- **H3** (5-12 ans) transformational

**Critique Blank 2026** : l'IA générative a **collapsé l'axe temps**. Un H3 (LLM) devient H1 en 18 mois. → Audit H2/H3 trimestriel obligatoire.

### Bet/Believe Matrix pour spike IA
- High belief / high evidence = **ship**
- High belief / low evidence = **spike** (acheter info)
- Low belief / high evidence = **challenger l'hypothèse**
- Low belief / low evidence = **pas maintenant**

## Hidden Technical Debt in ML Systems (Sculley et al. NeurIPS 2015)

**À LIRE INTÉGRALEMENT** — 9 pages. Identifie 7+ types de dette spécifiques ML :
- **Boundary erosion**
- **Entanglement (CACE)** : Change Anything Changes Everything
- **Hidden feedback loops**
- **Undeclared consumers**
- **Data dependencies** (pire que code deps)
- **Configuration debt**
- **Changes in external world** : distribution drift

**Citation clé** : "Hidden debt compounds silently."
→ Réserver **15% capacity model debt** explicitement.

## Roadmap formats

### Now / Next / Later (Janna Bastow, ProdPad 2012)
**Pas de dates.** Reflète le cone of uncertainty.

Bastow : 3 mensonges des roadmaps dates :
1. "On sait combien de temps"
2. "Ça marchera du premier coup"
3. "Ça vaut le coup"

### GIST (Itamar Gilad)
- **Goals** (1+ an, OKR-aligned)
- **Ideas** (collecte permanente)
- **Step-projects** (trimestre, < 10 semaines, test 1 hypothèse)
- **Tasks** (1-2 semaines, sprint)

### Outcome-based (Melissa Perri)
Chaque item roadmap = un outcome (KR), pas une feature.
> "Le management ne doit pas dicter les features mais articuler le *pourquoi*."

## Continuous Discovery (Teresa Torres)

**Opportunity Solution Tree** :
```
Outcome
├── Opportunity 1 (douleur client)
│   ├── Solution 1.1 → Assumption test
│   └── Solution 1.2
├── Opportunity 2
```

**Cadence** : 1-3 interviews/semaine par product trio (PM + designer + ingé).

## OKR pour équipe IA (Doerr + Wodtke)

### Cadence Wodtke (Radical Focus)
- Quarterly : 1 Objective qualitatif + 3 KR quantitatifs ambitieux (confidence 50%)
- **Lundi 1h** : commit semaine + check progression
- **Vendredi 1h** : démos + célébrations
- Trimestre : "Pivot, persevere, perish"

### Template OKR Neoteem (exemple Q3)
```
Objective : Devenir l'IA proptech qui fait gagner 1 jour/semaine à chaque gestionnaire

KR1 (outcome) : 70% gestionnaires utilisent ≥ 1 agent IA quotidiennement
KR2 (model) : Hallucination agent dossier locataire 8% → <2%
KR3 (latency) : P95 réponse classification < 1.5s
KR4 (business) : Coût par dossier traité -25%
```

**Règle Doerr** : un KR doit pouvoir se répondre OUI/NON sans débat.

## Allocation capacity Neoteem (proposition)

| Personne | Discovery | Delivery | Model debt | Exploration |
|---|---|---|---|---|
| **Toi (Lead IA)** | 25% | 40% | 20% | 15% |
| **Devs (1-3)** | 10% | 75% | 10% | 5% |

## Gestion demandes inbound — "No Factory" (Cagan)

### Intake template
| Champ | Description |
|---|---|
| Demandeur | Personne + rôle |
| Problème (pas la solution) | "Notre équipe X galère sur Y parce que Z" |
| Outcome attendu (mesurable) | "Réduire temps de traitement de 40%" |
| Impact business si on ne fait rien | € ou nb users impactés |
| Deadline réelle | Source : contrat, réglementation |
| Confidence sur estimation | % |

**SLA réponse** : 5 jours ouvrés. Réponse = "Yes if...", "Not now because...", "Won't because...". Jamais "non" brut.

### Yes if framing
- "**Yes if** on retire X du Next" — force trade-off explicite
- "**Not now** because la confidence sur l'impact est <50%, on relance en Q+1 après spike"
- "**Won't** because incompatible avec l'outcome trimestre, mais on garde en Parking Lot"

## Anti-patterns priorisation

| Anti-pattern | Description | Antidote |
|---|---|---|
| **HiPPO** | Highest Paid Person's Opinion override la data | Scores RICE/WSJF transparents |
| **Squeaky Wheel** | Client qui crie obtient l'huile | Intake process + SLA + backlog transparent |
| **ZEBRA** | Bold claim sans evidence | Toujours demander la donnée |
| **RHINO** | Stakeholder sporadique qui perturbe | Updates réguliers |
| **WOLF** | Pivote sur chaque incident | Cadence trimestrielle, pas mensuelle |
| **Roadmap promise** | Dates fermes 6+ mois | Now/Next/Later, dates sur Now uniquement |
| **Sunk cost** | "On a déjà investi 3 mois, faut finir" | Kill criteria explicites |
| **Resume-driven dev** | Stack cool pour CV | Outcome-based prio |
| **Feature factory** (Cagan) | Sortir features pour sortir features | Outcome-based + missionaries not mercenaries |

## Build pipeline IA (stages + exit criteria)

| Stage | Objectif | Exit criteria | Sortie |
|---|---|---|---|
| **Discovery** | Identifier opportunity | ≥3 interviews + opportunity validée OST | Hypothèse écrite |
| **Spike** | Faisabilité technique | Prototype run, métriques mesurées | Go/No-Go documenté |
| **MVP** | Test 5-10 users internes | Métrique clé bouge + 0 régression critique | Pilote externe |
| **A/B** | Validation statistique | Lift significatif (p<0.05) | Rollout staged |
| **Scale** | Production hardening | SLO atteints | GA |
| **Maintain** | Service dette modèle | Drift < seuil, retraining cadencé | Stable |
| **Sunset** | Tuer ce qui ne marche pas | KPI raté 2 trimestres ou ROI négatif | Decommission |

**Règle non négociable (IBM stage-gating)** : pas d'avancement sans **action vérifiable**.

## Livres prioritaires (ordre)

1. **Sculley et al. — Hidden Technical Debt in ML Systems** (NeurIPS 2015, 9 pages gratuit)
2. **Melissa Perri — Escaping the Build Trap**
3. **Teresa Torres — Continuous Discovery Habits**
4. **Marty Cagan — Empowered + Transformed**
5. **Christina Wodtke — Radical Focus** (cadence Mon/Fri)

## Sources

- [RICE — Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- [WSJF — SAFe](https://framework.scaledagile.com/wsjf)
- [Opportunity Solution Tree — Product Talk](https://www.producttalk.org/opportunity-solution-trees/)
- [GIST — Itamar Gilad](https://itamargilad.com/gist-framework/)
- [Hidden Tech Debt ML — Sculley NeurIPS 2015 PDF](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)
- [Now-Next-Later — ProdPad Bastow](https://www.prodpad.com/blog/invented-now-next-later-roadmap/)
- [Three Horizons](https://strategicmanagementinsight.com/tools/three-horizons-growth-model/)
- [Empowered Product Teams — SVPG Cagan](https://www.svpg.com/empowered-product-teams/)
- [Radical Focus — Wodtke summary](https://theprocesshacker.com/blog/radical-focus-christina-wodtke-summary)
- [IBM Stage-Gating AI](https://www.ibm.com/think/insights/measuring-ai-outcomes-7-step-stage-gating-framework)
