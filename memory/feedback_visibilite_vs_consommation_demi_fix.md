---
name: visibilite-vs-consommation-demi-fix
description: Rendre une donnée VISIBLE (liste synced, doc à jour) ≠ rendre le CONSOMMATEUR capable de l'utiliser. Un sync qui met à jour une liste mais pas les queries/code qui la consomment = moitié cosmétique. Vérifier le chemin complet donnée→usage avant de déclarer FAIT.
metadata:
  type: feedback
---

Quand un chantier « synchronise » ou « met à jour » une donnée partagée, distinguer deux moitiés : (1) la **visibilité** — la donnée est à jour, lisible, propre ; (2) la **consommation** — le code/process qui l'utilise vise réellement la nouvelle donnée. Résoudre (1) sans (2) = moitié cosmétique qui *paraît* finie.

**Why:** Chantier C cc-news (27 mai 2026). Le script sync-leaders a régénéré la table « Leaders canonisés » des domain-*.md depuis le vault (visibilité ✓). Mais les agents cc-news exécutent le bloc `## Queries à exécuter`, PAS la table Leaders — et les queries n'ont pas été régénérées. Donc cc-news continuait à rater ~50 leaders pourtant désormais listés. C'était précisément le problème que le chantier devait résoudre. Le report du script listait les leaders sans query sous mes yeux, mais mon self-check l'a évacué en « dette mineure » au lieu de le voir comme la moitié manquante. L'advisor a rattrapé.

**How to apply:** Avant de déclarer un sync/refonte « FAIT », tracer le chemin complet **donnée → consommateur → usage effectif** et vérifier que chaque maillon pointe vers la nouvelle donnée. Si un maillon reste sur l'ancien (queries hardcodées, cache, mapping figé), ce n'est pas livré — c'est tracé comme dette explicite et annoncé comme tel (cf [[ecart-consigne-chiffree-surfacer]]). Ne jamais présenter la moitié visible comme le tout. Lien : [[pas-de-symetrie-artificielle-priorisation]] (impact réel, pas équilibre cosmétique).
