---
name: edit-tool-read-obligatoire-meme-en-parallele
description: "Edit tool EXIGE Read préalable du fichier, même si l'Edit est lancé en parallèle avec d'autres tools"
trigger: Edit, MultiEdit, parallele, batch, Read
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 02a72a18-03e9-497d-9fbe-ea0961ddfa79
---

Le tool `Edit` retourne `File has not been read yet. Read it first before writing to it.` si le fichier n'a pas été lu dans la session courante, **même quand l'Edit est lancé en parallèle avec d'autres tools dans le même message**.

Erreur ia_back 25 mai 2026 : tentative de 8 Edit en parallèle sur 8 skills différentes pour raccourcir descriptions → 7/8 ont échoué (1 seul ayant été lu par hasard avant). J'ai dû re-Read les 7 puis ré-Edit, doublant le nombre de round-trips.

**Why:** le harness Claude Code vérifie le file state PAR fichier. Les tool calls en parallèle dans un seul message N'autorisent PAS Claude à voir les résultats des autres avant la fin du batch — donc 8 Edit en // sans Read préalable = 7 failures garanties.

**How to apply:**
- Batch Edit multi-fichiers : faire un batch Read EN PREMIER (tous les fichiers en //), puis batch Edit en //
- Pour un seul fichier : Read implicite dans le même message OK
- Si tu vois "File has not been read yet" : Read le fichier, re-tente l'Edit, pas la peine de re-essayer en // après
- Note : ne s'applique PAS à Write (qui peut créer un fichier sans Read) ni à MultiEdit sur 1 seul fichier déjà lu
