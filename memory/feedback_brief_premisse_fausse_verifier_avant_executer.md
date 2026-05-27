---
name: brief-premisse-fausse-verifier-avant-executer
description: Un brief de mission peut poser une prémisse factuelle fausse (fichier ciblé, chiffre, état du repo). Vérifier matériellement la prémisse AVANT d'exécuter, et si fausse, surfacer + ré-arbitrer le périmètre — jamais exécuter le brief littéralement.
metadata:
  type: feedback
---

Un brief de mission (même détaillé, même avec méthode A→E) n'est pas une source de vérité : il encode l'intention de Raphael à un instant T, pas l'état réel du repo. Avant d'exécuter une instruction qui repose sur une prémisse factuelle (« le fichier X contient N lignes ad-hoc », « la garde Y existe », « le déploiement Z reste à faire »), la vérifier matériellement. Si la prémisse est fausse, surfacer l'écart + ré-arbitrer le périmètre via AskUserQuestion — ne jamais exécuter le brief littéralement sur une base fausse.

**Why:** 27 mai 2026 — brief « nettoyer settings.json claude-forge, ~66 lignes de permissions ad-hoc accumulées ». Vérif empirique : `settings.json` versionné = 163L mais DISCIPLINÉ (chaque entrée a un commit traçable, 11 hooks tous vivants, 23L de permissions seulement). La vraie dette ad-hoc (38/51 entrées mortes/redondantes : cp/sed/node -e morts, git -C doublon de git *, MCP) était dans `settings.local.json` (gitignored, perso) — un fichier que le brief ne mentionnait même pas. Exécuter le brief littéralement = épurer le mauvais fichier pour un gain marginal et rater 95% de la dette. Surfacé via AskUserQuestion → Raphael a confirmé le pivot de périmètre et salué la correction.

**How to apply:** au démarrage d'un chantier, lister les prémisses factuelles du brief (fichiers nommés, chiffres, états supposés) et les matérialiser avant de planifier : `ls`/parse/`git log` sur les fichiers cités, ET chercher les fichiers VOISINS que le brief n'a pas nommés (settings.json ⨯ settings.local.json, .md ⨯ references/). Si le réel diverge du brief sur un point qui change ce que je touche → AskUserQuestion de périmètre, pas exécution littérale.

Extension de [[diagnostic-empirique-avant-affirmer-une-garde]] (vérifier une garde avant de l'ÉCRIRE) au brief comme source faillible : ici on vérifie une prémisse avant de l'EXÉCUTER. Distinct de [[ecart-consigne-chiffree-surfacer]] (écart de MON livrable vs cible chiffrée) — ici c'est une prémisse du brief qui est fausse en amont. Lié à [[spec-brief-distant-repo-scope]] (un brief distant = contrat, pas vérité interne).
