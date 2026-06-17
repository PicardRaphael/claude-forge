---
name: changer-mecanisme-lire-tests-qui-verrouillent
description: Avant de changer un MÉCANISME ou un contrat dans un fichier (canal de lecture, présence d'un import, signature, valeur loggée), lire les TESTS qui le verrouillent — pas seulement le fichier modifié. Un test patche/grep souvent l'ancien mécanisme et casse en silence.
metadata:
  type: feedback
---

Quand une modification change le **mécanisme** ou le **contrat observable** d'un fichier (pas juste sa logique interne), des tests ailleurs peuvent le verrouiller et casser — y compris des tests qui ne testent PAS le sujet modifié. Lire le fichier édité ne suffit pas : il faut lire ses **tests** AVANT de changer le mécanisme.

**Why :** 2026-06-17, fix Langfuse neo_ia. J'ai changé le canal de lecture du statut (`os.getenv(...)` → `get_config().is_configured()`) et retiré `import os` de neodoc/main.py (devenu mort). Fonctionnellement correct (prouvé : `is_configured()` = True). Mais ça a cassé **9 tests** : 8 patchaient `neodoc.main.os.getenv` (dont 6 comme effet NEUTRE, sans rien à voir avec Langfuse — startup, flush, checkpointer) → `AttributeError: module has no attribute 'os'` ; 1 grepait `"LANGFUSE_PUBLIC_KEY" in source` de main.py (anti-régression mono-projet) → la mention littérale avait disparu. `/go` (give-Claude-a-way-to-verify) les a rattrapés, mais j'aurais dû les voir AVANT en lisant `test_main.py` du fichier que je modifiais.

**How to apply :** avant de changer un mécanisme/contrat dans `X.py`, grep ses tests pour les 3 dépendances fragiles — (1) `patch("X.<attr>")` / `mock.patch.object(X, ...)` (un patch cible un nom ; retirer ce nom casse le patch, même si le test ne teste pas ce nom) ; (2) `read_text()` / grep du source de X (tests structurels qui vérifient la présence/absence d'un symbole littéral) ; (3) imports du module (`from X import Y` côté test). Si l'un existe → adapter le test dans le même changement, en préservant son INTENTION (un test « neutre » qui patchait os.getenv pour l'effet → patcher la nouvelle source neutre ; un test anti-régression qui grepait une clé → vérifier le nouveau canal, pas l'ancien symbole). Distinct de [[edit-tool-read-obligatoire-meme-en-parallele]] (lire le fichier édité) et de [[regression-diagnostic-diff-avant-redesign]] (diagnostiquer une régression déjà là) : ici on ANTICIPE la casse de tests d'un changement de mécanisme.
