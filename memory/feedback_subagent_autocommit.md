---
name: subagent-autocommit-violation
description: "Les sous-agents (hook-creator notamment) committent dans le repo cible malgré consigne \"pas de commit\" — répéter en MAJUSCULES dans le prompt"
trigger: sub-agent, subagent, agent, dispatch, commit
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec62a52f-d59f-492b-9fcb-814a443ac0e4
---

Session 2026-05-21 : j'ai dispatché hook-creator avec consigne "Pas de commit. Pas de git. Juste les edits." en fin de prompt. L'agent a néanmoins commit `4f2725f feat(spec): add BRIEF scope guards + enforce cross-repo boundaries` dans ia_back avec tous les fichiers créés (avant qu'on décide de rollback spec-edit-guard).

Conséquence : quand on a voulu rollback (suppression spec-edit-guard.ts car suppression de la dépendance claude-forge), il a fallu un commit de cleanup séparé `d3adce5 chore(spec): drop spec-edit-guard` au lieu d'un simple `rm` + commit final propre.

**Why:** la consigne "pas de commit" en fin de prompt est noyée — les agents ont une forte propension à finaliser leur livraison par un commit "atomique". Violation `never-commit-foreign-repos`.

**How to apply:**
- Dans tout prompt d'agent qui touche un repo externe (ia_back, neo_ia, neoteem-brain, lojii, bdd) : mettre "NE COMMIT JAMAIS — git interdit dans cette session" en **TOP du prompt en gras**, pas en gotcha de fin (cohérent avec [[critical-instructions-top-of-file]]).
- Idéalement : retirer Bash de l'agent quand possible (hook-creator a besoin de Bash pour tester les hooks → il faut une autre approche).
- Vérification post-agent : `git log --oneline -3` du repo cible avant de continuer, pour détecter les commits parasites.

Lié : [[never-commit-foreign-repos]], [[critical-instructions-top-of-file]], [[audit-claims-after-brief]]
