---
titre: "Over-Specification Paradox"
resume: "Papier UCL (arXiv 2601.00880) : au-delà du seuil S*=0.509, chaque spécification supplémentaire dégrade les performances des modèles frontier de façon quadratique"
aliases:
  - "over-specification paradox"
  - "paradoxe sur-spécification"
  - "UCL prompting paper"
  - "seuil S star"
  - "UCL 2601.00880"
  - "over specification"
domaine: technique
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://arxiv.org/abs/2601.00880"
  - "https://arxiv.org/abs/2510.22251"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Description

Papier académique de Anthony Mikinka (UCL, arXiv 2601.00880, déc. 2025). Prouve mathématiquement via le framework **Universal Conditional Logic (UCL)** qu'il existe un seuil de spécification optimal au-delà duquel les performances se dégradent.

Testé sur 305 prompts, 11 modèles. Résultat : **29.8% de réduction de tokens** possible sans perte de performance.

## Le seuil S* = 0.509

Au-delà de 50.9% du niveau de spécification optimal :
- Dégradation **quadratique** des performances
- Les contraintes deviennent des "menottes" plutôt que des guides
- Plus de spécification = moins bon résultat

## Transition Guardrail → Handcuff

Papier "You Don't Need Prompt Engineering Anymore: The Prompting Inversion" (arXiv 2510.22251, **Imran Khan**, indépendant, oct 2025) — concept "Sculpting" :

> Les contraintes qui aident les modèles mid-tier causent de l'**hyper-literalism** sur les modèles avancés.

Ce qui protège un GPT-4o-mini contre les dérives devient une contrainte qui empêche un gpt-5 (ou Opus 4.7) de trouver de meilleures solutions. Mesuré sur GSM8K : Sculpting améliore gpt-4o (97% vs 93%) mais NUIT gpt-5 (94% vs 96.36% baseline).

**Guardrail** (modèles standard) → **Handcuff** (modèles avancés) = même règle, effet inverse.

> ⚠️ Correction 2026-05-23 : attribution forge précédente "Mikinka UCL" pour ce paper était fausse — Sculpting paper = **Imran Khan (indépendant)**, distinct du paper UCL Mikinka 2601.00880.

## Implications pratiques

| Ce qu'on pensait | Ce que les données montrent |
|---|---|
| Plus de contraintes = plus de contrôle | > S*=0.509 : contraintes dégradent le résultat |
| Instructions détaillées = meilleure sortie | Frontier models font mieux avec moins |
| Exemples multiples = ancrage fort | Few-shot overwhelm le raisonnement interne |
| MUST/NEVER renforce les règles | Coupe la capacité du modèle à trouver mieux |

## 29.8% de réduction de tokens

Optimum atteint en supprimant les spécifications au-delà du seuil. Impact double :
- Coût tokens réduit
- Performance augmentée

## Quand utiliser

- Audit de prompts existants sur modèles frontier (Opus 4.7, GPT-5.x, Gemini 2.5)
- Avant de déployer un prompt en production : vérifier qu'on n'est pas au-delà de S*
- Justification pour simplifier des prompts complexes hérités de 2023-2024

## Liens

- [[outcome-first-prompting]] — Alternative : définir l'outcome, pas le process
- [[deprecated-techniques-2026]] — Techniques désormais contre-productives
- [[Context Engineering]] — Paradigme optimal : composition, ranking, optimization
- [[amanda-askell-prompt-engineering]] — TDD system prompts, approche Anthropic
- [[MOC-Techniques]]
