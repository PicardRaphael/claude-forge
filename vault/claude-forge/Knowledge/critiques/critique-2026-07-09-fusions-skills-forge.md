---
titre: "Critique — Plan de fusions de skills forge (forge-review 9 juil.)"
resume: "DA sur plan 5 fusions skills forge : F2 BLOCKING (moins réversible, mal tiéré), F4 sort du plan (KILL-vs-keep), F5 mauvais foyer (NOT-clause), F1/F3 SHIP conditionnels"
aliases:
  - "critique fusions skills 9 juillet"
  - "DA plan fusion skills forge"
  - "critique F1 F2 F3 F4 F5 skills"
  - "fusion trio doctrine pivot-check"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-09
auteur: claude
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---

# Critique — Plan de fusions de skills forge

Cadre du jugement (Raphael) : **performance de déclenchement > budget tokens**. Une fusion n'est acceptable que si le routing s'améliore OU reste intact. Budget listing = motif secondaire.

## Verdict par item

| Item | Verdict | Score | Une ligne |
|---|---|---|---|
| F1 cc-rag-ref → rag-design/references/ | **SHIP** (1 verify) | 45 | Fold le plus propre (0 trigger), vérifier que rag-design ne force pas le dialogue guidé sur une requête debug |
| F2 trio doctrine → skill à modes | **BLOCKING** | 80 | Item le MOINS réversible placé dans le tier committed ; surface de migration élevée ; measure-first (précédent revirement) |
| F3 web-search-canonical → rule | **SHIP** (fix lean) | 35 | Doctrine toujours-vraie = rule (application 100 %) est juste ; distiller la doctrine, pas dumper la procédure |
| F4 python-script-refactor-masse → python-ref | **FIX (sortir du plan)** | 70 | Décision KILL-vs-keep déguisée en fusion ; viole le critère prime par aveu de l'auteur ; mal domicilié |
| F5 cc-prompt-ref → craft-prompt/references/ | **FIX (mauvais foyer)** | 65 | craft-prompt DISCLAIME les composants CC = exactement le domaine de cc-prompt-ref ; triggers mal re-routés |
| « aucun KILL » | **NOTE** | 40 | La cible F4 EST le vrai candidat KILL qu'on évite |

BLOCKING : 1 (F2) · FIX : 2 (F4, F5) · SHIP conditionnel : 2 (F1, F3).

**Décision recommandée : LIVRER AVEC CORRECTIONS** — re-tiérer (F2 hors committed) + revoir F4/F5 avant présentation arbitrage.

## Réponses aux 3 questions posées

**(a) Une fusion à modes dégrade-t-elle le déclenchement vs 3 descriptions spécialisées ?**
Pas au niveau du *firing* SI le trio réutilise `triggers_by_subject` (précédent `forge-brain` dans `.skill-triggers.json` : phrase → sujet/mode). Les triggers FR déterministes restent déterministes. La dégradation réelle est ailleurs : (1) auto-invocation depuis la DESCRIPTION — une seule desc ≤250 chars doit couvrir 3 intentions, la densité de mots-clés par intention chute ; (2) 3 MOMENTS de déclenchement distincts (finding arrive / décision de pivoter / après édition canonique) collapsent dans une skill qui doit s'auto-router. Net : firing intact si `triggers_by_subject`, mais la sélection-de-mode sur auto-invoke est une surface d'échec NEUVE, non prouvée neutre → mesurer.

