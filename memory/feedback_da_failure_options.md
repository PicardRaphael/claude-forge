---
name: da-failure-decision-protocol
description: "DA fail (529, timeout, output vide) → relancer 1×, sinon advisor fallback, sinon STOP. Jamais livrer sans verdict"
metadata:
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Cf [[erreur-devils-advocate-tronque]] (doctrine canonique vault — bug structural surcharge contexte + annonce malhonnête).

**Protocole résumé 3 options ordre** :
1. Relancer DA 1 fois (5 min plus tard)
2. Invoquer advisor comme remplacement (voit conversation complète)
3. STOP livraison : commit WIP, capitaliser draft, finir en session dédiée

**Cas Windows PowerShell heredoc 22 mai** : DA tourne 15-20 min, retourne fragment shell au lieu de critique → le `resume:` frontmatter contient souvent un verdict utile même quand le body est vide. Fix systémique : prompt explicitement DA à utiliser `mcp__forge-brain__create_note`.

**Override conscient** : si user dit "fais tout commit push" sans verdict DA valide → signaler explicitement "DA n'a pas validé, advisor recommandait STOP, tu confirmes override ?". Absence de verdict ≠ verdict positif.
