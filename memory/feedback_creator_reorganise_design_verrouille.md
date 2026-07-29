---
name: creator-reorganise-design-verrouille
description: Un agent créateur (skill-creator/agent-creator) réorganise/dilue un design déjà verrouillé avec l'utilisateur. Vérifier empiriquement le livrable bloc par bloc vs design validé.
trigger: skill-creator, subagent-creator, design, verrouille, reorganise
metadata:
  type: feedback
---

Quand on délègue à `skill-creator` (ou `agent-creator`) une création dont la **structure a été verrouillée avec l'utilisateur** (blocs ordonnés, contenu doctrinal précis), le créateur tend à **réinterpréter et réorganiser** au lieu de suivre verbatim — même avec un brief détaillé.

**Cas observé (5 juin 2026, skill `loop-forge`)** : design = 9 blocs ordonnés validés question par question avec Raphael. skill-creator a livré un SKILL.md qui : (1) fondait le bloc JOB dans le CONTEXTE, (2) supprimait l'explication des 3 types de loop (cœur doctrinal), (3) faisait disparaître la règle READ/WRITE cross-repo du SKILL.md, (4) diluait la vérification "obligatoire bloquante" (tip #1 Boris) dans l'observabilité. Les 4 écarts portaient précisément sur les points les plus discutés.

**Why** : le créateur optimise pour "une bonne skill générique" selon ses canoniques, pas pour "CE design précis". Plus le design est arrêté en amont, plus l'écart est coûteux (on perd le travail de cadrage).

**How to apply** :
1. Dans le brief : numéroter les blocs, dire explicitement "ordre et contenu validés avec l'utilisateur, ne pas réinterpréter ni fusionner".
2. TOUJOURS vérifier empiriquement le livrable **bloc par bloc vs design validé** (Read du fichier réel, pas le résumé du sub-agent — cf [[auditor-empirical-verify]]). Le résumé du créateur disait "9 blocs séquentiels" alors que 4 blocs étaient déviés.
3. Renvoyer corriger via SendMessage avec les écarts précis plutôt que ré-spawner.

Lié : [[subagent-autocommit-violation]] (sub-agents dévient des instructions), [[erreur-vault-jamais-consulte-session-principale]] (vérif empirique après créateur), feedback edit-tool-read-obligatoire.
