---
aliases:
  - OKR-equipe-IA
  - OKR-Wodtke
  - OKR-Mon-Fri
  - OKR-Doerr-Wodtke
  - radical-focus
resume: "OKR pour équipe IA (Doerr + Wodtke Radical Focus) — cadence Mon/Fri, template OKR Q3 Neoteem complet, règle KR répondable OUI/NON, mix KR business + modèle."
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#domaine/okr"
  - "#casquette/responsable-ia"
---

## TL;DR

- **Doerr** : "Measure What Matters" — OKR Google depuis 1999
- **Christina Wodtke** : "Radical Focus" — cadence opérationnelle Mon/Fri
- **Lundi commit**, **vendredi démos** (rituel non négociable)
- 1 Objective qualitatif + 3-5 KR mesurables
- Règle Doerr : **chaque KR répondable OUI/NON** en fin de trimestre
- Pour équipe IA : **mixer KR business + KR modèle + KR latence**

## Structure OKR

```
Objective (qualitatif, inspirant, 1 phrase)
├── KR1 (mesurable, outcome)
├── KR2 (mesurable, outcome)
├── KR3 (mesurable, outcome)
└── KR4 (mesurable, outcome — optionnel)

Health metrics (suivis non promus)
```

### Règles strictes

| Élément | Règle |
|---|---|
| Objective | Inspire, pas mesurable. "Devenir X" pas "Faire Y" |
| KR | Outcome (résultat), pas output (livrable) |
| Test Doerr | "Le KR est-il répondable OUI/NON en fin de Q ?" |
| Nombre KR | 3-5 max. Au-delà, dilution focus |
| Stretch | KR atteint à 70% = succès (sinon trop facile) |

## Cadence Mon/Fri (Wodtke)

### Lundi — Commit (30 min)

| Item | Contenu |
|---|---|
| Status confidence OKR | Probabilité atteindre chaque KR (1-10) |
| Priorités semaine | 3-5 items qui font bouger les KR |
| Status santé | Health metrics (anti-burnout, anti-trade-off) |
| Bets long terme | 1-2 paris semestriels |

### Vendredi — Démos (30 min)

- Démo de ce qui a bougé les KR
- Pas de slide deck, pas de status report
- "Show, don't tell" — modèle qui répond, écran partagé
- Capture vidéo courte → archive trimestrielle

### Pivot/Persevere/Perish (fin trimestre)

Pour chaque KR à mi-trimestre (semaine 6/13) :

- **Persevere** : on continue, confidence ≥ 5/10
- **Pivot** : on change l'approche (même Objective, KR adjusté)
- **Perish** : on abandonne ce KR, pas atteignable

Pas honteux d'avoir des Perish — c'est honteux de **fake** un succès.

## Template OKR Q3 Neoteem — complet

```yaml
trimestre: 2026 Q3
equipe: IA Loji
owner: Raphael Picard

objective: |
  Devenir l'IA proptech qui fait gagner 1 jour/semaine
  à chaque gestionnaire syndic.

key_results:
  - id: KR1
    type: outcome
    metric: "% gestionnaires utilisant ≥1 agent IA quotidiennement"
    baseline: 18%
    target: 70%
    measure: telemetrie back2.0 (login + tool_call NeoChat/NeoDocs/Aurore)
    cadence_review: hebdo

  - id: KR2
    type: model
    metric: "Taux hallucination NeoChat sur questions mandats"
    baseline: 8%
    target: < 2%
    measure: eval set 500 questions, audit hebdo
    cadence_review: hebdo

  - id: KR3
    type: latency
    metric: "P95 latence NeoChat end-to-end"
    baseline: 2.8s
    target: < 1.5s
    measure: Datadog / OpenTelemetry GCP Cloud Run
    cadence_review: quotidien

  - id: KR4
    type: business
    metric: "Coût IA / mandat traité"
    baseline: 0.42 EUR
    target: 0.31 EUR (-25%)
    measure: facturation Gemini + GCP + opérations manuelles évitées
    cadence_review: mensuel

health_metrics:
  - "NPS gestionnaires utilisateurs IA (anti-trade-off vélocité vs qualité)"
  - "% temps Raphael sur shipping vs intake (anti-burnout)"
  - "Nombre incidents production IA / mois (anti-trade-off vitesse vs stabilité)"
  - "Couverture eval set NeoChat (anti-régression silencieuse)"
```

## Mixer KR business + KR modèle

### Erreur fréquente

Tout KR business → ignore qualité IA, on shippe bullshit qui convertit
Tout KR modèle → labo, pas de valeur business

### Mix recommandé équipe IA

| Catégorie | Exemple | % du total |
|---|---|---|
| Outcome utilisateur | Adoption, satisfaction, time saved | 30-40% |
| Modèle / qualité IA | Précision, hallucination, eval | 30-40% |
| Performance / coût | Latence, coût/requête, throughput | 20-30% |
| Business pur | Revenue, retention, NPS | 10-20% |

## Anti-patterns

- **KR = livrable** ("Livrer feature X") → c'est un task, pas un outcome
- **KR pas répondable OUI/NON** ("Améliorer la qualité") → test Doerr fail
- **Stretch goal atteint à 100%** → soit chance, soit trop facile. 70% = bon stretch
- **Cascader OKR top-down** → en équipe 1-5, alignement direct suffit
- **Réviser OKR à mi-trimestre** ("on baisse le target") → tue la discipline
- **OKR identique chaque trimestre** → pas un OKR, c'est une KPI baseline
- **Pas de health metrics** → optimiser vélocité au prix de qualité/burnout
- **OKR sur 13 semaines + Now/Next/Later** non aligné → roadmap dérive

## Anti-pattern Neoteem spécifique

"Implémenter Aurore v2" = mauvais KR (livrable).
**Bon KR** : "80% mandats classés auto sans intervention gestionnaire" (outcome).

## Sources

- John Doerr, "Measure What Matters" (2018)
- Christina Wodtke, "Radical Focus" 2e éd. (2021)
- Christina Wodtke blog — https://eleganthack.com/the-art-of-the-okr/
- Google rework — https://rework.withgoogle.com/guides/set-goals-with-okrs/

## Voir aussi

- [[index]]
- [[roadmap-now-next-later]]
- [[frameworks-comparatif]]
- [[intake-no-factory-yes-if]]