**(b) F3 : la doctrine perdue en tant que skill listable est-elle mieux servie en rule ?**
Oui. Les rules sont TOUJOURS chargées (application 100 %), les skills sont probabilistes (trigger). Pour une doctrine toujours-vraie (« préférer la source canonique »), la rule est strictement meilleure pour l'APPLICATION. La « listabilité » perdue n'est pas une vraie perte : on n'invoque pas une doctrine, on l'applique. Deux gardes : distiller la doctrine seule (pas de checklist procédurale qui bloaterait le contexte toujours-chargé) ; garder le fold à 2-3 lignes (coûte des tokens sur CHAQUE tâche alors qu'elle n'est pertinente qu'en recherche externe).

**(c) Risques de migration.**
- **F2** (le plus lourd) : golden-set validator (deps de chemins dans scripts/), remap du slash-command `/pivot-check` vers un mode, reconstruction `.skill-triggers.json` en `triggers_by_subject`, fusion de 3 bodies, ET réécriture des cross-refs — `[[methode-pivoter-doctrine]]` et `pivot-check` sont référencés dans `devils-advocate-pipeline.md`, `comportement-proactif.md`, `sequence-canonique-modification.md` + canoniques vault. Fusionner casse ces wikilinks/lignes de table s'ils ne sont pas tous mis à jour. Précédent direct : `critique-2026-05-21-refonte-hooks-16-vers-6` — « fusion triplet impossible = 3 bugs demain matin ».
- **F5** : remap des triggers `.skill-triggers.json` + réécriture de la route `comportement-proactif` (« Amélioration de prompt / description → cc-prompt-ref ») qui n'a AUCUNE destination valide post-fold (craft-prompt disclaime le domaine) + vérifier les skills créatrices qui consomment cc-prompt-ref.
- **F1** : minimal (0 trigger). Seule vérif : rag-design branche-t-il servir-référence vs lancer-dialogue.

## Angle réversibilité (angle manquant du plan)

Le plan tiére F1-F3 committed / F4-F5 option, mais ne classe pas par RÉVERSIBILITÉ — ce dont Raphael a besoin pour arbitrer un plan try-and-measure :
- F1 / F4 / F5 → fold dans `references/` = **cheap à annuler** (remettre le fichier, restaurer la desc). Safe à tester-mesurer.
- F3 → skill→rule = modéré (annuler = recréer la skill).
- F2 → 3 skills → 1 + golden-set migré + slash-command remap = **coûteux à annuler**.

**Ceci inverse le tiering du plan** : F2 est dans le tier committed mais est le MOINS réversible. Recommandation : livrer les collision-fixes réversibles (F1, F5 corrigé) + F3, MESURER listing + déclenchement, PUIS décider F2. C'est honorer le précédent revirement au lieu de seulement le citer.

## Budget — mécanisme réel

Le gain budget est réel mais PAS par « moins d'entrées sous 2k » : les fichiers `references/` n'apparaissent PAS dans le listing. Chaque fold retire une entrée entière du listing, quel que soit le total. Angle qui le renforce : les skills foldées sont les MOINS utilisées = exactement celles que CC droppe en premier. Les folder dans une référence fiablement chargée PROTÈGE leur contenu du drop. C'est le vrai gain, à formuler ainsi.

## Si je devais le faire marcher

1. **F2** : sortir du tier committed → tier « measure-first ». Avant tout : lire le validateur golden-set + lister TOUS les backlinks des 3 stems (rules + vault). Construire `triggers_by_subject` (calqué forge-brain). Décider comment `/pivot-check` mappe à un mode. Puis A/B trigger via outcomes-test/fixtures AVANT commit. Réversibilité documentée.
2. **F4** : retirer de la liste des fusions. Trancher explicitement KILL (0 ref + 0 trigger = mort) OU keep+fix-triggers. Le fold dans python-ref est le pire des deux (anti-pattern language-agnostic mal domicilié dans une skill « avant d'écrire du Python »).
3. **F5** : ne PAS folder dans craft-prompt (disclaime le domaine). cc-prompt-ref = infra partagée des créateurs → soit keep, soit home dans skill-creator/references partagé. Grep les consommateurs d'abord.
4. **F1** : SHIP après vérif branche debug/dialogue de rag-design.
5. **F3** : SHIP en distillant 2-3 lignes de doctrine pure dans contenu-externe-non-fiable.md.

## Vault — historique pertinent

- `raisonnement-revirement-pipeline-mai-2026` : fusion déjà ANNULÉE dans forge quand la mesure a montré gain modeste vs risque élevé (measure-before-optimize). S'applique directement à F2.
- `critique-2026-05-21-refonte-hooks-16-vers-6` : « fusion triplet impossible = 3 bugs demain matin » — précédent sur la fusion de composants pipeline tightly-coupled. Directement analogue au trio F2 (golden-set + slash-command + cross-refs).
- `e-descriptions-keyword-stuffing` : densité de mots-clés par intention dans les descriptions — soutient l'argument (a) sur la dilution en desc fusionnée.
