---
name: conformite-aveugle-regle-generique
description: Appliquer une règle générique (harness, doctrine, convention) sans juger si elle sert le contexte = conformité aveugle, que "scan aveugle interdit" condamne aussi pour les workflows. Quand une garde refuse une action, diagnostiquer son INTENTION (lire settings/code) avant de contourner ou de la "corriger".
metadata:
  type: feedback
---

Une règle générique appliquée par réflexe — sans se demander si elle sert le contexte réel — est de la conformité aveugle. C'est le pendant workflow de « scan aveugle interdit » : le jugement contextuel ne se suspend pas parce qu'une règle existe.

**Why:** 27 mai 2026, fin Chantier C. (1) J'ai créé une branche feature + PR pour un chantier solo 100% testé, par application mécanique du défaut harness « branch first » + caveat CLAUDE.md, sans juger que la PR review est un cérémonial vide en repo mono-utilisateur. (2) Quand `git merge` a été refusé, j'ai d'abord cru à une garde subie — la lecture des settings a révélé que `git merge *` est en **deny global intentionnel** (gate d'intégration humain voulu). Le pattern « branche + merge humain » n'était pas un bug à corriger mais un design à expliciter. Mon premier réflexe (inverser la règle) aurait cassé une cohérence que j'avais oublié de diagnostiquer.

**How to apply:** Avant d'appliquer OU de « corriger » une règle de workflow : (a) juger si elle sert le contexte réel (solo vs équipe, trivial vs risqué) — l'appliquer consciemment, pas par réflexe ; (b) si une garde (hook/deny/permission) refuse une action, LIRE sa définition (settings, code du hook) pour comprendre son intention AVANT de contourner ou de proposer de la changer. Une garde refusée est souvent intentionnelle. Le bon fix est alors d'**expliciter** la règle (pour que le réflexe devienne conscient), pas de l'inverser. Lien : [[comment-creer-hook]] (distinction garde hook vs harness), [[pattern-vault-source-unique-sync-mecanique]].
