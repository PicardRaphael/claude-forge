---
name: regex-lookahead-greedy-trap
description: "Bug regex récurrent — \\s* greedy + lookahead négatif laisse passer faux positifs par backtrack. Forcer position avec [ \\t]+ avant lookahead."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Quand un regex combine `\s*` (greedy, peut matcher 0 char) suivi d'un lookahead négatif, le moteur regex backtrack : si `\s*` matche 0 char, le lookahead vérifie l'ESPACE lui-même, qui n'est généralement pas dans la blacklist → faux positif garanti.

**Cas concret 24 mai 2026** :
```python
# BUG : laisse passer "Source : `code`" comme s'il était attribution
re.compile(r"(?m)^\s*Source\s*:\s*(?![`<{]|\[(?!\[))", re.IGNORECASE)

# FIX advisor : [ \t]+ force au moins 1 espace, lookahead sur vrai caractère suivant
re.compile(r"(?m)^[ \t]*Source\s*:[ \t]+(?![`<{]|\[(?!\[))", re.IGNORECASE)
```

**Why :** `\s*` étant greedy avec backtrack autorisé, le moteur essaie tous les match possibles : `\s*` matche 3 espaces (lookahead voit `` ` ``, négatif OK donc no match) PUIS `\s*` matche 2 espaces (lookahead voit espace, négatif OK donc MATCH faux positif). Le backtrack trouve un match là où on n'en voulait pas.

**How to apply :**
- Si lookahead négatif suit un quantifieur sur espace → utiliser `[ \t]+` (au moins 1, restreint au type d'espace voulu)
- Tester avec un set d'inputs `expected_pass` ET `expected_block` AVANT de déployer le regex
- Utiliser `re.DEBUG` ou un script standalone de test pour valider isolément
- Si possible : éviter `\s*` AVANT un lookahead — préférer `[ \t]*` (sans backtrack vertical) ou ancrage strict
- Pour les cas d'enforcement (hook bloquant), tests adverses obligatoires sur les 2 directions (pass + block)

**Pattern méta :** "le regex passe les tests existants mais foire en prod" = très souvent un backtrack imprévu sur quantifieur greedy. Première chose à vérifier.
