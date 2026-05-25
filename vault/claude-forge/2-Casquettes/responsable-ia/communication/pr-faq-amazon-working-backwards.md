---
aliases:
  - "PR-FAQ Amazon"
  - "Working Backwards"
  - "press release first"
  - "PRFAQ"
  - "Amazon working backwards"
  - "PR/FAQ"
resume: "Format PR-FAQ Amazon (Bryar/Carr) — écrire le communiqué de presse AVANT de coder pour forcer l'alignement outcome et l'investissement justifié."
derniere-maj: 2026-05-25
tags:
  - "#type/technique"
  - "#domaine/communication"
  - "#casquette/responsable-ia"
---

## TL;DR

- Écris le communiqué de presse de la feature **avant** de la construire
- Force à formuler le bénéfice client en langage non-tech
- Si tu n'arrives pas à écrire un PR convaincant en 1 page, la feature n'est probablement pas prête
- Itère le PR-FAQ jusqu'à conviction, **puis** brief tech

## Origine

- Colin Bryar + Bill Carr, *Working Backwards* (2021)
- Pratique Amazon depuis ~2004
- Standard d'entrée des Six-Pagers Bezos → voir [[../reunions/codir-6-pager-bezos]]

## Structure PR-FAQ

### Press Release (1 page max)

| Section | Contenu | Longueur |
|---------|---------|----------|
| Heading | Nom feature + bénéfice principal | 1 ligne |
| Sub-heading | Cible + outcome chiffré | 1 ligne |
| Summary | Quoi, pour qui, quand | 3-4 lignes |
| Problem | Douleur actuelle quantifiée | 3-4 lignes |
| Solution | Comment ça marche (non-tech) | 4-5 lignes |
| Citation dirigeant | Vision business | 2 lignes |
| Citation client | Bénéfice vécu | 2 lignes |
| Comment commencer | Onboarding utilisateur | 2-3 lignes |

### FAQ Externe (questions client)

- Comment ça coûte ?
- Quelle différence vs concurrent X ?
- Que se passe-t-il si l'IA se trompe ?
- Mes données sont-elles utilisées pour entraîner un modèle ?

### FAQ Interne (questions Comex)

- Économie unitaire : coût marginal par usage vs prix vendu ?
- TAM : combien de mandats actifs adressables sur le marché FR ?
- Faisabilité technique : dépendances bloquantes ?
- Cannibalisation : impact sur autres briques Loji ?

## Template Neoteem rempli — Aurore

```markdown
# Loji lance Aurore : la fiche mandat rédigée en 90 secondes

**Pour les syndics et gérants, Aurore génère une fiche mandat complète
à partir des documents bruts en moins de 2 minutes — au lieu de 45.**

## Résumé
Aurore est la nouvelle brique IA de Loji. Disponible dans NeoDocs dès
juillet 2026, elle lit les pièces du dossier (bail, état des lieux, RIB,
DPE) et propose une fiche mandat structurée, validée par le gérant en 1 clic.

## Problème
Un gérant immobilier rédige aujourd'hui une fiche mandat en 30 à 45 min.
Sur 800 mandats actifs, c'est 2 ETP mobilisés. Les erreurs de saisie
provoquent 8% de retours notaire.

## Solution
Aurore utilise GEMINI couplé à NeoDocs pour extraire les données clés
des pièces uploadées et pré-remplir la fiche Loji. Le gérant relit,
ajuste, valide. Aucune donnée n'est envoyée hors UE.

## "Notre métier, c'est de signer plus de mandats, pas de remplir
des formulaires. Aurore rend 2 ETP au commercial."
— Claire Dumas, COO Loji

## "J'ai validé ma première fiche en 90s. Avant je bloquais une
demi-journée par semaine sur la saisie."
— Marc Berger, syndic test alpha

## Comment commencer
Activez Aurore dans NeoDocs → Paramètres → IA. Premier mandat offert.
```

## Quand utiliser

| Cas | PR-FAQ ? |
|-----|----------|
| Nouvelle brique IA (Aurore, futurs agents) | OUI — obligatoire |
| Feature majeure NeoChat / NeoDocs | OUI |
| Refonte UX visible client | OUI |
| Bug fix / optimisation interne | NON |
| Spike technique | NON — utiliser ADR |

## Anti-patterns

- Écrire le PR-FAQ **après** avoir codé → rationalisation
- PR > 1 page → la feature fait trop de choses
- Citation dirigeant en langage marketing creux ("révolutionner", "disrupter") → re-écrire
- FAQ interne absente → Comex va refuser le go
- Pas de chiffre dans le problem → "c'est juste un nice-to-have"
- Citation client inventée sans interview alpha-tester → fragile en Comex

## Sources

- Colin Bryar, Bill Carr — *Working Backwards: Insights, Stories, and Secrets from Inside Amazon* (2021) https://www.workingbackwards.com/
- Ian McAllister (ex-Amazon) — https://www.quora.com/What-is-Amazons-approach-to-product-development-and-product-management
- Lenny Rachitsky — https://www.lennysnewsletter.com/p/the-ultimate-guide-to-writing-prfaqs

## Liens

- [[index]]
- [[../index]]
- [[../reunions/codir-6-pager-bezos]]
