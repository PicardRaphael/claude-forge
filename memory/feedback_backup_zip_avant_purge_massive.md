---
name: backup-zip-avant-purge-massive
description: "Avant toute purge > 50 fichiers, Compress-Archive .zip defensif. 303 KB pour 240 fichiers = cout zero, securite totale"
metadata:
  type: feedback
---

Avant toute purge massive (>50 fichiers) ou refonte de structure dossier (auto-memory, vault folder, .claude/skills entier), creer un backup .zip dans le repo (versionne ou gitignore) AVANT l'action destructive.

**Why** : 28 mai 2026 Step 1 audit context — purge 240 fichiers auto-memory user-scope. Backup `_auto_memory_backup_pre_purge_2026-05-28.zip` = 303 KB pour 240 fichiers. Cout disque negligeable, possibilite de restaurer instantanement en cas d'erreur d'arbitrage. Aucun regret n'est arrive, mais le filet a permis de purger sans hesitation.

**How to apply** : `Compress-Archive -Path "<dir>\*" -DestinationPath "<repo>/memory/_<purge-name>_backup_<date>.zip" -Force` AVANT `Remove-Item -Recurse -Force`. Nommer `_<x>_backup_<date>.zip` pour rester en tete de liste alphabetique. Supprimer le backup apres 7-30 jours sans regret.
