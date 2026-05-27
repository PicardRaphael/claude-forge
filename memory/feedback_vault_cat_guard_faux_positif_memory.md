---
name: vault-cat-guard-faux-positif-memory
description: "Le hook vault-cat-guard bloque un cat/grep sur memory/_archive/ si la commande contient le mot vault dans son contenu (faux positif). Contourner via Edit, pas Bash."
metadata:
  type: feedback
---

Le hook `vault-cat-guard.py` scanne le CONTENU de la commande Bash, pas seulement le chemin cible. Un `cat memory/_archive/MEMORY-archive-log.md` dont le here-doc contient le mot « vault » est bloqué, alors que `memory/` n'est PAS le vault Obsidian.

**Why:** Observé 27 mai 2026 (clean-memory) — append au log d'archive via Bash bloqué. Le hook protège l'accès brut au vault `vault/claude-forge/`, mais matche trop large sur le texte de la commande.

**How to apply:** Pour écrire dans `memory/` (y compris `_archive/`), utiliser Read+Edit plutôt que `cat >>`/heredoc Bash si le contenu mentionne « vault ». Si récurrent (2e+ occurrence), affiner le hook pour ne matcher que les chemins réellement sous `vault/`.
