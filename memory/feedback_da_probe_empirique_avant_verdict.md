---
name: da-probe-empirique-avant-verdict
description: DA sur idée-produit dont la prémisse est falsifiable = mesurer AVANT de débattre des garde-fous. Verdict (c) tuer si échec de prémisse, (b) garde-fous si échec de calibration. Sinon le verdict est de l'opinion.
metadata:
  type: feedback
---

Quand le DA porte sur une **idée-produit dont la valeur dépend d'une question mesurable** (ex : "% de transcript capitalisable et nouveau"), faire la **probe empirique AVANT de rédiger le verdict** — pas après, pas en hand-waving. La probe peut inverser le verdict attendu.

Critère d'arbitrage (c) vs (b) :
- **Échec de prémisse** (la donnée dit que le gisement n'existe pas, ex : 0/12) → verdict (c) tuer. Les garde-fous seraient du polish sur un puits sec.
- **Échec de calibration** (le bruit est modulable : heuristique trop large, fenêtre à borner, seuil à monter) → verdict (b) garde-fous.

**Why:** Session 27 mai, DA sur compounding rétroactif (A1×A3). Sans probe, j'allais vers (b) "build avec garde-fous". L'advisor a recadré : "sans le chiffre, ton verdict est de l'opinion". Probe sur 123 transcripts → 0/12 capitalisable-ET-nouveau sur la slice la PLUS chargée en signal → verdict (c). Tuer, pas calibrer. Distinct de [[verify-exhaustive-claims]] (grep avant déclaration "tous/zéro") et [[da-dicte-tests-adverses]] (code destructif).

**How to apply:** DA sur une idée à builder dont la prémisse est falsifiable → 1) identifier la question mesurable qui fait tenir/tomber l'idée, 2) mesurer sur l'existant en lecture seule (parseur réel, échantillon classé à la main, caveat de taille assumé), 3) classer (c)/(b) selon prémisse-vs-calibration. Ne JAMAIS proposer un "(b) light" pour épargner une idée séduisante quand la donnée dit (c) — c'est le biais que le DA est censé tuer.
