---
name: merge-ref-morte-croisee
description: Merge de branches divergentes — vérifier la CONVERSE (un côté référence-t-il un fichier que l'autre supprime/archive ?), une réf morte qu'aucune branche seule n'avait
trigger: merge, branche, develop, main, reference morte
metadata:
  type: feedback
---

Lors d'un merge de branches divergentes où un côté **supprime/archive/renomme** des fichiers et l'autre **ajoute des références** (dans un index, une rule, un CLAUDE.md, une note), le merge peut créer une **référence morte qu'aucune branche seule ne contenait** — c'est le seul risque proprement *merge-spécifique*, invisible en regardant chaque branche isolément.

**Why:** `git merge` fusionne le contenu textuellement mais ne valide aucune cohérence sémantique cross-fichiers. Chaque branche est cohérente en soi (branche A retire le fichier X + retire ses pointeurs ; branche B ajoute un pointeur vers un fichier vivant Y). Mais si B ajoute un pointeur vers X pendant que A archive X, le résultat fusionné pointe vers un fichier absent. `commit-push-check` (status + diff) ne l'attrape pas ; `zero-dette-technique` traite une réf morte *trouvée*, pas une réf morte *née du merge*.

**How to apply:** avant de commiter un merge, faire les DEUX sens :
1. Sens direct — les pointeurs ajoutés par un côté ciblent-ils des fichiers vivants ? (déjà réflexe naturel)
2. **Converse** — aucun des commits de l'AUTRE côté n'introduit-il une référence vers un fichier que ce côté-ci supprime/archive ? Grep les stems supprimés/archivés dans les fichiers touchés par l'autre côté (`git diff <merge-base>..<autre-côté> --name-only` puis grep). 30 s, coût quasi nul.

Découvert via advisor pendant le merge `worktree-clean-memory-2026-07` → `main` (2026-07-13) : branche archivait 64 fichiers memory, main ajoutait 2 pointeurs. Cas clean ici (les 2 pointeurs de main ciblaient des fichiers neufs sans rapport), mais le check était l'angle mort de mon auto-vérif. Cf [[feedback_commit_push_check]] + [[feedback_zero_dette_technique]].
