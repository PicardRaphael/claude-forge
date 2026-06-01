---
name: zip-import-slash-pas-compress-archive
description: "Zip d'import (skill Cowork) = slashes. Compress-Archive met des backslashes → casse"
metadata:
  type: feedback
---

Pour produire un zip importable (skill/plugin Cowork, ou tout zip lu en POSIX), `Compress-Archive`
PowerShell écrit des **backslashes** dans les chemins (`dossier\fichier`) → l'extracteur POSIX/Cowork
voit un fichier nommé `dossier\fichier` au lieu d'une arborescence → import cassé. Utiliser
`System.IO.Compression.ZipFile` en remplaçant `\`→`/` dans chaque entrée. Toujours vérifier
`unzip -l` avant de livrer.

**Why:** Session 1er juin 2026 — premiers `.skill` produits avec Compress-Archive avaient des
backslashes ; auraient cassé l'import Cowork. Rattrapé après vérification.
**How to apply:** tout packaging zip sous Windows destiné à un import/extraction non-Windows.
