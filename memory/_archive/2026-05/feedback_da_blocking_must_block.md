---
name: da-blocking-must-block-pre-ship
description: "Verdict DA \"BLOCKING\" doit bloquer le ship/promulgation, pas être noté pour plus tard"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f400e641-e24e-449a-8544-745efaea81ec
---

Quand un devils-advocate retourne BLOCKING >= 1, NE PAS shipper / promulguer / commiter la doctrine tant que chaque BLOCKING n'est pas (a) résolu par fix dans la même session, ou (b) explicitement acté comme "accepté avec dette documentée" par Raphael — pas par moi seul.

**Why** : Self-audit 24-25 mai 2026 a révélé que la doctrine meta-commentaires a été promulguée (commits 74916cd + 7614f51 + hook enforcement) malgré BLOCKING 1 du DA = "claude-forge/CLAUDE.md viole déjà la règle, 7 infractions L3/L51/L54/L55/L74/L87/L99". Doctrine appliquée aux nouveaux composants mais référence en violation = drift garanti dans 2 semaines. C'est exactement [[feedback_doctrine_drift_pattern]] qui se reproduit malgré son existence en mémoire. Le DA est un théâtre s'il ne bloque pas.

**How to apply** : après chaque appel devils-advocate, parser le verdict.
1. Si "BLOCKING >= 1" : lister les BLOCKING au user en clair
2. Pour chaque BLOCKING : proposer fix immédiat OU acceptation explicite avec note "dette" documentée
3. NE PAS commit/ship/promulguer avant arbitrage explicite du user
4. PARTIAL fix d'un BLOCKING = encore PARTIAL, pas PASS — ne pas s'auto-congratuler
5. Si Raphael dit "ship quand même", créer note vault `Knowledge/dettes/` documentant la dette acceptée

Lié à [[feedback_doctrine_drift_pattern]] (même pattern, niveau supérieur) et `.claude/rules/devils-advocate-pipeline.md` (à amender : ajouter section "Que faire d'un BLOCKING").
