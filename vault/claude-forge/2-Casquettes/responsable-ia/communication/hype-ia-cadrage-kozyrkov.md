---
aliases:
  - "cadrage hype IA"
  - "Kozyrkov hype"
  - "anti-FOMO IA"
  - "marketing victims IA"
  - "désamorcer hype IA"
  - "freiner dirigeants IA"
resume: "Désamorcer la hype IA en interne (CEO/COO/Sales) avec le diagnostic Kozyrkov et 3 scripts de cadrage prêts à l'emploi."
derniere-maj: 2026-05-25
tags:
  - "#type/technique"
  - "#domaine/communication"
  - "#casquette/responsable-ia"
---

## TL;DR

- Le risque #1 du Lead IA n'est pas le retard, c'est le **launch at all costs**
- Diagnostic Kozyrkov : les "marketing victims" lancent sans fondations data
- Ton job = ritualiser un langage de cadrage qui protège la boîte sans tuer l'élan
- Toujours valider l'objectif, jamais le calendrier hype-driven

## Diagnostic Kozyrkov

Cassie Kozyrkov (ex-Chief Decision Scientist Google) identifie 3 symptômes :

1. **Marketing victims** : dirigeants qui réagissent au bruit LinkedIn/TechCrunch, pas aux signaux clients
2. **Launch at all costs** : sortir une feature IA "pour exister", sans eval, sans data, sans cas d'usage validé
3. **Absence de fondations data** : pas d'eval set, pas de baseline, pas de métrique → impossibilité de mesurer succès ou échec

> "When you invite complexity at scale, you may have quite the opposite of ROI."
> — Cassie Kozyrkov

## Triple cadrage Neoteem

### 1. CEO : "Il faut faire comme OpenAI"

```
CEO : "OpenAI sort un agent pour l'immobilier. Il faut qu'on ait le nôtre."

TOI : "Je suis aligné sur l'objectif : on doit avoir une réponse IA visible
       d'ici septembre. Trois questions avant de m'engager sur le 'comment' :

       1. Quel problème client est-ce qu'on veut résoudre en priorité —
          fiche mandat, relance locataire, ou recherche dans baux ?
       2. Sur quels 3 KPI on mesure le succès dans 6 mois ?
       3. Quel budget compute on cible sur 12 mois ?

       Avec ça je te reviens avec 2 scénarios chiffrés sous 1 semaine."
```

### 2. COO : "Mettre ChatGPT partout"

```
COO : "On devrait mettre ChatGPT dans tous les écrans Loji."

TOI : "L'instinct est juste — l'IA doit être visible dans le produit.
       Le risque de mettre 'ChatGPT' générique partout : on devient
       un wrapper, sans moat. Notre avantage c'est NeoDocs sur les baux,
       NeoChat sur les locataires.

       Je propose 2 chantiers IA verticaux où on a la data unique :
       Aurore (fiche mandat) et un assistant relance locataire.
       Plutôt qu'un chatbot horizontal. Je t'envoie un PR-FAQ sur chaque
       cette semaine, tu tranches."
```

### 3. Commercial : "J'ai promis l'IA au prospect"

```
SALES : "J'ai promis à Foncia que Loji aurait l'IA dispo en juin."

TOI : "OK. Avant de partir en panique, on cadre :
       - L'IA est dispo : NeoChat est en prod depuis mars.
       - Ce qui n'est pas dispo : Aurore en GA (cible 01/07).
       - Foncia attend quoi exactement ? Un agent conversationnel ou
         la rédaction automatique de fiches ?

       Je te propose 2 options pour Foncia :
       a) Démo Aurore alpha avant le 15/06 — j'organise
       b) Lettre d'engagement GA 01/07 avec SLA chiffré

       Je préfère ne pas mentir sur la GA — Foncia parle à 4 autres
       syndics, le bouche-à-oreille tue plus que le délai."
```

## 5 phrases magiques à ritualiser

```
1. "Je suis aligné sur l'objectif. Avant de m'engager sur le 'comment',
    on a besoin de [eval set | baseline | budget compute]."

2. "Le risque dans 6 mois c'est pas le retard, c'est de lancer un truc
    qu'on ne sait pas mesurer."

3. "On a 2 scénarios : conservateur, ambitieux. Je préfère sur-livrer
    sur le conservateur que rater l'ambitieux."

4. "Notre moat n'est pas le modèle, c'est la data Loji. Si on lance
    un wrapper, on est mort dans 12 mois."

5. "Cette feature, je peux la livrer. Voici les 2 contreparties :
    [délai | scope | autre chantier dépriorisé]."
```

## Anti-patterns

- Dire "non" sans alternative → on te court-circuite
- Promettre sans eval set → tu paies l'addition dans 3 mois
- Lancer une POC pour "prouver qu'on fait" → POC bloquée en POC purgatory
- Tomber dans la guerre des outils ("Anthropic vs OpenAI") → exec s'en fout
- Snobisme technique ("vous ne comprenez pas le RAG") → perte d'influence
- Sous-estimer la pression Sales → ce sont eux qui ramènent le revenu

## Quand céder

Cas où tu cèdes au calendrier hype-driven :

- Risque contractuel direct (deal > X k€ à signer)
- Décision Board / investisseurs qui crée un effet d'annonce
- Feature lancée en mode "alpha contrôlé" avec opt-in explicite

Tu **ne cèdes jamais** sur :

- Eval set absent
- Aucun owner business identifié
- Pas de plan de rollback
- Pas de mesure de qualité côté client

## Sources

- Cassie Kozyrkov — *Marketing victims of AI* https://kozyrkov.medium.com/
- Cassie Kozyrkov — *The first step of an AI project* https://hbr.org/2019/05/the-first-step-of-an-ai-project
- Ethan Mollick — *Co-Intelligence* (2024) https://www.oneusefulthing.org/
- a16z — *The state of AI report* https://a16z.com/

## Liens

- [[index]]
- [[../index]]
- [[parler-non-tech-vulgarisation]]
- dire-non-yes-and-fournier
- [[../reunions/reunion-client-hype-management]]
