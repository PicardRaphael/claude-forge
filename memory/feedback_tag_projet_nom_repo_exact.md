---
name: tag-projet-nom-repo-exact
description: Tag projet = nom EXACT du repo (séparateur compris), jamais de normalisation cosmétique — vérifier le nom réel avant fusion
trigger: tag, nom du repo, projet, separateur, normaliser
metadata:
  type: feedback
---

Un tag `#projet/*` doit matcher le **nom réel du repo** (disque + remote git), pas une normalisation cosmétique du séparateur. Les repos officiels portent un underscore : `neo_ia`, `ia_back` (noms Bitbucket/disque). Le repo forge porte un tiret : `claude-forge` (vérifié `git remote` : `github.com/PicardRaphael/claude-forge`).

**Why :** un tag projet sert à retrouver les notes d'un repo précis. S'il diverge du nom réel (tiret vs underscore), il fragmente la navigation et casse l'alignement tag↔repo. Le séparateur n'est pas cosmétique : il fait partie du nom officiel.

**How to apply :** avant toute fusion de tags projet, vérifier le nom réel (`ls` disque + `git remote -v`), PUIS figer la forme canonique sur ce nom — jamais sur le count ni sur une convention kebab-case générique. Les tags `#domaine/*` (thèmes, pas des repos) restent en tiret (convention existante). Décidé chantier 2/5 normalisation tags forge-brain (7 juin 2026). Cf [[localiser-repos-avant-workflow-multi-repo]], [[brief-premisse-fausse-verifier-avant-executer]].
