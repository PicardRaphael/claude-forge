---
name: doctrine-deployment-lag-piege
description: Quand une revision majeure de doctrine est capitalisee dans le vault, verifier sous 24h le deploiement effectif sur TOUS les repos concernes, sinon la session suivante revit l'erreur initiale
metadata:
  type: feedback
---

Quand une critique aboutit a une revision majeure de doctrine (ex pipeline 22 mai 2026), la note vault et les commits dans 1-2 repos ne suffisent PAS. Verifier qu'aucun repo concerne n'est reste sur l'ancienne doctrine.

**Why** : 21 mai 2026, Raphael a perdu 4h sur un fix de bug parce que neo_ia avait gardé un setup TDD strict + chaine markers 5 hooks alors que la doctrine corrigee existait dans le vault depuis 24h. Contradictions internes detectees (quality-gates.md ligne 116 vs testing-mandatory.md ligne 124). La session a litteralement revecu l'erreur deja documentee.

**How to apply** : Quand on critique un setup et qu'on trouve dans le vault que la correction a deja ete capitalisee mais pas appliquee a ce repo, ne PAS reciter la critique — diagnostiquer le delai de deploiement comme le vrai probleme. Verifier les 3 fichiers cles : rules avec contradictions internes, hooks avec bugs deja patches dans Knowledge/erreurs/, agents avec instructions desuetes.

**Symptome rapide** : si vault dit "phase REFACTOR SUPPRIMEE" et rule dit encore "test-writer phase=refactor" → desynchronisation deterministe, generera des erreurs.

Lie a [[workaround-becomes-sediment]] (memoire forge) et [[erreur-pipeline-trop-long-frustration]] (vault).
