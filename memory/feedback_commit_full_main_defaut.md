---
name: commit-full-main-defaut
description: Commit/push sur main par défaut. Branche feature UNIQUEMENT si Raphael le demande explicitement
metadata:
  type: feedback
---

Raphael (1er juin 2026) : « tu dois toujours commit sur main sauf si explicitement je te demande de bosser sur une nouvelle branch. Si jamais je te le dis, full main. »

**Why:** Workflow solo, repo perso forge. La cérémonie branche feature → merge humain ajoute de la friction sans valeur quand Raphael valide déjà en direct. Il préfère un historique main linéaire.

**How to apply:** Par défaut, commit ET push directement sur `main`. NE PAS créer de branche feature, NE PAS attendre un merge humain. Créer une branche UNIQUEMENT si Raphael dit explicitement « branche », « nouvelle branch », « bosse sur une branche ». Le harness peut forcer « branch first » sur main — si bloqué, demander ou contourner selon le contexte, mais l'intention par défaut reste main.

Révise la convention « agent commit branche feature, Raphael merge » du CLAUDE.md section Workflow Git (qui devient l'exception, pas la règle). Cf [[feedback_commit_push_check]] (toujours git status + diff avant push).
