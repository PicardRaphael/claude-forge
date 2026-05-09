---
description: "Run devils-advocate agent before delivering major work — skills, agents, architecture decisions, technique proposals"
---

# Devil's Advocate — OBLIGATOIRE avant livraison majeure

## Qui est concerné

TOUT LE MONDE. Les agents spécialisés ET la session principale (moi).

- **Agents** : le hook `devil-advocate-guard.py` rappelle automatiquement après chaque agent qui produit un livrable
- **Session principale** : AVANT de proposer une innovation, une architecture, une technique à Raphael → lancer devil's advocate. Pas "challenger mentalement" — LANCER L'AGENT. La session 2026-05-09 a prouvé que le challenge mental ne suffit pas (3 bloquants trouvés par l'agent que j'avais manqués).

## Quand invoquer

| Livrable | Devil's advocate ? |
|----------|-------------------|
| Nouvelle skill créée | OUI — hook automatique |
| Nouvel agent créé | OUI — hook automatique |
| Nouveau hook créé | OUI — hook automatique |
| Décision d'architecture | OUI — session principale |
| Proposition de technique / innovation | OUI — session principale |
| Proposition Jarvis (croisement inédit) | OUI — surtout celles-là |
| Modification de CLAUDE.md | NON — trop fréquent |
| Fix de bug / correction mineure | NON |
| Recherche / synthèse informative | NON |

## Comment l'intégrer

1. Terminer le livrable normalement (via agents spécialisés)
2. Lancer `devils-advocate` avec le livrable en contexte
3. Présenter à Raphael : le livrable + la critique + ta réponse à la critique
4. Le devil's advocate sauvegarde sa critique dans le vault (`Knowledge/critiques/`)

## Pipeline complet avec devil's advocate

```
architect-first → implémentation → test/review → devil's advocate → livraison
```

Le devil's advocate est le DERNIER gate avant la livraison. Il ne bloque pas — il informe.

## Ce que le devil's advocate consulte dans le vault

AVANT de critiquer, il DOIT chercher :
- `Knowledge/erreurs/` — erreurs passées similaires
- `Knowledge/critiques/` — critiques précédentes sur le même sujet
- `Knowledge/raisonnements/` — raisonnements validés pertinents

## Anti-patterns

- Invoquer devil's advocate sur tout → fatigue, on l'ignore. Réservé aux livrables MAJEURS.
- Ignorer systématiquement ses objections BLOCKING → alors autant ne pas l'avoir.
- Ne pas sauvegarder dans le vault → on perd l'apprentissage.
