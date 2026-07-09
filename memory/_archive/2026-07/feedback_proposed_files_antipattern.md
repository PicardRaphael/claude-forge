---
name: proposed-files-antipattern-supprimer-apres-application
description: "Fichiers `.proposed` (ex: settings.json.proposed) = transitoires d'instructions. Toujours supprimer après application, ne PAS laisser polluer le repo."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Quand un sub-agent ou la session ne peut pas modifier un fichier protégé (auto-mode classifier, delegate-guard), il génère parfois un fichier `.proposed` avec des instructions de copier-coller. Ce fichier est TRANSITOIRE — à supprimer dès que l'application réelle a eu lieu.

**Why :** `.proposed` files restés en place créent :
- Confusion sur l'état réel (le settings.json ou le .proposed est la source de vérité ?)
- Pollution git (fichier inutile commité par erreur)
- Drift documentaire (les instructions du .proposed deviennent obsolètes au prochain change settings)

Observé 24 mai 2026 : `settings.json.proposed` créé par hook-creator pour l'entrée `meta-commentary-detector`. Après application réussie (auto-mode classifier a laissé passer), le `.proposed` n'avait plus de raison d'être.

**How to apply :**
- Après application réussie du contenu d'un `.proposed` → `rm <fichier>.proposed`
- Commit dans le même commit que l'application : "apply X + cleanup .proposed"
- Si auto-mode classifier ré-bloque dans une future session → re-générer un `.proposed` à la volée, ne pas laisser le précédent traîner
- Préférer toujours essayer l'édition directe AVANT de générer un `.proposed` — auto-mode classifier laisse passer les additions hooks bien formées
- Pattern alternatif : pour les modifs settings non-bloquées, éditer direct sans passer par .proposed
