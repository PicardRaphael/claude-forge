---
aliases:
  - "SCQA"
  - "Pyramid Principle"
  - "Barbara Minto"
  - "pyramide Minto"
  - "Situation Complication Question Answer"
  - "top-down communication"
resume: "Structure SCQA + Pyramide Minto pour faire passer une recommandation IA à une direction non-tech sans la perdre."
derniere-maj: 2026-05-25
tags:
  - "#type/technique"
  - "#domaine/communication"
  - "#casquette/responsable-ia"
---

## TL;DR

- Réponse en premier, justification après — logique top-down
- SCQA = amorce universelle : **S**ituation → **C**omplication → **Q**uestion → **A**nswer
- Sous chaque idée, 3 sous-idées MECE (Mutually Exclusive, Collectively Exhaustive)
- Une direction non-tech décroche à la 4e ligne — fais entrer la conclusion ligne 1

## Origine

- Barbara Minto, *The Pyramid Principle* (1973), ex-McKinsey
- Standard consulting (BCG, Bain, McKinsey)
- Repris dans les notes Amazon, Google, Stripe

## Le triangle Minto

```
              [Recommandation principale]
                       /    |    \
                     /      |      \
              [Argument 1] [Arg 2] [Arg 3]
                /  |  \    /  |  \   /  |  \
            [data] [data] ... preuves chiffrées
```

- Sommet = LA réponse à la question business
- 2e niveau = 2-4 raisons MECE
- Base = données / faits / sources

## SCQA — l'amorce

| Étape | Question implicite | Longueur |
|-------|-------------------|----------|
| Situation | Ce que tout le monde sait | 1-2 phrases |
| Complication | Pourquoi ça ne suffit plus | 1-2 phrases |
| Question | Décision à prendre | 1 phrase |
| Answer | Recommandation chiffrée | 1 phrase |

L'Answer **est** le sommet de la pyramide.

## Exemple — Email COO Neoteem

```
Objet : Délai fiche mandat — recommandation : automatiser plutôt que recruter

Claire,

Situation : nous avons 4 conseillers qui gèrent 800 mandats actifs.

Complication : depuis février, le délai de rédaction d'une fiche
mandat est passé de 2 à 6 jours. 12% des syndics tests ont demandé
un crédit. Le pipeline alpha est bloqué.

Question : recruter 2 ETP supplémentaires (~110k€/an) ou automatiser
la rédaction de fiches ?

Recommandation : automatiser via Aurore (RAG NeoChat + GEMINI).
ROI sur 8 mois, qualité supérieure mesurée sur cohorte test.

Trois raisons :
1. Coût total Y1 38k€ contre 110k€ recrutement (cf. business case joint)
2. Qualité : taux d'erreur notaire descendu de 8% à 1.5% sur 40 fiches test
3. Scalabilité : aucun coût marginal au-delà de 800 mandats

Je propose une décision au prochain Comex du 12 juin.
Tu trouveras le business case 1-page et le PR-FAQ Aurore en pièce jointe.

Raphael
```

## Règle MECE — exemples

| Découpage | MECE ? |
|-----------|--------|
| Coût / Qualité / Temps | OUI |
| Coût build / Coût run / Coût opportunité | OUI |
| Tech / Business | NON (overlap) |
| Court terme / Important / Urgent | NON (catégories qui se chevauchent) |

## Quand utiliser

- Email > 5 lignes au Comex / COO / CEO
- Slide d'ouverture board / Comex
- Slack `#exec` annonce décision
- Première page d'un Six-Pager → voir [[../reunions/codir-6-pager-bezos]]

## Anti-patterns

- Démarrer par "Suite à notre échange..." → 0 information, perdu en ligne 1
- Mettre la recommandation en conclusion → personne ne lit jusqu'au bout
- 7 raisons listées → le cerveau en retient 3, choisis-les
- Mélanger faits et opinions sans étiquette → perte de crédibilité
- Sous-idées qui se chevauchent → non-MECE, signal de pensée floue

## Sources

- Barbara Minto — *The Pyramid Principle: Logic in Writing and Thinking* (1996, 3e éd.) https://www.barbaraminto.com/
- McKinsey — *Communicating with Impact* (formation interne, public via SlideShare)
- Lenny Rachitsky — https://www.lennysnewsletter.com/p/the-art-of-communication

## Liens

- [[index]]
- [[../index]]
- [[../reunions/codir-6-pager-bezos]]
- [[bluf-bottom-line-up-front]]
