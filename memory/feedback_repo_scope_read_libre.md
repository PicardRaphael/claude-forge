---
name: repo-scope-read-libre-write-marker
description: "Politique repo-scope-guard 26 mai 2026 — lecture cross-repo LIBRE depuis ia_back et neo_ia, écriture garde marker. Plus de phrase magique pour read."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 542ed2f8-3b74-4f92-b60a-c856ec65b44f
---

Depuis 2026-05-26, les hooks `repo-scope-guard.ts` (ia_back) et `repo-scope-guard.py` (neo_ia) ont une politique assouplie :

- **Read/Grep/Glob/Bash read** sur tout neot-v2/ (bdd, neofront, lojii, etc.) = **libre, sans marker, sans phrase magique**
- **Write/Edit/MultiEdit** :
  - repo courant = libre
  - cross ia_back ↔ neo_ia = interdiction absolue (doit se faire depuis le bon repo)
  - autres repos = marker `.repo-auth-<repo>` requis (créé via "regarde X" / "check X" / "autorisé X")

**Why:** Raphael veut consulter bdd / autres repos depuis ia_back ou neo_ia sans friction. Les phrases magiques bloquaient des consultations légitimes (vérifier schéma bdd, lire neofront). La sécurité est sur l'écriture, pas la lecture.

**How to apply:**
- Si user demande "regarde X" / "check X" et qu'il s'agit juste de lecture → plus besoin, c'est déjà autorisé
- Si user veut écrire dans un repo voisin (hors ia_back/neo_ia cross) → la phrase magique reste nécessaire pour créer le marker
- Si on touche à la doctrine cross-repo write, propager aux DEUX hooks (ts + py) pour rester symétrique

Lié : [[critique-2026-05-24-regex-source-faux-positifs]]
