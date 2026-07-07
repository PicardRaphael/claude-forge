---
name: diff-crlf-faux-positif-audit
description: Auditer des copies de fichiers cross-repo Windows = md5sum/diff crient DIFFÉRENT sur du contenu identique (CRLF vs LF). Re-diff avec --strip-trailing-cr avant tout verdict de divergence.
metadata:
  type: reference
---

Quand on compare des copies d'un même fichier entre repos sur Windows (audit de drift, vérif de synchro), `md5sum` et `diff` bruts crient **« DIFFÉRENT » / `1,Nc1,N` (toutes lignes)** alors que le **contenu est identique** — seul l'encodage des fins de ligne diffère (un repo en LF, l'autre en CRLF, selon `core.autocrlf` / l'outil qui a écrit).

**Le piège de jugement (vécu 26 juin, audit skill /spec ×3 repos) :** un MD5 « DIFFERENT » sur 13/14 references m'a fait conclure « les references divergent → c'est la cause du bug ». Re-diff avec `diff --strip-trailing-cr` : **0 ligne de diff réel** sur 12/13. La divergence était un artefact CRLF, pas du contenu. Conclure sur le MD5 brut = faux diagnostic.

**Réflexe avant TOUT verdict de divergence/synchro :**
1. `file <a> <b>` → repère « with CRLF line terminators » d'un côté seulement.
2. Re-comparer en neutralisant les EOL : `diff --strip-trailing-cr a b` (ou `git diff --ignore-cr-at-eol`, ou normaliser avant `md5sum`).
3. Le verdict « identique / divergent » se prononce sur le diff EOL-neutre, jamais sur le MD5/diff brut.

Symétrique du write-path : [[decision-byte-for-byte-splice-test-live]] (la couche IO Python `write_text` TRADUIT `\n`→`\r\n` à l'écriture). Ici c'est le READ/COMPARE-path qui ment. Même racine (EOL Windows), deux moments différents : l'un casse l'écriture byte-exact, l'autre casse l'audit de comparaison.
