---
name: capitaliser-methode-pas-que-resultat
description: Après un chantier réussi, capitaliser la MÉTHODE réutilisable (recette de déploiement, routage dans la skill créatrice) — pas seulement le RÉSULTAT (note de design). Sinon un futur repo re-réinvente l'ordre des opérations et les pièges.
metadata:
  type: feedback
---

Quand un chantier produit un design qui sera redéployé ailleurs (ex : relais /feature sur neo_ia + neoteem-back-ts, 2026-06-16), capitaliser le RÉSULTAT (la note de design dans le vault) ne suffit PAS. Il faut aussi capitaliser :

1. **La MÉTHODE de déploiement** — l'ordre des opérations + les pièges qui ont rendu le chantier propre (ex : lire les formats réels avant de trancher, grep REPO-WIDE pas seulement `.claude/`, adapter pas copier, ne pas détracker les livrables durables). Foyer : enrichir la note de design elle-même (search-then-enrich), pas une note orpheline.
2. **Le ROUTAGE dans la skill créatrice** — pour que le besoin soit CAPTÉ quand l'user le formule. Ex : si l'user dit « mémoire entre agents », `subagent-creator` doit désambiguïser et router vers le hub, sinon il répond à côté (`memory: project`).

**Why :** observé 3× dans la même session (16 juin). À chaque fois Raphael a dû pousser pour combler l'écart entre « ce qu'on a fait » et « ce qui est réutilisable/découvrable » : (a) le grep s'arrêtait à `.claude/` → cf [[verify-exhaustive-claims]] ; (b) « tout est dans tes notes pour qu'un futur repo soit top ? » → le design était capitalisé, la méthode non ; (c) « ça doit matcher si je parle mémoire entre agents » → le sujet n'était pas capté par la skill créatrice. Le résultat seul laisse un futur moi (ou un collègue) re-réinventer l'ordre des opérations et retomber dans les pièges.

**How to apply :** à la fin d'un chantier redéployable, se poser 2 questions AVANT de déclarer fini — (1) « un futur repo aurait-il la RECETTE, pas juste le résultat ? » → sinon enrichir la note de design d'une section « Déployer sur un nouveau repo ». (2) « si l'user FORMULE ce besoin, une skill créatrice le capte-t-elle et le route-t-elle ? » → sinon ajouter la question d'interview + le gotcha de routage. Distinct de [[proactive-references-extraction]] (déporter du volume) : ici on capture l'ACTIONNABILITÉ et la DÉCOUVRABILITÉ, pas le rangement.
