---
aliases:
  - NBER 34836 Firm Data AI
  - AI productivity paradox 2026
  - 6000 executives survey AI
  - 89 percent zero productivity
  - Bloom Davis AI firm survey
  - infrastructure gap productivity AI
resume: "NBER Working Paper 34836 (Yotzov, Barrero, Bloom, Davis et al., fév 2026) — survey 6000 execs US/UK/DE/AU. 89% des firmes rapportent ZÉRO impact productivité AI. Gap = infrastructure, pas modèle."
derniere-maj: 2026-05-26
tags:
  - "#type/news"
  - "#domaine/industrie"
  - "#source/nber"
  - "#statut/canonique"
---

# NBER Working Paper 34836 — Firm Data on AI

## Source primaire

- NBER WP 34836, février 2026
- Auteurs : Ivan Yotzov, Jose Maria Barrero, **Nicholas Bloom**, Philip Bunn, **Steven J. Davis**, Kevin M. Foster, Aaron Jalca, Brent H. Meyer, Paul Mizen, Michael A. Navarrete, Pawel Smietanka, Gregory Thwaites, Ben Zhe Wang
- Survey : ~6000 senior executives US / UK / Allemagne / Australie

## Résultats chiffrés clés

### Adoption large, usage shallow

- **69% des firmes** utilisent activement AI
- **Plus des 2/3 des execs** utilisent régulièrement AI
- Mais usage moyen exec = **1.5 heures par semaine seulement**

### 89% : ZERO productivity impact

- **89% rapportent aucun impact** sur labor productivity (sales per employee) sur 3 ans
- **>90% rapportent aucun impact** sur l'emploi propre
- Seulement une petite minorité voit des effets positifs

### Usage typique

1. Text generation via LLM
2. Visual content creation
3. Data processing via machine learning

### Anticipations futures (3 ans)

- +1.4% productivité prévue
- +0.8% output
- -0.7% employment
- Larger firms plus optimistes
- Employés plus optimistes (+0.5% jobs) que execs (-0.7%)

## Le pattern Solow Paradox 2.0

> $2.5 trillion dépensés globalement sur AI en 2026, mais 9 firmes sur 10 ne peuvent pointer un seul chiffre productivité qui a bougé.

Echo de Robert Solow 1987 : *"you can see the computer age everywhere but in the productivity statistics"*.

Paper sœur NBER 34984 ajoute : **productivity paradox** = gains perçus > gains mesurés (delay de réalisation des revenus).

## Implications pour forge / claude-forge

1. **L'avantage n'est pas dans le modèle, il est dans l'infrastructure autour**. C'est exactement la thèse de ECC (Affaan Mustafa) et de notre setup claude-forge.
2. **89% des execs en sont au stage "AI feature isolée"**. Notre 28+ agents + 30 skills + 14 hooks = stade qu'aucune entreprise du survey n'atteint.
3. **Companies avec infra agentique = 30-50% acceleration** (cf [[software-factory-pattern-2026]]). Confirme que l'investissement infrastructure paie.
4. Argument fort pour défendre notre dimensionnement vs sceptiques.

## Liens

- [[ecc-pattern-personal-dev-setup]] — exemple d'infrastructure qui marche
- [[affaan-mustafa-ecc-hackathon-winner]]
- [[software-factory-pattern-2026]]

## Référence

- [NBER WP 34836 PDF](https://www.nber.org/system/files/working_papers/w34836/w34836.pdf)
- [NBER WP 34836 page](https://www.nber.org/papers/w34836)
- [The Register coverage Feb 2026](https://www.theregister.com/2026/02/18/ai_productivity_survey/)
- Paper sœur : [NBER WP 34984](https://www.nber.org/papers/w34984)
