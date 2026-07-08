---
aliases:
  - WSJF
  - Weighted-Shortest-Job-First
  - WSJF-Reinertsen
  - WSJF-SAFe
  - cost-of-delay
resume: "WSJF (Weighted Shortest Job First) de Reinertsen / SAFe — formule, Fibonacci, exemple RGPD vs intégration, quand l'utiliser en équipe 1-5 personnes."
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#domaine/priorisation"
  - "#casquette/responsable-ia"
---

## TL;DR

- **WSJF = Cost of Delay / Job Size**
- **CoD = Business Value + Time Criticality + Risk Reduction / Opportunity Enablement**
- Échelle **Fibonacci** : 1, 2, 3, 5, 8, 13, 20 (force différenciation)
- Équipe 1-5 : utiliser uniquement pour **compliance** + **dépendances cross-équipe**
- Pour features produit standard → [[rice-en-pratique]]

## Formule

```
WSJF = (Business Value + Time Criticality + Risk Reduction/Opportunity Enablement) / Job Size

CoD = BV + TC + RR/OE
```

### Pourquoi Fibonacci

Échelle 1-10 → tout devient 6 ou 7. Fibonacci (1, 2, 3, 5, 8, 13, 20) force à choisir un ordre de grandeur.

## Les 4 composantes

| Composante | Question clé | Score Fibo |
|---|---|---|
| **Business Value (BV)** | Quelle valeur économique livrée ? Revenue/coût évité ? | 1-20 |
| **Time Criticality (TC)** | La valeur décroît-elle si on retarde ? Deadline légale ? | 1-20 |
| **RR/OE** | Réduit-on un risque ? Débloque-t-on autre chose ? | 1-20 |
| **Job Size** | Effort relatif équipe (proxy effort + complexité) | 1-20 |

## Exemple chiffré — Patch sécu RGPD vs nouvelle intégration

### Item A — Patch RGPD logs NeoChat

Anonymiser les logs NeoChat (PII locataires actuellement loggés en clair).

| Composante | Score | Justif |
|---|---|---|
| BV | 3 | Pas de revenue direct |
| TC | 20 | CNIL audit possible Q4, amende potentielle 4% CA |
| RR/OE | 13 | Risque RGPD majeur |
| **CoD** | **36** | |
| Job Size | 3 | 2 semaines back2.0 + audit |
| **WSJF** | **12** | |

### Item B — Intégration Pennylane comptabilité syndics

Connecteur API Pennylane pour syndics Loji (demande commerciale 3 prospects).

| Composante | Score | Justif |
|---|---|---|
| BV | 13 | 3 deals signés conditionnels |
| TC | 5 | Concurrents (Genius Immo) ont déjà |
| RR/OE | 3 | Pas critique |
| **CoD** | **21** | |
| Job Size | 8 | 6 semaines dev + API partenaire |
| **WSJF** | **2.6** | |

### Décision

**Item A WSJF=12 > Item B WSJF=2.6** → patch RGPD d'abord. Pourtant Pennylane "rapporte plus" en BV brut — c'est exactement le point de WSJF : intégrer le coût du retard.

## Quand utiliser WSJF en équipe 1-5

### OUI

- Patch sécurité, compliance (RGPD, hébergement données santé HDS)
- Dépendances bloquantes cross-équipe (dev back2.0 attend devops, design attend redaction)
- Choix entre 2 chantiers de durée très différente (1 sem vs 2 mois)
- Arbitrage technical debt vs feature (TC + RR/OE explicite)

### NON

- Roadmap features classique → RICE plus simple
- Backlog > 20 items → WSJF devient lourd, utiliser RICE puis WSJF sur top 5
- Équipe 1 personne sans dépendance → théâtre process

## Cadence Neoteem

- **Trimestriel** : scoring WSJF des 5 candidats "compliance/debt/dépendance"
- **Ad hoc** : tout patch sécu critique → WSJF immédiat avant intake form

## Template scoring inline

```markdown
| Item | BV | TC | RR/OE | CoD | Size | WSJF |
|---|---|---|---|---|---|---|
| [nom] | | | | =BV+TC+RR | | =CoD/Size |
```

## Anti-patterns

- **Gonfler artificiellement RR/OE** pour pousser sa techno préférée ("ça réduit la dette") — challenger à 2
- **TC à 20 par défaut** sur tout — diluer le signal urgence
- Job Size = effort réel en jours (perdre la propriété relative) → garder Fibonacci
- WSJF appliqué à 50 items = paralysie. Filtrer top 10 d'abord
- Confondre BV avec "ce qui me plaît" — exiger preuve (deal signé, demande répétée)
- Recalibrer Fibonacci à mi-trimestre → casse la baseline

## WSJF vs RICE

| Critère | RICE | WSJF |
|---|---|---|
| Public cible | Product managers | Lean/SAFe teams |
| Échelle | Numérique (Reach réel) | Fibonacci relatif |
| Time criticality | Implicite (Reach × période) | **Explicite (TC)** |
| Risk/compliance | Faible | **Fort (RR/OE)** |
| Vitesse scoring | 2 min/item | 5 min/item |
| Idéal pour | Features produit | Compliance, dépendances, debt |

## Sources

- Donald Reinertsen, "The Principles of Product Development Flow" (2009), ch. 2
- SAFe Framework — https://scaledagileframework.com/wsjf/
- Joshua Arnold, "Cost of Delay Divided by Duration" — https://blackswanfarming.com/cost-of-delay-divided-by-duration/

## Voir aussi

- [[index]]
- [[frameworks-comparatif]]
- [[rice-en-pratique]]
- hidden-tech-debt-ml-sculley
