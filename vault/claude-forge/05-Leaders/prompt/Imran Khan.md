---
titre: "Imran Khan"
resume: "Chercheur indépendant, auteur de 'You Don't Need Prompt Engineering Anymore: The Prompting Inversion' (arXiv 2510.22251, oct 2025) — paper introducing 'Sculpting' et concept Guardrail-to-Handcuff"
aliases:
  - "Imran Khan"
  - "imran khan"
  - "Khan"
  - "Sculpting paper author"
  - "Prompting Inversion author"
domaine: prompt-engineering
type: leader
affiliation: "Independent Researcher"
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://arxiv.org/abs/2510.22251"
tags:
  - "#type/leader"
  - "#domaine/prompt-engineering"
---

## Profil

Chercheur indépendant. Information publique minimale — connu via son paper arXiv d'octobre 2025.

## Contribution canonique

### "You Don't Need Prompt Engineering Anymore: The Prompting Inversion" (octobre 2025)

[arXiv 2510.22251](https://arxiv.org/abs/2510.22251). Introduit :

#### 1. "Sculpting"

Méthode de prompting contrainte et basée sur des règles, conçue pour améliorer le Chain-of-Thought standard.

#### 2. Concept "Guardrail-to-Handcuff"

Les contraintes qui aident les modèles mid-tier deviennent des **menottes** sur les modèles avancés. Phénomène d'**hyper-literalism**.

#### 3. Mesures sur GSM8K

Testé sur 3 générations OpenAI (gpt-4o-mini, gpt-4o, gpt-5) :
- Sculpting **améliore** gpt-4o : 97% vs 93% baseline
- Sculpting **nuit** gpt-5 : 94% vs 96.36% baseline

→ Conclusion : "simpler prompts for more capable models"

## Pourquoi le citer

Source primaire **single source acceptable** sur :
- Concept Sculpting (auteur original)
- Guardrail-to-Handcuff transition
- Mesures empiriques GSM8K sur gpt-4o vs gpt-5

⚠️ **Attribution forge précédemment incorrecte** : ce paper était attribué à "Mikinka UCL" — c'est faux. Imran Khan, indépendant.

## Liens

- [[Anthony Mikinka]] — paper UCL distinct (arxiv 2601.00880)
- [[over-specification-paradox]] — note vault avec Sculpting
- [[deprecated-techniques-2026]] — concepts liés
- [[MOC-Leaders]]
